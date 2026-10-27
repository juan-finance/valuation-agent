# Indicative data sources (the professor's list, adapted)
These sources are INDICATIVE, not exclusive. Use any other trustworthy source as well, and
always cross-check key figures against at least one independent source. Several links in
the original list are old: if a link is dead, find the current equivalent and record it.
Our companies are European and report under IFRS, so US-only sources (SEC EDGAR, 10-K, 10-Q)
are replaced by the equivalents below.

| Input | What is needed | Where to look |
|---|---|---|
| Risk-free rate | 10-year government yield in the cash-flow currency | ECB Data Portal, Bundesbank, Bank of England, FRED (USD); Bloomberg or CNN markets pages if accessible; Damodaran |
| Country default spread, ERP | Country rating, default spread, country/currency ERP | Damodaran "Risk Premiums for Other Markets"; Moody's and S&P sovereign ratings (public pages) |
| Beta | Market regression beta, bottom-up beta, leverage | Online regression betas (Morningstar, Yahoo Finance, Investing.com), Damodaran industry betas (Europe and global), own regression if time allows |
| Business breakdown | Segment revenue and EBIT | Annual report segment note (IFRS 8) |
| Cost of debt | Bond rating, synthetic rating, default spread, CDS | Rating agency public pages; synthetic rating from interest coverage using Damodaran's rating table; company bond yields where public. CDS only on Bloomberg (user must export it; not available otherwise) |
| Marginal tax rate | Statutory corporate rate by country | KPMG, PwC or OECD corporate tax tables (cite the year); also note any rate in the annual report tax note |
| Weights | Market value of equity and of debt | Exchange or Morningstar for market cap; annual report debt footnotes for maturity, coupons and fair value of debt |
| Cash flows | Earnings checks, leases, net capex, R&D, working capital | Annual report: income statement, cash flow statement, notes (leases, PP&E, intangibles, provisions) |
| Growth | Historical, analyst, fundamental growth | Annual report history; analyst estimates from trusted public pages (Morningstar, Zacks, exchange pages, Investing.com); fundamental growth computed by the agent |
| General data | Macro data, stock prices and returns | Yahoo Finance, Stooq, Quandl or Nasdaq Data Link, ECB, Eurostat, IMF, OECD |
| Financial distress | Bankruptcy and distress checks | Annual report going-concern notes; interest coverage; rating agency commentary |

## Sources that need a human (not available to the agent)
Bloomberg, Datastream and Thomson/LSEG Eikon. If the user exports data from these and
attaches it, use it and label it with the source and the date of the export. Otherwise,
say it was not available. Never ask for or store any login details.

## Source ranking and rules
1. Annual and interim reports, and official exchange pages.
2. Damodaran datasets, central banks, ECB, Eurostat, OECD.
3. Morningstar, Investing.com, Yahoo Finance and other aggregators, as cross-checks only.
Record the URL and access date for every figure in source_log.csv.
