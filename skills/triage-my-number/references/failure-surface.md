# Failure surface — triage-my-number

Load when running the engine (loop step 3). The job: enumerate the *whole* path a number travels, attach a **discriminating check** to each candidate, and keep "a defect you can read" separate from "the cause of this number." Comprehensive thinking, lean output: walk every branch, record only the candidates that could produce *this* symptom.

## Decompose first (do this before naming any cause)
The single highest-value move, and the one a tunnelling diagnosis skips. Before chasing causes, split the symptom so you chase the right half:
- **Numerator vs denominator.** A rate moved — did the numerator jump or the denominator shrink? They have completely different causes. Print both as raw counts for the broken period *and* a normal period; never reason from the ratio alone.
- **Scope.** One metric, one segment, one source, or everything? A break in one slice points at that slice's data/join; a break everywhere points at the pipeline or the definition.
- **Onset.** Since when? A step-change on a date points at a load/source/code change on that date; a gradual drift points at data or a real trend.

`(numerator vs denominator) × (scope) × (onset)` usually halves the differential before you've named a single root cause.

## The branches (the engine)
Walk all five. The classic failure is to stop at the first plausible hit — usually the code, because it's the thing you can read.

**1. Code** — the logic that computes the number. Reuse `review-my-query`'s taxonomy: grain/cardinality (fan-out, wrong-grain denominator, misaligned numerator/denominator cohorts, a non-additive measure re-aggregated below its grain), filter/context (filter at the wrong stage, `<> 'x'` dropping NULLs, a magic `NOT IN` list), NULL/type, time (UTC-vs-reporting-zone truncation, period off-by-one, fiscal vs calendar), set logic, SCD, determinism. *Discriminating check:* recompute the number the way the definition intends (corrected denominator / timezone / trial exclusion) and see if it returns to normal — the **user** runs it; if it collapses back, the code is the cause.

**2. Data** — the same code can output a wrong number on changed input. Late-arriving / backdated rows landing in an already-reported period; a backfill or replay; an upstream/source-system change (a renamed status, a new plan code, a migrated billing table); a new or out-of-range value; a volume spike (e.g. a marketing push inflating trials). *Discriminating check:* pull the raw rows behind the spike (the cancels this month vs a normal month; the new/changed values) and eyeball — more events, or the same events recounted? clustered by one source/cohort/timestamp?

**3. Pipeline** — the number can be wrong because the data is incomplete or stale, not wrong. A partial or failed load (denominator silently halved); a step that errored but didn't alarm; a stale refresh / cached layer serving yesterday's data; a dependency that ran out of order. *Discriminating check:* row counts and freshness/`max(loaded_at)` for the relevant tables vs a normal day; did every step land?

**4. Definition** — the number changed because what it *means* changed. Someone edited the view/measure; the metric's contract drifted; two reports use two definitions of "the same" number (the classic "they don't reconcile"). *Discriminating check:* diff the object/definition against its last-known-good version and against `kpi-contract.md`; for a reconciliation gap, line up the two definitions side by side before touching data.

**5. Real change** — it might just be true. A genuine churn event, a real cohort shift, a true business move. Do not rule this out because the code is ugly — but do not *assume* it because the number is scary. *Discriminating check:* once 1–4 are ruled out (or the corrected recompute still shows it), confirm against an independent signal (Finance, the source system, a second metric that should move with it).

> Two rules while hunting: **"nothing changed" is the assumption to trust least** (branches 2 and 3 are exactly the silent changes); and **a defect you can read is a suspect, not the cause** — only a check that ties it to *this* number confirms it, and that check is the user's to run.

## The calibrated holding line
Before a cause is confirmed, the stakeholder still needs a sentence. Give the honest one, not a guess: state the *likelihood* and the *plan to confirm*, never an unverified cause as fact.
- Good: *"The 11% looks like a measurement artifact, not a real trend — the inherited view compares cancellations against the wrong base. I'm recomputing on a corrected base and will have a verified number by EOD; early read is retention is near the ~4% norm, but I won't give you a figure I haven't validated."*
- Bad: *"Churn doubled because of trials."* (a suspect, stated as the cause, to the board).

## Worked example — the churn-spike triage (the same vw_monthly_churn, done right)
Symptom: monthly logo churn printed ~11% this month vs the usual ~4%; leadership wants why before the board call.

**Decompose first:** print `accounts_start` and `accounts_lost` separately, this month vs a normal month — did cancels jump, or did the start-base shrink? (This alone usually tells you which branch.)

```markdown
## Differential
| # | Branch | Candidate cause | Discriminating check (user runs) | Status |
|---|--------|-----------------|----------------------------------|--------|
| 1 | code/grain | denominator = "accounts whose period *started* this month," not "active at month start"; a quiet base shrinks the denominator and spikes the rate | recompute with the start-base as a point-in-time membership test; compare to the printed rate | open |
| 2 | code/filter | trials carry status='active' and sit in the base; a trial-volume swing moves the rate | recompute excluding the trial marker; does the rate fall back? | open |
| 3 | data/late | a batch of backdated cancellations landed in this period | pull cancels with canceled_at this month, group by reported-vs-actual date; clustered? | open |
| 4 | pipeline | partial load shrank the active base | row count + freshness of subscriptions this month vs a normal month | open |
| 5 | time | UTC vs fiscal/Pacific pulled a boundary cluster into the wrong month | check cancel timestamps near the month boundary | open |
| 6 | real | genuine churn — one large multi-logo account, a real cohort | once 1–5 ruled out, reconcile against Finance / the source | open |

## What I can say now (calibrated line)
"Likely a measurement artifact in an inherited view, not a real doubling. Recomputing on a corrected base; verified number by EOD."

## Confirmed
- (none yet — every row is a suspect until its check ties it to the number)
```

Note what the triage does NOT do: it never runs the recompute itself, never computes the rate from a pasted sample, and never writes "churn doubled because of trials" into the board line. It decomposes, enumerates the whole surface, checks-then-concludes, and hands the checks to the user.
