# Company universe

The original 20 companies, tickers, buckets and indicative reporting currencies are retained below. This is a supplied selection list, not a refreshed security master. Verify identity, primary listing, reporting currency and corporate actions at the valuation cutoff before use.

| Company | Yahoo ticker | Bucket | Reporting currency (verify) |
| --- | --- | --- | --- |
| EDP Renováveis | EDPR.LS | B | EUR |
| Ørsted | ORSTED.CO | B | DKK |
| Iberdrola | IBE.MC | A | EUR |
| Enel | ENEL.MI | A | EUR |
| SSE | SSE.L | A | GBP |
| ENGIE | ENGI.PA | A | EUR |
| Verbund | VER.VI | A | EUR |
| Vestas | VWS.CO | C | EUR |
| Siemens Energy | ENR.DE | C | EUR |
| Schneider Electric | SU.PA | D | EUR |
| Prysmian | PRY.MI | D | EUR |
| NKT | NKT.CO | D | EUR |
| Alfa Laval | ALFA.ST | D | SEK |
| Air Liquide | AI.PA | D | EUR |
| ArcelorMittal | MT.AS | E | USD |
| TotalEnergies | TTE.PA | F | USD |
| Shell | SHEL.L | F | USD |
| BP | BP.L | F | USD |
| Equinor | EQNR.OL | F | USD |
| Neste | NESTE.HE | F | EUR |

## Classification and selection checks

- A: utilities; B: renewable developers/operators; C: equipment makers; D: industrials; E: steel; F: oil, gas and fuels. Apply [sector adjustments](sector_adjustments.md).
- Use these buckets for comparability and scenario design, not as automatic Damodaran industry classifications. Map each material business segment to its actual industry for beta, debt, CapEx and NWC benchmarks.
- Reporting currency, trading currency and geographic revenue exposure are separate. Select Rf from valuation currency; build CRP from revenue geography. Check GBP versus GBp for London prices and convert only with a sourced FX rate/date.
- Preserve the nonfinancial-company scope. Do not introduce bank/fund dividend models into this DCF workflow.
- Confirm share-class and parent/group perimeter, especially where listed subsidiaries, minority stakes or dual listings could cause double counting.

## Relative valuation universes

The table above is the TARGET list. It is neither a list of preapproved peers nor the regression estimation universe. Preserve all 20 rows; do not add peers to the target list or relabel them is_sample=TRUE.

| Use | Selection basis | Membership and exclusions |
| --- | --- | --- |
| Comparable candidates | 20–30 initial candidates per target; expand, filter, score and select 10 | MSCI Europe first, then permitted MSCI World developed-market relaxation; target/parent/subsidiary and >20% cross-holdings excluded |
| Regression full route | All nonfinancial constituents, not selected peers | MSCI Europe, then model-specific World fallback; exclude financials and REITs; retain parent/subsidiary pairs with dependence flagged |
| Regression web-minimum route | All eligible constituents in Utilities, Energy, Industrials and Materials | Same geography fallback, explicitly reduced-market coverage |
| Regression A | Industry → Industry Group with specified Europe/World ladder; World Sector last | At least 30 valid observations per fitted model; not a peer-set regression |
| Regression B/C | Same market rows per multiple model | B has sector and applicable region dummies; C none |

Verify GICS Sector/Industry Group/Industry as dated fields. Internal buckets A–F are not GICS and must not become regression dummy values. For web mappings, distinguish inferred classifications from verified codes; ambiguous classification must not silently determine sector selection or typicality. Record both MSCI market classification and listing location because developed-market eligibility and the at-least-five-Europe-listed peer rule are different tests.

Relative-method business mapping: EDPR/Ørsted = renewable power; Iberdrola/Enel/SSE/ENGIE/Verbund = utilities; Vestas/Siemens Energy = power equipment; Schneider/Prysmian/NKT = electrical equipment and cables; TotalEnergies/Shell/BP/Equinor = oil/gas; Neste = renewable fuels; Air Liquide = gases; Alfa Laval = machinery; ArcelorMittal = steel. Verify main business/segment mix rather than asserting every issuer is a pure play.

No index membership, industry code, market cap, ticker or current listing status was refreshed in this document revision. Examples in sector_adjustments.md are candidate search seeds, subject to all filters.
