# PRY.MI relative valuation summary (published route + comparables)

## 1. Scope and route
Relative-only, stage 3. Stages 1, 2, 4 skipped_by_deviation (standing_approvals relative_only). Published Damodaran regression route, EUROPE equations (dataset regressions_multi_2026-01, as_of 2026-01-01); comparables per comparables_procedure.

## 2. Inputs
Price EUR 110.40; shares 292.25m; market cap EUR 32,264m; EPS 4.3456; book value/share 22.1523; source StockAnalysis, accessed 2026-11-01 (see relative_inputs.md).

## 3. Published regression predictions (decimal units, as_published_note)
| Multiple | Predicted | Actual | Published R2 | Value/share |
|---|---|---|---|---|
| P/E | 22.88x | 25.41x | 0.201 | EUR 99.43 |
| P/BV (chosen) | 3.87x | 4.98x | 0.423 | EUR 85.78 |
| EV/EBITDA | 24.74x | 18.03x | 0.262 | EUR 155.87 |

Substituted input: g_eps and g_rev set to fundamental growth 18.01% (ROE x retention; approval published_route_allow_fundamental_growth = yes), labelled substituted_input in valuation_multiples.csv.

## 4. Comparables
See comparables_report.md. Primary P/E median growth-adjusted EUR 134.61; P/BV median ROE-adjusted EUR 129.76; EV/EBITDA EUR 85.13.

## 5. Model choice and result
Published model chosen by highest published R2 among PE, PBV, EV/EBITDA: P/BV, value EUR 85.78 (-22.3% vs price). Alternatives: P/E EUR 99.43, EV/EBITDA EUR 155.87.

## 6. Limitations
- Relative only: no DCF, no recommendation (approved deviation).
- Published R2 values are low (0.20 to 0.42); the regression is a cross-section, not a PRY-specific fit.
- Peer and tier choices are agent judgement; index and ISIN checks not done.
- Annual-report cross-check of PRY inputs not performed; figures are web-sourced.
- Workbook formulas are live but not recalculated (LibreOffice not installed); see regression_valuation.xlsx.
- No Spot_check by a human reviewer yet (human_review pending).

Academic analysis for coursework only; not investment advice. Figures are from public web sources accessed 2026-11-01 and are not verified against annual reports.
