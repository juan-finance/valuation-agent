# Stage 3 relative valuation — AI.PA @ 2026-10-30 (published_damodaran)

## Published regressions (dataset regressions_multi_2026-01, EUROPE, vintage Jan-2026)
| Dependent | Equation (inputs decimal) | R² | Predicted | Equity €m | €/share |
|---|---|---|---|---|---|
| PE | 9.72 + 2.99·β + 49.82·g_eps + 7.98·payout | 0.201 | 19.14 | 67,347 | 105.8 |
| PBV | 0.73 + 3.92·g_eps + 0.13·β + 10.75·roe − 0.25·payout | 0.423 | 2.36 | 61,914 | 97.3 |
| EV/EBITDA | 18.15 + 35.25·g_rev − 0.11·dfr − 0.12·tax + 2.29·roic | 0.262 | 19.73 | 134,670 | 211.6 |

Inputs: β=0.612 observed (≤2.5, kept); g_eps=5.28% and g_rev=4.0% fundamental — `substituted_input` per published_route_allow_fundamental_growth; payout 62.25%; ROE 13.97%; dfr 0.130; tax 25.82%; ROIC 9.30%. Units: `as_published_note` = all decimals (approved). Best-R² model chosen per dependent. SEy/residuals/sensitivities: n/a_published_route.

## Comparables
Raw PE median €170.8; growth-scaled PE €90.7; EV/EBIT €201.2; EV/EBITDA €199.4. Range €91–201.

## Combined view
Regressions €97–212; comparables €91–201. Central cluster ~€100 (PBV, scaled PE, PE-regression) vs ~€200 (EV-based raw peer medians). Market €180.9. DCF €81.4. For stage 4: the EV-multiple optimism traces to peers' high EBITDA margins vs AI's 28% and the EV/EBITDA regression's g_rev term — discuss, don't tune.

## Limitations (section 7 of route file)
Published equations are market-level (all-sector) EUROPE regressions, vintage Jan-2026 (~10 months old — vintage flag); sector fit is coarse; R² 0.20–0.42 → wide dispersion; no PS equation exists (by design); standard mode ran PE/PBV/EVEBITDA only; SEy/D1–D10 residuals unavailable on this route.
