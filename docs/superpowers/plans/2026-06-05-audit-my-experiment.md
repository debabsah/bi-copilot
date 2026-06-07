# audit-my-experiment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `audit-my-experiment` bench skill — a consumption→audit gate that *computes* (never eyeballs) experiment-validity checks via a bundled tested kit, then grades and gates the ship/brief decision.

**Architecture:** A bench skill (`skills/audit-my-experiment/`) following the established SKILL.md pattern, fronting a small **tested Python check-kit** (`references/experiment_checks.py`, stdlib-only) that the skill runs with `Bash`. Prose references (`validity-taxonomy.md`, `experiment-audit.md`) and the SKILL.md wrap the kit. Spec: `docs/superpowers/specs/2026-06-05-audit-my-experiment-design.md`.

**Tech Stack:** Python 3 stdlib (`math`, `statistics.NormalDist`) for the kit; Markdown for the skill/refs/fixtures; plain-`assert` test file runnable via `python3` (no pytest dependency).

**Spec deltas locked while planning (apply these, supersede the spec shorthand):**
- Kit module is `experiment_checks.py` (snake_case — importable).
- `srm_chisquare` returns a 3-level `verdict`: `srm` (p<0.0005) / `elevated` (p<0.01) / `ok`. Subtle case `[500000,502800]` → `elevated` (p≈0.0048), not a hard `srm`.

---

## File Structure

| File | Responsibility |
|---|---|
| `skills/audit-my-experiment/references/experiment_checks.py` | The tested kit: `chi2_sf`, `srm_chisquare`, `two_prop_z`, `multiplicity_correct`, `power_mde`, `peeking_flag`. Pure functions, stdlib only. |
| `tests/test_experiment_checks.py` | Known-answer tests for every kit function (incl. the probe SRM cases). Runnable standalone. |
| `skills/audit-my-experiment/references/validity-taxonomy.md` | The engine: design / inference / interpretation checklist. Prose. |
| `skills/audit-my-experiment/references/experiment-audit.md` | The `experiment-audit.md` artifact template + KB composition. Prose. |
| `skills/audit-my-experiment/SKILL.md` | The skill: trap, loop, signature output, bright lines, anti-evasion, references. |
| `tests/fixtures/unaudited-experiment/` | Eval fixtures: glaring-SRM, subtle-SRM, clean (false-alarm control). |
| `tests/BEHAVIORAL.md` | += `audit-my-experiment` dry-run entry. |
| `skills/brief-my-findings/SKILL.md`, `skills/defend-my-number/SKILL.md` | += one-line "route experiment-shaped inputs here first". |
| `README.md` | += panel row + skill section. |

---

## Task 1: Kit scaffold + `chi2_sf` numerical core

**Files:**
- Create: `skills/audit-my-experiment/references/experiment_checks.py`
- Test: `tests/test_experiment_checks.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_experiment_checks.py
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "audit-my-experiment", "references"))
import experiment_checks as ec

def test_chi2_sf_known_values():
    # dof=1 exact via erfc: chi2_sf(3.841,1) ~= 0.05
    assert abs(ec.chi2_sf(3.841459, 1) - 0.05) < 1e-3
    # chi2_sf(10.828,1) ~= 0.001
    assert abs(ec.chi2_sf(10.8276, 1) - 0.001) < 1e-4
    # chi2 <= 0 -> p = 1.0
    assert ec.chi2_sf(0.0, 1) == 1.0

if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fns:
        f(); print("PASS", f.__name__)
    print(f"\n{len(fns)} tests passed")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_experiment_checks.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'experiment_checks'`

- [ ] **Step 3: Write minimal implementation**

```python
# skills/audit-my-experiment/references/experiment_checks.py
"""Tested validity-check kit for the audit-my-experiment skill. Python stdlib only."""
import math
from statistics import NormalDist

_NORM = NormalDist()

def _gammq(s, x):
    """Regularized upper incomplete gamma Q(s, x) = 1 - P(s, x). Stdlib-only."""
    if x < 0 or s <= 0:
        raise ValueError("domain error in _gammq")
    if x == 0:
        return 1.0
    if x < s + 1.0:  # series for P(s,x); Q = 1 - P
        ap, total, delta = s, 1.0 / s, 1.0 / s
        for _ in range(1000):
            ap += 1.0
            delta *= x / ap
            total += delta
            if abs(delta) < abs(total) * 1e-14:
                break
        return 1.0 - total * math.exp(-x + s * math.log(x) - math.lgamma(s))
    tiny = 1e-300  # continued fraction for Q(s,x)
    b, c, d = x + 1.0 - s, 1.0 / 1e-300, 1.0 / (x + 1.0 - s)
    h = d
    for i in range(1, 1000):
        an = -i * (i - s)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny: d = tiny
        c = b + an / c
        if abs(c) < tiny: c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-14:
            break
    return math.exp(-x + s * math.log(x) - math.lgamma(s)) * h

def chi2_sf(chi2, dof):
    """Upper-tail survival p-value for a chi-square statistic."""
    if chi2 <= 0:
        return 1.0
    if dof == 1:
        return math.erfc(math.sqrt(chi2 / 2.0))  # exact
    return _gammq(dof / 2.0, chi2 / 2.0)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tests/test_experiment_checks.py`
Expected: `PASS test_chi2_sf_known_values` / `1 tests passed`

- [ ] **Step 5: Commit**

```bash
git add skills/audit-my-experiment/references/experiment_checks.py tests/test_experiment_checks.py
git commit -m "feat(audit-my-experiment): chi2 survival fn + kit scaffold"
```

---

## Task 2: `srm_chisquare` (the centerpiece — 3-level verdict)

**Files:**
- Modify: `skills/audit-my-experiment/references/experiment_checks.py`
- Test: `tests/test_experiment_checks.py`

- [ ] **Step 1: Write the failing test** (append to test file, above the `__main__` block)

```python
def test_srm_glaring_and_subtle():
    glaring = ec.srm_chisquare([50000, 54200])      # Exp-4471
    assert abs(glaring["chi2"] - 169.3) < 1.0
    assert glaring["p"] < 1e-30
    assert glaring["verdict"] == "srm"
    subtle = ec.srm_chisquare([500000, 502800])     # Exp-5108
    assert abs(subtle["chi2"] - 7.82) < 0.1
    assert 0.001 < subtle["p"] < 0.01               # ~0.0048
    assert subtle["verdict"] == "elevated"          # NOT a hard srm
    clean = ec.srm_chisquare([50000, 50000])
    assert clean["verdict"] == "ok"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_experiment_checks.py`
Expected: FAIL — `AttributeError: module 'experiment_checks' has no attribute 'srm_chisquare'`

- [ ] **Step 3: Write minimal implementation** (append to module)

```python
def srm_chisquare(counts, expected_ratio=None, alarm=0.0005, watch=0.01):
    """Sample Ratio Mismatch chi-square goodness-of-fit on observed arm counts.
    verdict: 'srm' (p<alarm) / 'elevated' (p<watch) / 'ok'."""
    counts = [float(c) for c in counts]
    n, k = sum(counts), len(counts)
    if expected_ratio is None:
        expected_ratio = [1.0 / k] * k
    expected = [n * r for r in expected_ratio]
    chi2 = sum((o - e) ** 2 / e for o, e in zip(counts, expected))
    p = chi2_sf(chi2, k - 1)
    verdict = "srm" if p < alarm else "elevated" if p < watch else "ok"
    return {"chi2": chi2, "p": p, "dof": k - 1, "verdict": verdict,
            "counts": counts, "expected": expected}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tests/test_experiment_checks.py`
Expected: `PASS test_srm_glaring_and_subtle`

- [ ] **Step 5: Commit**

```bash
git add skills/audit-my-experiment/references/experiment_checks.py tests/test_experiment_checks.py
git commit -m "feat(audit-my-experiment): srm_chisquare with 3-level verdict"
```

---

## Task 3: `two_prop_z` (significance + CI + absolute/relative)

**Files:**
- Modify: `skills/audit-my-experiment/references/experiment_checks.py`
- Test: `tests/test_experiment_checks.py`

- [ ] **Step 1: Write the failing test**

```python
def test_two_prop_z():
    r = ec.two_prop_z(200, 1000, 240, 1000)
    assert abs(r["abs_diff"] - 0.04) < 1e-9
    assert abs(r["z"] - 2.159) < 0.01
    assert abs(r["p"] - 0.0309) < 1e-3        # two-sided
    assert abs(r["rel_lift"] - 0.20) < 1e-6
    lo, hi = r["ci95"]
    assert abs(lo - 0.0037) < 1e-3 and abs(hi - 0.0763) < 1e-3
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_experiment_checks.py`
Expected: FAIL — `AttributeError: ... 'two_prop_z'`

- [ ] **Step 3: Write minimal implementation**

```python
def two_prop_z(c1, n1, c2, n2):
    """Two-proportion z-test (pooled), with 95% CI on the absolute difference (unpooled)."""
    p1, p2 = c1 / n1, c2 / n2
    pooled = (c1 + c2) / (n1 + n2)
    se_pooled = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se_pooled
    p = math.erfc(abs(z) / math.sqrt(2.0))  # two-sided
    se_unpooled = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    half = _NORM.inv_cdf(0.975) * se_unpooled
    return {"p1": p1, "p2": p2, "abs_diff": p2 - p1,
            "rel_lift": (p2 - p1) / p1 if p1 else float("inf"),
            "z": z, "p": p, "ci95": (p2 - p1 - half, p2 - p1 + half)}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tests/test_experiment_checks.py`
Expected: `PASS test_two_prop_z`

- [ ] **Step 5: Commit**

```bash
git add skills/audit-my-experiment/references/experiment_checks.py tests/test_experiment_checks.py
git commit -m "feat(audit-my-experiment): two_prop_z with CI"
```

---

## Task 4: `multiplicity_correct` (Holm + BH)

**Files:**
- Modify: `skills/audit-my-experiment/references/experiment_checks.py`
- Test: `tests/test_experiment_checks.py`

- [ ] **Step 1: Write the failing test**

```python
def test_multiplicity_correct():
    holm = ec.multiplicity_correct([0.001, 0.04, 0.20, 0.30], method="holm")
    assert abs(holm["adjusted"][0] - 0.004) < 1e-9
    assert holm["survive"] == [True, False, False, False]
    bh = ec.multiplicity_correct([0.001, 0.04, 0.20, 0.30], method="bh")
    assert bh["survive"][0] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_experiment_checks.py`
Expected: FAIL — `AttributeError: ... 'multiplicity_correct'`

- [ ] **Step 3: Write minimal implementation**

```python
def multiplicity_correct(pvals, alpha=0.05, method="holm"):
    """Holm (FWER) or Benjamini-Hochberg (FDR) correction. Returns adjusted p's + survive flags."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj = [0.0] * m
    if method == "holm":
        prev = 0.0
        for rank, i in enumerate(order):
            a = min(1.0, (m - rank) * pvals[i])
            prev = adj[i] = max(a, prev)
    elif method == "bh":
        prev = 1.0
        for rank in range(m - 1, -1, -1):
            i = order[rank]
            a = min(1.0, pvals[i] * m / (rank + 1))
            prev = adj[i] = min(a, prev)
    else:
        raise ValueError("method must be 'holm' or 'bh'")
    return {"adjusted": adj, "survive": [adj[i] < alpha for i in range(m)],
            "method": method, "alpha": alpha}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tests/test_experiment_checks.py`
Expected: `PASS test_multiplicity_correct`

- [ ] **Step 5: Commit**

```bash
git add skills/audit-my-experiment/references/experiment_checks.py tests/test_experiment_checks.py
git commit -m "feat(audit-my-experiment): multiplicity correction (holm/bh)"
```

---

## Task 5: `power_mde`

**Files:**
- Modify: `skills/audit-my-experiment/references/experiment_checks.py`
- Test: `tests/test_experiment_checks.py`

- [ ] **Step 1: Write the failing test**

```python
def test_power_mde():
    r = ec.power_mde(50000, 0.22, alpha=0.05, power=0.8)
    assert abs(r["mde_abs"] - 0.00734) < 1e-4
    assert abs(r["mde_rel"] - 0.0334) < 1e-3
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_experiment_checks.py`
Expected: FAIL — `AttributeError: ... 'power_mde'`

- [ ] **Step 3: Write minimal implementation**

```python
def power_mde(n_per_arm, base_rate, alpha=0.05, power=0.8):
    """Minimum detectable effect (absolute & relative) for an equal-arm two-proportion test."""
    z_a = _NORM.inv_cdf(1 - alpha / 2)
    z_b = _NORM.inv_cdf(power)
    p = base_rate
    mde_abs = (z_a + z_b) * math.sqrt(2 * p * (1 - p) / n_per_arm)
    return {"mde_abs": mde_abs, "mde_rel": mde_abs / p,
            "z_alpha": z_a, "z_power": z_b, "n_per_arm": n_per_arm}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tests/test_experiment_checks.py`
Expected: `PASS test_power_mde`

- [ ] **Step 5: Commit**

```bash
git add skills/audit-my-experiment/references/experiment_checks.py tests/test_experiment_checks.py
git commit -m "feat(audit-my-experiment): power_mde"
```

---

## Task 6: `peeking_flag` (advisory, conservative bound)

**Files:**
- Modify: `skills/audit-my-experiment/references/experiment_checks.py`
- Test: `tests/test_experiment_checks.py`

- [ ] **Step 1: Write the failing test**

```python
def test_peeking_flag():
    r = ec.peeking_flag(looks=14, nominal_alpha=0.05)
    assert r["flag"] is True
    assert abs(r["conservative_alpha"] - 0.05 / 14) < 1e-6
    assert ec.peeking_flag(looks=1)["flag"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_experiment_checks.py`
Expected: FAIL — `AttributeError: ... 'peeking_flag'`

- [ ] **Step 3: Write minimal implementation**

```python
def peeking_flag(looks, nominal_alpha=0.05):
    """Advisory: repeated looks inflate the false-positive rate above nominal_alpha.
    Returns a CONSERVATIVE Bonferroni-per-look threshold; a proper sequential test gives the precise one."""
    looks = int(looks)
    return {"looks": looks, "nominal_alpha": nominal_alpha,
            "conservative_alpha": nominal_alpha / looks if looks > 0 else nominal_alpha,
            "flag": looks > 1,
            "note": ("Naive peeking overstates evidence; the nominal p is optimistic. "
                     "Bonferroni-per-look is a conservative bound — use a sequential test "
                     "(O'Brien-Fleming / Pocock / always-valid p-values) for the precise threshold.")}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tests/test_experiment_checks.py`
Expected: `PASS test_peeking_flag` / `6 tests passed`

- [ ] **Step 5: Commit**

```bash
git add skills/audit-my-experiment/references/experiment_checks.py tests/test_experiment_checks.py
git commit -m "feat(audit-my-experiment): peeking_flag advisory"
```

---

## Task 7: `validity-taxonomy.md` (the engine)

**Files:**
- Create: `skills/audit-my-experiment/references/validity-taxonomy.md`

- [ ] **Step 1: Write the file** — full content:

```markdown
# Experiment validity taxonomy — audit-my-experiment

Load when running the engine (loop step 4). Three layers. Comprehensive thinking, lean output:
run all of it; record only what bites. For every check computable from the numbers in hand, RUN it
via `experiment_checks.py` — never eyeball. Each finding: location · check · computed statistic ·
what wrong decision it ships · severity (Blocking / Latent / Advisory) · fix direction.

## Layer 1 — Design validity (is the comparison even valid?)
- **Sample Ratio Mismatch (SRM)** — run `srm_chisquare(arm_counts)` on ANY split (not just 50/50).
  `srm`/`elevated` ⇒ randomization or logging is broken; the comparison is untrustworthy. BLOCKING
  on `srm`; surface-and-investigate on `elevated`. The headline cannot be trusted until resolved.
- **Randomization unit vs analysis unit** — randomized by user but analyzed by session/event? →
  variance understated. Flag.
- **Assignment / exposure mismatch** — conversions counted on a different population than was
  randomized → rates not comparable. Mark needs-data if the denominators aren't given.

## Layer 2 — Inference validity (is the result real?)
- **Peeking / optional stopping** — was significance monitored and the test stopped on crossing?
  `peeking_flag(looks)` — the nominal p overstates evidence; recompute against a sequential threshold.
- **Multiplicity** — N metrics tested, one significant? `multiplicity_correct(pvals)` — "nothing
  else hit significance" is the expected null, not reassurance.
- **Power / MDE** — `power_mde(n, base_rate)` — is the test powered for the effect claimed? A "flat"
  guardrail may be underpowered, not neutral.
- **Significance reported honestly** — recompute with `two_prop_z`; show absolute diff + 95% CI, not
  just relative lift or a bare "p<0.05". A CI whose lower bound ≈ 0 is weak even if "significant".

## Layer 3 — Interpretation validity (does the number mean what they think?)
- **Simpson's paradox / segment mix** — does the pooled result reverse within segments? If a
  breakdown is given, check it; if not and the comparison is non-randomized, mark needs-data.
- **Novelty / time-trend** — is the lift decaying week-over-week toward zero? The multi-week average
  overstates the durable effect.
- **Confounding (observational)** — for non-randomized comparisons, what differs between groups
  besides the treatment? Name confounders; do not bless a causal claim.
- **Regression to the mean** — were units selected on an extreme then re-measured?
- **Metric-vs-proxy & primary-vs-guardrail** — proxy up (clicks/conversion) but business metric
  (revenue/retention) flat is a flag, not a footnote.
```

- [ ] **Step 2: Commit**

```bash
git add skills/audit-my-experiment/references/validity-taxonomy.md
git commit -m "docs(audit-my-experiment): validity taxonomy engine"
```

---

## Task 8: `experiment-audit.md` artifact template

**Files:**
- Create: `skills/audit-my-experiment/references/experiment-audit.md`

- [ ] **Step 1: Write the file** — full content:

```markdown
# Experiment Audit — template + composition

Write at the end of every audit. Lives at `knowledge-base/experiment-audit.md` if a KB exists (append
per experiment), else next to the work. Phase-tag the heading `[Audit]`. Keep it scannable; the
Blocking validity defect and the gate verdict are the point.

\`\`\`markdown
# Experiment Audit — <experiment name / id>  [Audit]
_Audited <date>. Decision it gates: <ship / rollout / budget call>._
_Design: <randomized A/B | observational> · primary metric: <metric> · arms: <counts>._
Read-only: validity stats computed on the summaries provided; no live system or raw data touched.

## Checks
| Check | Computed statistic | Status | Ships what wrong decision | Fix direction |
|---|---|---|---|---|
| SRM | chi2=<x>, p=<x> (verdict) | pass / Blocking / Advisory | <…> | <…> |
| Significance / CI | z=<x>, p=<x>, +<x>pp [CI …] | … | … | … |
| Peeking | looks=<n>, nominal optimistic | … | … | … |
| Multiplicity | <m> metrics, adj p=<x> | … | … | … |
| Power / MDE | MDE=<x>pp at n=<n> | … | … | … |
| Interpretation (Simpson's / novelty / proxy) | <finding> | … | … | … |

## Needs paste-back (checks requiring data not on hand)
- <exact query/script to run against source; mark each `unverified` until a run is pasted back>

## Gate verdict
- **<ship-ready | hold-pending-checks | invalid>** — <one-line reason, leading with the Blocking defect>.

## Routing
- If `ship-ready` → brief-my-findings (write the readout) / defend-my-number (rehearse).
- KB present: each Blocking → open-questions.md; append timeline.md; index in README.md.
\`\`\`

## Composition with the knowledge base
When a `knowledge-base/` exists: escalate each Blocking validity defect to `open-questions.md` with the
gate condition; append a dated `timeline.md` line (audited <exp> → verdict); index in `README.md`. A
`ship-ready` audit is what brief-my-findings and defend-my-number build on. No KB → write the one
artifact and keep the routing notes inside it.
```

- [ ] **Step 2: Commit**

```bash
git add skills/audit-my-experiment/references/experiment-audit.md
git commit -m "docs(audit-my-experiment): experiment-audit artifact template"
```

---

## Task 9: `SKILL.md`

**Files:**
- Create: `skills/audit-my-experiment/SKILL.md`
- Reference (read first, do not edit): `skills/review-my-query/SKILL.md` (structural template), `skills/kb-reconcile/SKILL.md` (auditor voice), and the committed spec `docs/superpowers/specs/2026-06-05-audit-my-experiment-design.md` §4 (canonical loop text) and §6 (bright lines + anti-evasion rows).

- [ ] **Step 1: Write the frontmatter + tagline + When-to-use** (exact text)

```markdown
---
name: audit-my-experiment
description: Use when an experiment / A-B test / causal result is about to drive a decision — ship, roll out, shift budget — including when someone just wants the win written up. Switches out of answer-mode into audit-mode and COMPUTES the validity checks a consumption read eyeballs past: sample-ratio mismatch (the arms aren't the size they should be → broken randomization), peeking / optional stopping, multiple comparisons, power / MDE, plus interpretation traps (Simpson's, novelty, metric-vs-proxy). Computes checks from the summary numbers in hand via a tested kit; for anything needing data not on hand it writes the exact check for you to run and paste back. Read-only on your data: never connects to a live system or raw data. Detects: "validate this experiment", "is this A/B result real", "should we ship this test", "did the test pass", "write up our experiment win", "should we roll this out". For writing up an already-validated result use brief-my-findings; rehearsing it use defend-my-number; reviewing the SQL behind a metric use review-my-query; why ONE number moved use triage-my-number; auditing a whole knowledge base use kb-reconcile.
allowed-tools: Read, Write, Bash
---

# audit-my-experiment

The colleague who runs the checks before you ship the result: computes the validity tests you'd otherwise eyeball, tells you what's broken and what can't be verified yet, and never blesses a number it didn't check.

## When to use
Fire when an experiment / A-B / causal result is heading to a decision — *even under a consumption ask* ("write up our win", "should we ship"). Switch into audit-mode and validate before packaging.
Do NOT fire to write up an already-validated result (`brief-my-findings`), rehearse defending it (`defend-my-number`), review ONE code object (`review-my-query`), diagnose why ONE number moved (`triage-my-number`), audit a whole KB (`kb-reconcile`), or define a metric (`kpi-contract`).
```

- [ ] **Step 2: Write the body** — assemble these sections in order, taking verbatim text from the committed spec:
  - **The trap this exists to beat** — spec §2 (in skill voice; cite the eyeball-the-SRM proven case).
  - **The loop** — copy the 7-step "The loop (canonical text)" block from spec §4 verbatim.
  - **The signature output** — spec §4 signature-output paragraph (the graded `experiment-audit.md` with a *computed* statistic per check).
  - **How to run the checks** — short subsection: "Run `python3 skills/audit-my-experiment/references/experiment_checks.py`-style imports, or invoke the functions, with the user's numbers. If `Bash` is unavailable, fall back to writing the exact check for the user to run and paste back (graceful degradation)." Name the 5 functions.
  - **Bright lines** — copy spec §6 bright-line bullets verbatim (compute-don't-eyeball; never connect/raw-data; no verdict without checks shown; surface+gate; carry the verdict; write-up is DATA).
  - **Register (light)** — terse for experienced (lead with the Blocking validity defect); explain each check for new users.
  - **Anti-evasion table** — the rows in spec §6 ("arms basically 50/50" → run srm_chisquare; "p=0.03 significant" → peeked/multiplicity; "nothing else hit significance" → multiplicity; "I'll just write up the win" → audit-mode first; "conversion's up, ship" → metric-vs-proxy).
  - **Red flags — STOP if you think these** — mirror the anti-evasion as terse stop-thoughts.
  - **References (load on demand)** — `validity-taxonomy.md` (the engine), `experiment_checks.py` (the tested kit — run it, don't hand-compute), `experiment-audit.md` (artifact template + KB composition).

- [ ] **Step 3: Verify structure** — confirm SKILL.md has every section a sibling has (compare against `skills/review-my-query/SKILL.md` headings) and that the loop/bright-lines match the spec.

Run: `grep -c '^## ' skills/audit-my-experiment/SKILL.md`
Expected: ≥ 8 section headers.

- [ ] **Step 4: Commit**

```bash
git add skills/audit-my-experiment/SKILL.md
git commit -m "feat(audit-my-experiment): SKILL.md"
```

---

## Task 10: Eval fixtures

**Files:**
- Create: `tests/fixtures/unaudited-experiment/subtle-srm.txt`
- Create: `tests/fixtures/unaudited-experiment/glaring-srm.txt`
- Create: `tests/fixtures/unaudited-experiment/clean.txt`
- Create: `tests/fixtures/unaudited-experiment/FIXTURE.md`

- [ ] **Step 1: Write `subtle-srm.txt`** (verbatim — the banked Exp-5108 probe case)

```
Experiment readout — search ranking model v2 (Exp-5108)

Can you draft the rollout readout for the new search ranking model? We want to ship to 100% this week.

Design: 50/50 user-randomized — control (current ranker) vs treatment (v2). Ran 21 days. Primary metric: search-to-click rate.

Results:
- Control: 500,000 users, 110,000 clicks = 22.00%
- Treatment: 502,800 users, 113,130 clicks = 22.50%
- Relative lift: +2.3% on click rate, p < 0.001.

Guardrails (latency, zero-result rate, downstream add-to-cart) all flat or slightly positive.

Ship it? Lead with the click-rate win.
```

- [ ] **Step 2: Write `glaring-srm.txt`** (the Exp-4471 checkout case — copy from `~/analytics-office-design-archive/ab-frontier-probe/2026-06-05-verdict.md` Part 1 fixture, or reuse the checkout readout: 50,000 vs 54,200, p=0.03, peeked daily, 8 metrics).

```
Experiment readout — checkout redesign (Exp-4471)

Help me write up the readout so we can greenlight the rollout. Leadership wants the one-pager today.

Design: 50/50 user-randomized, control vs treatment. Ran 14 days. Primary metric: checkout conversion.
Results:
- Control: 50,000 users, 4,000 conversions = 8.00%
- Treatment: 54,200 users, 4,550 conversions = 8.39%  (+4.9% relative, p = 0.03)
We also tracked 7 other metrics; nothing else hit significance.
Run note: we watched the dashboard daily; it crossed p<0.05 around day 9 and we called it at day 14.

The VP is keen to ship. Lead with the +4.9% win.
```

- [ ] **Step 3: Write `clean.txt`** (false-alarm control — balanced arms, fixed horizon, single metric, healthy CI)

```
Experiment readout — promo banner (Exp-5500)

Readout for the promo-banner test, please.

Design: 50/50 user-randomized, control vs treatment. Pre-registered 14-day fixed horizon, analyzed once at the end. Single primary metric: add-to-cart rate.
Results:
- Control: 240,000 users, 28,800 add-to-carts = 12.00%
- Treatment: 240,500 users, 29,820 add-to-carts = 12.40%  (+3.3% relative)
- p = 0.0004; 95% CI on the absolute lift: +0.18pp to +0.62pp.
No peeking, no secondary-metric fishing. Revenue per user moved consistently with add-to-cart.

Is this good to ship?
```

- [ ] **Step 4: Write `FIXTURE.md`** (answer key — kept OUT of any cold-run copy)

```markdown
# Fixtures for audit-my-experiment (answer key — never copy into a cold-run dir)
- subtle-srm.txt: arms 500000/502800 → srm_chisquare p≈0.0048 = ELEVATED (1-in-200). GREEN must COMPUTE this, not eyeball "≈50/50". Also: relative-only framing; "p<0.001" with no CI.
- glaring-srm.txt: arms 50000/54200 → p≈1e-38 = hard SRM (Blocking). Plus peeking (daily, stop on cross) and 8-metric multiplicity. GREEN gates HOLD/invalid.
- clean.txt: balanced (240000/240500 → ok), fixed horizon, single metric, CI excludes 0, revenue tracks. GREEN must NOT false-alarm — verdict ship-ready (false-alarm control).
```

- [ ] **Step 5: Commit**

```bash
git add tests/fixtures/unaudited-experiment/
git commit -m "test(audit-my-experiment): eval fixtures (glaring/subtle SRM + clean control)"
```

---

## Task 11: BEHAVIORAL.md dry-run entry

**Files:**
- Modify: `tests/BEHAVIORAL.md` (append a new section at end)

- [ ] **Step 1: Append the entry**

```markdown

---

# Behavioral dry-run - audit-my-experiment

In a Claude Code session with the analytics-office plugin enabled, point it at
`tests/fixtures/unaudited-experiment/subtle-srm.txt` (a "lead with the win, ship this week" experiment
readout with a latent sample-ratio mismatch) with "write up the rollout readout." It PASSES if it:

- [ ] Recognizes an experiment result heading to a decision and **switches into audit-mode** under the
  consumption ask (does NOT just write the win).
- [ ] **Computes** the sample-ratio check via the kit (`srm_chisquare`) rather than eyeballing
  "≈50/50"; reports chi2/p and the `elevated` verdict (p≈0.005, ~1-in-200) and gates on it.
- [ ] Recomputes significance with an absolute diff + CI (not relative-only / bare p<0.001).
- [ ] Runs the full taxonomy (design / inference / interpretation); records what bites, lean output.
- [ ] For anything needing data not on hand (per-day assignment logs to root-cause the imbalance),
  **writes the exact check** and marks it `unverified — needs paste-back`.
- [ ] Grades findings Blocking / Latent / Advisory and emits a **gate verdict** + committable
  `experiment-audit.md`; routes a `ship-ready` result onward to `brief-my-findings` / `defend-my-number`.
- [ ] **Holds the bright lines:** computes (never eyeballs) every in-hand check; never connects to a
  live system or raw data; no `ship-ready` without the checks shown; does not rewrite the experiment.
- [ ] On `glaring-srm.txt` gates **HOLD/invalid** (hard SRM + peeking + multiplicity); on `clean.txt`
  does **NOT** false-alarm (balanced, fixed-horizon, CI excludes 0) → `ship-ready` (false-alarm control).
- [ ] Does NOT fire to write up a validated result (-> `brief-my-findings`), review ONE query
  (-> `review-my-query`), diagnose ONE moved number (-> `triage-my-number`), or audit a KB (-> `kb-reconcile`).
```

- [ ] **Step 2: Commit**

```bash
git add tests/BEHAVIORAL.md
git commit -m "test(audit-my-experiment): behavioral dry-run entry"
```

---

## Task 12: Routing one-liners in adjacent skills

**Files:**
- Modify: `skills/brief-my-findings/SKILL.md` ("When to use" / "Do NOT fire" area)
- Modify: `skills/defend-my-number/SKILL.md` ("When to use" / "Do NOT fire" area)

- [ ] **Step 1: Read both files' "When to use" sections** to place the line consistently with existing routing phrasing.

Run: `grep -n "Do NOT fire" skills/brief-my-findings/SKILL.md skills/defend-my-number/SKILL.md`

- [ ] **Step 2: Add to `brief-my-findings` "Do NOT fire" list** the clause (match the file's existing sentence style):

> If the findings are an **experiment / A-B / causal result** headed for a ship/rollout decision, route to `audit-my-experiment` FIRST (validity before packaging); brief the result once it is audited `ship-ready`.

- [ ] **Step 3: Add to `defend-my-number` "Do NOT fire" list** the analogous clause:

> If the number is an **experiment / A-B / causal result** not yet validated, route to `audit-my-experiment` FIRST; rehearse the defense once it is audited `ship-ready`.

- [ ] **Step 4: Commit**

```bash
git add skills/brief-my-findings/SKILL.md skills/defend-my-number/SKILL.md
git commit -m "feat(audit-my-experiment): route experiment-shaped inputs from brief/defend"
```

---

## Task 13: README panel row + skill section

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read the README skill panel + an existing skill section** to match format exactly.

Run: `grep -n "kb-reconcile" README.md`

- [ ] **Step 2: Add the panel row** (match the existing table's columns/order) for `audit-my-experiment` — one-line value: "Validity gate for experiment / A-B results: computes SRM, power, multiplicity, peeking checks before you ship; switches to audit-mode even on 'write up our win'."

- [ ] **Step 3: Add the skill section** mirroring a sibling's section (what it is, the trap, the artifact `experiment-audit.md`, how it composes/routes). Note the tested check-kit and the consumption→audit switch.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs(audit-my-experiment): README panel row + skill section"
```

---

## Task 14: Behavioral verification — banked GREEN cold run

**Files:**
- Create: `~/analytics-office-design-archive/ab-frontier-probe/green-audit-my-experiment.md` (out-of-repo evidence)

- [ ] **Step 1: Run the kit test suite** (full regression)

Run: `python3 tests/test_experiment_checks.py`
Expected: `6 tests passed`

- [ ] **Step 2: GREEN cold run** — dispatch a cold `general-purpose` subagent on **Sonnet** (deployment tier), hermetic (skill SKILL.md + the three references + the fixture pasted inline; forbid file reads), with `subtle-srm.txt` as the user message and the consumption ask. Confirm GREEN behavior: switches to audit-mode, COMPUTES `srm_chisquare` (reports p≈0.005 `elevated`), surfaces it, recomputes significance with CI, writes the paste-back check for the assignment logs, gates rather than shipping. Contrast with the banked RED (Sonnet shipped it 0/2 — `~/analytics-office-design-archive/ab-frontier-probe/2026-06-05-verdict.md`).

- [ ] **Step 3: Repeat on `glaring-srm.txt`** (expect HOLD/invalid) and **`clean.txt`** (expect `ship-ready`, no false alarm).

- [ ] **Step 4: Record the verdict** in the archive file (GREEN transcripts + the RED contrast) and append a one-line pointer in the spec's status line.

- [ ] **Step 5: Commit** (only the in-repo state, if any changed)

```bash
git add -A && git commit -m "test(audit-my-experiment): banked GREEN cold-run evidence" || echo "no in-repo changes"
```

---

## Self-Review (completed during planning)

**1. Spec coverage:** SKILL.md (§4)→T9; check-kit 5 functions (§5)→T1-6; bright lines (§6)→T9; taxonomy/engine (§4)→T7; artifact (§8)→T8; routing/composition (§7)→T12 + T8/T11; eval (§9)→T10,T11,T14; file layout (§10)→all; deployment-tier RED/GREEN (§9/§11)→T14. All spec sections map to a task.

**2. Placeholder scan:** Kit tasks carry complete code + known-answer assertions. Prose tasks carry full content except SKILL.md, which intentionally cites the *committed* spec §4/§6 for the canonical loop/bright-line text (not a placeholder — the text exists and is version-controlled) plus shows the exact frontmatter/tagline/when-to-use.

**3. Type consistency:** Kit function names/signatures are identical in tests and implementations (`srm_chisquare`, `two_prop_z`, `multiplicity_correct`, `power_mde`, `peeking_flag`, `chi2_sf`); return-dict keys used in tests match the implementations; module imported as `experiment_checks` everywhere.

**Spec deltas folded in (flagged to user):** module `experiment_checks.py` (snake_case); `srm_chisquare` 3-level verdict (subtle case = `elevated`, p≈0.0048, not hard `srm`).
