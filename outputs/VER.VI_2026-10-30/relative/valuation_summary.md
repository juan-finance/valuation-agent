# Relative valuation by regression - Europe, VER.VI, 2026-10-30

## Scope
VER.VI only; no market sample/own estimation/DATA_BASE_MSCI under the published route.

## Headline
Draft PBV selected by highest eligible published R2 (0.423), a weaker heuristic than adjusted-R2/industry fit.

## Data
FY2025 uniform vendor inputs cross-checked with the VERBUND integrated annual report 2025. Austria listing resolves EUROPE exact. Sourced analyst consensus inputs used (g_eps -4.51%, g_rev -0.98%); no substitution needed. Payout 0.466 on FY2025 declared DPS 2.00/EPS 4.29 (cash-paid basis 0.89 flagged - special dividend). ROE on closing parent-common equity 10,341.

## Fitted models
| model     |   predicted |   published_r2 |   value_per_share |   actual |   deviation |
|:----------|------------:|---------------:|------------------:|---------:|------------:|
| PE        |    11.612   |          0.201 |           49.7676 | 16.2189  |    0.39674  |
| PBV       |     2.00275 |          0.423 |           59.6121 |  2.33536 |    0.166079 |
| EV/EBITDA |    18.0739  |          0.262 |          131.521  | 10.139   |   -0.439024 |

## Diagnostics
Integrity findings retained in regression_results.json and dataset_checks.json. GLOBAL PEG/PBV and EM EVEBITDA source anomalies do not affect these EUROPE equations. No n, SEy, adjusted R2, p-values, A/B/C, typicality or D1-D10 available: n/a_published_route. Classification: Not classified (no SEy published).

## Exact equations and t-statistics
See Coefficients_PE/PBV/EV_EBITDA workbook sheets.

## Valuation results (sorted from most undervalued to most overvalued)
| model     |   value_per_share |
|:----------|------------------:|
| EV/EBITDA |          131.521  |
| PBV       |           59.6121 |
| PE        |           49.7676 |

## Robustness
All units decimal as approved; predict_both_policies alternatives recorded in regression_results.json. Live predictions and price bridges reference Inputs; recalculation validation in formula_checks.json. Published EV definition undocumented.

## Key warnings
Market-wide, low-R2 equations are not sector fair-value proof. January 2026 vintage ~9 months old at valuation date. Published EV definition undocumented. Beta benchmark/frequency unspecified; vendor beta 0.14 atypically low. Negative consensus growth inputs (g_eps -4.51%, g_rev -0.98%) reflect normalization off the 2022-24 price spike - flagged; PE equation sensitive to sign of g. Austrian windfall levy EUR135.9m in FY2025 costs.

## Limitations
Equation R2 low (PE 0.201/PBV 0.423/EVEBITDA 0.262 published). Analyst-growth definition differs from our fundamental growth; sourced consensus used so no substitution. No residual dispersion or confidence range invented.

## Sources
source_log.csv; registered regressions_multi_2026-01 SHA regressions_multi_2026-01; issuer cross-check in relative_inputs.md.
