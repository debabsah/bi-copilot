# Open Questions  [all phases]
_What we don't know yet. Each: the gap, why it matters, who or where to resolve it._

- [x] What decision rides on the churn dashboard? Closed 2026-05-20 by the
  interrogation: fund onboarding vs fund growth (annual), plus the board story. See
  `purpose.md` and `requirements-brief.md`.
- [ ] **How must NRR reconcile to the Finance GL deck, and which retention number
  does the board see?** The board will compare the two; an unexplained gap is fatal
  (it cracked the rehearsal). Owner: Finance + RevOps. **Blocking the 2026-06-10 board meeting.**
- [ ] Win-backs / reactivations: does a returning account rejoin its original cohort
  or start fresh? Changes the NRR denominator. Owner: RevOps (contract fork left open).
- [ ] Early-life (first-90-day) churn by signup cohort is not built yet. The funding
  decision turns on it and the recommendation wobbled without it. Owner: this team.
- [ ] Who are the five hardcoded `NOT IN` accounts in `vw_monthly_churn`? They are
  silently dropped from every current figure. Owner: whoever inherits Dana's access.
- [ ] Are trials actually excluded from the active base? Inflates the base if not.
  Owner: billing / RevOps.
