"""Tested validity-check kit for the audit-my-experiment skill. Python stdlib only."""
import math
from statistics import NormalDist

__all__ = ["chi2_sf", "srm_chisquare", "two_prop_z", "multiplicity_correct", "power_mde", "peeking_flag", "classify_materiality"]

_NORM = NormalDist()


def _gammq(s, x):
    """Regularized upper incomplete gamma Q(s, x) = 1 - P(s, x). Stdlib-only."""
    if x < 0 or s <= 0:
        raise ValueError("domain error in _gammq")
    if x == 0:
        return 1.0
    if x < s + 1.0:  # series for P(s,x); Q = 1 - P
        ap, total, delta = s, 1.0 / s, 1.0 / s
        for _ in range(1000):
            ap += 1.0
            delta *= x / ap
            total += delta
            if abs(delta) < abs(total) * 1e-14:
                break
        return 1.0 - total * math.exp(-x + s * math.log(x) - math.lgamma(s))
    tiny = 1e-300  # continued fraction for Q(s,x)
    b, c, d = x + 1.0 - s, 1.0 / 1e-300, 1.0 / (x + 1.0 - s)
    h = d
    for i in range(1, 1000):
        an = -i * (i - s)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-14:
            break
    return math.exp(-x + s * math.log(x) - math.lgamma(s)) * h


def chi2_sf(chi2, dof):
    """Upper-tail survival p-value for a chi-square statistic."""
    if chi2 <= 0:
        return 1.0
    if dof == 1:
        return math.erfc(math.sqrt(chi2 / 2.0))  # exact
    return _gammq(dof / 2.0, chi2 / 2.0)


def srm_chisquare(counts, expected_ratio=None, alarm=0.0005, watch=0.01):
    """Sample Ratio Mismatch chi-square goodness-of-fit on observed arm counts.
    verdict: 'srm' (p<alarm) / 'elevated' (p<watch) / 'ok'."""
    counts = [float(c) for c in counts]
    n, k = sum(counts), len(counts)
    if expected_ratio is None:
        expected_ratio = [1.0 / k] * k
    if not math.isclose(sum(expected_ratio), 1.0, rel_tol=1e-9):
        raise ValueError("expected_ratio must sum to 1.0")
    expected = [n * r for r in expected_ratio]
    chi2 = sum((o - e) ** 2 / e for o, e in zip(counts, expected))
    p = chi2_sf(chi2, k - 1)
    verdict = "srm" if p < alarm else "elevated" if p < watch else "ok"
    return {"chi2": chi2, "p": p, "dof": k - 1, "verdict": verdict,
            "counts": counts, "expected": expected}


def two_prop_z(c1, n1, c2, n2):
    """Two-proportion z-test (pooled), with 95% CI on the absolute difference (unpooled)."""
    p1, p2 = c1 / n1, c2 / n2
    pooled = (c1 + c2) / (n1 + n2)
    se_pooled = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    if se_pooled == 0:
        z, p = 0.0, 1.0
    else:
        z = (p2 - p1) / se_pooled
        p = math.erfc(abs(z) / math.sqrt(2.0))  # two-sided
    diff = p2 - p1
    if diff == 0:
        rel_lift = 0.0
    elif p1 == 0:
        rel_lift = float("inf")
    else:
        rel_lift = diff / p1
    se_unpooled = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    half = _NORM.inv_cdf(0.975) * se_unpooled
    return {"p1": p1, "p2": p2, "abs_diff": diff,
            "rel_lift": rel_lift,
            "z": z, "p": p, "ci95": (diff - half, diff + half)}


def multiplicity_correct(pvals, alpha=0.05, method="holm"):
    """Holm (FWER) or Benjamini-Hochberg (FDR) correction. Returns adjusted p's + survive flags."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj = [0.0] * m
    if method == "holm":
        prev = 0.0
        for rank, i in enumerate(order):
            a = min(1.0, (m - rank) * pvals[i])
            prev = adj[i] = max(a, prev)
    elif method == "bh":
        prev = 1.0
        for rank in range(m - 1, -1, -1):
            i = order[rank]
            a = min(1.0, pvals[i] * m / (rank + 1))
            prev = adj[i] = min(a, prev)
    else:
        raise ValueError("method must be 'holm' or 'bh'")
    return {"adjusted": adj, "survive": [adj[i] < alpha for i in range(m)],
            "method": method, "alpha": alpha}


def power_mde(n_per_arm, base_rate, alpha=0.05, power=0.8):
    """Minimum detectable effect (absolute & relative) for an equal-arm two-proportion test."""
    z_a = _NORM.inv_cdf(1 - alpha / 2)
    z_b = _NORM.inv_cdf(power)
    p = base_rate
    mde_abs = (z_a + z_b) * math.sqrt(2 * p * (1 - p) / n_per_arm)
    return {"mde_abs": mde_abs, "mde_rel": mde_abs / p,
            "z_alpha": z_a, "z_power": z_b, "n_per_arm": n_per_arm}


def peeking_flag(looks, nominal_alpha=0.05):
    """Advisory: repeated looks inflate the false-positive rate above nominal_alpha."""
    if looks < 0:
        raise ValueError("looks must be >= 0")
    looks = int(looks)
    return {"looks": looks, "nominal_alpha": nominal_alpha,
            "conservative_alpha": nominal_alpha / looks if looks > 0 else nominal_alpha,
            "flag": looks > 1,
            "note": ("Naive peeking overstates evidence; the nominal p is optimistic. "
                     "Bonferroni-per-look is a conservative bound — use a sequential test "
                     "(O'Brien-Fleming / Pocock / always-valid p-values) for the precise threshold.")}


def classify_materiality(ci_low, ci_high, mme):
    """Classify a SIGNIFICANT result's effect against the minimum-meaningful-effect (MME).

    ci_low, ci_high: the 95% CI on the absolute difference (from two_prop_z); run this AFTER
    significance is established (CI excludes 0). mme: the smallest effect worth acting on — a
    positive magnitude. v1 assumes a positive effect direction; a two-sided / harmful-effect
    MME is a follow-on. Verdict: 'material' (whole CI clears the bar), 'immaterial' (whole CI
    below the bar), 'straddles-mme' (CI spans the bar — underpowered for the decision)."""
    if ci_low > ci_high:
        raise ValueError("ci_low must be <= ci_high")
    if ci_low >= mme:
        verdict = "material"
    elif ci_high < mme:
        verdict = "immaterial"
    else:
        verdict = "straddles-mme"
    return {"verdict": verdict, "mme": mme, "ci": (ci_low, ci_high)}
