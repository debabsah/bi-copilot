# reconcile.md — template + composition

Write at the end of every reconcile. Lives at `knowledge-base/reconcile.md` if a KB exists (append per run, newest on top), else next to the work. Phase-tag the heading `[Operate]` (the audit-before-use pass), or `[Validate]` when it doubles as pre-readout QA. Keep it scannable; the Blocking drift and the unverified numbers are the point.

```markdown
# Knowledge-Base Reconcile  [<phase>]
_Run <date>. Scope: <load-bearing first / exhaustive>. For: <the decision/readout it protects>._

## Reconciled clean (with what was checked)
- <claim> -- checked against <source file:line> -- holds.

## Drift (graded)
| # | Claim (file:line) | Drift type | Evidence (the conflicting file:line + verbatim) | Grade | Suggested action |
|---|---|---|---|---|---|
| 1 | ... | partial-update | ... | Blocking | propagate the closure to kpi-contract.md, or back out the brief edit -- [needs decision: which is true] |

## Unverified (no checkable source on hand) -- run these and paste back
- <claim>: run `<exact check>` against <source>; confirms if <X>, contradicts if <Y>.

## Paste-back results
- <claim>: ran -> <verbatim result> [source: <...>] -> verified / contradicted -> <fix>.

## Verdict
<what reconciles, what is drifted/Blocking, what is unverified pending a run>. Nothing here was computed by reading; numbers are from runs or marked unverified.
```

## Composition with the knowledge base
When a `knowledge-base/` exists, thread the result in rather than leaving it stranded — and never edit the audited files themselves:
- Every **Blocking** drift -> append to `open-questions.md` with the contradiction (both `file:line`) and the suggested reconciliation action.
- Append the reconcile as a dated event in `timeline.md` (happened: reconciled the KB for <the readout>; found <N> Blocking, <M> unverified; next: resolve the top Blocking drift / run the paste-back checks).
- Cross-ref the contradicting files so the next reader sees the conflict from either side; do NOT rewrite them to agree — that is the user's call once they confirm which side is true.
- A definition gap the reconcile exposes (a claim whose contract is silent or stale) -> route back toward `kpi-contract.md`; a wrong-code finding -> `review-my-query`; a single number whose cause is unknown -> `triage-my-number`.

A reconcile is the backward/audit counterpart to the seven capture skills: they write the record forward, this checks it before its conclusions are leaned on. If no `knowledge-base/` exists, write the reconcile next to the work and note that `groundwork` can stand up a KB so the record is auditable next time.
