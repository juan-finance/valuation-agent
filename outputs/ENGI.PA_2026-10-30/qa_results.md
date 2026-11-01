# QA checklist — block C (stage 3, relative_only deviation run) — ENGI.PA 2026-10-30

Run once on 2026-11-01. PASS / FAIL / n/a noted per item.

## Shared data and independence
- PASS Scope: single target outputs/ENGI.PA_2026-10-30/relative/; candidates from own research, no group workbook; web_minimum route; pool of 34 candidates; one price/FX date 2026-10-30; FY2025 bases recorded per row.
- PASS Target/peers/regression universe distinct (published-damodaran route → no batch regression sample at all); internal buckets not used as unverified GICS.
- PASS Raw financials vs class market cap within 2% (market_cap_check in candidate_raw.csv; all selected peers within tolerance). ENGI quote EUR single class; SSE/NG/CNA/ORSTED quotes GBP/DKK → EUR via ECB snapshot; non-EUR report currencies handled.
- PASS Field-level sources, membership vintage (universe.csv/URTH), transformations logged (fetch_manifest.json, candidate_gates.csv, source_log.csv). No per-row source switching (CEZ re-fetched, 404 again, documented).
- PASS-wn >50% benchmark gap: no Damodaran Europe utility EV/EBITDA benchmark registered → check disclosed as unavailable; EUROPE equation prediction (20.2x vs peer median 12.2x) documented as cross-reference, not resolved.
- PASS Human Spot_check recorded as PENDING (never claimed performed) in reports and workbook.
- PASS No DCF-proximity weighting / 30% cap — relative_only run, no DCF exists.

## Comparable method
- PASS 10 distinct qualified peers (ENEL, EOAN, EDP, FORTUM, VER, NG, SSE, CNA, SRG, ORSTED); counts reconcile with CSVs.
- PASS Hard filters: developed markets only, no financial/holding entities, ≥€1bn, size band €5.70–569.8bn, ownership gate (no ENGIE subsidiary/cross-holding in pool; Endesa eligible — Enel subsidiary, not target's), freshness gate (AY/BLX/INE), source gate (CEZ 404).
- PASS 10 Tier 1–2 (8 T1 + 2 T2), 10 Europe-listed; Tier 3 = 0; no relaxation.
- PASS 34-candidate pool (33 + CEZ evidence row), rejected/ranked list, weights and gate reasons in candidate_gates.csv / peer_selection.json.
- PASS 8 weights sum to 1 (comparables.WEIGHTS); pool-only 5/95 clipping, standardization, renormalization in library select_peers.
- PASS-wn Consensus growth unavailable on uniform web route → whole pool on fundamental ROE×retention with method label (documented); ENGI paid-cash payout 1.23 → growth 0, growth-scaled PE adjustment and PEG unavailable (positive-driver safeguard).
- PASS Full multiple set computed; unavailable marked (relative_pe, tobins_q n/a; ev_cf NM for target — negative vendor FY2025 CFO −1,476m vs issuer CFFO 13,600m, flagged); positive extremes retained.
- PASS Used multiples ≥6 valid: pe 9, ev_ebit 10, ev_ebitda 10, ev_cf 10 (target NM), pbv 10, ev_assets 10, ps 10, ev_sales 10; peg 7 valid but NM for target (growth 0); p25/median/p75 reported; PEG mean/median skew 48.4% flagged (>25% rule; multiple not valued).
- PASS Raw and adjusted shown (pbv/ps/ev_sales adjusted columns; pe adjustment unavailable — target driver zero, safeguard worked).
- PASS Primary = EV/EBITDA for bucket-A integrated utility; EV/CF flagged NM for target.
- PASS EV→equity inverse matches numerator: associates=0 on both sides (peer EV before associates; inverse adds none). Verified numerically.
- PASS Three reproducibly random EV checks (seed 20261030): CNA 7,259.35 ✓; FORTUM 22,713 ✓; ORSTED 85,992.72 ✓.
- PASS Sensitivities: issuer consolidated/ex-nuclear EBITDA and issuer NIGs/NRIgs scenarios in sensitivities.csv; quartiles labelled IQR not CI.
- PASS comparables.csv, multiples_summary.csv, comparables_report.md, comparables_audit.xlsx exist.

## Regression method (own-estimation items)
- n/a route `published_damodaran`: no master/estimation file, OLS, LINEST, typicality, D1–D10, robustness or Spot_check rows apply — recorded as `n/a_published_route` in valuation_multiples.csv and summary.

## Published-regression route
- PASS `datasets.equation_for('France', dep, '2026-10-30')` → EUROPE, regressions_multi_2026-01, match level and sha256 a894ea86 recorded in regression_results.json / source_log.csv; vintage Jan-2026 ~10 months old, flagged.
- PASS Integrity check run per model; findings stored (`integrity` lists); GLOBAL anomalies retained from stage 0, EUROPE equations not flagged.
- PASS Inputs per file definitions: analyst-consensus g_eps 4.73% / g_rev 5.60% (sourced), observed beta 0.57, payout 0.89 declared basis ≥0 (paid-cash 1.23 flagged), dfr/tax decimals. No substitutions (substituted_input = none).
- PASS Unit policy: decimal (user-approved `damodaran_dfr_tax_units: decimal`); both policies computed for EV/EBITDA (as_published 20.23 vs percent-points 11.92, recorded in unit_alternative; pp prediction near utility peer median 12.2x noted); units_unverified = no.
- PASS No SEy output: classification/adj-R²/p-values/A–C/D1–D10 all `n/a_published_route`; deviation and published R² shown.
- PASS Workbook predictions verified vs published_regressions.predict (<1e-9; formula text evaluated independently — LibreOffice recalc not installed on this box, disclosed); no PS equation; PEG/EV/IC/EV/Sales not used.
- PASS Section-7 limitations stated in valuation_summary.md.

## Data library
- PASS Resolver used (equation_for/resolve); EUROPE exact-region match for France; dataset id + sha256 logged; vintage pre-dates valuation date.
- n/a industry mapping for this run (no industry_row datasets consumed; peer GICS via web mapping labelled).
- PASS No low-confidence region mapping used (France → EUROPE direct).

## Result: NO FAILURES. Warned items (PASS-wn): no peer-benchmark dataset registered (disclosed); fundamental-growth pool rule + ENGI zero-growth/PEG NM (documented); vendor CFO negative vs issuer CFFO (EV/CF NM, documented); workbook formula check done outside Excel (LibreOffice absent — disclosed). One fix applied during QA: the EV spot-check recomputation used the same market-cap→report-currency path as prepare_pool after an initial NI-based reconstruction artefact on CNA (negative NI); all three checks now pass. No other fixes required.
