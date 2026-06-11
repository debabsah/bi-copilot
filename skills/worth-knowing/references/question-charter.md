# The Question Charter — artifact template

The living agenda of what's worth knowing. Lives at
`knowledge-base/question-charter.md`; every stakeholder session updates it in
place (STATE, not log — the session history goes to `timeline.md`). Phase-tag
`[Define]`.

```markdown
# Question Charter — <project / engagement>

Status: LIVING — last session <YYYY-MM-DD> with <who>
Vanity flag: <none | SET — no decision landscape elicitable; see note>
Charter summary: <N> decision-anchored · <M> curiosity · unasked: <K or
  "empty — reason">

## Decision landscape (elicited <date>, from <who>)
| Decision | Who acts | Cadence / next occurrence | Lever |
|---|---|---|---|
| <e.g. punch-pass renewal> | COO | annual, October | keep / reprice / kill |

## Estate as described (inventory of the askable)
| Source | What it holds | Availability evidence |
|---|---|---|
| Billing | subs, MRR, start/end | cited: <who/file, date> |
| Old CRM pre-2024 history | … | **UNVERIFIED** — check written below |

## Candidates (ranked; criteria below)
### Q1. <the question, as a question>
- Tier: ANCHORED — <decision, actor, cadence> | CURIOSITY
- Expected shape: HYPOTHESIS — no data examined. <what would follow if it
  confirms / disconfirms — never "will show">
- How to read: <magnitude on what base would matter; what would NOT count>
- Confirms via: <the route by name — explore-my-data pre-registered cut /
  kpi-contract first / map-my-estate first> — user runs, pastes back
- Data: <required> vs <available — cited or UNVERIFIED (+ the check)>
- Effort: L / M / H
- Status: PROPOSED | ACCEPTED → routed <skill, date> | DECLINED (<reaction,
  date — stays on the charter>) | RESHAPED → Q<n>

## The unasked (mandatory)
<≥1 candidate from outside the stated goals, unwelcome answers included —
or: "Empty — <written reason>". Never silently absent.>

## Ranking criteria (this charter's rubric)
Decision-weight × feasibility × effort, graded H/M/L; anchored before
curiosity, always. <Any project-specific weighting, in plain words.>
Rank changes between sessions name which axis moved and why.

## Session log
- <date> — <who> — <accepted Q1, declined Q4 ("…"), reshaped Q2→Q6;
  pressure noted: "just give us the answers by Friday" — recorded, not obeyed>
```

## How it composes into the knowledge base

- **No `knowledge-base/` anywhere up-tree?** Create it now containing this
  charter plus a stub `README.md` index — that IS the knowledge base starting;
  `groundwork` can flesh it out later.
- Open stakeholder questions (the decision landscape gaps, the UNVERIFIED
  checks) → `open-questions.md`. Accept/decline calls with rationale →
  `decisions.md`. Every session → a dated `timeline.md` event.
- A handed-over data-landscape note or ticket you cite gets a dated copy in
  `inputs/` (`YYYY-MM-DD-<name>`) so the citation survives.
- **Update stale STATE, don't just append**: if elicitation resolves something
  `purpose.md` or `open-questions.md` asserts, edit that file to current truth.
- A stopped fake-insight ("top 3 insights by tonight" refused, charter
  delivered) earns its `catches.md` line — that is the wins ledger.
- Git-tracked office: offer the commit —
  `kb(worth-knowing): charter <created|updated> — <N> anchored / <M> curiosity`.

## Re-fire behavior (the living part)

Re-fired with reactions in hand, the skill EDITS this charter: statuses move,
ranks change with their named reason, declined candidates stay visible,
reshaped ones link forward. A re-fire never starts a second charter file; one
engagement, one charter.
