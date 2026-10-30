import math
import numpy as np
import pandas as pd
import pytest
from scipy.optimize import LinearConstraint, Bounds, milp

from valuation_agent import comparables as C

DIMS = list(C.WEIGHTS)


def pool_and_target(n=40, seed=0):
    rng = np.random.default_rng(seed)
    pool = pd.DataFrame(rng.normal(size=(n, len(DIMS))), columns=DIMS, index=[f"P{i}" for i in range(n)])
    target = {d: float(v) for d, v in zip(DIMS, rng.normal(size=len(DIMS)))}
    return pool, target


def test_weights_sum_to_one():
    assert sum(C.WEIGHTS.values()) == pytest.approx(1.0)


def test_distance_hand_calculation_without_winsor_effect():
    pool, target = pool_and_target()
    scores, log = C.similarity_scores(pool, target, winsor=(0.0, 1.0))      # 0/100 percentile = no clipping
    z = (pool - pool.mean()) / pool.std(ddof=1)
    zt = {d: (target[d] - pool[d].mean()) / pool[d].std(ddof=1) for d in DIMS}
    i = "P3"
    expect = math.sqrt(sum(C.WEIGHTS[d] * (z.loc[i, d] - zt[d]) ** 2 for d in DIMS))
    assert scores.loc[i, "distance"] == pytest.approx(expect)
    assert scores.loc[i, "weight_coverage"] == pytest.approx(1.0) and scores.loc[i, "note"] == "ok"


def test_pool_is_winsorised_but_target_is_not_clipped():
    pool, target = pool_and_target()
    pool.loc["P0", "growth"] = 50.0                                       # extreme candidate
    target["growth"] = 50.0                                                # extreme target
    scores, log = C.similarity_scores(pool, target)
    w = np.clip(pool["growth"], pool["growth"].quantile(.05), pool["growth"].quantile(.95))
    p = log["params"]["growth"]
    assert p["mean"] == pytest.approx(w.mean()) and p["sd"] == pytest.approx(w.std(ddof=1))
    # target raw z uses the winsorised pool's mean/SD but the UNCLIPPED target value
    z_t = (50.0 - p["mean"]) / p["sd"]
    assert z_t > 5
    far = scores["distance"].max()
    assert far > 3   # an atypical target is visibly far from everyone (not clipped to look typical)


def test_missing_dimension_rescales_weights_and_reports_coverage():
    pool, target = pool_and_target()
    pool.loc["P1", "roe"] = np.nan
    scores, _ = C.similarity_scores(pool, target, winsor=(0.0, 1.0))
    cov = 1 - C.WEIGHTS["roe"]
    assert scores.loc["P1", "weight_coverage"] == pytest.approx(cov)
    dims = [d for d in DIMS if d != "roe"]
    z = (pool[dims] - pool[dims].mean()) / pool[dims].std(ddof=1)
    zt = {d: (target[d] - pool[d].mean()) / pool[d].std(ddof=1) for d in dims}
    expect = math.sqrt(sum(C.WEIGHTS[d] / cov * (z.loc["P1", d] - zt[d]) ** 2 for d in dims))
    assert scores.loc["P1", "distance"] == pytest.approx(expect)
    assert "rescaled" in scores.loc["P1", "note"]


def test_more_than_two_missing_fails_candidate_and_target():
    pool, target = pool_and_target()
    pool.loc["P2", ["roe", "beta", "payout"]] = np.nan
    scores, _ = C.similarity_scores(pool, target)
    assert np.isnan(scores.loc["P2", "distance"]) and "fails" in scores.loc["P2", "note"]
    t_bad = dict(target); t_bad.update({"roe": None, "beta": None, "payout": None})
    with pytest.raises(ValueError, match="stop scoring"):
        C.similarity_scores(pool, t_bad)


def test_zero_sd_dimension_removed_for_whole_pool_and_logged():
    pool, target = pool_and_target()
    pool["capex_sales"] = 0.05
    scores, log = C.similarity_scores(pool, target, winsor=(0.0, 1.0))
    assert log["zero_sd_dims"] == ["capex_sales"]
    dims = [d for d in DIMS if d != "capex_sales"]
    wsum = sum(C.WEIGHTS[d] for d in dims)
    z = (pool[dims] - pool[dims].mean()) / pool[dims].std(ddof=1)
    zt = {d: (target[d] - pool[d].mean()) / pool[d].std(ddof=1) for d in dims}
    expect = math.sqrt(sum(C.WEIGHTS[d] / wsum * (z.loc["P5", d] - zt[d]) ** 2 for d in dims))
    assert scores.loc["P5", "distance"] == pytest.approx(expect)


def synth_candidates(n=60, seed=1, p_t3=.35, p_eu=.6):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({"distance": rng.uniform(0.2, 3, n), "tier": rng.choice([1, 2, 3], n, p=[.25, .4, .35]),
                         "europe": rng.random(n) < p_eu, "isin": [f"ISIN{i:04d}" for i in range(n)]},
                        index=[f"C{i}" for i in range(n)])


def milp_optimum(df, n=20, min12=12, max3=4, min_eu=10):
    cap3 = min(max3, n - min12)
    d = df["distance"].to_numpy(); t3 = (df["tier"] >= 3).to_numpy().astype(float); eu = df["europe"].to_numpy().astype(float)
    A = np.vstack([np.ones(len(df)), 1 - t3, t3, eu])
    lo = np.array([n, min12, -np.inf, min_eu]); hi = np.array([n, np.inf, cap3, np.inf])
    r = milp(d, constraints=LinearConstraint(A, lo, hi), integrality=np.ones(len(df)), bounds=Bounds(0, 1))
    return r.fun if r.success else None


@pytest.mark.parametrize("seed", range(12))
def test_selection_equals_integer_program_optimum(seed):
    df = synth_candidates(seed=seed)
    sel, info = C.select_peers(df)
    best = milp_optimum(df)
    if best is None:
        assert sel is None and not info["feasible"]
        return
    assert len(sel) == 20 and info["total_score"] == pytest.approx(best, rel=1e-9)
    assert (sel["tier"] <= 2).sum() >= 12 and (sel["tier"] >= 3).sum() <= 4 and sel["europe"].sum() >= 10
    assert sel["rank"].tolist() == list(range(1, 21)) and sel["distance"].is_monotonic_increasing


def test_selection_tie_break_is_deterministic():
    df = pd.DataFrame({"distance": [1.0] * 6, "tier": [1, 1, 2, 2, 1, 2], "europe": [True] * 6,
                       "isin": ["Z", "A", "M", "B", "C", "D"]})
    sel, _ = C.select_peers(df, n=3, min_tier_1_2=3, max_tier_3=0, min_europe=1)
    assert list(sel["isin"]) == ["A", "C", "Z"]            # tier 1 first, then ISIN


def test_infeasible_when_europe_or_tier_constraints_cannot_hold():
    df = synth_candidates(n=60)
    df["europe"] = False
    sel, info = C.select_peers(df)
    assert sel is None and info["feasible"] is False
    df2 = synth_candidates(n=60); df2["tier"] = 3
    assert C.select_peers(df2)[0] is None


def test_tier3_cap_is_also_limited_by_n_minus_12():
    df = synth_candidates(n=80, seed=4)
    sel, info = C.select_peers(df, n=15)
    assert info["constraints"]["max_tier_3"] == 3 and (sel["tier"] >= 3).sum() <= 3


def test_relaxation_order_and_shortfall_marking():
    tight = synth_candidates(n=40, seed=2); tight["europe"] = tight["europe"] & (np.arange(40) < 9)   # only 9 Europe -> infeasible
    relaxed = synth_candidates(n=60, seed=3)
    sel, info, label = C.select_with_relaxation([("strict", tight, {}), ("a: add World", relaxed, {})])
    assert label == "a: add World" and info["relaxation_step"] == "a: add World" and not info["shortfall"]
    none, info2, lab2 = C.select_with_relaxation([("strict", tight.head(10), {})])
    assert none is None and lab2 is None and "stop" in info2["note"]


def test_multiple_stats_use_percentile_inc_and_gates():
    vals = list(range(1, 13)) + [np.nan, np.nan]
    s = C.multiple_stats(vals)
    assert s["n_valid"] == 12 and s["usable"] and s["median"] == pytest.approx(6.5)
    assert s["p25"] == pytest.approx(3.75) and s["p75"] == pytest.approx(9.25)         # Excel PERCENTILE.INC
    assert not C.multiple_stats([1, 2, 3])["usable"]
    assert C.multiple_stats([1] * 11 + [100])["skew_flag"] is True
    assert C.multiple_stats([np.nan])["n_valid"] == 0


def test_high_positive_multiples_are_kept_not_trimmed():
    s = C.multiple_stats([10] * 10 + [400])
    assert s["n_valid"] == 11 and s["mean"] > 30


def test_scaled_multiple_pe_over_100g():
    rng = np.random.default_rng(0)
    g = rng.uniform(.02, .10, 15); pe = 6 + 150 * g
    out = C.scaled_multiple(pe, g, target_driver=0.05, driver_scale=100)
    ratio = pe / (100 * g)
    assert out["available"] and out["n_valid"] == 15
    assert out["median"] == pytest.approx(np.median(ratio) * 5.0)
    assert out["p25"] == pytest.approx(np.percentile(ratio, 25) * 5.0) and out["p25"] <= out["median"] <= out["p75"]


def test_scaled_multiple_unavailable_cases():
    g = np.full(15, .05); pe = np.full(15, 12.0)
    assert not C.scaled_multiple(pe, g, -0.01, 100)["available"]                 # negative target driver
    g2 = g.copy(); g2[:8] = -0.01
    assert not C.scaled_multiple(pe, g2, 0.05, 100)["available"]                  # only 7 positive peer drivers


def test_ev_bridge_inverts_exactly():
    mcap, debt, nci, cash, assoc, ebitda = 5000., 2000., 300., 700., 400., 900.
    ev = C.comparable_ev(mcap, debt, nci, cash, assoc)
    assert ev == pytest.approx(5000 + 2000 + 300 - 700 - 400)
    mult = ev / ebitda
    assert C.implied_equity_from_ev(mult, ebitda, debt, nci, cash, assoc) == pytest.approx(mcap)
    neg = C.implied_equity_from_ev(1, ebitda, debt, nci, cash, assoc)    # distress flag case
    assert neg == pytest.approx(900 - 2000 - 300 + 700 + 400) and neg < 0
    assert C.per_share_from_equity_multiple(12, 100, 50) == pytest.approx(24)
    assert C.pence_to_pounds(1250) == pytest.approx(12.5)
