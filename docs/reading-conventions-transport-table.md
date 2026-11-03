# Transport table: an erasure and two linked unknowns

Prepared by **icekylinx and GPT-6 Astra Pro**, 3 November 2026 UTC.

The p189 E row in the [transport case](../cases/context/transport.md#most-likely-readings)
previously displayed *Anhaenger*, while its unchanged raw output says
`ANH?ENGER`. The corrected readable cell displays **Anh?enger**. This
restores an unresolved position without adding a source repair or choosing
a missing coordinate.

The [before-record](../data/reviews/reading_conventions_transport_table_before.json)
and [edit audit](../data/reviews/reading_conventions_transport_table_audit.json)
preserve the prior page and the exact change. All three fenced displays,
five headings, 43 existing inline-code occurrences, the source image, the
published-key register and the original transport certificate remain intact.

## Three displayed question marks have two causes

| Plaintext position | Source pair | Cause | Preserved constraint |
|---:|---|---|---|
| 26, before `AUTOS` | `VG` | Unassigned square cell | Same value as position 37; domain `234789QY`. |
| 37, before `ANH?ENGER` | `VG` | The same unassigned square cell | Same value as position 26. |
| 41, inside `ANH?ENGER` | `V?` | Literal invalid B at source index 81 | Domain `234789AKNQWYZ`; the missing coordinate remains unfilled. |

Indices are zero-based. The two complete `VG` pairs make a shared key-cell
constraint. The word's `V?` pair instead contains an erased source
coordinate. Its domain includes A, but membership alone does not select A.
The count-like context of the other two positions does not identify a digit
or discard their Q/Y alternatives.

## Live coverage

The [table manifest](../data/reviews/transport_table_readable_mappings_20261103.json)
maps the complete p189 E readable cell to **45 ordered nonseparator labels**
of its 47-position raw stream, retaining all **three unknown positions**.
It binds the two `VG` positions and the independent source erasure to the
unchanged [transport certificate](../data/certificates/p185_D_transport.json).
The other four table rows remain byte-preserved with their original
editorial qualifications; they are not claimed as exact full-stream
mappings by this review.

The manifest-driven checker shares the table parsing and explicit bracket
rules used for the [Seifert table](reading-conventions-seifert-table.md).
It checks the current Markdown instead of only a frozen display string.

```sh
python data/reviews/verify_table_readable_mappings.py
python data/reviews/verify_semantic_readings.py --snapshot data/reviews/reading_conventions_transport_table_before.json --audit data/reviews/reading_conventions_transport_table_audit.json
```

Both commands are read-only and use the standard library. This is a display
correction and constraint explanation, with no new physical source record,
new recovered plaintext position or changed cipher model.
