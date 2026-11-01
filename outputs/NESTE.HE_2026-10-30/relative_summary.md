# Neste Oyj (NESTE.HE) — short relative-only report

Valuation date2026-10-30 | price date2026-10-30 | accessed2026-11-01 | EUR/share unless stated.

STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.

Scope: NESTE.HE only; standard / published_damodaran / web_minimum. 2026-10-30 dated cache reused; stage0 Finland sovereign top-up only. Full Stage1, DCF and Stage4 skipped by approved relative_only deviation. Mandatory short PDF supplied per explicit user override of no-PDF default.

1. Financial basis and definitions

FY2025 calendar year (not TTM/forward); EURm. Sales19016; EBIT466 (issuer503, 7.9% vendor gap); EBITDA1124 vendor-uniform basis (issuer reported1438 / comparable1683, sensitivities shown); CFO1747; capex910; common equity7314; assets15749; debt incl leases5183; cash&ST1367; NCI0; LT investments90 excluded from EV bridge; dividends paid154.

Issuer cross-check via Neste FY2025 financial statements release: NI144, EPS0.19, DPS0.20; effective tax27.64% (tax55/pretax199). ROE1.96% is a cyclical trough and payout1.069 capped at1.0 collapses fundamental growth to ~0; this substituted_input (approved for the published route) is NOT analyst consensus.

Current quote28.34 EUR; shares768.28m; market cap EUR21772m. EV EUR25586m = 21772+5183+0-1367 (debt+NCI-cash&ST); LT investments not in bridge. Vendor beta0.56 kept (within 0-2.5 band); no relevering needed.

2. Peer diagnostics — not source-qualified fair value

40 candidate rows collected, 38-name scored initial pool, Europe-first; Europe step infeasible (7 T12_EU under Tier3 cap2) -> World expansion (ordered step b) used, default Tier3 cap2 kept; final numeric10 peers, 8 Tier1/2, 2 Tier3, 8 Europe-listed. Standard proxies: IEUR MSCI Europe IMI for European names, URTH MSCI World (holdings2026-10-29) entity/name match for US/Canada. Ordered expansion World used; size band and Tier3 cap unchanged. No other hard filter waived. Peers: ENI, PSX, VLO, REP, SPM, OMV, TTE, SUBC, BP, EQNR.

Eight score weights: growth30%, beta15%, net debt/EBITDA10%, ROE10%, EBITDAmargin10%, payout7.5%, capex/sales7.5%, log EURcap10%. Pool-only5/95 clipping/sampleSD; positive extremes retained. Vendor 5Y betas across the pool are implausibly low/negative (uniform source, disclosed); distance driven mainly by size/leverage/margins.

Bucket F primary EV/EBITDA, unscaled per procedure rule 118 (no prescribed EV driver; EV/Sales-by-margin equivalent is not independent evidence). Peer EV/EBITDA median8.388418x; target growth0.00% vs peer median growth0.71% (same fundamental basis). Indicative value7.305385EUR; peer-IQR dispersion4.564674–9.563066; vs quote-74.2224%. IQR is NOT a confidence interval; peer EV basis is pre-LT-investment and qualified only.

Raw equals chosen basis (unscaled): 7.305385EUR. Cross-checks EV/CF then PE in multiples_summary.csv; TobinQ and matching-index relativePE unavailable, not invented. BP FY2025 NI collapse (PE2362) retained as positive extreme.

3. Published-regression diagnostics

Finland resolves EUROPE exact; January2026 equations asof2026-01-01 (302days old). No market estimation, sector-specific fit, SEy, p-values, adjustedR2, A/B/C, D1–D10 or residual classification. Classification: Not classified (no SEy published). Model choice by highest publishedR2 is a weak heuristic only.

PE: prediction19.374400000x; publishedR20.201; implied3.631376EUR. Equation: 9.72 +2.99 beta +49.82 g_eps +7.98 payout.

PBV: prediction0.764448893x; publishedR20.423; implied7.277528EUR. Equation: .73 +3.92 g_eps +.13 beta +10.75 ROE -.25 payout.

EV/EBITDA: prediction18.165061640x; publishedR20.262; implied21.608696EUR. Equation: 18.15 +35.25 g_rev -.11 DFR -.12 tax +2.29 ROIC.

Chosen published PBV implied7.277528EUR; vs quote-74.3206%. Highest publishedR20.423, not sector fit or proof of mispricing. Decimal DFR/tax policy explicitly approved; EV/EBITDA alternative percent-point prediction12.787522564x. Both scenarios preserved; source-unit ambiguity not resolved by approval.

Registered dataset regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5. GLOBAL PEG sign/tstat, GLOBAL PBV beta sign and EM ROIC sign warnings not used. All exact coefficients/tstats and input IDs in live workbook; post-LibreOffice recalculation all predictions/prices/scores agree with library within1e-9. Published EV definition undocumented.

4. Benchmark, sensitivity and limits

Closest Oil/Gas (Integrated) EUROPE published ratios: EVEBITDA5.94x (12 firms, pos-EBITDA basis), PBV2.14. E&P alternative2.66x (83 firms). These are NOT verified industry medians; aggregate-versus-median comparison remains a QA failure. Target EVEBITDA22.76x exceeds both published ratios; peer-median8.39x far below the target multiple drives the large negative indicative gap (implied below quote); not proof of mispricing.

Sensitivities: raw/scaled and peer quartiles, leave-one-out peer set, issuer EBITDA-basis diagnostic (vendor1124 vs reported1438 / comparable1683) and target EBITDA -10% cyclicality diagnostic (not normalized); details in sensitivities.csv. No substantiated uniform normalization constructed.

Unresolved QA: full two-way ownership/event/history qualification for all candidates, authentic matching industry medians, uniform material-one-off normalization and comparable EV claim/lease/LT-investment consistency. Three seeded arithmetic EV checks PASS, human Spot_check PENDING (not performed/waived). Ten numeric names do not satisfy ten qualified peers until these gates are cleared. No final fair-value recommendation is issued.

5. Source and reproducibility pointers

Uniform raw financial/statistics/history: https://stockanalysis.com/quote/hel/NESTE/financials/ and peer-specific URLs in relative/source_log.csv. Issuer: Neste FY2025 financial statements release (linked in relative_inputs.md). Standard proxy dated2026-10-29: https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv . Library IDs/SHA/vintage/mappings and all qualification evidence: relative/evidence_review.md, regression_results.json, dataset_checks.json, candidate_gates.csv. All numbers derive from the attached run artifacts; no DCF used.

Reproduce from repository root: PYTHONPATH=src python outputs/NESTE.HE_2026-10-30/relative/build.py; LibreOffice headless recalculate both workbooks in a separate directory, compare with formula_checks.json. finalize_stage3.py is a one-time checkpoint helper, not safe to rerun on finished state. qa_and_report.py intentionally refuses a second full QA run. Cached parsed data and source locators committed; market cache never rebuilt except the approved Finland sovereign top-up.

Academic analysis only. Not investment advice; source limitations and model assumptions can materially change results.
