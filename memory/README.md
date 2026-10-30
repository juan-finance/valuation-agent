# Memory: how the agent learns and remembers

Devin sessions start empty. Anything the agent should still know next week has to be in this repository (merged to the branch the
next session starts from). Memory is **facts, preferences and lessons**. It is never methodology: it cannot override
lecture notes, procedures or stage files (see the hierarchy in `.agents/skills/company-valuation/SKILL.md`).

## Layout
| Path | Who writes | What it holds |
|---|---|---|
| `standing_approvals.md` | the user | Decisions made once: data route, batch valuation date, mode, outline approval, approved deviations |
| `index.md` | the agent | One-screen map of everything below, with last-updated dates |
| `inbox/` | the user | New information to ingest (files, links, notes). See `inbox/README.md` |
| `companies/<ticker>.md` | the agent | Per-company facts, judgement calls and why, data quirks, open questions |
| `sectors/<bucket>.md` | the agent | Sector facts and benchmarks found by research, with source, date and expiry |
| `source_playbook.md` | the agent | Which source/URL/field worked, what failed, verified column meanings |
| `lessons.md` | the agent | Process lessons, mistakes made and fixed, proposed rule changes for the user |
| `run_log.csv` | the agent | Minutes per stage per run (cost tracking) |

## Entry format (every entry in companies/, sectors/, source_playbook.md, lessons.md)
```
### <short title>            (added YYYY-MM-DD, run <ticker>_<date> or "user")
- fact / lesson: <one or two sentences>
- source: <URL, file and page, or "user inbox: <file>">
- confidence: high | medium | low        status: verified | unverified | user-provided
- valid_until: <date or "vintage <name>" or "none">
- used for: <which decision or step it informs>
```

## Rules
1. **Read narrowly.** At session start read `index.md` and only the entries for the company/sector at hand.
2. **Write at stage end**, not continuously. Four questions, answered in at most ten lines in total:
   what took the longest, what was done twice, which rule was ambiguous, what would I tell the next run?
3. **Facts expire.** Prices, ratings, yields, consensus and index membership are date-bound. Store the vintage; before reuse, check
   `valid_until`. A stale fact is a lead to re-verify, never an input.
4. **Contradictions:** if new evidence contradicts a stored entry, do not delete it. Add the new entry, mark the old one
   `status: superseded by <title>`, and say so in the stage message if it changes a number.
5. **User-provided beats researched, but not beats methodology.** User input is stored with `status: user-provided`. If it asks for
   something the methodology forbids (for example paid-database data without the file, or a different formula), follow the hierarchy
   and ask the user to confirm an explicit override; record it under "Approved deviations" in `standing_approvals.md`.
6. **Proposed rule changes** go to the section of that name in `lessons.md`. The user decides; the agent never edits `methodology/`.
7. **No secrets, no personal data.** Credentials and API keys never enter the repository.
8. **Keep it small.** Merge duplicates, delete nothing that is still valid, and cap each company file at about one page by
   promoting repeated facts into the sector file.
