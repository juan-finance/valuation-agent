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
- [ ] Every number has a source and a date, and is logged in source_log.csv using the 21 fields in data_sources.md (not the retired 5-column format).

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

### Shared data and independence

- [ ] Scope stated: single target in outputs/<ticker>_<date>/relative/ (orchestrator) or batch in outputs/relative_<date>/. Peer candidates and cross-checks come from the agent's own research (no group workbook). Data route confirmed/reused; full versus minimum universe stated. One valuation/FX date, cutoff and separately named FY/TTM/forward bases recorded.
- [ ] Target list, selected peers and broad regression market remain distinct; internal A–F buckets are not used as unverified GICS sectors.
- [ ] Raw financials and class-level market cap reconcile within 2%; price currencies/GBX, reporting currencies, ADRs, share classes and dilution are handled explicitly.
- [ ] Field-level sources, membership vintage, exact industry mapping, fallback formulas and all transformations are logged. No unsupported imputation or per-row web-source switching.
- [ ] >50% benchmark gaps are investigated and resolved; benchmark median/period/industry comparability is verified.
- [ ] Human Spot_check status is recorded separately; pending/waived review is never described as performed.
- [ ] No DCF-proximity/size-based weighting, generic 30% weight cap, or assumption selection aimed at matching DCF remains in the stage 3 base.

### Comparable method

- [ ] Each target has 20 distinct qualified peers, or 15–19 with an explicit feasible shortfall; below 15 is blocked. Counts/CSV totals reflect actual coverage.
- [ ] All hard filters applied, including developed-market status, financial/holding exclusions, EUR1bn minimum, permitted size band, ownership, restructuring, history and missing metrics.
- [ ] At least 12 Tier 1–2 and 10 Europe-listed peers; Tier 3<=4 unless explicit permitted relaxation to 8, always also <=peer_count−12. No other filter relaxed.
- [ ] 40–60 initial candidate pool, expansions, full rejected/ranked list, score parameters and business-description review are auditable.
- [ ] Eight score weights sum to one; pool-only 5%/95% clipping, standardization, common metric fallback definitions, missing-dimension renormalization and zero-variance handling are reproducible.
- [ ] Consensus coverage rule applied before missing-data exclusion; >30% gap switches whole target/pool to fundamental growth, with method labels.
- [ ] Full required multiple set computed or marked unavailable/NM; positive peer extremes retained. Regression PE cap/clipping are not applied to peer statistics.
- [ ] Every used raw AND scaled multiple has >=10 valid observations. Median/mean/p25/p75 shown; >25% mean–median skew flagged.
- [ ] Raw and adjusted values shown; PEG uses percentage-point growth and matched basis. Positive-driver safeguards and scaled-ratio quartiles applied.
- [ ] One primary multiple per valued target follows business suitability/ordered fallback. CF and replacement-cost definitions are defensible; limitations explicit.
- [ ] EV-to-equity inverse matches peer numerator, including associates/leases/NCI/other claims once; quote-currency share value and upside reconcile.
- [ ] Three reproducibly random EV calculations checked; all selected ISINs verified and each peer has an economic inclusion reason/source.
- [ ] Peer-set, quartile, multiple and material normalization sensitivities are reported; peer interquartile ranges are not called confidence intervals.
- [ ] comparables.csv, multiples_summary.csv and comparables_report.md exist; scoring/selection/Spot_check audit schedules are provided.

### Regression method

- [ ] Master first 18 columns and appended fields match the schema; all targets retained. Complete eligible universe, raw-row count and excluded records reconcile per model.
- [ ] Europe/World A ladder and B/C whole-market fallback logged per model. Full/minimum post-clean sample gates respected; losses excluded only from invalid models.
- [ ] Beta replacement uses >2.5/missing/negative rule before final missing-X exclusion; original and sourced replacement logged. Observed payout retained, cap only in growth formula.
- [ ] Unit conversions follow source metadata; median>1 is only a review trigger. FY and TTM PE not mixed; regression ROE/growth differs explicitly from DCF/peer fields where applicable.
- [ ] Raw ratio formulas retained; estimation Y and continuous X winsorized at 1%/99%, dummies untouched. Raw-IQR flags preserved; B/C use identical model rows/cutoffs.
- [ ] PE/PBV/PS/EVEBITDA specs correct; PBV has no extra g. B sector reference and World A/B region coding valid; C has no dummies. ET off unless requested.
- [ ] Constant/redundant X handled explicitly; full rank, n, retained k, df and positive SEy verified. Model-specific names/ranges prevent cross-model references.
- [ ] Live LINEST, reverse coefficient mapping, SE/t/p/CI/R²/adjusted R²/F/SS/VIF and prediction formulas used; no static ToolPak coefficients or broken external links.
- [ ] Workbook actually recalculated and formulas preserved; only documented unused LINEST error cells remain.
- [ ] Independent OLS on identical transformed rows/design matches at <1e−6 relative difference, with stated near-zero absolute tolerance; three predictions checked.
- [ ] Typicality pure-play/ROE-beta-payout-g percentile/valid-A tests recorded per target/model. Routed eligible adjusted-R² ranking and next-two alternatives reproducible.
- [ ] Actual target valuations and clipped estimation diagnostics separate; positive predictions/valid denominators required. Unvalued/excluded targets remain in output.
- [ ] D1–D10 computed with required restrictions. DFR/ambiguous signs not invented; residual bands use exact boundaries and aren't presented as proof of mispricing.
- [ ] Triggered outlier/highest-VIF robustness separate from unchanged base; refit infeasibility/changed classifications recorded.
- [ ] Same chosen multiple compared across A/B/C; no claim A−C equals a sector dummy. Published Global/Western Europe checks respect equation units and 30% rule or disclose unavailability.
- [ ] Spot_check contains targets plus 20 reproducibly random non-target rows; >2 confirmed errors repaired before final use.
- [ ] Four core regression files exist, report headings/values match workbook, one CSV row per requested target, review/model-quality statuses explicit.

## D. Recommendation and report (stage 4)
- [ ] Comparable primary estimate, regression selected estimate and DCF are shown independently before reconciliation; any final synthesis is justified without retroactive tuning.
- [ ] Final value is compared with the current market price. Any gap above 25% is explained.
- [ ] Fair value range and ONE recommended price stated. Mispricing in % and in currency.
- [ ] Recommendation tied to the annual report narrative and one mispriced parameter.
- [ ] Discussion of market expectations and current conditions included.
- [ ] Extraordinary items commented on.
- [ ] recommendation_summary.csv written.
- [ ] Same method and thresholds as in the other companies, or deviations justified.
- [ ] No reference to relative_model.xlsx, weights_table or relative_decisions.md remains; any stage 4 synthesis weights are stated, justified and not tuned to the DCF or the market price.
- [ ] Report outline approval reused or requested per report_template.md; work was not blocked while waiting.
- [ ] Data gaps section lists everything missing or estimated.
- [ ] Plain-English summary is readable by a non-specialist. Glossary and disclaimer included.
