# Focused readable-display corrections

Reviewed by **icekylinx and GPT-6 Astra Pro**, 3 November 2026 UTC.

This review corrects five readable displays and clarifies one earlier
attributed interpretation. The underlying source transcriptions, raw and
edited machine strings, conditional frames, key assignments, repair prices
and prior attributions remain unchanged. The review follows the
[reading conventions](reading-conventions.md); it does not certify every
German translation in the corpus.

## Findings and treatment

| Case | Evidence retained in the machine layer | Readable-display treatment |
|---|---|---|
| [p205 A](../cases/finance/p205_A.md) | A3 has `GEMUEGT`; A4 ends with `KX?XBDXNRX1???STRICH11XB?X`. | Show **gemügt [genügt]**, identifying the bracketed spelling as prose-only normalization. Display the five unresolved footer positions as `?`, `1???` and `B?`, rather than variable-length ellipses. The three previously priced word repairs are unchanged. |
| [p187b](../cases/p187b.md) | The raw and conditional edited outputs end with `NACHCHEF?X??????`. | Show that exact closing field, retaining seven unknown positions and its known `X`. Norbert's word normalization and the separately priced adjacent-coordinate swap retain their earlier attribution and conditional status. |
| [ZITAG cancellation](../cases/finance/zitag_purchase_orders.md) | p103 B2 ends with `SOFORTIGERUECKKEHR`. | Space this as **sofortige Rückkehr**. The former **sofortiger Rückkehr** added an extra display-only `R`. No preposition or grammatical repair is supplied. |
| [Dobrudscha report](../cases/military/dobrudscha_report.md) | Both raw and edited outputs contain `STELLUNGSNAHME`. | Retain **Stellungsnahme**, with **[Stellungnahme]** separately identified as a prose-only spelling normalization. The additional `S` is not deleted from either machine string. |
| [p201 reporting order](../cases/military/p201_p206_orders.md) | B1 has `WANNERSTENTEILE`; B2 preserves the unresolved closing reference. | Restore **wann ersten Teile** in the readable display and label it as a body excerpt. The awkward `ERSTEN` and `DESSIND` remain literal; no extra source repair is introduced. |
| [p89 A2](../cases/supplementary/p89_A2.md) | Both retained machine strings have `EZ`. | Keep the earlier credited **Ex.** quote unchanged, while explicitly identifying it as an interpretation of the abbreviation. It is not presented as exact spacing, a new `Z→X` repair or an independently established office title. |

The p205 and Dobrudscha alternatives are visible beside their literal
spellings. Their brackets do not indicate extra decoded positions or
coordinate fills. The accompanying notes define their category at the
point of use.

Three initially suspicious displays required no change. The
[military-allowance case](../cases/finance/military_allowances.md) already
prices its local `0→X` repair. The [p210 transport case](../cases/naval/p210_A.md)
and [p211 key schedule](../cases/radio/p211_key_schedule.md) already account
for the spelling changes in their readable passages with explicit
coordinate substitutions and, in p211, an invalid-glyph fill. Those checks
illustrate why the readable passage must be assessed against its stated
edited layer, not only against raw output.

## Preservation and bounded character mappings

The [frozen before-record](../data/reviews/reading_conventions_semantic_before.json)
stores all six pre-edit Markdown files. The
[audit](../data/reviews/reading_conventions_semantic_audit.json) records
the old and new displays, required local qualifications and exact source
fragments. Its verifier checks:

- **26 complete fenced blocks** and **33 prior headings** remain byte-for-byte
  identical and in order.
- All **143 prior inline-code occurrences** remain in their original order.
- **13 protected evidence files**, including the keys, challenge messages
  and relevant source/certificate records, retain their prior SHA-256
  digests.
- **Six selected display fragments** match their frozen source fragments
  after only the explicitly declared display transformations. This includes
  retaining all five p205 closing unknowns and all seven p187b closing
  unknowns.
- The separate **p89 attributed interpretation** remains different from
  literal `EZ`, with that difference disclosed locally. Its historical
  correctness is not inferred from the display check.

The permitted mapping transformations are German umlaut transcription,
capitalization, removal of display punctuation/spacing, removal of the
explicitly bracketed spelling alternative, and—only for the p205 footer—
displaying known `X` separators as spaces. They do not license deleting an
unknown position or relabelling a numeral.

## Reproduce

From the repository root:

```sh
python data/reviews/verify_semantic_readings.py
```

The standard-library verifier derives the repository path from its own
location and can also run by absolute path from another working directory.
Use `--output /tmp/reading-semantic-check.json` for a JSON report. The
[full presentation checker](../data/reviews/check_reading_presentation.py)
separately checks the current tree against its reviewed display manifest.
Neither check decrypts ciphertext or replaces the source packages'
independent arithmetic and image verification.
