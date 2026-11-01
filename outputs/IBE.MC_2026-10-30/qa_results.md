# QA checklist — block C (stage 3, relative_only deviation run) — IBE.MC 2026-10-30

Run once on 2026-11-01. PASS / FAIL / n/a noted per item.

## Shared data and independence
- PASS Scope: single target outputs/IBE.MC_2026-10-30/relative/; candidates from own research, no group workbook; web_minimum route; pool of 33 + subsidiary evidence row; one price/FX date 2026-10-30; FY2025 bases recorded per row.
- PASS Target/peers/regression universe distinct (published-damodaran route → no batch regression sample at all); internal buckets not used as unverified GICS.
- PASS Raw financials vs class market cap within 2% (market_cap_check in candidate_raw.csv; all selected peers within tolerance). IBE quote EUR single class; SSE/NG/DRX/CNA quotes GBP and ORSTED DKK → EUR via ECB snapshot; report currencies taken from verified fetch units (SSE/NG/DRX/CNA GBP, ORSTED DKK, SCATC NOK, World names USD/CAD).
- PASS Field-level sources, membership vintage (universe.csv/URTH), transformations logged (fetch_manifest.json, candidate_gates.csv, source_log.csv). No per-row source switching (CEZ dropped on 404).
- PASS-wn >50% benchmark gap: no Damodaran Europe utility EV/EBITDA benchmark registered → check disclosed as unavailable; EUROPE equation prediction (19.7x vs peer median 12.6x) documented as cross-reference, not resolved.
- PASS Human Spot_check recorded as PENDING (never claimed performed) in reports and workbook.
- PASS No DCF-proximity weighting / 30% cap — relative_only run, no DCF exists.

## Comparable method
- PASS 10 distinct qualified peers (SSE, RWE, NTGY, NG, EDP, EOAN, TRN, SRG, VER, ENGI); counts reconcile with CSVs.
- PASS Hard filters: developed markets only, no financial/holding entities, ≥€1bn, size band €14.79–1,479.4bn, ownership gate (ELE ~70% subsidiary of candidate ENEL excluded), freshness gate (AY/BLX/INE), source gate (CEZ 404).
- PASS 10 Tier 1–2 (8 T1 + 2 T2), 10 Europe-listed; Tier 3 = 0; no relaxation.
- PASS 33-candidate pool, rejected/ranked list, weights and gate reasons in candidate_gates.csv / peer_selection.json.
- PASS 8 weights sum to 1 (comparables.WEIGHTS); pool-only 5/95 clipping, standardization, renormalization in library select_peers.
- PASS-wn Consensus growth unavailable on uniform web route → whole pool on fundamental ROE×retention with method label (documented); growth-scaled PE/PEG distorted by near-zero peer growth → flagged, raw multiples retained.
- PASS Full multiple set computed; unavailable marked (relative_pe, tobins_q n/a); positive extremes retained.
- PASS Used multiples ≥6 valid: pe 10, ev_ebit 10, ev_ebitda 10, ev_cf 9, pbv 10, ev_assets 10, ps 10, ev_sales 10; peg 9 valid; p25/median/p75 reported.
- PASS Raw and adjusted shown (pbv/ps/ev_sales/pe adjusted columns; raw retained alongside).
- PASS Primary = EV/EBITDA for bucket-A integrated utility; EV/CF CFO-based flagged secondary.
- PASS EV→equity inverse matches numerator: associates=0 on both sides (peer EV before associates; inverse adds none). Verified numerically.
- PASS Three reproducibly random EV checks (seed 20261030) in comparables_audit.xlsx EV_check.
- PASS Sensitivities: issuer adjusted/reported EBITDA and issuer reported/adjusted NI scenarios in sensitivities.csv; quartiles labelled IQR not CI.
- PASS comparables.csv, multiples_summary.csv, comparables_report.md, comparables_audit.xlsx exist.

## Regression method (own-estimation items)
- n/a route `published_damodaran`: no master/estimation file, OLS, LINEST, typicality, D1–D10, robustness or Spot_check rows apply — recorded as `n/a_published_route` in valuation_multiples.csv and summary.

## Published-regression route
- PASS `datasets.equation_for('Spain', dep, '2026-10-30')` → EUROPE, regressions_multi_2026-01, match level and sha256 a894ea86 recorded in regression_results.json / source_log.csv; vintage Jan-2026 ~10 months old, flagged.
- PASS Integrity check run per model; findings stored (`integrity` lists); GLOBAL anomalies retained from stage 0, EUROPE equations not flagged.
- PASS Inputs per file definitions: analyst-consensus g_eps 9.15% / g_rev 4.05% (sourced), observed beta 0.45, payout 0.75 ≥0 declared basis (scrip CF-paid 0.21 flagged not used), dfr/tax decimals. No substitutions (substituted_input = none).
- PASS Unit policy: decimal (user-approved `damodaran_dfr_tax_units: decimal`); both policies computed for EV/EBITDA (recorded in unit_alternative); units_unverified = no.
- PASS No SEy output: classification/adj-R²/p-values/A–C/D1–D10 all `n/a_published_route`; deviation and published R² shown.
- PASS Workbook predictions verified vs published_regressions.predict (<1e-9; formula text evaluated independently — LibreOffice recalc not installed on this box, disclosed); no PS equation; PEG/EV/IC/EV/Sales not used.
- PASS Section-7 limitations stated in valuation_summary.md.

## Data library
- PASS Resolver used (equation_for/resolve); EUROPE exact-region match for Spain; dataset id + sha256 logged; vintage pre-dates valuation date.
- n/a industry mapping for this run (no industry_row datasets consumed; peer GICS via web mapping labelled).
- PASS No low-confidence region mapping used (Spain → EUROPE direct).

## Result: NO FAILURES. Warned items (PASS-wn): no peer-benchmark dataset registered (disclosed); fundamental-growth pool rule + distorted growth-scaled PE/PEG (documented, raw retained); workbook formula check done outside Excel (LibreOffice absent — disclosed). No fixes required.
