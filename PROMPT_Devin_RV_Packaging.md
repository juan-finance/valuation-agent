# TASK: Package the relative valuations of all 20 companies (1 Excel + 1 PDF each, plus a master summary)

You work inside this repository. Everything you need is already in it. Do not ask me to attach files.
Read first, in this order: `AGENTS.md` (operating rules: be efficient, no narration, write to disk in batches),
then `packaging/README_PACKAGING.md`, then the three spec files it points to. Do not read lecture notes, DCF files,
examples/ or the method guides unless a specific doubt remains.

## 1. Goal
The relative valuations (stage 3) of the 20 companies are finished and live in `outputs/<TICKER>_2026-10-30/`.
You are NOT re-running any valuation. You package each company's existing results into two standardised
deliverables so a separately built DCF can be placed beside them in a final PowerPoint:

| Deliverable | Name | Spec |
|---|---|---|
| Excel, one per company | `RV_<TICKER>.xlsx` (e.g. `RV_VER.VI.xlsx`), 13 sheets, live formulas | `packaging/SPEC_excel.md` |
| PDF, one per company | `RV_<TICKER>.pdf`, 4-6 pages + 1-page methodology appendix | `packaging/SPEC_pdf.md` |
| Master workbook | `RV_All_Companies_Summary.xlsx` (sheets Summary, Flags) | `packaging/SPEC_excel.md` section 5 |
| Log | `packaging_log.md` | section 6 below |

Every company must have identical structure, labels, units and cell positions. Companies: the 20 rows of
`packaging/company_master.csv` (AI.PA, ALFA.ST, BP.L, EDPR.LS, ENEL.MI, ENGI.PA, ENR.DE, EQNR.OL, IBE.MC, MT.AS,
NESTE.HE, NKT.CO, ORSTED.CO, PRY.MI, SHEL.L, SSE.L, SU.PA, TTE.PA, VER.VI, VWS.CO). There are no "not run" companies.

## 2. Hard rules
1. Source of truth: numbers from CSV/XLSX/JSON files; narrative from `.md` files. If a figure differs between files by
   more than 0.5%, use the CSV value and log the conflict in sheet QA_Flags and in packaging_log.md.
2. Never invent, estimate or round away a figure. Missing = `n/a - not in run files`, and log it.
3. Do not change peers, multiples, weights, statuses or conclusions. Do not fetch new data. Do not edit `methodology/`,
   `memory/standing_approvals.md` or any existing run file. All your work goes under `packaging/` and `outputs_packaged/`.
4. The only data you may add: (a) the ECB FX rate for 30 Oct 2026, taken first from `cache/macro/2026-10-30.json`
   and labelled `[FX added in packaging]` only if you had to add it; (b) ISIN/exchange from `packaging/inputs/`
   (SPIF list) if present. Nothing else.
5. No Buy/Hold/Sell, no blended "fair value" mixing RV and regression, no DCF numbers (AI.PA and MT.AS folders contain
   DCF files: ignore them completely, also `recommendation_summary.csv`, `report.pdf`, `report.md`).
6. Keep every run status and warning exactly as the run states it (PROVISIONAL, "human Spot_check PENDING", etc.).
   Never drop a flag to make a report look cleaner. Keep the "Academic analysis only; not investment advice" line.
7. Where a recomputed value differs from the run's reported value by >0.5%, keep the run's value as official, fill the
   cell amber, log it. Never override.

## 3. What is different from a generic packaging job (read `packaging/KNOWN_ISSUES.md` for details)
- Four format families exist (column `format_family` in company_master.csv). Use ONE generic builder with a small
  adapter per family, not 20 bespoke scripts. Family C (AI.PA, MT.AS, SU.PA, PRY.MI) has fewer columns and no
  `is_primary` column; take primary multiple from the summary text/`valuation_summary.md`.
- `multiples_summary.csv` holds two sets of per-share values where a multiple is scaled: `value_per_share_*` is the run's
  reported (adjusted) value, `raw_value_*` the unadjusted one. Report both, label which is headline, recompute both.
- The primary multiple differs by company (EV/EBITDA, P/E growth-scaled, EV/EBIT, P/BV). Do not assume EV/EBITDA.
- Reporting currency, trading currency and the currency of the run's per-share figures can all differ
  (ORSTED, NKT, VWS, SHEL, TTE, BP, EQNR, ALFA, MT). The run's price currency is not always stated in the CSV:
  read `relative_inputs.md` / `relative_summary.md`, state it, and add trading-currency columns where they differ.
- EDPR.LS: show both vendor and issuer-basis EBITDA rows, keep the run headline, raise it as a Point for the group.
- BP.L: EV/EBITDA regression is DIAGNOSTIC ONLY, no chosen model. PPT_Link rows 14-17 follow the rule in SPEC_excel.md.
- Cluster: the repo uses buckets A-F (internal, `methodology/company_universe.md`); the SPIF list uses clusters A/B/C.
  If `packaging/inputs/SPIF_20_Selected_Companies.pdf` exists, use its cluster, ISIN, exchange and currencies. If not,
  use the repo bucket, label the field `bucket (repo)` and log "SPIF cluster pending" once. Do not guess.
- Three runs show `final_status: in_progress` in run_state.json (IBE.MC, NESTE.HE, NKT.CO) while their summaries say
  provisional. Report the status as written in relative_summary.md / qa_results.md AND log the discrepancy.

## 4. Workflow (stop points are mandatory)
Follow AGENTS.md: one stage per session, commit at the end of each stage, short stage messages.
1. **Inventory** (no building). For each of the 20 folders list which files of `packaging/SPEC_excel.md` section 1 exist.
   Write `packaging/inventory.md` (gaps only + format family). Compare with `company_master.csv`; report differences.
2. **Builder.** Write `packaging/build/` (generic Python builder, openpyxl for xlsx, matplotlib for the PNG chart,
   reportlab for the PDF). Reuse `src/valuation_agent` helpers where they fit; do not duplicate the stats code, but the
   Excel formulas themselves must be live Excel formulas.
3. **Pilot: VER.VI.** Build `RV_VER.VI.xlsx` and `RV_VER.VI.pdf`. Recalculate with LibreOffice headless, run the
   QA of section 5, show me the two files, then STOP and wait for my confirmation of layout and style.
4. **Batch.** After my OK, build the other 19 with the same template, no more questions. Process by format family,
   write to disk after each company. Fix the template once if something breaks; do not hand-patch single companies.
5. **Master** `RV_All_Companies_Summary.xlsx`: link to each company's PPT_Link sheet (or copy values with a source
   column), 20 rows, flag |RV mid vs price| > 50% as "needs discussion" (computed, not hard-coded).
6. **Final QA and output**: `outputs_packaged/RV_Packaged_2026-10-30.zip` = 20 xlsx + 20 pdf + master + packaging_log.md.

## 5. Final QA (run once, record in packaging_log.md)
- Recalculate each xlsx with LibreOffice headless; zero `#REF! #DIV/0! #N/A #NAME? #VALUE!` outside intended blanks.
- PPT_Link B1:B21 filled for all 20 (B22:B23 blank and yellow; B24 formula returns "").
- Each PDF: A4, 4-6 report pages + 1 appendix page (5-7 total); all 10 sections + appendix present; headline box numbers equal PPT_Link.
- Headline control: PPT_Link B6, B8-B12, B15-B16 must equal `company_master.csv` columns (price_in_run, primary_median,
  val_low/mid/high, r2, reg_value) within 0.5%. Differences are logged, not silently fixed.
- List every amber check and every n/a in `packaging_log.md` sections: Conflicts, Missing fields, FX added, Check failures,
  Status discrepancies, Companies with |RV mid vs price| > 50%.

## 6. Definition of done
The zip exists; log is complete; I can open any `RV_<TICKER>.xlsx`, copy PPT_Link!B6:B24 into a PowerPoint table
and get the same layout for every company; the PDFs read identically in structure.
