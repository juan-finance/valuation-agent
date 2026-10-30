# Comparables — Air Liquide (AI.PA), valuation date 2026-10-30
Route: published_damodaran (regression side separate). Mode: standard. Single target.

## Profile and peer selection
Industrial & medical gases, Euronext Paris, market cap ~€115.1bn, price ~€181. Primary multiple for industrial gases = PE (sector_adjustments); cross-check EV/EBIT and EV/EBITDA.

Funnel: 30 cached candidates → 3 Tier-1 (LIN, APD, Nippon Sanso via world expansion) + 26 Tier-2 Europe. Hard exclusions: NSIS.B (Novonesis merger Jan-2024, comparison-period distortion), SYENS (Solvay spinoff Dec-2023), 16 names outside the relaxed 0.05–20× size band or <€1bn (incl. SOL 5.4bn — the European gases pure play failed the band; documented). 14 eligible → scored on growth 30 (fundamental g=ROE×(1−payout), web route), beta 15, ND/EBITDA 10, ROE 10, EBITDA margin 10, payout 7.5, capex/sales 7.5, ln(size) 10; pool winsorized 5/95; L2 weighted distance.

## Selected 10 (exactly 10, all T1–T2, 7 Europe-listed)
LIN (US, gases), APD (US, gases), 4091 (JP, gases, world expansion), GIVN (CHF), BAS (DE), ALFA (SE), EMSN (CH), SY1 (DE), YAR (NO), DSFIR (NL).
Constraints: T1-2 = 10/10 (≥8 required); Europe-listed = 7 (≥5); T3 = 0. World expansion invoked only for LIN/APD/4091 (Tier 1 cannot otherwise reach the peer count); relaxed size band invoked for YAR (9.7bn), CRDA and SY1 already in relaxed band — flagged `relaxed` in comparables.csv.

## Multiples (min_valid=6, see multiples_summary.csv)
PE: n=8 (APD, DSFIR have loss/n.a. PE), median 30.9, P25 15.0, P75 41.0. EV/EBITDA n=10 median 18.7. EV/EBIT n=10 median 27.0. PBV n=10 median 2.86. PS n=10 median 2.83.

## Value
- PE median 30.9 × NI parent 3,517.9 → €170.8/sh (raw).
- Growth-scaled PE (scaled_multiple, fundamental g target 5.28% vs peers, min_valid=6): 16.4 → €90.7/sh. Wide raw-vs-adjusted gap driven by LIN/GIVN/EMSN/SY1 high-PE, high-growth names.
- EV/EBIT 27.0 → equity €128.1bn → €201.2/sh. EV/EBITDA 18.7 → €199.4/sh.
Market price €180.9 sits between raw peer median and scaled-PE. Point estimate reported as a range €91–201, central ~€171 raw / €91 growth-adjusted.

## Sensitivities & limitations
APD PE unavailable (FY Sep basis, NI≈0); DSFIR PE n/a (negative NI) — min_valid satisfied. Peer multiples are single-source (stockanalysis, accessed 2026-10-30); Spot_check sheet in comparables_audit.xlsx recomputes EV for LIN/GIVN/YAR (diff ≤0.2%). Manual spot-check review pending — flagged, not auto-approved.

## Sources
stockanalysis.com statistics pages (cached 2026-10-30, per-peer URLs in source_log); Air Liquide FY2025 AR PR PDFs; ECB FX 2026-10-30; iShares IEUR universe.
