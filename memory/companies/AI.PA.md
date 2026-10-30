# AI.PA — L'Air Liquide S.A.

Company facts (verify against `valid_until`; last update 2026-10-30, confidence high unless noted):

- Euronext Paris, ticker AI, ISIN FR0000120073, EUR, FY-end Dec-31. CAC-40. Bucket D industrials.
- Shares: 636.47m outstanding post Jun-8-2026 1:10 free-share attribution (avg FY2025: 576.79m). Per-share figures pre/post Jun-2026 differ by factor 1.1 — always state basis. (confidence high)
- FY2025: revenue 26,940; OIR 5,581.6; IFRS op. income 5,278.7; net profit (Group) 3,517.9; EPS 6.10; DPS proposed 3.70; net debt 8,415.5; net D/E 31.2%; ROCE 10.7%. (AR FY2025 PR)
- 5Y beta 0.61 (stockanalysis); market cap ~€115bn @2026-10-30. (valid_until: next stage)
- Jun-2026 interim (stockanalysis): cash 2,061; total debt 17,259; net debt 15,198 — large 2026 bond issuance; re-verify vs H1-2026 report if used. (confidence medium)
- Definitional gotcha: stockanalysis "Operating Income" ≠ company OIR and ≠ IFRS operating income (5,201 vs 5,581.6 vs 5,278.7 for FY2025). Use AR series; OIR is the company's recurring metric.
- WC swings sign-flip near zero; capex+M&A lumpy; use multi-year averages in stage 2. Buybacks discretionary (paused 2025); dividends are the stable payout (payout ~63% per AR).
- FY2022–2025 figures AR-sourced and cross-checked vs stockanalysis (ties). FY2021 column aggregator-only — if needed, pull FY2022 PR comparatives.
- Best source: FY results press-release PDFs on airliquide.com (full consolidated IS/BS/CF, ~p.36-39). Fetch with plain or Chrome UA; needs `/sites/airliquide.com/files/YYYY-MM/...pdf`.

## Stage 2 (DCF, 2026-10-30)
- Model: FCFF two-stage (FCFE rejected — debt unstable after DIG Airgas acquisition step-up: interim net debt €15.2bn vs €8.4bn FY25). Ratings: S&P A / Moody's A2 / Scope A, stable.
- Segment→industry beta map: LI→Chemical (Basic) 0.50; IM→Chemical (Specialty) 1.01; Healthcare→Healthcare Products 1.13; Electronics→Electronics (General) 1.04; E&T→Engineering/Construction 0.80. βU 0.891 → βL 0.970 (vs regression beta 0.61 — big gap, bottom-up preferred).
- Ke 8.24% / WACC 7.70% / Kd 4.16%. OIR margin 20.7%, sales +4%, NCE/NOPAT 38%, r_NWC 7.74% (course avg forces €2.3bn year-1 WC build).
- Result €81.4/sh vs ~€181 (−55%); TV share 85.7%; range 58–113. Bridge: −debt+leases 13,637 −NCI 733 −pensions/prov 2,422 +cash 3,962 +assoc 175.
- Gotchas: NWC/Sales slightly negative (−0.58%) — course avg dominates forecast; DIG Airgas closes 2026 — keep interim debt in mind for stage 4 equity story.

## Stage 3 relative (2026-10-30, published_damodaran)
- Peers (10, all T1-2): LIN, APD, 4091 (world expansion), GIVN, BAS, ALFA, EMSN, SY1, YAR, DSFIR. SOL excluded: €5.4bn < relaxed band floor €5.75bn. Restructuring exclusions: NSIS.B, SYENS.
- Comparables: PE median 30.9 → €171/sh; growth-scaled PE 16.4 → €91/sh; EV/EBIT 27.0 → €201; EV/EBITDA 18.7 → €199. APD/DSFIR no valid PE.
- Regression (EUROPE Jan-2026, decimals): PE 19.14 → €105.8; PBV 2.36 → €97.3; EV/EBITDA 19.73 → €211.6. Inputs β0.612, g_eps 5.28% (fundamental substituted), payout 62.25%, ROE 13.97%, g_rev 4.0%, dfr 0.130, tax 25.82%, ROIC 9.30%.
- Published-route `predict` unit policy = 'as_published_note' (decimal). RunState needs the .json path.

## Stage 4 recommendation (2026-10-30)
- Sell, fair value €80/110/170, 12-m target €110 vs market €180.9 (−39%). Synthesis weighted to DCF + growth-scaled PE (accounting consistency), stated ex ante.
- What the market may be mispricing: margin durability + implied ~5% Ke; consensus "Strong Buy" target €200.29 (stockanalysis aggregator, single source).
- Open: Spot_check human review pending; FY2021 aggregator-only; external Ke unavailable.
