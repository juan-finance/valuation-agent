# TotalEnergies SE (TTE.PA) — short relative-only report

Valuation date 2026-10-30 | price date 2026-10-30 | accessed 2026-11-02 | EUR/share unless stated.

STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.

Scope: TTE.PA only; standard / published_damodaran / web_minimum. 2026-10-30 dated cache reused as approved (France/USD/EUR already present); no stage-0 rebuild or top-up. Full Stage1, DCF and Stage4 skipped by approved relative_only deviation. Mandatory short PDF supplied per explicit user override of no-PDF default.

1. Financial basis and definitions

FY2025 calendar year (not TTM/forward); USDm. Revenues from sales 182,344 (= issuer exactly; issuer headline Sales 201,196 is a broader aggregate); EBIT 19,733 (issuer adjusted net operating income 18,474, −6.4% APM basis); EBITDA 32,770 = EBIT + D&A 13,037 (issuer adjusted EBITDA 40,555 includes equity affiliates, not used); CFO 27,343 (= issuer); CFFO 27,839; DACF 29,255; capex 15,756; parent common equity 114,883; assets 291,055; debt incl. leases 61,421; cash & ST investments 29,214; NCI 2,640; LT investments 42,462 (incl. equity affiliates) excluded from EV bridge; dividends paid 8,424; buybacks 8,853.

Issuer cross-check via SEC 6-K exhibit 99.1 (filed 2026-02-11): NI share 13,127 = vendor exactly; diluted EPS 5.78; declared DPS 3.992. Effective tax 40.5% (tax 9,092 / pretax 22,449). Closing-parent-ROE x capped-retention fundamental growth 4.04% is NOT analyst consensus and is an approved substituted_input for the published route.

Current quote EUR 85.43; shares 2,210m; market cap EUR 188.52bn ≈ USD 210.6bn (ECB 2026-10-30, USD 1.1172/EUR). EV USD 245.5bn using debt + NCI − cash & ST investments; LT investments/equity affiliates not in bridge. Vendor 5Y beta 0.04 kept as observed (positive, <2.5) but flagged very low for an integrated oil major.

2. Peer diagnostics — not source-qualified fair value

33 initial candidates; Europe step infeasible (8), World developed-market relaxation (a) applied -> pool 16; final numeric 10 peers, 10 Tier1/2, 0 Tier3, 5 Europe-listed (min 5 met). Proxies: IEUR MSCI Europe IMI for European names, URTH MSCI World (holdings 2026-10-29) entity/name match for US/Canada. No other hard filter waived; Tier 3 cap and size-band relaxations not invoked. Peers: SHEL, XOM, COP, VLO, REP, EQNR, ENI, CVX, OMV, EOG.

Eight score weights: growth 30%, beta 15%, net debt/EBITDA 10%, ROE 10%, EBITDA margin 10%, payout 7.5%, capex/sales 7.5%, log EUR cap 10%. Pool-only 5/95 clipping/sample SD; positive extremes retained. Vendor 5Y betas across the pool are implausibly low/negative (uniform source, disclosed); distance driven mainly by size/leverage/margins.

Bucket F primary EV/EBITDA, unscaled per procedure (no prescribed EV driver). Peer EV/EBITDA median 8.43x (p25 7.56 / p75 12.64); target 7.49x; target fundamental growth 4.04% vs peer median 3.31%. Indicative value 97.74 EUR; peer-IQR dispersion 86.21–153.71; vs quote 14.4%. IQR is NOT a confidence interval; peer EV basis is pre-LT-investment and qualified only.

Cross-checks EV/CF then PE in multiples_summary.csv (EV/CF median 8.75x, PE median 23.1x; BP FY2025 NI collapse PE 2362 retained as positive extreme). Tobin Q and matching-index relative PE unavailable, not invented.

3. Published-regression diagnostics

France resolves EUROPE exact; January 2026 equations as-of 2026-01-01 (~305 days old). No market estimation, sector-specific fit, SEy, p-values, adjusted R2, A/B/C, D1–D10 or residual classification. Classification: Not classified (no SEy published). Model choice by highest published R2 is a weak heuristic only.

PE: prediction 17.00x; published R2 0.201; implied 90.38 EUR; actual 16.04, gap -6%. Equation: 9.72 + 2.99 beta + 49.82 g_eps + 7.98 payout.

PBV: prediction 1.96x; published R2 0.423; implied 91.37 EUR; actual 1.83, gap -7%. Equation: 0.73 + 3.92 g_eps + 0.13 beta + 10.75 ROE - 0.25 payout.

EV/EBITDA: prediction 19.70x; published R2 0.262; implied 247.39 EUR; actual 7.49, gap -62%. Equation: 18.15 + 35.25 g_rev - 0.11 DFR - 0.12 tax + 2.29 ROIC.

Chosen published PBV implied 91.37 EUR; vs quote 6.9%. Highest published R2 0.423, not sector fit or proof of mispricing. Decimal DFR/tax policy explicitly approved; EV/EBITDA alternative percent-point prediction 12.43x. Both scenarios preserved; source-unit ambiguity not resolved by approval. EV/EBITDA equation predicted 19.7x vs actual 7.5x (−62%): market-wide equation cannot see oil-major pricing; headline limitation, not a mispricing signal.

Registered dataset regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5. GLOBAL PEG sign/tstat, GLOBAL PBV beta sign and EM ROIC sign warnings not used (EUROPE equations only). All exact coefficients/t-stats and input IDs in live workbook; Python formula re-evaluation (LibreOffice absent on this box) agrees with library predictions within 1e-9, disclosed. Published EV definition undocumented.

4. Benchmark, sensitivity and limits

Closest Oil/Gas (Integrated) EUROPE published ratios in industry_benchmarks.json are NOT verified medians; aggregate-versus-median comparison remains a QA failure. Peer EV/EBITDA median 8.43x vs published integrated ratio recorded, not "fixed" to match. Target EV/EBITDA 7.49x near peer p25.

Sensitivities: raw/scaled and peer quartiles, leave-one-out peer set, target EBITDA −10% cyclicality diagnostic (not normalized), LT-investments/equity-affiliate exclusion note; details in sensitivities.csv. No substantiated uniform normalization constructed.

Unresolved QA: full two-way ownership/event/history qualification for all candidates, authentic matching industry medians, uniform material-one-off normalization and comparable EV claim/lease/LT-investment consistency (TTE equity affiliates 2,553 in EBIT vs LT investments 42,462 outside EV). Three seeded arithmetic EV checks PASS, human Spot_check PENDING (not performed/waived). Ten numeric names do not satisfy ten qualified peers until these gates are cleared. No final fair-value recommendation is issued.

5. Source and reproducibility pointers

Uniform raw financial/statistics/history: https://stockanalysis.com/quote/epa/TTE/financials/ and peer-specific URLs in relative/source_log.csv. Issuer: TotalEnergies Q4/FY2025 SEC 6-K exhibit 99.1 (linked in relative_inputs.md). Standard proxy dated 2026-10-29: https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv . Library IDs/SHA/vintage/mappings and all qualification evidence: relative/evidence_review.md, regression_results.json, dataset_checks.json, candidate_gates.csv. All numbers derive from the attached run artifacts; no DCF used.

Reproduce from repository root: PYTHONPATH=src python outputs/TTE.PA_2026-10-30/relative/build.py; formula re-evaluation in Python (LibreOffice absent — disclosed), compare with formula_checks.json. finalize_stage3.py is a one-time checkpoint helper, not safe to rerun on finished state. qa_and_report.py intentionally refuses a second full QA run. Cached parsed data and source locators committed; market cache never rebuilt (no top-up needed: France/USD/EUR already dated).

Academic analysis only. Not investment advice; source limitations and model assumptions can materially change results.
