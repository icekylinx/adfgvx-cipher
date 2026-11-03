# Ober Ost troop movements: a conditional reading across two obliterations

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

The first part of p186 B proposes troop movements within the Ober Ost territory. This reading depends on explicitly excluding two obliterated group-width regions. The surviving second part independently describes soldiers wanting to travel home without authorization; it is published in the [native companion edition](home_departures_baltic_transport.md#p186-b2).

## Source geometry and its limits

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p186 excerpt](../../experiments/oberost_troop_movement_obliterations/sources/p186_reviewed.png) · [Inputs](../../experiments/oberost_troop_movement_obliterations/inputs.json) · [Position certificates and controls](../../experiments/oberost_troop_movement_obliterations/certificates.json)

**Source transcription — header:** `B) NKJ v LP (06.23 a.m., November 13th); FUER WAU 07.00 2 TLE; 1 TL RICHI-308`

The fourth ciphertext row has two heavily obliterated regions between GFDXG and the following C/G-ambiguous group. They occupy two ordinary group columns, but five separate original glyphs cannot be counted in either region. The disclosed **318-position composite layout** consists of **308 individually transcribed positions plus two regions modeled as five masks each**. It is not a claim that 318 separate original coordinate letters remain visible.

**Conditional interpretation — source-row layout with five inferred masks for each obliterated group column:**

```text
GFDXG ????? ????? FGCGA AFGFA GVXVD DXXXF AFFVF
```

The C/G-shaped glyph in FGCGA is transcribed C and masked; its ambiguity is independent of the two obliterated regions. The Y-like glyph in XYVXX is also masked. All other positions are retained in source order.

The primary frame excludes the ten modeled masks at composite source indices 125–134, yielding the advertised 308 coordinates. This costs **ten masked-layout-slot exclusions**. It deletes no observed coordinate. The agreement with the heading supports examining this geometry, but neither the heading nor a readable result proves that the obliterations were intended cancellations.

The certificate preserves all four choices: retain both regions (318 positions), exclude either region alone (313 positions), and exclude both (308 positions). Both odd-length controls explicitly identify their unpaired intermediate coordinate and its source index; their final coordinate is not silently discarded as source evidence. The two single-region controls happen to have identical streams because both regions are entirely masked.

## p186 B1

**Raw output — retain both five-mask regions in the 318-position composite layout; diagnostic only:**

```text
?0AMOVBM1ZRPVZR??LS?R5FDX?TXZO0SPX?5ICFJA??H?O6??R?K1CC6XP?PX?TK6V?MXV?I?F?Z0XENUF?6FVTPVC?EOHEPE??E?ZBIMA?INTCGMG?III???C?GZSELW?LUNMOB5XG?IMEDGS?EZ?EDNIBCLDP
```

**Raw output — conditional 308-coordinate frame after ten masked-layout-slot exclusions; 150 of 154 positions fixed:**

```text
GENXGOUVXWARSCHAUXZ0FORTX?MX1AXNRR6?1X15XGENXVX10X11XISTANOBOSTGEDRAHTETXXESWIRDVORGESCHLX?ENXTRUPPENVERSCHIEBUNG?NINNERHALBDESOBEROSTGEBIETSVORZUNEHMENXX
```

**Edited output — same conditional frame, one observed-coordinate substitution and two source-mask fills; 152 of 154 positions fixed:**

```text
GENXGOUVXWARSCHAUXZ0FORTX?MX1AXNRR6?1X15XGENXVX10X11XISTANOBOSTGEDRAHTETXXESWIRDVORGESCHLAGENXTRUPPENVERSCHIEBUNGENINNERHALBDESOBEROSTGEBIETSVORZUNEHMENXX
```

All indices below refer to the 318-position composite source layout. The observed substitution is **88 D→V**. The two source-mask fills are **91 Y-like glyph→X** and **137 C/G-shaped glyph→G**. The ten excluded masks do not receive guessed coordinate values and are not counted as fills.

**Readable German — conditional frame and explicitly priced changes; opaque fields retained:**

> Gen. Gouv. Warschau. Z0FORT. ?MX1AXNRR6?1X15XGENXVX10X11 ist an OBOST gedrahtet. Es wird vorgeschlagen, Truppenverschiebungen innerhalb des Oberostgebiets vorzunehmen.

**Meaning:** The body addresses GEN GOUV WARSCHAU, says that the referenced item has been wired to OBOST, and proposes troop movements within the Ober Ost territory. Z0FORT and the opening reference remain opaque literal fields. The text is a proposal, not evidence that the movements occurred.

The two remaining unknowns come from unresolved square cells: VG at plaintext index 25 and AF at index 35. The AF position is coupled to p186 C1 index 11; it must differ from GA, which is shared by p186 B2 index 109 and C1 index 9. All indices are zero-based, and none of these reference labels is historically assigned. The published Nov13–15b key is unchanged; its nonhistorical injective completion witness verifies compatibility without selecting historical numeral labels. Z0FORT is not silently normalized to SOFORT, and the reference `?MX1AXNRR6?1X15XGENXVX10X11` remains literal. The phrase “ist an OBOST gedrahtet” reports earlier transmission of the referenced item; the following sentence proposes movements. Neither establishes that troop movements occurred.

## Exact account

| Quantity | Count |
| --- | ---: |
| New physical source records | 1 |
| Individually transcribed positions | 308 |
| Added layout masks for two obliterated group columns | 10 |
| Composite layout positions | 318 |
| Conditional analyzed coordinates / plaintext positions | 308 / 154 |
| Fixed conditional raw / edited labels | 150 / 152 |
| Excluded layout masks / excluded observed coordinates | 10 / 0 |
| Observed-coordinate substitutions / source-mask fills | 1 / 2 |
| Inserted coordinates or reordered source positions | 0 |

These counts exclude the already separate native second part. The certificate's `printed_source_slots` is 308, while `composite_layout_slots` is 318; `source_deletions` counts the ten modeled-mask exclusions, with `observed_coordinate_deletions` separately fixed at zero. This prevents the group-width model from being represented as ten legible original letters.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.

[Earlier OCR candidates](../../experiments/oberost_troop_movement_obliterations/prior_candidates.json) and the [original OCR snapshot](../../experiments/oberost_troop_movement_obliterations/ocr_snapshot.json) remain separately frozen. The new source analysis does not treat an OCR token count as a historical received length.

```sh
python experiments/oberost_troop_movement_obliterations/verify.py --verify
python experiments/oberost_troop_movement_obliterations/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

Verification checks every source/model index, the four control frames, all position domains, each proposed change, exact readable-label preservation, an injective global completion witness, unchanged key provenance and the optional original-PDF crop pixels. A successful roundtrip establishes compatibility with the declared exclusion model, not a unique historical reading or cancellation intent.
