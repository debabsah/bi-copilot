# Triage artifact — triage-my-number

The committable record of a diagnosis: the symptom, the decomposition, the ranked differential, what's confirmed vs still open, and the calibrated line for stakeholders. Write it to `knowledge-base/triage.md` when a KB exists; otherwise write the one file and keep the routing notes inside it.

_Read-only: diagnosed from code, definitions, and what the user reports back; no query run, no live system touched, no data computed — including any pasted sample._

## Template

```markdown
# Triage: <metric / result>  [Operate]

**Symptom:** <what's wrong> vs <expected>. Since: <onset>. Scope: <one metric / segment / source / everything>.
**Status:** investigating | cause confirmed | resolved

## Decomposition
- Numerator vs denominator: <which moved — raw counts, broken period vs normal period>
- Scope: <where it shows / doesn't>
- Onset: <step-change on a date | gradual drift>

## Differential
| # | Branch | Candidate cause | Discriminating check (user runs) | Status |
|---|--------|-----------------|----------------------------------|--------|
| 1 | code / data / pipeline / definition / real | … | … | ruled out / confirmed / open |

## Confirmed cause
<the candidate a check tied to THIS number — or "none yet; all suspects open">

## Calibrated line (say this before the cause is confirmed)
> "<likelihood + plan to confirm + by when>, but I won't give a figure I haven't validated."

## Fix direction / hand-off
<a confirmed code defect → review-my-query; a definition gap → kpi-contract; a pipeline/data issue → the owner. The fix is the user's; this names the direction, not a rewrite.>

## Open
<checks still outstanding; what would change the conclusion>
```

## How it composes into the knowledge base
- **Reads:** `kpi-contract.md` (what the number is supposed to be — the sharpest anchor for "wrong"), `query-review.md` (defects already found — a known one is a fast suspect, not a re-investigation), `data-quality.md` / `notes.md` (known issues), `landscape.md` (lineage / what feeds it), `decisions.md` (don't re-open settled calls).
- **Writes:** `triage.md` (this artifact). On a **confirmed** cause, escalate it to `open-questions.md` (with the fix owner) and append a dated `[Validate]` entry to `timeline.md`.
- **Hands off:** a confirmed code defect → `review-my-query` (which grades it and points the fix); a definition drift or reconciliation gap → `kpi-contract` (to re-pin / version); a pipeline or source issue → the relevant owner. The calibrated line is what feeds a stakeholder or a `defend-my-number` rehearsal.
- **No KB?** Write `triage.md` alone and keep the hand-off notes inside it; `groundwork` can stand up a KB so the next triage builds on this one.
