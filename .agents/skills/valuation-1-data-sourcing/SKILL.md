---
name: valuation-1-data-sourcing
description: Stage 1 of a company valuation. Confirms company identity, ticker and exchange, sources financial data from annual reports, cross-checks it with public sources, flags abnormal year-on-year changes and normalizes missing or unusual values. Use before any DCF or relative valuation.
---

# Goal
Produce a verified, normalized data pack for ONE company. Setup (few minutes): follow AGENTS.md section 1, read
memory/companies/<ticker>.md, and read only methodology/data_sources.md (input map and source_log fields) and qa_checklist.md block A.
For definitions, grep knowledge/lecture_digest/ (do not open the PPTX files unless a doubt remains).
Use src/valuation_agent: anomaly.anomaly_table for step 5, sourcelog.SourceLog for step 6, runstate.RunState for checkpoints. Where my rules and the lecture notes differ, the lecture notes win; next
come the methodology procedures (methodology/dcf_procedure.md, which encodes Steps in Company
Valuation.docx together with its recorded corrections). See the precedence rules in the
company-valuation skill.

# Procedure
0. These are indicative sources; others are allowed. Replace US-only sources with the European equivalents listed in
   methodology/data_sources.md. Damodaran data comes from the data library (resolve with `datasets.resolve`, see data/README.md); families it lacks come from cache/damodaran/ (stage 0 step 0.1).
1. Identify the company. Confirm legal name, ISIN, ticker, exchange, country, reporting
   currency and fiscal year-end. Make sure it is exactly the company named by the user
   (not a subsidiary, ADR or similarly named firm). Write company_identity.md.
2. Source data from the annual reports (last 5 years plus the latest interim report):
   revenue, EBITDA, D&A, EBIT, interest, tax, net income, capex (read the narrative and
   tag organic-growth capex vs maintenance vs acquisitions), working capital, cash,
   financial and non-operating assets, gross debt (short/long), leases, hybrids,
   pensions, minorities, associates, book equity, shares outstanding, dividends, buybacks.
3. Cross-check every key figure against at least one independent public source
   (official exchange website, Morningstar, Investing.com, Bloomberg public pages, etc.).
   Record a discrepancy table. Explain differences (definitions, IFRS 16, restatements).
4. For missing or unusable values, normalize in this order:
   - a. Normalized value from Thomson Reuters/LSEG, ONLY if the user attached it.
   - b. Average of past years' ROE or debt ratio, if that ratio is stable. State the test used.
   - c. If not stable, Damodaran industry data (Europe first, then global), obtained ONLY via
      `datasets.resolve` (families it lacks come from cache/damodaran/, see step 1). If the resolver
      reports the dataset missing, ask the user to supply it; never read it straight from the website.
      (For locating the file only: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html)
5. ANOMALY CHECK (very important). For each line item compute the year-on-year change and
   the deviation from the 5-year average. Flag changes above +/-30% (default threshold).
   For each flag, in this order:
   - i. Write it in anomaly_report.md FIRST.
   - ii. Search news and the annual report for the cause.
   - iii. If there is news AND analysts agree it is the new status quo, keep the value.
     Otherwise normalize it using the order in step 4. Record the decision and reason.
6. Log every number in source_log.csv using the 21 fields defined in
   methodology/data_sources.md ("Required source_log.csv fields"): input_id, company,
   metric, value, unit, currency, period_start, period_end, as_of_date, publication_date,
   access_date, source_name, url_or_local_file, page_note_sheet_cell, dataset_vintage,
   reported_or_adjusted, consolidation_scope, method_or_formula, cross_check_source,
   status, limitation. (Old 5-column names map as: item→metric, value→value,
   URL→url_or_local_file, date→as_of_date/access_date, page→page_note_sheet_cell.) Write
   "n/a" in a field that does not apply; do not drop columns. Stages 2-3 append to this
   file and preserve these entries.

# Outputs (in outputs/<ticker>_<date>/)
company_identity.md, data_pack.xlsx, anomaly_report.md, source_log.csv (validate with sourcelog.validate), run_state.json.
Run the qa_checklist block A once. Write memory/companies/<ticker>.md (identity, perimeter, quirks, which sources worked) and
memory/source_playbook.md entries. Post a short summary to the user (include elapsed minutes). If any anomaly is material, say so clearly.
Then end the session; stage 2 starts fresh from the files.

# Rules
- Prefer annual reports over aggregators. Cite source and date for every number.
- If sources conflict, flag it. Never choose silently. Never invent data.
- London shares are quoted in pence (GBp): divide by 100 before comparing with GBP/USD data.
- Free sources only unless the user attached other data.
