import math
import pytest
from valuation_agent import dcf


def test_relever_unlever_roundtrip():
    bl = dcf.relever_beta(0.8, 0.5, 0.25)
    assert bl == pytest.approx(0.8 * (1 + 0.75 * 0.5)) == pytest.approx(1.1)
    assert dcf.unlever_beta(bl, 0.5, 0.25) == pytest.approx(0.8)


def test_debt_ratio_conversion():
    assert dcf.de_from_debt_ratio(0.3) == pytest.approx(0.3 / 0.7)
    assert dcf.debt_from_ratio(0.3, 700) == pytest.approx(300)
    with pytest.raises(ValueError):
        dcf.de_from_debt_ratio(1.0)


def test_weights_must_cover_100pct():
    assert dcf.weighted_average([0.6, 0.4], [1.0, 2.0]) == pytest.approx(1.4)
    with pytest.raises(ValueError):
        dcf.weighted_average([0.6, 0.3], [1.0, 2.0])


def test_ke_approaches_differ_only_in_crp_treatment():
    a1 = dcf.ke_additive(0.03, 1.1, 0.0423, 0.01)
    a2 = dcf.ke_beta_scaled(0.03, 1.1, 0.0423, 0.01)
    assert a1 == pytest.approx(0.03 + 1.1 * 0.0423 + 0.01)
    assert a2 == pytest.approx(0.03 + 1.1 * (0.0423 + 0.01))
    assert a2 - a1 == pytest.approx(0.1 * 0.01)       # (beta-1) x CRP
    assert dcf.ke_lambda(0.03, 1.1, 0.0423, 0.8, 0.02) == pytest.approx(0.03 + 1.1 * 0.0423 + 0.016)


def test_risk_free_subtracts_sovereign_spread_not_crp():
    assert dcf.risk_free(0.04, 0.008) == pytest.approx(0.032)
    assert dcf.risk_free(0.025) == 0.025


def test_kd_and_wacc():
    kd = dcf.kd_pre_tax(0.03, 0.012, a=0.5, weighted_sovereign_spread=0.01)
    assert kd == pytest.approx(0.03 + 0.012 + 0.005)
    with pytest.raises(ValueError):
        dcf.kd_pre_tax(0.03, 0.01, a=1.5)
    w = dcf.wacc(70, 30, 0.09, 0.05, 0.25)
    assert w == pytest.approx(0.7 * 0.09 + 0.3 * 0.05 * 0.75)
    # preferred: weights sum to one, no tax shield on preferred
    wp = dcf.wacc(60, 30, 0.09, 0.05, 0.25, EP=10, kep_=0.06)
    assert wp == pytest.approx(0.6 * 0.09 + 0.3 * 0.05 * 0.75 + 0.1 * 0.06)
    assert dcf.kep(6, 100) == pytest.approx(0.06)


def test_nwc_definition_and_floor_schedule():
    assert dcf.nwc(500, 100, 300, 50) == pytest.approx((500 - 100) - (300 - 50))
    assert dcf.forecast_nwc_ratio(0.12, 0.08) == pytest.approx(0.10)
    rows = dcf.nwc_schedule([100, 110, 105], r_nwc=0.10, nwc_opening=9)
    assert [round(r.nwc_balance, 6) for r in rows] == [10, 11, 10.5]
    assert [round(r.raw_delta, 6) for r in rows] == [1, 1, -0.5]
    assert [round(r.floored_delta, 6) for r in rows] == [1, 1, 0]       # floor only on the deduction, raw retained


def test_nwc_floor_impact_is_a_cost_when_raw_negative():
    rows = dcf.nwc_schedule([100, 110, 105], 0.10, 9)
    f = dcf.discount_factors([0.1, 0.1, 0.1])
    imp = dcf.nwc_floor_impact(rows, f, shares=10)
    assert imp["cumulative_difference"] == pytest.approx(0.5)
    assert imp["pv_cost"] == pytest.approx(0.5 * f[2])
    assert imp["per_share"] == pytest.approx(imp["pv_cost"] / 10)


def test_cash_flow_identities():
    assert dcf.nce(120, 90) == 30
    assert dcf.nopat(200, 0.25) == pytest.approx(150)
    assert dcf.fcff(200, 0.25, 30, 10) == pytest.approx(110)
    assert dcf.fcfe(100, 30, 10, 16) == pytest.approx(76)
    # stable leverage: FCFE = NI - (1-delta)(NCE+dNWC) equals fcfe() with net borrowing = delta x reinvestment
    assert dcf.fcfe_stable_leverage(100, 30, 10, 0.4) == pytest.approx(dcf.fcfe(100, 30, 10, 0.4 * 40))
    assert dcf.firm_reinvestment_rate(30, 10, 150) == pytest.approx(40 / 150)
    assert dcf.equity_reinvestment_rate(30, 10, 16, 100) == pytest.approx(0.24)
    assert dcf.fundamental_growth(0.4, 0.1) == pytest.approx(0.04)
    assert dcf.stable_reinvestment_rate(0.03, 0.10) == pytest.approx(0.3)


def test_growth_stage_heuristic_evaluates_three_stage_first():
    assert dcf.growth_stage_heuristic(0.15, 0.03) == "three_stage"       # > stable + 10pp
    assert dcf.growth_stage_heuristic(0.12, 0.03) == "two_stage"         # >7% but within 10pp
    assert dcf.growth_stage_heuristic(0.05, 0.03) == "one_stage_candidate"
    assert dcf.growth_stage_heuristic(0.13, 0.03) == "two_stage"         # exactly +10pp is NOT 'more than'


def test_terminal_value_refuses_invalid_denominator():
    assert dcf.terminal_value(10.5, 0.10, 0.02) == pytest.approx(131.25)
    for r in (0.02, 0.01):
        with pytest.raises(ValueError):
            dcf.terminal_value(10, r, 0.02)
    with pytest.raises(ValueError):
        dcf.check_stable_growth(0.05, 0.03, 0.04)
    assert dcf.check_stable_growth(0.02, 0.03, 0.08) == []
    assert "safeguard" in dcf.check_stable_growth(0.035, 0.03, 0.08)[0]


def test_value_cash_flows_hand_calculation():
    r = dcf.value_cash_flows([10, 10], [0.1, 0.1], 10.5, 0.10, 0.02)
    assert r.pv_explicit == pytest.approx(10 / 1.1 + 10 / 1.21)
    assert r.tv == pytest.approx(131.25)
    assert r.pv_tv == pytest.approx(131.25 / 1.21)          # TV at time n discounted to the valuation date
    assert r.total == pytest.approx(10 / 1.1 + 10 / 1.21 + 131.25 / 1.21)
    assert r.tv_share == pytest.approx(r.pv_tv / r.total) and r.tv_flag_over_75 is True


def test_varying_rates_use_cumulative_product():
    f = dcf.discount_factors([0.10, 0.08, 0.06])
    assert f[2] == pytest.approx(1 / (1.10 * 1.08 * 1.06))
    r = dcf.value_cash_flows([5, 5, 5], [0.10, 0.08, 0.06], 5.1, 0.06, 0.02)
    assert r.pv_tv == pytest.approx(5.1 / 0.04 * f[2])


def test_gordon_consistency_with_explicit_years():
    """Cash flows growing at g from year 1: explicit years + TV must equal FCF1/(r-g)."""
    fcf1, g, r, n = 12.0, 0.03, 0.09, 5
    flows = [fcf1 * (1 + g) ** t for t in range(n)]
    res = dcf.value_cash_flows(flows, [r] * n, fcf1 * (1 + g) ** n, r, g)
    assert res.total == pytest.approx(fcf1 / (r - g))


def test_tv_share_not_reported_when_total_nonpositive():
    r = dcf.value_cash_flows([-100, -100], [0.1, 0.1], 5, 0.10, 0.02)
    assert r.total < 0 and r.tv_share is None and r.tv_flag_over_75 is False


def test_equity_bridge_counts_each_claim_once():
    eq, items = dcf.equity_bridge(1000, [("excess cash", 80), ("financial debt", -300), ("NCI", -50), ("pension deficit", -20)])
    assert eq == pytest.approx(710) and len(items) == 4
    with pytest.raises(ValueError):
        dcf.equity_bridge(1000, [("cash", 80), ("Cash", 80)])
    assert dcf.value_per_share(710, 100) == pytest.approx(7.1)
    assert dcf.upside(7.1, 6.0) == pytest.approx(7.1 / 6 - 1)
    with pytest.raises(ValueError):
        dcf.value_per_share(710, 0)


def test_sensitivity_grid_marks_invalid_cells():
    grid = dcf.sensitivity_grid(lambda r, g: 1 / (r - g), [0.02, 0.06, 0.08], [0.02, 0.03])
    assert grid[0] == [None, None]                                     # rate <= g
    assert grid[1][0] == pytest.approx(1 / 0.04) and grid[2][1] == pytest.approx(1 / 0.05)


def test_rank_drivers_sorted_by_swing():
    out = dcf.rank_drivers(100, {"margin": (80, 130), "growth": (95, 105), "wacc": (70, 140)}, top=2)
    assert [d["driver"] for d in out] == ["wacc", "margin"] and out[0]["swing"] == 70
