# Operating rules for the valuation agent (read this first, every session)

This file is about HOW to run efficiently and how to remember. WHAT to compute is defined by
`.agents/skills/company-valuation/SKILL.md` (hierarchy, conflict handling) and `methodology/`. Nothing here changes a
methodology rule; if this file and a methodology file ever disagree, methodology wins and you record the conflict.

## 1. Start of every session (aim: under 5 minutes, no valuation work yet)
1. Read `memory/standing_approvals.md` (user decisions already made: data route, batch valuation date, mode, outline approval).
   Do not ask the user again for anything answered there.
2. Read `memory/index.md`, then only the memory files it points to for THIS company/sector.
3. Check `memory/inbox/` for new user material (see `memory/inbox/README.md`); ingest it before anything else.
4. If `outputs/<ticker>_<date>/run_state.json` exists, load it with `valuation_agent.runstate.RunState` and RESUME at
   `resume_point()`. Never restart a finished stage.
5. Check `cache/README.md` for what already exists for the valuation date (macro snapshot, market dataset) and run `python -m valuation_agent.datasets list` to see which
   reference datasets (Damodaran betas, capex, country risk, regressions, other regions) are registered in `data/`.

## 2. Efficiency rules (these exist because a single-company pilot used a full day of quota)
- **Never collect the same data twice.** Market-level data (Damodaran files, Rf/ERP/FX snapshot, the MSCI market dataset and its
  regressions) is identical for every company on the same valuation date. It is built ONCE by
  `.agents/skills/valuation-0-market-refresh/SKILL.md`, stored in `cache/`, and reused. A new valuation date means a new cache,
  so values for a batch of companies must share one date (`memory/standing_approvals.md`).
- **One stage per session.** End the session after the stage hand-off message and `run_state.json` update. Long single sessions
  carry the whole earlier transcript into every later step. The next stage starts fresh from the files, not from chat history.
- **Reference data comes from the data library, chosen by the resolver.** For any Damodaran dataset call `datasets.resolve(family, country=..., valuation_date=...)`; never
  guess a file name, never fetch a file that is registered, never use a dataset dated after the valuation date, and never silently accept a `fallback` region (record why it
  is representative). If the resolver says a dataset is missing, ask the user to supply it (one message, listing everything missing) and register it with `datasets add`.
  Read `data/README.md` once per session when you use the library.
- **Use the code library** (`src/valuation_agent/`, see `src/README.md`) for arithmetic, scoring, regressions, anomaly checks, the
  source log and caching. Do not re-implement them; do not re-run the test suite unless you changed `src/`. If a function disagrees
  with a procedure, the procedure wins: fix the code, add a failing test first, then fix.
- **Scripts, not browsing, for bulk data.** Fetch with `CachedFetcher` (parallel across hosts, at most ~1 request/second per host,
  results cached on disk). Browse by hand only for judgement-heavy reading (annual report notes, rating actions, ownership).
  Check a site's terms of use before bulk collection and tell the user if they look restrictive.
- **Write results to disk in batches** (every ~25 companies or every sub-step) so a quota cut-off loses minutes, not hours.
- **Read less, grep more.** Lecture and case content is in `knowledge/` as text; use `grep -n` there. Do not open the PPTX, the
  Word/PDF method guides or the example workbooks unless a doubt remains after grepping. Read the procedure sections named for your
  stage (section 3) rather than every methodology file. Do not re-read a file you already read in this session.
- **No duplicate QA.** Run the checklist block for your stage once, at the end of the stage, and record it in `qa_results.md`.
  Fix failures; do not re-run passing items after unrelated edits.
- **Do not narrate.** Stage messages are short: result, assumptions that matter, conflicts found, elapsed minutes. Put detail in the
  decisions files, not in chat.
- **Time check.** At every stage end record elapsed minutes (`RunState.finish`) and run `RunState.append_run_log('memory/run_log.csv')`.
  If a stage is running at more than twice the longest time of that stage in `memory/run_log.csv`, stop at the next checkpoint,
  say why (what is slow), and ask whether to continue. The user has a limited quota.
- **Modes** (`memory/standing_approvals.md`): `standard` (default) skips only what the procedures themselves call optional (second DCF
  method cross-check, lambda approach, supplementary multiples, optional one-driver peer fit, extra charts). `full` includes them.
  Neither mode relaxes a required rule, threshold or deliverable. Quality shortcuts that change a method are NOT allowed unless the
  user listed them under "Approved deviations" in `memory/standing_approvals.md`.

## 3. Read map per stage (read these, not everything)
| Stage | Read |
|---|---|
| 0 market refresh | `data/README.md`; `regression_procedure.md` sections 1-4 and 9 (route `own_estimation` only; route `published_damodaran`: `regression_published_route.md`); `comparables_procedure.md` sections 1-2 and 4; `data_sources.md` (stage 3 routes) |
| 1 data | `data_sources.md` (input map, source_log fields); `qa_checklist.md` block A |
| 2 DCF | `dcf_procedure.md` (full, as required); `sector_adjustments.md` (general, bridge checks, your bucket); `qa_checklist.md` block B |
| 3 relative (per company) | `SKILL-RELATIVE.md`; `comparables_procedure.md` (full); regression: route `own_estimation` -> `regression_procedure.md` sections 6-8 and 10, route `published_damodaran` -> `regression_published_route.md` (full) and `data/damodaran/NOTES.md`; `sector_adjustments.md` (relative parts); `qa_checklist.md` block C |
| 4 recommendation | `report_template.md`; `sector_adjustments.md` (scenario drivers); `qa_checklist.md` block D |

## 4. Memory: what to write and when (full protocol in `memory/README.md`)
- At the END of every stage write what a future run would need: company facts and judgement calls to
  `memory/companies/<ticker>.md`; sector facts to `memory/sectors/`; what worked or failed to `memory/source_playbook.md`;
  process lessons to `memory/lessons.md`. Keep each entry short, dated, sourced and with a confidence level.
- Memory holds facts and lessons, never rules. It cannot override the methodology hierarchy. Facts have a `valid_until`
  or a vintage; re-verify stale ones before use instead of trusting them.
- A lesson that would change a METHOD goes under "Proposed rule changes" in `memory/lessons.md` for the user to decide. You never
  edit `methodology/` or `lecture_notes/` yourself.
- Never store credentials, API keys or personal data in the repository.
- Learn beyond what the user supplies: when a run needs a fact that the repo lacks (a sector benchmark, a company event, a source's
  quirks), research it, use it, and store it with its source and date so the next run does not repeat the research.

## 5. Always (unchanged)
Never invent data; mark "not available". Cite and date every number. Keep the academic-analysis disclaimer on the final output.
Everything a run creates goes under `outputs/<ticker>_<date>/`; shared reusable assets go under `cache/`; learning goes under
`memory/`. Commit `memory/`, `cache/` (parsed data, not raw HTML) and `outputs/` at the end of each stage so the next session sees them.
