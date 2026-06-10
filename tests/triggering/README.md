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
