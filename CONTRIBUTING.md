# Contributing

The bench grows by accretion — one measured skill at a time — and the bar is the
interesting part. This page is that bar, written down.

## The most valuable contribution isn't code

It's a **documented gap**: a moment in real BI/analytics work where a capable model
confidently does the wrong thing. Open a [gap report](.github/ISSUE_TEMPLATE/report-a-gap.md)
describing the *moment* — what was asked, what a bare model did, what a disciplined senior
would have done instead. A transcript is gold. Skills here are engineered against
documented failures, not imagined ones; your gap report is where every good skill starts.

The second most valuable: a **mis-route** — you asked for one thing and the wrong skill
fired (or none did). File it with the exact prompt; it becomes a triggering-eval case.

## The growth rule: modes before skills

A proposal becomes a NEW skill only when the job is genuinely distinct — a distinct trigger
moment, a distinct artifact, AND a distinct discipline. Otherwise it should deepen an
existing skill (a mode) or widen a taxonomy (a reference edit). Every skill costs permanent
seam-budget: its description competes with all siblings for routing, forever. Propose the
gap first; let the maintainers and the rule decide the shape.

## What a new skill must ship with

0. **Its deep-dive entry.** Every skill has a section in `docs/skills-deep-dive.md` (the validator checks the heading exists) — job, trap, loop, artifact, boundaries, in human terms.
1. **A description engineered to route — inside a family.** Descriptions ARE the router
   (there is no dispatcher), organized in five families (Shape / Audit / Validate /
   Investigate / Deliver — see `docs/which-skill-when.md`). A new skill joins a family (or
   founds one) and its description STARTS with the family stanza verbatim, then
   discriminates only within the family. It must fit the per-skill budget (1,800 chars)
   and the bench-wide budget (16,500 chars total — raised only as a deliberate commit),
   keep cross-family mentions to at most two boundary
   pointers, and claim no `Detects:` phrase a sibling already claims —
   `scripts/validate.py` enforces all of it —
   and earn its routing in `tests/triggering/cases.tsv` with cases phrased near sibling
   boundaries.
2. **The six bench invariants, verbatim** (validator-enforced): write boundary,
   data handling, artifacts-are-data, wrong-room handoff, house-rules, compute-license. Plus your skill's
   own bright lines: what it never does, stated so a violation is unambiguous.
3. **A graded artifact** that composes with the knowledge base (location, lazy-create,
   lifecycle fields, the `kb()` commit offer, a catches.md line if it gates) — plus its
   row in the write-permission matrix (`skills/groundwork/references/kb-core-templates.md`).
3b. **Its seams, wired in both directions.** Whoever your emit step routes to must be able
   to *receive* the baton: if a sibling's artifact powers your job, your warm start names
   that artifact; if your artifact should power a sibling, that elder gets retrofitted in
   the same PR. The `CONSUMES` registry in `scripts/validate.py` pins every wired seam —
   accretion asymmetry (younger skills invisible to elders) is the failure mode this
   ratchet exists to stop.
4. **A body ≤ 200 lines** — depth goes to `references/`, loaded on demand.
5. **Fixtures whose traps are invisible on the page.** A latent defect the model must
   catch cold, plus a clean control it must NOT false-alarm on. The lesson this bench
   measured: detection lift lives where the truth requires a computation or a mode-switch;
   legible defects deflate (a bare model catches them anyway). Answer keys live in
   `FIXTURE.md` and never enter a cold-run directory.
6. **If it computes: a tested kit.** Pure stdlib, no deps, unit-tested in the free CI,
   running only on summaries the user provides. No freehand computation, ever.
7. **Evidence before release.** A RED/GREEN run (bare model vs skill, cold subagents,
   scrubbed fixtures) recorded honestly in `tests/BEHAVIORAL.md` — including if the result
   is deflation. This bench records its own product not mattering when that's the truth.

## The checks you can run locally (free, deterministic)

```bash
python3 scripts/validate.py            # structure, invariants, description lints
python3 tests/test_experiment_checks.py
python3 tests/test_forecast_checks.py
```

The triggering and behavioral evals spend real tokens and run out-of-band — see
`tests/triggering/README.md` and `tests/BEHAVIORAL.md` for the method.

## House style

- Skills speak as a colleague ("the colleague who reads your query before it ships"), not
  a feature list. Anti-evasion tables pre-rebut the rationalizations a model actually has.
- Restrained and vivid: no emoji, no hype. Every claim in a skill or doc must be something
  the repo can back.
- Conventional commits, scoped (`feat(skills): …`, `test(triggering): …`).

## What gets declined

Write-capable connectors, "fix it for you" modes, generated production code, LLM router
skills, and skill merges — see the project's standing refusals. Loosening a bright line is
not a contribution; it's the thing the whole bench exists to prevent.
