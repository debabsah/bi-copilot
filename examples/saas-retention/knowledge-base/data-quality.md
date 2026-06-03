# Data Quality  [Understand]
_Why retention numbers here are not yet board-trustworthy._

| Issue | Where | Impact | Status |
|---|---|---|---|
| Churn counted in logos only | `vw_monthly_churn` | misses seat contraction and downgrades; a healthy logo count can hide revenue bleed | carried into the contract, superseded by NRR + gross revenue churn |
| Trials may be counted as active | `vw_monthly_churn` (trials share status = 'active') | inflates the active base, understates the churn rate | open question; contract pins trials excluded |
| Hardcoded account exclusion list | `vw_monthly_churn` (`NOT IN (...)`) | unknown accounts silently dropped from every figure | open question |
| UTC truncation vs Pacific reporting | `vw_monthly_churn` | edge cancellations land in the wrong month | minor; contract pins the reporting timezone |
| No restatement of late cancellations | `vw_monthly_churn` | a closed month can be wrong after a backdated cancel | contract pins a 5-day close, then freeze |
| Churn view never reconciles to Finance retention | view vs Finance GL deck | the board sees two retention stories that disagree, and nobody can explain the gap | OPEN, blocking (see open questions + contract reconciliation) |

> Bottom line at orientation: do not present `vw_monthly_churn` as revenue
> retention. The number the board actually needs (NRR) does not exist in this estate
> yet, and the gap between the view and Finance has never been explained.
