# Changelog

Notable changes to the analytics-office bench. Versions follow the plugin manifest;
commit-level detail lives in git history.

## [0.17.0] — 2026-06-11

Structural release, no new skill — **family-structure routing** (the wall comes down):

- The 15 descriptions reorganize into four families — **Shape** (groundwork,
  requirements-interrogator, kpi-contract, model-contract), **Audit** (the three audits,
  review-my-query, kb-reconcile), **Investigate** (triage-my-number, explore-my-data,
  map-my-estate), **Deliver** (brief-my-findings, defend-my-number, status-truth). Each
  member's description opens with its family's shared stanza (validator-enforced
  verbatim); members discriminate only within the family; cross-family mentions are capped
  boundary pointers. A structured no-router — the bet is preserved, the O(n^2) bounded.
- The always-in-context description budget drops **15,779 -> 12,675 chars** (both prior
  cap raises undone; caps now 1,800/skill and 13,000 total), with every previously-passing
  Detects phrase preserved verbatim.
- The validator's skill-count wall is replaced by the family registry: every skill belongs
  to exactly one family, at most 6 members per family (a 7th forces a split decision), all
  lints RED-proven.
- Measured before/after on two models (the default plus a Sonnet-4.6 sensitivity baseline)
  plus a pure-bench probe: Sonnet intra-bench defects 5 -> 3; both kpi-contract known
  seams PASS pure-bench under family structure (their real-env failures are
  shadow-interaction, not description defects); one stanza retuned within the bounded fix
  budget after "the estate needs seeing" proved to be magnet vocabulary. Full story in
  tests/triggering/README.md.

## [0.16.0] — 2026-06-10

- **map-my-estate** (15th skill — provenance-graded cartography): ER and lineage views in
  mermaid where every edge cites its evidence (FK in DDL, a join in code, documented
  lineage, an attributed owner statement — never name similarity or a prefix convention);
  unsupported edges render dashed `[unverified]`, islands stay labeled islands, and every
  map ships its derived-from set, edge ledger, and coverage line — so the map doubles as a
  coverage picture of the record, and `kb-reconcile`'s new `map-staleness` drift type can
  flag it when the record moves on. Ships with the fabricated-edges trap + evidenced-map
  control and banked evidence (recorded honestly: the fourth consecutive detection
  deflation on the current frontier model — the lift is the canonical artifact form).
  Carries the second budget raise (14,900 → 15,800) **and the wall**: the validator now
  fails the build beyond 15 skills until family-structure routing lands.

## [0.15.0] — 2026-06-10

- **explore-my-data** (14th skill — the daily-est analyst moment, harnessed): open-ended
  exploration with pre-registration before looking, the cut counter (N cuts ⇒ ~N/20
  expected false hits, stated next to any striking pattern), magnitude-and-base before
  significance, found-vs-confirmed via pre-specified hold-outs the user runs, robust-vs-
  lucky tests, and dead ends recorded. Ships with the dredge-bait trap + robust-pattern
  control and banked RED/GREEN evidence (recorded honestly: detection fully deflates on
  the current frontier model — the lift is the registration/cut-log/pass-bar artifact
  structure). Carries the bench's first deliberate description-budget raise (14,000 →
  14,900); family-structure routing is due before ~skill 16.

## [0.14.0] — 2026-06-10

- **status-truth** (13th skill — opens the BI Program Manager persona): composes the
  status report from the record so the truth survives the pull to look green. The
  provenance-graded ledger (Done-evidenced / In-progress-attributed / Slipped-with-delta /
  Blocked-with-age / Risk-open / Unknown—asked), honest RAG against stated criteria with
  the watermelon test, expired verdicts routed back to their audits, re-bases named as
  re-bases, and positivity pressure recorded rather than obeyed. Ships with the
  watermelon-status trap + healthy-status control fixtures and banked RED/GREEN evidence
  (recorded honestly: detection deflates on a legible record; the lift is the ledger
  structure and color discipline).

## [0.13.0] — 2026-06-10

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
- **Routing re-baselined on the new default model** (full 31-case sweep): 18 pass, 3
  misroutes documented as known seams (preserved in `cases.tsv`, details in
  `tests/triggering/README.md`), 6 shadows / 4 misses (environment-dependent). Four
  description-surgery rounds could not move the seams without regressing passing foils;
  recorded honestly and filed for the next hardening pass.

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
