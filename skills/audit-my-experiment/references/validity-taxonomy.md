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
