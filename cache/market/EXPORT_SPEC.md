# Terminal export specification (use this if you have Bloomberg, LSEG Workspace or Capital IQ)

One coherent export is the fastest and most reliable route (`methodology/data_sources.md`: terminal export = full version). Export ONCE for
the batch valuation date and save it as `cache/market/<valuation_date>/export/<terminal>_<export_date>.xlsx` (or several sheets/CSVs in that folder).
Exact field names differ by terminal and version; use the closest field, write the field code next to each column header (a header row
plus a row below with the terminal field code), and put the export date and terminal version in a `README` sheet. Data must be as of the batch
valuation date (prices) and FY2025 for fundamentals; keep FY, TTM and next-year series in separate columns.

## Universe (rows)
All current constituents of MSCI Europe; then, as a second sheet, MSCI World constituents outside Europe (needed only if the comparables relaxation
or the World regression fallback is triggered). Include the 20 targets even if some are not constituents (flag them). Exclude nothing yourself:
the agent applies the exclusions (financials, REITs, etc.) and logs them. One row per security; include all share classes of an issuer.

## Columns (one per line; this is the superset needed by BOTH relative methods)
**Identification and classification:** name; exchange ticker; ISIN; country of listing; country of incorporation; price currency; reporting
currency; GICS sector, industry group, industry (names, and codes if available); MSCI market classification (developed/emerging); index
membership flag(s); fiscal year-end date.

**Market:** price and price date; shares outstanding by class (excluding treasury); market capitalisation (local and EUR if provided);
5-year monthly regression beta with the benchmark index named; dividend per share (last FY); dividend yield.

**Income statement (FY2025, plus TTM where available):** revenue; EBITDA; EBIT; depreciation and amortisation; interest expense (gross); pre-tax profit;
income tax expense; net income to parent common shareholders; net income including minorities; EPS (FY, TTM); next-fiscal-year consensus EPS.

**Balance sheet (latest FY end):** total assets; cash and equivalents; total financial debt including leases (short and long); non-controlling
interests; parent common book equity; equity-accounted investments (associates and JVs); preferred equity.

**Cash flow (FY2025):** cash from operations; capital expenditure; acquisitions (if separately available); dividends paid to common;
share repurchases.

**Growth:** consensus long-term (3-5 year) EPS growth, with the horizon and number of analysts.

**For the 20 targets and any peer on the final shortlist:** segment revenue and segment EBITDA (for the 50% pure-play test); listed
subsidiaries and holdings above 20%.

## Not needed from the terminal
Damodaran datasets, country risk premiums, ratings tables (the agent fetches those), and DCF-specific items (fair values of debt, adjusted EBIT reconciliations),
which come from annual reports in stages 1-2.
