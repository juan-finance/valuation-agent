# Findings from checking the supplied Damodaran files (2026-10-30)

Verified by code (`python -m valuation_agent.datasets check`) and tests; items marked "open" cannot be settled from the files alone.

## Files
- Byte-identical copies of the four supplied files (sha256 in `registry.csv`). Dates: betas and capex 5 Jan 2026 (header in Spanish month format `5-ene-26`), regressions "January 2026", risk premiums 1 Jul 2026 with default spreads corrected on 9 Jul 2026 (as-of used: 2026-07-09).
- Vintages differ across files. For a valuation dated before 9 Jul 2026 the risk-premium file is look-ahead and the resolver excludes it.

## Betas (Western Europe)
- 94 industries plus two aggregates. Unlevering parameter: marginal tax 24.71%. Internal consistency verified: unlevered beta = beta/(1+(1-t) D/E) and cash-corrected = unlevered/(1-cash/firm value) within 0.03 for all 94 industries.
- Use `beta_unlevered_cash_corrected`. Relever with the COMPANY's marginal tax rate and target D/E (dcf_procedure.md section 7), not the 24.71%.

## Capex (Europe)
- Net CapEx/EBIT(1-t) is not meaningful for Steel (884%) and Transportation (Railroads) (-14,595%): use another supported ratio and say so (dcf_procedure.md section 3). Some cells are `NA`.
- Aggregates are in US dollars; ratios are currency-free.

## Country and equity risk premiums (global)
- Mature ERP 4.20%. Every rated country's default spread equals the rating lookup table (verified). Total ERP = mature ERP + CRP for every row (verified). CRP = default spread x about 1.555 for all non-US rows (the stated 1.55 is rounded); the US row uses CRP = default spread (0.22%), a source quirk.
- Column naming: this vintage has "Rating-based Default Spread", not the "Adj. Default Spread" named in `methodology/data_sources.md`. The values equal the rating table, so they are the pure rating-based spread with no CDS adjustment. Record that mapping in dcf_decisions.md (open: confirm it is the intended quantity).
- Turkey is listed under Western Europe in this file; treat the mapping to the Europe datasets as low confidence. No corporate tax rate column in this file (cross-check source for marginal tax must come elsewhere).

## Published regressions
- 36 equations (6 multiples x 6 regions). The by-region and by-multiple views agree on all 30 equations present in both; Australia/NZ/Canada appears only in the by-multiple view although the intro lists five groupings.
- Source anomalies flagged for verification before use: Global PEG has +0.48 on ln(g_EPS) (all other regions about -1.2 to -1.7) and the same t-statistic (12.83) on two different terms; its R2 (41.4%) equals the US PEG R2. Global PBV beta (-0.12, t 2.6) and Emerging Markets EV/EBITDA ROIC (-4.88, t 7.0) have the opposite sign of all other regions.
- The file's worked Disney example uses 2022 coefficients (2.10, 6.07, 0.69, 5.09, -0.33); the printed 2026 US equation gives 4.21 instead of 4.35 for the same inputs. Do not copy the example.
- Open: units of DFR and Tax rate (decimal per the text, percentage points per coefficient scale). See methodology/regression_published_route.md section 4.
- No n, no residual standard error, no p-values: only a point prediction and R2 are possible.
