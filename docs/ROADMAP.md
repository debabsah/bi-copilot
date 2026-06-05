# Analytics-office bench — vision roadmap

_Living doc. Last updated 2026-06-05._

## Guiding filter
Cover the analytics ladder **where the base model reliably fails** — failure-proneness, *not* coverage-completeness (completeness for its own sake is a vanity metric). The **green-red gap** is the signal: build where a bare model, under a consumption ask, commits a real error a skill prevents. Measure on the **deployment tier (Sonnet)**, not the strongest model — an over-powered control hides the gap. A skill that only re-encodes what a strong model already does adds consistency/structure, not failure-prevention.

Recurring shape of a high-lift skill: a **consumption→audit switch** (kb-reconcile, audit-my-experiment) that forces the *check* the model skips — especially the **computational checks it eyeballs**, not the conceptual defects it already recites.

**Confirmed 2026-06-05 (forecasting probe + bench de-narration, from both directions):** lift exists only where the defect is **invisible** — where a computed check is needed to surface it (the SRM chi-square). Where the defect is **legible** (its severity is on the page: a thin forecast margin, two mismatched revenue numbers, a code-vs-contract conformance breach) the base model catches it unaided and the skill only adds **structure**. So forecasting-audit deflated; review-my-query and brief-my-findings deflated. **Build for invisibility, not legibility.**

## Coverage map (the ladder)

| Layer | Question | Coverage | Status |
|---|---|---|---|
| Descriptive | what happened | kpi-contract, review-my-query, brief-my-findings, model-contract | ✅ |
| Diagnostic | why did it move | triage-my-number | ✅ |
| Governance | can we trust the record | kb-reconcile, groundwork, requirements-interrogator | ✅ |
| Inferential / causal | does X cause Y | **audit-my-experiment** — experiment validity; also flags observational-causal traps | 🟡 partial |
| Predictive | what will happen | — _(forecasting-audit probed → no-build, 2026-06-05)_ | ⬜ open |
| Prescriptive | what should we do | — | ⬜ open |

_Cross-cutting (off-ladder): **defend-my-number** — rehearse defending a finished number; companion to brief-my-findings. Bench = **10 skills**._

## Open frontier (prioritized by likely green-red gap)
1. **Forecasting / backtest hygiene** (Predictive) — **PROBED → no-build (2026-06-05, 9 runs).** The hypothesised SRM-shaped computational gap did NOT survive: the defect's severity (thin margin, config spread, no out-of-sample) is **legible in the reported numbers**, so bare Sonnet's caution tracks it rather than eyeballing past. Only residual corner: a truly-invisible latent leakage (a *trace-the-lineage* gap, not *run-the-check*) — lower-probability, unprobed. Verdict: `archive/forecasting-frontier-probe/`.
2. **Causal-inference-from-observational** (Inferential) — partially covered by audit-my-experiment's interpretation checks (confounding / Simpson's / regression-to-mean). A *dedicated* skill is likely **low-lift** — probe evidence shows conceptual causal defects are base-model-robust at both tiers. Probe before building.
3. **Prescriptive** (what should we do — optimization / decision policy) — unprobed; furthest from the bench's current "get the number right and defensible" identity. Possibly a sibling product.

## Parked engineering threads (not new skills)
- ~~**Bench de-narration + honest `BEHAVIORAL.md`**~~ — **DONE (2026-06-05).** Audit found only 2 of 10 fixtures actually narrated their own trap (review-my-query, brief-my-findings — the rest were already latent). De-narrated both; added a verified-vs-specified + narration ledger to `BEHAVIORAL.md`. Banked RED/GREEN on Sonnet: **both deflate** — bare Sonnet catches the legible defects and refuses to smooth; the skills add structure/discipline, not detection. Verdict: `archive/bench-de-narration/`.
- ~~**Precision / clean controls**~~ — **DONE + MEASURED (2026-06-05).** Built a hard-negative clean fixture per auditor skill (`conformant-query/`, `explained-movement/`, `solid-number/`, `consistent-kb/`) and ran GREEN-on-clean on Sonnet. **3/4 PASS** (kb-reconcile, triage-my-number, defend-my-number — stay quiet / well-graded Advisory). **review-my-query FAILED → FIXED** (next bullet). Verdict: `archive/precision-controls/`.
- ~~**Fix `review-my-query`'s grading rubric**~~ — **DONE + VERIFIED (2026-06-05).** Root cause: the skill's own worked example graded an unconfirmed schema fact (trials-in-`active`) Blocking — it taught block-on-assumption. Fixed (SKILL.md + failure-modes.md): Blocking only when established from what's in hand; schema-conditional → Latent/verify + the discriminating check + "→ Blocking if confirmed". Verified on Sonnet — conformant query now returns **no-Blocking (2/2, was 3)**, recall preserved (the trap fixture still gets 3 established Blockings + the correct "do not ship"). Verdict: `archive/review-my-query-precision-fix/`.
- **RED-on-clean for review-my-query** — confirm bare Sonnet also returns no-Blocking, i.e. the fixed skill no longer ADDS false positives vs the base model.
- **Held-out query for a fair review-my-query *recall* GREEN** — its worked example IS the current trap-fixture (`vw_monthly_churn`), so GREEN there is teaching-to-the-test.
- **Finish the `defend-my-number` drill interactively** — multi-turn, confirm it concedes a strong answer + reaches "ready".
- **RED-test the remaining (spec-only) skills on the Sonnet deployment tier.**

## Method note
Probes use cold `general-purpose` subagents with the fixture + skill pasted **inline** (hermetic — no filesystem, so no repo answer-keys leak), on the deployment model. Default probe/RED target: **Opus** for the "is even the strongest model weak here?" go/no-go; **Sonnet** to measure deployment-tier value (Opus holding never clears Sonnet).

## Provenance / evidence
- Inferential-frontier probe (17 runs): `~/bi-copilot-design-archive/ab-frontier-probe/2026-06-05-verdict.md`
- Sonnet deployment sweep + latent-fixture probe: `~/bi-copilot-design-archive/sonnet-deployment-sweep/`
- audit-my-experiment: spec `docs/superpowers/specs/2026-06-05-audit-my-experiment-design.md` · plan `docs/superpowers/plans/2026-06-05-audit-my-experiment.md`
- Forecasting-frontier probe (9 runs → no-build): `~/bi-copilot-design-archive/forecasting-frontier-probe/2026-06-05-verdict.md`
- Bench de-narration + payoff (7 runs → both deflate): `~/bi-copilot-design-archive/bench-de-narration/2026-06-05-verdict.md`
- Precision / clean controls (built + measured, 3/4 pass): `~/bi-copilot-design-archive/precision-controls/2026-06-05-verdict.md`
- review-my-query precision fix (verified: precision fixed, recall preserved): `~/bi-copilot-design-archive/review-my-query-precision-fix/2026-06-05-verdict.md`
- agentmemory: `mem_mq185ru6` (session-wrap D — review-my-query precision fixed) · `mem_mq17h3up` (C — precision controls) · `mem_mq16a302` (B — forecasting no-build + de-narration) · `mem_mq0tpabz` (A) · `mem_mq0ta6pm` (A/B resolved + shipped) · `mem_mq0oiwou` (validation lessons)
