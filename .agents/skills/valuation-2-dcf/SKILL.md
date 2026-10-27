---
name: valuation-2-dcf
description: Stage 2 of a company valuation. Builds a DCF using FCFE or FCFF depending on debt-ratio stability, with intrinsic growth, multi-stage growth rules, market-implied and CAPM discount rates, and value per share. Use after data sourcing is complete.
---

# Goal
Value ONE company with a DCF following the professor's lecture notes (/lecture_notes:
Closure in Valuation, Cash Flows full 2026, Lecture 2 Discount Rates 2025). Where this
file and the notes differ, the notes win. Use the data pack from stage 1.

# Procedure
## A. Choose the model
1. Compute the market-value debt ratio D/(D+E) for 5+ years. Judge whether it is stable.
   Check whether the annual report states a target (e.g. leverage or rating target)
   and what analysts expect. Find or compute the stable rate and document it.
2. Stable debt ratio -> FCFE valuation. Not stable -> FCFF valuation.

## B. FCFE branch
3. Derive FCFE yourself as in the lecture notes. Read the annual report narrative and
   count only capex that creates ORGANIC growth (exclude acquisitions, and treat
   maintenance as covered by depreciation).
4. Compute the reinvestment rate as a share of earnings (preferred). If not feasible,
   use sales. If no reasonable estimate exists, use the industry average or Damodaran.
5. Always apply the stable debt ratio from step 1.

## C. FCFF branch
6. Start from EBIT of stage 1 (normalized if needed). Tax = effective tax rate from the P&L
   (flag it if abnormal). Reinvestment rate normalized from Damodaran, past investment,
   competitors or a trusted site. Prefer reinvestment as a share of EBIT(1-t); sales or
   depreciation are acceptable alternatives.

## D. Growth
7. Intrinsic growth = reinvestment rate x return (ROE for FCFE, ROC for FCFF).
8. Compare with (a) analyst growth estimates from trusted public sources and (b) a linear
   extrapolation of past earnings. Make a judgement:
   - trust intrinsic more when the information is good, analysts more when it is not;
   - check against the annual report narrative: a clear growth story -> trust intrinsic;
     no story -> trust analysts.
   Growth applies to net income (FCFE) or EBIT (FCFF).
9. Stable growth: country GDP growth, inflation, or 3%, whichever makes more sense.
   SAFEGUARD: never above the risk-free rate used in the model; flag any exception.
10. Number of stages (assumption, flag it): intrinsic growth up to 7% -> single stable-growth
    model; above 7% -> 2-stage (5 explicit years, then stable); more than 10 percentage
    points above stable growth -> 3-stage (5 + 5 years, then stable).
11. Terminal value ALWAYS with the growing perpetuity formula.

## E. Discount rates
12. Estimate the cost of equity and cost of debt "as implied by the market" from multiple
    sources (take the average for equity). For debt, target the 10-year corporate bond yield.
13. Then estimate the theoretical rates and compare:
    - Debt: risk-free rate + corporate risk premium.
    - Equity: CAPM, ke = rf + beta x MRP.
    - Risk-free rate = 10-year government bond yield in the currency MINUS the country
      default spread (Damodaran, "Risk Premiums for Other Markets"). Do not use the spot yield
      blindly: use averages or a target/normalized figure supported by analysts, news or
      exchange information.
    - Beta: compare the online beta with Damodaran's industry levered beta (use the
      datacurrent files). Explain the choice.
    - MRP = Damodaran equity risk premium for the country/currency.
14. For FCFF, WACC uses the stable debt ratio from step 1.

## F. Value
15. FCFE: equity value = PV of FCFE.
    FCFF: equity value = PV of FCFF + cash + non-operating assets - market value of debt
    - non-operating liabilities (also treat hybrids, minorities, pensions per the notes).
    Take these from the annual report and double-check with other sources.
16. Compute market cap and value per share. Verify the share count in the annual report AND
    on the exchange (exclude treasury shares, include dilution). Compare with the price.

# Outputs
dcf_model.xlsx (inputs on one sheet, no hardcoded numbers in formulas), dcf_decisions.md
(each judgement call with its reason), updated source_log.csv.
Show terminal value as a share of EV/equity value and flag it if above 75%.
Use tested Python functions in /src (create them with unit tests if missing).

# Additional requirements
- Justify the model choice (FCFE vs FCFF, number of growth stages, discount-rate method)
  in dcf_decisions.md, citing literature or data (e.g. Damodaran, Investment Valuation;
  Koller et al., Valuation) with chapter or table where possible. Only cite sources you
  have actually opened. If you cannot verify a citation, mark it "unverified". Never invent one.
- The professor's rule (FCFE if debt ratio stable, otherwise FCFF) is the DEFAULT. You may also
  run the other model as a cross-check. If you do, report both values and explain the difference.
- KEY VALUE DRIVERS: rank the 3-5 inputs that move the value most (growth, growth period,
  net capex or reinvestment, margin, cost of capital, debt ratio, etc.) using the sensitivity
  results. Explain in plain English why each matters for THIS company.
- Produce ONE summary picture of the DCF (assumptions, discount rates, growth stages, value per
  share) as dcf_summary.png. Make it clear and visually appealing.
- Comment in the decisions file on extraordinary or unusual historical items (from the
  stage 1 anomaly report) and how they affect the forecast.
- Read methodology/data_sources.md for the indicative sources of each input.
- Marginal tax rate: use the statutory corporate rate of the country (cite the table and year)
  for the after-tax cost of debt and for relevering beta. Keep the effective tax rate from
  the P&L for the FCFF cash flows (flag it if it is abnormal).
- Cost of debt: compare (a) actual bond rating or yields, (b) synthetic rating from interest
  coverage with Damodaran's table, and (c) risk-free rate + default spread. Explain the choice.
- Beta: compare the market regression beta, the bottom-up beta (industry mix from the segment
  note) and Damodaran's industry beta, all relevered at the stable debt ratio.
- Market value of debt: use the debt footnotes (maturity, coupons, fair value). If the market
  value is unavailable, say so and use book value with a stated reason.
- Operating leases are on the balance sheet under IFRS 16. Treat them consistently in debt,
  EBIT and cash flows. Mention R&D capitalization only if it is material for the company.

