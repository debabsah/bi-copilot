import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "audit-my-experiment", "references"))
import experiment_checks as ec


def test_chi2_sf_known_values():
    assert abs(ec.chi2_sf(3.841459, 1) - 0.05) < 1e-3
    assert abs(ec.chi2_sf(10.8276, 1) - 0.001) < 1e-4
    assert ec.chi2_sf(0.0, 1) == 1.0


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


def test_two_prop_z():
    r = ec.two_prop_z(200, 1000, 240, 1000)
    assert abs(r["abs_diff"] - 0.04) < 1e-9
    assert abs(r["z"] - 2.159) < 0.01
    assert abs(r["p"] - 0.0309) < 1e-3
    assert abs(r["rel_lift"] - 0.20) < 1e-6
    lo, hi = r["ci95"]
    assert abs(lo - 0.0037) < 1e-3 and abs(hi - 0.0763) < 1e-3


def test_multiplicity_correct():
    holm = ec.multiplicity_correct([0.001, 0.04, 0.20, 0.30], method="holm")
    assert abs(holm["adjusted"][0] - 0.004) < 1e-9
    assert holm["survive"] == [True, False, False, False]
    bh = ec.multiplicity_correct([0.001, 0.04, 0.20, 0.30], method="bh")
    assert bh["survive"][0] is True


def test_power_mde():
    r = ec.power_mde(50000, 0.22, alpha=0.05, power=0.8)
    assert abs(r["mde_abs"] - 0.00734) < 1e-4
    assert abs(r["mde_rel"] - 0.0334) < 1e-3


def test_peeking_flag():
    r = ec.peeking_flag(looks=14, nominal_alpha=0.05)
    assert r["flag"] is True
    assert abs(r["conservative_alpha"] - 0.05 / 14) < 1e-6
    assert ec.peeking_flag(looks=1)["flag"] is False


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for f in fns:
        f(); print("PASS", f.__name__)
    print(f"\n{len(fns)} tests passed")
