# Knowledge Base — Core Templates

The guide creates a `knowledge-base/` folder in the project repo. These are the **always-on core** files (seeded for every project) plus the index and agent pointer. Keep entries terse; record only what's known/relevant. Tag entries with the phase they satisfy: `[Understand] [Define] [Design] [Build] [Validate] [Deliver] [Operate]`.

## knowledge-base/README.md (the index — start here)
```markdown
# <Project> — Knowledge Base
_Last updated: <date>_
Start here. This is the living understanding of the project, for me and for AI agents.
- [Purpose](purpose.md) · [Landscape](landscape.md) · [Open Questions](open-questions.md)
- [Decisions](decisions.md) · [Notes & Glossary](notes.md) · [Timeline](timeline.md)
- Optional artifacts present: <list, or "none yet">
```

## knowledge-base/purpose.md
```markdown
# Purpose  [Understand→Define]
- What this project/system is for (business process served):
- Who/what consumes its outputs:
- The ask (as received) vs the real decision it supports:
```

## knowledge-base/landscape.md
```markdown
# Object & Data Landscape  [Understand]
- Systems in play (databases / warehouses / files / pipelines / other):
- Key objects (query/procedure / pipeline / scheduled job / report / table) — what each does:
- How they connect (lineage / dependencies):
- Grain & keys of important tables:
```

## knowledge-base/open-questions.md
```markdown
# Open Questions  [all phases]
_What I don't know yet. Each: the gap · why it matters · who/where to resolve it._
- [ ] <gap> — <why> — <ask whom>
```

## knowledge-base/decisions.md
```markdown
# Decisions & Assumptions  [all phases]
_Each: the decision · rationale · rejected alternatives · date · source event._
- <date> — Decided <X> because <Y>; rejected <Z>. (per timeline: <event>)
- Assumption: <A> — to confirm.
```

## knowledge-base/notes.md
```markdown
# Notes, Gotchas & Glossary  [all phases]
- Gotchas (hardcodes, manual steps, weird exceptions):
- Glossary (terms / acronyms):
- Caveats (what NOT to trust):
```

## knowledge-base/timeline.md (the continuity log — append-only)
```markdown
# Timeline  (append-only — newest at bottom)
_End of each session, append: what happened · decided · next · blocked. Drop external events with date + source._
## <date>
- happened:
- decided:
- next:
- blocked / waiting on:
- event (if any): <email/meeting/doc> from <source>
```

## AGENTS.md (place at the PROJECT ROOT, not inside knowledge-base/)
```markdown
# Agent Onboarding
If you are an AI agent working on this project, read `knowledge-base/README.md` first — it is the living state and history of this work.
```
