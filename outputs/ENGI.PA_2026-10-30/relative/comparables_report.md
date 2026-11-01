# ENGIE (ENGI.PA) comparables — 2026-10-30

PROVISIONAL: ownership/events/classification audit incomplete; human Spot_check pending; associates proxied by Long-Term Investments for the target only and NOT subtracted from peer EV (uniform EV-before-associates basis). No replacement-cost Tobin's Q; no sourced home-index PE (relative_pe unavailable). ISINs registry-mapped pending issuer-page verification. Vendor FY2025 CFO for ENGIE is NEGATIVE (-€1,476m vs issuer CFFO €13.6bn — Belgian nuclear cash-out and working-capital swings): EV/CF marked NM for the target.

## Route, basis, scope
Single target, orchestrator layout `outputs/ENGI.PA_2026-10-30/relative/`. Route: `web_minimum` (uniform stockanalysis raw fields); `published_damodaran` regression route; standard mode; FY2025 earnings basis; comparison currency EUR; one price date 2026-10-30 (ECB FX snapshot cache/macro/2026-10-30.json). No group workbook; candidates from issuer-named competitors, sector_adjustments Tier-1 seeds and own research. Vendor extracts shared with the EDPR/ENEL runs' dated cache (EDPRpool_*/ENELpool_*); only CEZ re-fetched (404 again, documented).

## Target profile
Integrated utility (bucket A): gas/power networks, renewables & BESS (57.2 GW installed), gas generation, energy supply; Belgian nuclear (Tihange 3/Doel 4) transferred to a JV with the Belgian State in 2025 — FY2025 figures still carry transition effects; UK Power Networks acquisition pending. EUR reporting = trading currency, Dec year-end. Net debt/EBITDA 3.1x (vendor basis), declared payout 67% of NRIgs (issuer) / ~89% of reported NI to common.

## Candidate pool and selection
Initial pool 33 + CEZ evidence row: 14 Tier-1 integrated/regulated European utilities (incl. Endesa — eligible for ENGI: subsidiary of Enel, not of the target), 18 Tier-2 (renewable IPPs, grid operators, generators, World-relaxation candidates). Rejected before scoring: CEZ (uniform source 404; MSCI EM anyway), ORA (US-listed, World-only), AY/BLX/INE (no common 2026-10-30 price date). Europe step feasible at default caps: 20 in-band Tier-1/2 candidates (size band €5.70–569.8bn on target €57.0bn). Selected 10 lowest scores: ENEL, EOAN, EDP, FORTUM, VER, NG, SSE, CNA, SRG, ORSTED — 8 Tier-1 + 2 Tier-2, all Europe-listed, no relaxation needed, no replacement after business-description review. Scores, winsorization (pool-only 5%/95%), weights and constraint logs in peer_selection.json / comparables_audit.xlsx. Iberdrola, RWE, NTGY, ELE, A2A scored above the selected set.

## Primary multiple and values
Bucket-A primary: **EV/EBITDA** (peer median 12.23x, n=10). Cross-checks: PE, PBV (ROE-scaled), EV/EBIT, EV/CF (target NM), PS, EV/Sales, EV/Assets. Headline uses uniform vendor FY2025 EBITDA (€13,012m) — see basis note below.

| Metric | p25 | median | p75 | EUR/share range |
|---|---|---|---|---|
| EV/EBITDA 12.23x × vendor EBITDA €13,012m | 8.85x | 12.23x | 15.97x | €27.43 – 45.51 – 65.55 |
| EV/EBITDA × issuer consolidated EBITDA €14,700m (sensitivity) | – | – | – | ~€54.00 mid |
| EV/EBITDA × issuer ex-nuclear EBITDA €13,400m (sensitivity) | – | – | – | ~€47.46 mid |
| PE median 23.35x × NI to common €3,687m | 16.72x | 23.35x | 26.97x | €25.37 – 35.44 – 40.92 |
| PE × issuer NIGs €3,827m (sensitivity) | – | – | – | ~€36.78 mid |
| PE × issuer NRIgs €4,900m (sensitivity) | – | – | – | ~€47.09 mid |
| PBV ROE-scaled 2.55x (unadjusted 2.38x) | – | 2.55x | – | €24.36 – 34.55 – 40.66 (scaled) |
| EV/EBIT 21.07x | 12.27x | 21.07x | 23.63x | €22.13 – 52.31 – 61.12 |
| EV/CF (reported CFO) 14.06x | 12.48x | 14.06x | 17.16x | NM — target FY2025 CFO negative |
| EV/Assets 1.00x | 0.82x | 1.00x | 1.32x | €37.16 – 49.71 – 72.26 |
| PS 2.15x (net-margin scaled 1.20x) | 0.76x | 2.15x | 4.02x | €25.37 – 35.44 – 40.92 raw / €22.56 – 63.59 – 119.14 scaled |
| EV/Sales 3.15x (margin-scaled 2.21x) | 1.42x | 3.15x | 4.71x | €22.04 – 73.41 – 119.47 scaled |
| PEG | – | – | – | NM (target fundamental growth = 0 on paid-cash payout basis) |

### EBITDA-basis note
Vendor EBITDA €13,012m is below issuer consolidated EBITDA €14,700m and ex-nuclear €13,400m (definition scope: vendor excludes items the issuer aggregates, incl. nuclear contribution). The issuer-basis sensitivities (€47.5–54.0/share vs €45.5 vendor basis) are retained in sensitivities.csv. NI basis: vendor "Net Income to Common" €3,687m vs issuer NIGs €3,827m — the vendor deducts a further ~€140m (hybrid/perpetual coupons; Engie has hybrids) — flagged, vendor basis kept for peer comparability, issuer bases in sensitivity (PE → €36.78 / €47.09 on NRIgs).

### CFO and payout notes
Vendor FY2025 operating cash flow -€1,476m is negative (Belgian nuclear cash-out and working-capital swings; issuer CFFO €13.6bn on its own definition) — EV/CF unusable for the target and recorded as NM rather than valued. Scoring growth uses the paid-cash dividend basis (€4,529m) → payout 1.23 capped at 1 → fundamental growth = 0 for ENGI, same pool rule as ENEL/FORTUM; PEG and growth-scaled PE adjustment are unavailable on this basis. For the published-route payout input the proposed FY2025 dividend (€1.35/sh ≈ €3,283m, issuer-stated 67% of NRIgs) is used → 0.89 on NI to common.

## Fundamental comparison vs peer medians
ENGI vs selected peers: actual EV/EBITDA 8.11x vs peer median 12.23x; PE 15.45x vs 23.35x; ROE 10.9% vs ~9.7%; net debt/EBITDA 3.13x vs ~3.26x; EBITDA margin 18.1% vs ~27.8% (vendor scope); beta 0.57 vs ~0.57.

## Exclusions, relaxations, replacements
All in candidate_gates.csv. No relaxation invoked (Europe step feasible at default caps). No Tier-3 member. ORA restricted to World-only pool which was never reached. Endesa inclusion documented (peer of Engie; its Enel parentage is not a target relationship — flagged for the pending ownership audit).

## Limitations
Vendor FY bases (Dec-25 for all selected). Paid-cash payout >100% for ENEL/FORTUM (and ENGI scoring basis) — fiscal-basis mismatch retained. Consensus growth unavailable on uniform route → fundamental ROE×retention used for scoring (pool rule applied). Spot_check pending. Benchmark: Damodaran Europe utility EV/EBITDA median not registered in data library — >50% gap check unavailable; EUROPE published EV/EBITDA equation predicts 20.2x for ENGI's inputs as the only cross-reference (market-wide, not a sector median). Peer EV multiples uniformly treat associates as before-associates; Engie's LT-investment balance (€13.2bn) is large — harmonized-EV caveat recorded.

## Sources
Per-row `field: URL (accessed 2026-11-01)` in candidate_gates.csv and source_log.csv. Issuer: ENGIE FY2025 results press release PDF (engie.com). ISINs registry-mapped.
