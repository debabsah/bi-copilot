# Forecast Audit — template + composition

Write at the end of every audit. Lives at `knowledge-base/forecast-audit.md` (append per forecast audited); no `knowledge-base/` anywhere up-tree → create it now with this artifact plus the stub `README.md` index (per the office convention in groundwork's kb-core-templates); the audited readout gets a dated copy in `inputs/`. Phase-tag the heading `[Audit]`. Keep it scannable; the Blocking temporal-validity defects and the gate verdict are the point.

```markdown
# Forecast Audit — <name> [Audit]
_Audited <date>. Forecast: <name / target metric / horizon>.
Plan it gates: <capacity / budget / headcount / rollout call>.
What was in hand: <actuals-vs-predicted series / backtest setup / stated intervals / feature list>.
Read-only: computed on provided actuals-vs-predicted; no model fit, no live system touched._

## Checks
| Check | Evidence (computed / structural) | Status | Ships what wrong plan | Fix direction |
|---|---|---|---|---|
| Leakage — feature as-of + split order | <traced / needs-data> | `pass` / Blocking / Latent / `unverified` | Plans on accuracy that won't recur live | Refit with a strictly time-ordered split; drop lookahead features |
| Backtest design — rolling-origin? | <rolling-origin / random K-fold / needs-data> | `pass` / Blocking / Latent / `unverified` | Overstated accuracy from shuffled time | Re-evaluate with rolling-origin / expanding-window |
| Skill vs naive — `mape_vs_naive` | forecast MAPE=<v>, naive MAPE=<v>; <beats / no-better> | `pass` / Blocking / `unverified` | Plans on a forecast no better than guessing | Beat a naive baseline or don't plan on it |
| Interval coverage — `interval_coverage` | nominal=<v>, empirical=<v> over n=<n> | `pass` / Blocking / `unverified` | False confidence from a dishonest band | Recalibrate the interval; report empirical coverage |
| Drift — `error_trend` | recent error <rising / stable>; last refit <date / needs-data> | `pass` / Latent / Blocking / `unverified` | Plans on a model that has silently decayed | Refit / monitor; shorten the horizon to the fresh window |

## Needs paste-back
Exact checks to run against data not on hand. Each remains `unverified` until a run is pasted back.
- <check 1 — exact script to run and paste back>

## Gate verdict
**`trustworthy` / `hold-pending-checks` / `not-trustworthy`**

<Lead with the Blocking defect if any. Example: "not-trustworthy — '95%' interval covers 61% (n=120); the plan's downside is not protected until the interval is recalibrated.">

**Re-audit when:** <the condition that invalidates this verdict — a refit, a regime change in the inputs, N new actuals, the horizon's midpoint. A verdict without an expiry is one that silently never expires.>

**Owner override:** the owner may proceed over this gate. The skill records, never relitigates: log to `decisions.md` (`<date> — OVERRIDE: proceeded over <gate> — owner <name>, rationale: <stated>`; no named owner or rationale = no override), stamp the row `→ overridden <date> by <owner>`, never erase the verdict — and every downstream brief/status carries "shipped over <the open gate>" visibly.

## Routing
- If `trustworthy`: hand to `brief-my-findings` (write up the forecast) or `defend-my-number` (rehearse).
- If `hold-pending-checks`: list the exact paste-back runs needed.
- If `not-trustworthy`: name the Blocking defect and the condition for re-audit.
- A production number that moved because of this forecast → `triage-my-number`; leakage living in the feature-build SQL (a window that peeks ahead) → `review-my-query`; an unpinned target metric → `kpi-contract`.
```

## Composition with the knowledge base
When a `knowledge-base/` exists, thread the result in rather than leaving it stranded:
- Every **Blocking** temporal-validity defect → append to `open-questions.md` with the gate condition.
- Append the audit as a dated event in `timeline.md` (audited <forecast> — gate verdict <verdict>).
- Add the Forecast Audit to the KB `README.md` index.
- No KB anywhere up-tree → create `knowledge-base/` with this artifact + stub index, routing notes inside it (`groundwork` can flesh it out later).
- When the office is git-tracked, offer the commit — `kb(audit-my-forecast): <forecast> — <gate verdict>` — one artifact, one commit (the git-native convention in groundwork's kb-core-templates).
- A Blocking temporal-validity defect (a bad plan stopped) also appends one line to `knowledge-base/catches.md` — the wins ledger.
