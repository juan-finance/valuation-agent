# Report structure (readers: private investors, medium to low technical level)
Academic exercise. Judged on the consistency and correctness of the decisions, not on
whether the recommendation proves right.

## Process
1. After stage 3, write report_outline.md in outputs/<ticker>_<date>/. Use the structure
   below as the starting point and adapt it if THIS company needs it. List the chapters,
   figures and tables, and explain any change.
2. Use existing user approval if the scope and outline are already authorized. Otherwise ask the user to approve or change the outline; continue independent valuation and QA work.
3. Build the final report once the outline is approved or the user explicitly authorizes proceeding without that separate step.
4. Afterwards, offer to save the approved outline as templates/approved_report_outline.md.
   Ask before writing it.

## Structure (default)
1. One-page summary: fair value range, recommended price, current price, upside/downside,
   Buy/Hold/Sell, 3 key drivers, and a "What this means in plain English" paragraph.
2. Company in 5 minutes: what it does, where it earns money, segments.
3. Industry and competitors: main characteristics of the industry and market (cycle,
   regulation, growth, capital intensity, commodity or rate exposure).
4. Financial history, with charts and one-sentence takeaways. Comment on extraordinary
   items and unusual historical results (from the anomaly report) and what they mean for
   the forecast.
5. Forecast assumptions, each with a reason.
6. DCF valuation: model choice justified with verified literature or data, key value
   drivers (ranked, with a plain-English reason for each), and ONE summary picture of the
   DCF assumptions and result.
7. Relative valuation: choice of multiples justified, peer set, regression results,
   distribution of valuations, football-field chart.
8. Scenarios and sensitivities for both DCF and relative valuation.
9. Reconciliation of DCF and relative valuation:
   - table of DCF assumptions vs assumptions implied by relative valuation, and the factors
     that make the two differ;
   - how market expectations and current market conditions affect the DCF inputs and the
     peers' multiples.
10. Final value estimate and recommendation:
    - Fair value: a range (low / base / high) and ONE recommended price.
    - Mispricing: current price vs fair value, in % and in currency.
    - Limitations: data gaps, model risk, the assumptions that matter most.
    - Visual scale of minimum and maximum valuations (DCF and relative) and the
      recommended range.
    - Comparison with analyst recommendations (trusted sources only).
    - Recommendation thermometer (Buy / Hold / Sell) with a short text tied to the annual
      report narrative and one parameter the market may be mispricing. It must be a
      marketable recommendation, as an analyst at a listed brokerage would publish it.
11. Risks, and what would change the view.
12. Glossary (EV, WACC, EBITDA, terminal value, etc.).
13. Appendices and footnotes: technical detail, sources with dates, adjustments,
    anomaly report summary, data gaps, disclaimer ("academic analysis for educational
    purposes; not personal investment advice").

## Style
- Short sentences. Define every term the first time. Avoid jargon.
- The main text must be easy for a non-specialist to read, yet convincing to an investor
  and giving a fair view of risks and potential returns.
- Put technical detail in appendices and footnotes so the main text stays readable.
- Every chart has a title that states its conclusion.
- Cite only sources you have opened. Mark anything unverified. Never invent citations.


## Required DCF evidence and appendices

Apply [DCF procedure](dcf_procedure.md) and [QA checklist](qa_checklist.md). Keep the main narrative accessible; put the following schedules in the appendix and summarize their effects in the DCF section:

1. Five-year market/book leverage, debt valuation/proxy, stability decision and target path.
2. Reported-to-adjusted EBIT/group NI, trailing bridge, extraordinary items, and group-to-parent reconciliation.
3. Effective/marginal tax distinction; current/prior and industry NCE and NWC ratios, recurrence choices, D&A alignment and no-restatement lease/R&D convention.
4. Raw versus floored ΔNWC and per-share impact; recurring acquisitions and forecast growth linkage.
5. Beginning-book-capital returns, reinvestment-growth identity, chosen duration, transition and terminal n+1 consistency.
6. Geographic revenue/CRP and segment/beta tables; Rf components, base and alternative Ke, actual/synthetic debt ratings, bond checks and any incremental sovereign adjustment.
7. Market-value WACC including preferred financing where relevant, hybrid terms/treatment, and the operating-value-to-common-equity bridge.
8. Current share count/dilution, matching market quote, valuation range, sensitivity-based driver ranking and terminal-value dependence.
9. A conflict/conventions table: course-specific choices, technical corrections, remaining uncertainties and quantified material effects. Distinguish them from facts explicitly stated by the professor.

Label the recommendation as the outcome of the academic model; the existing analyst-style presentation requirement does not justify overstating certainty. Preserve verified sources, dates, glossary, disclaimer and stage 3–4 requirements. Do not claim completion while material QA failures remain unresolved.
