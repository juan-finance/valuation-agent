# Relative valuation by regression — EUROPE, 2026-10-30 (published_damodaran route)

## Headline
Published EUROPE equations (regressions_multi_2026-01): **PBV chosen** — predicted 2.259x → **€16.96/share** vs price €22.18 (−23.5% rich, deviation actual/predicted −1 = +30.8%). Alternatives: EV/EBITDA predicted 19.69x → €33.04/share; PE predicted 21.61x → €19.62/share. Market-wide equations (low R²), not industry fits; deviation from prediction is not proof of mispricing. The peer method (comparables_report.md) gives EV/EBITDA €17.32/share mid — remarkably close to the regression PBV estimate; both sit below the current price, while the regression EV/EBITDA sits far above it.

## Data
Uniform vendor FY2025 inputs (StockAnalysis, reused dated cache extracts, accessed 2026-11-01), cross-checked vs Iberdrola FY2025 results (CNMV filing + press release). Inputs: beta 0.45 (vendor 5Y observed); g_eps 9.15% and g_rev 4.05% analyst consensus 3Y (sourced — no substitution needed); roe 0.1209 closing book (NI to common €6,055m / parent equity €50,068m); payout 0.750 (declared ~€4,543m / NI to common; CF-paid basis 0.21 distorted by scrip dividend — flagged, not used); dfr 0.2865; tax_rate 0.2064 effective FY2025; roic 0.0749. Negative inputs absent — all three models eligible.

## Fitted model
Route `published_damodaran`: `datasets.equation_for('Spain', dep, 2026-10-30)` → EUROPE region, regressions_multi_2026-01 (sha256 a894ea86…). Equations and published t-statistics on Coefficients_* sheets of regression_valuation.xlsx; live-formula predictions verified vs `published_regressions.predict` <1e-9 after recalculation. Model choice: highest published R² among eligible → PBV (R²=0.423) over EV/EBITDA (0.262) and PE (0.201); ranking by published R² is a weaker heuristic than own-sample adjusted R².

## Diagnostics
Not available under this route: n, SEy, adjusted R², p-values, A/B/C scopes, typicality routing, D1–D10, robustness refits and residual-band classification (all `n/a_published_route`). Reported instead: predicted multiple, actual multiple, deviation, published R² and t-statistics. Dataset integrity findings from stage 0 retained (GLOBAL anomalies do not affect EUROPE equations).

## Valuation results (sorted from most undervalued to most overvalued)

| model | predicted | published R² | actual | deviation | EUR/share |
|---|---|---|---|---|---|
| EV/EBITDA | 19.69x | 0.262 | 14.76 | −25.0% | €33.04 |
| PE | 21.61x | 0.201 | 24.43 | +13.1% | €19.62 |
| PBV | 2.259x | 0.423 | 2.95 | +30.8% | €16.96 |

## Robustness
Decimal unit policy is user-approved (`damodaran_dfr_tax_units: decimal`); percent-point alternative for EV/EBITDA shown in regression_results.json `unit_alternative`. Payout basis sensitivity: 0.75 declared vs 0.21 CF-paid (scrip) — declared basis is the economically meaningful one; noted. No PS equation exists (documented); supplementary PEG/EV/IC/EV/Sales not used in standard mode.

## Key warnings
Provisional: human Spot_check pending; ownership/event audit incomplete. The market-wide EV/EBITDA prediction (19.7x) sits far above the European utility peer median (12.6x): sector mix in a market-wide equation is not structure the model can see — same gap recorded for ENEL/ENGIE runs; peer-method result preferred for the EV/EBITDA view. Scrip dividend means vendor CF dividend data understate the payout; declared basis used.

## Limitations
Equation vintage Jan-2026 (~10 months > 6-month flag). Market-wide scope — no sector structure; utilities predictions can differ from sector reality (published R² 20–42%). Analyst-growth definition differs from project fundamental growth (consensus used and labelled). Damodaran EV/invested-capital definitions undocumented (leases/NCI/associates treatment may differ). No residual dispersion — deviation is not a residual-band classification. No DATA_BASE_MSCI.xlsx under this route.

## Sources
source_log.csv (S3_* rows); registered regressions_multi_2026-01 via data library; Iberdrola FY2025 CNMV filing and press release; stockanalysis uniform extracts; cache/macro/2026-10-30.json FX.
