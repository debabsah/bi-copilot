# Query Review — template + composition

Write at the end of every review. Lives at `knowledge-base/query-review.md` if a KB exists (append per object reviewed), else next to the work. Phase-tag the heading `[Build]` (or `[Build][Validate]` when it doubles as the reconciliation / QA pass). Keep it scannable; the Blocking findings are the point.

```markdown
# Query Review — <object name>  [Build]
_Reviewed <date>. Object: <SQL query / view / proc / dbt model / measure / calc group / RLS rule>.
Reviewed against: <kpi-contract.md vN | stated intent (no contract pinned)>.
Read-only: reviewed as text; not executed; no data or live system touched._

- **What it's supposed to produce:** <the metric / dataset, in one line>

## Findings
| # | Location | Failure mode | What it produces | Severity | Fix direction |
|---|---|---|---|---|---|
| 1 | <where> | <named failure mode> | <the wrong result> | Blocking / Latent / Advisory | <direction; one tiny fragment at most> |

## Verdict
- **Blocking:** <count> — must fix before this ships or gets defended.
- **Latent:** <count> — will break under <conditions>.
- **Advisory:** <count> — clarity / maintainability.
- **Assumptions this review depends on:** <schema / feeds the user confirmed, or that remain open>.
```

## Composition with the knowledge base
When a `knowledge-base/` exists (from `groundwork`), thread the result in rather than leaving it stranded:
- Every **Blocking** finding -> append to `open-questions.md` with the condition that makes it blocking.
- A definition gap the review exposes (the contract is silent on a fork the code had to choose) -> route back toward `kpi-contract.md`; if no contract exists, note that one should be pinned.
- Any methodology call or rejected alternative that surfaced -> `decisions.md` (with rationale and provenance).
- Append the review as a dated event in `timeline.md` (happened: reviewed <object> vs <contract>; next: resolve <top Blocking finding>).
- Add the Query Review to the KB `README.md` index.

A reviewed build then feeds `defend-my-number`: a number whose query was checked against the contract is what survives the data/method skeptic, and the Blocking findings here are the holes the drill would otherwise expose live.

If no `knowledge-base/` exists, write the review next to the work and note that `groundwork` can stand up a full KB so the next review (and the eventual defense) builds on this one.
