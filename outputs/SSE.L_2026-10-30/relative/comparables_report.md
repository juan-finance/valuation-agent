# SSE (SSE.L) comparables — 2026-10-30

PROVISIONAL: ownership/events/classification audit incomplete; human Spot_check pending; associates proxied by Long-Term Investments for the target only and NOT subtracted from peer EV (uniform EV-before-associates basis). No replacement-cost Tobin's Q; no sourced home-index PE (relative_pe unavailable). ISINs registry-mapped pending issuer-page verification. Endesa (ELE.MC) hard-excluded as ~70%-owned subsidiary of peer candidate ENEL (double-counting economics).

## Route, basis, scope
Single target, orchestrator layout `outputs/SSE.L_2026-10-30/relative/`. Route: `web_minimum` (uniform stockanalysis raw fields); `published_damodaran` regression route; standard mode; FY2025 earnings basis (SSE FY ends 31 March — Mar-2025 used as FY2025, not calendarized, flagged); comparison currency GBP (target reporting = trading currency; quote in pence, converted at comp.pence_to_pounds); one price date 2026-10-30 (ECB FX snapshot cache/macro/2026-10-30.json, GBP 0.8338/EUR). No group workbook; candidates from issuer-named competitors, sector_adjustments Tier-1 seeds and own research. All vendor extracts reused from the dated candidate cache (EDPRpool_* / ENELpool_* — shared market-data rule); CEZ unavailable (source 404, MSCI EM anyway).

## Target profile
Integrated UK electricity utility (bucket A): regulated networks (SSEN Transmission ~£7.2bn and Distribution ~£5.7bn RAV, 100% basis), renewables (onshore/offshore wind, hydro), thermal/flexible generation, energy customer solutions. GBP reporting = trading currency, March year-end. Net debt/EBITDA 3.38x (vendor basis incl. hybrid-as-debt), declared payout ~0.60 (CF-paid basis 0.40 underweights final-dividend timing — flagged). 2026 equity raise increased shares to ~1.21bn (+7.1% QoQ) — market value uses current count.

## Candidate pool and selection
Initial pool 33 + subsidiary evidence row: 13 Tier-1 integrated/regulated European utilities, 19 Tier-2 (renewable IPPs, grid operators, generators, World-relaxation candidates), 1 subsidiary row (ELE), plus CEZ (source unavailable/EM) and ORA (World-only). Rejected before scoring: ELE (subsidiary of candidate ENEL), CEZ (uniform source 404; MSCI EM anyway), ORA (World-only), AY/BLX/INE (no common 2026-10-30 price date). Europe step feasible at default caps: size band €3.80–380bn on target €38.0bn; ERG/SLR/GRE/SCATC/DRX below band floor. Selected 10 lowest scores: **RWE, EDP, Iberdrola, Acciona Energia, National Grid, A2A, Naturgy, E.ON, Ørsted, Terna** — 7 Tier-1 + 3 Tier-2, all Europe-listed, no relaxation needed, no replacement after business-description review. Scores, winsorization (pool-only 5%/95%), weights and constraint logs in peer_selection.json / comparables_audit.xlsx. ENEL, ENGIE, FORTUM, EDP Renováveis, CNA, SRG, VER scored above the selected set and were not needed.

## Primary multiple and values
Bucket-A primary: **EV/EBITDA** (peer median 11.78x, n=10). Cross-checks: PE (growth-scaled), PBV (ROE-scaled), EV/EBIT, EV/CF, PS, EV/Sales, EV/Assets. Headline uses uniform vendor FY2025 EBITDA (£2,850m) — see basis note below.

| Metric | p25 | median | p75 | GBP/share range |
|---|---|---|---|---|
| EV/EBITDA 11.78x × vendor EBITDA £2,850m | 9.12x | 11.78x | 14.33x | £13.01 – 19.28 – 25.27 |
| EV/EBITDA × issuer reported EBITDA £2,738m (sensitivity) | – | – | – | ~£18.19 mid |
| EV/EBITDA × issuer adjusted EBITDA £3,349m (sensitivity) | – | – | – | ~£24.14 mid |
| PE median 17.81x × NI to common £1,189m | 13.19x | 17.81x | 23.76x | £12.96 – 17.50 – 23.35 (raw) |
| PE growth-scaled 23.98x (g_eps fundamental 6.1%) | – | – | – | £9.60 – 23.57 – 36.29 (scaled; distorted by Orsted outlier growth — flagged) |
| PBV ROE-scaled 1.81x (unadjusted 1.72x) | 1.25x | 1.81x | 2.54x | £13.03 – 18.03 – 23.03 (scaled) |
| EV/EBIT 20.23x | 13.64x | 20.23x | 22.06x | £16.89 – 29.14 – 32.55 |
| EV/CF (reported CFO) 12.81x | 10.51x | 12.81x | 15.62x | £13.05 – 17.76 – 23.51 |
| EV/Assets 0.82x | 0.68x | 0.82x | 1.06x | £8.70 – 12.17 – 18.21 |
| PS margin-scaled 2.09x (unadjusted 1.98x) | 1.32x | 2.09x | 3.11x | £12.96 – 17.50 – 23.35 (scaled); raw £16.57 mid |
| EV/Sales margin-scaled 3.31x | 2.34x | 3.31x | 4.54x | £13.01 – 19.28 – 25.27 (scaled); raw £17.16 mid |
| PEG median 3.92 | – | – | – | not a headline (near-zero peer growth distortions; flagged) |

### EBITDA-basis note
Vendor EBITDA £2,850m sits between issuer reported EBITDA £2,738.3m and adjusted EBITDA £3,349.3m (definition scope; ~4% above reported). The issuer-basis sensitivity (£18.19–24.14/share vs £19.28 vendor basis) is retained in sensitivities.csv. Vendor EBIT £2,250m = EBITDA − D&A For EBITDA and is +14.7% above issuer reported operating profit £1,962.2m (>10% flag; issuer adjusted operating profit £2,419.2m recorded as normalized alternative). NI basis ties issuer reported attributable profit £1,189.4m exactly (after NCI £69.8m and hybrid coupon £73.7m); adjusted attributable £1,768.1m in sensitivity (PE → £26.02).

### Dividend and hybrid notes
Declared FY2025 dividend = DPS 64.2p × 1,106.3m shares in issue ≈ £710m → payout 0.597. CF dividends paid £475.8m (payout 0.40) underweights the final dividend timing; declared basis used for the published-route payout input and is recorded in flags. SSE's equity-accounted hybrid capital (£73.7m coupon to "other equity holders") appears inside vendor "Total Debt" (£10,712m net £9,621m vs issuer reported net debt £9,513.9m, adjusted net debt + hybrid capital £10,186.7m): the uniform EV bridge keeps vendor Total Debt across peers and target; disclosed, not harmonized.

## Fundamental comparison vs peer medians
SSE vs selected peers: actual EV/EBITDA 14.72x vs peer median 11.78x; PE 26.65x vs 17.81x (raw); PBV 2.63x vs 1.72x; fundamental growth 6.1% vs ~4.0%; ROE 10.2% vs ~10.3%; net debt/EBITDA 3.38x vs ~4.2x; EBITDA margin 28.1% vs ~26%; beta 0.53 vs ~0.57. SSE trades at a premium to its selected peers on every headline multiple — a regulated-RAV growth premium consistent with its lower leverage and high capex/sales (26.5%).

## Benchmark check
Damodaran Europe "Utility (General)" EV/EBITDA industry statistic ~11.06 (aggregate, dataset evebitda_industry_europe_2026-01, Jan-2026) vs selected-peer median 11.78 → +6.5% gap, below the >50% investigation trigger. Caveat: industry statistic is an aggregate, not a peer-set median; flagged per procedure.

## Exclusions, relaxations, replacements
All in candidate_gates.csv. No relaxation invoked (Europe step feasible at default caps). No Tier-3 member. ORA restricted to World-only pool which was never reached.

## Limitations
Mixed fiscal bases: SSE year ended Mar-2025 vs Dec-2025 for most peers (not calendarized — flagged). Consensus growth unavailable on uniform route → fundamental ROE×retention used for scoring (pool rule applied); SSE consensus (15.19% EPS 3Y) exists but pool uniform basis kept. Spot_check pending. Peer set is 3 Tier-2 members (ANE, ORSTED, TRN) — allowed (cap applies to Tier-3 only) but the renewables/grid mix differs from SSE's regulated-RAV core; business-description review accepted them as adjacent-economics members.

## Sources
Per-row `field: URL (accessed 2026-11-02)` in candidate_gates.csv and source_log.csv. Issuer: SSE FY2024/25 Preliminary Results (LSE RNS 4968J + sse.com statement PDF). ISINs registry-mapped.
