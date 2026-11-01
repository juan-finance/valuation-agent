# Market cache manifest — valuation date 2026-10-30

## BP.L-only authorized top-up — 2026-11-01
- Added United Kingdom Aa3, default spread 0.48%, CRP 0.74%, ERP 4.94%, from resolved ctryprem_global_2026-07.
- GBP: BoE IUDMNPY 10-year nominal par yield 5.3087%, observation 2026-10-28 (latest returned through Oct 30); default-free 4.8287% after UK spread. Oct 29/30 observations not returned; not a same-day yield. Exact official URL/access date in macro snapshot and topup_BP.L.json.
- UK published EUROPE PE/PBV/EV-EBITDA equations resolved. Existing integrity findings reused; vintage and pending human-review limitations unchanged.
- Reproducible script topup_bp.py asserts all existing countries, currencies and FX unchanged. No universe rebuild, candidate collection, or other-country changes. Elapsed: 4 minutes.

Built by `.agents/skills/valuation-0-market-refresh/SKILL.md` on 2026-10-30.
Route: `published_damodaran` (standing approvals). Scope: AI.PA pilot. Mode: standard.

## Data library check (step 0.1)
All 7 registered datasets verified (`datasets check`), resolved for France at 2026-10-30:

| dataset_id | family | match | note |
|---|---|---|---|
| beta_europe_2026-01 | beta | exact EUROPE | as-of 2026-01-05 |
| capex_europe_2026-01 | capex | exact EUROPE | warn: Steel/Railroads Net CapEx/EBIT(1-t) extreme — use other ratios for those industries |
| ctryprem_global_2026-07 | ctryprem | exact GLOBAL | as-of 2026-07-09 |
| dbtfund_europe_2026-01 | dbtfund | exact EUROPE | stage 2 |
| wcdata_europe_2026-01 | wcdata | exact EUROPE | stage 2 |
| ratings_global_2026-01 | ratings | **fallback** GLOBAL (no EUROPE vintage) | user confirmed acceptable 2026-10-30 |
| regressions_multi_2026-01 | regressions | exact EUROPE | vintage ~10 months old vs valuation date -> Limitations flag |

## Macro snapshot (step 0.2)
`cache/macro/2026-10-30.json`: Bund 10y 3.38% (Bundesbank BBSIS daily, obs 2026-10-30), mature ERP 4.20%, France Aa3 spread 0.48% / CRP 0.74%, Germany Aaa 0, ECB FX per-EUR rates obs 2026-10-30.

## Published-route equations (step 0.3)
Resolved `equation_for('FR', dep, 2026-10-30)` on regressions_multi_2026-01: **found** PE, PBV, EV/EBITDA (primary), PEG, EV/IC, EV/Sales (supplementary, full mode only). PS has no published equation (documented limitation). No equation blocks.

check_dataset findings (regressions_multi_2026-01): warnings — GLOBAL PEG ln(g_eps) +0.48 sign anomaly, GLOBAL PBV beta sign anomaly, EM EV/EBITDA roic sign anomaly, identical t-stats in GLOBAL PEG; units DFR/tax resolved by `damodaran_dfr_tax_units: decimal` (standing approvals, Facebook-example basis); no residual SE published. None affects the EUROPE equations used for AI.PA; EUROPE equations unaffected.

## Universe (step 0.3)
- Source: iShares Core MSCI Europe ETF (IEUR) holdings CSV, `latest-holdings.csv`, fund holdings dated Oct 29 2026 (latest published), accessed 2026-10-30. **Proxy**: tracks MSCI Europe IMI (large+mid+small cap); membership is a fund-holding proxy, not the index file — labelled proxy coverage.
- Raw file: `universe_source_ishares_ieur.csv` (1023 rows). Parsed: `universe.csv` — 1010 equity rows, 853 kept, 157 flagged `sector_financials`, 13 dropped (non-equity/no-ticker: futures, cash, rights, CVR).
- Coverage label: includes small caps (IMI); candidates still need index/ISIN verification per procedure in stage 3.

## AI.PA candidate cache (stage 3B pre-fetch)
- `candidates_AI.PA.csv`: 30 candidates — Tier 1 industrial gases: SOL SpA, Linde, Air Products, Nippon Sanso (world_expansion flag, developed-market only per relaxation order); Tier 2 chemicals/industrials Europe (26). Alfa Laval flagged as a batch-universe target.
- Fetched via `CachedFetcher` into `cache/web/2026-10-30/stockanalysis.com/` (gitignored raw cache): 180 pages (overview, statistics, income statement, balance sheet, cash flow, dividend) — all 200 OK. Uniform web source per `data_route_stage3: web_minimum`; LIN/APD use `/stocks/` slug form.
- Screening, scoring and selection of the final 10 happen in stage 3B; nothing here is a peer verdict.

## Timings
- Steps 0.1-0.3 total: ~25 min (session start 20:28 CET).
- run_log row: `AI.PA_2026-10-30,stage0_market,done,~25`.

## Status / limitations
- Spot_check: pending (no human review claimed).
- ratings fallback to GLOBAL recorded; regressions vintage flag recorded.
- MSCI World membership list NOT fetched (only needed if candidate relaxation reaches step (a)); Japan candidate Nippon Sanso fetched but needs World-membership verification if used.

## MT.AS-only top-up — 2026-10-31
- User changed companies_in_scope to MT.AS only; existing AI.PA assets, universe list, FX and EUR yield preserved. No candidate data collected in stage 0.
- Country Luxembourg, reporting currency USD. Added Luxembourg Aaa/default spread 0/CRP 0 and USD benchmark issuer United States Aa1/default spread 0.22%/CRP 0.22%, from registered ctryprem_global_2026-07. These are not substitutes for the company's revenue-weighted CRP.
- Added Treasury 10-year par yield **4.94%**, observation 2026-10-30, accessed 2026-10-31 (official Treasury CSV; exact URL in macro snapshot). Default-free USD Rf **4.72%** after subtracting benchmark-issuer spread 0.22%. FRED's then-latest observation was Oct 29 (4.98%); not used because same-day Treasury data is available.
- Country-specific resolutions and EUROPE PE/PBV/EV-EBITDA equations saved in topup_MT.AS.json. Existing completed library integrity checks reused; no library dataset redownloaded. Ratings GLOBAL fallback is representative as a common corporate coverage-to-spread cross-check, not as a European industry debt ratio.
- Existing regression warnings/Jan-2026 vintage limitations and Spot_check pending status remain unchanged. No universe rebuild or own-estimation work.
- Reproducible top-up: PYTHONPATH=src python cache/market/2026-10-30/topup_mt.py; assertions verify old EUR, ERP, FX and other snapshot fields unchanged.

## EQNR.OL-only top-up — 2026-11-01
- Norway was the only missing country for EQNR.OL (reports USD — already in risk_free; trades NOK — already in ECB FX 2026-10-30). Added Norway Aaa, default spread 0, CRP 0, total ERP 4.20% from registered ctryprem_global_2026-07. Stage 3 does not discount, so no NOK risk-free instrument was required.
- All datasets resolve for Norway: EUROPE exact for beta/capex/dbtfund/wcdata/regressions/industry benchmarks; ratings GLOBAL fallback unchanged (same warning as prior top-ups). EUROPE PE/PBV/EV-EBITDA equations resolved in topup_EQNR.OL.json.
- Reproducible script topup_eqnr.py asserts all existing countries, currencies, FX and snapshot fields unchanged. No universe rebuild, candidate collection, or other-country changes.

## IBE.MC-only top-up — 2026-11-01
- Spain was the only missing country for IBE.MC (reports and trades EUR — Bund 10y risk-free and ECB FX already in the snapshot). Added Spain A3, default spread 0.95%, CRP 1.48%, total ERP 5.68% from registered ctryprem_global_2026-07. Stage 3 does not discount, so no additional instrument was required.
- All datasets resolve for Spain: EUROPE exact for beta/capex/dbtfund/wcdata/regressions/pbv_industry/evebitda_industry; ratings GLOBAL fallback unchanged (same warning as prior top-ups). EUROPE PE/PBV/EV-EBITDA equations resolved in topup_IBE.MC.json.
- Reproducible script topup_ibe.py asserts all existing countries, currencies, FX and snapshot fields unchanged. No universe rebuild, candidate collection, or other-country changes.
