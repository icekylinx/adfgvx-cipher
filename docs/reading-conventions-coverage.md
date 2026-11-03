# Reading-convention coverage and preservation

Prepared by **icekylinx and GPT-6 Astra Pro**, 3 November 2026 UTC.

The [reading guide](reading-conventions.md) separates Raw output, Edited
output, Readable German and Conditional interpretation. The
[reviewed manifest](../data/reviews/reading_layer_manifest.json) lists every
substantive case present in this presentation snapshot, with a classification
and byte digest for every fenced or quoted display. It records **249 case
pages, 1065 fenced displays and 332 quoted displays**. These are display
counts, not counts of physical telegrams, newly recovered plaintexts or
independently authenticated readings. The checker excludes **48 explicit
compatibility redirects and eight navigation README pages**.

## What is classified

| Fenced display role | Count |
|---|---:|
| Raw output under its stated key and frame | 501 |
| Edited output under its stated repairs | 346 |
| Conditional interpretation | 9 |
| Readable German with linked variables | 1 |
| Earlier attributed reading | 27 |
| Recomputed prior reading | 11 |
| Literal source transcription | 72 |
| Re-encryption witness | 1 |
| Search diagnostic | 1 |
| Geometry-alternative list | 1 |
| Reproduction commands | 95 |

The quoted displays comprise 327 Readable German passages, four separately
labelled conditional interpretations and one English meaning. Their local
qualifiers remain part of the manifest. A Readable German label does not
cancel a stated conditional frame, editorial repair or historical
assumption. Conversely, a source header and a command example are not
classified as decrypted plaintext.

Two non-decoded displays retain explicit prose captions instead of a short
standard label: the cleartext signature outside the ciphertext in the
[hide-purchasing case](../cases/finance/caucasus_hide_purchasing.md), and the
six gap-start numbers in the [p175 C3 follow-up](../cases/military/p175_c3_withdrawal_followup.md).
Their manifest entries record the role, reason and exact local caption.
They are not exemptions for unlabelled plaintext.

## Preservation evidence

| Presentation pass | Scope | What the frozen before-record protects |
|---|---|---|
| Shared legend and initial count terminology | 121 cases, 575 fenced blocks | Complete fenced bytes, existing headings and six key/source evidence files |
| Focused German display review | 12 cases, 42 fenced blocks | The prior fences, 92 headings and 349 inline-code occurrences; the Tiflis readable text separately matches 330 nonseparator labels |
| External layer captions | 138 cases, 637 fenced blocks | Complete fenced bytes and every existing heading; conditional geometry and prior authorship stay explicit |
| English spacing and remaining count units | 25 cases, 91 fenced blocks | Fences, headings, inline code, quoted display lines, URLs and the numeric-token sequence |
| Focused readable-display corrections | 6 cases, 26 fenced blocks | Fences, 33 headings, 143 prior inline-code occurrences and 13 evidence digests; six selected fragment mappings and one explicitly attributed abbreviation interpretation |
| Follow-up shipping-display correction | 1 case, 6 fenced blocks | Six fences, five headings, 15 existing inline-code occurrences and five evidence digests; all three complete readable quotes map to 414 nonseparator labels |

These passes overlap. Their counts must not be added to claim a larger
source corpus. The full-case manifest also includes later source editions
whose authors used the convention when creating them; those pages were not
retroactively included in the first before-snapshot.

The exact before-records and edit inventories are linked from the manifest.
The [focused review](reading-conventions-manual-review.md) explains the
linguistic distinctions, including abbreviation expansion, prose-only
inserted letters, priced coordinate fills, linked unknown values and
conditional historical identification. Every earlier reading retains its
separate authorship and status.

Seven new p160/p161 readable passages additionally match all 614 nonseparator
labels and retain all eight unresolved positions. Five p99 passages have
separate complete mappings. Those exact checks belong to their source
packages; the full-case manifest does not claim universal translation proof.

The later [focused semantic review](reading-conventions-semantic-review.md)
corrects omitted unknown positions and unmarked display-only spelling
changes. Its finite character mappings are recorded separately from the
full-tree role inventory; it does not claim to validate every translation.

## Later label and routing review

The [legacy live-display mappings](../data/reviews/legacy_live_readable_mappings_20261103.json)
bind 37 older passages on 22 case pages to **3,736 ordered labels**, including
**38 unresolved positions**. They separately account for 109 explicitly
bracketed editorial letters. Literal X inside a word or reference is kept
at its reviewed position; it is not removed as generic punctuation.
Balanced inline-code delimiters may mark a literal field, but every label
inside the delimiters remains checked.

Two [documented display corrections](../data/reviews/reading_conventions_detail_audit.json)
restore the Rhine equipment message's `4B4??3?` reference and already encoded
final G in `ABTLG`, and preserve Glatz's literal numeral `2` instead of an
unencoded Roman-II rendering. The original source and decoded streams remain
byte-identical. A [separate prose review](../data/reviews/reading_conventions_detail_prose_audit.json)
clarifies spacing, count grammar, and immediate radio hops versus originating
stations while preserving 61 fenced blocks, 24 quotations and all 1,362
numeric tokens in its 13-file scope. These are overlapping presentation
checks, not additional source records or new historical numeral assignments.

The later [literal-token correction](../data/reviews/reading_conventions_legacy_tokens_audit.json)
retains p152's encoded `SECHSZEHN` and `STRICH`, and p109's complete
`ASOXK511` closing, rather than replacing them with a normalized spelling,
punctuation or a prose placeholder. The frozen source and decoded strings
are unchanged. A separate [count-unit pass](../data/reviews/reading_conventions_count_units_audit.json)
uses positions for streams containing separator and numeral labels while
preserving 18 fences, five quotations and all 611 numerical tokens.

The [Seifert table audit](reading-conventions-seifert-table.md) separately
binds seven readable table rows to 329 ordered labels, including one
unresolved displayed position. Its 19 display-only expansion letters and
two explicitly marked coordinate-completion letters keep distinct roles.
Fenced-block and blockquote coverage alone does not cover Markdown tables.

The [transport table correction](reading-conventions-transport-table.md)
retains the word erasure in `ANH?ENGER` and both count-like unknowns. Its live
table check binds 45 ordered labels with three unresolved positions, while
preserving four other table rows without claiming exact mappings for their
composite or excerpted readings. The two count-like positions share one
unassigned key cell; the word erasure has a separate source-coordinate cause.

The [accounting supplement mapping](reading-conventions-accounting-supplement.md)
binds the experiment README's conservative p175 quotation to 98 ordered
nonseparator labels, retaining both unknown positions and the complete
`89240911?` closing. These supplementary display checks add no physical
source records and do not choose historical numeral values.

Three [completed older quotations](reading-conventions-complete-displays.md)
now include formerly separate opening fields and retain encoded punctuation
words. Their full live mappings preserve 430 ordered labels without adding
any decoded position or repair. The before/after audit protects 19 fenced
blocks, 15 headings, 74 prior inline-code occurrences and eight evidence files.
The earlier excerpting and punctuation rendering were already disclosed.

## Run the checks

From the repository root:

```sh
python data/reviews/verify_reading_conventions.py
python data/reviews/verify_manual_readings.py
python data/reviews/verify_reading_conventions.py --snapshot data/reviews/reading_conventions_layers_before.json --audit data/reviews/reading_conventions_layers_audit.json
python data/reviews/verify_reading_conventions.py --snapshot data/reviews/reading_conventions_spacing_before.json --audit data/reviews/reading_conventions_spacing_audit.json
python data/reviews/check_reading_presentation.py
python data/reviews/verify_live_readable_mappings.py --manifest data/reviews/complete_displays_readable_mappings_20261103.json
python data/reviews/verify_semantic_readings.py --snapshot data/reviews/reading_conventions_complete_displays_before.json --audit data/reviews/reading_conventions_complete_displays_audit.json
python data/reviews/verify_table_readable_mappings.py
python data/reviews/verify_semantic_readings.py --snapshot data/reviews/reading_conventions_transport_table_before.json --audit data/reviews/reading_conventions_transport_table_audit.json
python data/reviews/verify_live_readable_mappings.py --manifest data/reviews/accounting_copy_readable_mapping_20261103.json
python data/reviews/verify_reading_conventions.py --snapshot data/reviews/reading_conventions_count_units_before.json --audit data/reviews/reading_conventions_count_units_audit.json
python data/reviews/verify_semantic_readings.py --snapshot data/reviews/reading_conventions_legacy_tokens_before.json --audit data/reviews/reading_conventions_legacy_tokens_audit.json
python data/reviews/verify_seifert_readable_table.py
python experiments/accounting_copy_reconciliation/verify.py --verify
python data/reviews/verify_live_readable_mappings.py --manifest data/reviews/legacy_live_readable_mappings_20261103.json
python data/reviews/verify_semantic_readings.py --snapshot data/reviews/reading_conventions_detail_before.json --audit data/reviews/reading_conventions_detail_audit.json
python data/reviews/verify_reading_conventions.py --snapshot data/reviews/reading_conventions_detail_prose_before.json --audit data/reviews/reading_conventions_detail_prose_audit.json
```

All scripts use the standard library and derive the repository location from
their own files. They can be invoked by absolute path from another working
directory. The first four commands compare actual stored before-records;
the last command scans the current case tree independently of the manifest.
It fails for a new unreviewed case, a missing or duplicated legend, changed
display bytes/order, or a changed/missing reviewed caption or qualifier.

Run the additional character-mapping and preservation check for the six
focused cases with:

```sh
python data/reviews/verify_semantic_readings.py
python data/reviews/verify_followup_readings.py --verify
```

For a new case or a deliberate evidence update, generate a current inventory
without modifying any case or the reviewed manifest:

```sh
python data/reviews/check_reading_presentation.py --inventory-output /tmp/reading-presentation-inventory.json --output /tmp/reading-presentation-check.json
```

Review the new or changed display roles against their source/model account
before updating the corresponding manifest entries. The inventory's
`role_from_caption` field merely reads a visible label; it does not infer
whether the author's label is historically or cryptographically justified.
Do not replace old before-snapshots to make a changed machine string pass.
A substantive correction needs its own evidence review and preserved
revision history.

These checks establish presentation coverage and preservation. The source
packages' independent cipher, repair and image checks remain responsible
for their own scientific claims.
