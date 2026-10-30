# QA results — Stage 1 (data sourcing), AI.PA @ 2026-10-30

## Block A — data sourcing

- [x] **Identity confirmed**: Air Liquide, Euronext Paris, ticker AI, EUR, FY-end Dec-31, ISIN FR0000120073, CAC-40 large cap.
- [x] **Financials tie to AR and BS balances**: FY2022–FY2025 sourced from official FY results press releases; TOTAL ASSETS = TOTAL EQUITY AND LIABILITIES each year (48,332.4/49,518.0/51,867.5/51,913.4). FY2021 from stockanalysis only — flagged `unavailable`/`unverified` where definitional; acceptable, recorded.
- [x] **Anomaly flags resolved**: 14 flags, all investigated and kept as reported (see anomaly_report.md); none normalized.
- [x] **Shares exclude treasury, checked vs report and exchange**: 636.47m current shares post Jun-2026 attribution (stockanalysis/Euronext); AR avg FY2025 576.79m and treasury shares -179.6m on BS consistent.
- [x] **Debt/cash reconciled to net debt**: borrowings 12,377.5 − cash 3,962.0 = net debt 8,415.5 exactly as AR; leases 1,259.4, pensions/provisions 2,421.9, NCI 733.3, equity affiliates 174.6 recorded separately for stage-2 bridge per sector_adjustments.
- [x] **Currency/units consistent**: all EUR millions; London-GBp issue n/a; interim values labelled.
- [x] **Every number sourced + dated in source_log.csv**: 130+ rows, `sourcelog.validate` clean (0 problems); sourced rows carry URL/file + page locator.

## Data-quality notes for later stages

1. Damodaran industry data: not needed at this stage; will come via `datasets.resolve` only (route confirmed).
2. Regressions vintage Jan-2026 (~10 months old) — already logged as Limitations item for stage 3.
3. FY2021 column is aggregator-only; if a stage-2 model needs AR-quality FY2021 balance items, fetch the FY2022 press release comparatives (~5 min).

## Block B — DCF (stage 2)

### Capital structure and earnings
- [x] Five-year market/book debt ratios aligned; book-debt proxy justified (IG bonds near par). No debt amount averaged with a percentage.
- [x] Debt stability assessed: FY22–25 stable, 2026 DIG Airgas step-up → unstable → **FCFF** chosen; FCFE cross-check skipped (standard mode, recorded).
- [x] Adjusted EBIT (OIR) and group NI reconciled to reported (non-recurring items excluded: −353.7m FY25); recurring exceptional costs assessed — provisions flows normal.
- [x] Trailing: no adjusted interim EBIT bridge available (PR lacks interim adjusted EBIT); annual FY2025 base used and disclosed. Jun-2026 debt step reflected in bridge discussion.
- [x] Group/parent scope: FCFF is group-wide; NCI removed once in bridge; parent shares used.
- [x] T_eff 25.24% (ops) vs T_marg 25% (financing/beta) separate and consistent.

### Reinvestment and growth
- [x] Capex assessed item-by-item: recurring PP&E+intangibles + recurring acquisitions (~250m/yr) inside NCE; DIG Airgas one-off excluded from recurring base (deal economics noted).
- [x] D&A consistent with adjusted earnings; no impairment double-add.
- [x] No R&D capitalization, no lease restatement; IFRS16 lease treatment reconciled (liabilities in debt, D&A in EBIT, repayments in CF).
- [x] NCE/NOPAT: company 38.8% (FY25), 34.9% (FY24) vs industry ~38.5%; selected 38% within range.
- [x] NWC: components reconciled (−0.58% FY25, −0.53% FY24), industry 16.07% weighted; course avg 7.74%.
- [x] Forecast NWC balances precede changes; floor max(Δ,0) applied incl. year n+1; floor non-binding (raw Δ all >0), PV cost €0 — reported.
- [x] FCFF signs/borrowing consistent; no repeated interest deduction.
- [x] ROE 13.1% / ROC 10.7% on beginning book capital; scope matched (group capital incl. NCI, cash excluded).
- [x] Growth evidence compared: fundamental 4.9%, historical ~8%, analyst ~5-6%, narrative positive → selected ~5%.
- [x] Three-stage test evaluated first; heuristic disclosed; two-stage transition justified (mature firm, g>stable).
- [x] Terminal g 3.0% ≤ Rf 3.38%; g < WACC in all computed cells (invalid cells labelled).
- [x] Year n+1 explicitly constructed (sales ×1.03, stable reinvestment 28%, floored ΔNWC); TV timing correct.

### Discount rates
- [x] Same Rf 3.38% (Bund, Germany Aaa, spread 0) in Ke and Kd; EUR nominal.
- [x] Bottom-up beta cash-corrected, 5 segments, weights=100%; relevered at market D/E. Regression beta 0.61 disclosed (index/window/methodology unavailable = data gap).
- [x] Geographic weights = 100% (Americas/EMEA/AsiaPac); regional proxies documented with limitations.
- [x] ERP/CRP/default spread separate; Jan-2026/Jul-2026 vintages, no hardcoded examples.
- [x] Base Ke additive (8.24%); beta-scaled 8.22% shown. Lambda not run (standard mode).
- [ ] External market Ke estimates: unavailable (no comparable public implied-Ke source found) — marked, not invented.
- [x] Rating A/A2 documented (S&P/Moody's/Scope pages); synthetic coverage 11.6 → Aaa as cross-check; company spread 0.78% used; a=0 sovereign incremental, justified.
- [x] WACC market weights sum to 1; no preferred/hybrids.

### Valuation and outputs
- [x] FCFF discounted at WACC, end-year, cumulative factors; TV at year 5 discounted correctly.
- [x] Bridge: cash, debt, NCI, associates, pensions/provisions each once; no debt double-subtraction.
- [x] Share count 636.47m (post-attribution, ex-treasury); EUR consistent; market cap computed independently.
- [x] TV share 85.7% disclosed and flagged >75%.
- [x] Low/base/high (58.1/81.4/113.4), WACC×g grid, driver ranking, implied-multiple gap discussion, convention impacts (NWC floor €0) shown.
- [x] Citations verified (AR PDFs, dataset files, rating pages); data gaps listed in dcf_decisions.md.
- [x] dcf_model.xlsx recalculated via library (dcf.py); library and workbook match by construction (same engine); supporting computation script in outputs.
- [x] dcf_model.xlsx, dcf_decisions.md, source_log.csv (validated), qa_results.md, dcf_summary.png all exist and reconcile.

**Unresolved**: external Ke comparison unavailable (marked); pension/provision bridge treatment conservative; NCI at book proxy. None blocking; label: base result stands, note -55% vs market is a stage-4 discussion item.
