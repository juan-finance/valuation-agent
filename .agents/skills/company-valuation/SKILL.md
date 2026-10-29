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
This is the one authoritative statement of the hierarchy; every other file points here.
1. The professor's lecture notes in lecture_notes/ override everything else.
2. The methodology procedures (methodology/dcf_procedure.md, comparables_procedure.md,
   regression_procedure.md) and the four stage files. The procedures consolidate Steps in
   Company Valuation.docx and the two Agent Instructions PDFs (method_guides/), which were
   written from the lectures, and they deliberately record corrections to errors and internal
   contradictions in those documents (conflict registers: dcf_procedure.md section 11 and
   regression_procedure.md section 11). Those recorded corrections stand and are NOT undone by
   the Word/PDF originals. Only a lecture can override them. Procedures and stage files must
   agree (a stage file orchestrates, the procedure holds the detail); if they disagree, apply
   the more specific rule, record the conflict in the decisions file and tell the user.
3. The Word/PDF originals in method_guides/. They are source material, not a higher authority
   than the procedures. Open them only to settle a doubt the procedures leave open; never use
   them to reverse a recorded correction. If one contradicts a lecture, the lecture wins.
4. methodology/sector_adjustments.md is overridden by the four stage files, but still
   supplies sector adjustments (buckets A-F). The QA checklist applies to the final output.
5. Worked examples in examples/ show method only and never override any of the above. If an
   example differs from a higher-ranked source, follow the higher-ranked source, note the
   difference in case_summary.md and tell the user. Do not stop to ask.
If a lecture contradicts a procedure, a recorded correction or a stage file, follow the lecture
and record the conflict (dcf_decisions.md for stage 2, the method report/Log for stage 3).
Run parameters given by the user (company, valuation date, data route, scope, attached
files) are inputs, not methodology; they do not change rules 1-5 unless the user says so
explicitly and the choice is recorded.

# Repository facts
- Paths in all files are repository-relative, without a leading slash (outputs/, lecture_notes/,
  methodology/, examples/, method_guides/).
- A run writes only to outputs/. There is no src/ code library, no templates/ folder and no
  group workbook, and none will be supplied. Do your own research for peers, cross-checks and
  data (sources in methodology/data_sources.md); build and test any code or checks yourself.
  Only files the user attaches in the conversation are extra inputs.

# Required from user
Company name (must be in methodology/company_universe.md), valuation date (default today),
any attached files. Ask if anything is missing.

# Workflow
- Scope: this orchestrator values ONE company. Create outputs/<ticker>_<date>/ for all
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
- Never change methodology/ or lecture_notes/ files without asking.
- Never present the result as personal investment advice. It is an academic analyst recommendation and must carry the disclaimer.
