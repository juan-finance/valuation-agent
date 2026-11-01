# Relative valuation by regression — BP.L, Europe, 2026-10-30


## Headline
Conditional market-wide EV/EBITDA 18.072785x, GBP23.5868/ordinary share; NOT a recommendation. Published R2 26.2%. Comparable method blocked, so no independent corroboration. The large gap to GBP6.274 is model/definition risk, not evidence of mispricing.

## Data
Uniform vendor FY2025 fields retained; issuer cross-checks and claim scope separate. Growth substitution is approved fundamental g_eps=0 (closing common ROE x capped retention), g_rev=g_eps fallback; sourced3Y consensus12.99%/2.45% does NOT meet next5Y definition and is not passed as such. Beta negative replaced using resolved cash-corrected unlevered industry beta .41 and source marginal tax24.71%. Payout93.6667 retained; only retention capped. Regression ROE closing common, peer ROE average common. DFR gross debt / debt+current equity. Effective tax expense/pretax. Fiscal bridge frozen at Dec31,2025; quote Oct30,2026, not a current net-debt estimate.

## Fitted model
$\text{PE} = \underset{(8.29)}{9.72} + \underset{(4.85)}{2.99} \, \text{Beta} + \underset{(11.95)}{49.82} \, g_{\text{EPS}} + \underset{(9.22)}{7.98} \, \text{Payout}$
Published R2=0.201; status=not selected: near-zero reported NI and extreme payout

$\text{PBV} = \underset{(3.70)}{0.73} + \underset{(5.87)}{3.92} \, g_{\text{EPS}} + \underset{(1.38)}{0.13} \, \text{Beta} + \underset{(24.81)}{10.75} \, \text{ROE} - \underset{(2.43)}{0.25} \, \text{Payout Ratio}$
Published R2=0.423; status=not valued: negative prediction

$\text{EV/EBITDA} = \underset{(28.40)}{18.15} + \underset{(13.96)}{35.25} \, g - \underset{(10.65)}{0.11} \, \text{DFR} - \underset{(5.19)}{0.12} \, \text{Tax Rate} + \underset{(5.06)}{2.29} \, \text{ROIC}$
Published R2=0.262; status=conditional point estimate

## Diagnostics
n/a_published_route: n, SEy, p-values, adjustedR2, A/B/C, typicality, D1–D10, residual classification, own-estimation sample schema and LINEST. Integrity finds EUROPE views agree; flagged GLOBAL PEG sign/identical-t and GLOBAL PBV sign and EM EV/EBITDA sign are NOT used. DFR/tax ambiguity addressed by standing decimal approval, both policies disclosed. Recalculation/library comparison is saved separately.

## Valuation results (sorted from most undervalued to most overvalued)
| model     |   predicted |   published_r2 |     actual |   deviation |   value_per_share_gbp | status                                                 |
|:----------|------------:|---------------:|-----------:|------------:|----------------------:|:-------------------------------------------------------|
| EV/EBITDA |     18.0728 |          0.262 |    6.19272 |   -0.657346 |              23.5868  | conditional point estimate                             |
| PE        |    758.921  |          0.201 | 2405.18    |    2.16921  |               1.97967 | not selected: near-zero reported NI and extreme payout |
| PBV       |    -22.6    |          0.423 |    2.44913 |  nan        |             nan       | not valued: negative prediction                        |

## Robustness
| scenario                                                         |   EBITDA_usdm |   multiple_held_fixed |   GBP_per_share | note                                                                               |
|:-----------------------------------------------------------------|--------------:|----------------------:|----------------:|:-----------------------------------------------------------------------------------|
| EBITDA -20% mechanical stress                                    |       24134.4 |              18.0728  |        18.3193  | mechanical conditional sensitivity, not commodity forecast or peer dispersion      |
| base vendor EBITDA                                               |       30168   |              18.0728  |        23.5868  | mechanical conditional sensitivity, not commodity forecast or peer dispersion      |
| EBITDA +20% mechanical stress                                    |       36201.6 |              18.0728  |        28.8543  | mechanical conditional sensitivity, not commodity forecast or peer dispersion      |
| issuer PBIT + DDA parallel                                       |       30464   |              18.0728  |        23.8452  | mechanical conditional sensitivity, not commodity forecast or peer dispersion      |
| issuer impairment-addback parallel                               |       36501   |              18.0728  |        29.1157  | mechanical conditional sensitivity, not commodity forecast or peer dispersion      |
| full FY decommissioning provision as incremental debt-like claim |       30168   |              18.0728  |        22.9949  | conservative stress only; may double-count operating provision economics, not base |
| percentage-point DFR/tax unit alternative                        |       30168   |               4.27672 |         3.48181 | not user-approved base; illustrative unit risk                                     |
Alternative policy numbers in regression_results.json. No fake Global-equation check or robustness refit. Peer plausibility check unavailable because the qualified sector median is blocked; candidate diagnostics explicitly unqualified.

## Key warnings
PROVISIONAL. Comparable valuation BLOCKED: no certified peer panel, missing uniform associate/other-claims adjustments and no registered matching Damodaran industry-median dataset. Human Spot_check pending, never asserted performed. No target peer price or upside is reported. Candidate scores are an audit, not a compliant selected panel.
Regulatory/commodity exposure, extreme payout, tiny NI and high effective tax make extrapolation severe. Negative PBV never clipped to zero. PE considered but not primary for integrated oil earnings distorted by impairments.

## Limitations
Equations Jan1,2026 are302 days old, >6months. Market-wide, lowR2, no sector structure or residual dispersion. Approved growth proxy differs from analyst5Y growth. Damodaran EV/invested-capital definitions undocumented. Regression EV retains associates; peer EV removes them only when earnings excluded. Debt72,529 includes leases14,571. NCI20,948 includes hybrid15,955; no double deduction. Preference21 carrying proxy deducted separately. No associates addback in regression inverse. Common equity53,031 excludes preference. Fiscal claims stale vs quote; current bridge and fair values could differ materially. No DCF-proximity tuning, blending, recommendation, stage4 or DATA_BASE_MSCI.xlsx.

## Sources
https://stockanalysis.com/quote/lon/BP/financials/income-statement/ | https://stockanalysis.com/quote/lon/BP/financials/balance-sheet/ | https://stockanalysis.com/quote/lon/BP/financials/cash-flow-statement/ | https://stockanalysis.com/quote/lon/BP/statistics/ | https://stockanalysis.com/quote/lon/BP/history/
https://www.sec.gov/Archives/edgar/data/313807/000031380726000006/R5.htm
damodaran/2026-01/regressions_multi.md sha256 a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5
See source_log.csv (one row/source) and issuer_crosschecks.json. Academic analysis only; not investment advice.
