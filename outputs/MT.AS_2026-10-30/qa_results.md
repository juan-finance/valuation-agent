# MT.AS final QA — PROVISIONAL

Executed once at company end under approved one-session deviation. Numerical checks do not clear material evidence failures. No full src suite rerun (src unchanged). {'PASS': 75, 'FAIL_OPEN': 14, 'N/A_PUBLISHED_ROUTE': 12}

15 company tests passed (9 DCF +6 relative). Fatal-error Ruff checks passed for company scripts; mypy passed for report and relative generator with imports skipped and missing imports ignored (not a full typed-library audit). Four workbooks have no formula errors/external links. DCF difference2.84e-14; max peer-score difference4.00e-15; regression differences1.33e-15 and3.20e-14. Registered equation sha256 verified. PDF text/layout inspected;18+ pages as generated.

## Global human review
Pending. No person has signed Spot_check. Report and portfolio row remain provisional; portfolio_eligible=False.

## Unresolved material failures
- A04: Exact October30 common/diluted shares and independent exchange-close reconciliation unavailable. DCF estimates basic749.710746m plus3m dilution; vendor basic754.04m retained separately.
- B03: Signed EBIT reconciliation supplied, but NI tax/NCI allocation is estimated25%, not item-specific verified. NI estimates do not drive FCFF.
- B09: Existing lease debt/DA/ROU convention disclosed, but full additions/payment/current-scope reconciliation remains imperfect. No unqualified pass.
- B25: Actual and synthetic rating/spread checks supplied; current comparable bond YTM/CDS missing.
- B28: No double counting detected. Associates9937, NCI2003, pension1821 and debt fair premium295 use book/estimated-tax/fair-value proxies; material current claim valuation unverified.
- B29: FX/units and arithmetic reconcile, but cutoff shares/dilution are estimates and exchange close independently unavailable.
- C03: Selected numeric cap checks within2%; quote/report FX and GBX fixed. All class/treasury-share/ADR/perimeter evidence not independently completed.
- C04: Field extracts and dates supplied; primary industry/classification and some identifier/ownership evidence not fully verified. Source-policy conflict1667 versus3628 EBIT retained.
- C05: A matched industry median from the registered reference assets is unavailable. Regional aggregate is not mislabeled median; cannot complete benchmark-gap resolution.
- C08: Nine preliminary candidates satisfy count constraints after all ordered relaxations. They are NOT nine fully qualified audited peers yet; no padding.
- C09: Ownership >20%, FY24-25 restructuring and some classification/primary identifier checks not complete for every selected peer. Preliminary gates cannot be treated as passes.
- C13: Uniform approved fundamental proxy used; no verified whole-pool consensus-coverage percentage audit. No claimed analyst five-year growth.
- C18: EV before associates only. Required matched associate/perimeter adjustments cannot be completed; EV numbers are qualified checks, not primary fair values.
- C19: Three seeded mechanical EV checks present, but not all selected primary ISIN and inclusion evidence verified; human Spot_check pending.

## Full checklist

### A01 — PASS
Ticker, exchange and company identity confirmed.
- Evidence: company_identity.md; financials.json; data_pack.xlsx; anomaly_report.md; source_log.csv; company tests
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### A02 — PASS
Historical financials tie to the annual report (revenue, EBITDA, net income, total assets, net debt). Balance sheet balances.
- Evidence: company_identity.md; financials.json; data_pack.xlsx; anomaly_report.md; source_log.csv; company tests
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### A03 — PASS
Anomaly report written and each flag resolved (kept or normalized, with reason).
- Evidence: company_identity.md; financials.json; data_pack.xlsx; anomaly_report.md; source_log.csv; company tests
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### A04 — FAIL_OPEN
Current common shares exclude treasury shares and are checked against report AND exchange, with issues, splits and buybacks updated. Dilution follows a disclosed method; historical weighted-average EPS shares are not used blindly.
- Evidence: company_identity.md; financials.json; data_pack.xlsx; anomaly_report.md; source_log.csv; company tests
- Reason/impact: Exact October30 common/diluted shares and independent exchange-close reconciliation unavailable. DCF estimates basic749.710746m plus3m dilution; vendor basic754.04m retained separately.

### A05 — PASS
The valuation debt/cash definition is reconciled to the company's reported net debt; hybrids, leases, pensions, NCI and provisions follow sector_adjustments.md without double counting.
- Evidence: company_identity.md; financials.json; data_pack.xlsx; anomaly_report.md; source_log.csv; company tests
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### A06 — PASS
Currency and units consistent everywhere. GBp vs GBP checked for London stocks.
- Evidence: company_identity.md; financials.json; data_pack.xlsx; anomaly_report.md; source_log.csv; company tests
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### A07 — PASS
Every number has a source and a date, and is logged in source_log.csv using the 21 fields in data_sources.md (not the retired 5-column format).
- Evidence: company_identity.md; financials.json; data_pack.xlsx; anomaly_report.md; source_log.csv; company tests
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B01 — PASS
Five-year market and book debt ratios use aligned dates and units; debt fair value/proxy is justified. No debt amount is averaged with an industry percentage.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B02 — PASS
Debt stability, target leverage and any transition path justify FCFE/FCFF; optional cross-check values are reconciled.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B03 — FAIL_OPEN
Adjusted EBIT and group NI reconcile item by item to reported figures; recurring exceptional costs are assessed.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Signed EBIT reconciliation supplied, but NI tax/NCI allocation is estimated25%, not item-specific verified. NI estimates do not drive FCFF.

### B04 — PASS
Trailing EBIT/NI use comparable adjusted annual/YTD legs and the information cutoff; unavailable bridges are disclosed.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B05 — PASS
Group/parent/NCI scopes are aligned for NI, ROE, cash flows, bridge and shares.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B06 — PASS
Five-year effective tax review and marginal tax selection are separate; beta and debt tax shield share the same justified marginal rate.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B07 — PASS
PP&E, intangible and recurring acquisition investment are assessed individually; acquisition-led growth has its cash cost.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B08 — PASS
D&A matches adjusted earnings; excluded impairments are not added back again. Maintenance is not automatically assumed equal to depreciation.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B09 — FAIL_OPEN
No extra R&D capitalization or lease restatement is applied in the course base case; existing lease accounting is reconciled across debt/earnings/investment/payments.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Existing lease debt/DA/ROU convention disclosed, but full additions/payment/current-scope reconciliation remains imperfect. No unqualified pass.

### B10 — PASS
Current/prior NCE/NOPAT and industry ratio are shown; selected ratio is justified within range or an explicit denominator/data exception is recorded.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B11 — PASS
NWC components, five-year trend, current/prior NWC/Sales and industry definitions are reconciled.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B12 — PASS
Selected company/industry NWC average and forecast NWC balances precede raw changes; floor=max(raw change,0) applies only to forecasts, including terminal year. Its value impact is reported.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B13 — PASS
FCFF/FCFE signs, borrowing/repayment and stable financing assumption reconcile; no repeated interest deduction.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B14 — PASS
ROE/ROC use beginning book capital, matched cash/NCI scope and valid denominators; market values are reserved for weights.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B15 — PASS
Fundamental growth and analyst/historical/narrative evidence are compared on matching NI/EBIT/EPS definitions; sales are independently forecast where needed.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B16 — PASS
Three-stage test is evaluated first; 7%/10-point heuristics and 3/5-year choices are disclosed. A one-stage model actually satisfies maturity assumptions.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B17 — PASS
Terminal g respects the course Rf safeguard or has a documented exception and compliant alternative; g is strictly below terminal discount rate in every calculated cell.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B18 — PASS
Explicit n+1 cash flow reconciles g, return, reinvestment, tax, leverage and NWC floor; terminal timing is correct.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B19 — PASS
Currency and nominal/real basis match cash flows; Ke and Kd use the same Rf. Government spread subtraction uses the actual benchmark issuer's sovereign default spread.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B20 — PASS
Bottom-up beta uses cash-corrected unlevered industry data, segment weights totaling 100%, and the applicable market D/E. Regression index/window/frequency/date are disclosed or marked unavailable.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B21 — PASS
Geographic revenue weights total 100%; regional proxies and missing coverage are explained.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B22 — PASS
Equity CRP, sovereign default spread and mature/total ERP are separate; January 2026 examples are not treated as timeless inputs.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B23 — PASS
Base Ke uses the additive weighted CRP; beta-scaled comparison is shown. Lambda is used only with supported exposure data and no duplicate adjustment.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B24 — PASS
External Ke comparisons identify actual method/vintage; unavailable market-implied rates are not invented.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B25 — FAIL_OPEN
Actual rating, synthetic coverage, company spread and bond-yield check are documented; incremental country adjustment has a justified coefficient and no duplicate sovereign risk.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Actual and synthetic rating/spread checks supplied; current comparable bond YTM/CDS missing.

### B26 — PASS
WACC uses market weights and consistent leverage; weights sum to one, including preferred securities where relevant. No automatic preferred tax shield or arbitrary CoCo split.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B27 — PASS
FCFE uses Ke and FCFF uses WACC, including correct cumulative factors when rates vary and disclosed stub/midyear timing.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B28 — FAIL_OPEN
Equity bridge handles cash, debt, NCI, preferred/hybrid claims, associates, pensions and provisions once; FCFE does not subtract debt twice.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: No double counting detected. Associates9937, NCI2003, pension1821 and debt fair premium295 use book/estimated-tax/fair-value proxies; material current claim valuation unverified.

### B29 — FAIL_OPEN
Common-share denominator, dilution, quote units, FX and market-cap calculation reconcile.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: FX/units and arithmetic reconcile, but cutoff shares/dilution are estimates and exchange close independently unavailable.

### B30 — PASS
Terminal value's discounted share and denominator are disclosed; >75% is flagged, invalid/negative-base ratios explained.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Discounted terminal share78.7242% flagged >75%. Warning disclosed, not treated as reassurance.

### B31 — PASS
Low/base/high and rate×g sensitivity, key driver ranking, DCF-implied multiples and material convention impacts are shown.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B32 — PASS
Literature citations are verified; decisions, anomaly effects and missing data are documented.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B33 — PASS
Workbook formulas reference inputs and recalculate without errors; supporting valuation tests actually ran with results recorded.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### B34 — PASS
dcf_model.xlsx, dcf_decisions.md, source_log.csv, qa_results.md and dcf_summary.png exist and reconcile.
- Evidence: dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C01 — PASS
Scope stated: single target in outputs/<ticker>_<date>/relative/ (orchestrator) or batch in outputs/relative_<date>/. Peer candidates and cross-checks come from the agent's own research (no group workbook). Data route confirmed/reused; full versus minimum universe stated. One valuation/FX date, cutoff and separately named FY/TTM/forward bases recorded.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C02 — PASS
Target list, selected peers and broad regression market remain distinct; internal A–F buckets are not used as unverified GICS sectors.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C03 — FAIL_OPEN
Raw financials and class-level market cap reconcile within 2%; price currencies/GBX, reporting currencies, ADRs, share classes and dilution are handled explicitly.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Selected numeric cap checks within2%; quote/report FX and GBX fixed. All class/treasury-share/ADR/perimeter evidence not independently completed.

### C04 — FAIL_OPEN
Field-level sources, membership vintage, exact industry mapping, fallback formulas and all transformations are logged. No unsupported imputation or per-row web-source switching.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Field extracts and dates supplied; primary industry/classification and some identifier/ownership evidence not fully verified. Source-policy conflict1667 versus3628 EBIT retained.

### C05 — FAIL_OPEN
>50% benchmark gaps are investigated and resolved; benchmark median/period/industry comparability is verified.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: A matched industry median from the registered reference assets is unavailable. Regional aggregate is not mislabeled median; cannot complete benchmark-gap resolution.

### C06 — PASS
Human Spot_check status is recorded separately; pending/waived review is never described as performed.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Human review explicitly pending, not described as performed. This disclosure pass is not a human audit pass.

### C07 — PASS
No DCF-proximity/size-based weighting, generic 30% weight cap, or assumption selection aimed at matching DCF remains in the stage 3 base.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C08 — FAIL_OPEN
Each target has 10 distinct qualified peers, or 8–9 with an explicit feasible shortfall; below 8 is blocked. Counts/CSV totals reflect actual coverage.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Nine preliminary candidates satisfy count constraints after all ordered relaxations. They are NOT nine fully qualified audited peers yet; no padding.

### C09 — FAIL_OPEN
All hard filters applied, including developed-market status, financial/holding exclusions, EUR1bn minimum, permitted size band, ownership, restructuring, history and missing metrics.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Ownership >20%, FY24-25 restructuring and some classification/primary identifier checks not complete for every selected peer. Preliminary gates cannot be treated as passes.

### C10 — PASS
At least 6 Tier 1–2 (8 under the default Tier 3 cap) and 5 Europe-listed peers; Tier 3<=2 unless explicit permitted relaxation to 4, always also <=peer_count−6. No other filter relaxed.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: 9 peers,6 Tier1/2,3 Tier3,6Europe; cap4 relaxation, Tier3<=9-6. Count pass only, eligibility still failed atC08/C09.

### C11 — PASS
20–30 initial candidate pool, expansions, full rejected/ranked list, score parameters and business-description review are auditable.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C12 — PASS
Eight score weights sum to one; pool-only 5%/95% clipping, standardization, common metric fallback definitions, missing-dimension renormalization and zero-variance handling are reproducible.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C13 — FAIL_OPEN
Consensus coverage rule applied before missing-data exclusion; >30% gap switches whole target/pool to fundamental growth, with method labels.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Uniform approved fundamental proxy used; no verified whole-pool consensus-coverage percentage audit. No claimed analyst five-year growth.

### C14 — PASS
Full required multiple set computed or marked unavailable/NM; positive peer extremes retained. Regression PE cap/clipping are not applied to peer statistics.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C15 — PASS
Every used raw AND scaled multiple has >=6 valid observations. Median/mean/p25/p75 shown; >25% mean–median skew flagged.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C16 — PASS
Raw and adjusted values shown; PEG uses percentage-point growth and matched basis. Positive-driver safeguards and scaled-ratio quartiles applied.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C17 — PASS
One primary multiple per valued target follows business suitability/ordered fallback. CF and replacement-cost definitions are defensible; limitations explicit.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C18 — FAIL_OPEN
EV-to-equity inverse matches peer numerator, including associates/leases/NCI/other claims once; quote-currency share value and upside reconcile.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: EV before associates only. Required matched associate/perimeter adjustments cannot be completed; EV numbers are qualified checks, not primary fair values.

### C19 — FAIL_OPEN
Three reproducibly random EV calculations checked; all selected ISINs verified and each peer has an economic inclusion reason/source.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Three seeded mechanical EV checks present, but not all selected primary ISIN and inclusion evidence verified; human Spot_check pending.

### C20 — PASS
Peer-set, quartile, multiple and material normalization sensitivities are reported; peer interquartile ranges are not called confidence intervals.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C21 — PASS
comparables.csv, multiples_summary.csv and comparables_report.md exist; scoring/selection/Spot_check audit schedules are provided.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C22 — PASS
Master first 18 columns and appended fields match the schema; all targets retained. Complete eligible universe, raw-row count and excluded records reconcile per model.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Published-route one-target master retains first18 fields and appended n/a outputs; no local estimation market sample claimed.

### C23 — N/A_PUBLISHED_ROUTE
Europe/World A ladder and B/C whole-market fallback logged per model. Full/minimum post-clean sample gates respected; losses excluded only from invalid models.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.

### C24 — N/A_PUBLISHED_ROUTE
Beta replacement uses >2.5/missing/negative rule before final missing-X exclusion; original and sourced replacement logged. Observed payout retained, cap only in growth formula.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.

### C25 — PASS
Unit conversions follow source metadata; median>1 is only a review trigger. FY and TTM PE not mixed; regression ROE/growth differs explicitly from DCF/peer fields where applicable.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C26 — N/A_PUBLISHED_ROUTE
Raw ratio formulas retained; estimation Y and continuous X winsorized at 1%/99%, dummies untouched. Raw-IQR flags preserved; B/C use identical model rows/cutoffs.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.

### C27 — N/A_PUBLISHED_ROUTE
PE/PBV/PS/EVEBITDA specs correct; PBV has no extra g. B sector reference and World A/B region coding valid; C has no dummies. ET off unless requested.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.

### C28 — N/A_PUBLISHED_ROUTE
Constant/redundant X handled explicitly; full rank, n, retained k, df and positive SEy verified. Model-specific names/ranges prevent cross-model references.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.

### C29 — N/A_PUBLISHED_ROUTE
Live LINEST, reverse coefficient mapping, SE/t/p/CI/R²/adjusted R²/F/SS/VIF and prediction formulas used; no static ToolPak coefficients or broken external links.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.

### C30 — PASS
Workbook actually recalculated and formulas preserved; only documented unused LINEST error cells remain.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C31 — N/A_PUBLISHED_ROUTE
Independent OLS on identical transformed rows/design matches at <1e−6 relative difference, with stated near-zero absolute tolerance; three predictions checked.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.

### C32 — N/A_PUBLISHED_ROUTE
Typicality pure-play/ROE-beta-payout-g percentile/valid-A tests recorded per target/model. Routed eligible adjusted-R² ranking and next-two alternatives reproducible.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.

### C33 — PASS
Actual target valuations and clipped estimation diagnostics separate; positive predictions/valid denominators required. Unvalued/excluded targets remain in output.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C34 — N/A_PUBLISHED_ROUTE
D1–D10 computed with required restrictions. DFR/ambiguous signs not invented; residual bands use exact boundaries and aren't presented as proof of mispricing.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.

### C35 — N/A_PUBLISHED_ROUTE
Triggered outlier/highest-VIF robustness separate from unchanged base; refit infeasibility/changed classifications recorded.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.

### C36 — N/A_PUBLISHED_ROUTE
Same chosen multiple compared across A/B/C; no claim A−C equals a sector dummy. Published Global/Western Europe checks respect equation units and 30% rule or disclose unavailability.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.

### C37 — N/A_PUBLISHED_ROUTE
Spot_check contains targets plus 20 reproducibly random non-target rows; >2 confirmed errors repaired before final use.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.

### C38 — PASS
Four core regression files exist, report headings/values match workbook, one CSV row per requested target, review/model-quality statuses explicit.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C39 — PASS
Equation obtained through `datasets.equation_for`; dataset id, vintage, as-of date, region used, match level and warnings recorded. As-of date not after the valuation date; age versus valuation date stated.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C40 — PASS
Integrity check of the regressions dataset run; every warning (sign anomalies, identical t-statistics, units) addressed; an equation flagged as an anomaly is not used until verified.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C41 — PASS
Every input follows the FILE's definition (analyst g_eps / g_rev, observed beta, payout >= 0). Any substituted input is labelled `substituted_input` and was approved in standing approvals.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C42 — PASS
Unit policy handled: both policies computed where DFR or tax rate is used, plausibility check against the sector median recorded, chosen policy justified or `units_unverified` shown.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Approved decimal policy. PBV/PE do not contain DFR/tax; both policies identical. EV equation not used, so no sector plausibility claim is made.

### C43 — PASS
No SEy-based output appears: classification, std residual, adjusted R2, p-values, A/B/C and D1-D10 are `n/a_published_route`; deviation and equation R2 shown instead.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C44 — PASS
Workbook predictions equal `published_regressions.predict` to 1e-9 after recalculation; no PS equation invented; supplementary multiples (PEG, EV/IC, EV/Sales) labelled and not primary.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C45 — PASS
Summary states the limitations of section 7 of regression_published_route.md (market-wide scope, low R2, analyst-growth definition, vintage, undocumented EV definition).
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C46 — PASS
Dataset chosen by `datasets.resolve`, not by file name; fallback matches justified; vintage not after the valuation date; dataset id and sha256 in `source_log.csv`.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C47 — PASS
Logical-to-actual column mapping recorded; industry mapping uses exact industry names (`industry_row` raised no suggestion error); not-meaningful cells (for example Net CapEx/EBIT(1-t) of Steel and Railroads) not used.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### C48 — PASS
Low-confidence country mappings (`regions.csv`) acknowledged.
- Evidence: relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### D01 — PASS
Comparable primary estimate, regression selected estimate and DCF are shown independently before reconciliation; any final synthesis is justified without retroactive tuning.
- Evidence: report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### D02 — PASS
Final value is compared with the current market price. Any gap above 25% is explained.
- Evidence: report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### D03 — PASS
Fair value range and ONE recommended price stated. Mispricing in % and in currency.
- Evidence: report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### D04 — PASS
Recommendation tied to the annual report narrative and one mispriced parameter.
- Evidence: report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### D05 — PASS
Discussion of market expectations and current conditions included.
- Evidence: report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### D06 — PASS
Extraordinary items commented on.
- Evidence: report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### D07 — PASS
recommendation_summary.csv written.
- Evidence: report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### D08 — PASS
Same method and thresholds as in the other companies, or deviations justified.
- Evidence: report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### D09 — PASS
No reference to relative_model.xlsx, weights_table or relative_decisions.md remains; any stage 4 synthesis weights are stated, justified and not tuned to the DCF or the market price.
- Evidence: report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### D10 — PASS
Report outline approval reused or requested per report_template.md; work was not blocked while waiting.
- Evidence: report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures
- Reason/impact: Direct original user task authorizes proceeding with the approved outline; legacy standing field not yet is preserved and disclosed. Default13-chapter outline reused with steel/published-route adaptations.

### D11 — PASS
Data gaps section lists everything missing or estimated.
- Evidence: report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.

### D12 — PASS
Plain-English summary is readable by a non-specialist. Glossary and disclaimer included.
- Evidence: report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures
- Reason/impact: Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.
