# Experiment Audit — Guided Onboarding Pilot [Audit]
_Audited 2026-07-06. Experiment: Guided Onboarding Email Sequence (Apr-1 – Jun-15 2026, stopped week 7 of 10).
Decision it gates: Fund dedicated onboarding / CS team (annual budget).
Design: Randomized A/B (new signups, 50/50 assignment). Primary metric: 30-day activation (≥3 core actions in 30 days). Arm counts: Control 412 / Treatment 405.
Read-only: computed on provided summary numbers; no live system or raw data touched._

## Checks

| Check | Computed statistic | Status | Ships what wrong decision | Fix direction |
|---|---|---|---|---|
| SRM — arm counts | N=817; E=408.5 each; χ²=(3.5²+3.5²)/408.5=0.060, p≈0.807 | `pass` | Ships result from broken randomization | — |
| Significance (two-prop z) | p̂₁=0.2864, p̂₂=0.3506; z=0.0642/0.03259=**1.970**; p=0.049; abs diff=+6.42 pp; 95% CI [+0.04 pp, +12.80 pp] | see Peeking | Ships misleading confidence | Report abs diff + CI; not relative lift alone |
| **Peeking / optional stopping** | Weekly dashboard checks; stopped at week 7 of 10 planned (t=0.70). O'Brien-Fleming z_crit=2.036/√0.70=**2.433**; Pocock z_crit=**2.527**. Observed z=**1.970** fails both. Nominal p=0.049 does NOT survive sequential correction. | **Blocking** | Ships a false-positive as budget evidence | Pre-specify stopping rule or run to planned n; reanalyze with sequential test (O'Brien-Fleming or Lan-DeMets α-spending) |
| Multiplicity | Single primary metric (activation); p-values=[0.049]; no correction required | `pass` | — | — |
| Power / MDE | MDE=2.802×√(2×0.2864×0.7136/408.5)=**8.86 pp**; claimed effect=6.42 pp < MDE; power for 6.42 pp = Φ(0.069)≈**53%** | Advisory | Ships "underpowered win" — observed effect is likely an overestimate (winner's curse) | Acknowledge; do not treat point estimate as reliable for budget sizing |
| Randomization unit vs analysis unit | Unit: new signup → analyzed at signup level. Consistent. | `pass` | — | — |
| Assignment / exposure mismatch | Intention-to-treat assumed (all assigned signups in denominator). Confirm treatment arm includes non-openers. | `unverified — needs paste-back` | Inflated treatment rate if non-openers excluded | Confirm denominator = all assigned signups, regardless of email open |
| Simpson's paradox / segment mix | No segment breakdown provided. | `unverified — needs paste-back` | Ships pooled result that reverses within a segment (e.g., SMB vs enterprise, acquisition channel) | Run activation by signup segment; flag if available |
| Novelty / time-trend | No week-over-week activation data provided. | `unverified — needs paste-back` | Ships novelty spike as durable lift | Pull weekly activation cohort rates; confirm lift is stable across weeks 4–7 |
| **Metric-vs-proxy / primary-vs-guardrail** | Primary measured: 30-day activation (proxy). Actual decision metric: 90-day churn. "Churn itself is not measured yet — too early for 90-day churn on the later cohorts." | **Latent** | Ships a proxy win to fund a team when the business outcome (reduced churn) is unconfirmed | Do not frame activation as a churn result; report as a proxy; plan churn measurement gate before CS team headcount is committed |
| Materiality vs MME | MME not provided (no cost/LTV breakeven supplied). CI=[+0.04 pp, +12.80 pp]; wide. Cannot run `classify_materiality`. | `materiality-unverified` | Ships an immaterial significant result as budget-justifying evidence | Pin MME as: minimum activation lift that recoups CS team annual cost via reduced churn / increased LTV; rerun once peeking is resolved |

## Needs paste-back

Run these and paste the outputs back to clear the `unverified` rows:

1. **Assignment / exposure mismatch** — confirm denominators are intention-to-treat:
   ```sql
   SELECT arm, COUNT(*) AS assigned, SUM(activated_30d) AS activated
   FROM onboarding_pilot
   WHERE signup_date BETWEEN '2026-04-01' AND '2026-06-15'
   GROUP BY arm;
   -- Confirm: assigned count matches 412 / 405 and includes non-email-openers
