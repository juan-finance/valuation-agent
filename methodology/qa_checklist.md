# QA checklist: run before delivering
Run each block after its stage, and run the whole list again before delivering.
Record the result of every item (pass / fail / fixed / not applicable) in /outputs.

## A. Identity and data (stage 1)
[ ] Ticker, exchange and company identity confirmed.
[ ] Historical financials tie to the annual report (revenue, EBITDA, net income,
    total assets, net debt). Balance sheet balances.
[ ] Anomaly report written and each flag resolved (kept or normalized, with reason).
[ ] Share count is current and diluted, with treasury shares excluded. It was checked in
    the annual report AND on the exchange, including recent capital increases and buybacks.
[ ] Net debt definition matches the company's own, with hybrids, leases,
    pensions, minorities and provisions treated per methodology/valuation_standards.md.
[ ] Currency and units consistent everywhere. GBp vs GBP checked for London stocks.
[ ] Every number has a source and a date, and is logged in source_log.csv.

## B. DCF (stage 2)
[ ] FCFE vs FCFF choice justified by debt-ratio stability (a cross-check with the
    other model is optional but, if run, both values are reported).
[ ] Model choice justified with verified literature or data (no invented citations).
[ ] Risk-free rate is net of the country default spread. Risk-free rate, ERP and beta have
    source and date, and the beta was compared with Damodaran's.
[ ] Cost of equity (and WACC if FCFF) is within a plausible range and compared with the
    market-implied rates.
[ ] Number of growth stages matches the 7% / 10-point rule.
[ ] Stable growth <= risk-free rate (any exception flagged). Terminal value share reported,
    and flagged if above 75%.
[ ] DCF-implied EV/EBITDA is compared with peers and with history.
[ ] Key value drivers identified and ranked. DCF summary picture produced.
[ ] Marginal tax rate and cost-of-debt method documented, with sources and dates.

## C. Relative valuation (stage 3)
[ ] Peers are in the right bucket, with consistent periods. Fewer than 4 peers is stated.
[ ] Choice of key multiples justified. Regression R-squared and input ranges checked.
[ ] Weights in the relative valuation sum to 100% and no weight exceeds 30%.
    The unweighted median is shown, and the effect of weighting toward the DCF is reported.

## D. Recommendation and report (stage 4)
[ ] Final value is compared with the current market price. Any gap above 25% is explained.
[ ] Fair value range and ONE recommended price stated. Mispricing in % and in currency.
[ ] Recommendation tied to the annual report narrative and one mispriced parameter.
[ ] Discussion of market expectations and current conditions included.
[ ] Extraordinary items commented on.
[ ] recommendation_summary.csv written.
[ ] Same method and thresholds as in the other companies, or deviations justified.
[ ] Data gaps section lists everything missing or estimated.
[ ] Plain-English summary is readable by a non-specialist. Glossary and disclaimer included.

