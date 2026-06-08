---
name: brief-my-findings
description: Use when a BI/analytics professional has finished the analysis and needs to communicate the findings to a stakeholder or decision-maker — write up the results, put together the findings brief, or draft the readout for a board, exec, or VP. Composes the brief from the evidence on hand and makes every claim carry its provenance and status, so open questions stay open and the verdict is carried, not smoothed into a confident story. Detects: "write up my findings", "findings brief", "communicate the results", "summarize this analysis for <stakeholder>". For orienting use groundwork; the request-to-decision is requirements-interrogator; the metric definition is kpi-contract; the code behind a number is review-my-query; rehearsing the defense is defend-my-number; and if the number comes straight from an inherited source whose definitions you have NOT validated (a proc/query/export's output), audit the assumptions first with audit-my-assumptions — brief only a finding whose inputs are vetted. It never computes or re-derives numbers, never manufactures a finding the evidence doesn't support, and never writes the final stakeholder-facing deck or email.
allowed-tools: Read, Write
---

# brief-my-findings

The colleague who helps you write up what you found: every number in the brief carries its evidence, every open question stays open, and nothing gets smoothed to make the story land.

## When to use
Fire when the analysis is done and the question is "how do I communicate this" — write up the findings, put together the brief, draft the readout for a board / exec / VP. Triggers: "write up my findings", "findings brief", "communicate the results", "summarize this analysis for <stakeholder>", "draft the readout", "how do I present what I found".
Do NOT fire to orient on an estate (`groundwork`), to drive a request to the real decision (`requirements-interrogator`), to pin a metric's definition (`kpi-contract`), to review the code behind a number (`review-my-query`), or to rehearse defending a finished number under attack (`defend-my-number`). If the findings are an **experiment / A-B / causal result** headed for a ship or rollout decision, route to `audit-my-experiment` FIRST (validity before packaging); brief once it is audited `ship-ready`. **Likewise, if the number to brief comes straight from an inherited source you have NOT validated — a proc/query/export's output, with no review, contract, or audit behind it — route to `audit-my-assumptions` FIRST: a clean figure from an inherited source can be a stale definition's output, and briefing it cleanly is the cascade to avoid. Brief once its inputs are vetted.** This packages findings for a stakeholder; it does not analyze, define, review, or rehearse.

**This vs. its neighbors.** brief COMPOSES the write-up — one pass, one artifact (`findings-brief.md`) — from already-vetted findings. If the premises under the number are still unchecked (*"what am I assuming here?"*) → `audit-my-assumptions` first. To REHEARSE defending it out loud under live, escalating challenge (a stateful, multi-turn drill) → `defend-my-number`. Same room, different jobs.

## The trap this exists to beat
Asked to "write up the findings," a capable assistant produces a clean, well-structured brief — and that is the problem. Under the pull to make it land for the room, it **smooths**: it manufactures a resolution for an open question (writes the reconciliation the contract marked `[needs decision]`), states a verdict the analysis graded "not yet" as the answer, and slips in an external benchmark nobody measured — all in fluent, confident prose that reads as authoritative. The more context it is handed, the more it over-claims. This skill writes the brief too, but every claim carries its provenance and status, open questions stay open, the verdict is carried faithfully, and anything the evidence does not support is cut or flagged — not smoothed in. It briefs; it does not embellish.

## The loop
1. **Gather the evidence base** — take the findings to communicate. If a `knowledge-base/` exists, read what backs the brief: `kpi-contract.md` (the locked definitions), `query-review.md` (what is validated / still broken), `defense-sheet.md` (what held / cracked + the readiness verdict), `decisions.md`, `open-questions.md` (the `[needs decision]`s), `purpose.md` (the decision this informs), `data-quality.md` (caveats). Build the brief FROM these; do not run fresh analysis. No findings in hand? Wrong skill — the analysis comes first (hand back to the analysis work or `groundwork`). **Provenance gate — before composing anything:** if the headline number's load-bearing premises are unexamined — whether it came straight from an inherited source (a proc/query/export's output) OR is your own fresh/long-trusted analysis with no review, contract, or assumption-audit behind it — no `query-review.md`, no locked `kpi-contract.md`, no `assumption-register.md` — STOP and route to `audit-my-assumptions` first. A clean, unremarkable figure is exactly what a stale inherited definition produces; do not brief a number whose inherited assumptions were never audited.
2. **Anchor to the decision + audience** — what decision this informs, who is in the room (exec / technical / board), what register. The brief serves the decision, not a data dump.
3. **Build the claim ledger (the engine)** — for every claim the brief will make, fix `claim · source · status · qualifier`, status one of Supported / Directional-only / `[Open - needs decision]` / Inferred (rubric in `references/brief-craft.md`). A claim with no source is cut or demoted to an open question. A `[needs decision]` stays `[Open]`. The readiness verdict is carried as-is. **A figure travels with its qualifier or it is `[Open]`: an *estimate* that arrived with an interval/n/scope keeps it (dropping it is laundering); an *exact* full-population count carries its base and scope but needs no interval. Never compute a missing interval — that's `[Open]`, not estimated.** (estimate-vs-exact test in `references/brief-craft.md`)
4. **Compose the brief** — observation → implication → action → watch-for, anchored to the decision, calibrated to the audience, every line backed by the ledger. A dedicated "What is still open / not yet sayable" section quarantines the `[Open]` items. Confidence language matches status: directional is not certified.
5. **Emit + thread** — write `findings-brief.md` (template in `references/findings-brief.md`). If a `knowledge-base/` exists, append `timeline.md`, route any newly-exposed open question to `open-questions.md`, and let the watch-for items feed `defend-my-number`. **No KB? Write the one artifact and keep the routing notes inside it** (`groundwork` can stand up a KB so the next brief builds on this). Then stop.

## The signature output: the claim-to-evidence ledger
Every claim the brief makes, tied to its source and graded by status — the analog of `kpi-contract`'s fork log and `review-my-query`'s graded findings. A polished writer makes the story flow; this makes every line answer "says who?": *NRR is 108% [Supported: kpi-contract + query-review]; it has not been reconciled to Finance [Open - needs decision]; the recommendation is not yet defensible [verdict carried: not yet].* Status rubric and a worked brief live in `references/brief-craft.md`.

## Bright lines (non-negotiable; inherits groundwork's read-only line)
- **Never compute, re-derive, or recompute a number for the brief.** Report what the analysis found; a figure not in the evidence is `[Open]`, not estimated. ("Let me just recompute to be sure" → stop; that is the analysis lane.)
- **Never manufacture a finding, interpretation, or reconciliation the evidence does not support** to make the story land. A `[needs decision]` stays open; an unexplained gap is reported as unexplained.
- **Carry the verdict faithfully.** A "not yet" is not a conditional yes; directional is not certified. Do not upgrade confidence to make the recommendation cleaner.
- **Surface, don't render.** Author the internal brief (`findings-brief.md`); do not write the final stakeholder-facing deck, email, or slides — that medium is the user's.
- **No claim without provenance.** Every statement traces to a finding / contract fork / KB file / analyst-supplied figure, or it is cut or flagged as an assumption.
- **Don't brief an unvetted inherited number.** A figure straight from an inherited source (a proc/query/export's output) with no review / contract / audit behind it routes to `audit-my-assumptions` FIRST; brief only vetted inputs. Packaging a stale-definition number cleanly is exactly the cascade this and `audit-my-assumptions` exist to stop.
- **A figure travels with its qualifier, or it is `[Open]`.** The interval (for an estimate), the denominator/base, and the measurement-scope caveat ride with the number — dropping a qualifier the figure *arrived* with is laundering. Carry it into the brief and instruct that it stay attached on the slide; never compute a missing one (that's `[Open]`).

Violating the letter is violating the spirit: a confident-prose explanation of an unresolved gap, or a conditioned recommendation written as the answer, both defeat the brief.

## Register (light)
Experienced user: terse, lead with the decision and the recommendation's status, batch the Supported claims, foreground the open items. New user: walk observation → implication → action → watch-for and explain why each claim's status is what it is. Either way, never re-state what is settled in `decisions.md` — carry it.

## Anti-evasion table
| Thought | Reality |
|---|---|
| "I'll explain the gap so the brief reads cleanly." | If it is `[needs decision]`, it stays `[Open]`. Explaining an unresolved gap in confident prose is manufacturing a finding. |
| "The recommendation is basically supported, I'll state it." | Carry the verdict. If the analysis graded it "not yet" / wobbled, the brief says so. A conditioned recommendation written as the answer is over-stating. |
| "A benchmark will give the board context." | If nobody measured it, it is not a finding. No claim without provenance; cut it or mark it Inferred. |
| "I'll just write the polished board deck for them." | Surface, don't render. The internal brief is yours to author; the final stakeholder medium is theirs. |
| "I'll recompute this to be sure before I write it." | Read-only. The brief reports what the analysis found; you do not re-derive numbers. |
| "This number was validated, so I'll present it as certified." | Status matches evidence. Directional-only stays directional; only what is reconciled / validated reads as certified. |
| "The ±/n/scope clutters the slide — I'll drop it." | That's estimate-laundering: a soft number read as hard. The qualifier rides with the figure; keep it and instruct it onto the slide. A figure whose interval/base/scope you can't state is `[Open]`, not a clean number. |

## Red flags — STOP if you think these
| Thought | Reality |
|---|---|
| "Let me make the story land." | The honest brief is the deliverable; smoothing is the failure mode. |
| "I'll fill the gap with a reasonable interpretation." | Open stays open. |
| "I'll add a number for context." | No claim without provenance. |
| "I'll draft the actual slides / email." | Stop at the internal brief; the final medium is the user's. |

## References (load on demand)
- `references/brief-craft.md` — the claim-ledger engine, the status rubric, audience calibration, the observation→implication→action→watch-for shape, and a worked Meridian brief done right. Load when building the ledger (loop step 3).
- `references/findings-brief.md` — the Findings Brief artifact template + how it composes into the knowledge base.
