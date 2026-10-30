# Published-regression route (user-approved alternative to own estimation)

**Authority.** Selected by `regression_route: published_damodaran` in `memory/standing_approvals.md` (set by the user, 2026-10-30). While that
setting holds, this file replaces `regression_procedure.md` sections 2-9 for the regression method (market dataset, estimation, A/B/C, diagnostics).
`regression_procedure.md` remains the rule set for `regression_route: own_estimation`. Its prohibition on replacing estimation with published
coefficients applies to that route only; here the published equations ARE the model, by the user's decision, and the limits below are stated, not hidden.
Lectures still outrank this file. The equations come from the registered dataset `regressions_multi_<vintage>` (see `data/README.md`).

## 1. Choosing the equation
1. Call `datasets.equation_for(<listing country>, <dependent>, valuation_date)`. It returns the equation, the dataset, the region used (exact or
   fallback) and warnings. Record dataset id, vintage, as-of date, region used and any warning in `source_log.csv` and the decisions file.
2. The default region is the listing country's. For a company with material revenue elsewhere compare with `resolve_for_company` and record the choice.
   Never average equations from different regions into one number (same rule as the benchmark fields of `regression_procedure.md` section 9).
3. The dataset's as-of date must not be after the valuation date (the resolver enforces this). If the equation is more than 6 months older than the
   valuation date, say so under Limitations (market multiples move; it is a flag, not a stop).
4. If no dataset exists for the needed region, the resolver says so: stop and ask the user to supply the file. Do not use another family or invent coefficients.

## 2. Which multiples exist
| Repo multiple | Published equation | Note |
|---|---|---|
| PE | PE | inputs beta, g_eps, payout |
| PBV | PBV | inputs g_eps, beta, roe, payout (region-dependent term list) |
| EVEBITDA | EV/EBITDA | inputs g_rev, dfr, tax_rate, roic (EM and Japan lists differ) |
| PS | none | not published. EV/Sales is a different multiple (enterprise value): do not substitute it silently |
| supplementary | PEG, EV/IC, EV/Sales | shown only in `full` mode, labelled supplementary, never the primary |

## 3. Inputs: definitions are the file's, not ours
| Variable | Definition in the file | Rule here |
|---|---|---|
| g_eps | expected EPS growth, next 5 years, analyst estimates | Sourced consensus. Our regression procedure uses fundamental growth (ROE x retention); that is a DIFFERENT definition. Use the fundamental proxy only if `published_route_allow_fundamental_growth: yes` in standing approvals, label it `substituted_input`, and show it separately. Otherwise the equation is "unavailable". |
| g_rev | expected revenue growth, next 5 years (file: use g_eps if unavailable) | Sourced consensus; the g_eps fallback is the file's own rule, label it. |
| beta | regression beta | Observed regression beta, sourced. Missing, negative or above 2.5: replace with the bottom-up relevered beta (`regression.replace_beta`) and flag. |
| payout | dividends / earnings | Observed, same fiscal basis. Negative payout: equation not valued for that target (outside the definition). |
| roe | net income / book equity | Last fiscal year, parent common basis, state the basis. |
| roic | EBIT(1 - tax rate) / invested capital (equity + debt - cash) | State the EBIT and capital definitions used. |
| dfr | total debt / (total debt + market equity) | Gross debt incl. leases, market equity at the price date. |
| oper_margin, tax_rate | pre-tax operating income / sales; effective tax rate | As defined; effective, not marginal. |
Inputs are entered as DECIMALS (25% = 0.25). Never clip or repair an input to make an equation run; unavailable stays unavailable.

## 4. Units: an unresolved issue that must be settled per run
The file says to enter decimals. The coefficients on DFR and Tax rate (for example -0.11 and -0.12 with t-statistics of 5 to 90) have the scale of
percentage points (0 to 100), not decimals. This is an inference from the coefficient scale, not something the files confirm.
`published_regressions.predict` therefore has no default unit policy.
- Run `predict_both_policies` for every equation that uses DFR or tax_rate. Where the two predictions differ by more than 10% (relative),
  the unit question is material: verify against Damodaran's variable-definition page or his dataset, and run the plausibility check below.
- Plausibility check: compare each policy's predicted multiple with the sector median multiple of the peer set (stage 3 comparables). Record both
  numbers, the policy chosen and why in the decisions file. If it cannot be verified, report both side by side, set `units_unverified`, and use neither as a headline.
- `memory/standing_approvals.md` field `damodaran_dfr_tax_units` stores the verified answer once settled; the agent reuses it.

## 5. From multiple to value
Same bridges and invariants as `regression_procedure.md` section 7: PE x EPS on the matching earnings basis; PBV x book value per share on the matching
equity basis; EV/EBITDA x EBITDA then the exact inverse of the EV construction (debt incl. leases, NCI, cash, associates; `comparables.implied_equity_from_ev`);
per-share on the current share count. Disclose that Damodaran's EV and invested-capital definitions are not specified in the file (treatment of leases, NCI, associates may differ from ours).

## 6. What the published route cannot produce (report as not available, never estimate)
n, residual standard error, p-values, adjusted R2, sector dummies, A/B/C scopes, typicality routing, D1-D10 diagnostics, robustness refits, and therefore the
residual-band classification. Report instead: predicted multiple, actual multiple, `deviation = actual/predicted - 1`, the equation's R2 as the only fit statistic,
and the t-statistics as published. Equation R2 is low for the Western Europe & UK set (PE 20%, PBV 42%, EV/EBITDA 26%, EV/Sales 14%): a market-wide equation
has no sector structure, so predictions for utilities, oil majors or steel makers can differ from sector reality for reasons the equation cannot see. State this in the headline.

## 7. Model choice and output contract
- Eligible models: PE, PBV, EVEBITDA with all inputs available, restricted by the bucket's primary-multiple guidance in `sector_adjustments.md`.
  Rank by published R2 as the project heuristic (weaker than adjusted R2 on our own sample: say so). Output the chosen model and the next two alternatives.
- Files: `valuation_multiples.csv` (same columns as `regression_procedure.md` section 10; fields the route cannot produce contain `n/a_published_route`;
  `primary_regression = published_damodaran_<REGION>_<vintage>`; `classification = Not classified (no SEy published)`; add `published_r2`, `units_policy`,
  `units_unverified`, `equation_dataset_id`, `substituted_input`; keep `damodaran_global` and `damodaran_western_europe_uk` filled), `regression_valuation.xlsx`
  (inputs with source_log ids, coefficients typed with dataset id and page, live-formula predictions and bridge), `valuation_summary.md`.
  `DATA_BASE_MSCI.xlsx` is not produced in this route (no market sample is built); say so.
- Independent check: recalculate the workbook, then compare every prediction with `published_regressions.predict` to 1e-9. Never copy Python numbers into the workbook.
- `valuation_summary.md` keeps the ten headings of section 10. Section 4 shows the equation(s) and t-statistics; section 5 states "not available under this route"
  plus the data-library check findings for the dataset; section 7 shows both unit policies; section 9 adds: equation vintage versus valuation date, market-wide scope,
  analyst-growth definition, unit uncertainty, undocumented EV definition, no residual dispersion, cheap versus prediction is not proof of mispricing.

## 8. Stops
Stop that target's regression (others continue) if: no dataset for the region, a needed input is unavailable and no approved substitution applies, the integrity
check of the dataset has an error, or units are unverified and the user did not approve reporting both. Source anomalies the integrity check flags
(for example the Global PEG equation) make that equation `not used until verified`; use another region's equation or report unavailable.
