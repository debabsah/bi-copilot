# Findings Brief — template + composition

Write at the end of every briefing pass. Lives at `knowledge-base/findings-brief.md` if a KB exists (append per decision/audience briefed), else next to the work. Phase-tag the heading `[Deliver]`. Keep it scannable; the decision, the open items, and the carried verdict are the point.

```markdown
# Findings Brief — <decision / topic>  [Deliver]
_Briefed <date>. For: <audience / stakeholder>. Decision it informs: <the call riding on this>._
_Built from: <kpi-contract vN · query-review · defense-sheet · decisions · ... | stated findings (no contract / KB)>.
Read-only: composed from evidence on hand; no number computed or re-derived; nothing manufactured._

- **Bottom line:** <the one-line takeaway, at the confidence the evidence supports — including "not yet" if that is the verdict>

## Findings
Each: observation → implication → action → watch-for. Tag every claim with its status AND qualifier `[Supported | Directional-only | Open - needs decision | Inferred : source · n=<base>, ±<interval>, scope <window/filter>]` — the qualifier rides with the figure (drop nothing the number arrived with; an exact count needs no interval). **Carry each figure's qualifier onto the final slide/email — the brief states it; the downstream medium must not strip it.**
1. **<observation, carrying its qualifier — e.g. "churn 4.2% (n=1,240; trailing-90-day)">** `[Supported : kpi-contract + query-review]`
   - Implication: <what it means for the decision>
   - Action: <what to do / recommend — or "hold" if the verdict is not yet>
   - Watch-for: <what would change this; the pushback to expect → feeds defend-my-number>

## What is still open / not yet sayable
| # | Open item | Status | Why it matters to the decision | Owner / where it resolves |
|---|---|---|---|---|
| 1 | <the [needs decision] / unbuilt cut / unreconciled gap> | Open | <consequence if presented as resolved> | <owner> |

## Readiness
- **Verdict carried:** <e.g. "not yet" from defense-sheet — do not present until the open items close | ready, with the caveats above>.
- **Confidence:** <which claims are Supported vs Directional-only; what would move a Directional claim to Supported>.
```

## Composition with the knowledge base
When a `knowledge-base/` exists (from `groundwork`), thread the result in rather than leaving it stranded:
- The `[Open]` items the brief surfaces -> reconcile against `open-questions.md`; add any new one, with the condition that keeps it open. Never close one here that the analysis has not closed.
- A carried verdict (e.g. "not yet") -> keep it consistent with `defense-sheet.md`; the brief does not overturn the rehearsal.
- Any communication call made (what to lead with, what to hold) -> `decisions.md`, with rationale.
- Append the brief as a dated event in `timeline.md` (happened: briefed <decision> for <audience>; next: close <top open item> before presenting).
- Add the Findings Brief to the KB `README.md` index.

The brief's **watch-for** items are the attacks `defend-my-number` should rehearse next: a number written up with its provenance and its open gaps is what survives the room, and the gaps named here are the holes the drill would otherwise expose live.

If no `knowledge-base/` exists, write the brief next to the work, keep the provenance/status tags inline, and note that `groundwork` can stand up a full KB so the next brief (and the defense) builds on this one.
