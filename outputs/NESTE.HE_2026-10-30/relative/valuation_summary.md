# Relative valuation by regression — Europe, NESTE.HE, 2026-10-30

## Headline
Draft PBV selected by highest eligible published R2 (0.423), a weaker heuristic rather than adjusted-R2/industry fit.

## Scope
NESTE.HE only; no market sample/own estimation/DATA_BASE_MSCI under published route.

## Data
FY2025 uniform vendor inputs cross-checked with issuer. Finland listing resolves EUROPE exact. Fundamental growth uses closing parent ROE 0.0197 x capped retention, explicitly approved substitution for unavailable matching 5Y analyst growth; vendor 5Y beta 0.56 kept (within 0-2.5); no replacement needed.

## Fitted model
| model     |   predicted |   published_r2 |   value_per_share |    actual |   actual_predicted_gap |
|:----------|------------:|---------------:|------------------:|----------:|-----------------------:|
| PE        |   19.3744   |          0.201 |           3.63138 | 151.181   |               6.80311  |
| PBV       |    0.764449 |          0.423 |           7.27753 |   2.97648 |               2.89363  |
| EV/EBITDA |   18.1651   |          0.262 |          21.6087  |  22.7633  |               0.253139 |

## Diagnostics
Integrity findings retained in regression_results.json. GLOBAL PEG/PBV and EM EVEBITDA source anomalies do not affect these EUROPE equations. No n, SEy, adjusted R2, p-values, A/B/C, typicality or D1-D10 available: n/a_published_route. Classification: Not classified (no SEy published).

## Valuation results (sorted from most undervalued to most overvalued)
| model     |   value_per_share |
|:----------|------------------:|
| EV/EBITDA |          21.6087  |
| PBV       |           7.27753 |
| PE        |           3.63138 |

## Robustness
All units decimal as approved; EVEBITDA alternative percentage-point DFR/tax prediction saved. Live predictions and price bridges reference Inputs; recalculation validation follows in formula_checks.json. Published EV definition undocumented.

## Key warnings
DRAFT pending human Spot_check. Primary EV/EBITDA per bucket F renewable-fuels mapping; target EBITDA basis is the dominant divergence (vendor uniform 1,124 vs issuer reported 1,438 / comparable 1,683) - sensitivities shown, vendor basis kept for peer consistency. Peer EV uses cash&ST-investments and book NCI with no associate/LT-investment harmonization - qualified. Vendor 5Y betas anomalous across pool (several negative/near-zero); score dimension retained with flag. NESTE payout>1 collapses fundamental growth to ~0 and FY2025 ROE is a cyclical trough (1.96%) - growth dimension and published-equation inputs flagged. No DCF, recommendation, synthesis weight or residual-band classification.

## Limitations
Market-wide, low-R2 equations not sector fair-value proof. January 2026 vintage ~302 days old at valuation date. File requires analyst 5Y growth, not our substituted sustainable growth; beta benchmark/frequency unspecified for peers and vendor values anomalous. Neste FY2025 effective tax 27.64% within European range; payout capped at 1.0 (actual 1.069) makes g_eps ~0 - flagged, not analyst consensus. No residual dispersion or confidence range invented.

## Sources
source_log.csv; registered regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5; issuer cross-check in relative_inputs.md.

## Exact equations and t-statistics
See Coefficients_PE/PBV/EV_EBITDA workbook sheets.
$\text{PE} = \underset{(8.29)}{9.72} + \underset{(4.85)}{2.99} \, \text{Beta} + \underset{(11.95)}{49.82} \, g_{\text{EPS}} + \underset{(9.22)}{7.98} \, \text{Payout}$
$\text{PBV} = \underset{(3.70)}{0.73} + \underset{(5.87)}{3.92} \, g_{\text{EPS}} + \underset{(1.38)}{0.13} \, \text{Beta} + \underset{(24.81)}{10.75} \, \text{ROE} - \underset{(2.43)}{0.25} \, \text{Payout Ratio}$
$\text{EV/EBITDA} = \underset{(28.40)}{18.15} + \underset{(13.96)}{35.25} \, g - \underset{(10.65)}{0.11} \, \text{DFR} - \underset{(5.19)}{0.12} \, \text{Tax Rate} + \underset{(5.06)}{2.29} \, \text{ROIC}$
