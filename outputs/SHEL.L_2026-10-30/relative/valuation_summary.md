# Relative valuation by regression — Europe, SHEL.L, 2026-10-30

## Headline
Draft PBV selected by highest eligible published R2 (0.423), a weaker heuristic rather than adjusted-R2/industry fit.

## Scope
SHEL.L only; no market sample/own estimation/DATA_BASE_MSCI under published route.

## Data
FY2025 uniform vendor inputs cross-checked with issuer. United Kingdom listing resolves EUROPE exact. Fundamental growth uses closing parent ROE 0.1023 x capped retention, explicitly approved substitution for unavailable matching 5Y analyst growth; vendor beta -0.19 negative; replaced by bottom-up relevered beta ~0.47 (Oil/Gas Integrated EUROPE unlevered cash-corrected 0.41, effective tax 39.11%) per the published-route rule.

## Fitted model
| model     |   predicted |   published_r2 |   value_per_share |   actual |   actual_predicted_gap |
|:----------|------------:|---------------:|------------------:|---------:|-----------------------:|
| PE        |    17.5947  |          0.201 |           41.0922 | 17.2945  |             -0.0170578 |
| PBV       |     1.98255 |          0.423 |           45.2696 |  1.7689  |             -0.107763  |
| EV/EBITDA |    20.1636  |          0.262 |          119.748  |  7.44643 |             -0.630699  |

## Diagnostics
Integrity findings retained in regression_results.json. GLOBAL PEG/PBV and EM EVEBITDA source anomalies do not affect these EUROPE equations. No n, SEy, adjusted R2, p-values, A/B/C, typicality or D1-D10 available: n/a_published_route. Classification: Not classified (no SEy published).

## Valuation results (sorted from most undervalued to most overvalued)
| model     |   value_per_share |
|:----------|------------------:|
| EV/EBITDA |          119.748  |
| PBV       |           45.2696 |
| PE        |           41.0922 |

## Robustness
All units decimal as approved; EVEBITDA alternative percentage-point DFR/tax prediction saved. Live predictions and price bridges reference Inputs; recalculation validation follows in formula_checks.json. Published EV definition undocumented.

## Key warnings
DRAFT pending human Spot_check. Primary EV/EBITDA per bucket F, but peer EV uses cash&ST-investments and book NCI with no associate/LT-investment harmonization - qualified. Vendor 5Y betas anomalous across pool (mostly negative); score dimension retained with flag. No DCF, recommendation, synthesis weight or residual-band classification.

## Limitations
Market-wide, low-R2 equations not sector fair-value proof. January 2026 vintage ~302 days old at valuation date. File requires analyst 5Y growth, not our substituted sustainable growth; beta benchmark/frequency unspecified for peers and vendor values anomalous. Effective tax 39.11%; g inputs are substituted fundamental growth, not analyst consensus. No residual dispersion or confidence range invented.

## Sources
source_log.csv; registered regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5; issuer cross-check in relative_inputs.md.

## Exact equations and t-statistics
See Coefficients_PE/PBV/EV_EBITDA workbook sheets.
$\text{PE} = \underset{(8.29)}{9.72} + \underset{(4.85)}{2.99} \, \text{Beta} + \underset{(11.95)}{49.82} \, g_{\text{EPS}} + \underset{(9.22)}{7.98} \, \text{Payout}$
$\text{PBV} = \underset{(3.70)}{0.73} + \underset{(5.87)}{3.92} \, g_{\text{EPS}} + \underset{(1.38)}{0.13} \, \text{Beta} + \underset{(24.81)}{10.75} \, \text{ROE} - \underset{(2.43)}{0.25} \, \text{Payout Ratio}$
$\text{EV/EBITDA} = \underset{(28.40)}{18.15} + \underset{(13.96)}{35.25} \, g - \underset{(10.65)}{0.11} \, \text{DFR} - \underset{(5.19)}{0.12} \, \text{Tax Rate} + \underset{(5.06)}{2.29} \, \text{ROIC}$
