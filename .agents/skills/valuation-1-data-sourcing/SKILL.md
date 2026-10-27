---
name: valuation-1-data-sourcing
description: Stage 1 of a company valuation. Confirms company identity, ticker and exchange, sources financial data from annual reports, cross-checks it with public sources, flags abnormal year-on-year changes and normalizes missing or unusual values. Use before any DCF or relative valuation.
---

# Goal
Produce a verified, normalized data pack for ONE company. Read /lecture_notes first for
any definitions. Where my rules and the lecture notes differ, the lecture notes win.

0. Read methodology/data_sources.md. These are indicative sources; others are allowed.
   Replace US-only sources with the European equivalents listed there.

# Procedure
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
   a. Normalized value from Thomson Reuters/LSEG, ONLY if the user attached it.
   b. Average of past years' ROE or debt ratio, if that ratio is stable. State the test used.
   c. If not stable, Damodaran industry data (Europe first, then global):
      https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html
5. ANOMALY CHECK (very important). For each line item compute the year-on-year change and
   the deviation from the 5-year average. Flag changes above +/-30% (default threshold).
   For each flag, in this order:
   i.   Write it in anomaly_report.md FIRST.
   ii.  Search news and the annual report for the cause.
   iii. If there is news AND analysts agree it is the new status quo, keep the value.
        Otherwise normalize it using the order in step 4. Record the decision and reason.
6. Log every number in source_log.csv (item, value, source URL, date, document page).

# Outputs (in /outputs/<ticker>_<date>/)
company_identity.md, data_pack.xlsx, anomaly_report.md, source_log.csv.
Post a short summary to the user. If any anomaly is material, say so clearly.

# Rules
- Prefer annual reports over aggregators. Cite source and date for every number.
- If sources conflict, flag it. Never choose silently. Never invent data.
- London shares are quoted in pence (GBp): divide by 100 before comparing with GBP/USD data.
- Free sources only unless the user attached other data.
