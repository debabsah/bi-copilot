# Experiment validity taxonomy — audit-my-experiment

Load when running the engine (loop step 4). Three layers. Comprehensive thinking, lean output:
run all of it; record only what bites. For every check computable from the numbers in hand, RUN it
via `experiment_checks.py` — never eyeball. Each finding: location · check · computed statistic ·
what wrong decision it ships · severity (Blocking / Latent / Advisory) · fix direction.

## Layer 0 — Identification / design router (run FIRST)
Before any check, pin how causality is identified — the RCT kit (SRM, two-prop, power) only validates a *randomized* comparison.
- **RCT / randomized A/B** → Layers 1–3 below apply as written.
- **DiD / staggered rollout** → the RCT kit does NOT apply; run the DiD check-set below. Identifying assumption: **parallel trends**.
- **Any other non-RCT (geo holdout, pre/post, IV, synthetic-control, observational)** → the RCT kit does NOT establish causality; name the design's identifying assumption, mark `needs-data` / `uncovered`, and do not bless a causal claim. *(Roadmap: geo / pre-post / IV next.)*

The trap: treating a non-RCT as "basically an A/B" and running SRM — irrelevant when the split isn't a coin flip.

### DiD checks (the only non-RCT design fully covered in v1; all paste-back — they need the pre-period series, which is data not in hand)
- **Parallel pre-trends (the identifying assumption)** — paste back the by-period outcome for treated and control across the *pre*-period; a divergence *before* the intervention ⇒ the DiD is confounded. BLOCKING if pre-trends diverge.
- **Concurrent / common shock** — did anything else hit one group at the intervention time (a promo, a release, a seasonality split)? A coincident shock to one arm is indistinguishable from the treatment → Blocking if plausible and unaddressed.
- **Composition stability** — did the makeup of either group change across the window (entrants/exits, mix shift)? A composition change masquerades as an effect.

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
  guardrail may be underpowered, not neutral. (MDE = smallest *detectable* effect — distinct from the
  MME, the smallest *meaningful* effect; see Materiality.)
- **Significance reported honestly** — recompute with `two_prop_z`; show absolute diff + 95% CI, not
  just relative lift or a bare "p<0.05". A CI whose lower bound ≈ 0 is weak even if "significant".
- **Materiality vs the decision (significance ≠ materiality)** — significance says the effect is
  non-zero; materiality says it's big enough to act on. Pin the **minimum-meaningful-effect (MME)**
  (elicit it, or mark `materiality-unverified` — never invent it), then `classify_materiality(ci_low,
  ci_high, mme)`: whole CI ≥ MME → **material**; CI straddles the MME → **straddles-MME** (significant
  but underpowered *for the decision*); significant but CI entirely below MME → **immaterial** (real
  but too small to act on). **MDE ≠ MME:** `power_mde` is the smallest *detectable* effect (design /
  sensitivity); the MME is the smallest *meaningful* effect (business). "Powered to detect" is not
  "worth shipping" — conflating them is the trap.

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
