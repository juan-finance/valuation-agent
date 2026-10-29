# Data sources and evidence requirements

Use this file with [DCF procedure](dcf_procedure.md), [comparables procedure](comparables_procedure.md) and [regression procedure](regression_procedure.md). The existing DCF sources are indicative, not exclusive; the stage 3 route-specific rules below are stricter and govern relative datasets. Locate the current or archived equivalent when a link is unavailable; log the substitution. Match every input to the valuation information cutoff. Do not use a later dataset for a historical valuation without disclosing look-ahead bias.

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

The DCF instruction set's 4.23% mature ERP and example sovereign spreads/ratings belong to its January 2026 setting. Verify the required vintage; never hardcode them as timeless inputs. Do not infer country equity risk from the cash-flow currency alone.

## Source ranking and inaccessible data

1. Issuer filings, official exchanges, security prospectuses and official macro/tax sources.
2. Damodaran datasets and primary research, central banks and official statistical agencies.
3. Accessible research and aggregators such as Morningstar, Investing.com and Yahoo Finance as corroboration; analyst estimates may be sourced there with their limitations stated.

Cross-check material inputs independently when possible; otherwise record the unavailable check. Do not fabricate agreement. European IFRS filings replace US-only SEC forms unless relevant to the actual issuer. Bloomberg, Datastream and LSEG/Refinitiv require authorized access or user-supplied exports; record export date and source, and never request credentials. CDS is not inherently Bloomberg-only: a legitimate alternative is acceptable if instrument, currency, maturity and date are verifiable.

## Required source_log.csv fields

One schema for ALL stages (stage 1 creates the file with these columns; stages 2-3 append). The earlier five-column format (item, value, URL, date, page) is retired: item→metric, URL→url_or_local_file, date→as_of_date and access_date, page→page_note_sheet_cell. Write "n/a" where a field does not apply.

Use: input_id, company, metric, value, unit, currency, period_start, period_end, as_of_date, publication_date, access_date, source_name, url_or_local_file, page_note_sheet_cell, dataset_vintage, reported_or_adjusted, consolidation_scope, method_or_formula, cross_check_source, status, limitation.

Use stable input IDs in workbook inputs and decisions. Derived numbers must reference their source input IDs and calculation, not pretend to be vendor observations. Mark each input sourced, derived, estimated, unavailable or unverified. Preserve original stage 1 entries and record replacements transparently. Cite only pages/files actually opened; a search snippet alone does not verify a company input.

## Stage 3 data routes and sources

Confirm terminal-export availability once for the joint relative task; reuse a prior explicit route choice. Prefer a coherent export from Bloomberg, LSEG Workspace/Eikon or S&P Capital IQ. Verify field definitions in the actual terminal version; the following names are retrieval hints, not guaranteed commands or verified live fields.

- Bloomberg: index constituent screen MEMB or EQS membership filter for MSCI Europe/World (commonly MXEU/MXWO; verify); RV for peer candidates, FLDS to verify fields; BEst for consensus growth. Typical fields include PX_LAST, CUR_MKT_CAP, EQY_BETA/EQY_RAW_BETA, PE_RATIO, PX_TO_BOOK_RATIO, PX_TO_SALES_RATIO, RETURN_COM_EQY, DVD_PAYOUT_RATIO, ID_ISIN, CRNCY, COUNTRY and GICS classification names. Use raw fields to recompute ratios rather than trust a field label alone.
- LSEG Workspace/Eikon: Screener index constituents and peers, consistent fundamentals and I/B/E/S growth horizon; record exact fields and export date.
- Capital IQ: constituent screening, comparable-company candidates and raw fundamentals; preserve Name (Exchange:Ticker) layout.
- No export: use stockanalysis.com raw statistics, income statement, balance sheet, cash-flow statement and dividend pages uniformly. Do not use different sites' multiples or switch source for one missing company. A global source-policy change needs explicit authorization and consistent recollection; the generic DCF flexibility does not authorize piecemeal substitution.

| Relative input | Required source evidence |
| --- | --- |
| Index universe | MSCI/authorized terminal constituent list; otherwise dated tracking ETF holdings with all pages, reported count and exclusions reconciled; label proxy coverage |
| Candidate peers | Issuer-named competitors, same-industry screener and the agent's own research (no group workbook exists or will be supplied); verify membership and all hard filters separately |
| Raw financials | Price/current shares, parent common NI/EPS/book equity, consolidated sales/EBIT/EBITDA/assets, total debt with leases, cash, NCI, associates, CFO, CapEx, D&A, tax/pretax profit, dividends/DPS and dates/units |
| Earnings basis | Separate FY, TTM and NTM/next-FY series; matching fiscal dates and available interim data for any calendarization |
| Consensus growth | Consistent 3–5-year EPS horizon; source availability assessed before candidate exclusions; fallback coverage logged |
| Beta | Five-year regression estimate, benchmark, frequency/window/source; permitted bottom-up replacement using sourced industry beta, D/E and marginal tax |
| GICS | Terminal verified Sector/Industry Group/Industry; web industry-to-GICS mapping with official definitions, level and ambiguity flag |
| Developed-market filter | MSCI market classification at cutoff; listing location is a separate field |
| Ownership/events | Issuer reports/exchange announcements: target/parent/subsidiary, >20% stakes, restructuring and trading-history dates |
| ISIN | Final verification from exchange, MSCI or issuer IR; profile sites only as locators |
| FX | Dated ECB reference rates; record quotation direction and cross conversion; no silent current FX in historical models |
| Sector benchmark | Damodaran regional industry statistic with exact median/aggregate definition and period; do not relabel a weighted aggregate as a median |
| Published regression check | Open MReg26 January 2026 equations for Global and Western Europe & UK; exact multiple, units, transforms and coefficients |
| Relative PE / Tobin Q | Sourced home-index PE on matching basis / documented replacement-cost data; unavailable when not supported |

Use current reachable official pages during execution; historical statements that a particular holdings download was inaccessible are not permanent constraints. Prefer an accessible issuer holdings file over a secondary paginated proxy when available. Retain full universe provenance even when company figures come from the uniform web source.

Regression grows from its specified fundamental ROE×retention formula; terminal consensus is not silently substituted. Comparable scoring may use consensus or its prescribed pool-level fallback. DCF, peer-score and regression ROE/growth/beta fields may differ by definition: retain method-specific names and reconciliation.

## Stage 3 evidence and audit additions

Preserve the existing source_log.csv columns and append method, entity_id, target_ticker, field_id, price_date, earnings_basis, gics_level, universe_vintage, source_route, raw_value, normalized_value, transformation and review_status as needed. No sourced figure is accepted without an exact locator. Derived values reference raw input IDs and formula; do not cite them as vendor observations.

In output source_urls fields use `field: exact URL (accessed YYYY-MM-DD)`, separated by ` | `. For nonpublic terminal exports use terminal, ticker, field/screen, export date and local export locator; do not fabricate public URLs. A supplied source URL is a retrieval lead, not proof it was opened. Report source conflicts >2% with both locators and a reasoned resolution. Link judgments to business/segment/ownership evidence.

The master workbook must retain raw observations, membership/classification maps, clean-to-raw row IDs, beta/fallback/winsorization logs, source-linked Spot_check lists and review status. Uniform sourcing is compatible with independent report/exchange verification; such cross-checks must not silently replace isolated production inputs. DCF sourcing remains under its existing rules.
