# Iberdrola (IBE.MC) comparables — 2026-10-30

PROVISIONAL: ownership/events/classification audit incomplete; human Spot_check pending; associates proxied by Long-Term Investments for the target only and NOT subtracted from peer EV (uniform EV-before-associates basis). No replacement-cost Tobin's Q; no sourced home-index PE (relative_pe unavailable). ISINs registry-mapped pending issuer-page verification. Endesa (ELE.MC) hard-excluded as ~70%-owned subsidiary of peer candidate ENEL (double-counting economics).

## Route, basis, scope
Single target, orchestrator layout `outputs/IBE.MC_2026-10-30/relative/`. Route: `web_minimum` (uniform stockanalysis raw fields); `published_damodaran` regression route; standard mode; FY2025 earnings basis; comparison currency EUR; one price date 2026-10-30 (ECB FX snapshot cache/macro/2026-10-30.json). No group workbook; candidates from issuer-named competitors, sector_adjustments Tier-1 seeds and own research. All vendor extracts reused from the dated candidate cache (EDPRpool_* / ENELpool_* — shared market-data rule); CEZ unavailable (source 404, MSCI EM anyway).

## Target profile
Integrated utility (bucket A): regulated networks (Spain/UK/US/Brazil ~60% of adjusted EBITDA), renewables and conventional generation, retail. EUR reporting = trading currency, Dec year-end. Net debt/EBITDA 3.79x (vendor basis), declared payout ~0.75 on a scrip dividend (CF-paid basis 0.21 — flagged, not used).

## Candidate pool and selection
Initial pool 33 + subsidiary evidence row: 13 Tier-1 integrated/regulated European utilities, 19 Tier-2 (renewable IPPs, grid operators, generators, World-relaxation candidates), 1 subsidiary row (ELE), plus CEZ (source unavailable/EM) and ORA (World-only). Rejected before scoring: ELE (subsidiary of candidate ENEL), CEZ (uniform source 404; MSCI EM anyway), ORA (World-only), AY/BLX/INE (no common 2026-10-30 price date). Europe step feasible at default caps: size band €14.79–1,479.4bn on target €147.9bn; CNA/A2A/REE/IG/ERG/ANE/SLR/GRE/SCATC/DRX below band floor. Selected 10 lowest scores: SSE, RWE, NTGY, NG, EDP, EOAN, TRN, SRG, VER, ENGI — 8 Tier-1 + 2 Tier-2, all Europe-listed, no relaxation needed, no replacement after business-description review. Scores, winsorization (pool-only 5%/95%), weights and constraint logs in peer_selection.json / comparables_audit.xlsx. Enel, Iberdrola's closest listed comparator, scored 11th of the eligible pool (distance to target) and just missed selection; FORTUM and ORSTED also above the selected set.

## Primary multiple and values
Bucket-A primary: **EV/EBITDA** (peer median 12.56x, n=10). Cross-checks: PE, PBV (ROE-scaled), EV/EBIT, EV/CF, PS, EV/Sales, EV/Assets. Headline uses uniform vendor FY2025 EBITDA (€14,700m) — see basis note below.

| Metric | p25 | median | p75 | EUR/share range |
|---|---|---|---|---|
| EV/EBITDA 12.56x × vendor EBITDA €14,700m | 10.47x | 12.56x | 14.31x | €12.71 – 17.32 – 21.18 |
| EV/EBITDA × issuer adjusted EBITDA €15,684m (sensitivity) | – | – | – | ~€19.18 mid |
| EV/EBITDA × issuer reported EBITDA €16,592m (sensitivity) | – | – | – | ~€20.89 mid |
| PE median 17.11x × NI to common €6,055m | 15.65x | 17.11x | 20.83x | ~€14.21 – 15.53 – 18.91 (raw) |
| PE × issuer reported net profit €6,285m (sensitivity) | – | – | – | ~€16.12 mid |
| PBV ROE-scaled 2.12x (unadjusted 2.29x) | 1.74x | 2.12x | 2.54x | €14.83 – 15.95 – 17.81 (scaled) |
| EV/EBIT 19.66x | 14.37x | 19.66x | 21.99x | €11.14 – 19.06 – 22.55 |
| EV/CF (reported CFO) 13.77x | 12.57x | 13.77x | 14.36x | €11.56 – 13.65 – 14.69 |
| EV/Assets 1.04x | 0.82x | 1.04x | 1.09x | €9.42 – 14.70 – 16.01 |
| PS margin-scaled 2.35x (unadjusted 2.65x) | 1.32x | 2.35x | 3.36x | €14.20 – 15.53 – 18.91 (scaled); raw ~€17.52 mid |
| PEG median 5.57 | – | – | – | growth-scaled PE 54.8x — distorted by near-zero peer growth; flagged, not a headline |

### EBITDA-basis note
Vendor EBITDA €14,700m is below issuer adjusted EBITDA €15,684m and reported EBITDA €16,592m (vendor excludes items the issuer aggregates; ~11–13% gap). The issuer-basis sensitivity (€19.2–20.9/share vs €17.3 vendor basis) is retained in sensitivities.csv. NI basis: vendor "Net Income to Common" €6,055m vs issuer reported net profit €6,285m — the vendor deducts €230m "Preferred Dividends & Other Adjustments" which corresponds to Iberdrola's perpetual subordinated-note (hybrid) coupon — a real claim on common, kept and flagged; adjusted NI €6,749m in sensitivity (PE → €17.31).

### Scrip-dividend note
Iberdrola's "Retribución Flexible" means most shareholders take shares: CF dividends paid €1,275m (payout 0.21) understates the declared dividend (~€4,543m = DPS €0.68 × 6,681m shares → payout 0.75). Declared basis used for the published-route payout input and scoring growth; scrip issuance of €5,107m common stock documented.

## Fundamental comparison vs peer medians
IBE vs selected peers: actual EV/EBITDA 14.76x vs peer median 12.56x; PE 24.4x vs 17.1x (raw); PBV 2.95x vs 2.29x; fundamental growth 9.8% vs ~3.1%; ROE 12.1% vs ~10.6%; net debt/EBITDA 3.79x vs ~5.03x; EBITDA margin 33.4% vs ~26.7%; beta 0.45 vs ~0.57. IBE trades at a premium to its selected peers on every headline multiple — consistent with its higher growth/ROE and lower leverage profile.

## Exclusions, relaxations, replacements
All in candidate_gates.csv. No relaxation invoked (Europe step feasible at default caps). No Tier-3 member. ORA restricted to World-only pool which was never reached.

## Limitations
Vendor FY bases (Dec-25 for all selected). Consensus growth unavailable on uniform route → fundamental ROE×retention used for scoring (pool rule applied). Spot_check pending. Benchmark: Damodaran Europe utility EV/EBITDA median not registered in data library — >50% gap check unavailable; EUROPE published EV/EBITDA equation predicts 19.7x for IBE's inputs as the only cross-reference (above peer median 12.6x — market-wide equation, recorded not resolved).

## Sources
Per-row `field: URL (accessed 2026-11-01)` in candidate_gates.csv and source_log.csv. Issuer: Iberdrola FY2025 results (CNMV filing) and press release. ISINs registry-mapped.
