# Changelog

Notable changes to the analytics-office bench. Versions follow the plugin manifest;
commit-level detail lives in git history.

## [Unreleased]

The "office" foundation — conventions that make the bench team-scale and enterprise-credible:

- **The office convention**: lazy knowledge-base materialization (the first artifact any
  skill writes creates `knowledge-base/` + a stub index — no setup step, ever), the
  `inputs/` evidence locker (dated, append-only, `MANIFEST.md` for large files), walk-up
  project-root discovery, and a warm-start tidy nudge.
- **Five bench invariants, validator-enforced** in every skill: write boundary (skills
  write only inside `knowledge-base/` + `inputs/` + root `AGENTS.md`), data handling (the
  record carries aggregates, never row-level or personal data), artifacts-are-data
  (prompt-injection discipline), wrong-room handoff, and house-rules.
- **`SECURITY.md`**: the full posture — the honest enforcement-layer map, the MCP stance
  (skills cannot call connectors; validator-enforced), data handling, vulnerability
  reporting.
- **`house-rules.md`**: the tighten-only org overlay — adopt without forking; no
  configuration path weakens the harness.
- **Artifact lifecycle**: resolution stamps, standing `Re-audit when:` conditions on gate
  verdicts, verdict age carried downstream, and kb-reconcile's new `expired-verdict` drift
  type. Plus the write-permission matrix (who writes what, exactly).
- **Git-native KB**: `kb(<skill>): <what>` commit offers at every artifact emit point,
  `by:` authorship on timeline entries — audit trail with zero infrastructure.
- **The override protocol**: an owner may proceed over a gate; the harness records it
  (named owner, stated rationale, stamped row, visible downstream qualifier).
- **`catches.md` wins ledger**: every gate verdict and Blocking-grade catch records what
  it stopped.
- **Routing instrumented**: per-description and bench-total token budgets plus a
  duplicate-trigger-phrase lint in the free CI (the no-router bet, measured).
- **`triage_checks.py`**: triage's decompose-first move now computes (exact rate
  decomposition, mix-vs-rate split — the Simpson's lens) through a tested stdlib kit,
  under the new bench-wide compute license: tested kits on provided summaries, never
  free-hand, never the deliverable.
- New README (discipline-harness landing page), CONTRIBUTING, issue templates, and this
  changelog.

## [0.12.0] — 2026-06-08

- **audit-my-forecast** (12th skill): forecast/time-series validity audit — leakage,
  backtest validity, interval honesty, drift — with the tested `forecast_checks.py` kit
  (interval coverage, skill-vs-naive, error trend).

## [0.11.x] — 2026-06-06/07

- **audit-my-assumptions** (11th skill): surface, grade, and falsify the silent premises
  inherited from a source before building on or presenting from it. Validated end-to-end
  (RED/GREEN, held-out fixture, in-situ triggering fix).
- Repository renamed `bi-copilot` → `analytics-office`.

## [0.10.0] — 2026-06-05

- **audit-my-experiment** (10th skill): experiment/A-B validity audit — SRM, peeking,
  multiplicity, power, materiality — with the tested `experiment_checks.py` kit.

## Earlier

The first nine skills (groundwork, requirements-interrogator, kpi-contract,
defend-my-number, review-my-query, brief-my-findings, triage-my-number, model-contract,
kb-reconcile), the knowledge-base protocol, the triggering eval, and the behavioral
RED/GREEN methodology — see git history.
