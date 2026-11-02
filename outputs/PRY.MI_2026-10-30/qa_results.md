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
