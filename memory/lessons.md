# Lessons and proposed rule changes

## Lessons (newest first)
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
