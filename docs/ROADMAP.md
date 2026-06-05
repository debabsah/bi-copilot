# Analytics-office bench — vision roadmap

_Living doc. Last updated 2026-06-05._

## Guiding filter
Cover the analytics ladder **where the base model reliably fails** — failure-proneness, *not* coverage-completeness (completeness for its own sake is a vanity metric). The **green-red gap** is the signal: build where a bare model, under a consumption ask, commits a real error a skill prevents. Measure on the **deployment tier (Sonnet)**, not the strongest model — an over-powered control hides the gap. A skill that only re-encodes what a strong model already does adds consistency/structure, not failure-prevention.

Recurring shape of a high-lift skill: a **consumption→audit switch** (kb-reconcile, audit-my-experiment) that forces the *check* the model skips — especially the **computational checks it eyeballs**, not the conceptual defects it already recites.

## Coverage map (the ladder)

| Layer | Question | Coverage | Status |
|---|---|---|---|
| Descriptive | what happened | kpi-contract, review-my-query, brief-my-findings, model-contract | ✅ |
| Diagnostic | why did it move | triage-my-number | ✅ |
| Governance | can we trust the record | kb-reconcile, groundwork, requirements-interrogator | ✅ |
| Inferential / causal | does X cause Y | **audit-my-experiment** — experiment validity; also flags observational-causal traps | 🟡 partial |
| Predictive | what will happen | — | ⬜ open |
| Prescriptive | what should we do | — | ⬜ open |

_Cross-cutting (off-ladder): **defend-my-number** — rehearse defending a finished number; companion to brief-my-findings. Bench = **10 skills**._

## Open frontier (prioritized by likely green-red gap)
1. **Forecasting / backtest hygiene** (Predictive) — *best next candidate; unprobed.* Likely a **computational** gap (train/test leakage, no out-of-sample validation, ignored regime change) — the same shape as SRM. Probe latent, on Sonnet, before designing.
2. **Causal-inference-from-observational** (Inferential) — partially covered by audit-my-experiment's interpretation checks (confounding / Simpson's / regression-to-mean). A *dedicated* skill is likely **low-lift** — probe evidence shows conceptual causal defects are base-model-robust at both tiers. Probe before building.
3. **Prescriptive** (what should we do — optimization / decision policy) — unprobed; furthest from the bench's current "get the number right and defensible" identity. Possibly a sibling product.

## Parked engineering threads (not new skills)
- **Bench de-narration + honest `BEHAVIORAL.md`** — *highest-value unactioned item.* The existing non-auditor fixtures **narrate their own traps**, so they test compliance, not detection, and can't show failure-prevention lift. De-narrate (bury the landmine so the model must detect it), re-bank RED/GREEN on the Sonnet tier, and update `BEHAVIORAL.md` to mark verified-vs-specified and record the deployment-tier reality.
- **RED-test the remaining skills on the Sonnet deployment tier.**

## Method note
Probes use cold `general-purpose` subagents with the fixture + skill pasted **inline** (hermetic — no filesystem, so no repo answer-keys leak), on the deployment model. Default probe/RED target: **Opus** for the "is even the strongest model weak here?" go/no-go; **Sonnet** to measure deployment-tier value (Opus holding never clears Sonnet).

## Provenance / evidence
- Inferential-frontier probe (17 runs): `~/bi-copilot-design-archive/ab-frontier-probe/2026-06-05-verdict.md`
- Sonnet deployment sweep + latent-fixture probe: `~/bi-copilot-design-archive/sonnet-deployment-sweep/`
- audit-my-experiment: spec `docs/superpowers/specs/2026-06-05-audit-my-experiment-design.md` · plan `docs/superpowers/plans/2026-06-05-audit-my-experiment.md`
- agentmemory: `mem_mq0ta6pm` (A/B resolved + shipped) · `mem_mq0p0ceo` (handoff) · `mem_mq0oiwou` (validation lessons)
