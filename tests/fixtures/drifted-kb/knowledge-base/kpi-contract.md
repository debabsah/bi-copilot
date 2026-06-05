# KPI Contract  [Define]
_Locked 2026-05-22, v1.0. Source: the reframed metrics in `requirements-brief.md`._

## Net Revenue Retention (NRR) - the headline

- **Definition (one sentence):** for a fixed cohort of paying accounts active at the
  start of a period, the share of their starting MRR retained at the end including
  expansion, contraction, and churn, and excluding new logos.
- **Formula:** (start-of-period cohort MRR + expansion - contraction - churned MRR) /
  start-of-period cohort MRR. Trailing 12-month window.
- **Grain:** one cohort per period; account grain underneath.
- **Dimensions:** plan tier, signup cohort, region. Misleading: blending all cohorts
  into one company-wide NRR hides early-life churn, which is the decision's whole point.
- **Source of record:** MRR from the billing system. NOT `vw_monthly_churn` (logo
  based) and NOT the Finance GL (recognized revenue; includes new logos and services).
- **Reconciliation:** NRR (billing MRR, cohort-only) will NOT equal Finance's GL
  revenue growth. Expected bridge: GL revenue = cohort-retained MRR + new-logo MRR +
  one-time / services revenue, with billed-vs-recognized timing differences.
  **[needs decision: Finance + RevOps to confirm the exact bridge and sign off on
  which retention number the board sees.]**
- **Refresh:** quarterly (board cadence); recomputed at each fiscal quarter close.
- **Threshold / direction:** up is good; at or above 100% means the base grows on its
  own. Below 100% with high early-life churn argues for funding onboarding.
- **Owner:** RevOps, co-signed by Finance.
- **Caveats:** is NOT logo retention; is NOT total company revenue growth; excludes
  new logos by construction.
- **Version / effective-date:** v1.0, 2026-05-22.

### Fork log - the choices this definition makes
| Fork | Options | Pinned choice | Why it matters |
|---|---|---|---|
| Revenue unit | MRR / ARR / recognized revenue | MRR (billing) | recognized revenue drags in GL timing and services; MRR is the retention unit |
| Cohort base | start-of-period / average / end-of-period | start-of-period MRR | the denominator everyone argues about; start-of-period is standard |
| Window | monthly / trailing 12-month | trailing 12-month | smooths seasonality; matches the annual funding decision |
| Grain | account / subscription / seat | account | the board and the funding call are per customer |
| Contraction & downgrades | included / excluded | included | excluding them is exactly how logo churn hid the bleed |
| Trials & free | included / excluded | excluded | trials are not retained revenue |
| Win-backs / reactivations | rejoin original cohort / start fresh | [needs decision] | changes the denominator for returning accounts; RevOps to rule |
| Period basis & timezone | calendar UTC / fiscal US-Pacific | fiscal, US/Pacific | aligns with the board period; fixes the view's UTC edge bug |
| Late cancellations | restate forever / freeze at close | 5-business-day close, then freeze | keeps a reported quarter stable |
| Source of record | billing MRR / Finance GL / the old view | billing MRR | the others measure different things; see reconciliation |
| Reconciliation to Finance | known bridge / unknown | [needs decision] | the board WILL compare to Finance; an unexplained gap sinks the number |

## Gross Revenue Churn - the secondary

- **Definition:** MRR lost to full cancellation and downgrades in the period, as a
  share of start-of-period MRR. Never netted against expansion.
- **Formula:** (churned MRR + contraction MRR) / start-of-period MRR.
- **Grain / source / timezone / late data:** as above.
- **Threshold / direction:** down is good; pairs with NRR so the board sees gross loss
  and net retention side by side.
- **Owner:** RevOps. **Version:** v1.0, 2026-05-22.
- **Caveats:** gross churn improving while NRR is flat can mean expansion is slowing;
  read the two together, never alone.
