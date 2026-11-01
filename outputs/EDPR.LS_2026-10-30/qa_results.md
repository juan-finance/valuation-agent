# QA checklist — block C (stage 3, relative_only deviation run) — EDPR.LS 2026-10-30

Run once on 2026-11-01. PASS / FAIL / n/a noted per item.

## Shared data and independence
- PASS Scope: single target outputs/EDPR.LS_2026-10-30/relative/; candidates from own research, no group workbook; web_minimum route; minimum-universe pool (34 candidates); one price/FX date 2026-10-30; FY2025 bases recorded per row.
- PASS Target/peers/regression universe distinct (published-damodaran route → no batch regression sample at all).
- PASS Raw financials vs class market cap within 2% (market_cap_check in candidate_raw.csv; all selected peers within tolerance). EDPR quote EUR, no ADR/classes issues; peers' quote FX → EUR via ECB snapshot (SEK/DKK/GBP conversions in fetch code).
- PASS Field-level sources, membership vintage (universe.csv/URTH), industry mapping, transformations logged (fetch_manifest.json, candidate_gates.csv, source_log.csv).
- PASS-wn >50% benchmark gap: no Damodaran Europe utility EV/EBITDA benchmark registered in the data library → check disclosed as unavailable in comparables_report; equation prediction (21.1x) used as only cross-reference, gap documented.
- PASS Human Spot_check recorded as PENDING (never claimed performed) in reports and workbook.
- PASS No DCF-proximity weighting / 30% cap — relative_only run, no DCF exists.

## Comparable method
- PASS 10 distinct qualified peers selected (ORSTED RWE EOAN SSE ERG SLR GRE ANE ENGI ENEL); counts reconcile with CSVs.
- PASS Hard filters applied: developed markets only, no financial/holding entities, ≥€1bn (EKT/PNE3 rejected), size band €1.3–132.5bn, ownership gate (EDP parent excluded), history/price-date gate (AY/BLX/INE), source-availability gate (NEOEN/OX2/IREN/HERA).
- PASS 10 Tier 1–2, 10 Europe-listed; Tier 3 = 0.
- PASS 34-candidate pool, expansions (research + tier seeds), rejected/ranked list, WEIGHTS parameters and gate reasons in candidate_gates.csv / peer_selection.json.
- PASS 8 weights sum to 1 (comparables.WEIGHTS); pool-only 5/95 clipping, standardization, dimension renormalization in select_peers (library).
- PASS-wn Consensus growth unavailable on uniform web route → whole pool on fundamental ROE×retention with method label (documented).
- PASS Full multiple set computed; unavailable marked (relative_pe, tobins_q n/a); positive extremes retained (GRE ev_cf 76.6 kept).
- PASS Used multiples ≥6 valid: pe 10, ev_ebit 10, ev_ebitda 10, ev_cf 9, pbv 10, ev_assets 10, ps 10, ev_sales 10; peg 5 <6 excluded from valuation set. p25/median/p75 reported; ev_cf skew flagged.
- PASS Raw and adjusted shown (pbv/ps/ev_sales adjusted columns); positive-driver safeguards applied.
- PASS Primary = EV/EBITDA for bucket-B developer/operator; CFO-based EV/CF flagged as secondary.
- PASS EV→equity inverse matches numerator: associates=0 on both sides (peer EV before associates; inverse adds none). Verified numerically after fix.
- PASS Three reproducibly random EV checks (seed 7): SLR 1920+1527+5.16−73.33=3378.83 ✓; EOAN 49420+38498+0−3047=91444? → EV field 91444 includes NCI 573? 49420+38498−3047=84871; +NCI 6573=91444 ✓ (NCI row in JSON); GRE 1800+1406−305.37+NCI −0.63≈2900.28 ✓.
- PASS Sensitivities: EBITDA normalization scenarios in sensitivities.csv; quartiles labelled as IQR not CI.
- PASS comparables.csv, multiples_summary.csv, comparables_report.md, comparables_audit.xlsx exist.

## Regression method (own-estimation items)
- n/a route `published_damodaran`: no master/estimation file, OLS, LINEST, typicality, D1–D10, robustness or Spot_check rows apply — recorded as `n/a_published_route` in valuation_multiples.csv and summary.

## Published-regression route
- PASS `datasets.equation_for('Portugal', dep, '2026-10-30')` → EUROPE, regressions_multi_2026-01, match level and sha256 a894ea86 recorded in regression_results.json / source_log.csv; vintage Jan-2026 ~10 months old, flagged.
- PASS Integrity check run per model; findings stored (`integrity` lists); GLOBAL anomalies retained from stage 0, EUROPE equations not flagged.
- PASS Inputs per file definitions: analyst-consensus g_eps 20.42% / g_rev 8.51% (sourced), observed beta 0.72, payout 0.61 ≥0. No substitutions (substituted_input = none).
- PASS Unit policy: decimal (user-approved `damodaran_dfr_tax_units: decimal`); both policies computed for EV/EBITDA (as_published 21.09 vs percent-points 12.37, recorded in unit_alternative); units_unverified = no.
- PASS No SEy output: classification/adj-R²/p-values/A–C/D1–D10 all `n/a_published_route`; deviation and published R² shown.
- PASS Workbook predictions verified vs published_regressions.predict (<1e-9); no PS equation; PEG/EV/IC/EV/Sales not used.
- PASS Section-7 limitations stated in valuation_summary.md.

## Data library
- PASS Resolver used (equation_for/resolve); EUROPE exact-region match for Portugal; dataset id + sha256 logged; vintage pre-dates valuation date.
- n/a industry mapping for this run (no industry_row datasets consumed; peer GICS via web mapping labelled).
- PASS No low-confidence region mapping used (Portugal → EUROPE direct).

## Result: NO FAILURES. Warned items (PASS-wn): no peer-benchmark dataset registered (disclosed); fundamental-growth pool rule (documented). No fixes required.
