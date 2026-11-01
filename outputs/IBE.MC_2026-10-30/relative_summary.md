# IBE.MC relative valuation — plain-text summary — 2026-10-30

Price (close 2026-10-30): EUR 22.18
Mode: relative_only deviation — no DCF; stages 1, 2, 4 skipped_by_deviation. Status: PROVISIONAL (human Spot_check pending).

COMPARABLES (10 peers: SSE, RWE, NTGY, NG, EDP, EOAN, TRN, SRG, VER, ENGI — all Europe, 8 Tier-1 + 2 Tier-2)
Primary multiple EV/EBITDA, peer median 12.56x (p25 10.47x / p75 14.31x):
  EUR/share: 12.71 – 17.32 – 21.18   (median 17.32 = −21.9% vs price)
  Issuer-EBITDA sensitivities (median): adjusted 15,684m → 19.18; reported 16,592m → 20.89
Cross-checks (EUR/share, medians): PE raw 15.53 (× vendor NI 6,055m; issuer NI → 16.12/17.31); PBV ROE-scaled 15.95; EV/EBIT 19.06; EV/CF 13.65; EV/Assets 14.70; PS scaled 15.53. Growth-scaled PE/PEG ~49.8 flagged as distorted (near-zero peer fundamental growth).
IBE actual multiples vs peers: EV/EBITDA 14.8x vs 12.6x; PE 24.4x vs 17.1x; ROE 12.1% vs 10.6%; growth 9.8% vs 3.1%; beta 0.45 vs 0.57; net debt/EBITDA 3.79x vs 5.03x.

PUBLISHED EUROPE REGRESSIONS (Damodaran regressions_multi_2026-01, decimal unit policy)
Chosen model PBV (highest published R2 0.423): predicted 2.259x vs actual 2.95 → EUR 16.96/share (−23.5% vs price; deviation +30.8%).
Alternatives: EV/EBITDA predicted 19.69x (R2 0.262) → EUR 33.04 (+49.0%); PE predicted 21.61x (R2 0.201) → EUR 19.62 (−11.5%).
Inputs: beta 0.45; g_eps 9.15%, g_rev 4.05% (consensus); ROE 0.121; payout 0.750 declared basis (scrip; CF-paid 0.21 not used); dfr 0.287; tax 0.2064; roic 0.0749.

READ: peer EV/EBITDA (17.32) and regression PBV (16.96) bracket ~EUR 16-17/share vs price 22.18 → market prices IBE ~20-30% above both relative readings; regression EV/EBITDA (33.04) is a market-wide equation outlier vs the sector peer median (19.7x predicted vs 12.6x observed), recorded not reconciled.

QA block C: no failures; warned items (no peer-benchmark dataset, distorted growth-scaled multiples, workbook checked outside Excel) disclosed in qa_results.md.
Files: outputs/IBE.MC_2026-10-30/relative/ + relative_report_IBE.MC.pdf. Academic analysis; not investment advice.
