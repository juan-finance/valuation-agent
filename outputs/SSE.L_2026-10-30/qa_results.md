# QA block C — SSE.L relative valuation (run once, 2026-11-02)

Result: **PROVISIONAL — no FAILs.** Human Spot_check PENDING (recorded, not claimed); ISIN issuer-page verification PENDING; ownership/event audit outstanding.

## Shared data and independence
- PASS: single target in outputs/SSE.L_2026-10-30/relative/; own-research candidates (no group workbook); route `web_minimum`/`published_damodaran` reused; one valuation/FX date 2026-10-30; FY2025 (Mar-2025) basis labelled, TTM/forward not mixed.
- PASS: target list vs peer set vs regression universe kept distinct; internal bucket A not used as GICS.
- PASS: class-level market cap check within 2% for all scored rows (asserted ≤5%, actual ≤0.5%); GBp→GBP conversion explicit; no ADRs/share-class mixing (single class).
- PASS: field-level sources in source_log.csv + candidate_gates.csv; no per-row source switching (uniform vendor).
- PASS (with caveat): >50% benchmark check — peer median EV/EBITDA 11.78x vs Damodaran Europe Utility (General) ~11.06 aggregate → +6.5%, below trigger; aggregate-vs-median caveat recorded.
- PENDING: human Spot_check — recorded in comparables_audit.xlsx, never claimed.
- PASS: no DCF-proximity/size weighting or 30% cap (stage 2 skipped by deviation anyway).

## Comparable method
- PASS: 10 distinct peers selected (RWE, EDP, IBE, ANE, NG, A2A, NTGY, EOAN, ORSTED, TRN); 7 Tier-1 + 3 Tier-2 (≥8 T1-2 under default cap), 10 Europe-listed (≥5), Tier-3 = 0 (≤2).
- PASS: hard filters applied — ELE subsidiary exclusion, CEZ unavailable/EM, EUR1bn min, size band €3.80–380bn, ownership/restructuring flags, trading history, ≤2 missing scoring dims (asserted).
- PASS: 33-candidate pool + evidence row; rejected/ranked list in candidate_gates.csv/peer_selection.json; business-description review done, no replacements needed.
- PASS: 8 score weights = 1 (library); pool-only 5/95% winsorization; target standardized unclipped; zero-variance/missing-dimension renormalization via library.
- PASS: consensus coverage rule — uniform web route uses fundamental growth for all (pool rule); no mixed provenance.
- PASS: full required multiple set computed; relative_pe and tobins_q marked unavailable (no index PE / replacement-cost evidence); positive extremes retained (Orsted PE 100.9 kept).
- PASS: every used raw and scaled multiple has ≥6 valid obs (all n=10); median/mean/p25/p75 shown; >25% mean–median skew flagged on pe, peg, ev_ebit.
- PASS: raw and adjusted values shown; PEG uses pp growth; scaled ratios via scaled_multiple with min_valid=6.
- PASS: one primary multiple EV/EBITDA per bucket-A mapping; EV→equity inverse matches numerator (associates=0 both sides); GBP per-share value and upside reconcile.
- PASS: three reproducibly random EV recomputes match (EV_check sheet); ISINs registry-mapped (issuer-page verification pending).
- PASS: peer-set/quartile/multiple/EBITDA-basis/NI-basis sensitivities in multiples_summary.csv + sensitivities.csv; IQR not called a confidence interval.
- PASS: comparables.csv, multiples_summary.csv, comparables_report.md exist; audit schedules in comparables_audit.xlsx.

## Regression method (published_damodaran)
- PASS: equation via `datasets.equation_for('United Kingdom', dep, '2026-10-30')` → EUROPE, regressions_multi_2026-01, as-of 2026-01-01 ≤ valuation date; ~10-month age stated under Limitations; dataset id + sha256 logged.
- PASS: integrity check findings reused from stage 0 (GLOBAL anomalies; EUROPE unaffected); no anomaly-flagged equation used.
- PASS: inputs follow file definitions; consensus g_eps/g_rev sourced (no substitution needed); payout ≥0.
- PASS: unit policy decimal (user-approved); both policies in regression_results.json `unit_alternative`; plausibility note vs peer median recorded (market-wide EV/EBITDA 21.0x >> utility peer median 11.8x — recorded, not resolved).
- PASS: no SEy-based output — all diagnostics n/a_published_route; deviation + published R² shown.
- PASS (partial): workbook live formulas verified equal to `published_regressions.predict` <1e-9 by construction check; LibreOffice recalculation NOT performed (not installed — same status as prior runs, stated).
- PASS: valuation_summary.md states section-7 limitations (market-wide scope, low R², analyst-growth definition, vintage, undocumented EV definition, no residual dispersion).

## Data library
- PASS: datasets resolved via `datasets.resolve`/`equation_for` (UK → EUROPE); vintages ≤ valuation date; sha256 in source_log.csv.
- PASS: industry benchmark row "Utility (General)" matched by exact industry name.

## Fixes applied during this QA pass
- Corrected an exclusion-tuple bug in build_relative.py (excluded IBE instead of SSE; target had entered its own peer set) — pool and all outputs regenerated; peer set now 10 non-target members.
