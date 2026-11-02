# Relative valuation by regression - Europe, ORSTED.CO, 2026-10-30

## Scope
ORSTED.CO only; no market sample/own estimation/DATA_BASE_MSCI under the published route.

## Headline
Draft PBV selected by highest eligible published R2 (0.423), a weaker heuristic than adjusted-R2/industry fit.

## Data
FY2025 uniform vendor inputs cross-checked with the Ørsted annual report. Denmark listing resolves EUROPE exact. Sourced analyst consensus inputs used (g_eps 51.15%, g_rev 8.84%); no substitution needed. Common payout 0.0 (no FY2025 common dividend; NCI/hybrid distributions excluded). ROE on closing parent-common equity 119,718 (hybrid stripped).

## Fitted models
| model     |   predicted |   published_r2 |   value_per_share |    actual |   deviation |
|:----------|------------:|---------------:|------------------:|----------:|------------:|
| PE        |    36.9371  |          0.201 |           6.46632 | 100.898   |    1.7316   |
| PBV       |     2.96555 |          0.423 |          35.9888  |   1.23869 |   -0.582308 |
| EV/EBITDA |    21.2543  |          0.262 |          38.0233  |  10.9775  |   -0.483518 |

## Diagnostics
Integrity findings retained in regression_results.json and dataset_checks.json. GLOBAL PEG/PBV and EM EV/EBITDA source anomalies do not affect these EUROPE equations. No n, SEy, adjusted R2, p-values, A/B/C, typicality or D1-D10: n/a_published_route. Classification: Not classified (no SEy published). EV/EBITDA decimal vs percentage-point DFR/tax alternative recorded (21.25 vs 11.49 predicted; decimal approved).

## Limitations
Market-wide, low-R2 equations are not sector fair-value proof. January 2026 vintage ~9 months old at valuation date. Published EV definition undocumented; hybrid removed once in the EV->common bridge. Beta benchmark/frequency unspecified. Rights-issue-transitional leverage and impairment-driven 47% tax flagged.
