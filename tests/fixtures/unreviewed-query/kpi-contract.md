# KPI Contract - Board retention metrics  [Define]
_Locked 2026-05-22, v1.0._

## Net Revenue Retention (NRR) - the headline

- **Definition:** for a fixed cohort of paying accounts active at the start of a period,
  the share of their starting MRR retained at the end including expansion, contraction,
  and churn, and excluding new logos.
- **Formula:** (start-of-period cohort MRR + expansion - contraction - churned MRR) /
  start-of-period cohort MRR. Trailing 12-month window.
- **Grain:** one cohort per period; account grain underneath.
- **Source of record:** MRR from the billing system. NOT a logo-based churn view.
- **Refresh:** quarterly (board cadence).

## Gross Revenue Churn - the secondary

- **Definition:** MRR lost to full cancellation and downgrades in the period, as a share
  of start-of-period MRR. Never netted against expansion.
- **Formula:** (churned MRR + contraction MRR) / start-of-period MRR.

## Pinned forks (the choices this contract makes)
| Fork | Pinned choice | Why it matters |
|---|---|---|
| Revenue unit | MRR (billing), NOT logos | logo churn hides seat contraction and downgrades; a seat business can bleed revenue while logo churn looks flat |
| Cohort base | start-of-period MRR | the denominator everyone argues about |
| Window | trailing 12-month | smooths seasonality; matches the annual decision |
| Contraction & downgrades | included | excluding them is exactly how logo churn hides the bleed |
| Trials & free | excluded | trials are not retained revenue |
| Period basis & timezone | fiscal, US/Pacific | aligns with the board period |
| Late cancellations | 5-business-day close, then freeze | keeps a reported quarter stable |
| Source of record | billing MRR | not the old logo view, not the Finance GL |
