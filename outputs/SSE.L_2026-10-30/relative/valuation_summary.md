# Relative valuation by regression — EUROPE, 2026-10-30 (published_damodaran route)

## Headline
Published EUROPE equations (regressions_multi_2026-01): **PBV chosen** — predicted 2.305x → **£22.98/share** vs price £26.27 (−12.5% rich, deviation actual/predicted −1 = +14.0%). Alternatives: PE predicted 23.64x → £23.23/share; EV/EBITDA predicted 20.98x → £40.94/share. Market-wide equations (low R²), not industry fits; deviation from prediction is not proof of mispricing. The peer method (comparables_report.md) gives EV/EBITDA £19.28/share mid — below the regression PBV estimate; both sit below the current price, while the regression EV/EBITDA sits far above it.

## Data
Uniform vendor FY2025 inputs (StockAnalysis, reused dated cache extracts, accessed 2026-11-02), cross-checked vs SSE FY2024/25 preliminary results (LSE RNS 4968J + sse.com statement PDF; revenue 10,131.9 and attributable NI 1,189.4 exact ties). Inputs: beta 0.53 (vendor 5Y observed); g_eps 15.19% and g_rev 7.71% analyst consensus 3Y (sourced — no substitution needed); roe 0.0986 closing book (NI to common £1,189m / parent equity £12,064m); payout 0.597 (declared ~£710m / NI to common; CF-paid basis 0.40 underweights final-dividend timing — flagged, not used); dfr 0.2526; tax_rate 0.2799 effective FY2025 (issuer-stated reported ETR 29.4% noted); roic 0.0747. Negative inputs absent — all three models eligible.

## Fitted model
Route `published_damodaran`: `datasets.equation_for('United Kingdom', dep, 2026-10-30)` → EUROPE region, regressions_multi_2026-01 (sha256 a894ea86…). Equations and published t-statistics on Coefficients_* sheets of regression_valuation.xlsx; live-formula predictions verified vs `published_regressions.predict` <1e-9 after recalculation. Model choice: highest published R² among eligible → PBV (R²=0.423) over EV/EBITDA (0.262) and PE (0.201); ranking by published R² is a weaker heuristic than own-sample adjusted R².

## Diagnostics
Not available under this route: n, SEy, adjusted R², p-values, A/B/C scopes, typicality routing, D1–D10, robustness refits and residual-band classification (all `n/a_published_route`). Reported instead: predicted multiple, actual multiple, deviation, published R² and t-statistics. Dataset integrity findings from stage 0 retained (GLOBAL anomalies do not affect EUROPE equations).

## Valuation results (sorted from most undervalued to most overvalued)

| model | predicted | published R² | actual | deviation | GBP/share |
|---|---|---|---|---|---|
| EV/EBITDA | 20.98x | 0.262 | 14.72 | −29.9% | £40.94 |
| PE | 23.64x | 0.201 | 26.65 | +12.7% | £23.23 |
| PBV | 2.305x | 0.423 | 2.63 | +14.0% | £22.98 |

## Robustness
Decimal unit policy is user-approved (`damodaran_dfr_tax_units: decimal`); percent-point alternative for EV/EBITDA shown in regression_results.json `unit_alternative`. Payout basis sensitivity: 0.597 declared vs 0.40 CF-paid — declared basis is the economically meaningful one; noted. No PS equation exists (documented); supplementary PEG/EV/IC/EV/Sales not used in standard mode.

## Key warnings
Provisional: human Spot_check pending; ownership/event audit incomplete. The market-wide EV/EBITDA prediction (21.0x) sits far above the European utility peer median (11.8x): sector mix in a market-wide equation is not structure the model can see — same gap recorded for IBE/ENEL/ENGIE runs; peer-method result preferred for the EV/EBITDA view. SSE's vendor Total Debt appears to include equity-classified hybrid capital (dfr slightly overstated); Mar-2025 fiscal basis vs Dec basis of equations' underlying sample; 2026 equity raise changed the share count (~1.10bn → ~1.21bn).

## Limitations
Equation vintage Jan-2026 (~10 months > 6-month flag). Market-wide scope — no sector structure; utilities predictions can differ from sector reality (published R² 20–42%). Analyst-growth definition differs from project fundamental growth (consensus used and labelled). Damodaran EV/invested-capital definitions undocumented (leases/NCI/associates treatment may differ). No residual dispersion — deviation is not a residual-band classification. No DATA_BASE_MSCI.xlsx under this route.

## Sources
source_log.csv (S3_* rows); registered regressions_multi_2026-01 via data library; SSE FY2024/25 preliminary results (LSE RNS 4968J + sse.com statement PDF); stockanalysis uniform extracts; cache/macro/2026-10-30.json FX.
