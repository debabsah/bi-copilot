"""Tested validity-check kit for the audit-my-forecast skill. Python stdlib only.
Runs on user-supplied actuals-vs-predicted summaries ONLY — never fits a model or reads a live series."""

__all__ = ["interval_coverage", "mape_vs_naive", "error_trend"]


def interval_coverage(actuals, lows, highs, nominal=0.95):
    """Empirical coverage of a prediction interval: fraction of actuals within [low, high].
    A '95%' interval whose empirical coverage is far below nominal is dishonest.
    verdict: 'honest' (>= nominal-0.05) / 'low' (>= nominal-0.15) / 'dishonest'."""
    n = len(actuals)
    if n == 0 or not (len(lows) == len(highs) == n):
        raise ValueError("actuals, lows, highs must be non-empty and equal length")
    inside = sum(1 for a, lo, hi in zip(actuals, lows, highs) if lo <= a <= hi)
    cov = inside / n
    verdict = "honest" if cov >= nominal - 0.05 else ("low" if cov >= nominal - 0.15 else "dishonest")
    return {"coverage": cov, "nominal": nominal, "n": n, "inside": inside,
            "gap": nominal - cov, "verdict": verdict}


def _mape(actuals, predicted):
    pairs = [(a, p) for a, p in zip(actuals, predicted) if a != 0]
    if not pairs:
        raise ValueError("MAPE undefined: all actuals are zero")
    return sum(abs((a - p) / a) for a, p in pairs) / len(pairs)


def mape_vs_naive(actuals, predicted, naive):
    """Forecast MAPE vs a naive baseline's MAPE (last-value / seasonal). A forecast that does not
    beat naive is NOT validated. Equal lengths; actuals == 0 are skipped (MAPE undefined there)."""
    n = len(actuals)
    if n == 0 or not (len(predicted) == len(naive) == n):
        raise ValueError("actuals, predicted, naive must be non-empty and equal length")
    f, b = _mape(actuals, predicted), _mape(actuals, naive)
    verdict = "beats-naive" if f < b else "no-better-than-naive"
    return {"mape_forecast": f, "mape_naive": b, "verdict": verdict}


def error_trend(errors_by_period):
    """Drift signal: is per-period |error| rising over time? Least-squares slope of |error| vs
    period index, scaled by mean error. verdict: 'rising' (rel slope > 0.05) — accuracy decaying
    since fit; 'improving' (< -0.05); else 'stable'."""
    n = len(errors_by_period)
    if n < 2:
        raise ValueError("need >= 2 periods to assess a trend")
    errs = [abs(e) for e in errors_by_period]
    xs = list(range(n))
    mx, my = sum(xs) / n, sum(errs) / n
    denom = sum((x - mx) ** 2 for x in xs)
    slope = (sum((x - mx) * (y - my) for x, y in zip(xs, errs)) / denom) if denom else 0.0
    rel = slope / my if my else 0.0
    verdict = "rising" if rel > 0.05 else ("improving" if rel < -0.05 else "stable")
    return {"slope": slope, "rel_slope": rel, "verdict": verdict, "n": n}
