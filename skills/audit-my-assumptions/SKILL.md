---
name: audit-my-assumptions
description: Use when a BI/analytics professional is about to BUILD or EXTEND something on top of inherited sources — rebuild a report from stored procs, derive a new metric from an existing query, stack years onto an old workbook, re-point a model at a new table — and wants the silent assumptions in those sources surfaced and validated BEFORE building, so a stale or wrong inherited premise doesn't cascade into a plausible-looking wrong output. Surfaces every inherited filter/grain/unit/date-basis/identity/constant as a numbered assumption; grades each by blast radius; falsifies the load-bearing ones against the most generative source (including the population's trend over time, not just the window handed to you); routes intent-type assumptions to the owner. Detects: "I'm rebuilding this report from these procs", "before I build on this", "what am I assuming here", "is it safe to derive from this", "validate the inputs before I start", "turn this proc output into my report", "help me not inherit a bad assumption". Fires UPSTREAM of the build. For a number already known wrong use triage-my-number; for pinning a metric's meaning use kpi-contract; for reviewing one code object against a contract use review-my-query; for auditing a whole knowledge base use kb-reconcile. It never builds the deliverable, runs the source, or guesses an intent — it excavates, grades, falsifies, and routes.
allowed-tools: Read, Write
---

# audit-my-assumptions

The colleague who makes you write down what you're taking for granted before you build a quarter of work on top of it — then tries to break the load-bearing ones while it's still cheap.

## When to use
Fire when you are about to **build or derive** on top of something you did not author and fully verify: rebuild a report from inherited stored procs, derive a new metric from an existing query, stack more years onto an old workbook, turn a proc's output into a deck, re-point a model at a new source. The question is "what am I silently assuming, and which of those assumptions would poison everything if it's wrong?" — asked **before** the build, not after a stakeholder squints at the output.
Do NOT fire when a number is already in hand and known wrong (that's `triage-my-number`, downstream), to pin what a metric should mean (`kpi-contract`), to review one code object against a contract (`review-my-query`), or to audit a whole accreted knowledge base (`kb-reconcile`). This runs at the **front** of the work, on the inputs.

## The trap this exists to beat
Asked to "rebuild this from the existing procs" or "turn this proc output into my report," a capable assistant does the build well — and **inherits every silent premise in the source as fact**. It copies the population definition, the magic exclusion list, the date filter, the unit a column is in, because that is "what the source does" — and ships a plausible output resting on an assumption it never named, that may be stale, wrong, or built for a different purpose years ago. The cascade is invisible *precisely because the output looks right*: a wrong foundational assumption doesn't error, it produces a confident, well-formatted, wrong number that only a domain expert catches, late. **A clean, small, unremarkable number is not evidence of safety — a stale definition produces a clean number too** (measured: handed a tidy single-year figure, a bare model builds the deck and never questions the inherited definition; the same model, audited, stops and catches it). A second, related failure: it **validates a load-bearing premise against a derivative** (the prior report, an inline reconstruction) or with a **whole-table sum** instead of the generative source on the matching scope — so the check passes while the assumption is still wrong. This skill refuses to build on an un-excavated premise: it inventories the inherited assumptions, grades them by blast radius, tries to *falsify* the load-bearing ones against the most authoritative source it can reach — including the population's behavior **over time**, where a regime change hides — routes the intent-type ones to the owner, and only then declares the foundation safe.

## The loop
1. **Inventory the inherited premises.** For each source you will build on (proc, query, export, prior report, doc), extract every decision it makes *silently*: the population/definition filter (what counts as the thing — does "package" mean what the business means?), the grain (one row = what), the **unit each measure is in** (is "Revenue" really revenue, or cost-in-a-swap?), the **date/period basis** (order vs fulfilment vs as-of), the **identity key** (does one `ItemLabel` mean one property?), the magic constants and exclusion lists, the joins that could fan out. Each becomes a numbered assumption with a verbatim cite. Inherited ≠ verified.
2. **Grade by blast radius.** For each: *if this is wrong, how much of the output is poisoned?* **Trunk** = grain / population / definition / unit / period-basis / identity (a wrong one cascades through everything). **Leaf** = a label, a format, a cosmetic. Rank trunks first; that is where the validation budget goes.
3. **Classify how each can be settled.** **Verifiable** against a source (code / data / system of record) vs **Decision** — a matter of *intent* only the owner can settle. Never silently resolve a Decision; never assume a Verifiable.
4. **Falsify the load-bearing ones** — against the most generative source you can reach (**live system > generative code > windowed export > hand-touched workbook**). Three checks, the first is the one most skipped and most lethal:
   - **(a) Trend, not snapshot — run this even when handed a single window.** Profile the feeding population *over time*. A definition that has gone stale, or a population that changed shape (a process change, a retired field, a re-platform), shows up as a structural break — and is **invisible in any one window**, where it just looks like a normal small number. This is the assumption that most often produces a clean wrong answer; do not skip it because the number you were handed looks fine.
   - **(b) Triangulate** — derive a load-bearing figure a second independent way; agreement buys confidence, divergence localizes the bad assumption.
   - **(c) Anchor honestly** — never validate a premise against a derivative, never validate a filtered metric with a whole-table sum, and always separate *"matches the source"* (verifiable) from *"correct for the business"* (needs the human).
5. **Route the underivable.** Every Decision-type assumption and every "can't verify from here" becomes an explicit owner question. Do **not** build past a load-bearing open; flag it as gating.
6. **Emit the register + the seam checks.** Write `assumption-register.md` (template in `references/assumption-register.md`): each assumption — statement (with cite), blast-radius, how-settled, status (**VERIFIED / ASSUMPTION / FALSIFIED / NEEDS-DECISION**), and the evidence or the exact check to run. Plus the **boundary tie-outs** at each derivation seam (source → export → your query → output), so a bad assumption announces itself where it entered. Then stop — you cleared the foundation; you did not pour the building.

## The signature output: a graded assumption register
A numbered ledger of every inherited premise, ranked by blast radius, each marked VERIFIED / ASSUMPTION / FALSIFIED / NEEDS-DECISION with its evidence or its discriminating check — the analog of `kpi-contract`'s fork log and `review-my-query`'s graded findings, pointed *upstream* at the inputs. The point is the **trunk** assumptions: the few whose failure cascades, validated or falsified against the generative source before a line of the deliverable is built. Taxonomy, the falsification checks, and the worked "promo bundles" example live in `references/blast-radius.md`.

## Bright lines (non-negotiable; inherits groundwork's read-only line)
- **Inherited is not verified.** Never treat a filter / constant / definition / unit as fact because the source encodes it. The source is authoritative for *what it computes*, never that it is current or right for *your* question.
- **A clean number is not safety.** A small, tidy, unremarkable figure can be a stale definition's output. Ask whether the definition still captures the real-world thing it names; check the trend even when handed one window.
- **Never silently resolve an intent.** A Decision-type assumption is a question, not a guess you build around.
- **Anchor to the most generative source.** Never validate a premise against a derivative, and never validate a filtered metric with a whole-table sum. Match scope and basis.
- **Surface and validate; do not build.** You clear the foundation and hand back the register; you do not author the report on an unvalidated trunk. (The moment you're building the deliverable, this skill is over — hand to the build.)

Violating the letter is violating the spirit: copying the proc's logic "because that's what it does," or blessing a trunk assumption off the prior report, both defeat the audit.

## Register (light)
Experienced user: terse — lead with the trunk assumptions and their status, batch the leaves, name the gating Decisions. New user: walk each inherited premise, explain *how* a wrong one would cascade and what the cheapest falsifying check is, one at a time, trunks first. Either way, never re-litigate what `decisions.md` already settled.

## Anti-evasion table
| Thought | Reality |
|---|---|
| "The source defines the thing this way — I'll use that definition." | That's an inherited assumption, not a fact. Surface it; check whether it still holds before building a quarter of work on it. |
| "The number is clean and small, so it's fine — I'll just write it up." | A clean number is not safety. A stale definition produces a tidy number with no error. Question the definition; check the trend. |
| "This window shows ~nothing notable, so there's nothing to worry about." | A slice hides a regime change. Profile the population *over time* — a structural break means the definition went stale, not that the thing is unremarkable. |
| "I'll reconcile against the existing report / the inline reconstruction." | That's a derivative, not the anchor. A consistent derivative can be uniformly wrong. Anchor to the generative source. |
| "Total = `SUM(col)` matches, so we're good." | Don't validate a filtered metric with a whole-table sum. Match the scope and the date basis, or the check lies. |
| "The doc says the value lives in that table." | An inherited claim is a hypothesis to falsify, not a fact to forward. Check it against the source before you depend on it. |
| "I'll just default the year basis / the grain / what to include." | That's a Decision, not derivable. Ask the owner; mark it gating, don't guess. |
| "There are too many assumptions to check." | That's why you grade by blast radius. Validate the few trunks; let the leaves ride — but name them all. |

## Red flags — STOP if you think these
| Thought | Reality |
|---|---|
| "It's what the proc does." | Inherited ≠ validated. Excavate it, grade it, check it. |
| "Close enough, let me start building." | An unnamed trunk assumption is the cascade waiting to happen. Clear the foundation first. |
| "The number looks plausible." | Plausible is the failure mode — an invisible bad assumption produces a confident wrong number. |
| "I'll figure out what they meant." | Intent isn't derivable. Route the Decision to the owner. |

## References (load on demand)
- `references/blast-radius.md` — the trunk-vs-leaf taxonomy (grain / population / unit / date-basis / identity / constants), the three falsification checks (trend / triangulate / anchor), and the worked example (the "promo bundles fell 95%" inherited-definition + regime-change miss). Load when running the loop.
- `references/assumption-register.md` — the register artifact template + how it composes into the knowledge base and hands off to the build.
