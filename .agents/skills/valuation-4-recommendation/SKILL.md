---
name: valuation-4-recommendation
description: Stage 4 of a company valuation. Combines the DCF and relative valuations with scenario and sensitivity analysis, reconciles the differences, discusses market expectations, compares with analyst recommendations and gives a fair value range, a recommended price and a Buy/Hold/Sell recommendation with visuals. Use after stages 2 and 3.
---

# Setup
Follow AGENTS.md section 1 and resume from run_state.json. Read only methodology/report_template.md, the scenario-driver part of
sector_adjustments.md and qa_checklist.md block D, plus the files stages 1-3 produced (they are the evidence; do not recollect data).
The report outline approval is read from memory/standing_approvals.md (`report_outline`); ask only if it says `not yet`.

# Goal
Final analyst recommendation for investors with medium to low technical knowledge. Academic
exercise: the work is judged on the consistency and correctness of the decisions, not on
whether the recommendation proves right. The professor will calibrate this stage later, so
keep the structure easy to change.

# Required content
1. DCF: scenario analysis (bear/base/bull) and sensitivity to the main inputs (tornado chart
   and a WACC vs growth table). Identify the key value drivers and say why they matter.
2. Relative valuation: scenario analysis too, built on the stage 3 outputs and kept separate for the two methods: comparables (p25/median/p75, primary multiple versus cross-check multiples, peer-set variants) and regression (the chosen model versus the next two eligible alternatives, and A/B/C). No stage 3 weights_table or 30% cap exists. If stage 4 combines methods into one value, use explicit method-suitability weights or a stated choice, justified in writing, never chosen because they move the result toward the DCF or the market price; show the sensitivity of the synthesis to those choices and keep the underlying estimates visible.
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
  report_outline.md. If the user already approved scope/outline (see memory/standing_approvals.md), reuse that approval;
  otherwise ask for approval and keep doing independent work (QA, figures, workbooks,
  recommendation_summary.csv) in the meantime. Build report.pdf once the outline is
  approved or the user explicitly authorizes proceeding without it. Deliver the Excel
  models (data_pack.xlsx, dcf_model.xlsx), the stage 3 core files already produced
  for the configured regression_route (comparables.csv, multiples_summary.csv, comparables_report.md,
  DATA_BASE_MSCI.xlsx (own_estimation only), regression_valuation.xlsx, valuation_multiples.csv, valuation_summary.md) and all
  figures as PNG. relative_model.xlsx no longer exists.

# End of stage
Update run_state.json, write memory/companies/<ticker>.md (final result pointer, what the market may be mispricing, open questions) and memory/lessons.md
(four questions in memory/README.md), append timings to memory/run_log.csv, commit, and post the short final message.
