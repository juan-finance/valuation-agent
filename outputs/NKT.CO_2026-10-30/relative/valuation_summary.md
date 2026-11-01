# Relative valuation by regression - Europe, NKT.CO, 2026-10-30

## Headline
Draft PBV selected by highest eligible published R2 (0.423), a weaker heuristic rather than adjusted-R2/industry fit.

## Scope
NKT.CO only; no market sample/own estimation/DATA_BASE_MSCI under published route.

## Data
FY2025 uniform vendor inputs cross-checked with issuer annual report. Denmark listing resolves EUROPE exact. Fundamental growth uses closing parent-common ROE 0.1292 x capped retention, explicitly approved substitution for unavailable matching 5Y analyst growth; vendor 5Y beta 0.65 kept (within 0-2.5); no replacement needed.

## Fitted model
| model     |   predicted |   published_r2 |   value_per_share |   actual |   actual_predicted_gap |
|:----------|------------:|---------------:|------------------:|---------:|-----------------------:|
| PE        |    18.1656  |          0.201 |           89.7234 | 22.7268  |              0.251089  |
| PBV       |     2.67866 |          0.423 |          102.385  |  2.73592 |              0.0213753 |
| EV/EBITDA |    23.5097  |          0.262 |          319.583  |  7.27871 |             -0.690395  |

## Diagnostics
Integrity findings retained in regression_results.json. GLOBAL PEG/PBV and EM EVEBITDA source anomalies do not affect these EUROPE equations. No n, SEy, adjusted R2, p-values, A/B/C, typicality or D1-D10 available: n/a_published_route. Classification: Not classified (no SEy published).

## Valuation results (sorted from most undervalued to most overvalued)
| model     |   value_per_share |
|:----------|------------------:|
| EV/EBITDA |          319.583  |
| PBV       |          102.385  |
| PE        |           89.7234 |

## Robustness
All units decimal as approved; EVEBITDA alternative percentage-point DFR/tax prediction saved. Live predictions and price bridges reference Inputs; recalculation validation follows in formula_checks.json. Published EV definition undocumented; hybrid EUR150m removed once from the EV->common bridge.

## Key warnings
DRAFT pending human Spot_check. Primary PE per bucket-D electrical-equipment/cables mapping; hybrid EUR150m stripped from NI-to-common (264) and book common equity (2,043) for the parent-common basis - flagged. Dominant divergence: vendor uniform EBIT 578/EBITDA 680 vs issuer EBIT 257/operational EBITDA 390 (vendor routes -272 metal-price/hedge/other below EBIT; pretax 294 exact) - EV cross-checks qualified only, issuer-basis sensitivities shown. Peer EV uses cash&ST-investments and book NCI with no associate/LT-investment harmonization - qualified. FY2025 effective tax 6.46% is one-off-driven; vendor 5Y betas across the pool carry benchmark/frequency unavailable flag. No DCF, recommendation, synthesis weight or residual-band classification.

## Limitations
Market-wide, low-R2 equations not sector fair-value proof. January 2026 vintage ~302 days old at valuation date. File requires analyst 5Y growth, not our substituted sustainable growth; beta benchmark/frequency unspecified for peers. NKT effective tax 6.46% one-off-driven and vendor EBIT basis differs from issuer (578 vs 257) - flagged, not analyst consensus.

## Exact equations and t-statistics
See Coefficients_PE/PBV/EV_EBITDA workbook sheets.
$\text{PE} = \underset{(8.29)}{9.72} + \underset{(4.85)}{2.99} \, \text{Beta} + \underset{(11.95)}{49.82} \, g_{\text{EPS}} + \underset{(9.22)}{7.98} \, \text{Payout}$
$\text{PBV} = \underset{(3.70)}{0.73} + \underset{(5.87)}{3.92} \, g_{\text{EPS}} + \underset{(1.38)}{0.13} \, \text{Beta} + \underset{(24.81)}{10.75} \, \text{ROE} - \underset{(2.43)}{0.25} \, \text{Payout Ratio}$
$\text{EV/EBITDA} = \underset{(28.40)}{18.15} + \underset{(13.96)}{35.25} \, g - \underset{(10.65)}{0.11} \, \text{DFR} - \underset{(5.19)}{0.12} \, \text{Tax Rate} + \underset{(5.06)}{2.29} \, \text{ROIC}$
