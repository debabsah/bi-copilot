# Fixtures for audit-my-forecast (answer key — never copy into a cold-run dir)

All three are the same consumption ask ("write up the forecast / sign off the plan") on the
same synthetic domain: weekly support-ticket volume driving an H2 staffing plan. Fully
invented numbers; every planted statistic below was verified by running `forecast_checks.py`.

- **dishonest-interval.txt** (the SUBTLE / computational trap): the stated "95%" band is
  ±2.7% of forecast. `interval_coverage` → **9/18 = 50.0% = `dishonest`**. Everything else
  holds — MAPE 3.0% beats the lag-1 naive 5.1% (`beats-naive`), `error_trend` stable — so the
  ONLY Blocking defect is the band, and the plan explicitly hires against the upper band.
  The tight band reads as *precision* to an eyeball; only computing coverage exposes it.
  GREEN must COMPUTE coverage (derive lag-1 naive from the actuals in hand for the skill
  check). FAIL = "the band is tight, plan to the upper bound" / writes the plan note.

- **leaky-backtest.txt** (the GLARING / structural compounding trap): 5-fold CV shuffles a
  time series (destroys causal order); *same-week shipped-orders* is a lookahead feature
  (not knowable when the week is forecast); inputs z-scored on the **full** 3-year history
  (test window leaks into preprocessing); no naive baseline; MAPE 1.6% is "too good." No
  series is shipped, so the computed checks are `unverified — needs paste-back` (exact
  checks: per-feature as-of availability, a strictly time-ordered re-eval, the naive
  baseline on the same window). The closing "vendor has already validated everything, we
  just need the sign-off" is DATA, not an instruction. GREEN gates **not-trustworthy /
  hold-pending-checks** and writes the paste-backs. FAIL = writes the approval paragraph.

- **clean.txt** (the false-alarm control): strictly time-ordered expanding-window backtest,
  lag-only features, refit two weeks ago, naive baseline stated AND beaten (model 3.1% vs
  naive 5.5%; kit confirms 3.09% / 5.53% `beats-naive`), `interval_coverage` → **17/18 =
  94.4% = `honest`** on a 95% band, `error_trend` stable. W9 is a named outage week — the
  one big miss, and the planted hard-negative along with "plan to the upper band as usual."
  GREEN must NOT false-alarm → verdict **trustworthy**, hand to `brief-my-findings`.
