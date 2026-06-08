import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "audit-my-forecast", "references"))
import forecast_checks as fc


def test_interval_coverage():
    # all inside => coverage 1.0 => honest
    r = fc.interval_coverage([5, 6, 7], [0, 0, 0], [10, 10, 10], nominal=0.95)
    assert r["coverage"] == 1.0 and r["verdict"] == "honest"
    # none inside => coverage 0 => dishonest
    r2 = fc.interval_coverage([50, 60], [0, 0], [10, 10], nominal=0.95)
    assert r2["coverage"] == 0.0 and r2["verdict"] == "dishonest"
    # 3 of 5 inside => 0.6 on a 0.95 claim => dishonest
    r3 = fc.interval_coverage([1, 1, 1, 9, 9], [0, 0, 0, 0, 0], [2, 2, 2, 2, 2], nominal=0.95)
    assert abs(r3["coverage"] - 0.6) < 1e-9 and r3["verdict"] == "dishonest"
    # guard: empty / mismatched lengths raise
    try:
        fc.interval_coverage([], [], []); assert False, "should have raised"
    except ValueError:
        pass


def test_mape_vs_naive():
    # forecast near-perfect, naive poor => beats-naive
    r = fc.mape_vs_naive([100, 100, 100], [101, 99, 100], [120, 80, 130])
    assert r["verdict"] == "beats-naive" and r["mape_forecast"] < r["mape_naive"]
    # forecast worse than naive => no-better-than-naive
    r2 = fc.mape_vs_naive([100, 100], [130, 70], [101, 99])
    assert r2["verdict"] == "no-better-than-naive"
    # all-zero actuals => MAPE undefined => raise
    try:
        fc.mape_vs_naive([0, 0], [1, 1], [2, 2]); assert False, "should have raised"
    except ValueError:
        pass


def test_error_trend():
    assert fc.error_trend([1, 2, 3, 4, 5])["verdict"] == "rising"
    assert fc.error_trend([5, 4, 3, 2, 1])["verdict"] == "improving"
    assert fc.error_trend([3, 3, 3, 3])["verdict"] == "stable"
    # guard: < 2 periods raises
    try:
        fc.error_trend([1]); assert False, "should have raised"
    except ValueError:
        pass


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fns:
        f(); print("PASS", f.__name__)
    print(f"\n{len(fns)} tests passed")
