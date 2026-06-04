# Triage: monthly logo-churn spike  [Operate]
_Triaged 2026-06-05. Symptom: the inherited `vw_monthly_churn` printed ~11% for the latest month, up from the usual ~4%._
_Read-only: diagnosed from the view, the contract, and the prior query review; no query run, no data computed, no live system touched._

- **Symptom:** the internal exec dashboard, still fed by the (board-)retired `vw_monthly_churn`, shows ~11% monthly logo churn vs the usual ~4%. An exec asked whether churn is spiking, ahead of the 2026-06-10 board call.
- **Since:** this month's run only. **Scope:** the logo-churn metric from the inherited view; the NRR rebuild is not live yet, so nothing else is affected.
- **Status:** investigating. Working call: almost certainly a measurement artifact, not a real trend; one decomposition check from confirmed.

## Decomposition (before naming a cause)
The 11% is `accounts_lost / accounts_start`. Ask for both raw counts, this month vs a normal ~4% month, rather than reasoning from the ratio:
- If `accounts_start` (the denominator) is unusually **low** the base shrank and the rate spiked with no real change in churn. This is the prime suspect, and the view is already known to do exactly this (see below).
- If `accounts_lost` (the numerator) genuinely **jumped** it is a different conversation; keep going down the differential.

## Differential
Every row is a suspect until a check ties it to *this* month. The code suspects are not new defects; they are the ones `query-review.md` already graded, now the first place to look.

| # | Branch | Candidate cause | Discriminating check (user runs) | Status |
|---|---|---|---|---|
| 1 | code / grain | the `active_start` cohort-grain bug (`query-review.md` #4): the denominator is "accounts whose period *started* this month", so a quiet month for new or renewing periods shrinks the base and spikes the rate | decompose: is `accounts_start` low this month? recompute the base as active-at-month-start and see if the rate falls back toward 4% | open (prime) |
| 2 | code / filter | trials in the base (`query-review.md` #2): a swing in trial volume moves the rate | group the base by the real trial marker, this month vs a normal month | open |
| 3 | data / late | a backdated-cancel batch landed in this period (`query-review.md` #7: no close-then-freeze rule) | pull this month's `canceled_at` rows; are they clustered on a few days or one ingest? | open |
| 4 | pipeline | a partial load of `subscriptions` shrank the active base | row count + freshness of `subscriptions` this month vs a normal day | open |
| 5 | real | a genuine churn event (one large multi-logo account, a real cohort) | once 1 to 4 are ruled out, reconcile against Finance or the source system | open |

## Confirmed cause
None yet. `query-review.md` confirmed these **defects** exist in the code; whether the grain bug (or trials, or a late batch) produced **this** month's 11% needs the decomposition check above. A defect you can read is a suspect, not the cause.

## Calibrated line (say this now, before the cause is confirmed)
> "The 11% is almost certainly a measurement artifact in the inherited logo-churn view we already flagged for retirement, not a real trend. That view's denominator can shrink on its own and it counts free trials as customers (see `query-review.md`). I'm decomposing it now and will have a verified read by EOD; the early expectation is that underlying retention is near the normal ~4%, but I won't hand over a figure I haven't validated. This is one more reason to accelerate the NRR rebuild."

## Fix direction and hand-off
No new fix. The code suspects are already graded in `query-review.md`, and the view is already slated for retirement (`decisions.md`, 2026-05-28). This Operate-phase spike is the retirement decision proving itself in production: the board number must come from the NRR rebuild, not a patched logo view.

## Open
- The one check that confirms the cause: decompose `accounts_start` vs `accounts_lost`, this month vs a normal month (outstanding, user to run).
- No new open question escalated: the underlying defects (#4 grain, #2 trials, #5 exclusions) are already in `open-questions.md` via the query review.

## What this triage changed in the knowledge base
- **Appended `timeline.md`:** a 2026-06-05 `[Operate]` event (the spike, the differential, the calibrated line, the pending check).
- **Reinforced `decisions.md`:** production confirmation of the 2026-05-28 retire decision; no new decision, no new fix.
- **No new `open-questions.md` item:** the suspects are already open from `query-review.md`; nothing is escalated until a check confirms a cause.
- **Reads, not recomputes:** built from `kpi-contract.md`, `query-review.md`, and `data-quality.md`; no number computed, no query run, no sample touched.
