import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

from valuation_agent import regression as R


def make_market(n=400, seed=7):
    rng = np.random.default_rng(seed)
    sectors = rng.choice(["Industrials", "Utilities", "Energy", "Materials", "Tiny"], n, p=[.4, .25, .2, .1, .05])
    g = rng.normal(.05, .03, n); beta = rng.normal(1, .25, n); payout = rng.uniform(0, .9, n)
    roe = rng.normal(.1, .05, n); margin = rng.normal(.08, .04, n)
    dfr = rng.uniform(.05, .6, n); tax = rng.uniform(.1, .35, n); roic = rng.normal(.08, .03, n)
    pe = 8 + 90 * g - 4 * beta + 6 * payout + rng.normal(0, 1.5, n) + (sectors == "Utilities") * 1.5
    pbv = 0.5 + 12 * roe - 0.3 * beta + 0.6 * payout + rng.normal(0, .2, n)
    ps = 0.2 + 8 * margin + 0.5 * payout + 3 * g + rng.normal(0, .15, n)
    ev = 4 + 25 * g + 1 * dfr - 3 * tax + 20 * roic + rng.normal(0, .8, n)
    return pd.DataFrame({"Company Name": [f"C{i}" for i in range(n)], "GICS Sector": sectors, "region": "Europe", "g": g, "beta": beta,
                         "Payout ratio": payout, "Return on Equity": roe, "Net Profit Margin": margin, "DFR": dfr,
                         "Tax Rate": tax, "ROIC": roic, "Current PE": pe, "PBV": pbv, "PS": ps, "EV/EBITDA": ev})


def test_percentile_inc_matches_excel_definition():
    assert R.percentile_inc(range(1, 11), .25) == pytest.approx(3.25)      # Excel PERCENTILE.INC({1..10},0.25)=3.25
    assert R.percentile_inc([1, 2, 3, 4], .5) == pytest.approx(2.5)


def test_winsorize_clips_to_percentiles():
    x = np.arange(1, 101, dtype=float)
    w, lo, hi = R.winsorize(x, .01, .99)
    assert lo == pytest.approx(R.percentile_inc(x, .01)) and w.min() == pytest.approx(lo) and w.max() == pytest.approx(hi)
    assert (w[1:-1] == x[1:-1]).all()


def test_iqr_flags():
    y = np.array([1, 2, 2, 3, 3, 3, 4, 4, 5, 100.])
    f = R.iqr_outlier_flags(y)
    assert f[-1] and f.sum() == 1


@pytest.mark.parametrize("n,k", [(120, 1), (300, 4)])
def test_ols_matches_statsmodels(n, k):
    rng = np.random.default_rng(3)
    X = pd.DataFrame(rng.normal(size=(n, k)), columns=[f"x{i}" for i in range(k)])
    y = 1.5 + X.to_numpy() @ rng.normal(size=k) + rng.normal(size=n)
    mine = R.ols(y, X)
    ref = sm.OLS(y, sm.add_constant(X)).fit()
    assert mine.intercept == pytest.approx(ref.params.iloc[0], rel=1e-9)
    np.testing.assert_allclose(mine.coef, ref.params.iloc[1:], rtol=1e-9)
    np.testing.assert_allclose(mine.se, ref.bse.iloc[1:], rtol=1e-9)
    np.testing.assert_allclose(mine.p, ref.pvalues.iloc[1:], rtol=1e-6, atol=1e-12)
    assert mine.r2 == pytest.approx(ref.rsquared) and mine.adj_r2 == pytest.approx(ref.rsquared_adj)
    assert mine.F == pytest.approx(ref.fvalue) and mine.sig_f == pytest.approx(ref.f_pvalue, abs=1e-12)
    assert mine.sey == pytest.approx(np.sqrt(ref.mse_resid)) and mine.df == int(ref.df_resid)
    assert mine.ss_res == pytest.approx(ref.ssr) and mine.ss_reg == pytest.approx(ref.ess)
    ci = ref.conf_int().iloc[1:].to_numpy()
    np.testing.assert_allclose(np.column_stack([mine.ci_low, mine.ci_high]), ci, rtol=1e-9)


def test_ols_guards():
    rng = np.random.default_rng(1)
    X = pd.DataFrame({"a": rng.normal(size=30), "const": 1.0})
    y = rng.normal(size=30)
    res = R.ols(y, X)
    assert res.dropped_constant == ["const"] and res.k == 1                 # constant removed explicitly, k recomputed
    X2 = pd.DataFrame({"a": rng.normal(size=30)}); X2["b"] = 2 * X2["a"]
    with pytest.raises(ValueError, match="full column rank"):
        R.ols(y, X2)
    with pytest.raises(ValueError, match="df"):
        R.ols(rng.normal(size=3), pd.DataFrame(rng.normal(size=(3, 2)), columns=["a", "b"]))


def test_linest_layout_and_comparison():
    rng = np.random.default_rng(5)
    X = pd.DataFrame(rng.normal(size=(80, 3)), columns=["a", "b", "c"])
    y = 2 + X["a"] * 1 - X["b"] * 2 + X["c"] * .5 + rng.normal(size=80)
    res = R.ols(y.to_numpy(), X)
    L = R.linest_layout(res)
    assert L.shape == (5, 4)
    assert L[0, 0] == res.coef[2] and L[0, 2] == res.coef[0] and L[0, 3] == res.intercept       # reversed order, intercept last
    assert L[3, 1] == res.df and L[2, 0] == res.r2
    assert R.compare_to_linest(res, L.copy()) == []
    bad = L.copy(); bad[0, 1] *= 1 + 1e-4
    assert len(R.compare_to_linest(res, bad)) == 1
    near_zero = L.copy(); near_zero[0, 0] = near_zero[0, 0]       # unchanged -> still passes
    assert R.compare_to_linest(res, near_zero) == []
    assert "shape mismatch" in R.compare_to_linest(res, L[:, :3])[0]


def test_vif_matches_auxiliary_regression():
    rng = np.random.default_rng(2)
    a = rng.normal(size=200); b = 0.8 * a + rng.normal(scale=.5, size=200); c = rng.normal(size=200)
    X = pd.DataFrame({"a": a, "b": b, "c": c})
    v = R.vif(X)
    for col in X.columns:
        aux = sm.OLS(X[col], sm.add_constant(X.drop(columns=col))).fit()
        assert v[col] == pytest.approx(1 / (1 - aux.rsquared), rel=1e-9)
    ref = variance_inflation_factor(sm.add_constant(X).to_numpy(), 1)
    assert v["a"] == pytest.approx(ref, rel=1e-9)
    assert R.vif(X[["a"]]).iloc[0] == 1.0


def test_beta_replacement_rules():
    assert R.replace_beta(1.0, .7, .25, .5)[:2] == (1.0, False)
    v, rep, note = R.replace_beta(-0.2, .7, .25, .5)
    assert rep and v == pytest.approx(.7 * (1 + .75 * .5)) and "negative" in note
    assert R.replace_beta(3.1, .7, .25, .5)[1] is True
    v, rep, note = R.replace_beta(None, .7, .25, None)
    assert np.isnan(v) and not rep and "stays missing" in note
    assert "flag" in R.replace_beta(0.05, .7, .25, .5)[2] and R.replace_beta(0.05, .7, .25, .5)[1] is False


def test_eligibility_first_failure_reason():
    df = pd.DataFrame({"Current PE": [10, 120, -5, np.nan, 15, 12], "g": [.05] * 6, "beta": [1] * 6,
                       "Payout ratio": [.3, .3, .3, .3, -.1, .3]})
    e = R.eligibility(df, "PE")
    assert list(e["eligible"]) == [True, False, False, False, False, True]
    assert e.loc[1, "reason"] == "PE>100" and e.loc[2, "reason"] == "nonpositive_Y"
    assert e.loc[3, "reason"].startswith("missing") and e.loc[4, "reason"] == "negative_payout"
    inv = pd.Series([False, False, False, False, False, True])
    assert R.eligibility(df, "PE", extra_invalid=inv).loc[5, "reason"] == "invalid_denominator"
    with pytest.raises(KeyError):
        R.eligibility(df.drop(columns="beta"), "PE")


def test_dummies_base_merge_and_zero_columns():
    s = ["Industrials"] * 20 + ["Utilities"] * 15 + ["Tiny1"] * 4 + ["Tiny2"] * 3
    df = pd.DataFrame({"GICS Sector": s}, index=range(len(s)))
    D, log = R.build_dummies(df, sector_col="GICS Sector")
    assert sorted(D.columns) == ["sector:Other", "sector:Utilities"]          # Industrials is the reference
    assert D["sector:Other"].sum() == 7
    assert set(log["sector"]["merged_to_Other"]) == {"Tiny1", "Tiny2"}
    with pytest.raises(ValueError, match="base sector"):
        R.build_dummies(pd.DataFrame({"GICS Sector": ["Utilities"] * 15}), sector_col="GICS Sector")
    reg = pd.DataFrame({"region": ["Europe"] * 30 + ["North America"] * 12 + ["Japan"] * 3})
    D2, _ = R.build_dummies(reg, region_col="region")
    assert sorted(D2.columns) == ["region:North America", "region:Other"]


@pytest.mark.parametrize("model", R.MODEL_ORDER)
def test_fit_model_B_C_share_rows_and_C_has_no_dummies(model):
    df = make_market()
    B = R.fit_model(df, model, "Europe", sector_col="GICS Sector", dummies=True)
    C = R.fit_model(df, model, "Europe")
    assert list(B.design.index) == list(C.design.index)                       # same model-specific rows
    assert all(not c.startswith(("sector:", "region:")) for c in C.design.columns)
    assert any(c.startswith("sector:") for c in B.design.columns)
    assert B.ols.n + len(B.excluded) == len(df) and C.ols.k == len(R.MODEL_SPECS[model]["x"])
    # independent check: refit the saved design with statsmodels
    ref = sm.OLS(B.y.to_numpy(), sm.add_constant(B.design)).fit()
    assert B.ols.r2 == pytest.approx(ref.rsquared) and B.ols.adj_r2 == pytest.approx(ref.rsquared_adj)
    np.testing.assert_allclose(B.ols.coef, ref.params.iloc[1:], rtol=1e-9)
    assert R.compare_to_linest(B.ols, R.linest_layout(B.ols)) == []


def test_winsorisation_happens_within_eligible_set_and_cutoffs_reusable():
    df = make_market()
    df.loc[0, "Current PE"] = 99.0                      # eligible extreme
    df.loc[1, "Current PE"] = 250.0                     # excluded (PE>100): must not influence cutoffs
    base = R.fit_model(df, "PE")
    assert base.cutoffs["Current PE"][1] <= 99.0 and 1 in base.excluded.index
    robust = R.fit_model(df, "PE", fixed_cutoffs=base.cutoffs, exclude_index=[0])
    assert robust.cutoffs == base.cutoffs and 0 in robust.excluded.index and robust.ols.n == base.ols.n - 1
    assert robust.excluded.loc[0, "reason"] == "robustness_exclusion"
    drop = R.fit_model(df, "PE", fixed_cutoffs=base.cutoffs, drop_x=["Payout ratio"])
    assert drop.ols.k == base.ols.k - 1


def test_predict_matches_manual_and_value_target_statuses():
    df = make_market()
    fit = R.fit_model(df, "PE")
    x = {"g": .06, "beta": 1.1, "Payout ratio": .4}
    manual = fit.ols.intercept + fit.ols.coef[0] * .06 + fit.ols.coef[1] * 1.1 + fit.ols.coef[2] * .4
    assert R.predict(fit, x) == pytest.approx(manual)
    out = R.value_target(fit, x, actual_multiple=manual + 2 * fit.ols.sey)
    assert out["status"] == "valued" and out["std_residual"] == pytest.approx(2.0) and out["classification"] == "Moderately overvalued"
    assert out["deviation"] == pytest.approx((manual + 2 * fit.ols.sey) / manual - 1)
    assert R.value_target(fit, {"g": .06, "beta": np.nan, "Payout ratio": .4}, 10)["status"] == "Not valued - missing data"
    assert "above 100x" in R.value_target(fit, x, 140)["status"]
    assert R.value_target(fit, {"g": -5, "beta": 3, "Payout ratio": 0}, 10)["status"].startswith("Not valued (nonpositive")
    ex = R.value_target(fit, {"g": 5.0, "beta": 1, "Payout ratio": .3}, 30)
    assert any("outside fitted range" in e for e in ex["extrapolation"])


@pytest.mark.parametrize("z,label", [(-2.01, "Significantly undervalued"), (-2.0, "Moderately undervalued"),
                                     (-1.0001, "Moderately undervalued"), (-1.0, "Fairly valued"), (1.0, "Fairly valued"),
                                     (1.0001, "Moderately overvalued"), (2.0, "Moderately overvalued"), (2.01, "Significantly overvalued"),
                                     (None, "Not classified (undefined residual)"), (float("nan"), "Not classified (undefined residual)")])
def test_residual_band_boundaries(z, label):
    assert R.classify_residual(z) == label


def test_typicality_inclusive_p10_p90_and_missing_fails():
    pool = pd.DataFrame({c: np.arange(1, 101, dtype=float) for c in ["Return on Equity", "beta", "Payout ratio", "g"]})
    lo, hi = R.percentile_inc(pool["g"], .1), R.percentile_inc(pool["g"], .9)
    ok = R.typicality_test(pool, {"Return on Equity": 50, "beta": 50, "Payout ratio": 50, "g": hi})
    assert ok["typical"] and ok["detail"]["g"]["pass"]                          # boundary inclusive
    assert not R.typicality_test(pool, {"Return on Equity": 50, "beta": 50, "Payout ratio": 50, "g": hi + .01})["typical"]
    miss = R.typicality_test(pool, {"Return on Equity": 50, "beta": None, "Payout ratio": 50, "g": 50})
    assert not miss["typical"] and miss["detail"]["beta"]["reason"] == "missing"


def test_rank_models_ties_use_relative_sey_then_model_order():
    c = [{"model": "PS", "adj_r2": .5, "sey": 1, "median_y": 4}, {"model": "PE", "adj_r2": .5, "sey": 2, "median_y": 8},
         {"model": "PBV", "adj_r2": .7, "sey": 1, "median_y": 2}, {"model": "EVEBITDA", "adj_r2": .5, "sey": 3, "median_y": 6}]
    order = [m["model"] for m in R.rank_models(c)]
    assert order[0] == "PBV"
    # PE and PS tie on adj R2 and on SEy/median(Y) (0.25 each) -> MODEL_ORDER puts PE before PS; EVEBITDA has 0.5
    assert order == ["PBV", "PE", "PS", "EVEBITDA"]


def test_choose_scope_A_follows_ladder():
    df = make_market(n=40)
    small = df.head(10)
    label, frame = R.choose_scope_A([("Europe Industry", small), ("Europe Industry Group", df.head(25)), ("World Industry", df)], "PE")
    n25 = int(R.eligibility(df.head(25), "PE")["eligible"].sum())
    assert label == ("Europe Industry Group" if n25 >= 30 else "World Industry")
    assert R.choose_scope_A([("x", small)], "PE") is None


def test_diagnostics_flags_sign_and_weak_models():
    df = make_market()
    fit = R.fit_model(df, "PE")
    d = R.diagnostics(fit)
    assert d["D1_sig_F_below_0.05"] is True and d["D2_r2_below_0.20"] is False
    assert d["D4_sign_disagreements"] == [] and d["D9_n_below_10k"] is False
    assert set(d["D5_vif"]) == {"g", "beta", "Payout ratio"}
    # force a model with the wrong sign for beta
    df2 = df.copy(); df2["Current PE"] = 8 + 90 * df2["g"] + 6 * df2["beta"] + 6 * df2["Payout ratio"]
    assert any(s.startswith("beta") for s in R.diagnostics(R.fit_model(df2, "PE"))["D4_sign_disagreements"])
    assert len(R.residuals(fit)) == fit.ols.n
