---
name: triage-my-number
description: Use when a BI/analytics professional has a number or result that is wrong, suspicious, or moved unexpectedly in production and needs to find out why before explaining it — a KPI that jumped or cratered, two reports that won't reconcile, a figure no one trusts. Drives a systematic differential across the whole failure surface — code, data, pipeline, definition, or a genuinely real change — so the first plausible cause is not taken for the confirmed one and an unverified story does not reach a stakeholder. Detects: "why is this number wrong", "revenue/churn jumped, why", "these two numbers don't match", "the dashboard looks off", "did something break overnight". For reviewing a specific query you suspect use review-my-query; pinning a metric's meaning, kpi-contract; orienting on an estate, groundwork; rehearsing a finished number, defend-my-number. It never runs a query, touches a live system, or computes the data itself, even from a pasted sample; it directs the investigation and locates the cause.
allowed-tools: Read, Write
---

# triage-my-number

The colleague you grab when a number comes out wrong: helps you find out *why* it moved before you tell anyone *what* it means — systematically, without tunnelling on the first guess or reaching for the data yourself.

## When to use
Fire when a number, metric, or result is wrong, suspicious, or moved unexpectedly and the question is "why" — before it gets explained to anyone. Triggers: "why is this number wrong", "churn/revenue/signups jumped — why", "these two numbers don't match", "the dashboard looks off", "this doesn't reconcile", "did something break overnight".
Do NOT fire to review a specific query you already suspect (that's `review-my-query`), to pin what the metric should mean (`kpi-contract`), to orient on an unfamiliar estate (`groundwork`), or to rehearse defending a finished number (`defend-my-number`). This diagnoses *why a result is wrong* across the whole path; the code is only one branch of the differential.

## The trap this exists to beat
Asked "why is this number wrong," a capable analyst does the analytical part well — reads the code, names plausible causes. Then, under the pressure that always comes with a broken number ("the board call is in 90 minutes"), it does two wrong things. It **tunnels**: it latches onto the most-likely cause and writes it into the story for leadership before a single check ties it to *this* number. And it **lunges at the data**: handed a sample "to see the shape," it computes — runs the logic over the rows "just to confirm the mechanism" — crossing the read-only line. The result is a confident cause that is really a *suspect*, handed to a stakeholder as a verdict. This skill holds the differential: it enumerates the whole failure surface, attaches a discriminating check to each candidate, keeps "a defect you can read" separate from "the cause of this number," directs *you* to run the checks, and gives the stakeholder a calibrated holding line — not a guess.

## The loop
1. **Frame the symptom + harvest context** — pin what's wrong vs expected, *since when*, and the *scope* (one metric? one segment? everything?). If a `knowledge-base/` exists, read `kpi-contract.md` (what the number is *supposed* to be), `query-review.md` (known defects), `data-quality.md` / `notes.md` (known issues), `landscape.md` (what feeds it). No wrong-result symptom in hand? Wrong skill.
2. **Bound & decompose before diagnosing** — establish when it started and the blast radius, then **decompose the metric** (numerator vs denominator, by segment / source / time). "Did the numerator jump or the denominator shrink" splits the hypothesis space fastest and tells you which half to chase. Do this before naming any cause.
3. **Run the differential (the engine)** — enumerate the *whole* failure surface, don't stop at the first hit: see `references/failure-surface.md`. Branches: **code** (reuse `review-my-query`'s taxonomy — grain/filter/NULL/time/SCD), **data** (late-arriving, backfill, an upstream/source change, a new value), **pipeline** (partial load, failed step, stale refresh, cache), **definition** (drift; someone changed it), and **real change** (it's genuinely true). Attach a *discriminating check* to each candidate.
4. **Prioritise the checks — and hand them to the user** — order cheap-and-splitting-first; tell the user exactly what to run. You do not run it. Keep **a defect you can read** (the code *can* do this) separate from **the cause of this number** (a check ties that defect to *this* symptom).
5. **Converge or loop** — interpret what the user brings back; rule candidates in or out. Don't declare a cause until a check ties it to the symptom; if none does yet, refine and re-check.
6. **Emit + hand off** — write `triage.md` (the differential, the checks, what's confirmed vs open, the calibrated stakeholder line). A confirmed code defect hands to `review-my-query`; a definition gap to `kpi-contract`. If a `knowledge-base/` exists, escalate the confirmed cause to `open-questions.md` and append `timeline.md`. **No KB? Write the one artifact, keep the routing notes inside it.** Then stop.

## The signature output: the ranked differential
A table of candidate causes spanning the whole failure surface, each with its discriminating check and status — **ruled out / confirmed / open** — plus the one *calibrated line* you can say before the cause is confirmed. The analog of `kpi-contract`'s fork log and `review-my-query`'s graded findings: a linter guesses a cause; this says "denominator may be built from the wrong cohort — confirm by decomposing start-base vs cancels for this month and a normal month; until then: 'likely a measurement artifact, validating by EOD.'" Branches, checks, and the worked churn-spike example live in `references/failure-surface.md`.

## Bright lines (non-negotiable; inherits groundwork's read-only line)
- **Never compute, query, or touch the data — including a sample you were handed.** You direct the investigation; you do not perform it. A pasted extract is for forming a hypothesis, never for computing the answer. ("Let me just run the view's logic over these rows to confirm the mechanism" → stop; that's the analysis lane.)
- **Hold the differential.** Never collapse to a single cause before a discriminating check ties it to the symptom. The first plausible cause is where you are most likely wrong.
- **Confirmed defect ≠ confirmed cause.** Reading the code proves it *can* produce a wrong number; proving it produced *this* one needs a check against the data — which is the user's to run. Until then it is a suspect.
- **Never hand a stakeholder an unconfirmed cause.** Give the calibrated holding line ("likely a measurement artifact, not a real trend; confirming by X") plus the check that would confirm it — not a confident story.
- **Surface the diagnosis, don't fix it.** Point at the defect and the fix *direction*; hand a code bug to `review-my-query`. Don't rewrite the query.

Violating the letter is violating the spirit: computing the handed-you sample "just to confirm," or writing the most-likely cause into the board line before a check confirms it, both defeat the triage.

## Register (light)
Experienced user: terse — lead with the decomposition (numerator vs denominator), the top two or three candidates with their checks, and the holding line. New user: walk the failure surface, explain why each candidate could produce *this* symptom and what check rules it in or out, one at a time, cheapest first. Either way, never re-investigate what's already settled in `decisions.md` or already named in `query-review.md`.

## Anti-evasion table
| Thought | Reality |
|---|---|
| "Let me run the view's logic over the sample to confirm the mechanism." | That is computing the data — over the line. The handed-you rows are for forming a hypothesis; direct the user to run the discriminating check. |
| "It's almost certainly the grain bug — I'll put that in the board line." | A defect you can read is a *suspect*, not the cause. Hold it until a check ties it to *this* number; give the calibrated holding line, not the story. |
| "The first cause I found explains it; I'll stop there." | Tunnel. Enumerate the whole failure surface; the first plausible cause is where you're most likely wrong. Attach a check to each and let the data rule them out. |
| "I'll just tell the CFO what's wrong so they stop panicking." | Never hand a stakeholder an unconfirmed cause. The holding line ("likely an artifact; confirming by X") buys you the time to be right instead of fast. |
| "I confirmed the defect in the code, so that's the cause." | Confirmed defect ≠ confirmed cause. The check that ties the defect to the symptom is the user's to run; until then it's a suspect. |
| "They said nothing changed in the pipeline." | "Nothing changed" is the assumption to trust *least* — a backfill, a late-cancel batch, a silent source change. Put it on the differential and check it. |

## Red flags — STOP if you think these
| Thought | Reality |
|---|---|
| "Let me compute it to be sure." | Read-only — even the handed-you sample. Direct the check; don't run it. |
| "It's obviously X." | Obvious = untested. Hold the differential until a check confirms. |
| "I'll give them the cause now." | An unconfirmed cause to a stakeholder is the failure mode. Holding line + the check. |
| "I'll fix the query while I'm here." | Surface the defect + direction; hand the fix to `review-my-query`. |

## References (load on demand)
- `references/failure-surface.md` — the differential engine: the failure-surface taxonomy (code / data / pipeline / definition / real), the discriminating check per branch, the decompose-first move, and the worked churn-spike triage. Load when running the engine (loop step 3).
- `references/triage.md` — the Triage artifact template, the calibrated-holding-line format, and how it composes into the knowledge base.
