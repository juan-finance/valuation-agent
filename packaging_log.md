# packaging_log.md — Relative valuation packaging, 20 SPIF companies

Valuation date 30-Oct-2026 · packaged 2026-11-02 · source repository `valuation-agent-relative-valuation.zip` (single snapshot; older 7/10/2-company ZIPs not used).

**Scope:** packaging only. No valuation rerun, no peer reselection, no change to weights, primary multiples, adjusted conventions, published equations, reported results or conclusions. No Buy/Hold/Sell. No DCF value imported (B22/B23 blank). **Successful packaging is not final valuation verification:** every run remains PROVISIONAL with human Spot_check pending.

## 1. Deliverables
- 20 × `RV_<TICKER>.xlsx` (13 sheets, identical order and PPT_Link positions)
- 20 × `RV_<TICKER>.pdf` (10 sections + identical one-page methodology appendix)
- `RV_All_Companies_Summary.xlsx` (README, Summary, Flags, PPT_Snapshots)
- `packaging_log.md` (this file)

## 2. Global decisions
- **Earnings period (user request 2-Nov-2026):** RV stays on FY2025 reported figures for target and peers; justification written into every workbook (QA_Flags T01) and PDF (section 7): Relative valuation is on FY2025 reported figures for the target AND every peer, not on TTM-2026 data, for three reasons: (1) consistency — a multiple is meaningful only if numerator and denominator, and target and peers, share the same period and definition (Lecture 1, slide 30: current, trailing or forward values, used consistently; repository comparables procedure: 'no TTM or FY mixing'); (2) the run's uniform source supplies audited FY2025 statements for all ~10 peers per target, while H1-2026 interims were not collected for them (several peers report on non-December or US/Japanese quarterly calendars), so putting only the target on TTM would apply FY2025 peer multiples to a 2026 earnings base; (3) the packaging brief forbids collecting new data. The group's DCF uses TTM-2026 / guidance / mid-cycle bases (claude/Piano_Discount_Rate_e_DCF.md), so RV-vs-DCF gaps include a period effect.
- **Canonical per-share units (SPIF list):** GBX for SSE, SHEL, BP (run GBP × 100); DKK for ORSTED and NKT (run EUR × 7.4735) and VWS (run DKK); NOK for EQNR; SEK for ALFA; EUR otherwise. PPT_Link B6 and B10:B19 use one unit per company.
- **FX:** only the runs' recorded ECB 30-Oct-2026 reference rates (cache/macro/2026-10-30.json: USD 1.1172, GBP 0.8338, DKK 7.4735, NOK 10.312, SEK 10.978 per EUR). **No FX was added in packaging** (no ECB fetch needed).
- **ISIN/exchange/cluster:** taken from the supplied SPIF_20_Selected_Companies.pdf (cluster A/B/C kept separate from repo buckets A–F).
- **Cross-check range (B18/B19):** MIN/MAX of reported selected-basis mids of run-usable multiples (Multiple_Stats column AW). Exclusions: BP raw P/E (USD 54m NI; run calls it 'not normalized earnings'), EQNR EV/EBITDA (run label 'diagnostic only').
- **Chart:** PEG not drawn (mechanically identical to adjusted P/E); VER also omits adjusted EV/Sales (≡ EV/EBITDA); BP omits raw P/E.
- **Headline-basis decisions:** SU and PRY adjusted P/E as instructed; AI.PA (legacy run, no designated headline) uses the growth-adjusted P/E EUR 90.7 per comparables_procedure.md §5 — **to be confirmed by the group**; raw EUR 170.8 shown as cross-check.
- **Derived in packaging:** SU adjusted p25/p75 per share (recorded adjusted quartiles × run EPS 7.4075 → EUR 138.71 / 206.04); AI adjusted p25/p75 (peer P/E÷g quartiles × target g × EPS → EUR 57.78 / 213.78). No reported benchmark; labelled.
- **Master synchronisation:** values copied (formula-evaluated after LibreOffice recalculation) from each `RV_<TICKER>.xlsx` PPT_Link!B1:B24 into `PPT_Snapshots` with provenance; `Summary` formulas reference only those local cells. No external links. Re-run the snapshot after any company-file change.
- **PPT_Link B17 for BP** evaluates blank by the prescribed formula `=IFERROR(B16/B6-1,"")` because B16 carries the label 'n/a – no headline regression'.

## 3. Recalculation and formula checks

| Ticker | Formulas | Formula errors | Failed 0.5% checks (amber; official values retained) |
|---|---:|---:|---|
| EDPR.LS | 487 | 0 | 0: none |
| ORSTED.CO | 484 | 0 | 3: Regression!P14 (PBV – Actual check); Target_Inputs!H36 (EV as recorded in run – Recomputed check); EV_Bridge!B13 (Check (0.5%)) |
| IBE.MC | 499 | 0 | 0: none |
| ENEL.MI | 495 | 0 | 0: none |
| SSE.L | 499 | 0 | 0: none |
| ENGI.PA | 491 | 0 | 0: none |
| VER.VI | 536 | 0 | 0: none |
| VWS.CO | 478 | 0 | 0: none |
| ENR.DE | 479 | 0 | 0: none |
| SU.PA | 562 | 0 | 2: Multiple_Stats!Z6 (P/E – Adjusted check); Multiple_Stats!AM6 (P/E – Mid check) |
| PRY.MI | 563 | 0 | 2: Regression!D8 (input check roe); Target_Inputs!H41 (ROE, closing equity (regression basis) – Recomputed check) |
| NKT.CO | 485 | 0 | 4: Regression!I8 (input check roic); Regression!P14 (PBV – Actual check); Target_Inputs!H50 (ROIC = EBIT(1−t)/(equity + debt − cash) – Recomputed check); EV_Bridge!B13 (Check (0.5%)) |
| ALFA.ST | 485 | 0 | 0: none |
| AI.PA | 367 | 0 | 9: Multiple_Stats!AM9 (EV/EBIT – Mid check); Multiple_Stats!AM10 (EV/EBITDA – Mid check); Regression!D8 (input check roe); Regression!G8 (input check dfr); Regression!I8 (input check roic); Regression!U15 (EV/EBITDA – Value check); Target_Inputs!H41 (ROE, closing equity (regression basis) – Recomputed check); Target_Inputs!H49 (Debt / (debt + market equity) – Recomputed check); Target_Inputs!H50 (ROIC = EBIT(1−t)/(equity + debt − cash) – Recomputed check) |
| MT.AS | 473 | 0 | 0: none |
| TTE.PA | 486 | 0 | 0: none |
| SHEL.L | 484 | 0 | 0: none |
| BP.L | 466 | 0 | 0: none |
| EQNR.OL | 472 | 0 | 0: none |
| NESTE.HE | 499 | 0 | 0: none |

Explanations of failed checks are in each workbook's QA_Flags (P01 and company flags): ORSTED/NKT target EV excludes the hybrid that the equity bridge deducts; NKT/ORSTED regression actual P/BV uses vendor book; PRY regression ROE on average equity; SU adjusted-P/E driver not reproducible from stored growth; AI EV values and regression input bases not stored in the legacy run.

Master workbook: recalculated, 0 formula errors.

## 4. Company manifest, status, QA chronology and flags

### EDPR.LS — EDP Renováveis, S.A.
- Run folder: `outputs/EDPR.LS_2026-10-30/` · status: **provisional_relative_only** · human Spot_check: PENDING
- QA chronology: QA block C run once with no FAIL items (warned items disclosed); status provisional. Checklist format without item headings: lines with warnings/pending items are listed below.
- Source logs: `source_log.csv` (541 rows)
- DCF earnings base (group): 2026 management guidance / normalised base
- Flags (material first):
  - [C01] **Material** · Basis dilemma · Current – group decision: Headline EV/EBITDA uses vendor EBITDA EUR 1,187m (EUR 3.92/share); issuer EBITDA EUR 1,947m gives ≈EUR 12.52 (sensitivities.csv) / ≈12.63 (relative_summary.md). Vendor EBITDA excludes equity-method/partnership income while EDPR's EV carries the matching claims (NCI 1,906m; deferred partnership revenues not deducted) — the run itself calls the headline 'biased low'.
  - [C03] **Material** · Outlier headline · Current – needs discussion: Official comparable mid EUR 3.92 is −69% vs price; chosen P/BV regression EUR 16.45 (+31.6%).
  - [C02] **Info** · Same-basis conflict · Current: Issuer-EBITDA sensitivity is 12.52 in sensitivities.csv but '~12.63' in relative_summary.md (+0.9%); recurring 12.83 vs '~12.86'.
  - [C04] **Info** · Low earnings base · Current: FY2025 NI 215.8m and ROE 2.1% (P/E 61.4x): P/E and ROE-scaled P/BV values (EUR 4.48 / 4.59) are depressed; SPIF list notes FY2024 loss and scrip dividends.

### ORSTED.CO — Ørsted A/S
- Run folder: `outputs/ORSTED.CO_2026-10-30/` · status: **provisional - limitations disclosed** · human Spot_check: PENDING
- QA chronology: Original QA block C had FAIL items on source certification, benchmarks, peer qualification, EV perimeter, normalisation and units; they were re-graded PASS-with-note under the documented standing approval qa_grading_and_remediation (item 1). Historical FAIL → subsequent PASS-with-note.
- Source logs: `source_log.csv` (541 rows)
- DCF earnings base (group): TTM 2026: EBIT = adjusted FY2025 EBIT + (H1 2026 − H1 2025)
- Flags (material first):
  - [C01] **Material** · Currency · Current – converted: Run price and values in EUR (EUR 17.65) although Ørsted trades in DKK (DKK 131.9); PPT_Link and chart converted × 7.4735 (run's ECB rate).
  - [C02] **Material** · Capital structure · Current: October 2025 rights issue (shares 1,321.062m) and DKK 20,955m hybrid (removed once from equity, once in bridge); FY2025 NI DKK 1,727m depressed by impairments (47% tax).
  - [C03] **Material** · Method dispersion · Current: Chosen P/BV regression EUR 35.99 (+104%) and EV/EBITDA regression EUR 38.02 (+115%) vs peer EV/EBITDA EUR 19.99 (+13%); P/E regression EUR 6.47.
  - [C04] **Info** · Issuer vs vendor · Current – sensitivity: Issuer EBITDA DKK 22,448m → EUR 21.11; 25,065m → EUR 24.56 (vendor 21,583m → 19.97).
  - [C05] **Info** · Peer overlap · Current: EDP and EDPR (itself a batch target) are both in the peer set; DRX has no EV multiples.
  - [C90] **Info** · Target EV vs bridge · Current – run inconsistency: The recorded target EV (DKK 236,927m) excludes the hybrid, while the EV→equity bridge for implied values deducts it (DKK 20,955m). Peer EVs exclude hybrids. The live EV check on EV_Bridge/Target_Inputs therefore fails by design; all implied values reproduce with the hybrid deducted.
  - [C91] **Info** · Source labels · Current – documentation: regression_valuation.xlsx Inputs sheet carries source labels copied from the EDPR run ('S3_EDPR_equity', EDPR payout text) and book 140,673 (vendor, incl. hybrid); the reported regression values use the common basis.
  - [P01] Amber packaging checks: Regression!P14 (PBV – Actual check); Target_Inputs!H36 (EV as recorded in run – Recomputed check); EV_Bridge!B13 (Check (0.5%))

### IBE.MC — Iberdrola, S.A.
- Run folder: `outputs/IBE.MC_2026-10-30/` · status: **in_progress (run_state.json; stage 3 'done_provisional')** · human Spot_check: PENDING
- QA chronology: QA block C run once with no FAIL items (warned items disclosed); status provisional. Checklist format without item headings: lines with warnings/pending items are listed below.
- Source logs: `source_log.csv` (598 rows)
- DCF earnings base (group): TTM 2026: EBIT = adjusted FY2025 EBIT + (H1 2026 − H1 2025)
- Flags (material first):
  - [C01] **Material** · Run status · Current – inconsistent: run_state.json final_status 'in_progress' while stage 3 is 'done_provisional'; relative_summary.md states PROVISIONAL.
  - [C02] **Info** · Issuer vs vendor · Current – sensitivity: Issuer EBITDA reported 16,592 → EUR 20.89; adjusted 15,684 → EUR 19.18 (vendor 14,700 → 17.32).
  - [C03] **Info** · Adjusted multiples · Current: Growth-scaled P/E/PEG (~EUR 49.8) flagged by the run as distorted (near-zero peer fundamental growth); raw P/E retained as cross-check.

### ENEL.MI — Enel S.p.A.
- Run folder: `outputs/ENEL.MI_2026-10-30/` · status: **provisional_relative_only** · human Spot_check: PENDING
- QA chronology: QA block C run once with no FAIL items (warned items disclosed); status provisional. Checklist format without item headings: lines with warnings/pending items are listed below.
- Source logs: `source_log.csv` (597 rows)
- DCF earnings base (group): TTM 2026: EBIT = adjusted FY2025 EBIT + (H1 2026 − H1 2025)
- Flags (material first):
  - [C01] **Material** · Method dispersion · Current: Peer EV/EBITDA (EUR 17.79, +91%) and the chosen published P/BV regression (EUR 6.95, −25%) bracket the price in opposite directions; the run records both and reconciles neither.
  - [C02] **Material** · Issuer vs vendor · Current – sensitivity: Vendor EBITDA 20,311 vs issuer reported 22,073 / ordinary 22,874 moves the EV/EBITDA mid to EUR 20.02 / 21.03; vendor NI 3,959 vs issuer group NI 4,225 (266m unexplained deduction).
  - [C03] **Info** · Same-basis conflict · Current – narrative rounding: relative_summary.md quotes the issuer-EBITDA sensitivity as '~20.59' and ordinary '~21.48'; sensitivities.csv gives 20.02 and 21.03 (−2.8% / −2.1%).
  - [C04] **Info** · Input · Current: Payout > 100% (declared dividend 4,982 / NI 3,959 = 1.26) and zero fundamental growth: PEG not meaningful; the PE regression uses the high payout.
  - [C05] **Info** · Run status · Current – documentation: run_state.json final_status is 'provisional_relative_only' (stage 3 'provisional').

### SSE.L — SSE plc
- Run folder: `outputs/SSE.L_2026-10-30/` · status: **done_provisional** · human Spot_check: PENDING
- QA chronology: QA block C run once with no FAIL items (warned items disclosed); status provisional. Checklist format without item headings: lines with warnings/pending items are listed below.
- Source logs: `source_log.csv` (599 rows)
- DCF earnings base (group): FY2026 (year to 31-Mar-2026), one fiscal year after the RV base (FY to 31-Mar-2025)
- Flags (material first):
  - [C01] **Material** · Fiscal period · Current – disclosed: FY2025 ends 31-Mar-2025; peers mostly 31-Dec-2025. Not calendarised.
  - [C02] **Material** · Issuer vs vendor · Current – sensitivity: Vendor EBITDA £2,850m → £19.28 (official). Issuer reported £2,738.3m → £18.19; adjusted £3,349.3m → £24.14.
  - [C03] **Material** · Hybrids / EV · Current – disclosed: Hybrid capital appears inside vendor Total Debt (counted once). Target long-term-investments proxy £1,996m is NOT subtracted (peer EV before associates) — non-harmonised associate basis.
  - [C04] **Material** · Share count · Current: Current 1,210m shares (post-2026 equity raise) vs FY2025 issuer shares 1,106.3m and weighted 1,099.2m: per-share values use the current count against a pre-raise earnings base.
  - [C06] **Material** · Regression outlier · Current: Market-wide EV/EBITDA regression gives £40.94/share (21.0x vs peer median 11.8x) — sector-blind outlier, not merged with peer value. Chosen P/BV £22.98 (R² 0.423).
  - [C05] **Info** · Units · Current – converted: Run in GBP (£26.27); LSE quote 2,627p. PPT_Link and chart converted × 100 to GBX.
  - [C07] **Info** · Payout basis · Current: Regression payout 0.597 on declared dividends vs cash-paid basis in scoring.

### ENGI.PA — ENGIE SA
- Run folder: `outputs/ENGI.PA_2026-10-30/` · status: **provisional_relative_only** · human Spot_check: PENDING
- QA chronology: QA block C run once with no FAIL items (warned items disclosed); status provisional. Checklist format without item headings: lines with warnings/pending items are listed below.
- Source logs: `source_log.csv` (597 rows)
- DCF earnings base (group): TTM 2026: EBIT = adjusted FY2025 EBIT + (H1 2026 − H1 2025)
- Flags (material first):
  - [C01] **Material** · Outlier headline · Current – needs discussion: Peer EV/EBITDA midpoint EUR 45.51 is +94% vs EUR 23.43; P/BV regression EUR 26.71 (+14%) and P/E EUR 35.44 are much closer to the price.
  - [C02] **Material** · Data anomaly · Current: Vendor FY2025 CFO is −1,476m (issuer CFFO positive): EV/CF not meaningful for the target.
  - [C03] **Info** · Issuer vs vendor · Current – sensitivity: Issuer consolidated EBITDA 14,700 → EUR 54.00; ex-nuclear 13,400 → EUR 47.46 (vendor 13,012 → 45.51).

### VER.VI — Verbund AG
- Run folder: `outputs/VER.VI_2026-10-30/` · status: **provisional - limitations disclosed** · human Spot_check: PENDING
- QA chronology: 8 historical FAILs (C4, C5, C8, C9, C11, C18, C20, C42) → PASS-with-note, rule-authorised re-grade 2026-11-02
- Source logs: `source_log.csv` (653 rows)
- DCF earnings base (group): TTM 2026 EBIT; net income from 2026 guidance (FCFE)
- Flags (material first):
  - [Q01] **Material** · Verification status · Current – unresolved: Run status is 'provisional - limitations disclosed'. Human Spot_check PENDING; peer ISINs registry-mapped pending issuer verification; inputs not fully verified against filings.
  - [T01] **Material** · Timing basis vs DCF · Current – disclosed by design: Relative valuation is on FY2025 reported figures for the target AND every peer, not on TTM-2026 data, for three reasons: (1) consistency — a multiple is meaningful only if numerator and denominator, and target and peers, share the same period and definition (Lecture 1, slide 30: current, trailing or forward values, used consistently; repository comparables procedure: 'no TTM or FY mixing'); (2) the run's uniform source supplies audited FY2025 statements for all ~10 peers per target, while H1-2026 interims were not collected for them (several peers report on non-December or US/Japanese quarterly calendars), so putting only the target on TTM would apply FY2025 peer multiples to a 2026 earnings base; (3) the packaging brief forbids collecting new data. The group's DCF uses a different earnings base for this company: TTM 2026 EBIT; net income from 2026 guidance (FCFE).
  - [Q03] **Material** · Same-basis conflict · Current – narrative error: report_notes.md (and relative_summary.md §5) state EV/EBIT value +34% and EV/EBITDA regression +69% vs price; the CSV/JSON values give +50.1% (EUR 104.35 / 69.50) and +89.2% (EUR 131.52 / 69.50).
  - [Q04] **Material** · Labelling conflict · Current – documentation: relative_summary.md §3 labels P/E, P/BV, P/S and EV/Sales rows 'raw' and shows the raw median, but the value columns are the run's selected (adjusted) values, e.g. P/E value mid EUR 29.40 is the adjusted 6.86x; raw P/E 17.50x implies EUR 74.98.
  - [Q07] **Material** · Input reliability · Current – group decision: SPIF list flags Verbund's beta as not reliable (small free float) and suggests an industry/bottom-up beta. The run uses the observed vendor beta 0.14 in the published P/E and P/BV equations (route rule replaces beta only if missing, negative or > 2.5) and in peer scoring.
  - [Q08] **Material** · Methodological warning · Current: Regression outputs disperse widely: P/E EUR 49.77 (−28.4%), chosen P/BV EUR 59.61 (−14.2%), EV/EBITDA EUR 131.52 (+89.2%). Negative consensus growth (g_eps −4.51%, g_rev −0.98%) lowers the P/E prediction; the market-wide EV/EBITDA equation (R² 0.262) has no utility structure.
  - [Q12] **Material** · Normalisation · Current – disclosed limitation: Austrian windfall-profit levy EUR 135.9m sits in FY2025 costs; not normalised uniformly across peers (original C20 FAIL, now PASS-with-note).
  - [Q02] **Info** · QA chronology · Historical FAIL → subsequent PASS-with-note: Original QA block C (2026-11-02): 31 PASS / 8 FAIL / 9 N/A, 'NOT PASSED / PROVISIONAL' and 'comparable conclusion is blocked'. Same day the 8 FAILs (C4, C5, C8, C9, C11, C18, C20, C42) were re-graded PASS-with-note under the documented standing approval qa_grading_and_remediation (item 1).
  - [Q05] **Info** · Narrative inconsistency · Current – documentation: relative_inputs.md says growth-scaled P/E adjustments are 'invalid — recorded as unavailable' (negative consensus growth), yet multiples_summary.csv records an adjusted P/E of 6.86x (n=7) scaled by the positive fundamental growth 1.57% (ROE × retention), as the procedure allows.
  - [Q06] **Info** · Labelling conflict · Current – documentation: sensitivities.csv rows named 'leave-one-out peer X' contain the single peer's EV/EBITDA applied to target EBITDA (the run's note column says so), not a leave-one-out median. CNA value blank (1.10x gives negative equity).
  - [Q09] **Info** · EV basis · Current – disclosed limitation: Uniform pre-associate EV bridge: long-term investments 1,419 not subtracted and equity-investment earnings 92.6 left in EBIT/EBITDA; peers' associates proxied by long-term investments. Run flags EV multiples 'not fully harmonized'.
  - [Q10] **Info** · Source difference · Current – within tolerance: Target EV recorded in candidate files 27,527.5 (vendor cap 24,150) vs relative_inputs.md 27,522 (price × shares 24,145.7 and incl. ST investments 1.1): −0.02%. Vendor quote-side EV 28.20bn (+2.4%) uses a broader perimeter.
  - [Q11] **Info** · Issuer vs vendor · Current – sensitivity: Issuer net debt 2,818.1 vs vendor 2,386 lowers the EV/EBITDA mid to EUR 76.67 (−1.6%); issuer EBITDA 2,737.5 raises it to EUR 78.64 (+0.9%).
  - [Q13] **Info** · Basis differences · Current – by design: Payout and ROE use different bases by purpose: regression payout 46.6% (declared DPS) vs scoring payout 89.3% (cash paid incl. special); regression ROE 14.40% (closing equity) vs scoring ROE 14.66% (average equity).
  - [Q14] **Info** · Funnel documentation · Current – reconciled by recomputation: SLR, GRE and SCATC are 'preliminary eligible' in candidate_gates.csv but absent from the scored Europe pool; the exclusion reason is not written in the gate file. Their market caps (1.3–1.9bn) are below 0.1× the target cap (2.415bn), the band in the run's build.py.
  - [Q15] **Info** · Peer outlier · Current: Centrica (CNA) EV/EBITDA 1.10x and EV/EBIT 1.15x (net-cash position on vendor data); P/E not meaningful. Retained by the run's rules; median is robust to it.
  - [Q16] **Info** · Benchmark · Current – disclosed limitation: Peer EV/EBITDA median 11.21x vs Damodaran Europe 'Utility (General)' aggregate 8.21x (+36.6%); P/BV 2.01x vs 1.51x (+33.0%). Aggregates, not medians; plausibility only.
  - [Q17] **Info** · Regression vintage/units · Current – disclosed limitation: Equations dated Jan-2026 (≈10 months old); no SEy/n/p-values. Decimal DFR/tax policy approved; percentage-point policy would give EV/EBITDA prediction 14.69x instead of 18.07x (−18.7%).
  - [Q18] **Info** · Overlap · Current: PEG value equals the adjusted P/E value (PEG × 100g × EPS ≡ median P/E÷g × g × EPS) and adjusted EV/Sales equals EV/EBITDA (margin scaling). They are not independent evidence.
  - [Q19] **Info** · Timing · Current – no concern identified: Access dates 1–2 Nov 2026 post-date the 30-Oct-2026 cutoff; prices are the 30-Oct history close and FY2025 data were published in March 2026, so no look-ahead is evident from run evidence.
  - [Q20] **Info** · Run documentation · Current – cosmetic: run_state.json records a 'valuation range EUR 54.42–131.52' (primary IQR low to regression high), a diagnostic span mixing methods; relative_summary.md status line repeats 'limitations disclosed'.
  - [Q21] **Info** · Narrative FX conflict · Current – documentation: comparables_report.md quotes ECB rates 'GBP 0.8785, DKK 7.4735, NOK 11.49'; the run cache (cache/macro/2026-10-30.json) and the peer EUR market caps use GBP 0.8338 and NOK 10.312 (e.g. SSE 31,690 / 0.8338 = EUR 38,007m). The text is wrong; the numbers use the cache rates.

### VWS.CO — Vestas Wind Systems A/S
- Run folder: `outputs/VWS.CO_2026-10-30/` · status: **(none recorded in run_state.json; relative_summary.md: provisional - limitations disclosed)** · human Spot_check: PENDING
- QA chronology: qa_results.md re-grades the original FAILs (C4, C5, C8, C9, C11, C15→C18, C19→C20, C37→C42 mapping documented) to PASS-with-note under qa_grading_and_remediation, but relative_summary.md still states 'open FAIL items: C4, C5, C8, C9, C11, C15, C19, C37'. Chronology and mapping are documented → historical FAIL → subsequent PASS-with-note; summary text is stale.
- Source logs: `relative/source_log.csv` (628 rows)
- DCF earnings base (group): 2026 management guidance / normalised base
- Flags (material first):
  - [C01] **Material** · QA text conflict · Current – documentation: relative_summary.md lists open FAILs (C4, C5, C8, C9, C11, C15, C19, C37) while qa_results.md documents their re-grade (with item mapping) to PASS-with-note.
  - [C02] **Info** · Peer count · Current: EV multiples have n = 8 (IMI and NKT invalid denominators).
  - [C03] **Info** · Share count · Current: 978.25m current shares; 999m weighted basic is a −2.1% sensitivity.
  - [C04] **Info** · Adjusted P/E · Current: Scaled P/E diagnostic DKK 252.63 (+55.8% vs EV/EBIT mid) driven by high vendor consensus growth.
  - [C05] **Info** · Peer overlap · Current: ENR.DE (separately remediated) is in the peer set with unchanged vendor figures.

### ENR.DE — Siemens Energy AG
- Run folder: `outputs/ENR.DE_2026-10-30/` · status: **provisional - limitations disclosed** · human Spot_check: PENDING
- QA chronology: Original QA block C had FAIL items on source certification, benchmarks, peer qualification, EV perimeter, normalisation and units; they were re-graded PASS-with-note under the documented standing approval qa_grading_and_remediation (item 1). Historical FAIL → subsequent PASS-with-note.
- Source logs: `relative/source_log.csv` (628 rows)
- DCF earnings base (group): 2026 management guidance / normalised base
- Flags (material first):
  - [C01] **Material** · Outlier headline · Current – needs discussion: EV/EBIT mid EUR 44.18 is −65% vs EUR 126.92; growth-scaled P/E EUR 71.47; P/BV regression EUR 35.94.
  - [C02] **Material** · Earnings fragility · Current: Weak wind margin: mechanical EBIT-margin 4/6/8/10% sensitivity gives EUR 167.07 (+278%); issuer EBIT 2,149 (incl. 580 equity income) gives EUR 58.43 (+32%).
  - [C03] **Info** · Fiscal period · Current: FY ends 30-Sep-2025; peers mostly December. Shares 855.34m (vendor) vs 850m issuer (+0.63% sensitivity).
  - [C04] **Info** · Peer set · Current: 10 peers: 7 Tier 1–2, 3 Tier 3, 9 Europe-listed (Tier-3 relaxation used).

### SU.PA — Schneider Electric SE
- Run folder: `outputs/SU.PA_2026-10-30/` · status: **done_provisional** · human Spot_check: PENDING
- QA chronology: QA block C run once with no FAIL items (warned items disclosed); status provisional. Checklist format without item headings: lines with warnings/pending items are listed below.
- Source logs: `source_log.csv` (4 rows), `source_log_stage3.csv` (5 rows)
- DCF earnings base (group): TTM 2026: EBIT = adjusted FY2025 EBIT + (H1 2026 − H1 2025)
- Flags (material first):
  - [C01] **Material** · Adjusted vs raw · Current – headline definition: Primary is the growth-adjusted P/E median 23.43x → EUR 173.59 (official headline); raw P/E median 31.40x → EUR 232.63 is a cross-check only. multiples_summary.csv main value fields hold RAW values; the adjusted headline is in adjusted_value_mid.
  - [C03] **Material** · Funnel count · Current – unreconciled: Narrative says 104 candidates screened; pool files contain 11 eligible + 98 rejected = 109 unique tickers.
  - [C02] **Info** · Derived range · Current – derived in packaging: No reported adjusted low/high per share: derived = adjusted p25 18.73x / p75 27.82x × EPS 7.4075 → ≈EUR 138.7 / 206.0 (labelled; no benchmark).
  - [C04] **Info** · Peer composition · Current: 10 peers: 8 Tier 1–2 and 2 Tier 3 (at the cap); the very large target size band drives the Tier-3 inclusion. Prysmian is a peer and also has its own run.
  - [C05] **Info** · Payout bases · Current: Declared payout 0.567 (regression and scoring) vs CF-paid 0.526; a sensitivities row quotes fundamental growth 0.0685 vs 0.0721 while relative_inputs.md gives 0.0659.
  - [C06] **Info** · EV components · Current – gap: Peer debt/NCI/cash not stored in the peer files: peer EV bridge shown as n/a.
  - [C07] **Info** · Regression values · Current: regression_results.json stores predictions only; per-share values (PE 207.15, PBV 145.78, EV/EBITDA 288.95) are quoted from relative_summary.md.
  - [C08] **Info** · Adjustment reproducibility · Current – not reproducible: The growth-adjusted P/E median (23.43x) could not be reproduced from the stored peer fundamental growth (live recomputation ≈21.4x): the run's growth driver for this adjustment is not fully specified in the files. Reported adjusted statistics retained.
  - [P01] Amber packaging checks: Multiple_Stats!Z6 (P/E – Adjusted check); Multiple_Stats!AM6 (P/E – Mid check)

### PRY.MI — Prysmian S.p.A.
- Run folder: `outputs/PRY.MI_2026-10-30/` · status: **provisional - limitations disclosed** · human Spot_check: PENDING
- QA chronology: Remediated QA (relative/qa_results.md): no FAIL items; annual-report cross-check NOT performed (disclosed).
- Source logs: `source_log.csv` (7 rows)
- DCF earnings base (group): 2026 management guidance / normalised base
- Flags (material first):
  - [C01] **Material** · Adjusted vs raw · Current – headline definition: Primary is the growth-adjusted P/E median 30.98x → EUR 134.61 (IQR EUR 111.52–178.60, adjusted basis); raw P/E median 26.98x → EUR 117.23 is a cross-check. ROE-adjusted P/BV (EUR 129.76) is a further cross-check.
  - [C03] **Material** · Source log granularity · Current – gap: source_log.csv has only 7 rows and 5 columns (source, location, accessed, used_for, status); no field-level URLs per metric.
  - [C04] **Material** · Verification · Current – unresolved: Annual-report cross-check NOT performed; StockAnalysis figures unverified; associates not collected (EV before associates).
  - [C07] **Material** · P/E vs EV divergence · Current: Net debt/EBITDA 1.62x vs peer median 0.16x and tax 21.6% vs ~26%: EV/EBIT EUR 79.65 and EV/EBITDA EUR 84.27 sit 24–28% below the price while the adjusted P/E is +22%.
  - [C02] **Info** · Same-metric conflict · Current – different basis: EV/EBITDA midpoint EUR 84.27 (multiples_summary.csv, n = 10, median 14.17x) vs EUR 85.13 in relative/valuation_summary.md and comparables_report.md (n = 7, median 14.29x): +1.0%, but on a different valid count, so not the same basis. The top-level summary and CSV agree on 84.27.
  - [C05] **Info** · Growth substitution · Current: Consensus growth not collected; approved fundamental ROE × retention (18.0%) substituted in the regressions (substituted_input).
  - [C06] **Info** · Perimeter · Current: Encore Wire acquisition (July 2024): FY2025 is the first full-year base.
  - [C08] **Info** · Peer ISIN · Current: Vestas has two cached ISINs (DK0061539921 kept; DK0010268606 unresolved).
  - [C09] **Info** · Regression ROE basis · Current – by design: Regression ROE 0.2197 is NI / average equity; the workbook's live check uses NI / closing equity (0.1962), so that input check fails by design.
  - [P01] Amber packaging checks: Regression!D8 (input check roe); Target_Inputs!H41 (ROE, closing equity (regression basis) – Recomputed check)

### NKT.CO — NKT A/S
- Run folder: `outputs/NKT.CO_2026-10-30/` · status: **in_progress (run_state.json); relative_summary.md: provisional - limitations disclosed** · human Spot_check: PENDING
- QA chronology: Original QA block C had FAIL items on source certification, benchmarks, peer qualification, EV perimeter, normalisation and units; they were re-graded PASS-with-note under the documented standing approval qa_grading_and_remediation (item 1). Historical FAIL → subsequent PASS-with-note.
- Source logs: `source_log.csv` (2 rows), `relative/source_log.csv` (718 rows)
- DCF earnings base (group): TTM 2026: EBIT = adjusted FY2025 EBIT + (H1 2026 − H1 2025)
- Flags (material first):
  - [C02] **Material** · Adjusted headline · Current: Primary P/E is growth-scaled (27.92x vs raw 26.98x).
  - [C03] **Material** · One-off tax · Current: FY2025 effective tax 6.46%; statutory-22% sensitivity cuts the P/E value to about EUR 115 (near the price).
  - [C04] **Material** · Issuer vs vendor · Current: Vendor EBIT 578 / EBITDA 680 vs issuer EBIT 257 / operational EBITDA 390.
  - [C01] **Info** · Currency · Current – converted: Run quotes EUR 112.26 (DKK 839.0 at 7.4735); NKT lists in DKK. PPT_Link converted × 7.4735.
  - [C05] **Info** · Run status · Current – inconsistent: run_state.json final_status 'in_progress' while QA is re-graded and summary says provisional.
  - [C06] **Info** · Peer swap · Current: TKA replaced by ALFA on business fit (scaled P/E ~EUR 151 → 138).
  - [C90] **Info** · Target EV vs bridge · Current – run inconsistency: The recorded target EV (EUR 5,036.9m) excludes the hybrid, while the EV→equity bridge for implied values deducts it (EUR 150m). Peer EVs exclude hybrids. The live EV check on EV_Bridge/Target_Inputs therefore fails by design; all implied values reproduce with the hybrid deducted.
  - [P01] Amber packaging checks: Regression!I8 (input check roic); Regression!P14 (PBV – Actual check); Target_Inputs!H50 (ROIC = EBIT(1−t)/(equity + debt − cash) – Recomputed check); EV_Bridge!B13 (Check (0.5%))

### ALFA.ST — Alfa Laval AB (publ)
- Run folder: `outputs/ALFA.ST_2026-10-30/` · status: **provisional_relative_only** · human Spot_check: PENDING
- QA chronology: QA block C run once with no FAIL items (warned items disclosed); status provisional. Checklist format without item headings: lines with warnings/pending items are listed below.
- Source logs: `source_log.csv` (541 rows)
- DCF earnings base (group): TTM 2026: EBIT = adjusted FY2025 EBIT + (H1 2026 − H1 2025)
- Flags (material first):
  - [C01] **Material** · Adjusted headline · Current: Primary is the growth-scaled P/E (adjusted median 33.23x vs raw 26.69x) → SEK 665.01; raw-basis P/E gives a lower value (see Multiple_Stats).
  - [C02] **Info** · Share classes · Current: ATCO.A and EPI.A market caps deviate +4.25% / +4.75% (dual A/B share classes; vendor counts only A shares).
  - [C03] **Info** · Method dispersion · Current: Published P/BV regression SEK 343.26 (−37%), P/E SEK 434.06 (−20%), EV/EBITDA SEK 710.47 (+30%).
  - [C04] **Info** · No sensitivities file · Current: No sensitivities.csv in this run; the audit workbook has a Live_PE_G sheet only.

### AI.PA — L'Air Liquide S.A.
- Run folder: `outputs/AI.PA_2026-10-30/` · status: **done (stage 4 executed in legacy run — recommendation and DCF IGNORED here)** · human Spot_check: PENDING
- QA chronology: Legacy single qa_results.md with blocks A–D; block C has no FAILs and one open item (manual Spot_check pending). Blocks B and D (DCF, recommendation) are outside this package.
- Source logs: `source_log.csv` (204 rows)
- DCF earnings base (group): TTM 2026: EBIT = adjusted FY2025 EBIT + (H1 2026 − H1 2025)
- Flags (material first):
  - [C01] **Material** · Headline basis · Current – packaging decision to confirm: The legacy run reports P/E as primary but gives 'central ~EUR 171 raw / EUR 91 growth-adjusted' without designating one. Per comparables_procedure.md §5 ('for positive drivers use the adjusted version as the primary-method point estimate') the growth-adjusted EUR 90.7 is used as headline; raw EUR 170.8 is the cross-check.
  - [C02] **Material** · Legacy layout · Current – gaps: No relative_summary.md, no sensitivities.csv, 8-column multiples_summary.csv without per-share values: per-share figures quoted from comparables_report.md / valuation_summary.md; low/high for the headline derived in packaging.
  - [C04] **Material** · DCF and rating in run · Current – excluded: This legacy run also contains a DCF model and a stage-4 investment rating; both are excluded from this package by the brief (no figures imported).
  - [C03] **Info** · EV values · Current – not reproducible: EV/EBIT (EUR 201.2) and EV/EBITDA (EUR 199.4) values cannot be reproduced: the target EBIT/EBITDA and EV bridge used by the run are not stored; live checks use issuer figures and are expected to differ.
  - [C05] **Info** · Regression choice · Current – packaging rule: No single chosen regression recorded ('best-R² model chosen per dependent'); P/BV (highest published R² 0.423) reported as chosen per the route rule.
  - [C06] **Info** · Peer composition · Current: World expansion for LIN, APD, 4091; relaxed size band for YAR; SOL (European gases pure play) excluded by the size band; APD P/E unavailable (Sep FY), DSFIR loss-making.
  - [C07] **Info** · Narrative vs CSV · Current – CSV retained: comparables_report.md states P/BV median 2.86 and P/S median 2.83; multiples_summary.csv (and the live recomputation from peers) give 3.95x and 3.03x.
  - [C08] **Info** · Regression input bases · Current: Run regression inputs (ROE 13.97%, DFR 0.130, ROIC 9.3%) do not match NI/equity, debt/(debt+cap) and EBIT-based recomputations from the issuer figures on Target_Inputs (13.4%, 0.106, 15.9%): the legacy run used other (vendor/average) bases not stored. Live input checks fail by design.
  - [P01] Amber packaging checks: Multiple_Stats!AM9 (EV/EBIT – Mid check); Multiple_Stats!AM10 (EV/EBITDA – Mid check); Regression!D8 (input check roe); Regression!G8 (input check dfr); Regression!I8 (input check roic); Regression!U15 (EV/EBITDA – Value check); Target_Inputs!H41 (ROE, closing equity (regression basis) – Recomputed check); Target_Inputs!H49 (Debt / (debt + market equity) – Recomputed check); Target_Inputs!H50 (ROIC = EBIT(1−t)/(equity + debt − cash) – Recomputed check)

### MT.AS — ArcelorMittal S.A.
- Run folder: `outputs/MT.AS_2026-10-30/` · status: **provisional** · human Spot_check: PENDING
- QA chronology: Run's final QA (qa_results.md) records 14 FAIL_OPEN items (evidence/ownership/event and verification); no rule-authorised re-grade is documented for this run → currently UNRESOLVED.
- Source logs: `source_log.csv` (989 rows)
- DCF earnings base (group): mid-cycle normalised margin (FY2022-25 average)
- Flags (material first):
  - [C01] **Material** · QA status · Current – unresolved FAIL: Final QA lists 14 FAIL_OPEN items; no documented re-grade under qa_grading_and_remediation for MT.AS.
  - [C02] **Material** · Peer shortfall · Current: Exactly 10 infeasible after all ordered relaxations: 9 peers (6 Tier 1–2, 3 Tier 3, 6 Europe-listed); Tier-3 cap 4 and 0.05–20× band used.
  - [C03] **Material** · Growth substitution · Current: Approved fundamental-growth substitution (closing ROE × retention) replaces analyst g_eps; g_rev unavailable, so the EV/EBITDA regression is not valued.
  - [C05] **Material** · Issuer vs vendor · Current – unresolved: Vendor FY2025 EBIT 1,667 vs issuer 3,628 remains unresolved; EV ratios are qualified cross-checks only.
  - [C04] **Info** · Currency · Current: Reports USD, trades EUR: per-share values in EUR at ECB 1.1172.
  - [C06] **Info** · Regression vs peers · Current: Published P/BV regression EUR 112.26 (+109%) vs peer P/BV EUR 76.75; market-wide equation, not a steel fair value.

### TTE.PA — TotalEnergies SE
- Run folder: `outputs/TTE.PA_2026-10-30/` · status: **provisional - limitations disclosed** · human Spot_check: PENDING
- QA chronology: Original QA block C had FAIL items on source certification, benchmarks, peer qualification, EV perimeter, normalisation and units; they were re-graded PASS-with-note under the documented standing approval qa_grading_and_remediation (item 1). Historical FAIL → subsequent PASS-with-note.
- Source logs: `source_log.csv` (3 rows), `relative/source_log.csv` (745 rows)
- DCF earnings base (group): mid-cycle normalised: average adjusted margin FY2021 and FY2023-25 × FY2025 revenue (TTM as a control)
- Flags (material first):
  - [C01] **Material** · Issuer vs vendor · Current – sensitivity: Issuer adjusted EBITDA 40,555 vs vendor 32,770 → EUR 124.32 (+27.2%).
  - [C02] **Info** · Beta · Current: Vendor 5Y beta 0.04 retained and flagged (SPIF: beta 0.09 not reliable).
  - [C03] **Info** · Regression outlier · Current: Market-wide EV/EBITDA equation cannot price oil majors (predicted ≈20x vs actual ≈7x): diagnostic only. EUR 247.39.
  - [C04] **Info** · Growth substitution · Current: Fundamental growth 4.04% substituted for analyst growth in the regressions (approved).

### SHEL.L — Shell plc
- Run folder: `outputs/SHEL.L_2026-10-30/` · status: **provisional - limitations disclosed** · human Spot_check: PENDING
- QA chronology: Original QA block C had FAIL items on source certification, benchmarks, peer qualification, EV perimeter, normalisation and units; they were re-graded PASS-with-note under the documented standing approval qa_grading_and_remediation (item 1). Historical FAIL → subsequent PASS-with-note.
- Source logs: `relative/source_log.csv` (745 rows)
- DCF earnings base (group): mid-cycle normalised: average adjusted margin FY2021 and FY2023-25 × FY2025 revenue (TTM as a control)
- Flags (material first):
  - [C02] **Material** · Issuer vs vendor · Current – sensitivity: Issuer adjusted EBITDA 56,135 vs vendor 47,658 → GBP 55.87 (+20.1%).
  - [C01] **Info** · Units · Current – converted: Run values in GBP (40.365) for a GBX quote (4,036.5p); PPT_Link × 100.
  - [C03] **Info** · Beta · Current: Vendor beta −0.19 retained for scoring (flag) and replaced by a relevered industry beta (~0.47) in the published regression.
  - [C04] **Info** · Regression outlier · Current: Market-wide EV/EBITDA equation cannot price oil majors (predicted ≈20x vs actual ≈7x): diagnostic only. GBP 119.75.

### BP.L — BP p.l.c.
- Run folder: `outputs/BP.L_2026-10-30/` · status: **provisional - limitations disclosed** · human Spot_check: PENDING
- QA chronology: Earlier stricter QA failures were rechecked under qa_grading_and_remediation (qa_failed_item_recheck.md, qa_approved_recheck.json); only qualified peers are used and numeric_prospects_NOT_QUALIFIED.csv is excluded.
- Source logs: `source_log.csv` (156 rows)
- DCF earnings base (group): mid-cycle normalised: average adjusted margin FY2021 and FY2023-25 × FY2025 revenue (TTM as a control)
- Flags (material first):
  - [C01] **Material** · Regression status · Current: No chosen regression: PE not selected (near-zero NI, payout 93.7x), PBV not valued (negative prediction), EV/EBITDA 18.07x / GBP 23.59 DIAGNOSTIC ONLY.
  - [C02] **Material** · Earnings distortion · Current: FY2025 NI USD 54m (impairment/tax): P/E and scaled P/BV/PS values collapse; EBITDA add-back of USD 6,037m impairment → GBP 13.66 (+25%).
  - [C04] **Material** · Outlier headline · Current – needs discussion: Peer EV/EBITDA mid GBP 10.93 is +74.2% vs GBP 6.27.
  - [C00] **Info** · Cross-check range · Current – packaging choice: The raw P/E value (GBP 0.06 per share on USD 54m NI) is usable by the run's count rule but economically meaningless (the run calls it 'a very low cross-check, not normalized earnings'); it is excluded from the PPT cross-check range (Multiple_Stats AW) and from the chart, and kept in the tables.
  - [C03] **Info** · Qualified peers · Current: Only qualified peers used; OXY/HBR/CVX/OMV excluded for completed deals and replaced by XOM/COP/SHEL/PSX; numeric_prospects_NOT_QUALIFIED.csv not used.
  - [C05] **Info** · Units · Current – converted: GBP (not GBp) in run; LSE quote 627.4p; PPT × 100.

### EQNR.OL — Equinor ASA
- Run folder: `outputs/EQNR.OL_2026-10-30/` · status: **provisional - limitations disclosed** · human Spot_check: PENDING
- QA chronology: Original QA block C had FAIL items on source certification, benchmarks, peer qualification, EV perimeter, normalisation and units; they were re-graded PASS-with-note under the documented standing approval qa_grading_and_remediation (item 1). Historical FAIL → subsequent PASS-with-note.
- Source logs: `relative/source_log.csv` (745 rows)
- DCF earnings base (group): mid-cycle normalised: average adjusted margin FY2021 and FY2023-25 × FY2025 revenue (TTM as a control)
- Flags (material first):
  - [C01] **Material** · Primary choice · Current: EV/EBITDA rejected as primary: ~80–97% effective-tax names (EQNR, VAR, AKRBP) sit at the lowest EV/EBITDA multiples; the EV/EBITDA value (+118%) is diagnostic only.
  - [C02] **Info** · P/E outliers · Current: Peer P/Es include BP 2,362x and AKRBP 203x; the median is robust but the mean is not.
  - [C03] **Info** · Regression outlier · Current: EV/EBITDA equation predicts 18.48x vs actual 3.59x (−81%): cannot price an ~80% tax producer.
  - [C04] **Info** · Ownership · Current: Norwegian state ~67% holder; Eni ~63% of peer VAR (peer–peer); Adura JV noted.
  - [C05] **Info** · Cross-check range · Current: EV/EBITDA is labelled 'diagnostic only' by the run (petroleum-tax wedge): excluded from the PPT cross-check range B18/B19 and drawn as a diagnostic bar.

### NESTE.HE — Neste Oyj
- Run folder: `outputs/NESTE.HE_2026-10-30/` · status: **in_progress (run_state.json); qa_results.md: provisional - limitations disclosed** · human Spot_check: PENDING
- QA chronology: run_state.json still records qa_C 'failed_provisional' with 9 FAIL, while qa_results.md documents a 2026-11-01 re-grade of C4, C5, C8, C9, C11, C17, C18, C20, C42 to PASS-with-note under qa_grading_and_remediation (with a business-description peer remediation). The later, rule-authorised re-grade is treated as current; run_state was not updated.
- Source logs: `source_log.csv` (2 rows), `relative/source_log.csv` (906 rows)
- DCF earnings base (group): mid-cycle normalised margin (FY2023-25)
- Flags (material first):
  - [C01] **Material** · Outlier headline · Current – needs discussion: EV/EBITDA mid EUR 6.71 is −76.3% vs EUR 28.34: FY2025 trough (EBITDA −40% vs FY2023) plus vendor basis below issuer.
  - [C02] **Material** · Normalisation sensitivity · Current – sensitivity: FY2023-25 average EBITDA → EUR 9.27; issuer comparable EBITDA 1,683 → EUR 13.41; EV/Sales raw → EUR 22.82.
  - [C04] **Material** · QA/run status · Current – inconsistent: run_state qa_C 'failed_provisional' vs qa_results re-grade; final_status 'in_progress'.
  - [C03] **Info** · Peer remediation · Current: SPM and SUBC (oilfield services) replaced by MPC and GALP on business fit.
  - [C05] **Info** · Growth input · Current: Payout > 1 capped at 1.0 gives g_eps ≈ 0; FY2025 ROE 1.96% is a trough (substituted_input).

## 5. Missing / uncorroborated inputs (summary)
- Peer EV components (debt/NCI/cash) not stored for SU and PRY peers; AI peer NCI not stored → shown as n/a.
- PRY: source_log.csv has 7 rows × 5 columns (no field-level URLs); annual-report cross-check not performed.
- AI: no relative_summary.md, no sensitivities.csv; target EV, EV/EBIT and EV/EBITDA bases not stored.
- ALFA: no sensitivities.csv.
- MT: 14 FAIL_OPEN QA items, 9 peers, vendor vs issuer EBIT unresolved.
- All runs: peer ISINs registry-mapped (issuer verification pending); inputs from one vendor (StockAnalysis) with issuer figures as sensitivities only; access dates 30-Oct to 2-Nov-2026 (no look-ahead evident).

## 6. 'Needs discussion' (|official RV mid vs price| > 50%, recomputed from the 20 PPT_Link snapshots)

- EDPR.LS: -68.6%
- ENEL.MI: +90.8%
- ENGI.PA: +94.2%
- ENR.DE: -65.2%
- BP.L: +74.2%
- NESTE.HE: -76.3%