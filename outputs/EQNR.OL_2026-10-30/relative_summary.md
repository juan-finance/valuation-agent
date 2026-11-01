# Equinor ASA (EQNR.OL) — short relative-only report

Valuation date2026-10-30 | price date2026-10-30 | accessed2026-11-01 | NOK/share unless stated.

STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.

Scope: EQNR.OL only; standard / published_damodaran / web_minimum. 2026-10-30 dated cache reused; stage0 Norway sovereign top-up only. Full Stage1, DCF and Stage4 skipped by approved relative_only deviation. Mandatory short PDF supplied per explicit user override of no-PDF default.

1. Financial basis and definitions

FY2025 calendar year (not TTM/forward); USDm. Sales105828 (as-reported106462); EBIT26437 (issuer net operating income25352, +4.3% vendor gap); D&A8874; EBITDA35311; CFO19971; capex13994; common equity40424; assets131727; debt incl leases31221; cash&ST19333; NCI74; LT investments15343 excluded from EV bridge; dividends paid4791.

Issuer cross-check via SEC 6-K Q4 report: group NI5058 = parent5043 + NCI15; EPS1.94, DPS1.50. Petroleum effective tax79.84% (tax20030/pretax25088) far above European peers; flagged. Closing-parent-ROE x capped-retention fundamental growth0.6234% is NOT analyst consensus and is an approved substituted_input for the published route.

Current quote447.5 NOK; shares2380m; market cap NOK1065410m ≈ EUR102793m (ECB2026-10-30, USD→NOK9.2302). EV NOK1175791m using debt+NCI−cash&ST; LT investments not in bridge. Vendor negative beta−0.65 replaced by bottom-up relevered beta0.4769 (Oil/Gas Integrated EUROPE cash-corrected unlevered0.41, marginal tax40%, market D/E).

2. Peer diagnostics — not source-qualified fair value

33 initial candidates; final numeric10 peers, 10 Tier1/2, 0 Tier3, 8 Europe-listed. Standard proxies: IEUR MSCI Europe IMI for European names, URTH MSCI World (holdings2026-10-29) entity/name match for US/Canada. Ordered expansions: Europe -> World ->0.05–20x size ->Tier3 cap4. No other hard filter waived. Peers: REP, SHEL, TTE, OMV, ENI, XOM, BP, AKRBP, COP, VAR.

Eight score weights: growth30%, beta15%, net debt/EBITDA10%, ROE10%, EBITDAmargin10%, payout7.5%, capex/sales7.5%, log EURcap10%. Pool-only5/95 clipping/sampleSD; positive extremes retained. Vendor 5Y betas across the pool are implausibly low/negative (uniform source, disclosed); distance driven mainly by size/leverage/margins.

Bucket F primary EV/EBITDA, unscaled per procedure rule 118 (no prescribed EV driver; EV/Sales-by-margin equivalent is not independent evidence). Peer EV/EBITDA median7.468431x; Target growth0.6234% vs peer median growth1.3597% (same fundamental basis). Indicative value976.369995NOK; peer-IQR dispersion791.761390–1111.073257; vs quote118.1832%. IQR is NOT a confidence interval; peer EV basis is pre-LT-investment and qualified only.

Raw equals chosen basis (unscaled): 976.369995NOK. Cross-checks EV/CF then PE in multiples_summary.csv; TobinQ and matching-index relativePE unavailable, not invented. BP FY2025 NI collapse (PE2362) retained as positive extreme.

3. Published-regression diagnostics

Norway resolves EUROPE exact; January2026 equations asof2026-01-01 (302days old). No market estimation, sector-specific fit, SEy, p-values, adjustedR2, A/B/C, D1–D10 or residual classification. Classification: Not classified (no SEy published). Model choice by highest publishedR2 is a weak heuristic only.

PE: prediction19.037678683x; publishedR20.201; implied372.338531NOK. Equation: 9.72 +2.99 beta +49.82 g_eps +7.98 payout.

PBV: prediction1.920014456x; publishedR20.423; implied301.008531NOK. Equation: .73 +3.92 g_eps +.13 beta +10.75 ROE -.25 payout.

EV/EBITDA: prediction18.483749957x; publishedR20.262; implied2484.858932NOK. Equation: 18.15 +35.25 g_rev -.11 DFR -.12 tax +2.29 ROIC.

Chosen published PBV implied301.008531NOK; vs quote-32.7355%. Highest publishedR20.423, not sector fit or proof of mispricing. Decimal DFR/tax policy explicitly approved; EV/EBITDA alternative percent-point prediction6.671111774x. Both scenarios preserved; source-unit ambiguity not resolved by approval.

Registered dataset regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5. GLOBAL PEG sign/tstat, GLOBAL PBV beta sign and EM ROIC sign warnings not used. All exact coefficients/tstats and input IDs in live workbook; post-LibreOffice recalculation all predictions/prices/scores agree with library within1e-9. Published EV definition undocumented.

4. Benchmark, sensitivity and limits

Closest Oil/Gas (Integrated) EUROPE published ratios: EVEBITDA5.94x (12 firms, pos-EBITDA basis), PBV2.14. E&P alternative2.66x (83 firms). These are NOT verified industry medians; aggregate-versus-median comparison remains a QA failure. Target EVEBITDA3.59x sits between E&P and Integrated published ratios. Peer-scaled EV/EBITDA median above target multiple drives the large positive peer-diagnostic gap; not proof of mispricing.

Sensitivities: raw/scaled and peer quartiles, leave-one-out peer set, target EBITDA −10% cyclicality diagnostic (not normalized), cash-definition EV bridge (+USD5.6bn sensitivity); details in sensitivities.csv. No substantiated uniform normalization constructed.

Unresolved QA: full two-way ownership/event/history qualification for all candidates, authentic matching industry medians, uniform material-one-off normalization and comparable EV claim/lease/LT-investment consistency. Three seeded arithmetic EV checks PASS, human Spot_check PENDING (not performed/waived). Ten numeric names do not satisfy ten qualified peers until these gates are cleared. No final fair-value recommendation is issued.

5. Source and reproducibility pointers

Uniform raw financial/statistics/history: https://stockanalysis.com/quote/osl/EQNR/financials/ and peer-specific URLs in relative/source_log.csv. Issuer: Equinor Q4-2025 SEC 6-K report (linked in relative_inputs.md). Standard proxy dated2026-10-29: https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv . Library IDs/SHA/vintage/mappings and all qualification evidence: relative/evidence_review.md, regression_results.json, dataset_checks.json, candidate_gates.csv. All numbers derive from the attached run artifacts; no DCF used.

Reproduce from repository root: PYTHONPATH=src python outputs/EQNR.OL_2026-10-30/relative/build.py; LibreOffice headless recalculate both workbooks in a separate directory, compare with formula_checks.json. finalize_stage3.py is a one-time checkpoint helper, not safe to rerun on finished state. qa_and_report.py intentionally refuses a second full QA run. Cached parsed data and source locators committed; market cache never rebuilt except the approved Norway sovereign top-up.

Academic analysis only. Not investment advice; source limitations and model assumptions can materially change results.
