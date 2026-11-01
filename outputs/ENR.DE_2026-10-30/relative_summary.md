# Siemens Energy AG (ENR.DE) — short relative-only report

Valuation date2026-10-30 | information cutoff2026-10-30 | accessed2026-11-01 | EUR/share unless stated.

STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.

Scope: ENR.DE only; standard / published_damodaran / web_minimum. Germany/EUR dated cache reused, no Stage0 rebuild or top-up. Full Stage1, DCF and Stage4 skipped by approved relative_only deviation. Mandatory short PDF supplied per explicit user override of no-PDF default.

1. Financial basis and definitions

FY2025 ended2025-09-30 (not TTM/forward); EURm. Sales39077; parent NI1414; standardized vendor EBIT1569; income-statement D&A1111; EBITDA2680; CFO5821; capex1724; common equity10301 (prior9075); assets56637; lease-inclusive debt3966; cash9162; NCI375; associates703 book proxy.

Issuer operating2149 less equity-accounted580 reconciles vendor1569. ParentNI1414 plus minority271 reconciles group1685. EBITDA2680 is not cashflow D&A-based; customer advances make CFO unlike FCFF. FY2025 cash dividend0; proposed0.70 is not paid-FY2025 payout. NI/average-common-equity fundamental growth14.5954% for peers; closing-common-equity13.7278% for published route. Growth is NOT analyst consensus.

Current quote126.92; uniform vendor shares855.34m and rounded cap108560m. Issuer states850m ISSUED asof2026-10-13: outstanding/treasury definition unresolved. Cap arithmetic within0.00023% does not settle it. All fixed-equity per-share values at850m increase0.628235%.

2. Peer diagnostics — not source-qualified fair value

26 initial candidates; final numeric10 peers, 7 Tier1/2, 3 Tier3, 9 Europe-listed. Standard World proxy entity/name match used; IMI-only candidates excluded. Ordered expansions: Europe -> World ->0.05–20x size ->Tier3 cap4 (3 used). No other hard filter waived. Peers: WRT1V, VWS, SAND, ETN, SU, G1A, LR, METSO, ALFA, SPX.

Eight score weights: growth30%, beta15%, leverage10%, ROE10%, EBITDAmargin10%, payout7.5%, capex/sales7.5%, log EURcap10%. Pool-only5/95 clipping/sampleSD; positive extremes remain in multiple distributions. Full pool/selection/parameter/source schedules retained.

Equipment default EV/EBIT cannot be unqualified because peer associates/claim/lease definitions are unresolved; EV/sales shares the same bridge problem. PE used only as indicative equity fallback. Raw PE median31.243353x; growth-scaled PE median43.233905x (10 valid). Indicative scaled-PE value71.471861; peer-IQR dispersion60.560166–104.067212; vs quote-43.6875%. IQR is NOT a confidence interval.

Raw PE value51.649755. Share sensitivity at850m: indicative scaled PE71.920873; IQR60.940627–104.720999. Other full raw/scaled multiples/counts/skew in multiples_summary.csv; relativePE and TobinQ unavailable, not invented.

3. Published-regression diagnostics

Germany resolves EUROPE; January2026 equations asof2026-01-01 (302days old). No market estimation, sector-specific fit, SEy, p-values, adjustedR2, A/B/C, D1–D10 or residual classification. Classification: Not classified (no SEy published). Model choice by highest publishedR2 is a weak heuristic only.

PE: prediction22.090203039x; publishedR20.201; implied36.518282;850m sensitivity36.747702. Equation: 9.72 +2.99 beta +49.82 g_eps +7.98 payout.

PBV: prediction2.984224881x; publishedR20.423; implied35.939510;850m sensitivity36.165295. Equation: .73 +3.92 g_eps +.13 beta +10.75 ROE -.25 payout.

EV/EBITDA: prediction23.492377566x; publishedR20.262; implied79.244010;850m sensitivity79.741849. Equation: 18.15 +35.25 g_rev -.11 DFR -.12 tax +2.29 ROIC.

Chosen published PBV implied35.939510; vs quote-71.6833%. Highest publishedR2.423, not sector fit or proof of mispricing. Decimal DFR/tax policy explicitly approved; EVEBITDA alternative percent-point prediction20.278194964x, implied69.173150. Both scenarios preserved; source-unit ambiguity not resolved by approval.

Registered dataset regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5. GLOBAL PEG sign/tstat, GLOBAL PBV beta sign and EM ROIC sign warnings not used. All exact coefficients/tstats and input IDs in live workbook; post-LibreOffice recalculation all predictions/prices/scores agree with library within1e-9. Published EV definition undocumented; no associate removal imposed on regression EV bridge.

4. Benchmark, sensitivity and limits

Closest Electrical Equipment EUROPE published ratios: EVEBITDA18.94, EVEBIT24.34, PBV5.71 (146 firms). Machinery/GreenRenewable alternatives investigated. These are NOT verified industry medians; aggregate-versus-median comparison remains a QA failure. Target EVEBITDA38.70858 is104.38% above18.94, plausibly recovery-priced against weak reported FY margins, not grounds to overwrite data. Neither unit policy >30% above18.94; this plausibility is not unit proof.

Sensitivities: raw/scaled and peer quartiles, leave-one-out peer set, all-observation EBIT margins4/6/8/10% (mechanical scaling largely cancels),850m share denominator, both unit policies; target-only net special-item+6 removal is a diagnostic, NOT uniform normalized peer earnings. Gross target restructuring/standalone costs exceed10% EBIT while offsetting portfolio gains mask net. No substantiated uniform normalization constructed.

Unresolved QA: full two-way ownership/event/history qualification for all candidates, valid outstanding shares, authentic matching industry medians, uniform material-one-off normalization and comparable EV claim/lease/associate consistency. Three seeded arithmetic EV checks PASS, human Spot_check PENDING (not performed/waived). Ten numeric names do not satisfy ten qualified peers until these gates are cleared. No final fair-value recommendation is issued.

5. Source and reproducibility pointers

Uniform raw financial/statistics/history: https://stockanalysis.com/quote/etr/ENR/financials/ and peer-specific URLs in relative/source_log.csv. Issuer: https://www.siemens-energy.com/global/en/home/investor-relations/share.html and FY2025 annual report (linked in relative_inputs.md / relative/evidence_review.md). Standard proxy dated2026-10-29: https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv . Library IDs/SHA/vintage/mappings and all qualification evidence: relative/evidence_review.md, regression_results.json, dataset_checks.json, candidate_gates.csv. All numbers derive from the attached run artifacts; no DCF used.

Reproduce from repository root: PYTHONPATH=src python outputs/ENR.DE_2026-10-30/relative/build.py; LibreOffice headless recalculate both workbooks in a separate directory, compare with formula_checks.json. finalize_stage3.py is a one-time checkpoint helper, not safe to rerun on finished state. qa_and_report.py intentionally refuses a second full QA run. Cached parsed data and source locators committed; market cache never rebuilt.

Academic analysis only. Not investment advice; source limitations and model assumptions can materially change results.
