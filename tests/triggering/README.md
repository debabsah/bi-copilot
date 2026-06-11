# Triggering eval

An automated check of the bench's **self-routing**. The bench ships no router: each
skill fires on its own `description`. As the bench grows, the risk is that two
descriptions overlap and the wrong skill wins (or none fires). This eval measures that
objectively, so a description edit can be scored instead of guessed.

It is the instrument the rest of the bench-hardening work is gated on: a hardening is
only "better" if it moves a measured number. This is one of those numbers.

## What it does

For each labelled prompt in `cases.tsv` it spawns a fresh headless `claude -p`,
captures the first `Skill` the model invokes, and classifies it against the expected
bench skill.

Two design choices were settled empirically (and matter):

1. **Neutral working directory.** Each case runs in a throwaway temp dir, never inside
   this repo. Run from inside `analytics-office/` and the model reads "design a data model"
   as *repo-development work on this project* and starts exploring the codebase instead
   of routing. The runner handles this for you.
2. **First action only.** Wandering tools are blocked and `--max-turns 1`, so the
   model's first move is the routing decision. Cheap, and unambiguous to parse.

## Run it

From your normal logged-in environment:

```bash
python3 tests/triggering/run_triggering_eval.py             # full sweep
python3 tests/triggering/run_triggering_eval.py --limit 2   # smoke test (first N cases)
MODEL=claude-haiku-4-5 python3 tests/triggering/run_triggering_eval.py   # cheaper/faster
```

Each case spawns one nested headless `claude` turn, so the full sweep costs real
tokens and a few minutes. No credentials, config dirs, or keychain access are touched;
it uses whatever session you are already logged into.

## Reading the result

| Verdict | Meaning |
|---|---|
| `PASS` | the expected bench skill fired (or, for a `none` case, no bench skill fired) |
| `WRONG-BENCH` | a *different* bench skill fired - an intra-bench mis-route. **This is the defect the eval exists to catch, and it fails the build.** |
| `FALSE-FIRE` | a bench skill fired on a true-negative prompt. Also a defect; fails the build. |
| `SHADOW` | a co-installed non-bench skill won (for example `superpowers:brainstorming`). Reported as a warning, not a failure. |
| `MISS` | nothing fired. Warning. |

Exit code is nonzero only on `WRONG-BENCH` or `FALSE-FIRE` - the failures that are
about *our* descriptions. `SHADOW` and `MISS` depend on what else is installed.

## The shadow caveat (important)

This runs in your real environment, so every other installed plugin competes. In
particular, **`superpowers:brainstorming` tends to win "design / define / structure"
prompts**, which can shadow `model-contract`, `kpi-contract`, and
`requirements-interrogator`. That is a real co-installation finding worth knowing, but
it is *not* evidence that our descriptions are dull.

To measure pure intra-bench routing (only the bench in play), run with the other
plugins disabled - for example temporarily `claude plugin disable superpowers` in a
throwaway profile, or a config that enables only this plugin. The default runner does
**not** require that, and does not change your setup.

## Known seams (measured 2026-06-10, default model claude-fable-5)

A full sweep on the then-new default model: 18 PASS, 3 intra-bench misroutes, 6 shadows,
4 misses. The three misroutes are commented out in `cases.tsv` as `KNOWN-SEAM` (preserved
for re-testing, not silently deleted): a before-we-build definition-lock going to
requirements-interrogator, a "reconciles differently" definition dispute going to
kb-reconcile, and a "write up the win" unaudited A/B going to brief-my-findings. Four
rounds of description surgery — verbatim Detects claims on the rightful winner,
opening-position constraints on the thief, then de-baiting the route-away clauses — did
not move any of them, and two rounds regressed a previously-passing foil; the loop was
stopped on that overfit signal and the descriptions reverted to the best-measured state.

## Family structure (v0.17.0, 2026-06-11) — the measured verdict

The bench reorganized into four description families (Shape / Audit / Investigate /
Deliver), each member's description opening with a validator-enforced shared stanza;
budget 15,779 -> 12,675 chars. Measured with a Sonnet-4.6 sensitivity baseline (a weaker
router surfaces description faults the default model absorbs) + full after-sweeps on both
models + a pure-bench probe (co-installed plugins disabled).

Results: Sonnet intra-bench defects 5 -> 3 (the two fixed are cross-family, as the stanza
thesis predicted). One fix round was spent: the Investigate stanza's "the estate needs
seeing" proved orientation-flavored magnet vocabulary and was retuned to "a picture of the
estate needs drawing" (the magnet lesson now operates at stanza level), and kb-reconcile
claimed "audit the whole knowledge base" after a within-family loss. After the fix the
default-model gate passed with zero new defects. The pure-bench probe delivered the
headline: BOTH kpi-contract KNOWN-SEAMs PASS under family structure when only the bench is
installed — their remaining real-environment failures are shadow-interaction (co-installed
skills shift intra-bench ranking), not description defects. The "write up the win" seam
persists everywhere (flaky on Sonnet) and stays filed; its behavioral provenance gate
contains it downstream.

Addendum (v0.20.0, the Audit family split): the new Validate family (experiment, forecast
— stanza pre-seeds parity vocabulary) probed clean: SRM and both forecast positives fire,
all three remaining-Audit regressions pass. The "write up the win" seam (sm27) is
UNCHANGED under the new stanza — fourth description-level configuration it has survived;
the conclusion is that this seam is lexical ("write up" owns the routing moment), it stays
filed, and brief's behavioral provenance gate remains its containment.

Addendum (v0.25.0, `worth-knowing` — the full dual-model protocol): same-day Sonnet
before-baseline on the untouched 18-skill bench (29 PASS / 4 WRONG-BENCH / 6 SHADOW /
1 MISS — the pre-existing flaky classes; prove-my-parity's baseline defect vanished in
the after-sweep, confirming that class is model-flaky, not structural). After adding the
skill: **fable-5 after-sweep 42/42 PASS — the first perfect sweep on record** (zero
defects, zero shadows, zero misses; both new positives fire). Sonnet after-sweep: one NEW
defect — the engagement-opening positive ("we just got an analytics budget… what can our
data tell us? We have billing, wholesale orders…") routed to explore-my-data despite
containing two of worth-knowing's Detects-class phrases verbatim. Fix round 1 (the
thief-side boundary pointer — explore-my-data's first cross-family mention) did not move
it; all four explore/groundwork/interrogator foils stayed green, so the loop was stopped
before overfit. The pure-bench probe reclassified the seam: with co-installed plugins
disabled the same case fails to a DIFFERENT thief (groundwork, not explore-my-data) —
this is not a stable lexical capture (the sm27 class) but a **three-room basin**: the
engagement-opening phrasing legitimately resembles orientation, exploration, and the
charter, and the weaker router's pick shifts with the environment while fable-5 resolves
it correctly in every configuration. FILED as Sonnet-sensitivity-only; containment is
body-level — explore-my-data's gate now hands the no-question moment to worth-knowing by
name post-fire. The second positive passes everywhere on both models. Pure-bench bonus
data: groundwork's real-env loss to map-my-estate and interrogator's loss to
brainstorming both PASS pure-bench — the established shadow-interaction class, again.

Addendum (v0.21.0): `prove-my-parity`'s two positives both FIRE on the fresh install; the
kb-reconcile foil holds its case and the triage foil MISSes (the known flaky class) rather
than being stolen by the new "reconcile" vocabulary — both contested seams held.

Addendum (v0.19.0): `review-my-dashboard`'s two positives both FIRE on the fresh install;
the review-my-query foil MISSed (nothing fired — the known fable flaky-miss class; the new
sibling did NOT steal it, which is the seam that mattered).

Addendum (v0.18.0): `change-impact`'s two positives SHADOW to the co-installed `graphify`
(the same environment class as map-my-estate — codebase/lineage vocabulary is its home
turf here); zero intra-bench defects, and the Investigate stanza's new fourth clause
passed its sibling regression probes (triage, explore both fire).

Addendum (v0.16.0): `map-my-estate`'s two positives SHADOW to a co-installed `graphify`
skill in this runner's environment (diagram vocabulary is its home turf) — zero intra-bench
defects; same environment-dependent class as `superpowers:brainstorming` shadowing
model-contract. To measure the map↔model-contract seam purely, run with other plugins
disabled.

Addendum (v0.14.0): `status-truth`'s two positives probed on a verified-fresh install —
"are we on track / project status" fires; the "weekly status update for the steering
committee" phrasing MISSes (nothing fired) — the same fable-5 miss class as the four
sweep misses, recorded as a warning per the policy above.

Two honest notes. First: routing is model-dependent — these three were not defects on the
previous baseline model, so the re-baseline cadence is not optional. Second: the
brief-my-findings misroute is caught downstream anyway — its behavioral provenance gate
routes an unaudited result back to the audit after firing — so the routing defect is a
detour, not a discipline breach. The next levers are structural (description family
grouping), not more prose.

## Adding cases

Append `expected<TAB>prompt` lines to `cases.tsv` (`none` = no bench skill should
fire). Keep prompts realistic and phrase them near a sibling boundary, so a pass
actually means the description discriminated rather than that the case was trivial.
