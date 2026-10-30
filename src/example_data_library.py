"""How a run uses the data library (ILLUSTRATIVE target inputs, real Damodaran values from data/). Run: python src/example_data_library.py"""
from valuation_agent import datasets as D, dcf, published_regressions as PR

DATE, COUNTRY = "2026-10-30", "Spain"

# 1) stage 2 inputs: the resolver picks the files, logical names pick the columns
b = D.resolve("beta", country=COUNTRY, valuation_date=DATE); c = D.resolve("capex", country=COUNTRY, valuation_date=DATE)
rp_res = D.resolve("ctryprem", country=COUNTRY, valuation_date=DATE)
for r in (b, c, rp_res):
    print("resolved:", r.summary())
beta_df, capex_df, rp = D.load_industry(b.dataset), D.load_industry(c.dataset), D.load_risk_premiums(rp_res.dataset)
beta_u = D.get_value(beta_df, "beta", "Power", "beta_unlevered_cash_corrected")
net_capex = D.get_value(capex_df, "capex", "Power", "net_capex_to_ebit_1mt")
cr = D.country_risk(rp, COUNTRY)
print(f"Power: unlevered beta (cash corrected) {beta_u}, net capex/EBIT(1-t) {net_capex:.1%}; {COUNTRY}: rating {cr['rating']}, default spread {cr['default_spread']:.2%}, CRP {cr['crp']:.2%}; mature ERP {D.mature_erp(rp):.2%}")
beta_l = dcf.relever_beta(beta_u, de=dcf.de_from_debt_ratio(0.45), t_marg=0.25)           # company's own marginal tax and target leverage
print(f"relevered beta {beta_l:.3f}; Ke (additive CRP) = {dcf.ke_additive(0.03 - cr['default_spread'], beta_l, D.mature_erp(rp), cr['crp']):.2%}")

# 2) stage 3, published route: equation, both unit policies, no invented SEy
eq, res, info = D.equation_for(COUNTRY, "EV/EBITDA", DATE)
x = {"g_rev": 0.04, "dfr": 0.40, "tax_rate": 0.22, "roic": 0.06}                          # illustrative, decimals
both = PR.predict_both_policies(eq, x)
print(f"{eq.dependent} {eq.region} (R2 {eq.r2:.1%}, vintage {res.dataset.vintage}): as_published_note {both['as_published_note']:.2f}x vs dfr_tax_percent_points {both['dfr_tax_percent_points']:.2f}x "
      f"-> unit policy differs by {both['max_relative_difference']:.0%}: verify and record before using")
eq2, _, _ = D.equation_for(COUNTRY, "PE", DATE)
print(f"PE {eq2.region}: {PR.predict(eq2, {'beta': 0.9, 'g_eps': 0.05, 'payout': 0.6}, 'as_published_note'):.1f}x (R2 {eq2.r2:.1%}, no SEy: deviation only, no residual band)")
