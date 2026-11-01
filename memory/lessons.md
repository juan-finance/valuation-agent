# Lessons and proposed rule changes

## Lessons (newest first)
### Relative-route implementation gotchas (added2026-11-01, BP.L)
- lesson: RunState.append_run_log only covers its fixed STAGES; a deviation custom input stage needs its own append. Retrospective elapsed estimates must be explicitly labelled, not presented as measured. pandas statistics columns can deserialize as integer1; stringify keys before looking up '1', or cap/beta silently become missing. Check reference availability before lengthy candidate sourcing.
- source: src/valuation_agent/runstate.py; outputs/BP.L_2026-10-30/relative/normalize.py and peer_selection.json
- confidence: high; status: verified implementation; valid_until: current source version; used for: efficient relative-only orchestration.
### Market data is date-keyed and company-independent  (added 2026-10-29, repo review)
- lesson: The MSCI market dataset, its A/B/C regressions and the Damodaran files are the same for every company valued on the same
  date. Rebuilding them per company is the main cause of the 40+ minute stage 3 in the pilot.
- source: user pilot report (stage 1 = 9 min, stage 2 = 17 min, stage 3 > 40 min, stage 4 not run for lack of quota)
- confidence: high (design reasoning from the procedures); the exact split of the 40 minutes is not yet measured.   status: unverified
- valid_until: none          used for: valuation-0-market-refresh and the stage 3 architecture
### Reading everything at every stage costs context  (added 2026-10-29, repo review)
- lesson: Stage 1 asked for the lecture PPTX files (about 33 MB) and stages 2 and 3 each re-read roughly 80-110 KB of procedures and shared files; a four-stage run in one
  session also carries the whole transcript forward. Fixed by text digests in `knowledge/`, a per-stage read map, and one stage per session.
- confidence: medium (not measured per file)   status: unverified   valid_until: none   used for: AGENTS.md sections 2-3
### No reusable code meant rewriting the same maths every run  (added 2026-10-29, repo review)
- lesson: The repo said no code library would be supplied, so each run rebuilt and re-tested DCF, OLS and scoring functions. `src/` now
  holds tested versions (133 tests).   confidence: high   status: verified (tests)   valid_until: none   used for: stages 2-3

## Questions to answer after each run (max ten lines in total)
What took longest? What did I do twice? Which rule was ambiguous? What would I tell the next run?

## Proposed rule changes (the USER decides; the agent never edits methodology/)
- (none yet)


### MT stage3 checkpoint (added 2026-10-31, run MT.AS_2026-10-30)
- fact / lesson: Longest: membership/ownership checks, not arithmetic. Repeated: SSAB class and GBP conversion fixed in cached parser; no refetch needed. Ambiguous: industry median unavailable, so never relabel regional aggregate as median. Next run: use dated standard-index proxy before scoring; provisional evidence is not a completed audit.
- confidence: medium; status: unverified
- valid_until: vintage 2026-10-30
- used for: relative valuation and final QA


### MT report handoff (added 2026-10-31, run MT.AS_2026-10-30)
- fact / lesson: Longest work: standard-index and hard-gate peer evidence. Repeated work: metadata field dates/currencies corrected at finalQA, preserving source policy. Ambiguity: PBV/ROE can proxy PE and amplifies reported one-off NI; isolated bargain-gain stress is not full peer normalization. Next run: collect normalized peer evidence and consensus-coverage audit before scoring; stop provisional rather than pad unverified peers. Evidence: MT.AS report chapters7–10 and finalQA.
- confidence: low; status: unverified
- valid_until: vintage 2026-10-30
- used for: company evidence review
