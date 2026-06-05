import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "audit-my-experiment", "references"))
import experiment_checks as ec


def test_chi2_sf_known_values():
    assert abs(ec.chi2_sf(3.841459, 1) - 0.05) < 1e-3
    assert abs(ec.chi2_sf(10.8276, 1) - 0.001) < 1e-4
    assert ec.chi2_sf(0.0, 1) == 1.0
    assert abs(ec.chi2_sf(9.487729, 4) - 0.05) < 1e-4   # continued-fraction path
    assert abs(ec.chi2_sf(16.811894, 6) - 0.01) < 1e-4  # continued-fraction path
    assert abs(ec.chi2_sf(2.0, 4) - 0.7357588823428848) < 1e-9  # series path


def test_srm_glaring_and_subtle():
    glaring = ec.srm_chisquare([50000, 54200])
    assert abs(glaring["chi2"] - 169.3) < 1.0
    assert glaring["p"] < 1e-30
    assert glaring["verdict"] == "srm"
    subtle = ec.srm_chisquare([500000, 502800])
    assert abs(subtle["chi2"] - 7.82) < 0.1
    assert 0.001 < subtle["p"] < 0.01
    assert subtle["verdict"] == "elevated"
    assert ec.srm_chisquare([50000, 50000])["verdict"] == "ok"
    # 3-arm balanced: dof=2, verdict ok
    assert ec.srm_chisquare([1000, 1000, 1000])["verdict"] == "ok"
    # 3-arm genuinely imbalanced: pin exact computed values
    r3 = ec.srm_chisquare([1000, 1000, 1200])
    assert r3["dof"] == 2
    assert abs(r3["chi2"] - 25.000000000000004) < 1e-9
    assert abs(r3["p"] - 3.726653172078664e-06) < 1e-15
    assert r3["verdict"] == "srm"


def test_two_prop_z():
    r = ec.two_prop_z(200, 1000, 240, 1000)
    assert abs(r["abs_diff"] - 0.04) < 1e-9
    assert abs(r["z"] - 2.1591675854376513) < 1e-6
    assert abs(r["p"] - 0.0309) < 1e-3
    assert abs(r["rel_lift"] - 0.20) < 1e-6
    lo, hi = r["ci95"]
    assert abs(lo - 0.003732721356494516) < 1e-4
    assert abs(hi - 0.07626727864350544) < 1e-4


def test_multiplicity_correct():
    holm = ec.multiplicity_correct([0.001, 0.04, 0.20, 0.30], method="holm")
    assert abs(holm["adjusted"][0] - 0.004) < 1e-9
    assert holm["survive"] == [True, False, False, False]
    # assert FULL adjusted array element-wise
    expected_holm = [0.004, 0.12, 0.40, 0.40]
    for got, exp in zip(holm["adjusted"], expected_holm):
        assert abs(got - exp) < 1e-4
    bh = ec.multiplicity_correct([0.001, 0.04, 0.20, 0.30], method="bh")
    assert bh["survive"][0] is True
    # assert FULL BH adjusted array element-wise
    expected_bh = [0.004, 0.08, 0.26666666666666666, 0.30]
    for got, exp in zip(bh["adjusted"], expected_bh):
        assert abs(got - exp) < 1e-4


def test_power_mde():
    r = ec.power_mde(50000, 0.22, alpha=0.05, power=0.8)
    assert abs(r["mde_abs"] - 0.00734) < 1e-4
    assert abs(r["mde_rel"] - 0.0334) < 1e-3


def test_peeking_flag():
    r = ec.peeking_flag(looks=14, nominal_alpha=0.05)
    assert r["flag"] is True
    assert abs(r["conservative_alpha"] - 0.05 / 14) < 1e-6
    assert ec.peeking_flag(looks=1)["flag"] is False
    # guard: negative looks must raise
    try:
        ec.peeking_flag(looks=-1); assert False, "should have raised"
    except ValueError:
        pass


def test_srm_custom_ratio_and_guard():
    # custom ratio: [60,40] with equal expected => chi2 should be 4.0
    assert abs(ec.srm_chisquare([60, 40], [0.5, 0.5])["chi2"] - 4.0) < 1e-9
    # guard: ratios that don't sum to 1.0 must raise ValueError
    try:
        ec.srm_chisquare([100, 100], [0.4, 0.4]); assert False, "should have raised"
    except ValueError:
        pass


def test_two_prop_z_zero_variance():
    # both arms have identical 100% conversion => se_pooled=0, no division by zero
    r = ec.two_prop_z(1000, 1000, 1000, 1000)
    assert r["z"] == 0.0
    assert r["p"] == 1.0
    assert r["rel_lift"] == 0.0
    # both arms 0 conversions => se_pooled=0
    r2 = ec.two_prop_z(0, 1000, 0, 1000)
    assert r2["z"] == 0.0
    assert r2["p"] == 1.0
    assert r2["rel_lift"] == 0.0


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fns:
        f(); print("PASS", f.__name__)
    print(f"\n{len(fns)} tests passed")
