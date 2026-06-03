# Requirements Brief - Board churn dashboard  [Define]
_Interrogated 2026-05-20 with Priya (VP, Customer Success). Verdict: reframe._

- **Requestor / date:** Priya (VP Customer Success), 2026-05-20.
- **As-requested (the solution Y):** a board dashboard with monthly logo churn %, MRR
  churn %, and a 12-month cohort retention curve, broken out by plan tier.
- **Real decision (X):** whether to fund a dedicated onboarding / CS team next year
  (to reduce early-life churn) vs put that budget into new-logo growth, plus the
  retention story told to the board. Annual budget decision; quarterly board visibility.
- **Root need (JTBD):** When deciding next year's CS investment, I want to know
  whether we keep and grow the revenue we already won, so I can decide whether to
  fund onboarding to fix early churn.
- **Success & threshold:** the base holds its own when NRR is at or above 100%
  (expansion offsets churn); early-life churn is the lever onboarding can move. If
  NRR is comfortably above 100%, the story is "healthy, invest in growth."
- **Feasibility note:** seat and plan-change history lives in the billing system, so
  revenue-based retention is plausibly buildable; logo churn already exists. (Plain
  language only; nothing was queried.)

## Decision-derived metrics vs as-requested (the delta)
| As requested | Decision-derived | Gap |
|---|---|---|
| Monthly logo churn % | Net Revenue Retention (NRR) | logo churn hides seat contraction and expansion; for a seat-expansion business it can look healthy while revenue bleeds, or the reverse |
| MRR churn % | Gross revenue churn % (keep) | fine, but only meaningful paired with expansion / contraction |
| 12-month cohort retention curve by tier | Early-life (first-90-day) churn by signup cohort | the 12-month curve is board decoration (Priya: "the board likes a nice chart"); the funding decision turns on EARLY churn, the part onboarding can move |
| (not requested) | Expansion / contraction MRR | needed to interpret NRR and the invest-in-growth vs fix-churn fork |

- **Open questions for the stakeholder:** whose NRR definition is authoritative for
  the board (Finance, RevOps, or this team)? How must NRR reconcile to the Finance
  GL deck? (Carried to `open-questions.md`.)
- **Verdict:** **reframe** - the goal is real and fundable, but the metrics are
  wrong. Build NRR + gross revenue churn + early-life churn by cohort, not logo churn
  plus a decorative curve. Lock the definitions before building (see `kpi-contract.md`).
