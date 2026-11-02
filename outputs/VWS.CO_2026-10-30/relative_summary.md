# Vestas Wind Systems A/S (VWS.CO) — short relative-only report

Valuation date 2026-10-30 | information cutoff 2026-10-30 | accessed 2026-11-02 | DKK/share unless stated.

STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.

Scope: VWS.CO only; standard / published_damodaran / web_minimum. Denmark/DKK dated cache reused (DKK 7.4735/EUR); no Stage 0 rebuild or top-up needed. Full Stage 1, DCF and Stage 4 skipped by approved relative_only deviation. Mandatory short PDF supplied per explicit user instruction.

1. Financial basis and definitions

FY2025 ended 2025-12-31 (calendar year); EURm. Revenue 18822; vendor EBIT 1067 (= issuer EBIT before special items; issuer reported 1015, special items -52 = 4.9% of EBIT, below the 10% normalized-alternative trigger); vendor EBITDA 1501 (issuer 2053, -26.9% definitional gap — favours EV/EBIT primary); NI 778 (issuer 780, minority -2); CFO 2286; PP&E capex 821 (total investments 1251 incl. intangibles 457); common equity 3867 (prior 3529); assets 25732; lease-inclusive debt 3374; cash 4384 + ST investments 164; NCI 14; LT investments 739 (recorded, not deducted — equity-investment earnings remain in denominators).

EV base: mcap 24772 (DKK 185.13bn / 7.4735) + debt 3374 + NCI 14 - cash 4384 = 23776 EURm. Pre-associate bridge; peer associates/claim/lease definitions unresolved (qualified status).

Current quote DKK 189.25 (Nasdaq Copenhagen, 2026-10-30 close); shares 978.25m current (weighted basic 999m). Declared FY2025 DPS DKK 0.74 (~EUR 0.10) -> declared payout 0.128 for regression input; consensus 3Y g_eps 32.41%, g_rev 8.34%; beta 0.94; closing-equity ROE 20.12%.

2. Peer diagnostics — not source-qualified fair value

27 initial candidates incl. target; final numeric 10 peers on the FIRST Europe step (no relaxation): 9 Tier1/2, 1 Tier3, 10 Europe-listed. Ordered expansions Europe -> World -> 0.05-20x size -> Tier3 cap 4 were defined but not needed. Peers: NDX1, WRT1V, IMI, G1A, ALFA, ENR, NKT, ANDR, LR, ROR.

Europe membership evidence = dated IEUR MSCI Europe IMI holdings proxy (Oct 29 2026); URTH World standard proxy required only for non-European World expansion (ETN confirmed member, not needed; GEV event-excluded). This diverges deliberately from the ENR.DE run, which excluded IMI-only names — recorded in evidence_review.md. Hard exclusions: SIE (Altair), PRY (Encore Wire), ABBN (Robotics/Gamesa), GEV (spin), SMIN (disposals), NEX (Lynxeo), SKF.B (separation), ATCO.A and EPI.A (class-cap reconciliation >2%).

Eight score weights: growth30%, beta15%, leverage10%, ROE10%, EBITDAmargin10%, payout7.5%, capex/sales7.5%, log EURcap10%. Pool-only 5/95 clipping/sampleSD; positive extremes retained. Full pool/selection/parameter/source schedules retained.

Equipment-primary EV/EBIT is the declared primary, qualified (pre-associate EV only): raw median 18.959980x on 8 valid observations; implied DKK 162.161758; peer-IQR dispersion 135.860129-182.405885; vs quote -14.3135%. IQR is NOT a confidence interval.

Cross-checks: PE raw median 26.976012x / PEG-scaled 42.504420x -> DKK 252.631715 (33.49%); EV/Sales -> DKK 195.029468 (3.05%); PBV median 5.225240x -> DKK 165.712485 (-12.44%). EV multiples n=8 (IMI, NKT invalid denominators). relativePE and TobinQ unavailable, not invented.

3. Published-regression diagnostics

Denmark resolves EUROPE exact; January 2026 equations as of 2026-01-01 (~304 days old). No market estimation, sector-specific fit, SEy, p-values, adjustedR2, A/B/C, D1-D10 or residual classification. Classification: Not classified (no SEy published). Model choice by highest published R2 is a weak heuristic only.

PE: prediction 29.700338923x; published R2 0.201; implied DKK 176.528644 (-6.72%). Equation: $\text{PE} = \underset{(8.29)}{9.72} + \underset{(4.85)}{2.99} \, \text{Beta} + \underset{(11.95)}{49.82} \, g_{\text{EPS}} + \underset{(9.22)}{7.98} \, \text{Payout}$.

PBV: prediction 4.253408409x; published R2 0.423; implied DKK 125.656639 (-33.60%). Equation: $\text{PBV} = \underset{(3.70)}{0.73} + \underset{(5.87)}{3.92} \, g_{\text{EPS}} + \underset{(1.38)}{0.13} \, \text{Beta} + \underset{(24.81)}{10.75} \, \text{ROE} - \underset{(2.43)}{0.25} \, \text{Payout Ratio}$.

EV/EBITDA: prediction 21.688800198x; published R2 0.262; implied DKK 256.317475 (35.44%). Equation: $\text{EV/EBITDA} = \underset{(28.40)}{18.15} + \underset{(13.96)}{35.25} \, g - \underset{(10.65)}{0.11} \, \text{DFR} - \underset{(5.19)}{0.12} \, \text{Tax Rate} + \underset{(5.06)}{2.29} \, \text{ROIC}$.

Chosen published PBV (highest R2 0.423) implied DKK 125.656639; vs quote -33.6028%. EUROPE PBV/PE carry no DFR/tax terms (unit policies identical); EV/EBITDA percent-point alternative preserved in regression_results.json — decimal policy approved.

Registered dataset regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5. GLOBAL/EM anomaly warnings not used (EUROPE exact). All exact coefficients/t-stats and input IDs in live workbook; post-LibreOffice recalculation all predictions/prices/scores agree with the library within 1e-9. Published EV definition undocumented; no associate removal imposed on the regression EV bridge.

4. Benchmark, sensitivity and limits

Closest published EUROPE industry ratios (Machinery 210 firms, Green & Renewable Energy 60, Electrical Equipment 146; see industry_benchmarks.json). These are NOT verified medians; aggregate-versus-median comparison remains a QA failure. Peer EV/EBIT median 18.96 sits inside the published range, not grounds to overwrite data.

Sensitivities: raw/scaled and peer quartiles, leave-one-out PE/growth set, all-observation EBIT margins 4/6/8/10%, target-only issuer-reported-EBIT-1015 diagnostic (special items 4.9% EBIT, below trigger — diagnostic only, not uniform normalization), both unit policies. No substantiated uniform normalization constructed.

Unresolved QA: full two-way ownership/event/history qualification for all candidates, authentic matching industry medians, comparable EV claim/lease/associate consistency, substantiated uniform normalization. Three seeded arithmetic EV checks PASS; human Spot_check PENDING (not performed/waived). Ten numeric names do not satisfy ten qualified peers until these gates are cleared. No final fair-value recommendation is issued.

5. Source and reproducibility pointers

Uniform raw financial/statistics/history: stockanalysis.com (per-ticker URLs in relative/source_log.csv); issuer figures cross-checked against the Vestas FY2025 annual report (links in relative_inputs.md / evidence_review.md). Standard proxies dated 2026-10-29: iShares MSCI World (URTH) and MSCI Europe IMI (IEUR) holdings CSVs. Library IDs/SHA/vintage/mappings: relative/evidence_review.md, regression_results.json, dataset_checks.json, candidate_gates.csv. All numbers derive from the attached run artifacts; no DCF used.

Reproduce from repository root: PYTHONPATH=src python3 outputs/VWS.CO_2026-10-30/relative/build.py; LibreOffice headless recalculate both workbooks in a separate directory, compare with formula_checks.json. finalize_stage3.py is a one-time checkpoint helper, not safe to rerun on finished state. qa_and_report.py intentionally refuses a second full QA run. Cached parsed data and source locators committed; market cache never rebuilt.

Academic analysis only. Not investment advice; source limitations and model assumptions can materially change results.
