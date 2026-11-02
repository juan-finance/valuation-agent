# SU.PA comparables report (relative-only, 2026-10-30)

Academic analysis for coursework only; not investment advice. Figures are from public web sources accessed 2026-10-30/31 and cross-checked against Schneider Electric FY2025 results (26 Feb 2026).

## Peer set
10 peers, all European-listed, 8 tiers 1-2 + 2 tier 3 (at the cap). Selection by comparables.select_peers with
min_tier_1_2=6, max_tier_3=2, min_europe=5 (procedure section 3). Peers: SAND (Sandvik), LR (Legrand), ATCO.A (Atlas Copco A), EPI.A (Epiroc A), METSO (Metso), HLMA (Halma), ALFA (Alfa Laval), ENR (Siemens Energy), WRT1V (Wartsila), PRY (Prysmian).

Candidate universe: shared dated stockanalysis extracts of all prior runs (104 European rows screened). SU's
~EUR 134bn market cap sets the 0.1-10x size band at EUR 13.4bn-1,337bn, which excludes most mid-cap electrical
names (NEX, NKT, IMI, SPX, SKF.B, ANDR, G1A, SUN, WEIR, ROR...). Restructuring exclusions per the FY2024-25 window:
ABBN (Robotics disposal + Gamesa), SIE (Altair), NEX (divestments), SMIN, SKF.B, GEV. Tier 3 was required because
only 9 tier-1/2 candidates survived all filters.

## Multiples (median, n valid >= 6)
| Multiple | n | Median | P25 | P75 | Value/share median |
|---|---|---|---|---|---|
| pe | 10 | 31.40 | 27.34 | 32.77 | EUR 232.63 |
| pbv | 10 | 5.24 | 5.04 | 6.78 | EUR 225.02 |
| ps | 10 | 3.43 | 2.68 | 4.28 | EUR 244.55 |
| ev_ebit | 9 | 23.06 | 20.75 | 23.77 | EUR 257.81 |
| ev_ebitda | 9 | 18.02 | 16.96 | 18.93 | EUR 226.16 |
| ev_cf | 9 | 24.48 | 17.82 | 26.20 | n/a |
| ev_sales | 9 | 3.45 | 2.65 | 4.07 | EUR 218.22 |
| ev_assets | 9 | 2.19 | 1.83 | 2.88 | n/a |

Growth-adjusted P/E median 23.43x (scaled_multiple, driver 100 x growth, target fundamental growth
7.21%). ROE-adjusted P/BV median 4.84x. Positive extremes retained (ENR P/E 76.8).

## Limitations
- Peers and tiers are judgement (agent). Index membership and ISIN checks not performed (IEUR proxy membership only).
- Peer data from stockanalysis dated extracts, not verified against filings. Growth is fundamental (ROE x retention), no consensus.
- EV multiples have n=9 (HLMA lacks EV in the source); EV basis is before associates.
- Tier-3 peers (Sandvik, Epiroc) are mining equipment: allowed under the cap because tier-1/2 supply 9 < 10; documented shortfall driver is the target's size band.
- Payout scoring basis is CF dividends paid / NI (0.526); the published-route payout input is declared DPS/EPS (0.567).
