# Shell plc (SHEL.L) — short relative-only report

Valuation date 2026-10-30 | price date 2026-10-30 | accessed 2026-11-02 | GBP/share unless stated.

STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.

Scope: SHEL.L only; standard / published_damodaran / web_minimum. 2026-10-30 dated cache reused as approved (United Kingdom/USD/GBP already present); no stage-0 rebuild or top-up. Full Stage1, DCF and Stage4 skipped by approved relative_only deviation. Mandatory short PDF supplied per explicit user override of no-PDF default.

1. Financial basis and definitions

FY2025 calendar year (not TTM/forward); USDm. Revenue 266,886 (issuer Total revenue and other income 273,731 recorded separately); EBIT 29,834; EBITDA 47,658 = EBIT + D&A-for-EBITDA 17,824 (issuer adjusted EBITDA 56,135, APM basis); CFO 42,863 (= issuer); capex 18,947; parent common equity 174,392; assets 370,350; debt incl. leases 75,688; cash & ST investments 30,216; NCI 927; LT investments 29,332 excluded from EV bridge; dividends paid 8,472; buybacks 15,179.

Issuer cross-check via Shell Q4/FY2025 results (published 2026-02-05): income attributable to shareholders 17,838 vs vendor 17,837; CFO 42,863 = vendor exactly; DPS 1.446 = vendor; basic EPS 3.03 = vendor. Effective tax 39.11% (tax 11,637 / pretax 29,756). Closing-parent-ROE x capped-retention fundamental growth 5.37% is NOT analyst consensus and is an approved substituted_input for the published route.

Current quote GBP 40.365 (4,036.5 GBX); shares 5,700m; market cap GBP 230.23bn ≈ EUR 276.12bn ≈ USD 308.47bn (ECB 2026-10-30, USD 1.1172/EUR, GBP 0.8338/EUR). EV USD 354.87bn using debt + NCI − cash & ST investments; LT investments/equity-accounted investments not in bridge. Vendor 5Y beta -0.19 is negative: retained for scoring with flag, replaced in the published regression by the relevered industry beta ~0.47.

2. Peer diagnostics — not source-qualified fair value

33 initial candidates; Europe step infeasible (5 eligible), World developed-market relaxation (a) applied -> pool 13; final numeric 10 peers, 10 Tier1/2, 0 Tier3, 5 Europe-listed (min 5 met). Proxies: IEUR MSCI Europe IMI for European names, URTH MSCI World (holdings 2026-10-29) entity/name match for US/Canada. No other hard filter waived; Tier 3 cap and size-band relaxations not invoked. Peers: TTE, XOM, COP, REP, EQNR, VLO, CVX, ENI, BP, EOG.

Eight score weights: growth 30%, beta 15%, net debt/EBITDA 10%, ROE 10%, EBITDA margin 10%, payout 7.5%, capex/sales 7.5%, log EUR cap 10%. Pool-only 5/95 clipping/sample SD; positive extremes retained. Vendor 5Y betas across the pool are implausibly low/negative (uniform source, disclosed); distance driven mainly by size/leverage/margins.

Bucket F primary EV/EBITDA, unscaled per procedure (no prescribed EV driver). Peer EV/EBITDA median 8.43x (p25 7.59 / p75 12.64); target 7.45x; target fundamental growth 5.31% vs peer median 3.31%. Indicative value 46.52 GBP; peer-IQR dispersion 41.30–72.83; vs quote 15.2%. IQR is NOT a confidence interval; peer EV basis is pre-LT-investment and qualified only.

Cross-checks EV/CF then PE in multiples_summary.csv (EV/CF median 9.10x, PE median 24.82x; BP FY2025 NI collapse PE 2362 retained as positive extreme). Tobin Q and matching-index relative PE unavailable, not invented.

3. Published-regression diagnostics

United Kingdom resolves EUROPE exact; January 2026 equations as-of 2026-01-01 (~305 days old). No market estimation, sector-specific fit, SEy, p-values, adjusted R2, A/B/C, D1–D10 or residual classification. Classification: Not classified (no SEy published). Model choice by highest published R2 is a weak heuristic only.

PE: prediction 17.59x; published R2 0.201; implied 41.09 GBP; actual 17.29, gap -2%. Equation: 9.72 + 2.99 beta + 49.82 g_eps + 7.98 payout.

PBV: prediction 1.98x; published R2 0.423; implied 45.27 GBP; actual 1.77, gap -11%. Equation: 0.73 + 3.92 g_eps + 0.13 beta + 10.75 ROE - 0.25 payout.

EV/EBITDA: prediction 20.16x; published R2 0.262; implied 119.75 GBP; actual 7.45, gap -63%. Equation: 18.15 + 35.25 g_rev - 0.11 DFR - 0.12 tax + 2.29 ROIC.

Chosen published PBV implied 45.27 GBP; vs quote 12.2%. Highest published R2 0.423, not sector fit or proof of mispricing. Decimal DFR/tax policy explicitly approved; EV/EBITDA alternative percent-point prediction 13.37x. Both scenarios preserved; source-unit ambiguity not resolved by approval. EV/EBITDA equation predicted 20.2x vs actual 7.4x (−63%): market-wide equation cannot see oil-major pricing; headline limitation, not a mispricing signal.

Registered dataset regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5. GLOBAL PEG sign/tstat, GLOBAL PBV beta sign and EM ROIC sign warnings not used (EUROPE equations only). All exact coefficients/t-stats and input IDs in live workbook; Python formula re-evaluation (LibreOffice absent on this box) agrees with library predictions within 1e-9, disclosed. Published EV definition undocumented.

4. Benchmark, sensitivity and limits

Closest Oil/Gas (Integrated) EUROPE published ratios in industry_benchmarks.json are NOT verified medians; aggregate-versus-median comparison remains a QA failure. Peer EV/EBITDA median 8.43x vs published integrated ratio recorded, not "fixed" to match. Target EV/EBITDA 7.45x below peer p25.

Sensitivities: raw/scaled and peer quartiles, leave-one-out peer set, target EBITDA −10% cyclicality diagnostic (not normalized), LT-investments/equity-affiliate exclusion note; details in sensitivities.csv. No substantiated uniform normalization constructed.

Unresolved QA: full two-way ownership/event/history qualification for all candidates, authentic matching industry medians, uniform material-one-off normalization and comparable EV claim/lease/LT-investment consistency (SHEL earnings from equity investments 1,618 in pretax vs LT investments 29,332 outside EV). Three seeded arithmetic EV checks PASS, human Spot_check PENDING (not performed/waived). Ten numeric names do not satisfy ten qualified peers until these gates are cleared. No final fair-value recommendation is issued.

5. Source and reproducibility pointers

Uniform raw financial/statistics/history: https://stockanalysis.com/quote/lon/SHEL/financials/ and peer-specific URLs in relative/source_log.csv. Issuer: Shell plc Q4/FY2025 unaudited results (linked in relative_inputs.md). Standard proxy dated 2026-10-29: https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv . Library IDs/SHA/vintage/mappings and all qualification evidence: relative/evidence_review.md, regression_results.json, dataset_checks.json, candidate_gates.csv. All numbers derive from the attached run artifacts; no DCF used.

Reproduce from repository root: PYTHONPATH=src python outputs/SHEL.L_2026-10-30/relative/build.py; formula re-evaluation in Python (LibreOffice absent — disclosed), compare with formula_checks.json. finalize_stage3.py is a one-time checkpoint helper, not safe to rerun on finished state. qa_and_report.py intentionally refuses a second full QA run. Cached parsed data and source locators committed; market cache never rebuilt (no top-up needed: United Kingdom/USD/GBP already dated).

Academic analysis only. Not investment advice; source limitations and model assumptions can materially change results.
