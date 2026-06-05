-- vw_gross_revenue_churn
-- Board Gross Revenue Churn (GRC), per the locked retention contract v1.0.
-- Inherited from the data team; the style is theirs.

CREATE VIEW vw_gross_revenue_churn AS
WITH period_close AS (
    -- only fiscal periods past the 5-business-day close freeze (final, reportable)
    SELECT fiscal_period_id, period_start_pt, period_end_pt
    FROM fiscal_calendar
    WHERE close_frozen_at IS NOT NULL
),
cohort_mrr AS (
    -- start-of-period billing MRR for PAID accounts active at period start
    SELECT
        pc.fiscal_period_id,
        b.account_id,
        b.mrr_usd AS start_mrr
    FROM period_close pc
    JOIN billing_mrr_daily b
      ON b.as_of_date = pc.period_start_pt            -- billing snapshot stored in US/Pacific
    WHERE b.plan_type = 'paid'                         -- trials/free excluded per contract
      AND b.mrr_usd > 0
      AND b.account_id NOT IN (SELECT account_id FROM governed_exclusions)  -- governed table, reasoned + owned
),
revenue_lost AS (
    -- MRR lost to full cancellation AND downgrades in the period (gross; never netted vs expansion)
    SELECT
        pc.fiscal_period_id,
        e.account_id,
        SUM(
            CASE e.change_type
                WHEN 'cancel'    THEN e.mrr_delta_usd          -- delta stored negative
                WHEN 'downgrade' THEN e.mrr_delta_usd          -- contraction, included per contract
                ELSE 0                                         -- expansion/upgrade excluded from GRC
            END
        ) * -1 AS mrr_lost                                     -- flip to a positive loss amount
    FROM period_close pc
    JOIN mrr_change_events e
      ON e.fiscal_period_id = pc.fiscal_period_id          -- events pre-keyed to fiscal period (US/Pacific)
    WHERE e.change_type IN ('cancel', 'downgrade')
    GROUP BY pc.fiscal_period_id, e.account_id
)
SELECT
    c.fiscal_period_id,
    SUM(c.start_mrr)                                          AS start_of_period_mrr,
    COALESCE(SUM(l.mrr_lost), 0)                              AS gross_mrr_lost,
    COALESCE(SUM(l.mrr_lost), 0) / NULLIF(SUM(c.start_mrr), 0) AS gross_revenue_churn
FROM cohort_mrr c
LEFT JOIN revenue_lost l
       ON l.fiscal_period_id = c.fiscal_period_id
      AND l.account_id       = c.account_id
GROUP BY c.fiscal_period_id;
