# SU.PA relative valuation summary (published route + comparables)

## 1. Scope and route
Relative-only, stage 3. Stages 1, 2, 4 skipped_by_deviation (standing_approvals relative_only). Published
Damodaran regression route, EUROPE equations (dataset regressions_multi_2026-01, as_of 2026-01-01); comparables
per comparables_procedure.

## 2. Inputs
Price EUR 237.50; shares 563.05m; market cap EUR 133,724m; EPS 7.4075 (basic); book
value/share 42.9784; sources in relative_inputs.md (vendor extract cross-checked vs Schneider FY2025 release).

## 3. Published regression predictions (decimal units, as_published_note)
| Multiple | Predicted | Actual | Published R2 | Value/share |
|---|---|---|---|---|
| P/E | 27.96x | 32.06x | 0.201 | EUR 207.15 |
| P/BV (chosen) | 3.39x | 5.53x | 0.423 | EUR 145.78 |
| EV/EBITDA | 22.48x | 18.83x | 0.262 | EUR 288.95 |

Inputs: analyst consensus growth g_eps 20.40% / g_rev 11.56% (3Y, vendor statistics) — NO fundamental substitution
needed; roe 17.20% (closing book), payout 0.567 (declared DPS/EPS), beta 1.19, dfr 0.1296, tax 25.06%, roic 13.23%.

## 4. Comparables
See comparables_report.md. Primary P/E median growth-adjusted EUR 173.59 (raw EUR 232.63);
P/BV median ROE-adjusted EUR 208.13; EV/EBITDA EUR 226.16; EV/EBIT EUR 257.81.

## 5. Model choice and result
Published model chosen by highest published R2 among PE, PBV, EV/EBITDA: P/BV, value EUR 145.78
(-38.6% vs price). Alternatives: P/E EUR 207.15, EV/EBITDA EUR 288.95.
The P/BV prediction (3.39x vs actual 5.53x, +63% deviation) cannot see Schneider's ROE premium — a market-wide
equation limitation, not evidence of mispricing.

## 6. Limitations
- Relative only: no DCF, no recommendation (approved deviation).
- Published R2 values are low (0.20 to 0.42); the regression is a market cross-section, not an SU-specific fit.
- Peer and tier choices are agent judgement; index and ISIN checks pending; IEUR proxy membership only.
- Tier-3 peers used at cap (mining equipment economics) because the size band excluded most mid-cap electrical names.
- Workbook formulas are live but not recalculated (LibreOffice not installed); see regression_valuation.xlsx.
- No Spot_check by a human reviewer yet (human_review pending).

Academic analysis for coursework only; not investment advice. Figures are from public web sources accessed 2026-10-30/31 and cross-checked against Schneider Electric FY2025 results (26 Feb 2026).
