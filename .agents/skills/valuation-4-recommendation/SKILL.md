---
name: valuation-4-recommendation
description: Stage 4 of a company valuation. Combines the DCF and relative valuations with scenario and sensitivity analysis, reconciles the differences, discusses market expectations, compares with analyst recommendations and gives a fair value range, a recommended price and a Buy/Hold/Sell recommendation with visuals. Use after stages 2 and 3.
---

# Goal
Final analyst recommendation for investors with medium to low technical knowledge. Academic
exercise: the work is judged on the consistency and correctness of the decisions, not on
whether the recommendation proves right. The professor will calibrate this stage later, so
keep the structure easy to change.

# Required content
1. DCF: scenario analysis (bear/base/bull) and sensitivity to the main inputs (tornado chart
   and a WACC vs growth table). Identify the key value drivers and say why they matter.
2. Relative valuation: scenario analysis too (peer quartiles, alternative weights, multiples).
3. Reconciliation: an EXTENDED analysis of why DCF and relative valuation differ. Table of
   DCF assumptions vs the assumptions implied by relative valuation, with the factors that make
   them differ. Identify DCF assumptions that would bring the DCF closer to the multiples.
4. Market expectations and current conditions: discuss how expectations drive market prices
   today and how they affect (a) the DCF inputs and (b) the multiples of the peers.
5. Visual scale with the minimum and maximum valuations from stages 2 and 3.
6. Judge which scenario is most likely. Show a figure with the recommended valuation range.
7. Compare with analyst recommendations from highly trustworthy sources only (exchanges,
   LSEG/Thomson Reuters, Bloomberg, Morningstar). Say which sources you could access. Use the
   market's standard language (Buy / Hold / Sell, 12-month target price).
8. FINAL CONCLUSION, with these headings:
   - Fair value: a range (low / base / high) and ONE recommended price (12-month target).
   - Mispricing: current price vs fair value, in % and in currency.
   - Limitations: data gaps, model risk, assumptions that matter most.
   - Recommendation: Buy / Hold / Sell, with the thermometer figure and a short text tied
     to the annual-report narrative and to one parameter (margin, growth, cost of equity...)
     that the market may be mispricing. The recommendation must be marketable: a position
     an analyst at an exchange-listed brokerage could publish.
9. Write recommendation_summary.csv, one row, for the pool used in portfolio construction:
   ticker, company, exchange, currency, valuation_date, current_price, fair_value_low,
   fair_value_base, fair_value_high, recommended_price, upside_pct, rating, model_used,
   cost_of_equity, key_driver, confidence (low/medium/high).

# Rules
- Plain-English summary first. Define every term. Add a glossary. Put technical detail in
  appendices and footnotes so the main text stays readable.
- Comment on unusual historical items (extraordinary items) and what they mean for the result.
- The text should be technical enough to persuade an investor and clear enough for a
  non-specialist. Give a fair view of risks and potential returns.
- Include the disclaimer: academic analysis for educational purposes; not personal
  investment advice.
- Run methodology/qa_checklist.md before delivering. Report data gaps.
- Before writing the report, follow methodology/report_template.md: propose the outline in
  report_outline.md, wait for the user's approval, then build report.pdf, the Excel models
  (data_pack.xlsx, dcf_model.xlsx, relative_model.xlsx) and all figures as PNG.
