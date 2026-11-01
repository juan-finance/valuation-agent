# Enel (ENEL.MI) comparables — 2026-10-30

PROVISIONAL: ownership/events/classification audit incomplete; human Spot_check pending; associates proxied by Long-Term Investments for the target only and NOT subtracted from peer EV (uniform EV-before-associates basis). No replacement-cost Tobin's Q; no sourced home-index PE (relative_pe unavailable). ISINs registry-mapped pending issuer-page verification. Endesa (ELE.MC) hard-excluded as ENEL's ~70%-owned subsidiary.

## Route, basis, scope
Single target, orchestrator layout `outputs/ENEL.MI_2026-10-30/relative/`. Route: `web_minimum` (uniform stockanalysis raw fields); `published_damodaran` regression route; standard mode; FY2025 earnings basis; comparison currency EUR; one price date 2026-10-30 (ECB FX snapshot cache/macro/2026-10-30.json). No group workbook; candidates from issuer-named competitors, sector_adjustments Tier-1 seeds and own research. Vendor extracts shared with the EDPR run's dated cache (EDPRpool_*) plus 5 new ENELpool_* fetches (NG, TRN, REE, SRG, IG) and 2 documented source failures (CEZ, REE-route fixed to bme/RED).

## Target profile
Integrated utility (bucket A): generation (incl. large renewables fleet via Enel Green Power), regulated grids in Italy/Spain/LatAm, retail; ~40% of ordinary EBITDA from grids (issuer segment table). EUR reporting = trading currency, Dec year-end. Net debt/EBITDA 3.1x (vendor basis), payout >100% of reported NI (dividend part-funded from retained earnings — flagged).

## Candidate pool and selection
Initial pool 33 + subsidiary evidence row: 13 Tier-1 integrated/regulated European utilities, 17 Tier-2 (renewable IPPs, grid operators, generators, World-relaxation candidates), 1 subsidiary row (ELE), plus CEZ (source unavailable/EM) and ORA (World-only). Rejected before scoring: ELE (subsidiary), CEZ (uniform source 404; MSCI EM anyway), ORA (World-only), AY/BLX/INE (no common 2026-10-30 price date). Europe step feasible at default caps: 14 in-band Tier-1/2 candidates (size band €9.25–924.6bn on target €92.5bn); CNA/A2A/REE/IG below band floor; smaller IPPs (ERG, ANE, SLR, GRE, SCATC, DRX) below band too. Selected 10 lowest scores: ENGI, EOAN, EDP, NG, SRG, SSE, TRN, ORSTED, VER, FORTUM — 8 Tier-1 + 2 Tier-2, all Europe-listed, no relaxation needed, no replacement after business-description review. Scores, winsorization (pool-only 5%/95%), weights and constraint logs in peer_selection.json / comparables_audit.xlsx. Iberdrola (higher growth profile, cap €148bn) and RWE scored above the selected set.

## Primary multiple and values
Bucket-A primary: **EV/EBITDA** (peer median 12.56x, n=10). Cross-checks: PE, PBV (ROE-scaled), EV/EBIT, EV/CF, PS, EV/Sales, EV/Assets. Headline uses uniform vendor FY2025 EBITDA (€20,311m) — see basis note below.

| Metric | p25 | median | p75 | EUR/share range |
|---|---|---|---|---|
| EV/EBITDA 12.56x × vendor EBITDA €20,311m | 10.47x | 12.56x | 15.48x | €13.50 – 17.79 – 23.77 |
| EV/EBITDA 12.56x × issuer reported EBITDA €22,073m (sensitivity) | – | – | – | ~€20.59 mid |
| EV/EBITDA 12.56x × issuer ordinary EBITDA €22,874m (sensitivity) | – | – | – | ~€21.48 mid |
| PE median 17.81x × NI to common €3,959m | 16.35x | 17.81x | 25.66x | €6.52 – 7.11 – 10.24 |
| PE × issuer group NI €4,225m (sensitivity) | – | – | – | ~€7.58 mid |
| PBV ROE-scaled 2.13x (unadjusted 2.29x) | – | 2.13x | – | €6.25 – 6.90 – 9.90 (scaled) |
| EV/EBIT 21.07x | 14.37x | 21.07x | 21.99x | €12.71 – 22.34 – 23.67 |
| EV/CF (reported CFO) 14.34x | 13.06x | 14.34x | 16.24x | €10.40 – 12.21 – 14.87 |
| EV/Assets 1.04x | 0.82x | 1.04x | 1.31x | €6.84 – 10.79 – 15.68 |
| PS 3.22x / EV/Sales scaled 3.21x | 0.92x | 3.22x | 4.04x | €6.52 – 7.11 – 10.24 / €13.50 – 17.79 – 23.77 |
| PEG | – | – | – | NM (target fundamental growth = 0; no per-share value) |

### EBITDA-basis note
Vendor EBITDA €20,311m is below issuer reported EBITDA €22,073m and ordinary EBITDA €22,874m (definition scope: vendor excludes items the issuer aggregates). Unlike EDPR there is no matching-claims mismatch of the same materiality, but the issuer-basis sensitivity (€20.6–21.5/share vs €17.8 vendor basis) is retained in sensitivities.csv. NI basis: vendor "Net Income to Common" €3,959m vs issuer Group net income €4,225m — the vendor deducts a further €266m "Preferred Dividends & Other" though Enel has no preferred; flagged, vendor basis kept for peer comparability, issuer basis in sensitivity (PE → €7.58).

### Payout >100% note
Declared FY2025 dividend €4,982m (€0.49/share, of which €0.215 funded from retained earnings) vs NI to common €3,959m → payout 1.26, and vendor paid-cash basis €6,060m → 1.53. Fundamental growth = ROE×(1−min(payout,1)) = 0 for ENEL — scoring weight for growth is carried at 0 with the pool rule documented; PEG and growth-scaled PE adjustment are unavailable on this basis.

## Fundamental comparison vs peer medians
ENEL vs selected peers: actual EV/EBITDA 8.43x vs peer median 12.56x; PE 23.4x vs 17.8x (vendor NI basis depressed by FY2025 writedowns); ROE 12.0% vs ~10%; net debt/EBITDA 3.15x vs ~4.3x (median of selected); EBITDA margin 25.6% vs ~34% (median); beta 0.84 vs ~0.6 median.

## Exclusions, relaxations, replacements
All in candidate_gates.csv. No relaxation invoked (Europe step feasible at default caps). No Tier-3 member. ORA restricted to World-only pool which was never reached.

## Limitations
Vendor FY bases (Dec-25 for all selected). Payout>100% for ENGI/ENEL/FORTUM (fiscal-basis mismatch, retained). Consensus growth unavailable on uniform route → fundamental ROE×retention used for scoring (pool rule applied). Spot_check pending. Benchmark: Damodaran Europe utility EV/EBITDA median not registered in data library — >50% gap check unavailable; EUROPE published EV/EBITDA equation predicts 19.4x for ENEL's inputs as the only cross-reference (above peer median 12.6x — market-wide equation, recorded not resolved).

## Sources
Per-row `field: URL (accessed 2026-11-01)` in candidate_gates.csv and source_log.csv. Issuer: Enel FY2025 results press release PDF (enel.com). ISINs registry-mapped.
