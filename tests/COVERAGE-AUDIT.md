# Coverage Audit — analytics-office bench

_Read-only audit, 2026-06-04. Maps every claimed behavior across the 9 skills to whether any
test actually exercises it. Produced to answer one worry: the RED→GREEN validation proves a skill
**can** catch its one planted trap once; it never measures catch-rate, crack-rate, or
false-alarm-rate. This converts that worry into a ranked list of unbacked claims._

This is a diagnostic, not a change to any skill or test. Tick the next-move boxes as they close.

## How "is it tested?" is defined here

The bench has three test instruments; they cover very different things, so "does any test exercise
claim X" must be answered per-instrument.

| Instrument | Where | What it proves |
|---|---|---|
| **Triggering eval** | `tests/triggering/cases.tsv` (automated) | the *right skill fires* — routing only, not behavior |
| **Behavioral checklist** | `tests/BEHAVIORAL.md` `- [ ]` boxes | a *spec* of what a manual dry-run should check — **not a run** |
| **Banked behavioral run** | BEHAVIORAL.md kb-reconcile block + `~/bi-copilot-design-archive/` | an actual RED/GREEN transcript — **the only real evidence** |

Key fact: **every behavioral checkbox across all 9 skills is an unticked `- [ ]`.** Only
`kb-reconcile` carries a "Behavioral evidence (banked)" block with an actual transcript. The other
8 skills' green checkmarks are specifications of a dry-run, not records that one happened. Banked
evidence beyond kb-reconcile lives in `~/bi-copilot-design-archive/`, organized by *cross-cutting
property* (injection, data-grounding, citation, composition, consume-mode) — out-of-repo, n=1, and
mostly kb-reconcile-flavored.

## The matrix

| Skill | Claim surface (its own taxonomy) | Fixture instantiates | Breadth | Banked run (in-repo) | Routing cases | Clean/precision control |
|---|---|---|---|---|---|---|
| **kb-reconcile** | 8 drift types | partial-update + unsourced-number | **2/8** | ✅ RED+GREEN+injection | 3 | ❌ (archive explored "poisoned-consistent", never banked as a result) |
| **review-my-query** | ~25 modes / 8 families + conformance | 6 planted defects | **~6/25; 6/8 families** | ❌ spec only | 3 | ❌ |
| **triage-my-number** | 5 branches + decompose | all 5 as *suspects*, **0 confirmed** | 5/5 mapped, 0 to conclusion | ❌ spec only | 3 | ❌ |
| **kpi-contract** | ~18 forks / 7 families | ~5 named forks | **~5/18** | ❌ spec only | 2 | ❌ |
| **model-contract** | 13 forks | source-grain gate + SCD | **2/13** | ❌ spec only | 2 | ❌ |
| **requirements-interrogator** | 6 frameworks + 2 modes | 1 (solution-shaped, *live* mode) | warm-start & prep-mode **uninstantiated** | ❌ spec only | 1 | ❌ |
| **defend-my-number** | 3 archetypes + mixed drill | 1 (skeptical CFO) | **~1–2/3** | ❌ spec only | 1 | ❌ |
| **brief-my-findings** | 4 status grades + 4-part shape | directional / open / inferred-cut | ~4/4 grades | ❌ spec only | 1 | ❌ |
| **groundwork** | 4 project types (A–D) | 1 (Type A inherited estate) | **1/4** | ❌ spec only | 1 | ❌ |

**Tallies:** banked in-repo run **1/9** · clean/precision control **0/9** · only-one-routing-case
**4/9** · median breadth ≈ **25–30% of the claimed taxonomy**.

**Cross-cutting properties banked in the archive** (out-of-repo, n=1, mostly kb-reconcile fixtures):
injection resistance · data-grounding (no compute from pasted sample) · quote-the-line citation ·
composition/warm-start · consume-mode-switch. These back the recurring bright-line claims, but not
per-skill and not in the repo.

## Ranked list of unbacked claims

1. **Precision / false-positive rate: UNMEASURED for all 9 (0 clean fixtures).** Every fixture is a
   trap; nothing tests that a skill stays *quiet* on a clean record. For the four auditor-type
   skills (kb-reconcile, review-my-query, triage-my-number, defend-my-number) the false-positive
   rate is the trust-defining number. Highest leverage, cheap to fix. (See "Precision controls" below.)
2. **8/9 skills have no banked run; the checkmark is a spec.** The bench's own artifact shows
   unticked boxes. Only kb-reconcile has a transcript.
3. **Breadth: claim surface ≫ evidence surface.** kb-reconcile 2/8, model-contract 2/13,
   kpi-contract ~5/18, groundwork 1/4, defend 1–2/3. The skills advertise comprehensive taxonomies;
   the fixtures sample the blatant slice.
4. **Specced-but-uninstantiated paths.** `requirements-interrogator` warm-start + prep-mode; every
   "if a `knowledge-base/` exists, thread X/Y/Z" composition claim (per-skill fixtures are
   standalone — composition is only tested cross-cuttingly in the archive); `triage`'s "escalate
   only a *confirmed* cause" (nothing is ever confirmed in its fixture, by design).
5. **n=1 everywhere.** Even kb-reconcile is one draw per condition. No repeats, rephrasings, or
   temperature spread → a sample, not a rate.
6. **Teaching-to-the-test.** Fixture + skill co-authored; a real adversary plants traps the author
   didn't anticipate. Structural, hardest to fix (needs held-out traps or a third party).
7. **Routing eval is thin & asymmetric.** 4 skills have a single case; all 3 negatives are
   far-domain (linked list, carbonara, TCP) — no in-domain-but-no-skill near-negative; and the eval
   can pass vacuously (it already did once, all-MISS) because there's no positive-fire control.

## What is genuinely backed (the floor is real)

- **Confound discipline** is real and rare: neutral temp dir, scrubbed `FIXTURE.md`, injection
  probe, GREEN re-confirmed after REFACTOR.
- **review-my-query** has the broadest fixture (6 graded defects across 6 of 8 families).
- **kb-reconcile** has by far the deepest evidence stack (RED + GREEN + injection + archive poison
  variants).
- Routing has true negatives and boundary probes at all — most skill packs ship zero.

## Precision controls — what move #1 actually is

A **precision control** is a fixture that is deliberately **clean** (no real defect), where the PASS
condition is that the skill **stays quiet** — clears the record *with its checks shown* and
manufactures no problem. It measures the false-positive rate the current trap-fixtures cannot see.

The confusion matrix the bench only half-tests:

|  | Defect present | Record clean |
|---|---|---|
| **Skill fires** | True Positive — *the REDs test this* | **False Positive — UNTESTED** |
| **Skill quiet** | False Negative — *RED-vs-GREEN contrast* | **True Negative — UNTESTED** |

The REDs measure (a weak form of) **recall**. **Precision** needs the false-positive rate, which
needs a clean fixture. Make it a **hard negative** — clean but *looks* suspicious — or it proves
nothing. Per auditor skill:

- **kb-reconcile:** a genuinely consistent KB, plus a number that looks unsourced but the GL export
  *is* in the tree. PASS: "reconciled / verified where checkable", invents no contradiction, does
  not flag the sourced number as unsourced.
- **review-my-query:** a query that conforms to the contract but is written in an odd style. PASS:
  "conforms, no Blocking", at most an Advisory — invents no Blocking defect.
- **triage-my-number:** a number that moved for a *real* reason. PASS: branches 1–4 ruled out by
  their checks, lands on "real change" — manufactures no artifact.
- **defend-my-number:** a number that is genuinely solid. PASS: grades the answers "held", concedes
  the strength, verdict "ready" — does not manufacture a crack to seem rigorous.

Related but distinct: the archive's **"poisoned-consistent"** variant (internally consistent but
wrong vs reality) guards "coherence ≠ truth", a different axis from false-positives. Both are
negative-space tests; the precision control proper is the clean/hard-negative one above.

## Next moves (cheapest-first)

- [ ] **1. Clean/precision fixture per auditor skill** + bank the "held quiet" GREEN (kills the #1 gap).
- [ ] **2. Bank the 8 missing per-skill runs** (cold-subagent RED/GREEN, kb-reconcile's method) — or tick/annotate the boxes honestly so the artifact stops over-claiming.
- [ ] **3. Widen the highest-stakes fixtures** toward their taxonomies (kb-reconcile +decision-violated/status-rot; model-contract +additivity/conformed-dims).
- [ ] **4. Thicken routing**: a 2nd case for the 4 thin skills, one near-domain negative, a positive-fire control so it can't pass vacuously.
- [ ] **5. Small-n** (3–5 rephrasings) on the load-bearing claims only; document teaching-to-the-test as a known ceiling.

## Provenance

Built by reading: `tests/BEHAVIORAL.md`, `tests/triggering/{cases.tsv,README.md}`, all 9
`skills/*/references/*` taxonomy docs, `tests/fixtures/*`, the git RED/GREEN trail, and
`~/bi-copilot-design-archive/` verdicts. Numbers (breadth ratios, routing counts) are countable from
those sources; re-run the audit when fixtures or checklists change.
