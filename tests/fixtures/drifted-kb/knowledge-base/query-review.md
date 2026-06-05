# Query Review - vw_monthly_churn  [Build][Validate]
_Reviewed 2026-05-28. Object: the inherited SQL view (`inputs/vw_monthly_churn.sql`)._
_Reviewed against: `kpi-contract.md` v1.0 (NRR headline + gross revenue churn)._
_Read-only: reviewed as text; not executed; no data or live system touched._

- **What it's supposed to produce:** the board's retention number. The locked contract
  pins that as MRR-based Net Revenue Retention (headline) and gross revenue churn
  (secondary). This inherited view produces a monthly logo-churn rate.

Bottom line up front: the view implements neither contracted metric. It answers a
different question (how many logos canceled) than the contract asks (how much revenue
was retained), and it carries correctness bugs that would distort even a logo-churn read.

## Findings
| # | Location | Failure mode | What it produces | Severity | Fix direction |
|---|---|---|---|---|---|
| 1 | whole view | conformance, revenue unit: counts logos (`COUNT(DISTINCT account_id)`); the contract pins MRR | a logo-churn rate standing in for revenue retention; it can look flat while MRR bleeds, and it is exactly why this view has never reconciled to Finance's dollar-based retention (the gap Dana flagged on day one) | Blocking | this cannot be patched into NRR; the contracted metric is a separate build against billing MRR (start-of-period cohort MRR, expansion, contraction, churn). Out of scope for a review |
| 2 | `WHERE s.status = 'active'` | conformance + filter: trials carry `status = 'active'` in this schema (the view's own comment says so); the contract excludes trials | the start-of-month base is inflated with non-paying trials, so the churn rate is understated | Blocking | exclude trials by the real trial marker; that field is not visible in this view, so confirm it with billing / RevOps rather than trusting `status` |
| 3 | `DATE_TRUNC('month', period_start)` and `DATE_TRUNC('month', canceled_at)` | time: truncates UTC timestamps; the contract pins fiscal US/Pacific | cancellations near a month boundary land in the wrong month, and the period itself does not match the board calendar | Blocking | convert to the reporting timezone on the fiscal calendar before truncating |
| 4 | `active_start` CTE | grain: buckets accounts by the month a billing period started, not by membership "active at the start of the month"; the final join then requires the cancel to fall in that same month | the denominator becomes "accounts whose period started this month." Accounts on annual or multi-month plans drop out of the base in months with no period boundary, and a prior cohort's cancellation is not matched, so churn is undercounted | Blocking | define the start cohort as a point-in-time membership test (active on the period's first instant), independent of the cancel month. Confirm the grain of `subscriptions` (one row per period vs per month) with the owner |
| 5 | `NOT IN (4471, 4472, 5012, 5013, 5014)` | filter: undocumented magic list ("no idea who these are") | silently removes five accounts no one can identify from every figure; the number is not reproducible or auditable | Latent | identify and document; if they are real accounts, move them to a documented exclusion table with a reason, or remove |
| 6 | `acct.plan_code <> 'internal'` | NULL: `NULL <> 'internal'` evaluates to NULL (falsy), so the row is dropped | any account with a NULL `plan_code` is silently excluded from the base | Latent | decide intent; `plan_code IS DISTINCT FROM 'internal'` keeps NULL-plan accounts in |
| 7 | no close rule anywhere in the view | time / late data: the contract pins a 5-business-day close, then freeze | a cancellation backdated after month close silently changes an already-reported month | Latent | apply the close-then-freeze rule from the contract |
| 8 | `1.0 * COUNT(...) / COUNT(...)` | determinism: no zero guard on the denominator | divide-by-zero or NULL on a month with an empty cohort | Advisory | guard the denominator, e.g. `NULLIF(denominator, 0)` |

## Verdict
- **Blocking:** 4 - must resolve before any number from this view feeds the board or
  gets defended. Most fundamentally finding #1: the view answers a different question
  than the contract.
- **Latent:** 3 - will distort or drift under real data (manual exclusions, NULL plans,
  backdated cancellations).
- **Advisory:** 1.
- **Assumptions this review depends on (open, asked of the owner, not assumed):** the
  real trial marker field (#2), the grain of `subscriptions`, one row per billing period
  vs per month (#4), the fiscal-calendar definition (#3), and the identity of the five
  excluded account IDs (#5).

## What this review changed in the knowledge base
- **Escalated to `open-questions.md`:** the `active_start` cohort-grain bug (#4) is new
  here. The trials base (#2), the hardcoded exclusions (#5), and the Finance
  reconciliation were already open; this review confirms them at the code level.
- **Recorded in `decisions.md`:** retire `vw_monthly_churn` as a source for the board
  retention number; build NRR fresh against billing MRR per the contract.
- **The Finance thread:** the root cause of the non-reconciliation is finding #1 (logos
  vs dollars). The forward bridge, how the new NRR reconciles to the Finance GL, remains
  the contract's open `[needs decision]`; this review explains the old gap but does not
  close the new one.
- **Feeds `defend-my-number`:** the Blocking findings here are the holes the board drill
  would otherwise expose live. #1 is why "Finance says 2%, you say 108%" still has no
  clean answer.
