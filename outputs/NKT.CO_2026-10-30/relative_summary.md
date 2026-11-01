# NKT A/S (NKT.CO) - short relative-only report

Valuation date 2026-10-30 | price date 2026-10-30 | accessed 2026-11-01 | EUR/share unless stated (quote DKK 839.0 = EUR 112.26 at ECB 7.4735).

STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.

Scope: NKT.CO only; standard / published_damodaran / web_minimum. 2026-10-30 dated cache reused; stage0 Denmark sovereign top-up only. Full Stage1, DCF and Stage4 skipped by approved relative_only deviation. Mandatory short PDF supplied per explicit user override of no-PDF default.

1. Financial basis and definitions

FY2025 calendar year (not TTM/forward); EURm. Sales 3,565; EBIT 578 / EBITDA 680 vendor-uniform basis (issuer EBIT 257 / operational EBITDA 390; pretax 294 reconciles exactly - dominant divergence, sensitivities shown); NI 275; NI to common 264 (hybrid coupon ~11 stripped); group equity 2,193 incl EUR 150m equity-classified hybrid -> common 2,043; debt incl leases 251; cash&ST 1,214 (net cash 963); NCI 0; CFO 499; capex 695; dividends paid 11; effective tax 6.46% one-off-driven (tax 19/pretax 294).

Issuer cross-check via NKT annual report 2025: revenue 3,565, NI 275, equity 2,193, NIBD -963, CFO 499, CapEx -695 match vendor exactly. Hybrids: EUR 150m 7.24% callable 1-Jul-2026 (DK0030510995) and EUR 150m 5.00% issued Mar 2026; equity-classified - claim deducted once in the EV-to-common bridge.

Current quote DKK 839.0 (EUR 112.26); shares 53.45m; market cap EUR ~6,001m. EV EUR 5,038m = 6,001+251+0-1,214 (debt+NCI-cash&ST); LT investments not in bridge. Vendor beta 0.65 kept (within 0-2.5 band); no relevering needed.

2. Peer diagnostics - not source-qualified fair value

31 candidate rows collected, Europe-first; first Europe step already feasible - 10 numeric peers, 8 Tier1/2, 2 Tier3, 10 Europe-listed; no relaxation step used. Standard proxies: IEUR MSCI Europe IMI for European names. Hard exclusions: ELHA (Greece MSCI EM), GEV (Apr-2024 spin-off inside FY2024-25 comparison period + one-off FY2025 tax benefit), ATCO.A/EPI.A (dual-class cap reconciliation >2%). Peers: G1A, NEX, VWS, TKA, PRY, SKF.B, IMI, SPX, ANDR, LR.

Eight score weights: growth 30%, beta 15%, net debt/EBITDA 10%, ROE 10%, EBITDA margin 10%, payout 7.5%, capex/sales 7.5%, log EUR cap 10%. Pool-only 5/95 clipping/sampleSD; positive extremes retained. Vendor betas carry a benchmark/frequency-unavailable flag; distance driven mainly by size/leverage/margins.

Bucket-D primary PE (scaled by growth, 10 valid). Peer PE median 26.3847x raw / 30.5862x growth-scaled; target growth 12.38% fundamental (ROE x retention). Indicative value 151.071130 EUR (scaled); raw-basis 130.319193 EUR; peer-IQR dispersion 95.113240-240.990149 EUR; vs EUR quote 34.5685%. IQR is NOT a confidence interval.

Cross-check EV/EBIT median 19.5306x -> 226.411528 EUR (qualified: pre-LT-investment perimeter, hybrid claim once). Other multiples in multiples_summary.csv; relative PE (matching index) and Tobin Q unavailable, not invented.

3. Published-regression diagnostics

Denmark resolves EUROPE exact; January 2026 equations as-of 2026-01-01 (302 days old). No market estimation, sector-specific fit, SEy, p-values, adjusted R2, A/B/C, D1-D10 or residual classification. Classification: Not classified (no SEy published). Model choice by highest published R2 is a weak heuristic only.

PE: prediction 18.165583945x; published R2 0.201; implied 89.723371 EUR. Equation: 9.72 +2.99 beta +49.82 g_eps +7.98 payout.

PBV: prediction 2.678659936x; published R2 0.423; implied 102.385449 EUR. Equation: .73 +3.92 g_eps +.13 beta +10.75 ROE -.25 payout.

EV/EBITDA: prediction 23.509668620x; published R2 0.262; implied 319.582613 EUR. Equation: 18.15 +35.25 g_rev -.11 DFR -.12 tax +2.29 ROIC. Extreme implied value driven by substituted 12.4% growth and vendor EBITDA basis - diagnostic only.

Chosen published PBV implied 102.385449 EUR; vs EUR quote -8.7988%. Highest published R2 0.423, not sector fit or proof of mispricing. Decimal DFR/tax policy explicitly approved; EV/EBITDA alternative percent-point prediction 22.304631721x.

Registered dataset regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5. GLOBAL PEG sign/tstat, GLOBAL PBV beta sign and EM ROIC sign warnings not used. All exact coefficients/tstats and input IDs in live workbook; post-LibreOffice recalculation all predictions/prices/scores agree with library within 1e-9. Published EV definition undocumented.

4. Benchmark, sensitivity and limits

Closest Electrical Equipment EUROPE published ratios: EVEBITDA 18.94x, EVEBIT 24.34x (146 firms, pos-EBITDA basis), PBV 5.71. Machinery alternative: 14.98x / 4.05 (210 firms). These are NOT verified industry medians; aggregate-versus-median comparison remains a QA failure.

Sensitivities: raw/scaled and peer quartiles, leave-one-out peer set, group-NI 275 (vs common 264), issuer EBITDA 390 and issuer EBIT 257 basis diagnostics (vs vendor 680/578) in sensitivities.csv. No substantiated uniform normalization constructed.

Unresolved QA: full two-way ownership/event/history qualification for all candidates, authentic matching industry medians, uniform material-one-off normalization and comparable EV claim/lease/LT-investment consistency. Three seeded arithmetic EV checks PASS, human Spot_check PENDING (not performed/waived). Ten numeric names do not satisfy ten qualified peers until these gates are cleared. No final fair-value recommendation is issued.

5. Source and reproducibility pointers

Uniform raw financial/statistics/history: https://stockanalysis.com/quote/cph/NKT/financials/ and peer-specific URLs in relative/source_log.csv. Issuer: NKT annual report 2025 (linked in relative_inputs.md). Standard proxy dated 2026-10-29: https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv . Library IDs/SHA/vintage/mappings and all qualification evidence: relative/evidence_review.md, regression_results.json, dataset_checks.json, candidate_gates.csv. All numbers derive from the attached run artifacts; no DCF used.

Reproduce from repository root: PYTHONPATH=src python outputs/NKT.CO_2026-10-30/relative/build.py; LibreOffice headless recalculate both workbooks in a separate directory, compare with formula_checks.json. finalize_stage3.py is a one-time checkpoint helper, not safe to rerun on finished state. qa_and_report.py intentionally refuses a second full QA run. Cached parsed data and source locators committed; market cache never rebuilt except the approved Denmark sovereign top-up.

Academic analysis only. Not investment advice; source limitations and model assumptions can materially change results.
