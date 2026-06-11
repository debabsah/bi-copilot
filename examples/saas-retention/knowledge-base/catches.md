# Catches — fabricated edges refused  [Understand]
_Each line is a plausible wiring that was not drawn because nothing on hand confirms it._

| Date | Edge refused | Why it was tempting | Why it was refused |
|---|---|---|---|
| 2026-06-09 | Billing System → accounts (as evidenced) | accounts is JOIN'd alongside subscriptions in vw_monthly_churn; billing systems typically own account tables | No DDL, system-of-record statement, or any source documentation for accounts is on hand |
| 2026-06-09 | billing_export_daily → subscriptions | A daily billing extract plausibly loads or refreshes the subscriptions table | No ETL job, DDL, or proc on hand confirms any load path |
| 2026-06-09 | Finance GL ↔ Billing System | Revenue recognition normally flows from a billing system into a GL | No documented feed direction, job name, or connection statement on hand |
| 2026-06-09 | crm_accounts_sync → vw_monthly_churn | CRM segment data might enrich the churn view | CRM fields appear nowhere in vw_monthly_churn.sql; the view reads only subscriptions and accounts |
# Catches — would-have-shipped breakages found by pre-flight

| Date | Change | What would have shipped | Found by |
|---|---|---|---|
| 2026-06-15 | billing_export_daily → billing_export_v2 | event_type rename (new→created, cancel→churned, upgrade/downgrade→expansion/contraction): mart ETL movement-measure filters would have returned 0 rows against v2; NRR = 100% for all cohorts with no pipeline error — silent, and board-visible | change-impact walk, 2026-06-15 |
| 2026-06-15 | billing_export_daily → billing_export_v2 | mrr_amount unit change (integer cents → DECIMAL dollars): kpi-contract.md does not pin units; any computation joining a v1-sourced cents snapshot with v2-dollar events produces a ~100× ratio error in NRR; contract amendment and owner sign-off required before board deck regeneration | change-impact walk, 2026-06-15 |
