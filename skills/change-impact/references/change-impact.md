# Change Impact — template + composition

Write per assessment. Lives at `knowledge-base/change-impact.md` (append per change,
newest on top); no `knowledge-base/` anywhere up-tree → create it now with this artifact
plus the stub `README.md` index (per the office convention in groundwork's
kb-core-templates); a provided manifest/DDL gets a dated copy in `inputs/`. Phase-tag
`[Build]` (or `[Operate]` for production changes).

```markdown
# Change Impact — <the change, one line>  [Build]
_Assessed <date>, by <who>. Before/after: <exact>. Deploy pressure noted: <if any>.
**Walked from:** <estate-map (as-of) / manifest (as-of) / files on hand> — the radius is
only as complete as this evidence; coverage boundary below._

## Verdict
<N> BREAKS · <M> SILENT-DRIFT risks (<K> on locked contracts — owner sign-off required) ·
<P> unaffected (evidenced) · <U> UNKNOWN. **Safe to ship: <no / only after the pre-flight
checks clear / yes WITHIN this evidence>.** Coverage boundary: <what the evidence cannot
see>.

## The radius (every node, graded)
| Node | Reached via | Verdict | Evidence / check |
|---|---|---|---|
| <object> | <edge + cite> | BREAKS / SILENT-DRIFT (<type>) / unaffected / **UNKNOWN** | <file:line / the pre-flight check> |

## Pre-flight checks (run and paste back before the change)
- <the query/grep that confirms or kills each UNKNOWN and drift suspicion>.

## Post-change verification
- <before/after parity on each touched contract metric; the assertion that proves clean>.

## Sign-offs and rollback
- <contract owner for each meaning-drift>; rollback: <the one-liner of how this reverts>.
```

## Composition with the knowledge base
- UNKNOWNs → `open-questions.md` with owners; the assessment → a dated `timeline.md` event
  (`by:`); add to the KB `README.md` index.
- A meaning-drift on a locked contract also gets a note in the contract's file ("change
  proposed <date>, impact assessed, owner sign-off <pending/granted>").
- A would-have-shipped breakage stopped (the rename that would have silently rounded the
  board metric) appends one line to `knowledge-base/catches.md`.
- When the office is git-tracked, offer the commit — `kb(change-impact): <change> — <N> breaks, <M> drifts, <U> unknown` — one artifact, one commit (the git-native convention in groundwork's kb-core-templates).
