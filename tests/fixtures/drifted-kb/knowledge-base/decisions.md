# Decisions & Assumptions  [all phases]
_Each: the decision, rationale, rejected alternatives, date, source event._

- 2026-05-20 - **Reframe the request** from a logo-churn dashboard to NRR + gross
  revenue churn + early-life churn by cohort. Rationale: logo churn cannot answer the
  funding decision and hides seat contraction. Rejected: building the dashboard as
  asked (logo-churn headline + 12-month decorative curve). (per timeline: the
  interrogation with Priya.)
- 2026-05-22 - **NRR is the headline retention metric; billing MRR is the source of
  record.** Rejected: Finance GL revenue (includes new logos, services, and timing)
  and the inherited logo view. (per timeline: contract lock v1.0.)
- 2026-05-22 - Pinned forks: start-of-period cohort base, trailing-12-month window,
  account grain, contraction included, trials excluded, fiscal US/Pacific, 5-day
  close then freeze. Left open: win-back cohort rule, Finance reconciliation bridge.
- 2026-05-28 - **Retire `vw_monthly_churn` as a source for the board retention number.**
  Reviewed against the locked contract, it implements neither contracted metric (logo
  churn, not MRR retention) and carries 4 Blocking defects. Rationale: it cannot be
  patched into NRR; the contracted metric is a separate build against billing MRR.
  Rejected: salvaging the view by bolting MRR onto the logo logic. (per timeline:
  `query-review.md`.)
- 2026-06-01 - **Hold the board recommendation** ("invest in growth, not onboarding")
  pending the Finance reconciliation and an early-life cohort cut. Rationale: the
  rehearsal cracked on the unreconciled gap. (per timeline: defense rehearsal.)
- 2026-06-02 - **Brief the board honestly: carry the "not yet" verdict.** The findings
  brief presents NRR 108% as directional (not reconciled), keeps the Finance bridge and
  the early-life cohort cut as open items, and does not assert the recommendation.
  Rationale: a confident "retention is healthy, invest in growth" readout would over-state
  an unreconciled number and an unevidenced recommendation. Rejected: smoothing the open
  gap, or stating the recommendation as the answer. (per timeline: `findings-brief.md`.)
- 2026-06-03 - NRR 108% is board-ready. The Finance reconciliation is resolved as definitional: NRR (existing-cohort billing MRR) and Finance's total GL revenue growth measure different bases and were never expected to match; RevOps (J. Okafor) + Finance (M. Chen) agreed NRR is the existing-base retention measure and signed off. Supersedes the 2026-06-02 "carry the not-yet" on the reconciliation; the early-life cohort cut remains open for the funding recommendation.
- 2026-06-05 - **Production reinforced the retirement of `vw_monthly_churn`.** The retired
  view spiked to ~11% on the internal dashboard; triage diagnosed it as almost certainly a
  measurement artifact (its own grain bug or trial inclusion, per `query-review.md`), not a
  real churn event, and gave the exec a calibrated holding line rather than a confirmed
  cause. No new fix and no new decision: the board number comes from the NRR rebuild, not a
  patched logo view. Rationale: the spike is exactly the unreliability the retirement
  decision anticipated. (per timeline: `triage.md`.)
