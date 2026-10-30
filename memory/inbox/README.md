# Inbox: give the agent more information

Drop anything you want the agent to learn here: files (PDF, Excel, Word, CSV, screenshots), links, or a short note. Then add one line per
item to `memory/inbox/INBOX.md` in this form (create the file if absent):

`<file or link> | applies to: <ticker, sector bucket, or "all"> | type: fact / preference / data / rule-override | note: <one sentence>`

Types: **fact** = something true about a company or sector; **preference** = how you want things done; **data** = numbers the agent may use as
an input (it will log them as user-provided with your file as the source); **rule-override** = you want a procedure changed. A rule-override is
never applied silently: the agent asks you to confirm it and records it under "Approved deviations" in `standing_approvals.md`.

## What the agent does with it (first thing in the next session)
1. Reads each line, opens the item, writes a short entry in the right memory file with `status: user-provided`, your file as source, and
   a `valid_until` if the information is date-bound.
2. Moves the item to `inbox/processed/` and appends `processed YYYY-MM-DD -> <memory file>` to the line.
3. Reports in one message what it stored and anything it could not interpret.

## Useful things to provide (see also the checklist in CHANGES.md)
Terminal exports (Bloomberg, LSEG, Capital IQ), LSEG normalised values, analyst reports you can legally share, your professor's calibration for
stage 4, corrections to anything the agent got wrong, preferred peers or peers to exclude, company-specific events, and examples of
recommendations you consider good.
