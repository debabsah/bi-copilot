# Notes, Gotchas & Glossary  [all phases]

## Gotchas
- `vw_monthly_churn` hardcodes `account_id NOT IN (4471, 4472, 5012, 5013, 5014)`.
  Origin unknown (Dana inherited it from a prior analyst). Do not extend or trust it
  blindly; see open questions.
- The view's period boundary truncates UTC timestamps while reporting is US/Pacific.
  Cancellations near midnight can land in the wrong month.
- Late or backdated cancellations are not restated once a month closes.

## Glossary
- **Logo churn** - count of customers (accounts) lost, regardless of dollars.
- **Gross revenue churn** - MRR lost to cancellations and downgrades, as a share of
  starting MRR. Never negative.
- **Expansion / contraction MRR** - MRR gained or lost from existing accounts
  changing seats or plans (not from new logos or full cancellation).
- **NRR (Net Revenue Retention)** - for a fixed cohort of accounts, end MRR over
  start MRR including expansion, contraction, and churn, excluding new logos. Above
  100% means the existing base grew on its own.
- **Cohort** - accounts grouped by when they started, tracked over time.

## Caveats (what NOT to trust)
- The board's current churn slide (logo-based) is not a revenue-retention measure
  and must not be read as one. See `data-quality.md` and `kpi-contract.md`.
