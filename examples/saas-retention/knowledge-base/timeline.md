# Timeline  (append-only, newest at bottom)
_End of each session, append: what happened, decided, next, blocked. Drop external events with date + source._

## 2026-05-18  [Understand]
- happened: oriented on the inherited retention estate (read `vw_monthly_churn` and
  Dana's `metrics_notes.md` as text; no database touched). Stood up this KB.
- decided: classified as an inherited estate; do not trust the logo view as revenue retention.
- next: validate the real decision behind the "churn dashboard" before rebuilding.
- blocked / waiting on: nothing yet.
- note: Dana's handoff flags that the view and Finance retention "never line up";
  recorded as a data-quality caveat and an open question.

## 2026-05-20  [Define]
- happened: interrogated Priya's dashboard request; ran decision-backwards, the XY
  split, and the delta. Verdict reframe. Wrote `requirements-brief.md`.
- decided: build NRR + gross revenue churn + early-life churn by cohort, not logo
  churn plus a decorative curve. Updated `purpose.md` to the confirmed goal and closed
  the "what decision rides on this" open question.
- next: lock the metric definitions before any build.
- blocked / waiting on: whose NRR definition is authoritative, and how it reconciles
  to Finance (open for Finance + RevOps).

## 2026-05-22  [Define / Design]
- happened: pinned the metric definitions; walked the fork checklist; locked
  `kpi-contract.md` v1.0 (NRR + gross revenue churn).
- decided: billing MRR is the source of record; pinned base, window, grain,
  contraction, trials, timezone, and late-data handling.
- next: build the cohort model from the locked contract.
- blocked / waiting on: two `[needs decision]` forks open, the Finance reconciliation
  bridge and the win-back cohort rule.

## 2026-05-28  [Build / Validate]
- happened: reviewed the inherited `vw_monthly_churn` view (as text, not run) against
  the locked contract. Walked each pinned fork, then the failure-mode taxonomy. Wrote
  `query-review.md`: 8 findings, 4 Blocking.
- decided: retire the view as a board-number source; it implements neither contracted
  metric (it is logo churn, not MRR retention). Build NRR fresh from billing.
- next: build the NRR cohort model from the contract; resolve the cohort-grain bug
  before it ships.
- blocked / waiting on: the trial marker field, the grain of `subscriptions`, and the
  identity of the five excluded accounts (all open, asked of the owner).
- note: the review confirms at the code level why the view never lined up with Finance,
  finding #1, logos vs dollars. The forward reconciliation bridge stays a contract `[needs decision]`.

## 2026-06-01  [Validate]
- happened: rehearsed the board readout vs a data/method skeptic (ex-CFO). Harvested
  the locked contract and `query-review.md` as ammunition. Wrote `defense-sheet.md`.
- decided: not ready; hold the recommendation pending the Finance reconciliation and
  an early-life cohort cut.
- next: close the reconciliation [needs decision] with Finance + RevOps; build the
  cohort cut; rehearse again.
- blocked / waiting on: Finance + RevOps sign-off (blocking the 2026-06-10 board meeting).
- event: board meeting scheduled 2026-06-10 (per Priya's request).

## 2026-06-02  [Deliver]
- happened: composed the board findings brief from the KB (contract, query-review,
  defense-sheet, open-questions). Wrote `findings-brief.md`.
- decided: brief the board honestly, lead with the "not yet" verdict, present NRR 108%
  as directional (not reconciled), and keep the two open items visible rather than
  smoothing them into a confident story.
- next: close the Finance reconciliation and build the early-life cohort cut, then update
  the brief and re-rehearse before the 2026-06-10 meeting.
- blocked / waiting on: Finance + RevOps reconciliation; the early-life cohort cut.

## 2026-06-05  [Operate]
- happened: the internal exec dashboard (still fed by the board-retired `vw_monthly_churn`)
  printed ~11% monthly logo churn vs the usual ~4%; an exec asked if churn is spiking.
  Triaged it against the KB (`query-review.md`, `kpi-contract.md`, `data-quality.md`) and
  wrote `triage.md`.
- decided: working call is a measurement artifact, not a real trend; gave a calibrated
  holding line and did NOT hand the exec a confirmed cause. The code suspects are the
  defects `query-review.md` already graded (the grain bug, trials), now the first place to look.
- next: decompose `accounts_start` vs `accounts_lost` (this month vs a normal month) to
  confirm the grain bug as the cause; the real fix is the NRR rebuild, not a patch.
- blocked / waiting on: the one decomposition check (user to run). Nothing computed here.
- note: this Operate-phase spike is the 2026-05-28 retire decision proving itself in
  production. No new open question; the defects are already open.
