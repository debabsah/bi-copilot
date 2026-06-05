# Experiment Audit — template + composition

Write at the end of every audit. Lives at `knowledge-base/experiment-audit.md` if a KB exists (append per experiment audited), else next to the work. Phase-tag the heading `[Audit]`. Keep it scannable; the Blocking validity defects and the gate verdict are the point.

```markdown
# Experiment Audit — <name> [Audit]
_Audited <date>. Experiment: <name / ticket / link>.
Design: <randomized / observational>. Primary metric: <metric>. Arm counts: <control n / treatment n>.
Read-only: computed on provided summary numbers; no live system or raw data touched._

## Checks
| Check | Computed statistic | Status | Ships what wrong decision | Fix direction |
|---|---|---|---|---|
| SRM — arm counts | χ²=<val>, p=<val> | `pass` / Blocking / Latent / Advisory / `unverified` | Ships result from a broken randomization | Re-examine assignment/logging pipeline |
| Significance (two-prop z) | z=<val>, p=<val>, abs diff=<val>, 95% CI [<lo>, <hi>] | `pass` / Blocking / Latent / Advisory / `unverified` | Ships false or misleading confidence | Recompute; report abs diff + CI not relative lift only |
| Peeking / optional stopping | looks=<n>; nominal p overstates evidence | `pass` / Blocking / Latent / Advisory / `unverified` | Ships inflated significance from early stop | Apply sequential threshold; pre-register stopping rule |
| Multiplicity | adjusted p's: <list>; survivors at α=0.05: <list> | `pass` / Blocking / Latent / Advisory / `unverified` | Ships false positive from untreated multiple tests | Apply Holm/BH correction; report adjusted p's |
| Power / MDE | detectable effect = <val>; claimed effect = <val> | `pass` / Blocking / Latent / Advisory / `unverified` | Ships "flat guardrail" from an underpowered test | Acknowledge power gap; do not call guardrail neutral |
| Randomization unit vs analysis unit | <user / session / event> | `pass` / Blocking / Latent / Advisory / `unverified` | Understated variance → false significance | Reanalyze at randomization unit |
| Assignment / exposure mismatch | denominators: <control / treatment> | `pass` / Blocking / Latent / Advisory / `unverified` | Rates not comparable across populations | Align numerator and denominator populations |
| Simpson's paradox / segment mix | <segment breakdown present or needs-data> | `pass` / Blocking / Latent / Advisory / `unverified` | Ships pooled result that reverses within segments | Check segment-level results; flag if unavailable |
| Novelty / time-trend | <week-over-week lift: decaying / stable / needs-data> | `pass` / Blocking / Latent / Advisory / `unverified` | Ships overstated durable lift from early novelty | Report week-over-week; do not average over novelty period |
| Metric-vs-proxy / primary-vs-guardrail | proxy: <val>; primary: <val>; guardrail: <val> | `pass` / Blocking / Latent / Advisory / `unverified` | Ships proxy win that doesn't move the business metric | Require primary metric to move; treat flat guardrail as a flag |

## Needs paste-back
Exact checks to run against data not on hand. Each remains `unverified` until a run result is pasted back.

- <check 1 — exact script/query to run and paste back>
- <check 2>

## Gate verdict
**`ship-ready` / `hold-pending-checks` / `invalid`**

<Lead with the Blocking defect if any. Example: "invalid — SRM χ²=7.8 p=0.005; the comparison is untrustworthy until randomization/logging is audited.">

## Routing
- If `ship-ready`: hand off to `brief-my-findings` (to write up the result) or `defend-my-number` (to rehearse the defense).
- If `hold-pending-checks`: list the exact paste-back runs needed before the gate can clear.
- If `invalid`: name the Blocking defect and the condition for re-audit.
```

## Composition with the knowledge base
When a `knowledge-base/` exists, thread the result in rather than leaving it stranded:
- Every **Blocking** validity defect → append to `open-questions.md` with the gate condition (what must be resolved before the result can be used in a decision).
- Append the audit as a dated event in `timeline.md` (happened: audited <experiment> — gate verdict <verdict>; next: <top Blocking action>).
- Add the Experiment Audit to the KB `README.md` index.
- No KB → write the one artifact and keep the routing notes inside it (`groundwork` can stand up a KB so the next audit and eventual defense build on this one).
