---
name: valuation-3-relative
description: Stage 3 of a company valuation. Selects the most relevant sector multiples, runs Damodaran-style regressions, values the firm on all other multiples, weights the results and plots the distribution of valuations. Use after the DCF stage.
---

# Goal
Relative valuation of ONE company, following /lecture_notes (Lecture 5 Relative Valuation).
Where this file and the notes differ, the notes win. Use stage 1 data and the DCF from stage 2.

# Procedure
1. Choose the 2-3 MOST RELEVANT multiples for this business. Use common sense, analyst
   recommendations and news (e.g. EV/DACF for oil, EV/EBITDA or EV/RAB for networks,
   EV per MW for renewables). Write the reasoning down. These are the "key multiples".
2. Build the peer set (same sector; the bucket in methodology/valuation_standards.md helps).
   Use at least 4 peers where possible; say clearly if fewer exist.
3. For the key multiples, run the regression analysis from Lecture 5. Use the Damodaran
   regression with the highest R-squared from
   https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html. Report R-squared,
   the coefficients, the company's inputs and the implied multiple and value per share.
   SAFEGUARD: do not use a regression with a very low R-squared or with company inputs
   far outside the sample range. State the thresholds you used.
4. For ALL other multiples you can find (P/E, P/B, P/S, EV/EBITDA, EV/EBIT, EV/Sales, P/CF,
   dividend yield, etc.), compute the sector median and quartiles and the implied value per
   share. Compare the company's market cap with competitors.
5. Weighting:
   - key multiples get higher weights than the others;
   - if the company's market cap is closer to the top of the peer group, weight the higher
     valuations more (and the reverse);
   - give higher weight to valuations closer to the DCF from stage 2, lower to those far away.
   SAFEGUARDS: exclude negative or meaningless multiples; trim outliers; no single weight
   above 30%; weights sum to 100% and are shown in a table; always also show the unweighted
   median. Warn that weighting toward the DCF creates circularity and report how much it
   moves the result.
6. Plot the distribution of all valuations (one point per multiple, marking the weighted
   average, the DCF value and the current price).

# Outputs
relative_model.xlsx, weights_table, distribution chart, relative_decisions.md.
