# Reading-convention coverage and preservation

Prepared by **icekylinx and GPT-6 Astra Pro**, 3 November 2026 UTC.

The [reading guide](reading-conventions.md) separates Raw output, Edited
output, Readable German and Conditional interpretation. The
[reviewed manifest](../data/reviews/reading_layer_manifest.json) lists every
substantive case present in this presentation snapshot, with a classification
and byte digest for every fenced or quoted display. It records **150 case
pages, 682 fenced displays and 152 quoted displays**. These are display
counts, not counts of physical telegrams, newly recovered plaintexts or
independently authenticated readings. The checker excludes **48 explicit
compatibility redirects and eight navigation README pages**.

## What is classified

| Fenced display role | Count |
|---|---:|
| Raw output under its stated key and frame | 314 |
| Edited output under its stated repairs | 185 |
| Conditional interpretation | 6 |
| Readable German with linked variables | 1 |
| Earlier attributed reading | 27 |
| Recomputed prior reading | 11 |
| Literal source transcription | 51 |
| Re-encryption witness | 1 |
| Search diagnostic | 1 |
| Geometry-alternative list | 1 |
| Reproduction commands | 84 |

The quoted displays comprise 147 Readable German passages, four separately
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

## Run the checks

From the repository root:

```sh
python data/reviews/verify_reading_conventions.py
python data/reviews/verify_manual_readings.py
python data/reviews/verify_reading_conventions.py --snapshot data/reviews/reading_conventions_layers_before.json --audit data/reviews/reading_conventions_layers_audit.json
python data/reviews/verify_reading_conventions.py --snapshot data/reviews/reading_conventions_spacing_before.json --audit data/reviews/reading_conventions_spacing_audit.json
python data/reviews/check_reading_presentation.py
```

All scripts use the standard library and derive the repository location from
their own files. They can be invoked by absolute path from another working
directory. The first four commands compare actual stored before-records;
the last command scans the current case tree independently of the manifest.
It fails for a new unreviewed case, a missing or duplicated legend, changed
display bytes/order, or a changed/missing reviewed caption or qualifier.

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
