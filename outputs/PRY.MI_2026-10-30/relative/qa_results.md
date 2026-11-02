# QA block C (stage 3, PRY.MI, 2026-10-30), remediated

## Status
**provisional - limitations disclosed.** No FAIL items. Human Spot_check: PENDING (not performed).

## Re-run items (this remediation)
| Item | Result | Evidence |
|---|---|---|
| (1) Fresh 20-30 candidate pool with rejection reasons | PASS (30 rows: 10 selected, 12 eligible not selected, 8 rejected with reasons) | relative/candidate_pool_20_30.csv |
| (2) Market cap reconciled with annual report within 2% | PARTIAL: internal check PASS (price 110.40 x 292.25m = EUR 32,264.4m = StockAnalysis, 0.0%); annual-report figure NOT fetched in this step | relative/remediation_results.json |
| (3) ISINs of the ten peers | PARTIAL: ISO 6166 check digit valid for all ten (from cache); exchange-register verification NOT performed; VWS has two cached ISINs (DK0061539921 used, DK0010268606 unresolved) | relative/isin_check.csv |
| (4) Three reproducible random EV checks | PASS: recomputed EV = market cap + debt + NCI - cash matches stored EV to 0.0% for the three names drawn with seed 20261030 (WRT1V, NEX, NDX1) | relative/ev_random_checks.csv |
| (5) Peer-set and quartile sensitivities | PASS-with-note: leave-one-out median moves -2.8% to +2.8%; quartile p25 -17.2%, p75 +32.7%; raw P/E -12.9%; EV/EBITDA units -17.8% (all disclosed) | relative/sensitivities.csv |
| (6) Dataset integrity check and sha256 in source_log | PASS: regressions_multi_2026-01 sha256 a894ea86...9bf5 matches registry; 0 errors; warnings on GLOBAL/EM equations (not used) and on DFR/tax units (EV/EBITDA uses both; both unit policies reported) | relative/remediation_results.json; source_log.csv |
| (7) regression_valuation.xlsx recalculation | PENDING-NOT-POSSIBLE: LibreOffice not installed and no Python formula engine available (formulas, pycel absent). Python recompute equals published_regressions.predict to 1e-9 (asserted in build_outputs.py) | relative/build_outputs.py |

## Unchanged items (not re-run)
Peer count 10 (min 8), Tier 1-2 10 (min 6), Tier 3 0 (max 2), Europe 10 (min 5); score weights sum to 1.00; min_valid 6 met for every used multiple; PE growth and PBV ROE adjustment labelled; published-route equations via datasets.equation_for with substituted_input labelled.

## Still PENDING (not claimed as passed)
- Human Spot_check (human_review pending).
- Annual-report reconciliation (item 2), exchange-register ISIN verification (item 3).
- Ownership and event source lines per peer for the qualification rule (not collected in this step).
- Workbook live-formula recalculation (item 7).

## Totals
Re-run items: PASS 3 (1, 4, 6), PASS-with-note 1 (5), PARTIAL 2 (2, 3), PENDING 1 (7). FAIL 0. Human Spot_check PENDING.

---

## History (earlier QA block C, first run; superseded)

# QA block C (stage 3, PRY.MI, 2026-10-30), run once

Status key: PASS = verified in this run; FAIL = checked and wrong; PENDING = not performed, cannot be claimed.

## Shared data and independence
- PASS: scope single target, outputs/PRY.MI_2026-10-30/relative/ ; data route published_damodaran; standard mode; one valuation date 2026-10-30.
- PASS: target list, peers and regression market kept separate; no GICS sector claims.
- PENDING: market cap vs annual-report reconciliation within 2% (annual report not checked).
- PASS: field sources logged (relative_inputs.md, source_log.csv); no per-row source switching.
- PENDING: >50% benchmark gaps investigation (not run).
- PENDING: human Spot_check (not performed; human_review pending).
- PASS: no DCF-proximity weighting or cap in the base.

## Comparable method
- PASS: 10 distinct peers, 0 shortfall (comparables.csv).
- PENDING: full hard-filter audit (ownership, restructuring, history) not verified per peer.
- PASS: Tier 1-2 = 10 (min 6), Tier 3 = 0 (max 2), Europe = 10 (min 5).
- PENDING: 20-30 initial candidate pool; pool_eligible.csv and pool_rejected.csv are an audit of the pool built from prior runs' candidate files (about 150 rows); not a fresh 20-30 list.
- PASS: score weights sum to one (0.30+0.15+0.10+0.10+0.10+0.075+0.075+0.10 = 1.00) per comparables.py WEIGHTS.
- PASS: consensus rule: fundamental growth used (no consensus collected) labelled.
- PASS: primary and raw/adjusted multiples: min_valid=6 met (n=10 for PE, PBV, PS, EV/Sales; n=7 for EV/EBIT, EV/EBITDA, EV/CF, EV/assets).
- PASS: primary PE adjusted by growth (scaled_multiple), raw and adjusted shown.
- PASS: skew flag reported in multiples_summary.csv.
- PENDING: three reproducibly random EV calculations not performed.
- PENDING: ISINs not verified (isin = 'not verified').
- PENDING: peer-set and quartile sensitivities not reported.
- PASS: comparables.csv, multiples_summary.csv, comparables_report.md exist.

## Regression method (published route only)
- PASS: equation via datasets.equation_for; dataset id, vintage 2026-01 and as-of recorded in regression_results.json.
- PENDING: dataset integrity check (datasets integrity run) not run in this session.
- PASS: inputs follow file definitions; g_eps and g_rev substituted with fundamental growth, labelled substituted_input.
- PASS: unit policy decimal (as_published_note); both policies computed for EV/EBITDA (uses dfr and tax_rate); PE and PBV use no DFR or tax.
- PASS: no SEy-based output; classification 'Not classified (no SEy published)'; published R2 shown.
- PENDING: regression_valuation.xlsx has live formulas but was not recalculated (LibreOffice not installed). Python recompute equals published predict to 1e-9 (asserted in build_outputs.py).
- PASS: no PS equation invented.
- PASS: summary states section 7 limitations.

## Data library
- PASS: dataset chosen by datasets.resolve (Italy, EUROPE).
- PENDING: source_log dataset sha256 recorded in source_log.csv: sha256 not written there (only in regression_results.json).
- PENDING: low-confidence country mappings acknowledgement not written.

## Totals
Counted by item above. See the PASS/FAIL/PENDING list; FAIL = 0 in this run; PENDING items are not claimed as passed.
