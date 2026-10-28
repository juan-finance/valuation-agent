# Valuation methodology

This repository uses two folders: skills/ for agent instructions and methodology/ for shared valuation rules. Replace the supplied files at the paths below and add the two new methodology documents. These are replacement documents for Devin; they do not install a ChatGPT skill or change a remote repository.

| Path | Role |
| --- | --- |
| skills/SKILL-DCF.md | Stage 2 execution instructions |
| methodology/dcf_procedure.md | Complete DCF calculations, policies and conflict resolutions |
| methodology/data_sources.md | Input sources, precise dataset fields and source-log schema |
| methodology/company_universe.md | Original 20-company list and verification requirements |
| methodology/sector_adjustments.md | Sector drivers and consistent equity-bridge conventions |
| methodology/qa_checklist.md | Stage checks and completion evidence |
| methodology/report_template.md | Report workflow and presentation requirements |
| methodology/CHANGE_SUMMARY.md | Comparison with the Word document and changes by file |

## Authority and conflict handling

The current explicit professor/project instructions govern assignment choices. Use the supplied lecture materials for conceptual support and Steps in Company Valuation.docx for the detailed workflow. The revised DCF procedure records the operational interpretation of those steps. Do not silently let the old skill override the Word document, or copy a demonstrable mathematical inconsistency simply because it appears in the Word document.

Where supplied sources conflict, log both passages and the selected treatment in dcf_decisions.md. Follow the explicit corrections and course-specific conventions in dcf_procedure.md. If later professor instructions require a different treatment, record it and quantify a separate variant where material. Unresolved issues that prevent a reliable base case make the valuation provisional; continue independent work.

The comparison in this revision covers the seven supplied Markdown files and the full Word document. It is not a slide-by-slide audit of the lectures or a review of other, unprovided stage skills. Locate course files by their actual names; do not assume the old skill's /lecture_notes filenames exist.

## Reading and execution order

Read SKILL-DCF.md → dcf_procedure.md → data_sources.md → sector_adjustments.md and company_universe.md → qa_checklist.md. Use report_template.md for the later report. Paths such as outputs/ and src/ are relative to the repository root, not filesystem-root directories.

Keep stage 1 sourcing, stage 2 DCF, stage 3 relative valuation and stage 4 recommendation distinct. Preserve existing stages 1, 3 and 4; reconcile their instructions with the revised methodology before using them. This package does not claim to supply those other skills.

Use one dated information set across the model. The Word document's January 2026 premium examples and 2025/2024 financial years are not permanently fixed current values. For an assigned historical valuation, use information available by the cutoff and archive the corresponding dataset version.
