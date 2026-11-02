# SSE.L — reduced input step (relative_only deviation)

Valuation date: 2026-10-30. Earnings basis: FY2025 = SSE fiscal year ended 31 March 2025 (non-December FY; latest full FY as labelled, not calendarized — flagged). Reporting = trading currency: GBP (quote in pence). No full stage 1 (no data_pack.xlsx, no anomaly report); one line per source in source_log.csv.

## Identity
- SSE plc, London Stock Exchange (LSE:SSE), ISIN GB0007908733. Sector: Utilities / integrated electricity utility — regulated networks (SSEN Transmission/Distribution), renewables generation, thermal/flex, energy customer solutions (bucket A). Single share class. In IEUR proxy universe (universe.csv row SSE).
- Shares outstanding: 1,210m (vendor statistics "Shares Outstanding 1.21B", +7.08% QoQ — post a 2026 equity issue; issuer shares in issue at 31.03.2025: 1,106.3m; weighted FY2025 basic 1,099.2m). Current count used for market value; weighted basis flagged for EPS.
- Price 2026-10-30 close: GBp 2,627.0 = GBP 26.27 (vendor history, LSE). Market cap = 26.27 × 1,210m = GBP ~31.79bn (vendor snapshot 31.69B; gap 0.3% — shares rounding).
- Equity raise: vendor statistics show +7.08% QoQ share growth (~100m new shares during 2026); consistent with SSE's enlarged investment programme funding; recorded as a corporate-action flag, not verified to an issuer announcement here.
- Hybrids: SSE pays a hybrid equity coupon (£73.7m FY2025, "other equity holders"); vendor "Total Debt" 10,712m − cash 1,091m = 9,621m net vs issuer reported net debt 9,513.9m and adjusted net debt AND hybrid capital 10,186.7m — vendor total debt appears to include the equity-classified hybrid capital as debt. Uniform EV bridge keeps vendor Total Debt; disclosed in flags.
- FY2025 dividend: GBp 64.2/share declared (interim 21.2p paid + final 43.0p proposed); cash paid basis £475.8m.

## FY2025 figures (GBP millions, year ended 31 Mar 2025)

| Field | stockanalysis FY2025 | SSE issuer FY2024/25 preliminary results (21 May 2025) | Note |
|---|---|---|---|
| Revenue | 10,132 | 10,131.9 | exact match |
| EBITDA | 2,850 | reported 2,738.3; adjusted 3,349.3 | vendor ~4% above issuer reported; adjusted basis retained as sensitivity |
| EBIT (operating income) | 2,250 | reported operating profit 1,962.2 | +14.7% gap: vendor EBIT = EBITDA − D&A For EBITDA; issuer includes JV/associates share and exceptional remeasurements differently; normalized alternative exists (>10% flag) |
| D&A | 599.9 (D&A for EBITDA) / 665.6 (CF) | – | multiple vendor bases recorded |
| Net income to common | 1,189 | reported attributable to ordinary shareholders 1,189.4 | exact match (after NCI 69.8 and hybrid coupon 73.7) |
| Pretax income / tax | 1,851 / 518 | 1,850.9 / 518.0 | effective tax 27.99% on reported lines; issuer-stated reported ETR 29.4% recorded |
| Total common equity | 12,064 | – | parent common equity; shareholders' equity 12,693 incl. NCI 628.8 |
| Minority interest (NCI) | 628.8 | profits attributable to NCI 69.8 | BS vs IS lines, both recorded |
| Total debt | 10,712 | reported net debt 9,513.9; adjusted net debt + hybrid capital 10,186.7 | vendor gross incl. leases and (apparently) hybrid capital; both recorded |
| Cash & equivalents | 1,091 | – | plus restricted cash 19.2 |
| Associates / long-term investments | 1,996 | – | proxy for equity-accounted JVs/associates (SSE has material JV stakes, e.g. Scotia Gas Networks retained stake, wind JVs) |
| Total assets | 30,364 | – | |
| CFO | 2,477 | – | |
| CapEx | 2,689 | adjusted capital investment 2,910.4; reported investment 3,837.0 | issuer basis broader (acquisitions, intangibles); vendor CF basis kept |
| Dividends paid (CF) | 475.8 | declared DPS 64.2p × 1,106.3m = ~710 | declared basis used for payout (cash-paid underweights timing of final dividend) |
| Beta (5Y) | 0.53 | – | vendor observed; index/frequency unverified |
| Analyst growth | EPS +15.19% (3Y), Revenue +7.71% (3Y) | – | consensus, used for published-route inputs |
| Issuer-adjusted measures | – | adj. operating profit 2,419.2; adj. EBITDA 3,349.3; adj. EPS 160.9p; adj. PAT attributable 1,768.1 | kept separate from reported basis |
| Ratings | – | not captured this step | not needed for stage 3 |

## Regression (published route) inputs derived
- roe (closing book) = 1,189 / 12,064 = 0.0986 (avg-equity scoring basis 0.1020)
- payout = declared dividend (0.642 × 1,106.3m = ~710.2) / NI to common 1,189 = 0.597; CF-paid basis 475.8/1,189 = 0.400 not used (final-dividend timing)
- dfr = 10,712 / (10,712 + 31,690) = 0.2526 (market equity in GBP millions)
- tax_rate = 0.2799 effective FY2025 (reported lines; issuer-stated reported ETR 29.4% noted)
- roic = 2,250 × (1 − 0.2799) / (12,064 + 10,712 − 1,091) = 0.0747
- g_eps = 0.1519 consensus; g_rev = 0.0771 consensus (no fundamental substitution needed)
- fundamental scoring growth = 0.1020 × (1 − 0.597) = 0.0411

## Cache coverage check (stage 0 top-up decision)
- Country United Kingdom: present in cache (Aa3, spread 0.48%, CRP 0.74%, ERP 4.94% — BP.L top-up).
- Currency GBP: ECB FX rate 0.8338 per EUR in snapshot; GBP 10y default-free 4.8287% present (not needed — stage 3 does not discount).
- EUROPE PE/PBV/EV-EBITDA published equations resolve for 'United Kingdom' (verified in stage 3).
- Conclusion: no stage-0 top-up required; existing dated cache is sufficient.

## Sources (one line each)
- S1: https://stockanalysis.com/quote/lon/SSE/financials/ + balance-sheet + cash-flow-statement + statistics + history + profile (accessed 2026-11-02; reused EDPRpool_SSE_* dated cache extract, all pages 200 OK) — uniform vendor extract.
- S2: SSE plc Preliminary Results for the year ended 31 March 2025 (LSE RNS 4968J, published 2025-05-21): https://www.londonstockexchange.com/en/news/article/SSE/preliminary-results-for-the-year-ended-31-march-25/17046625 and SSE FY25 preliminary results statement PDF https://www.sse.com/media/0oyhxdqq/fy25-preliminary-results-statement.pdf (consolidated income statement p.46; accessed 2026-11-02): revenue 10,131.9, reported op profit 1,962.2, EBITDA reported 2,738.3/adjusted 3,349.3, PBT 1,850.9, tax 518.0, PAT 1,332.9, attributable 1,189.4, EPS 108.2p, DPS 64.2p, net debt and hybrid capital 9,513.9 (adjusted 10,186.7).
- S3: cache/market/2026-10-30/universe.csv (IEUR proxy membership; SSE row Utilities/United Kingdom/LSE).
- S4: cache/macro/2026-10-30.json — ECB FX (GBP 0.8338 per EUR) and UK macro fields.
