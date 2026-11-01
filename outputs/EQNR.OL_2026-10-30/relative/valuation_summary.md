# Relative valuation by regression — Europe, EQNR.OL, 2026-10-30

## Headline
Draft PBV selected by highest eligible published R2 (0.423), a weaker heuristic rather than adjusted-R2/industry fit.

## Scope
EQNR.OL only; no market sample/own estimation/DATA_BASE_MSCI under published route.

## Data
FY2025 uniform vendor inputs cross-checked with issuer. Norway listing resolves EUROPE exact. Fundamental growth uses closing parent ROE 0.1248 x capped retention, explicitly approved substitution for unavailable matching 5Y analyst growth; vendor negative beta -0.65 replaced by bottom-up relevered beta (Oil/Gas Integrated EUROPE unlevered-cash-corrected 0.41, marginal 40%, market D/E).

## Fitted model
| model     |   predicted |   published_r2 |   value_per_share |   actual |   actual_predicted_gap |
|:----------|------------:|---------------:|------------------:|---------:|-----------------------:|
| PE        |    19.0377  |          0.201 |           372.339 | 22.7722  |               0.196165 |
| PBV       |     1.92001 |          0.423 |           301.009 |  2.84089 |               0.47962  |
| EV/EBITDA |    18.4837  |          0.262 |          2484.86  |  3.59101 |              -0.805721 |

## Diagnostics
Integrity findings retained in regression_results.json. GLOBAL PEG/PBV and EM EVEBITDA source anomalies do not affect these EUROPE equations. No n, SEy, adjusted R2, p-values, A/B/C, typicality or D1-D10 available: n/a_published_route. Classification: Not classified (no SEy published).

## Valuation results (sorted from most undervalued to most overvalued)
| model     |   value_per_share |
|:----------|------------------:|
| EV/EBITDA |          2484.86  |
| PE        |           372.339 |
| PBV       |           301.009 |

## Robustness
All units decimal as approved; EVEBITDA alternative percentage-point DFR/tax prediction saved. Live predictions and price bridges reference Inputs; recalculation validation follows in formula_checks.json. Published EV definition undocumented.

## Key warnings
DRAFT pending human Spot_check. Primary EV/EBITDA per bucket F, but peer EV uses cash&ST-investments and book NCI with no associate/LT-investment harmonization - qualified. Vendor 5Y betas anomalous across pool (mostly negative); score dimension retained with flag. No DCF, recommendation, synthesis weight or residual-band classification.

## Limitations
Market-wide, low-R2 equations not sector fair-value proof. January 2026 vintage ~302 days old at valuation date. File requires analyst 5Y growth, not our substituted sustainable growth; beta benchmark/frequency unspecified for peers and vendor values anomalous. Norwegian petroleum tax 79.84% is far above peer effective rates - DFR/tax term dispersion is material. No residual dispersion or confidence range invented.

## Sources
source_log.csv; registered regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5; issuer cross-check in relative_inputs.md.

## Exact equations and t-statistics
See Coefficients_PE/PBV/EV_EBITDA workbook sheets.
$\text{PE} = \underset{(8.29)}{9.72} + \underset{(4.85)}{2.99} \, \text{Beta} + \underset{(11.95)}{49.82} \, g_{\text{EPS}} + \underset{(9.22)}{7.98} \, \text{Payout}$
$\text{PBV} = \underset{(3.70)}{0.73} + \underset{(5.87)}{3.92} \, g_{\text{EPS}} + \underset{(1.38)}{0.13} \, \text{Beta} + \underset{(24.81)}{10.75} \, \text{ROE} - \underset{(2.43)}{0.25} \, \text{Payout Ratio}$
$\text{EV/EBITDA} = \underset{(28.40)}{18.15} + \underset{(13.96)}{35.25} \, g - \underset{(10.65)}{0.11} \, \text{DFR} - \underset{(5.19)}{0.12} \, \text{Tax Rate} + \underset{(5.06)}{2.29} \, \text{ROIC}$
