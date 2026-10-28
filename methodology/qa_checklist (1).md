# QA checklist: run before delivering
Run each block after its stage, and run the whole list again before delivering.
Record pass / fail / fixed / not applicable, evidence, reason and unresolved impact for every item in outputs/<ticker>_<valuation-date>/qa_results.md. A material unresolved failure makes the valuation provisional.

## A. Identity and data (stage 1)
- [ ] Ticker, exchange and company identity confirmed.
- [ ] Historical financials tie to the annual report (revenue, EBITDA, net income,
      total assets, net debt). Balance sheet balances.
- [ ] Anomaly report written and each flag resolved (kept or normalized, with reason).
- [ ] Current common shares exclude treasury shares and are checked against report AND exchange, with issues, splits and buybacks updated. Dilution follows a disclosed method; historical weighted-average EPS shares are not used blindly.
- [ ] The valuation debt/cash definition is reconciled to the company's reported net debt; hybrids, leases, pensions, NCI and provisions follow sector_adjustments.md without double counting.
- [ ] Currency and units consistent everywhere. GBp vs GBP checked for London stocks.
- [ ] Every number has a source and a date, and is logged in source_log.csv.

## B. DCF (stage 2)

### Capital structure and earnings

- [ ] Five-year market and book debt ratios use aligned dates and units; debt fair value/proxy is justified. No debt amount is averaged with an industry percentage.
- [ ] Debt stability, target leverage and any transition path justify FCFE/FCFF; optional cross-check values are reconciled.
- [ ] Adjusted EBIT and group NI reconcile item by item to reported figures; recurring exceptional costs are assessed.
- [ ] Trailing EBIT/NI use comparable adjusted annual/YTD legs and the information cutoff; unavailable bridges are disclosed.
- [ ] Group/parent/NCI scopes are aligned for NI, ROE, cash flows, bridge and shares.
- [ ] Five-year effective tax review and marginal tax selection are separate; beta and debt tax shield share the same justified marginal rate.

### Reinvestment and growth

- [ ] PP&E, intangible and recurring acquisition investment are assessed individually; acquisition-led growth has its cash cost.
- [ ] D&A matches adjusted earnings; excluded impairments are not added back again. Maintenance is not automatically assumed equal to depreciation.
- [ ] No extra R&D capitalization or lease restatement is applied in the course base case; existing lease accounting is reconciled across debt/earnings/investment/payments.
- [ ] Current/prior NCE/NOPAT and industry ratio are shown; selected ratio is justified within range or an explicit denominator/data exception is recorded.
- [ ] NWC components, five-year trend, current/prior NWC/Sales and industry definitions are reconciled.
- [ ] Selected company/industry NWC average and forecast NWC balances precede raw changes; floor=max(raw change,0) applies only to forecasts, including terminal year. Its value impact is reported.
- [ ] FCFF/FCFE signs, borrowing/repayment and stable financing assumption reconcile; no repeated interest deduction.
- [ ] ROE/ROC use beginning book capital, matched cash/NCI scope and valid denominators; market values are reserved for weights.
- [ ] Fundamental growth and analyst/historical/narrative evidence are compared on matching NI/EBIT/EPS definitions; sales are independently forecast where needed.
- [ ] Three-stage test is evaluated first; 7%/10-point heuristics and 3/5-year choices are disclosed. A one-stage model actually satisfies maturity assumptions.
- [ ] Terminal g respects the course Rf safeguard or has a documented exception and compliant alternative; g is strictly below terminal discount rate in every calculated cell.
- [ ] Explicit n+1 cash flow reconciles g, return, reinvestment, tax, leverage and NWC floor; terminal timing is correct.

### Discount rates

- [ ] Currency and nominal/real basis match cash flows; Ke and Kd use the same Rf. Government spread subtraction uses the actual benchmark issuer's sovereign default spread.
- [ ] Bottom-up beta uses cash-corrected unlevered industry data, segment weights totaling 100%, and the applicable market D/E. Regression index/window/frequency/date are disclosed or marked unavailable.
- [ ] Geographic revenue weights total 100%; regional proxies and missing coverage are explained.
- [ ] Equity CRP, sovereign default spread and mature/total ERP are separate; January 2026 examples are not treated as timeless inputs.
- [ ] Base Ke uses the additive weighted CRP; beta-scaled comparison is shown. Lambda is used only with supported exposure data and no duplicate adjustment.
- [ ] External Ke comparisons identify actual method/vintage; unavailable market-implied rates are not invented.
- [ ] Actual rating, synthetic coverage, company spread and bond-yield check are documented; incremental country adjustment has a justified coefficient and no duplicate sovereign risk.
- [ ] WACC uses market weights and consistent leverage; weights sum to one, including preferred securities where relevant. No automatic preferred tax shield or arbitrary CoCo split.

### Valuation and output checks

- [ ] FCFE uses Ke and FCFF uses WACC, including correct cumulative factors when rates vary and disclosed stub/midyear timing.
- [ ] Equity bridge handles cash, debt, NCI, preferred/hybrid claims, associates, pensions and provisions once; FCFE does not subtract debt twice.
- [ ] Common-share denominator, dilution, quote units, FX and market-cap calculation reconcile.
- [ ] Terminal value's discounted share and denominator are disclosed; >75% is flagged, invalid/negative-base ratios explained.
- [ ] Low/base/high and rate×g sensitivity, key driver ranking, DCF-implied multiples and material convention impacts are shown.
- [ ] Literature citations are verified; decisions, anomaly effects and missing data are documented.
- [ ] Workbook formulas reference inputs and recalculate without errors; supporting valuation tests actually ran with results recorded.
- [ ] dcf_model.xlsx, dcf_decisions.md, source_log.csv, qa_results.md and dcf_summary.png exist and reconcile.

## C. Relative valuation (stage 3)
- [ ] Peers are in the right bucket, with consistent periods. Fewer than 4 peers is stated.
- [ ] Choice of key multiples justified. Regression R-squared and input ranges checked.
- [ ] Weights in the relative valuation sum to 100% and no weight exceeds 30%.
      The unweighted median is shown, and the effect of weighting toward the DCF is reported.

## D. Recommendation and report (stage 4)
- [ ] Final value is compared with the current market price. Any gap above 25% is explained.
- [ ] Fair value range and ONE recommended price stated. Mispricing in % and in currency.
- [ ] Recommendation tied to the annual report narrative and one mispriced parameter.
- [ ] Discussion of market expectations and current conditions included.
- [ ] Extraordinary items commented on.
- [ ] recommendation_summary.csv written.
- [ ] Same method and thresholds as in the other companies, or deviations justified.
- [ ] Data gaps section lists everything missing or estimated.
- [ ] Plain-English summary is readable by a non-specialist. Glossary and disclaimer included.
