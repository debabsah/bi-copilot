# reconcile.md — template + composition

Write at the end of every reconcile. Lives at `knowledge-base/reconcile.md` (append per run, newest on top) — a reconcile presupposes a KB to audit, so there is no lazy-create case here. Phase-tag the heading `[Operate]` (the audit-before-use pass), or `[Validate]` when it doubles as pre-readout QA. Keep it scannable; the Blocking drift and the unverified numbers are the point.

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
`reconcile.md` is the only file you write. Everything below is RECOMMENDED to the user inside that report — kb-reconcile never edits the audited files itself (you cannot audit a record you are also rewriting):
- For every **Blocking** drift, recommend the `open-questions.md` entry to add (the contradiction, both `file:line`, and the reconciliation action) for the user to paste in.
- Recommend a dated `timeline.md` line (happened: reconciled the KB for <the readout>; found <N> Blocking, <M> unverified; next: resolve the top Blocking drift / run the paste-back checks).
- Cross-ref the contradicting files in the report so the next reader sees the conflict from either side; do NOT rewrite them to agree — that is the user's call once they confirm which side is true.
- Route a definitional gap back toward `kpi-contract.md`, a wrong-code finding toward `review-my-query`, a single number whose cause is unknown toward `triage-my-number`.

A reconcile is the backward/audit counterpart to the capture skills: they write the record forward, this checks it before its conclusions are leaned on. If no `knowledge-base/` exists, there is nothing to reconcile — point the user at `groundwork` (or any skill's first artifact, which creates the office) so the record is auditable next time.

When the office is git-tracked, offer the commit — `kb(kb-reconcile): reconcile — <N> Blocking, <M> unverified` — one artifact, one commit (the git-native convention in groundwork's kb-core-templates).

A Blocking drift caught before a readout leaned on it also appends one line to `knowledge-base/catches.md` — the wins ledger (recommended in the report; the user applies it, since this skill writes only `reconcile.md`).
