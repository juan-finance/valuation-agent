# Data sources and evidence requirements

Use this file with [DCF procedure](dcf_procedure.md). Sources are indicative, not exclusive. Locate the current or archived equivalent when a link is unavailable; log the substitution. Match every input to the valuation information cutoff. Do not use a later dataset for a historical valuation without disclosing look-ahead bias.

## Input map

| Input | Required evidence and field | Preferred source |
| --- | --- | --- |
| Identity, price, shares | ISIN, primary listing, share class, date, treasury shares, corporate actions and dilution | Official exchange, issuer annual/interim report and capital announcements; Morningstar cross-check |
| Five-year capital structure | Market cap, book debt/equity, market debt or proxy, ratios and target policy | Reports, debt fair-value notes, exchange prices; vendor data if available |
| Industry debt benchmark | Market Debt/(Debt+Equity), matched European industry and dataset vintage; ratio, not debt amount | Damodaran dbtfundEurope.xls via data index |
| Adjusted EBIT and NI | Reported-to-adjusted bridges, group/parent/NCI scope, annual and comparable interim figures | Issuer annual/interim results and alternative performance measure reconciliation |
| Effective tax | Tax expense, pretax earnings, five-year trend and exceptional items | Income statement and tax note |
| Marginal tax | Statutory corporate rate, jurisdiction/year, tax-shield relevance | Tax authority, OECD, PwC/KPMG; Damodaran Corporate Tax Rate as cross-check |
| CapEx and D&A | PP&E, intangibles, recurring acquisitions, cash acquired, depreciation, amortization, excluded impairment | Cash-flow statement and asset/acquisition notes; adjusted-earnings bridge |
| Industry net investment | Net CapEx / EBIT(1−t), with exact column and definition verified | Damodaran capexEurope.xls |
| NWC | Current assets, cash, current liabilities, current financing, annual sales | Balance sheet and notes; five years plus current/prior comparison |
| Industry working capital | Noncash working capital/Sales, exact column and scope verified | Damodaran wcdataEurope.xls |
| Book return capital | Beginning book equity, debt, cash, NCI and excluded nonoperating capital | Consolidated balance sheet and notes |
| Risk-free rate | Ten-year yield, currency, benchmark issuer, history and any normalization | ECB, Bundesbank, BoE, SNB, relevant central bank/official debt agency; FRED for USD |
| Sovereign default spread | Adj. Default Spread, rating, vintage; not equity CRP | Damodaran country table or justified sovereign CDS data |
| Mature ERP and equity CRP | Mature-market ERP and Country Risk Premium separately; total ERP is not an incremental CRP | Damodaran country table and archived datasets |
| Geographic revenue weights | Countries/regions, total denominator, coverage, regional proxy | Annual report geographic sales disclosure; country spreadsheet for regional premiums |
| Bottom-up beta | Unlevered beta corrected for cash, business mix, Europe/global scope | Damodaran betaEurope.xls or global equivalent; IFRS 8 segment note |
| Regression beta | Estimate, index, window, frequency, date, uncertainty if supplied | Bloomberg/Refinitiv exports, public vendors or documented own regression |
| Borrowing cost | Actual rating, adjusted EBIT/gross interest, synthetic rating mapping, long-term bond YTM | Issuer IR, rating agency, exchange bond data, Damodaran ratings/spreads table |
| Market Ke comparison | Multiple comparable estimates, method, date and whether genuinely implied | Public valuation research or accessible vendor estimates; distinguish CAPM estimates |
| Preferred/hybrid financing | Fair value, dividends/coupons, tax treatment and contractual conversion/write-down terms | Security prospectus, report financing notes, exchange quotes |
| Growth and terminal assumptions | Historical and analyst earnings growth, explicit sales growth, long-run inflation/economic growth | Issuer history/guidance, reliable analyst pages, central banks, Eurostat, IMF, OECD |
| Nonoperating bridge | Cash, financial assets, associates/JVs, pensions, NCI, provisions and overlap with cash flows | Report financial instruments, investments, pensions and provision notes |
| Distress | Going concern, liquidity, covenant/coverage and rating concerns | Reports and rating commentary |

## Dataset entry points

These links guide Devin's retrieval; individual spreadsheet contents must be opened and verified during the valuation. Do not assume a legacy filename or an example percentage is current.

- [Damodaran current and archived data index](https://pages.stern.nyu.edu/adamodar/New_Home_Page/datacurrent.html)
- [Country risk table](https://pages.stern.nyu.edu/adamodar/New_Home_Page/datafile/ctryprem.html)
- [Country risk spreadsheet](https://www.stern.nyu.edu/~adamodar/pc/datasets/ctryprem.xlsx)
- [European debt fundamentals](https://pages.stern.nyu.edu/~adamodar/pc/datasets/dbtfundEurope.xls)
- [European capital expenditure](https://pages.stern.nyu.edu/~adamodar/pc/datasets/capexEurope.xls)
- [European working capital](https://pages.stern.nyu.edu/~adamodar/pc/datasets/wcdataEurope.xls)
- [European betas](https://pages.stern.nyu.edu/~adamodar/pc/datasets/betaEurope.xls)
- [Ratings and spreads](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ratings.html)

The Word's 4.23% mature ERP and example sovereign spreads/ratings belong to its stated January 2026 setting. Verify the required vintage; never hardcode them as timeless inputs. Do not infer country equity risk from the cash-flow currency alone.

## Source ranking and inaccessible data

1. Issuer filings, official exchanges, security prospectuses and official macro/tax sources.
2. Damodaran datasets and primary research, central banks and official statistical agencies.
3. Accessible research and aggregators such as Morningstar, Investing.com and Yahoo Finance as corroboration; analyst estimates may be sourced there with their limitations stated.

Cross-check material inputs independently when possible; otherwise record the unavailable check. Do not fabricate agreement. European IFRS filings replace US-only SEC forms unless relevant to the actual issuer. Bloomberg, Datastream and LSEG/Refinitiv require authorized access or user-supplied exports; record export date and source, and never request credentials. CDS is not inherently Bloomberg-only: a legitimate alternative is acceptable if instrument, currency, maturity and date are verifiable.

## Required source_log.csv fields

Use: input_id, company, metric, value, unit, currency, period_start, period_end, as_of_date, publication_date, access_date, source_name, url_or_local_file, page_note_sheet_cell, dataset_vintage, reported_or_adjusted, consolidation_scope, method_or_formula, cross_check_source, status, limitation.

Use stable input IDs in workbook inputs and decisions. Derived numbers must reference their source input IDs and calculation, not pretend to be vendor observations. Mark each input sourced, derived, estimated, unavailable or unverified. Preserve original stage 1 entries and record replacements transparently. Cite only pages/files actually opened; a search snippet alone does not verify a company input.
