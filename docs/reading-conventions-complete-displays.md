# Completing three older readable quotations

Prepared by **icekylinx and GPT-6 Astra Pro**, 3 November 2026 UTC.

Three readable quotations now show their complete declared decoded streams.
The earlier pages disclosed their excerpting or punctuation rendering; this
is a completeness and convention improvement, with no newly recovered
source position, changed cipher model or revised repair price.

| Source | Visible completion | Unchanged reading model |
|---|---|---|
| [p129 B1 allowances](../cases/finance/military_allowances.md#p129-b1) | Includes the opening `ZU X M X RM X 30 NR X 228` reference, with its abbreviations unexpanded. | Five observed-coordinate substitutions and two source-erasure fills. |
| [p132 A register inquiry](../cases/radio/p132_radio_service.md#a-an-officer-register-request-with-the-name-unresolved) | Includes `MILITAERMISZIONKOSJOII`, retaining the encoded Z spelling and unresolved addressee field. | Six observed-coordinate substitutions and one source-dash fill. |
| [p108 A naval inquiry](../cases/radio/naval_arrival_inquiry.md#p108-a) | Keeps the encoded words `DOPPELPUNKT` and `FRAGEZEICHEN` visible in the complete readable layer. | Direct complete reading; zero substitutions or fills. |

The [live mapping register](../data/reviews/complete_displays_readable_mappings_20261103.json)
binds all three current quotations to **430 ordered nonseparator labels**,
with no display-only inserted letters. It preserves the opening numbers,
the entire `GENERALMAJRHYDEWALD` name field and `PAFR53540` closing, and the
naval references. It does not identify the unresolved fields or establish
historical numeral values.

The [before snapshot](../data/reviews/reading_conventions_complete_displays_before.json)
and [edit audit](../data/reviews/reading_conventions_complete_displays_audit.json)
retain the former text and prove that **19 fenced blocks, 15 section headings
and 74 prior inline-code occurrences** remain unchanged or in their original
order. Eight protected evidence files retain their exact digests, including
the source inputs and certificates for all three editions and the shared
key and challenge registers. The quote completions themselves are checked
against the whole unchanged decoded stream.

```sh
python data/reviews/verify_live_readable_mappings.py --manifest data/reviews/complete_displays_readable_mappings_20261103.json
python data/reviews/verify_semantic_readings.py --snapshot data/reviews/reading_conventions_complete_displays_before.json --audit data/reviews/reading_conventions_complete_displays_audit.json
```

These read-only checks use the existing standard-library verifiers. The
separate source/cipher certificates continue to establish each edition's
frame, repair prices and exact re-encryption witness.
