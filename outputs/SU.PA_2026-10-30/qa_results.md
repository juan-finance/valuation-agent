# QA block C — SU.PA relative valuation (run once, 2026-11-02)

Result: **PROVISIONAL — no FAILs.** Human Spot_check PENDING (recorded, not claimed); ISIN issuer-page verification PENDING; ownership/event audit outstanding.

## Shared data and independence
- PASS: single target in outputs/SU.PA_2026-10-30/relative/; candidate pool reused from prior same-date runs (SU.PA dirs excluded), consistent with "never collect data twice"; route `web_minimum`/`published_damodaran`; one valuation/FX date 2026-10-30; FY2025 basis labelled throughout.
- PASS: target vs peer set vs regression universe kept distinct; internal bucket D not used as GICS.
- PASS: class-level market cap check within 2% for all scored rows (price × shares vs vendor class mcap); EUR reporting and quote currency, no ADR/share-class mixing (single class, ISIN FR0000121972).
- PASS: field-level sources in source_log.csv + candidate_raw.csv; uniform vendor route, no per-row switching.
- PASS: >50% benchmark check — peer median EV/EBITDA 18.02x vs Damodaran Europe "Electrical Equipment" industry aggregates 18.94x (pos-EBITDA) / 23.42x (all firms) → -4.8% / -23.0%, below trigger.
- PENDING: human Spot_check — recorded in comparables_audit.xlsx, never claimed.
- PASS: no DCF-proximity/size weighting or 30% cap (stage 2 skipped by deviation).

## Comparable method
- PASS: 10 distinct peers selected (SAND, LR, ATCO.A, EPI.A, METSO, HLMA, ALFA, ENR, WRT1V, PRY); 8 Tier1-2 + 2 Tier-3 at cap (only 9 Tier1-2 eligible under size band; documented shortfall permitted); 10 Europe-listed (≥5).
- PASS: hard filters applied — EUR1bn min, size band €13.4bn–1,337bn (0.1–10× target mcap €133.7bn), event-exclusion list (SIE, ABBN, GEV, SMIN, NEX, SKF.B), oil/gas/utility/metals/offshore exclusions, ≤2 missing scoring dims.
- PASS: rejected/ranked list in pool_rejected.csv/peer_selection_raw.csv; business-description review done (2 Tier-3 mining-equipment peers documented as bucket-adjacent fallback).
- PASS: 8 score weights = 1 (library); pool-only 5/95% winsorization; target standardized unclipped; missing-dimension renormalization via library.
- PASS: consensus coverage — uniform route uses fundamental growth (web) for all peers; target additionally has analyst consensus (g_eps 0.2040, g_rev 0.1156) used only for published-regression inputs, documented.
- PASS: full required multiple set computed; relative_pe/tobins_q marked unavailable (no index PE / replacement-cost evidence); positive extremes retained (SAND PE 27.3, WRT1V PE 24.2 kept).
- PASS: every used multiple has ≥6 valid obs (PE/PBV/EV/EBITDA/EV/EBIT/EV/Sales n=10, EV/cf n=9 — HLMA cashflow missing); >25% mean–median skew flagged on pe, pbv, ev_sales in multiples_summary.csv.
- PASS: raw and adjusted values shown; scaled ratios via scaled_multiple with min_valid=6 (pe/pbv/ps/ev_sales).
- PASS: one primary multiple PE per bucket-D/sector mapping; EV→equity inverse matches numerator (no associates among peers: EV_before_associates = EV_after_associates); per-share value €173.59 (growth-adj PE primary) reconciles.
- PASS: EV spot-checks reproducible — SAND, LR, ATCO.A, METSO, ALFA, PRY, ENR, EPI.A, WRT1V all recompute exactly (delta = 0) from price×shares + debt + NCI − cash (HLMA EV not computed — no debt/NCI fields; EV multiples n=9).
- PASS: peer-set/multiple/NI-basis/payout-basis sensitivities in sensitivities.csv + comparables_report.md; IQR not called a confidence interval.
- PASS: comparables.csv, multiples_summary.csv, comparables_report.md exist; audit schedules in comparables_audit.xlsx.

## Regression method (published_damodaran)
- PASS: equations via `datasets.equation_for('France', dep, '2026-10-30')` → EUROPE, regressions_multi_2026-01, as-of 2026-01-01 ≤ valuation date; ~10-month vintage stated under Limitations; dataset id + sha256 in source_log_stage3.csv.
- PASS: stage-0 integrity findings reused; EUROPE not among anomaly-flagged regions.
- PASS: inputs follow file definitions; analyst-consensus growth used (labelled, no substitution); payout = declared-DPS basis 0.567 ≥0.
- PASS: unit policy decimal (user-approved `damodaran_dfr_tax_units: decimal`); plausibility note vs peer medians recorded (market-wide PBV eq. predicts 3.39x vs actual 5.53x → deviation +62.9%, recorded, not resolved).
- PASS: no SEy-based output — diagnostics n/a_published_route; published R² shown (PE 0.201, PBV 0.423, EV/EBITDA 0.262); chosen model PBV (highest published R²).
- PASS (partial): regression_valuation.xlsx live formulas verified equal to `published_regressions.predict` within 1e-9 by construction check; LibreOffice recalculation NOT performed (not installed — stated).
- PASS: valuation_summary.md states section-7 limitations (market-wide scope, low R², vintage, no residual dispersion, payout-basis note).

## Data library
- PASS: datasets resolved via `datasets.resolve`/`equation_for` (France → EUROPE); vintages ≤ valuation date; sha256 logged.
- PASS: industry benchmark "Electrical Equipment" matched by exact industry name.

## Fixes applied during this QA pass
- None — no failures found.
