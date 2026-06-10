# Dashboard Review — template + composition

Write per review pass. Lives at `knowledge-base/dashboard-review.md` (append per surface,
newest on top); no `knowledge-base/` anywhere up-tree → create it now with this artifact
plus the stub `README.md` index (per the office convention in groundwork's
kb-core-templates); provided exports/definitions get dated copies in `inputs/`. Phase-tag
`[Validate]`.

```markdown
# Dashboard Review — <surface, pages, as-of>  [Validate]
_Reviewed <date>, by <who>. Serves: <the decision/audience>. Reviewed from: <definitions /
export / configs / screenshots provided>. **Coverage boundary:** <what could not be
reviewed from text — RLS rules, live filter behavior, …> — named, not assumed._

## Verdict
**<Ship / Ship after Blocking fixes / Do not ship>** — <N> Blocking · <M> Latent ·
<K> Advisory. <One sentence: the single most room-facing risk.>

## Findings register
| # | Layer | Finding | Grade | Evidence | Fix direction |
|---|---|---|---|---|---|
| 1 | semantic / state / presentation | <what the assembly does wrong> | Blocking / Latent / Advisory | <definition/config cite> | <direction, not the edit> |

## Contract conformance
| Displayed metric | Contract | Conforms? |
|---|---|---|
| <metric> | <kpi-contract vX / NONE — finding #N> | yes / no (finding #N) |

## What passed
- <the measures/visuals that are right, said plainly — a review that only lists faults
  teaches nothing about what to keep>.
```

## Composition with the knowledge base
- Findings worth tracking → `open-questions.md` (with owners); the review → a dated
  `timeline.md` event (`by:`); add to the KB `README.md` index.
- A displayed metric with no contract → recommend `kpi-contract`; a defect in ONE
  measure's code → route to `review-my-query` rather than reviewing the code here.
- A would-have-shipped lie stopped (the double-counted total, the stale-as-live label)
  appends one line to `knowledge-base/catches.md`.
- When the office is git-tracked, offer the commit — `kb(review-my-dashboard): <surface> — <N>B/<M>L/<K>A` — one artifact, one commit (the git-native convention in groundwork's kb-core-templates).
