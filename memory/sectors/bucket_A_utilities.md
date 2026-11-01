# Bucket A: utilities

Sector-level facts found by research (benchmarks, regulation, accounting conventions, typical peers, recurring data problems).
Use the entry format in memory/README.md and always give source, date and valid_until. Companies in this bucket: see methodology/company_universe.md.

## Entries
(none yet)

## ENEL.MI run 2026-11-01 (relative_only, provisional)
- Peer set (10, all Europe, 8 T1 + 2 T2): ENGI EOAN EDP NG SRG SSE TRN ORSTED VER FORTUM. Size band EUR9.25-924.6bn at cap EUR92.5bn cut out CNA/A2A/REE/IG and all small IPPs; IBE/RWE scored above the selected set.
- Grid operators (TRN, SRG) work well as Tier-2 for integrated utilities; Endesa-type subsidiaries must be hard-excluded up front.
- Payout >100% is common in this bucket (ENGI/FORTUM/ENEL): fundamental growth collapses to 0 and PEG is NM — expect it.
- Primary EV/EBITDA peer median 12.56x FY2025 basis; published EUROPE EV/EBITDA equation predicts ~19x for these inputs — market-wide equation sits well above the sector, use only as flagged cross-reference.

## 2026-11-01 IBE.MC run notes (relative_only, provisional)
- IBE pool: ENEL scored 11th and just missed the 10-peer set — Iberdrola's own closest comparator isn't always selected when it's the target's peer (size/score ordering).
- Scrip dividends exist in this bucket (IBE "Retribución Flexible"): vendor CF-dividends can understate declared payout badly (0.21 vs 0.75) — always use declared basis for payout/growth inputs.
- Peer EV/EBITDA median again ~12.56x FY2025; published EUROPE equation predicts ~19.7x for utility inputs — same market-wide vs sector gap as ENEL/ENGIE runs.
- Report-currency gotcha: reused EDPRpool_* extracts lose the report currency (units=[]) — a UNITS map from the fetch manifest is required or GBP/DKK/NOK reporters get misread as EUR (ENEL run affected; fixed in IBE pipeline).
[source: outputs/IBE.MC_2026-10-30; confidence: medium]

## 2026-11-01 ENGIE run notes
- Vendor CFO for ENGIE FY2025 negative (-1,476 vs issuer CFFO 13.6bn; Belgian nuclear cash-out): EV/CF can be NM for a target even when peers are fine — mark NM, don't substitute.
- Peer EV/EBITDA medians for integrated utilities run ~12.2-12.6x vs Engie/Enel actual ~8.1-8.4x; published EUROPE EV/EBITDA equation predicts ~19-20x for utility inputs — keep flagging the market-wide vs sector gap.
[source: outputs/ENGI.PA_2026-10-30; confidence: medium]
