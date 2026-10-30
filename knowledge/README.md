# Knowledge digests (text only, generated once)

`lecture_digest/`: text of the five lecture decks. `case_digest/`: text of the six professor solutions (method only, never copy numbers).
Equations, charts and screenshots in the originals are NOT captured, so a digest finds the rule; open the original PPTX/DOCX only to settle
a doubt about a formula or figure.

Lectures rank highest in the repository hierarchy. When you rely on a lecture rule, cite it as `lecture_digest/<file>, slide N`.

## How to use (grep, do not read whole files)
| Need | Command |
|---|---|
| a definition or rule of thumb | `grep -n -i "<term>" knowledge/lecture_digest/*.md` |
| growth stage heuristics, terminal value | `L4_closure_terminal_value_growth.md` |
| beta, risk-free rate, ERP, country risk, cost of debt | `L2_discount_rates.md` |
| earnings, reinvestment, cash flow definitions | `L3_cash_flows.md` |
| multiples, regression, fundamentals behind PE/PBV/PS | `L5_relative_valuation.md` |
| how the professor handled a judgement call | `grep -n -i "<topic>" knowledge/case_digest/*.md` (FCFF: case 1, FCFE 2-stage: case 3, FCFE 3-stage: case 4, relative: cases 5-6; case 2 is a dividend model, financial firms only) |

Regenerating (if the source files change): `extract-text <file> > knowledge/...` (any tool that extracts slide/docx text works) and keep the header comment.
