# Temporal-validity taxonomy — audit-my-forecast

Load when running the engine (loop step 4). Four layers. Comprehensive thinking, lean output: run all of it; record only what bites. For every check computable from the actuals-vs-predicted numbers in hand, RUN it via `forecast_checks.py` — never eyeball. Each finding: location · check · computed-or-structural evidence · what wrong plan it ships · severity (Blocking / Latent / Advisory) · fix direction.

## Layer 1 — Leakage (structural; the #1 reason a backtest lies)
Future or peeked information in training makes the backtest far too good, so the plan trusts an accuracy that won't recur live. Hunt:
- **Target leakage** — a feature that encodes the outcome (or a post-outcome value).
- **Lookahead features** — a feature whose value at time t wasn't knowable until after t.
- **Whole-series scaling/normalization** — mean/std (or min/max) computed over the full series incl. the test window, so the test leaks into preprocessing.
- **Train/test time overlap** — the test window's rows (or their aggregates) appear in training.
*Check (structural, paste-back):* trace each feature's as-of availability at forecast time; confirm the split is strictly time-ordered (train entirely before test) and preprocessing is fit on train only. *Tell:* backtest accuracy "too good to be true." BLOCKING if a leak is confirmed.

## Layer 2 — Backtest validity (mixed)
- **Random K-fold on a time series** — shuffling destroys causal order; only rolling-origin / expanding-window respects time. Structural; Blocking if the eval shuffled time.
- **Single-split overstatement** — one lucky split is not skill; prefer rolling-origin across folds.
- **No naive baseline** — "low MAPE" is meaningless without a baseline. *Computed:* `mape_vs_naive` — a forecast that does not beat a naive (last-value / seasonal) baseline is NOT validated. BLOCKING on `no-better-than-naive`.

## Layer 3 — Interval honesty (computed)
- **Point shipped as certain** — a single number driving a downside-sensitive plan with no interval. BLOCKING if the plan needs the range.
- **Uncalibrated interval** — a stated band never coverage-checked. *Computed:* `interval_coverage` — empirical % of actuals inside the stated interval; a "95%" band covering far less is dishonest. BLOCKING when coverage is materially below nominal.

## Layer 4 — Drift (computed + structural)
- **Decaying accuracy** — the model was accurate at fit and has silently degraded. *Computed:* `error_trend` on recent residuals — a rising error is drift, not noise.
- **Stale fit / shifted inputs (structural)** — when was it last refit; has the input distribution moved (a new regime, a changed mix)? *Check:* compare recent error to the backtest error; ask the refit cadence. Latent → Blocking if the plan's horizon outruns the model's freshness.
