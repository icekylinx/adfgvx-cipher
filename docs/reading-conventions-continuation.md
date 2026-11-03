# Continuation cases: complete live readable mappings

Prepared by **icekylinx and GPT-6 Astra Pro** on 3 November 2026.

The [supplementary manifest](../data/reviews/live_readable_mappings_20261103_continuation.json)
binds **35 complete readable quotations on 16 case pages** to their exact
local raw or edited streams. These cover **34 physical records**: p144 B
has both a primary reading and a separately priced optional opening.
This display count adds no physical record. The original 141-mapping
manifest remains unchanged.

The existing [live checker](../data/reviews/verify_live_readable_mappings.py)
verifies **2,761 ordered nonseparator labels**, including **26 unresolved
positions across the displayed quotations**, with **no display-only
inserted letters**. It reads the current Markdown, pins the decoded stream
hash and both layer captions, then checks all labels in order. Numerals,
opaque fields, unusual spellings and every literal `?` remain subject to
that equality. No `?` is interpreted as sentence punctuation here.

## Included case pages

| Case | Physical records | Readable quotations |
| --- | --- | ---: |
| [Nikolajew acknowledgment](../cases/radio/nov2_nikolajew_acknowledgment.md) | p105 A | 1 |
| [Boat-crossing fragment](../cases/military/nov6_boat_crossing_fragment.md) | p144 B | 2 |
| [Tiflis Ringbahn instruction](../cases/radio/nov6_tiflis_ringbahn_instruction.md) | p146 C1/C2 | 2 |
| [Poti tobacco loading](../cases/naval/nov3_poti_tobacco_loading.md) | p113 C | 1 |
| [Flying-unit inquiry](../cases/military/nov4_flying_unit_inquiry.md) | p124 B | 1 |
| [Marine-service notice](../cases/radio/nov6_marine_service_notice.md) | p138 C | 1 |
| [Eilvese traffic schedule](../cases/radio/nov3_eilvese_traffic_schedule.md) | p113 D1 | 1 |
| [Reverse keys and date correction](../cases/radio/nov22_reverse_keys_and_date_correction.md) | p214 A1/C | 2 |
| [Radio personnel and key notice](../cases/radio/nov15_radio_personnel_and_key_notice.md) | p197 A1/A2/B | 3 |
| [Ships and vehicle sale](../cases/naval/nov27_ships_and_vehicle_sale.md) | p223 B/C | 2 |
| [Baku personnel inquiry](../cases/caucasus/baku_personnel_inquiry.md) | p185 B | 1 |
| [Crown airlift and embassy address](../cases/finance/nov9_crown_airlift_and_embassy.md) | p167 B1/B2/B3/E1 | 4 |
| [Embassy address parts](../cases/radio/nov7_8_embassy_address_parts.md) | p156 A1/B1/D1/E1; p158 A1/A2/B1 | 7 |
| [Serbian cavalry parallel](../cases/military/nov8_serbian_cavalry_parallel.md) | p158 E1 | 1 |
| [Arad provisions partial reading](../cases/military/arad_provisions_partial.md) | p159 A | 1 |
| [Danube crossings and message reports](../cases/military/nov7_danube_and_message_reports.md) | p152 B2/C/D; p153 A3/B1 | 5 |

## Literal fields and boundaries

Two `X` occurrences remain literal inside displayed fields: **position 4**
in p124 B's `??ERX?K??1?2??OP?`, and **position 22** in p113 D1's `3X13`.
These are zero-based plaintext positions. The manifest explicitly retains
them; the other omitted `X` occurrences in the selected streams are
reviewed separators. Fields such as `UPK3`, `???6?5`, `????STRICHA?`,
`4B47857`, `KIE?` and `O?MANIE` receive additional literal-field checks.
The exact ordered-label comparison also covers all repeated numeral labels
and the separate `28` and `10` displayed as `28/10` in the Poti record.
The pp. 152–153 extension also binds `EB?Q`, `219`, `EINSA11205BM4`,
`1189`, `35`, `21B` and `SEMUM`. Its complete quote equality retains the
unusual `NOORDL` spelling, while the separately priced word repairs remain
visible in the raw and edited layers.

No complete readable quotation on these pages was skipped, and no excerpt
was treated as a complete stream. A whole printed part can end mid-sentence;
the mapping supplies none of its missing continuation. Native-frame
diagnostics, alternative raw frames, the p156 A1 overstrike reading and the
older p162 D1 comparison remain separate evidence displays without their
own additional readable quotations. The 16 package READMEs contain no
blockquoted German displays at this review.

The ambiguous p156 A1 header count `[2/3] TLE` remains outside the plaintext
mapping and retains its two complete header alternatives in the source
package. These checks establish display fidelity, not source authenticity,
historical numeral assignments, coordinate repair prices, a unique frame
or unique historical wording. Each experiment's source and cipher verifier
continues to establish its separate arithmetic and evidence claims.

## Reproduce

From the repository root:

```sh
python data/reviews/verify_live_readable_mappings.py --manifest data/reviews/live_readable_mappings_20261103_continuation.json
```

No case quotation, raw or edited stream, source record, key or certificate
was changed to make these mappings pass.
