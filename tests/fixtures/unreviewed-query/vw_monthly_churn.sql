-- vw_monthly_churn
-- Author: Dana R. (left the company last quarter)
-- "Monthly customer churn for the board deck." Inherited as-is.
-- No documentation beyond a stale handoff note.

CREATE VIEW vw_monthly_churn AS
WITH active_start AS (
    -- accounts with an 'active' subscription at the start of the month
    SELECT
        DATE_TRUNC('month', s.period_start) AS month,
        s.account_id
    FROM subscriptions s
    WHERE s.status = 'active'
    GROUP BY 1, 2
),
canceled_in_month AS (
    SELECT
        DATE_TRUNC('month', s.canceled_at) AS month,
        s.account_id
    FROM subscriptions s
    WHERE s.canceled_at IS NOT NULL
    GROUP BY 1, 2
)
SELECT
    a.month,
    COUNT(DISTINCT a.account_id)                                      AS accounts_start,
    COUNT(DISTINCT c.account_id)                                      AS accounts_lost,
    1.0 * COUNT(DISTINCT c.account_id) / COUNT(DISTINCT a.account_id) AS churn_rate
FROM active_start a
LEFT JOIN canceled_in_month c
       ON c.account_id = a.account_id
      AND c.month      = a.month
JOIN accounts acct ON acct.account_id = a.account_id
WHERE acct.plan_code <> 'internal'                                   -- exclude internal accounts
  AND acct.account_id NOT IN (4471, 4472, 5012, 5013, 5014)
GROUP BY a.month;
