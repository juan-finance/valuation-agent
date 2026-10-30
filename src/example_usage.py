"""Minimal end-to-end FCFF run with ILLUSTRATIVE numbers (not a real company). Run: python src/example_usage.py
Shows how the agent chains the engine; real inputs come from the stage 1 data pack with source_log ids."""
from valuation_agent import dcf

# --- discount rate (all numbers illustrative)
rf = dcf.risk_free(0.030, 0.0)
beta_l = dcf.relever_beta(beta_u=0.75, de=dcf.de_from_debt_ratio(0.30), t_marg=0.25)
ke = dcf.ke_additive(rf, beta_l, erp_mature=0.045, crp_weighted=0.004)
kd = dcf.kd_pre_tax(rf, company_spread=0.012)
r = dcf.wacc(E=70, D=30, ke=ke, kd=kd, t_marg=0.25)

# --- five explicit years then perpetuity (two-stage), FCFF
sales = [1000 * 1.08 ** t for t in range(1, 6)]
nwc_rows = dcf.nwc_schedule(sales, r_nwc=0.08, nwc_opening=75)
fcff = []
for s, row in zip(sales, nwc_rows):
    ebit = 0.12 * s
    nce = 0.35 * dcf.nopat(ebit, 0.22)                     # NCE/NOPAT ratio selected in the capex schedule
    fcff.append(dcf.fcff(ebit, 0.22, nce, row.floored_delta))

g = 0.025
dcf.check_stable_growth(g, rf, r)
s6 = sales[-1] * (1 + g)                                    # explicit year n+1 from stable assumptions
nopat6 = dcf.nopat(0.12 * s6, 0.22)
reinv = dcf.stable_reinvestment_rate(g, 0.10)               # g / ROC
res = dcf.value_cash_flows(fcff, [r] * 5, nopat6 * (1 - reinv), r, g)
equity, bridge = dcf.equity_bridge(res.total, [("excess cash", 40), ("financial debt", -300), ("NCI", -25)])
print(f"Ke {ke:.2%}  WACC {r:.2%}  operating value {res.total:,.0f}  TV share {res.tv_share:.0%}  flag>75% {res.tv_flag_over_75}")
print(f"common equity {equity:,.0f}  per share {dcf.value_per_share(equity, 50):.2f}")
print("NWC floor effect:", dcf.nwc_floor_impact(nwc_rows, res.factors, shares=50))
def operating_value(rate, g_stable):
    """Rebuild explicit year n+1 from the stable assumptions for EACH (rate, g) cell; never scale year n by (1+g)."""
    n1 = dcf.nopat(0.12 * sales[-1] * (1 + g_stable), 0.22)
    return dcf.value_cash_flows(fcff, [rate] * 5, n1 * (1 - dcf.stable_reinvestment_rate(g_stable, 0.10)), rate, g_stable).total


assert abs(operating_value(r, g) - res.total) < 1e-9
grid = dcf.sensitivity_grid(operating_value, [r - .01, r, r + .01], [0.015, 0.025, 0.035])
print("rate x g grid (None = invalid):", [[None if v is None else round(v) for v in row] for row in grid])
