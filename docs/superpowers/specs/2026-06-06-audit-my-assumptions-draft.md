---
name: audit-my-assumptions
description: Use when a BI/analytics professional is about to BUILD or EXTEND something on top of existing sources — rebuild a report from stored procs, derive a new metric from an inherited query, stack years onto an old workbook, re-point a model at a new table — and wants the silent assumptions in those sources surfaced and validated BEFORE building, so a stale or wrong inherited premise doesn't cascade into a plausible-looking wrong output. Surfaces every inherited filter/grain/unit/date-basis/identity/constant as an explicit, numbered assumption; grades each by blast radius; falsifies the load-bearing ones against the most generative source (including the population's trend over time, not just the window); and routes intent-type assumptions to the owner. Detects: "I'm rebuilding this report from these procs", "before I build on this", "what am I assuming here", "is it safe to derive from this", "validate the inputs before I start", "help me not inherit a bad assumption". Fires UPSTREAM of the build. For a number already known wrong use triage-my-number; for pinning a metric's meaning use kpi-contract; for reviewing one code object use review-my-query; for auditing a whole knowledge base use kb-reconcile. It never builds the deliverable, runs the source, or guesses an intent — it excavates, grades, falsifies, and routes.
allowed-tools: Read, Write
---

# audit-my-assumptions

The colleague who makes you write down what you're taking for granted before you build a quarter of work on top of it — then tries to break the load-bearing ones while it's still cheap.

## When to use
Fire when you are about to **build or derive** on top of something you did not author and fully verify: rebuild a report from inherited stored procs, derive a new metric from an existing query, stack more years onto an old workbook, re-point a model at a new source. The question is "what am I silently assuming, and which of those assumptions would poison everything if it's wrong?" — asked **before** the build, not after a stakeholder squints at the output.
Do NOT fire when a number is already in hand and known wrong (that's `triage-my-number`, downstream), to pin what a metric should mean (`kpi-contract`), to review one code object against a contract (`review-my-query`), or to audit a whole accreted knowledge base (`kb-reconcile`). This one runs at the **front** of the work, on the inputs.

## The trap this exists to beat
Asked to "rebuild this from the existing procs" or "derive X from this query," a capable assistant does the build well — and **inherits every silent premise in the source as fact**. It copies the package definition, the magic exclusion list, the date filter, the unit a column is in, because that is "what the proc does" — and ships a plausible output resting on an assumption it never named, that may be stale, wrong, or built for a different purpose years ago. The cascade is invisible precisely because the output *looks* right: a wrong foundational assumption doesn't error, it produces a confident, well-formatted, wrong number that only a domain expert catches, late. A second, related failure: it **validates a load-bearing premise against a derivative** (the prior report, an inline reconstruction) or with a **whole-table sum** instead of the generative source on the matching scope — so the check passes while the assumption is still wrong. This skill refuses to build on an un-excavated premise. It inventories the inherited assumptions, grades them by blast radius, tries to *falsify* the load-bearing ones against the most authoritative source it can reach — including the population's behavior **over time**, where a regime change hides — routes the intent-type ones to the owner, and only then declares the foundation safe to build on.

## The loop
1. **Inventory the inherited premises.** For each source you will build on (proc, query, export, prior report, doc), extract every decision it makes *silently*: the population filter (what's in / out), the grain (one row = what), the **unit each measure is in** (is "Revenue" really revenue, or cost-in-a-swap?), the **date/period basis** (order vs fulfilment vs as-of), the **identity key** (does `ItemLabel` mean one property?), the magic constants and exclusion lists, the joins that could fan out, the swaps. Each becomes a numbered assumption with a verbatim cite. Inherited ≠ verified.
2. **Grade by blast radius.** For each: *if this is wrong, how much of the output is poisoned?* **Trunk** = grain / population / unit / period-basis / identity (a wrong one cascades through everything). **Leaf** = a label, a format, a cosmetic. Rank trunks first; that is where the validation budget goes.
3. **Classify how each can be settled.** **Verifiable** against a source (code / data / the system of record) vs **Decision** — a matter of *intent* only the owner can settle (order-vs-fulfilment default, whether a sub-item rolls into its parent category, whether to surface a thing). Never silently resolve a Decision; never assume a Verifiable.
4. **Falsify the load-bearing ones.** Try to *break* each trunk assumption, against the most generative source you can reach — **live system > generative code > windowed export > hand-touched workbook**. Three sharp checks: (a) **trend, not snapshot** — profile the feeding population *over time*; a structural break means your premise about what the data contains is obsolete (a window hides it); (b) **triangulate** — derive a load-bearing fact two independent ways and see if they agree; (c) **anchor honestly** — never validate a premise against a derivative, never validate a filtered metric with a whole-table sum, and always separate *"matches the source"* (verifiable) from *"correct for the business"* (needs the human).
5. **Route the underivable.** Every Decision-type assumption and every "can't verify from here" becomes an explicit owner question. Do **not** build past a load-bearing open; flag it as gating.
6. **Emit the register + the seam checks.** Write `assumption-register.md`: each assumption — statement (with cite), blast-radius (trunk/leaf), how-settled (verifiable/decision), status (**VERIFIED / ASSUMPTION / FALSIFIED / NEEDS-DECISION**), and the evidence or the exact check to run. Plus the **boundary tie-outs** you'd run at each derivation seam (source → export → your query → output) so a bad assumption announces itself where it entered. Then stop — you cleared the foundation; you did not pour the building.

## The signature output: a graded assumption register
A numbered ledger of every inherited premise, ranked by blast radius, each marked VERIFIED / ASSUMPTION / FALSIFIED / NEEDS-DECISION with its evidence or its discriminating check — the analog of `kpi-contract`'s fork log and `review-my-query`'s graded findings, but pointed *upstream* at the inputs. The point is the **trunk** assumptions: the few whose failure cascades, validated (or falsified) against the generative source before a line of the deliverable is built.

## Bright lines (non-negotiable; inherits groundwork's read-only line)
- **Inherited is not verified.** Never treat a filter / constant / definition / unit as fact because the source encodes it. The source is authoritative for *what it computes*, never that it is current or right for *your* question.
- **Never silently resolve an intent.** A Decision-type assumption (what the owner means) is a question, not a guess you build around.
- **Anchor to the most generative source.** Never validate a premise against a derivative (a prior report, an inline reconstruction), and never validate a filtered metric with a whole-table sum. Match scope and basis.
- **Look across time, not just the window.** A regime change — a population that changed shape — is invisible in a slice. Profile the trend before you trust the definition.
- **Surface and validate; do not build.** You clear the foundation and hand back the register; you do not author the report on top of an unvalidated trunk. (The moment you're building the deliverable, this skill is over — hand to the build.)

Violating the letter is violating the spirit: copying the proc's logic "because that's what it does," or blessing a trunk assumption off the prior report, both defeat the audit.

## Register (light)
Experienced user: terse — lead with the trunk assumptions and their status, batch the leaves, name the gating Decisions. New user: walk each inherited premise, explain *how* a wrong one would cascade and what the cheapest falsifying check is, one at a time, trunks first. Either way, never re-litigate what `decisions.md` already settled.

## Anti-evasion table
| Thought | Reality |
|---|---|
| "The proc defines packages as `BUNDLEID IS NOT NULL` — I'll use that." | That's an inherited assumption, not a fact. Surface it; check whether it still holds before building a year of work on it. |
| "This window shows ~no packages, so packages are negligible." | A slice hides a regime change. Profile the population *by year* — a structural break means the definition went stale, not that the thing disappeared. |
| "I'll reconcile against the existing report / the inline-prod reconstruction." | That's a derivative, not the anchor. A consistent derivative can be uniformly wrong. Anchor to the generative source. |
| "Total = `SUM(col)` matches, so we're good." | Don't validate a filtered metric with a whole-table sum. Match the scope and the date basis, or the check lies. |
| "The doc says the customer price lives in the PACKAGE table." | An inherited claim is a hypothesis to falsify, not a fact to forward. Check it against the source before you depend on it. |
| "I'll just default 'Year' to fulfilment year / roll a sub-item in / pick the grain." | That's a Decision, not derivable. Ask the owner; mark it gating, don't guess. |
| "It all ties out, ship it." | Ties out to *what*, on *which basis*? Name the anchor and the scope, or "ties out" is meaningless. |
| "There are too many assumptions to check." | That's why you grade by blast radius. Validate the few trunks; let the leaves ride — but name them all. |

## Red flags — STOP if you think these
| Thought | Reality |
|---|---|
| "It's what the proc does." | Inherited ≠ validated. Excavate it, grade it, check it. |
| "Close enough, let me start building." | An unnamed trunk assumption is the cascade waiting to happen. Clear the foundation first. |
| "The number looks plausible." | Plausible is the failure mode — an invisible bad assumption produces a confident wrong number. |
| "I'll figure out what they meant." | Intent isn't derivable. Route the Decision to the owner. |

## References (load on demand)
- `references/blast-radius.md` — the trunk-vs-leaf taxonomy (grain / population / unit / date-basis / identity / constants), the falsification checks (trend / triangulate / anchor), and the worked example (the "promo bundles fell 95%" inherited-definition + regime-change miss).
- `references/assumption-register.md` — the register artifact template + how it composes into the knowledge base and hands off to the build.
