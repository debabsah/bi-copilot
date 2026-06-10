# Defense Sheet — template + composition

Write at the end of every drill. Lives at `knowledge-base/defense-sheet.md`; no `knowledge-base/` anywhere up-tree → create it now with this artifact plus the stub `README.md` index (per the office convention in groundwork's kb-core-templates). Phase-tag the heading `[Validate]`. Keep it one page; the holes are the point.

```markdown
# Defense Sheet — <claim>  [Validate]

- **Claim defended:** <the number / finding / recommendation>
- **Decision it supports / audience:** <what rides on it; who you face>
- **Adversary rehearsed:** <archetype (+ real person, if named)>

## Attacks and answers
| Attack raised | Your best answer | Grade |
|---|---|---|
| ... | ... | held / wobbled / cracked |

## Weak spots to shore before the room
- <hole> -> <how to shore it: caveat / reconciliation / scope-limit / get more data / sensitivity cut>

- **Readiness verdict:** ready | rehearse again | not yet — <one line of why>
```

## Composition with the knowledge base
When a `knowledge-base/` exists (from `groundwork`), thread the result in rather than leaving it stranded:
- Weak spots that are open work -> append to `open-questions.md`.
- Any methodology call or rejected alternative that surfaced in the drill -> `decisions.md` (with rationale and provenance).
- Append the rehearsal as a dated event in `timeline.md` (happened: rehearsed defense of <claim> vs <archetype>; next: shore <top hole>).
- Add the Defense Sheet to the KB `README.md` index.

If no `knowledge-base/` exists anywhere up-tree, create it now with the sheet + stub `README.md` index (`groundwork` can flesh it out later) — the next rehearsal builds on this one.

When the office is git-tracked, offer the commit — `kb(defend-my-number): <claim> drill — <readiness>` — one artifact, one commit (the git-native convention in groundwork's kb-core-templates).

A cracked claim caught before the room caught it also appends one line to `knowledge-base/catches.md` — the wins ledger.
