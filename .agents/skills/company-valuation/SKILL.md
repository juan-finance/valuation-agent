---
name: company-valuation
description: Full valuation of ONE listed company (data sourcing, DCF, relative valuation, final Buy/Hold/Sell recommendation) for non-expert investors. Use whenever the user asks to value, analyze or price a company.
---

# Overview
Run four stages in order. For each stage, first READ the stage file, then follow it exactly:
1. .agents/skills/valuation-1-data-sourcing/SKILL.md
2. .agents/skills/valuation-2-dcf/SKILL.md
3. .agents/skills/valuation-3-relative/SKILL.md
4. .agents/skills/valuation-4-recommendation/SKILL.md

# Rules of precedence
1. The professor's lecture notes in /lecture_notes override everything else.
2. The four stage files override /methodology/valuation_standards.md.
3. /methodology/valuation_standards.md still supplies sector adjustments
   (buckets A-F) and the QA checklist applies to the final output.

# Required from user
Company name (must be in methodology/company_universe.md), valuation date (default today),
any attached files. Ask if anything is missing.

# Workflow
- Create /outputs/<ticker>_<date>/ for all deliverables.
- After stage 1, post a short message with the anomaly report and the confirmed ticker and
  exchange. After stage 2, post the model choice (FCFE or FCFF), the growth model and the
  discount rates. Continue unless something is critical or uncertain, in which case ask.
- Finish with the report, the Excel models, the figures and the source log.

# Forbidden
- Never invent data or fill gaps silently. Mark "not available".
- Never use paid-database data unless the user attached it.
- Never change /methodology or /lecture_notes files without asking.
