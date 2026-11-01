# EDPR.LS — reduced input step (relative_only deviation)

Valuation date: 2026-10-30. Earnings basis: FY2025 (Dec year-end, IFRS). Reporting = trading currency: EUR. No full stage 1 (no data_pack.xlsx, no anomaly report); one line per source in source_log.csv.

## Identity
- EDP Renováveis S.A., Euronext Lisbon, ISIN ES0127797019. Sector: Utilities / renewable developer-operator (bucket B). EDP S.A. holds ~71% of EDPR -> EDP itself is hard-excluded from the EDPR peer set.
- Shares outstanding: ~1,051m (stockanalysis filing-date shares; statistics "Shares Out 1.06B").
- Price 2026-10-30 close: EUR 12.50 (stockanalysis history, Euronext Lisbon). Market cap = 12.50 x 1,051m = EUR ~13.1bn (vendor snapshot 13.25B at a later quote; check within tolerance, recorded).
- Proposed scrip dividend EUR 0.13/share (EUR 132.1m total = 40% of recurring net profit), proposed for 2026 GSM.

## FY2025 figures (EUR millions)

| Field | stockanalysis FY2025 | EDPR FY25 Results Report | Note |
|---|---|---|---|
| Revenue | 2,267 | Revenues 2,688 (incl. income from institutional partnerships) | definitions differ; issuer total-revenues basis recorded |
| EBITDA | 1,187 | EBITDA 1,947; recurring 1,974 (ex-AR gains 1,855) | vendor EBITDA excludes equity-method/income items issuer includes; both retained |
| EBIT (operating income) | 303.07 | – | reported base |
| D&A | 933.83 (CF) / 945.01 (IS) | – | |
| Net income to common | 215.8 | 216 (equity holders); recurring 330 | match <0.1% |
| Pretax income | 476.2 | – | tax expense 168.43 -> effective 35.4% |
| Total common equity | 10,274 | Shareholders' equity 10,274 | exact match |
| Total equity | 12,180 | 12,180 (incl. minorities 1,906) | exact match |
| Total debt | 9,372 | Net debt 8,109 (Dec-25) | vendor total debt = gross debt incl. ST; leases not split by vendor ('-') |
| Cash & equivalents | 1,199 | – | |
| Minority interest (NCI) | 1,906 | – | |
| Associates / long-term investments | 1,158 (Long-Term Investments) | Equity MW consolidated 1,586 MW | equity-accounted associates basis; kept visible |
| CFO | 1,040 | Net cash-flow from operations 1,159 | ~11% gap, definitions differ; recorded |
| CapEx | 2,802 | Gross investment 2,398 | scope differs; recorded |
| Dividends paid | 40.4 (CF line 3.0 to shareholders per issuer) | Dividends paid to EDPR shareholders €3m cash | scrip programme: declared 132.1m for FY2025 |
| Beta (5Y) | 0.72 | – | vendor observed; index/frequency unverified |
| Analyst growth | EPS 20.42% (3Y), Revenue 8.51% (3Y) | – | consensus, used for published-route inputs |
| Effective tax rate | 35.37% (IS table) / 18.23% (statistics TTM) | – | FY basis 35.4% recorded with flag |

## Regression (published route) inputs derived
- roe (closing book) = 215.8 / 10,274 = 0.0210; recurring alternative 330/10,274 = 0.0321
- payout = proposed dividend 132.09 / 216 = 0.61 reported basis (0.40 on recurring NP per issuer policy); paid-cash basis 3/216 = 0.014 retained as flag
- dfr = 9,372 / (9,372 + 13,138) = 0.416
- tax_rate = 0.3537 effective FY2025
- roic = 303.07 x (1 - 0.3537) / (10,274 + 9,372 - 1,199) = 0.0106
- g_eps = 0.2042 consensus; g_rev = 0.0851 consensus (no fundamental substitution needed)

## Sources (one line each)
- S1: https://stockanalysis.com/quote/eli/EDPR/financials/ + balance-sheet + cash-flow-statement + statistics + history (accessed 2026-11-01) — uniform vendor extract.
- S2: https://www.edpr-investors.com/sites/edpr-investors/files/document/2026-02/FY25_ResultsReport_EDPR.pdf (accessed 2026-11-01) — issuer FY2025 results report; revenue/EBITDA/NI/equity/net-debt/dividend cross-checks.
- S3: universe row cache/market/2026-10-30/universe.csv line 437 (IEUR proxy membership).
- S4: cache/macro/2026-10-30.json — ECB FX and macro snapshot (EUR = base, no conversion needed).
