# EDP Renováveis (EDPR.LS) comparables — 2026-10-30

PROVISIONAL: ownership/events/classification audit incomplete; human Spot_check pending; associates proxied by Long-Term Investments for the target only and NOT subtracted from peer EV (uniform EV-before-associates basis). No replacement-cost Tobin's Q; no sourced home-index PE (relative_pe unavailable). ISINs registry-mapped pending issuer-page verification. EDP S.A. hard-excluded as EDPR's ~71% parent.

## Route, basis, scope
Single target, orchestrator layout `outputs/EDPR.LS_2026-10-30/relative/`. Route: `web_minimum` (uniform stockanalysis raw fields); `published_damodaran` regression route; standard mode; FY2025 earnings basis; comparison currency EUR; one price date 2026-10-30 (ECB FX snapshot cache/macro/2026-10-30.json). No group workbook; candidates from issuer-named competitors, sector_adjustments Tier-1 seeds and own research.

## Target profile
Renewable developer/operator (bucket B): 20.4 GW installed (18.8 GW EBITDA + 1.6 GW equity MW), wind/solar/storage across US and Europe; asset-rotation and US tax-equity partnership model means EBITDA margin (vendor 52%) and claims (NCI €1.9bn, deferred partnership revenues) are structurally different from integrated utilities.

## Candidate pool and selection
Initial pool 34 + parent evidence row: 16 Tier-1 renewable IPPs/developers, 17 Tier-2 integrated utilities with renewable fleets, 1 parent row (EDP). Rejected before scoring: EDP (parent), NEOEN/OX2/IREN/HERA (uniform source 404 — no per-row source switching), EKT/PNE3 (<€1bn), AY/BLX/INE (no common 2026-10-30 price date), ORA (kept World-only). Europe step feasible at default caps (17 in-band Tier-1/2 Europe candidates; size band €1.3–132.5bn on target €13.25bn). Selected 10: ORSTED, RWE, EOAN, SSE, ERG, SLR, GRE, ANE, ENGI, ENEL — 5 Tier-1 + 5 Tier-2, all Europe-listed, no relaxation needed. Scores, winsorization (pool-only 5%/95%), weights and constraint logs in peer_selection.json / comparables_audit.xlsx.

## Primary multiple and values
Bucket-B primary: **EV/EBITDA** (peer median 11.99x, n=10). Cross-checks: PBV (ROE-scaled), PE, EV/EBIT, EV/CF, PS, EV/Sales, EV/Assets. Headline uses the uniform vendor FY2025 EBITDA (€1,187m) — see definition warning below.

| Metric | p25 | median | p75 | EUR/share range |
|---|---|---|---|---|
| EV/EBITDA 11.99x × vendor EBITDA €1,187m | 8.97x | 11.99x | 14.29x | €0.53 – 3.92 – 6.49 |
| EV/EBITDA 11.99x × issuer EBITDA €1,947m (sensitivity) | – | – | – | ~€12.65 mid |
| PBV ROE-scaled 0.47x (unadjusted 2.15x) | – | 0.47x | – | €2.75 – 4.59 – 5.39 (scaled); raw 1.33x–2.70x → €12.99–26.3 |
| PE median 22.0x × NI €215.8m | 14.3x | 22.0x | 28.0x | €2.92 – 4.48 – 5.71 |
| EV/CF (reported CFO) 13.45x | 12.3x | 13.4x | 24.5x | €2.55 – 3.68 – 14.49 |
| EV/Assets 0.89x | 0.68x | 0.89x | 1.25x | €10.11 – 16.07 – 26.26 |

### EBITDA-definition warning (material)
Vendor EBITDA (€1,187m) excludes equity-method investment income (€472.6m) and institutional-partnership income that EDPR's issuer EBITDA (€1,947m reported, €1,974m recurring) includes — while EDPR's EV carries the matching claims (NCI €1,906m, deferred partnership revenues €2,149m). The vendor-EBITDA headline (€3.92/share) is therefore biased low versus the issuer basis (~€12.65/share, near the €12.50 market price). Both figures are retained; the issuer-EBITDA sensitivity is the economically consistent variant but is NOT the uniform peer basis. EDPR's deferred institutional-partnership revenues are not deducted as a debt-like claim in either variant (recorded limitation).

## Fundamental comparison vs peer medians
EDPR vs peer median: ROE 2.1% vs ~10%; fundamental growth 1.7% vs ~4%; net debt/EBITDA 6.9x vs ~4.1x; EBITDA margin 52% vs ~28%; capex/sales 124% vs ~37%. EDPR scores as low-return, high-leverage, high-reinvestment — consistent with scaled-multiple discounts (PBV 0.47x vs 2.15x unadjusted).

## Exclusions, relaxations, replacements
All in candidate_gates.csv. No relaxation invoked (Europe step feasible). No candidate replaced after business-description review; ORA restricted to World-only pool which was never reached.

## Limitations
Vendor FY bases (Dec-25 for all selected). Payout>100% for ERG/ENEL/ENGI (fiscal-basis mismatch, retained). Consensus growth unavailable on uniform route → fundamental ROE×retention used for scoring (pool rule applied). Spot_check pending. Benchmark: Damodaran Europe utility EV/EBITDA median not registered in data library — >50% gap check unavailable; EUROPE published EV/EBITDA equation predicts 21.1x for EDPR's own inputs as the only cross-reference.

## Sources
Per-row `field: URL (accessed 2026-11-01)` in candidate_gates.csv and source_log.csv. Issuer: EDPR FY25 Results Report PDF (edpr-investors.com). ISINs registry-mapped.
