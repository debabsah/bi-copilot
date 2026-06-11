# Forecast Audit — Gross Revenue Churn (CS Headcount Sizing) [Audit]
_Audited 2026-07-08. Forecast: monthly gross-revenue-churn %, 1-month-ahead rolling.
Plan it gates: CS headcount plan for next fiscal year.
What was in hand: 12-month actuals-vs-predicted backtest table with 80% intervals (2025-07 – 2026-06); no feature list; no split-design description.
Read-only: computed on provided actuals-vs-predicted; no model fit, no live system touched._

## Checks

| Check | Evidence (computed / structural) | Status | Ships what wrong plan | Fix direction |
|---|---|---|---|---|
| Leakage — feature as-of + split order | Feature list not provided; split ordering not confirmed | `unverified` | Plans on accuracy that won't recur live | Trace each feature's as-of availability at month-end; confirm train ends strictly before test window; confirm preprocessing fit on train only |
| Backtest design — rolling-origin? | Split methodology not described | `unverified` | Overstated accuracy from shuffled time | Confirm rolling-origin / expanding-window eval; if random K-fold was used, re-evaluate |
| Skill vs naive — `mape_vs_naive` | Model MAPE = 11.4%, naive (last-value) MAPE = 23.5%; n=11 comparable window — **beats** naive 2.1× | `pass` | — | — |
| Stated MAPE discrepancy | Finance states ~9%; computed from full 12-month table = 10.8%; the 9% figure is reproduced only by dropping December 2025 (worst month, APE=0.290). Investigate whether an outlier month was silently excluded | Advisory | Plans on an accuracy figure that may cherry-pick the backtest window | Finance to confirm the exact MAPE window and whether any months were excluded; disclose and justify if so |
| Interval coverage — `interval_coverage` | Nominal = 80%; empirical = **6/12 = 50%**; 5 of 6 failures are upper-bound breaches (actual churn exceeded ceiling in Aug, Oct, Dec 2025, Mar and May 2026) | **Blocking** | Plan assumes 80% confidence range; actual range is 50%; downside (understaffed CS) is systematically uncovered in high-churn months | Recalibrate intervals to empirical coverage; report empirical coverage not nominal; widen upper bounds particularly — the model consistently misses churn spikes on the upside |
| Drift — `error_trend` | First-half MAE = 0.367, second-half MAE = 0.167; trend declining; last refit date not provided | `pass` (computed) / `unverified` (refit date) | — | Confirm refit cadence; if model has not been refit since initial training, note that the improving trend may reflect a quiet period rather than durable accuracy |

## Needs paste-back

_Each `unverified` check remains open until a run is pasted back._

1. **Leakage — feature as-of and split order:**
