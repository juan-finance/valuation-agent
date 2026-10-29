---
name: company-valuation
description: Full valuation of ONE listed company (data sourcing, DCF, relative valuation, final Buy/Hold/Sell recommendation) for non-expert investors. Use whenever the user asks to value, analyze or price a company.
---

# Overview
Run four stages in order. For each stage, first READ the stage file, then follow it exactly:
1. .agents/skills/valuation-1-data-sourcing/SKILL.md
2. .agents/skills/valuation-2-dcf/SKILL-DCF.md
3. .agents/skills/valuation-3-relative/SKILL-RELATIVE.md
4. .agents/skills/valuation-4-recommendation/SKILL.md

# Rules of precedence (single hierarchy for the whole repository)
1. The professor's lecture notes in /lecture_notes override everything else.
2. Steps in Company Valuation.docx (and the two Agent Instructions PDFs in /method_guides)
   come next. They were written from the lectures, so if one contradicts a lecture, the
   lecture wins. Their content is already encoded in methodology/dcf_procedure.md,
   comparables_procedure.md and regression_procedure.md; open the originals only to
   settle a doubt.
3. The methodology procedures and the four stage files (they must agree; a stage file
   orchestrates and the procedure holds the detail). If they disagree, apply the more
   specific rule, record the conflict in the decisions file, and tell the user.
4. /methodology/sector_adjustments.md is overridden by the four stage files, but still
   supplies sector adjustments (buckets A-F). The QA checklist applies to the final output.
5. Worked examples in /examples show method only and never override any of the above.
Run parameters given by the user (company, valuation date, data route, scope, attached
files) are inputs, not methodology; they do not change rules 1-5 unless the user says so
explicitly and the choice is recorded.

# Required from user
Company name (must be in methodology/company_universe.md), valuation date (default today),
any attached files. Ask if anything is missing.

# Workflow
- Scope: this orchestrator values ONE company. Create /outputs/<ticker>_<date>/ for all
  deliverables, including stage 3 (single-target mode, folder relative/ inside it; see
  SKILL-RELATIVE.md). The 20-target batch run (outputs/relative_<date>/) is only for a
  direct request to run stage 3 for the whole universe, outside this orchestrator.
- Stage 3 single-target mode still estimates the regression on the full dated market
  dataset (all 20 target rows retained); it only VALUES the requested company.
- After stage 1, post a short message with the anomaly report and the confirmed ticker and
  exchange. After stage 2, post the model choice (FCFE or FCFF), the growth model and the
  discount rates. Continue unless something is critical or uncertain, in which case ask.
- Report outline: after stage 3, propose report_outline.md. Reuse an existing approval of
  scope/outline; otherwise ask the user and keep doing independent work (QA, figures,
  workbooks) while waiting. Build the final report once approved, or once the user
  explicitly authorizes proceeding (see methodology/report_template.md).
- Finish with the report, the Excel models (data_pack.xlsx, dcf_model.xlsx), the seven
  stage 3 core files (comparables.csv, multiples_summary.csv, comparables_report.md,
  DATA_BASE_MSCI.xlsx, regression_valuation.xlsx, valuation_multiples.csv,
  valuation_summary.md), the figures and the source log. relative_model.xlsx no longer
  exists.
- Consistency: apply the same method, thresholds and report structure to every company so
  that the recommendations can be compared in the portfolio stage. Any deviation must be
  stated and justified in the decisions files.
- The recommendation is judged on the consistency and correctness of its reasoning, not on
  whether it turns out right. Document every judgement call and its reason.

# Forbidden
- Never invent data or fill gaps silently. Mark "not available".
- Never use paid-database data unless the user attached it.
- Never change /methodology or /lecture_notes files without asking.
- Never present the result as personal investment advice. It is an academic analyst recommendation and must carry the disclaimer.
