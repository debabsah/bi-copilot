# Exploration Log — template + composition

Write as the exploration proceeds, not after. Lives at `knowledge-base/exploration-log.md`
(append per investigation); no `knowledge-base/` anywhere up-tree → create it now with
this artifact plus the stub `README.md` index (per the office convention in groundwork's
kb-core-templates); a handed results table/extract gets a dated copy in `inputs/`.
Phase-tag the heading `[Understand]` (or `[Validate]` once confirmations run).

```markdown
# Exploration Log — <question / dataset>  [Understand]
_Started <date>, by <who>. Decision it serves: <the call this exploration informs>.
Population/window/grain: <pinned before looking>. Finding-bar: <what magnitude on what
base would matter>. Read-only: cuts run by the user; nothing computed here._

## Hypothesis ledger
| # | Question / hypothesis | Registered | Status |
|---|---|---|---|
| H1 | <pre-registered question> | pre (before results) | open / supported / dead end |
| H2 | <pattern noticed in results> | **post-hoc** (<date seen>) | Exploratory — found |

## Cut log (the multiplicity counter)
Cuts examined: **N** (every fork, hits and misses). At α≈.05, ~N/20 false hits expected.
| # | Cut | Result (effect · base · scope) | Note |
|---|---|---|---|

## Findings (graded)
| Finding | Grade | Why | Confirmation path |
|---|---|---|---|
| <pattern> | Exploratory — found / Robust pattern / Dead end / **Confirmed (paste-back <date>)** | <bases, robustness tests passed/failed, the multiplicity line> | <the pre-specified hold-out check> |

## Confirmation checks (run and paste back)
- <finding>: <exact cut on data the finding hasn't seen — fresh window / untouched slice>,
  pre-registered threshold: <what confirms vs kills it>.

## Routing
- Confirmed findings → brief-my-findings. A causal claim → audit-my-experiment (design,
  not a cut). A definition wobble surfaced mid-cut → kpi-contract. A number found WRONG →
  triage-my-number.
```

## Composition with the knowledge base
- New questions worth keeping → `open-questions.md`; the exploration as a dated `timeline.md`
  event (`by:`); add the log to the KB `README.md` index.
- A dredge-mirage stopped (the goldmine that wasn't) also appends one line to
  `knowledge-base/catches.md` — the wins ledger.
- When the office is git-tracked, offer the commit — `kb(explore-my-data): <question> — <N> cuts, <M> findings` — one artifact, one commit (the git-native convention in groundwork's kb-core-templates).
