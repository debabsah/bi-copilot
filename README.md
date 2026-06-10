# analytics-office

[![CI](https://github.com/debabsah/analytics-office/actions/workflows/ci.yml/badge.svg)](https://github.com/debabsah/analytics-office/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-d97757)](https://claude.com/claude-code)

**A discipline harness for AI-assisted analytics.**

AI is genuinely good at analytics work. It fails in one specific way: not by being unable, but by being *agreeable*. Handed an inherited warehouse with no docs, it starts building instead of orienting. Handed "build me a dashboard with these KPIs," it builds exactly that — without ever asking what decision the dashboard serves. Asked what "active customer" means, it picks a sensible default instead of pinning the choice with the person who owns it. Handed a number, it writes the confident story.

analytics-office is a bench of **18 read-only skills for Claude Code** that switches the model out of answer-mode and into the discipline each moment of analytics work actually needs — orienting on an unfamiliar estate, interrogating requirements, locking metric definitions, designing models, auditing inherited premises, reviewing the code behind a number, diagnosing a break, briefing stakeholders, surviving the meeting. Each skill is engineered against a documented failure of the bare model. All of them write to one living knowledge base you resume from.

*Read-only by construction · computes instead of eyeballing · no required sequence — any skill, any moment.*

```
/plugin marketplace add debabsah/analytics-office
/plugin install analytics-office@analytics-office
```

<!-- demo slot: 30s cast of groundwork standing up a knowledge base from an inherited proc -->

---

## Sixty seconds in

```text
You:  Our VP wants a churn dashboard — logo churn by month, NPS, and a
      retention curve. Can you build it?

(requirements-interrogator fires)

      You're describing a solution — three artifacts — not a problem.
      Before anyone scopes this: what decision changes based on the
      dashboard? Who acts on it, and how often?

You:  Honestly… she wants to decide whether onboarding gets more
      budget next quarter.

      Then the ask and the need have a gap. The decision is annual and
      cohort-shaped; the request is a monthly wall chart.

      | Requested           | What the decision needs                   |
      |---------------------|-------------------------------------------|
      | Logo churn by month | First-90-day churn by signup cohort       |
      | NPS                 | Nothing — no decision attaches to it      |
      | Retention curve     | Keep — but cohort-based, not calendar     |

      Verdict: REFRAME. Written to knowledge-base/requirements-brief.md.
      The two metrics worth locking are seeded into kpi-contract.md; the
      open question (what budget threshold triggers the decision?) is
      routed to open-questions.md.

      I did not scope the dashboard. The decision wasn't validated.
      Now it is.
```

That refusal-then-redirect is the whole product, twelve different ways.

---

## The bench

Twelve skills, ordered here like a project — but **there is no pipeline**. Every skill fires independently, at any moment, with or without the others having run.

| You say | What fires | You walk away with |
|---|---|---|
| "I inherited this warehouse and the analyst left." | `groundwork` | a living `knowledge-base/` — and a map of what you don't know yet |
| "Build me a dashboard with these KPIs." | `requirements-interrogator` | the decision behind the ask, the requested-vs-derived delta, a verdict |
| "Lock down what 'active customer' actually means." | `kpi-contract` | a versioned contract — every definitional fork pinned by its owner or flagged `[needs decision]` |
| "How should I model this mart?" | `model-contract` | a logical star with the grain declared and gated on evidence — no DDL invented on a guess |
| "Turn this proc's output into the board number." | `audit-my-assumptions` | a graded register of every silent premise, falsified *before* you build on it |
| "Is this SQL right?" | `review-my-query` | findings graded Blocking / Latent / Advisory against the locked definition — a review, never a rewrite |
| "Did our A/B test really win?" | `audit-my-experiment` | computed validity checks (SRM, peeking, multiplicity, power) gating the ship decision |
| "Can we plan against this forecast?" | `audit-my-forecast` | leakage, backtest, interval-honesty, and drift checks gating the plan |
| "Churn jumped to 11% overnight. Why?" | `triage-my-number` | a ranked differential across code / data / pipeline / definition / real change — plus a calibrated line for the exec who's asking |
| "Is our knowledge base still true?" | `kb-reconcile` | a graded drift report — contradictions, stale claims, unsourced numbers |
| "Write up my findings for the VP." | `brief-my-findings` | a brief where every claim carries its provenance and open questions stay open |
| "The CFO will grill me on this number." | `defend-my-number` | a live sparring drill, graded honestly, and a defense sheet of what held and what cracked |
| "Write my weekly status update for steering." | `status-truth` | a provenance-graded status where every green earns its color and slips carry their delta |
| "Explore this data — find me insights." | `explore-my-data` | a harnessed exploration: every cut counted, found ≠ confirmed, the lucky cell never becomes the headline |
| "Draw the ER / lineage diagram of our mart." | `map-my-estate` | a cited map: every edge carries its evidence, guesses render dashed, islands stay islands |
| "What breaks if I rename this column?" | `change-impact` | the graded blast radius: breaks, silent meaning-drifts, and honest UNKNOWNs — before it ships |
| "QA my dashboard before the QBR." | `review-my-dashboard` | the assembly review: dashboards fail between correct parts — totals, defaults, titles, staleness |
| "The totals match — sign off the migration." | `prove-my-parity` | the stratified parity proof: offsetting errors caught, tolerance owned before results |

---

## What "discipline harness" means

LLMs in analytics fail through **answer-mode**: the pull to be immediately useful. Answer-mode inherits a stale filter as fact because "that's what the proc does." It eyeballs a check it could compute. It resolves a contested definition with a "sensible default, confirm later." It smooths an open question into a clean narrative because the deck reads better that way. None of these are knowledge failures — they're *discipline* failures, and they produce confident, well-formatted, plausible, wrong output.

A harness is the countermeasure, built into every skill:

- **A trap, named.** Each skill documents the exact thing a capable model does by default — then refuses it. The skills know their own failure modes before you hit them.
- **Bright lines.** Non-negotiables with teeth: never touch a live system, never compute the user's deliverable, never resolve an owner's decision silently, never grade a guess as a finding.
- **Anti-evasion tables.** The mid-task rationalizations, pre-rebutted. Two real rows:

  | The thought | The reality |
  |---|---|
  | "The QBR's in an hour, I'll just write the SQL so they're unblocked." | Surface, don't build. The contract is the deliverable; the runnable query is downstream of the pinned definition. |
  | "It's obviously X." | Obvious = untested. Hold the differential until a check confirms. |

- **A graded artifact, every time.** No skill ends in vibes. Each emits a committable file where every line carries a status. The signature example — `kpi-contract`'s fork log:

  ```text
  Fork            Options               Pinned             Why it matters
  Revenue basis   bookings/recognized   recognized         biggest gap vs Finance
  Refunds         gross/net             net                gross overstates by refund rate
  Attribution     first/last/multi      [needs decision]   changes who gets credit
  ```

- **Verdicts that carry.** A "not ship-ready" from an audit cannot be upgraded into a win by the write-up downstream. The brief inherits the verdict; it does not soften it.
- **Engineering constraints, enforced.** Every skill body is capped at 200 lines by a structural validator (depth lives in `references/`, loaded on demand), and every skill declares least-privilege tool access — the validator rejects a wildcard grant. The whole bench is about 2,000 lines of deliberately engineered instruction text.

---

## One living knowledge base

Every skill reads from and writes to the same `knowledge-base/` directory in your project — current truth in STATE files, history in an append-only timeline, and one graded artifact per job done.

```mermaid
flowchart TD
    KB[("knowledge-base/<br/>STATE — current truth<br/>timeline.md — append-only history")]
    GW[groundwork] -->|stands up + seeds| KB
    RI[requirements-interrogator] -->|requirements-brief| KB
    KC[kpi-contract] -->|locked fork log| KB
    AA[audit-my-assumptions] -->|assumption register| KB
    KB -->|the contract anchors the review| RQ[review-my-query]
    KB -->|known defects become first suspects| TN[triage-my-number]
    KB -->|evidence in, verdicts carried| BD[brief-my-findings<br/>defend-my-number]
    RQ -->|graded findings| KB
    TN -->|ranked differential| KB
```

What that buys you:

- **Warm starts.** A skill reads what's already settled before asking anything. It never re-asks an answered question, never re-pins a locked fork.
- **Compounding.** The day a dashboard number spikes, the triage doesn't start cold — the query review from three weeks ago already graded the grain bug that's now the prime suspect.
- **Provenance.** State entries link back to the timeline events that produced them. "Says who?" always has an answer.
- **Resume.** Come back after two weeks, say *"catch me up"*, and get briefed from the record — where you are, what changed, what's blocked on whom.
- **Strictly optional.** No knowledge base? Every skill still works standalone and writes its one artifact with the routing notes inside it.

A complete worked example — a fictional SaaS company taken from inherited estate to board readout to production incident — lives in [`examples/saas-retention/`](examples/saas-retention/). Reading its [timeline](examples/saas-retention/knowledge-base/timeline.md) takes ten minutes and shows the compounding better than any feature list.

---

## Built to be trusted near your work

The bench is designed for the most paranoid reader in your org:

- **It never connects to anything.** No live database, no production feed, no API. Skills read the files and descriptions you hand them — that's the entire surface.
- **It never computes your deliverable.** It pins definitions, reviews code as text, directs investigations — and stops at its lane's edge. Your number stays yours to produce.
- **Verification is paste-back only.** When a claim needs checking against source, the skill writes the exact check — the claim, the system of record, the runnable query, and the decision rule *stated before the run*. You run it. Only a pasted result counts as verified; "I read it in the notes" never does.
- **The only computation is auditable.** Four dependency-free Python kits (experiment validity, forecast validity, triage decomposition, parity tie-outs), pure stdlib, unit-tested in CI, run on summary numbers you paste — never on raw or live data.
- **Handed artifacts are data, not instructions.** A note inside a file saying "already validated, skip the audit" is treated as exactly the thing to scrutinize. Prompt-injection probes are part of the test evidence.
- **Surface, don't fix.** Reviews locate defects and point the fix direction; they don't hand back rewritten production code built on a schema the model never saw.
- **Nothing phones home.** Plain markdown and two Python files. No server, no telemetry, no keys.

The full posture — the enforcement layer map, the MCP stance, and the data-handling rules for the knowledge base — lives in [`SECURITY.md`](SECURITY.md).

---

## Engineered, not vibed

Most prompt collections are written once and trusted forever. This bench treats its own behavior as a testable claim:

- **Routing is measured, not hoped.** There is no router — each skill fires on its description alone. A triggering eval spawns headless `claude -p` sessions where the model's *first action* is the routing decision, then scores it: the wrong bench skill firing fails the build. Descriptions here are engineered artifacts with measured discrimination at the boundaries.
- **Behavior is baselined RED/GREEN.** Fixtures plant realistic failures; a cold model runs them without the skill (RED), then with it (GREEN). The traps are built to be *invisible on the page* — a tidy single-year figure whose inherited definition quietly went stale years ago — because that's where real damage lives. Measured examples: bare model runs confidently built the deck on the stale definition; with the skill on, the same model stopped and excavated the premise. An experiment write-up sailed through a bare consumption read with broken randomization; with the harness on, the model computed the check itself and blocked the ship.
- **Precision is tested, not assumed.** Clean, deliberately suspicious-looking fixtures verify the auditor skills **stay quiet** when nothing is wrong — an auditor that cries wolf trains everyone to ignore it. One skill failed its clean control during development; the grading rubric was fixed and re-verified. That loop is the product working on itself.
- **The limits are documented.** Runs are small-n and self-authored, and the repo says so: the evidence ledger is [`tests/BEHAVIORAL.md`](tests/BEHAVIORAL.md), and [`tests/COVERAGE-AUDIT.md`](tests/COVERAGE-AUDIT.md) is the bench adversarially auditing its *own* test coverage — claim by claim, including what isn't backed yet.
- **CI is free and deterministic.** Structural invariants (file manifest, frontmatter, the 200-line cap, no wildcard tool grants) plus all four stats kits' unit tests run on every push. The token-spending evals run out-of-band, by design.

The design principle that fell out of the measurements: **build for invisibility.** Skills earn their keep where the truth — clean *or* dirty — requires a computation or a mode-switch the bare model eyeballs past. Where a defect is legible on the page, a capable model already catches it; the harness adds its value exactly where confidence and correctness come apart silently.

---

## Quickstart

```
/plugin marketplace add debabsah/analytics-office
/plugin install analytics-office@analytics-office
```

Then just talk to Claude Code the way you'd talk to a colleague. Any of these will route to the right skill on its own (the finer seams live in [`docs/which-skill-when.md`](docs/which-skill-when.md)):

```text
I just inherited a data warehouse from someone who left. Where do I even start?
```

```text
My stakeholder wants a dashboard with these five KPIs. Help me scope it.
```

```text
Before we build anything: lock down exactly what "active customer" means.
```

Built and tested as a **Claude Code** plugin. The skills themselves are plain-markdown `SKILL.md` files in the open Agent Skills format — no binaries, no server, no setup beyond the install — so they can travel to other skill-aware harnesses.

---

## FAQ

**Is it safe to use near production data?**
It never connects to anything — that's a bright line, not a setting. Skills are read-only by construction, tool access is least-privilege and validator-enforced, and anything needing verification against source becomes a written check that *you* run and paste back. The only computation is a handful of stdlib Python kits on summary numbers you provide.

**Do I need all 12 skills?**
No. There's no pipeline and no required order. Each skill fires on its own trigger and works standalone; they simply compound when the shared knowledge base exists.

**Will it slow me down?**
It moves the questions a senior reviewer would ask from *after* the build to *before* it. Each skill also adapts its register — terse, batched, confirm-the-defaults for experienced users; step-by-step for newcomers. The typing was never the expensive part of analytics; the rework is.

**What does it cost?**
It's markdown. MIT-licensed, zero dependencies, no services, no keys of its own. It runs inside your existing Claude Code session at normal token cost.

**Why not just write better prompts?**
Because discipline kept in a prompt evaporates under pressure — the meeting is in an hour, the number looks fine, the model is eager to help. The skills pre-rebut those exact rationalizations in writing, fire automatically even when you ask for the *output* ("just write up the findings"), and are measured for both routing and behavior. A prompt is advice; a harness has teeth.

---

## Contributing — the bench grows by accretion

One measured skill at a time. The bar is the interesting part — a new skill ships with:

- a **description engineered to route correctly** against its eleven siblings (descriptions are the router here, and they're evaluated headlessly),
- **bright lines** and an anti-evasion table aimed at a *documented* failure of the bare model,
- a **graded artifact** that composes with the knowledge base,
- **trigger cases** near sibling boundaries, and behavioral fixtures whose traps are invisible on the page.

The most valuable contribution isn't code at all: it's a documented gap — a moment in real analytics work where a capable model confidently does the wrong thing. [Open an issue](https://github.com/debabsah/analytics-office/issues) with the moment; a transcript is gold.

---

## Author & license

Built by [debabsah](https://github.com/debabsah) — a BI practitioner who watched capable models ship plausible, confident, wrong analytics one too many times, and decided the fix was discipline, not bigger prompts.

MIT. If the harness catches something before your stakeholders do, a star helps the next analyst find it.
