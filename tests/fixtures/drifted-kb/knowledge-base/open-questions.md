# Open Questions  [all phases]
_What we don't know yet. Each: the gap, why it matters, who or where to resolve it._

- [x] What decision rides on the churn dashboard? Closed 2026-05-20 by the
  interrogation: fund onboarding vs fund growth (annual), plus the board story. See
  `purpose.md` and `requirements-brief.md`.
- [x] **How must NRR reconcile to the Finance GL deck, and which retention number
  does the board see?** The board will compare the two; an unexplained gap is fatal
  (it cracked the 06-01 rehearsal). **CLOSED 2026-06-03:** the gap is definitional (cohort billing-MRR vs total GL revenue); Finance + RevOps agreed and signed off.
- [ ] Win-backs / reactivations: does a returning account rejoin its original cohort
  or start fresh? Changes the NRR denominator. Owner: RevOps (contract fork left open).
- [ ] Early-life (first-90-day) churn by signup cohort is not built yet. The funding
  decision turns on it and the recommendation wobbled without it. Owner: this team.
- [ ] Who are the five hardcoded `NOT IN` accounts in `vw_monthly_churn`? They are
  silently dropped from every current figure. Owner: whoever inherits Dana's access.
- [ ] Are trials actually excluded from the active base? Inflates the base if not.
  Owner: billing / RevOps.
- [ ] **Cohort-grain bug in `vw_monthly_churn`:** the `active_start` CTE buckets by the
  month a billing period started, not by "active at month start," so accounts on annual
  or multi-month plans drop out of the denominator. Surfaced by `query-review.md`
  (Blocking #4); confirm the grain of `subscriptions` before any rebuild reuses this
  logic. Owner: whoever builds the NRR model.
- [ ] Full graded defect list for the inherited view: see `query-review.md` (4 Blocking,
  3 Latent, 1 Advisory). The Blocking ones gate any board number from this view.
