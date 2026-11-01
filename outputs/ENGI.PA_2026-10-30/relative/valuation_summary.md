# Relative valuation by regression — EUROPE, 2026-10-30 (published_damodaran route)

## Headline
Published EUROPE equations (regressions_multi_2026-01): **PBV chosen** — predicted 1.970x → **€26.71/share** vs price €23.43 (+14.0% upside; deviation actual/predicted −1 = −12.2%). Alternatives: PE predicted 20.89x → €31.69/share; EV/EBITDA predicted 20.23x → €88.37/share. Market-wide equations (low R²), not industry fits; deviation from prediction is not proof of mispricing. The peer method (comparables_report.md) gives EV/EBITDA €45.51/share mid — higher than the regression PBV but same direction (price below estimate). Both are shown, none reconciled under relative_only.

## Data
Uniform vendor FY2025 inputs (StockAnalysis, via 2026-10-30 dated cache), cross-checked vs ENGIE FY2025 results press release. Inputs: beta 0.57 (vendor 5Y observed); g_eps 4.73% and g_rev 5.60% analyst consensus 3Y (sourced — no substitution needed; issuer NRIgs 2026 guidance €4.6–5.2bn); roe 0.1119 closing book (NI to common €3,687m / parent equity €32,951m); payout 0.89 (proposed dividend ~€3,283m = €1.35/sh = issuer-stated 67% of NRIgs; paid-cash basis 1.23 flagged); dfr 0.492; tax_rate 0.2485 effective FY2025; roic 0.0851. Negative inputs absent — all three models eligible.

## Fitted model
Route `published_damodaran`: `datasets.equation_for('France', dep, '2026-10-30')` → EUROPE region, regressions_multi_2026-01 (sha256 a894ea86…). Equations and published t-statistics on Coefficients_* sheets of regression_valuation.xlsx; live-formula predictions verified vs `published_regressions.predict` <1e-9 after recalculation. Model choice: highest published R² among eligible → PBV (R²=0.423) over EV/EBITDA (0.262) and PE (0.201); ranking by published R² is a weaker heuristic than own-sample adjusted R².

## Diagnostics
Not available under this route: n, SEy, adjusted R², p-values, A/B/C scopes, typicality routing, D1–D10, robustness refits and residual-band classification (all `n/a_published_route`). Reported instead: predicted multiple, actual multiple, deviation, published R² and t-statistics. Dataset integrity findings from stage 0 retained (GLOBAL anomalies do not affect EUROPE equations).

## Valuation results (sorted from most undervalued to most overvalued)

| model | predicted | published R² | actual | deviation | EUR/share |
|---|---|---|---|---|---|
| EV/EBITDA | 20.23x | 0.262 | 8.11 | −59.9% | €88.37 |
| PE | 20.89x | 0.201 | 15.45 | −26.0% | €31.69 |
| PBV | 1.970x | 0.423 | 1.73 | −12.2% | €26.71 |

## Robustness
Decimal unit policy is user-approved (`damodaran_dfr_tax_units: decimal`); percentage-point alternative for EV/EBITDA shown in regression_results.json `unit_alternative` (20.23x decimal vs 11.92x pp — material 41% gap, decimal policy verified per standing approval; percent-point prediction 11.9x sits near the utility peer median 12.2x, recorded). Payout basis sensitivity: 0.89 declared vs 1.23 paid-cash — direction unchanged. No PS equation exists (documented); supplementary PEG/EV/IC/EV/Sales not used in standard mode.

## Key warnings
Provisional: human Spot_check pending; ownership/event audit incomplete. The market-wide EV/EBITDA prediction (20.2x) sits far above the European utility peer median (12.2x): sector mix in a market-wide equation is not structure the model can see; peer-method result preferred for the EV/EBITDA view. Engie's Belgian-nuclear JV transition and pending UKPN acquisition make FY2025 figures less typical than a steady-state year.

## Limitations
Equation vintage Jan-2026 (~10 months > 6-month flag). Market-wide scope — no sector structure; utilities predictions can differ from sector reality (published R² 20–42%). Analyst-growth definition differs from project fundamental growth (consensus used and labelled). Damodaran EV/invested-capital definitions undocumented (leases/NCI/associates treatment may differ). No residual dispersion — deviation is not a residual-band classification. No DATA_BASE_MSCI.xlsx under this route.

## Sources
source_log.csv (S3_* rows); registered regressions_multi_2026-01 via data library; ENGIE issuer FY2025 press release; stockanalysis uniform extracts; cache/macro/2026-10-30.json FX.
