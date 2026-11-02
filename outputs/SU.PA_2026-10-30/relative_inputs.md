# SU.PA — reduced input step (relative_only deviation)

Valuation date: 2026-10-30. Earnings basis: FY2025 = Schneider Electric fiscal year ended 31 December 2025
(calendar FY). Reporting = trading currency: EUR (Euronext Paris). No full stage 1 (no data_pack.xlsx, no
anomaly report); one line per source in source_log.csv.

## Identity
- Schneider Electric SE, Euronext Paris (SU), ISIN FR0000121972. Sector: electrical equipment / energy
  management + industrial automation (bucket D). Single share class. In IEUR proxy universe (universe.csv
  row SU).
- Shares outstanding: 563.05m (vendor statistics, −0.99% QoQ — buybacks net of issuance; filing-date shares
  FY2025: 562.22m; FY2025 basic weighted 562m, diluted 571m). Current count used for market value.
- Price 2026-10-30 close: EUR 237.50 (vendor history). Market cap = 237.50 × 563.05m = EUR ~133.72bn
  (vendor snapshot 133.72B — exact match).
- FY2025 dividend: EUR 4.20/share declared (progressive, +8%; to be paid 2026); cash dividends paid in
  FY2025: EUR 2,191m.

## FY2025 figures (EUR millions, year ended 31 Dec 2025)

| Field | stockanalysis FY2025 | Schneider Electric FY2025 results release (26 Feb 2026) | Note |
|---|---|---|---|
| Revenue | 40,152 | 40,152 | exact match |
| EBITDA | 7,927 | adj. EBITA 7,520; EBITA 7,156 | vendor EBITDA = EBIT 6,967 + D&A-for-EBITDA 960; issuer adj. EBITA is a different aggregate; both recorded |
| EBIT (operating income) | 6,967 | EBITA 7,156 = adj EBITA − restructuring −287 − other op. −77; EBITA − PPA amort −457 → ~6,699 | vendor EBIT is IFRS operating profit before unusual items (EBT-excl.-unusual basis 6,531 pretax); issuer-reported profit includes impairment of associates −388 |
| D&A | 960 (D&A for EBITDA) / 1,333 + 319 amort (CF) | – | multiple vendor bases recorded |
| Net income to common (Group share) | 4,163 | 4,163 | exact match |
| Pretax income / tax | 5,806 / 1,455 | 1,455 tax | effective tax 25.06% |
| Total common equity | 24,199 | – | parent common equity; shareholders' equity 24,455 incl. NCI 256 |
| Minority interest (NCI) | 256 | P&L NCI −188 | BS vs IS lines, both recorded |
| Total debt | 19,909 | – | incl. leases (current 307 + LT 1,247 = 1,554) |
| Cash & equivalents | 4,634 | – | cash & ST investments |
| Long-term investments | 1,388 | – | proxy for non-operating investments/associates (SU has associates; impairment −388 in FY2025) |
| Total assets | 62,504 | – | |
| CFO | 6,131 | FCF 4,635 (issuer definition) | issuer FCF = CFO − net capex/other per its definition |
| CapEx | 1,072 | – | cash capex; plus intangibles purchase 471 |
| Dividends paid (CF) | 2,191 | declared DPS 4.20 × ~562m = ~2,361 | declared basis used for payout |
| Beta (5Y) | 1.19 | – | vendor observed; index/frequency unverified |
| Analyst growth | EPS +20.40% (3Y), Revenue +11.56% (3Y) | FY26 target: adj. EBITA organic +10–15% | consensus, used for published-route inputs |
| Issuer-adjusted measures | – | adj. EBITA 7,520; adj. net income 4,829; adj. EPS 8.59 | kept separate from reported basis |

## Regression (published route) inputs derived
- roe (closing book) = 4,163 / 24,199 = 0.1720 (avg-equity scoring basis 4,163 / ((24,199+30,489)/2) = 0.1522)
- payout = declared dividend (4.20 × 562.22m ≈ 2,361) / NI to common 4,163 = 0.567; vendor payout ratio
  49.87% (different denominator basis — TTM/adjusted); CF-paid basis 2,191/4,163 = 0.526 not used
  (final-dividend timing)
- dfr = 19,909 / (19,909 + 133,720) = 0.1296 (market equity in EUR millions at 2026-10-30)
- tax_rate = 0.2506 effective FY2025 (reported lines)
- roic = 6,967 × (1 − 0.2506) / (24,199 + 19,909 − 4,634) = 5,221 / 39,474 = 0.1323
- g_eps = 0.2040 consensus; g_rev = 0.1156 consensus (no fundamental substitution needed)
- fundamental scoring growth = 0.1522 × (1 − 0.567) = 0.0659

## Cache coverage check (stage 0 top-up decision)
- Country France: present in cache (Aa3, spread 0.48%, CRP 0.74%, mature ERP 4.20% — built for AI.PA).
- Currency EUR: reporting currency; FX not needed (peer EUR conversion uses ECB snapshot rates).
- EUROPE PE/PBV/EV-EBITDA published equations resolve for 'FR' (verified at stage 0 MANIFEST).
- Conclusion: no stage-0 top-up required; existing dated cache is sufficient.

## Sources (one line each)
- S1: https://stockanalysis.com/quote/epar/SU/ financials + balance-sheet + cash-flow-statement +
  statistics + history + profile (reused dated cache extract cache/market/2026-10-30/candidates/SU_*,
  accessed 2026-10-30/31; all pages 200 OK) — uniform vendor extract.
- S2: Schneider Electric FY 2025 Full-Year Results press release (26 Feb 2026):
  https://www.se.com/ww/en/assets/564/document/528237/release-fy-results-2025.pdf and 2025 Universal
  Registration Document summary table (accessed 2026-11-02): revenues 40,152; adj. EBITA 7,520 (18.7%);
  EBITA 7,156; net income Group share 4,163; adj. net income 4,829; adj. EPS 8.59; DPS 4.20; FCF 4,635.
- S3: cache/market/2026-10-30/universe.csv (IEUR proxy membership; SU row Industrials/France/Euronext Paris).
- S4: cache/macro/2026-10-30.json — ECB FX snapshot and France macro fields.
