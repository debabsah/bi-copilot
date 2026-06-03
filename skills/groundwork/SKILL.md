---
name: groundwork
description: Get oriented on an unfamiliar BI/data project and build a living knowledge base. Use at the START of a new or inherited project, or when you've lost the thread — point it at what you have (an inherited SSIS/stored-proc/SQL-Agent/DB2i estate, a vague ticket, partial docs, or nothing) and it reads what it can, interviews you for the rest, and surfaces what you don't know yet. Detects: "new project", "inherited", "took over", "where do I start", "don't understand this estate", "catch me up". Reads code/text only — never connects to or queries live data. Once the project is understood and a task is defined, proceed with the work directly instead.
allowed-tools: Read, Write
---

# groundwork

The senior who walks you onto an unfamiliar BI/data project: reads what exists, interviews you for the rest, surfaces what you don't know, and captures it into a living knowledge base you and other agents can resume from.

## When to use
Fire at the START of a new or inherited project, or when you've lost the thread. Inputs: an inherited SSIS/proc/SQL-Agent/DB2i estate, a vague ticket, partial docs, or just a conversation. Triggers: "where do I start", "took over", "inherited", "catch me up", "I don't understand this".
Do NOT fire to execute an already-understood task — once oriented, just do the work. This skill orients; it does not build pipelines or run analysis.

## Bright line (non-negotiable)
Read **code, objects, and text only** (proc SQL, SSIS `.dtsx`, job definitions, docs). **Never connect to, query, or ingest live data.** If the user pastes data or query results, refuse and ask for a plain-language description or a sanitized object definition instead.

## The loop (point-and-interrogate)
1. **Classify** the project type — inherited estate / reporting request / migration / new pipeline. If unclear, ask. Load its checklist from `references/completeness-models.md`.
2. **Ingest** what the user points you at; read it as text. Note what each object does and how they connect.
3. **Run the gap engine** (below) to find what's unknown.
4. **Interview** the user one question at a time for the highest-value gaps; adapt follow-ups; respect the bright line.
5. **Write/update** the knowledge base (state) and **append** to the timeline (history) — see `references/kb-core-templates.md`.
6. **Report**: the current picture + the top open questions + the single recommended next move.

## Surfacing what you don't know (the gap engine — use all four)
- **Completeness model:** compare what's known against the project-type checklist; flag empty slots.
- **Loose threads:** from artifacts you read — a table nothing populates, a hardcoded magic value, a referenced object that's missing, an unexplained filter.
- **Socratic:** ask the senior questions whose unanswerability reveals gaps ("what happens if this job fails mid-run? who consumes this table?").
- **Cross-check:** compare ticket vs docs vs code for contradictions.
Comprehensive thinking, lean output: check everything; record only what matters.

## The knowledge base (state + continuity)
Create/maintain `knowledge-base/` in the project repo (templates: `references/kb-core-templates.md`; optional artifacts: `references/kb-catalog.md`).
- **Always-on core:** `README.md` (index), `purpose.md`, `landscape.md`, `open-questions.md`, `decisions.md`, `notes.md`, `timeline.md`, plus `AGENTS.md` at the project root.
- **State** = current truth (update/overwrite). Tag each entry with the phase it satisfies (`[Understand]`, `[Define]`, …) so progress is legible.
- **Continuity** = `timeline.md`, append-only. At the END of every session, append a dated entry (happened · decided · next · blocked). When the user reports an external event (email/meeting/doc), append it with date + source. Link state entries back to the timeline event that produced them (provenance).
- **Resume:** when the user returns or says "catch me up", read `timeline.md` + the core, and brief them: where they are, what's happened since, what's next, what's waiting on whom.
- **Adaptive catalog:** propose only the optional artifacts the project type needs; never instantiate the whole catalog. An irrelevant section simply doesn't exist.

## Register (light)
If the user is new to this kind of work, explain why each question/step matters. If they're experienced, be terse and just hunt gaps.

## Red flags — STOP if you think these
| Thought | Reality |
|---|---|
| "I'll just start building." | You don't understand it yet — orient first or you'll build the wrong thing. |
| "Let me peek at the actual data to check." | Bright line: code/text only. Ask for a description, not a data pull. |
| "I'll write the KB at the end." | Capture as you go and journal each session, or the thread is lost. |
| "I understand it well enough." | Run the completeness model anyway — the gap you can't see is the whole point. |

## References (load on demand)
- `references/completeness-models.md` — load the matching project-type checklist at step 1.
- `references/kb-core-templates.md` — when creating/updating the always-on core.
- `references/kb-catalog.md` — when proposing optional artifacts.
