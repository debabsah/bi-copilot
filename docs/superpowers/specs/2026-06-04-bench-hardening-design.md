# Bench Operating-Characteristics Suite — design spec

_2026-06-04 · status: approved, pre-implementation · owner: debabsah_

## 1. Problem

The analytics-office bench (9 skills) was built RED→GREEN→REFACTOR. The `tests/COVERAGE-AUDIT.md`
audit showed the green checkmarks certify **existence, not operating characteristics**: each RED
proves a skill *can* catch its one planted trap once; nothing measures catch-rate across the claimed
failure space, false-alarm-rate on a clean record, or crack-rate when it should hold. Concretely:

- **Precision unmeasured (0/9).** Every fixture is a trap; nothing tests that a skill stays *quiet*
  on a clean record. For the 4 auditor skills (kb-reconcile, review-my-query, triage-my-number,
  defend-my-number) the false-positive rate is the trust-defining metric.
- **Banked runs 1/9.** Only kb-reconcile has a recorded RED/GREEN transcript in-repo; the other 8
  have unticked `- [ ]` checklists. Cross-cutting evidence exists only out-of-repo in
  `~/bi-copilot-design-archive/`.
- **Breadth ~25–30%.** Fixtures instantiate a slice of each skill's taxonomy (kb-reconcile 2/8,
  model-contract 2/13, kpi-contract ~5/18, groundwork 1/4).
- **Uninstantiated paths.** warm-start, prep-mode, composition-threading, triage confirmed-cause
  escalation are specced but never exercised.
- **n=1, teaching-to-the-test, thin routing** (4 skills have a single routing case; negatives all
  far-domain; the eval can pass vacuously).

## 2. Goals / non-goals

**Goal:** a reproducible, measured operating-characteristics suite so this never has to be
re-derived. Output: per-skill **catch-rate / false-alarm-rate / crack-rate / delta** tables, gated
in a re-runnable harness.

**Non-goals (deliberately bounded to avoid a combinatorial vanity exercise):**
- NOT 100% taxonomy-row coverage. Target **family-coverage** + every *Blocking*-severity row once.
- NOT eliminating teaching-to-the-test. Held-out adversarial fixtures attack it; the residual
  (same model family authoring) is a documented ceiling.
- NOT every composition permutation — a representative path fixture per pattern.

## 3. Repository layout (all in-repo — fixes the out-of-repo-evidence weakness)

```
tests/
  behavioral/
    run_behavioral_eval.py      # the harness; mirrors triggering/run_triggering_eval.py
    rubrics/<skill>.yaml        # per-fixture: required_catches, forbidden_fires, bright_lines
    results/<date>-<skill>.json # banked transcripts + grader verdicts
  fixtures/
    <existing trap fixtures>    # widened in place
    clean/<skill>/...           # NEW precision (hard-negative) fixtures
    adversarial/<skill>/...     # NEW held-out fixtures (workflow-authored)
    paths/<pattern>/...         # NEW cross-cutting path fixtures
  BEHAVIORAL.md                 # gains the measured tables (auto-updated by the aggregator)
  COVERAGE-AUDIT.md             # next-move boxes ticked with evidence links
docs/superpowers/specs/2026-06-04-bench-hardening-design.md   # this spec
```

The `~/bi-copilot-design-archive/` stays as historical record; new evidence lands in-repo.

## 4. Fixture design

Three kinds per skill, plus cross-cutting path fixtures. Breadth rows are scored from the *same*
transcript via the rubric, so widening a fixture is near-free once it is rich.

### 4.1 Trap (positive) — widen the high-stakes ones to Blocking-family coverage
- **kb-reconcile** (`drifted-kb`): add **decision-violated**, **status-rot**, **broken-provenance**
  instances alongside the existing partial-update + unsourced-number → ~5/8 drift types.
- **model-contract** (`unmodelled-mart`): add a **semi-additive measure** (additivity fork) and an
  **unconformed "customer"** (conformed-dims fork) beyond source-grain + SCD.
- **kpi-contract** (`unpinned-metric`): add **timezone**, **late-arriving/restatement**, and
  **renewal-attribution** forks explicitly.
- **review-my-query** (`unreviewed-query`): already 6/8 families; add a **set-logic** and an **SCD**
  defect to reach 8/8 if cheap.
- **triage-my-number** (`spiking-number`): add a **confirmed-cause** continuation (a pasted-back
  check result) so the "escalate only a confirmed cause" claim is positively exercised.

### 4.2 Clean (precision / hard-negative) — one per skill; PASS = stays quiet, manufactures nothing
Each is clean but *tempting* (carries the surface features that correlate with defects):
- **kb-reconcile** — consistent KB; a number that *looks* unsourced but the GL export *is* in the
  tree. PASS: "reconciled / verified where checkable"; no manufactured contradiction; the sourced
  number is not flagged unsourced.
- **review-my-query** — a query that conforms to the contract but is written in an odd style. PASS:
  "conforms", at most an Advisory; invents no Blocking.
- **triage-my-number** — a number that moved for a *real* reason. PASS: branches 1–4 ruled out by
  their checks, lands on "real change"; manufactures no artifact.
- **defend-my-number** — a genuinely solid, reconciled number. PASS: grades answers "held", concedes
  the strength, verdict "ready"; manufactures no crack.
- **kpi-contract** — a metric whose forks are genuinely already settled. PASS: confirms the pinned
  choices; fabricates no inapplicable forks; re-opens nothing settled.
- **model-contract** — a design whose grain is clear and evidenced. PASS: declares the grain and
  proceeds; invents no grain ambiguity or SCD drama.
- **requirements-interrogator** — an already-validated, decision-linked spec. PASS: recognizes it is
  validated, does not re-interrogate, does not flag a real decision-linked metric as vanity.
- **brief-my-findings** — findings that *are* supported (reconciled). PASS: grades them Supported,
  states plainly; does not over-demote to Directional or manufacture open items.
- **groundwork** — a small, already-well-documented estate. PASS: orients without manufacturing
  loose threads; does not over-instantiate the catalog. (Weakest precision analog; included for
  symmetry, gated only on "no manufactured gaps".)

### 4.3 Adversarial (held-out) — workflow-authored, public-description-only
For the 4 auditors first (kb-reconcile, review-my-query, triage-my-number, defend-my-number). A
trap-author agent sees only the skill's public `description` (SKILL.md frontmatter) + a domain
primer — never the `SKILL.md` body or reference taxonomy — and plants ≥1 defect of a named type plus
a **sealed answer-key** the runner never sees. This is the real attack on teaching-to-the-test.

### 4.4 Path fixtures (~5, cross-cutting)
- **warm-start:** a skill (e.g. requirements-interrogator) run with a populated `knowledge-base/`
  present → reads settled context first, does not re-ask answered questions.
- **prep-mode:** requirements-interrogator with the stakeholder absent → emits the question script
  with `[awaiting stakeholder]` markers, fabricates no answers.
- **composition-threading:** a skill with a KB present → threads `open-questions.md` /
  `decisions.md` / `timeline.md` and indexes in `README.md`.
- **confirmed-cause escalation:** triage + a pasted-back check that confirms a cause → escalates to
  `open-questions.md` / `timeline.md` (and nothing before confirmation).

**Count:** ~9 widened traps + 9 clean + ~6 adversarial + ~5 path ≈ **~29 fixtures**.

## 5. Measurement harness — `tests/behavioral/run_behavioral_eval.py`

Mirrors the existing triggering eval's design choices (neutral dir, headless cold runs, parse the
behavior).

- **Conditions per fixture:** `RED` (baseline, no skill) and `GREEN` (skill active). Traps expect
  RED→crack / GREEN→hold; clean fixtures' load-bearing metric is GREEN false-alarm (RED is a sanity
  baseline).
- **Neutral scrubbed dir:** copy the fixture to a throwaway dir with only the artifacts under test —
  no `FIXTURE.md`, no rubric, no answer-key (the scrub-the-construction-artifacts rule).
- **n:** **5** on load-bearing conditions — each skill's **bright-line GREEN**, each **precision
  (clean) GREEN**, and each **Blocking** required-catch — and **1–2** on routine Latent/Advisory
  breadth rows. `n` is the primary cost knob.
- **Rubric (`rubrics/<skill>.yaml`):**
  ```yaml
  required_catches:        # each must be caught for a GREEN pass
    - id: conformance-revenue-unit
      severity: Blocking   # Blocking gates; Latent/Advisory are reported
      location: "whole view"
  forbidden_fires:         # must NOT be claimed (precision)
    - "manufactured contradiction on a clean record"
  bright_lines:            # must NOT do
    - "executes or connects to a DB"
    - "writes a drop-in production query"
    - "edits the audited files"
  ```
- **Grader:** a model scores each transcript against the rubric — required_catches caught?
  forbidden_fires triggered? bright_lines held? **Two graders per transcript**, disagreements
  escalated to a third (the workflow's adversarial-review property). Spot human check on a sample.
- **Output tables (per skill, written to BEHAVIORAL.md + results/):** Blocking catch-rate,
  Latent/Advisory catch-rate (reported), false-alarm-rate, crack-rate (baseline), GREEN−RED delta,
  bright-line hold-rate, with n and variance.
- **Gate (exit nonzero, like the triggering eval):** FAIL if Blocking catch-rate < 100% **or**
  false-alarm-rate > 0 on a precision fixture **or** any bright-line breach. Latent/Advisory rates
  and small-n variance are reported, not gated.

## 6. Dynamic-workflow execution

The harness is the deterministic core; the workflow supplies independence + scale.

| Agent role | Sees | Produces |
|---|---|---|
| **trap-author** (×N, independent) | skill name + public description + domain primer only | adversarial fixture + sealed answer-key (stored outside the scrubbed dir) |
| **runner** (×conditions×n, parallel) | the scrubbed fixture + a realistic user prompt | the first-action transcript |
| **grader** (×2 per transcript) | transcript + rubric/answer-key | per-criterion verdict; disagreements escalate |
| **aggregator** | all verdicts | the tables → BEHAVIORAL.md + results/; ticks COVERAGE-AUDIT.md boxes |

**Launch:** user triggers via "create a dynamic workflow to run `tests/behavioral` per the spec" or
the **ultracode** effort setting; alternatively the parent session emulates with parallel `Agent`
subagents. Either way the script and rubrics are the reproducible artifact.

## 7. Decisions (the four flagged defaults, approved)

1. **Gate, don't just report** — fail on missed-Blocking, any false-alarm, or a bright-line breach.
2. **n = 5** load-bearing / **1–2** routine.
3. **All in-repo**; archive stays as history.
4. **Adversarial** for the 4 auditors; **~5 path fixtures** as listed.

## 8. Acceptance criteria (definition of done)

- [ ] 9/9 skills have a banked GREEN (catch) **and** a banked precision (no-false-fire) run, in-repo.
- [ ] Every Blocking-severity taxonomy row is exercised ≥1; families covered per skill.
- [ ] Measured catch-rate / false-alarm-rate tables in BEHAVIORAL.md, produced by the gated harness.
- [ ] Held-out adversarial passed for the 4 auditors.
- [ ] Routing thickened: ≥2 cases/skill, ≥1 near-domain negative, ≥1 positive-fire control.
- [ ] `tests/COVERAGE-AUDIT.md` next-move boxes ticked with links to the banked evidence.

## 9. Risks & mitigations

- **Grader reliability (model grading model):** two graders + escalation + a human spot-check on a
  sample; gate on the binary Blocking-catch (less noisy than fine grading).
- **Stochasticity at n=5:** report variance; gate only on must-catch/must-not-fire binaries.
- **Adversarial fixture quality (unfair or trivial traps):** sealed answer-key + a sanity pass that a
  competent human reviewer would call the trap fair.
- **Residual teaching-to-the-test:** held-out authoring is same-model-family; documented as the
  remaining ceiling, not claimed solved.
- **Cost (~250 cold runs):** `n` and staging (auditors first) are the knobs; the workflow's
  parallelism absorbs wall-clock.

## 10. References

- `tests/COVERAGE-AUDIT.md` — the audit this spec closes.
- `tests/BEHAVIORAL.md` — current checklists + kb-reconcile's banked evidence (the method template).
- `tests/triggering/run_triggering_eval.py` — the harness pattern to mirror.
- `~/bi-copilot-design-archive/` — historical cross-cutting REDs (consume, injection, citation,
  composition, poison).
- Dynamic workflows: claude.com/blog/introducing-dynamic-workflows-in-claude-code ·
  code.claude.com/docs/en/workflows
