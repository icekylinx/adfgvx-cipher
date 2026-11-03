# Gomel route derailment and station-train forwarding

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

Two source editions concern railway operations: a freight-train derailment blocking both tracks on the proposed Gomel–Bachmatsch route, and a message about forwarding a station train and construction train to Group Winterfeld. The wagon count, train labels, abbreviations and office references remain literal.

## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed page excerpt](../../experiments/nov7_derailment_and_trains/sources/p155_reviewed.png) · [Second source excerpt](../../experiments/nov7_derailment_and_trains/sources/p169_reviewed.png) · [Exact inputs](../../experiments/nov7_derailment_and_trains/inputs.json) · [Position-by-position certificates](../../experiments/nov7_derailment_and_trains/certificates.json)

The unchanged published keys are `Nov7-9`. The [earlier unreviewed candidates](../../experiments/nov7_derailment_and_trains/prior_candidates.json) and [original OCR records](../../experiments/nov7_derailment_and_trains/ocr_snapshot.json) are preserved. The present work supplies an image-reviewed source edition and a reproducible repair account; it does not claim that every body is a first public decipherment.

| Record | Source slots | Fixed raw positions | Coordinate substitutions | Source-mask fills |
|---|---:|---:|---:|---:|
| [p155 D](#p155-d) | 316 | 152 / 158 | 3 | 5 |
| [p169 B](#p169-b) | 224 | 108 / 112 | 0 | 0 |

## p155 D

**Source transcription — header:** `D) NKJ v LP (3.55 p.m., November 7th); FUER UKS 1355; RICHI-316`

**Readable German** — based on the explicitly repaired output below.

> OK Mackensen. Morgenmeldung vom 7X11X18: Auf Strecke Gomel, Bachmatsch entgleiste ein Gueterzug. 2? Wagen zertruemmert. Beide Gleise sind gesperrt. Hrgr. Kiew RMX1XAX7097X18.

**Meaning:** A morning report addressed to Oberkommando Mackensen says a freight train derailed on the proposed Gomel–Bachmatsch route, that a quantity written 2? of wagons was wrecked, and that both tracks are blocked. The unresolved wagon-count label and final reference remain literal.

**Raw output** — every native source slot in printed order, under the stated published key.

```text
OKXMACKENSENXXMORGENMELDUNGVOM7X11X18AUFSTRECKEXGOMELXBNCHMABSCH?ENBGLEISTEEI?GUETERZUG?2?WAGENZE?TRUEMMERT?BEIDEGLEISESINDGESPERRTXXHRGRXKIEWXRMX1XAX7097X18X
```

**Edited output** — 3 observed-coordinate substitutions and 5 source-mask fills; no coordinate inserted, deleted or moved.

```text
OKXMACKENSENXXMORGENMELDUNGVOM7X11X18AUFSTRECKEXGOMELXBACHMATSCHXENTGLEISTEEINGUETERZUGX2?WAGENZERTRUEMMERTXBEIDEGLEISESINDGESPERRTXXHRGRXKIEWXRMX1XAX7097X18X
```

**Unresolved details and editorial limits.**

- The source has four dashes and a literal Y-shaped noncoordinate glyph in DXYVF. These five slots are masked before decoding and filled separately in the proposed reading.
- The place repair BNCHMABSCH to BACHMATSCH requires two observed-coordinate substitutions; the other substitution changes ENBGLEISTE to ENTGLEISTE. This is an explicit word proposal, not a new external geographical identification.
- The unknown in 2? is the globally unresolved XA cell, whose domain is {5,6} in the published Nov7–9 square. This edition does not choose 25 or 26 wagons.
- Correct source groups FVXDD and VXDVG each have five slots. Earlier OCR strings with repeated X coordinates are not treated as source evidence.

## p169 B

**Source transcription — header:** `B) ZM v SY (10.00 p.m., November 9th); 2245 (9/11); RICHI-224`

**Readable German** — based on the unchanged raw output.

> NACHRUEBGEL. FECH wird beschleunigt Stationszug S11?2 und Bauzug 1924 der Gruppe Winterfeld zufuehren. Nachchef 1B1??1?.

**Meaning:** The station train labelled S11?2 and construction train labelled 1924 are to be forwarded promptly to Group Winterfeld. The opening NACHRUEBGEL and FECH are preserved without forcing an expansion, and the train and office labels are not independently numbered.

**Raw output** — every native source slot in printed order, under the stated published key.

```text
NACHRUEBGELXFECHWIRDBESCHLEUNIGTSTATIONSZUGXS11?2XUNDBAUZUGX1924XDERGRUPPEXWINTERFELDZUFUEHRENXNACHCHEFX1B1??1?X
```

**Unresolved details and editorial limits.**

- The complete 224-slot source frame requires no observed-coordinate substitution or source-mask fill.
- DXGVV is a five-coordinate printed group; the older OCR included an extra uncertainty mark.
- The reference 1B1??1? and the station-train field retain all coupled unassigned square cells. A global witness is provided without claiming literal historical digit values.

## Coupled wagon and train labels

The unresolved symbols are linked by the unchanged Nov7–9 square. All indices below are zero-based plaintext positions.

| Square cell | Source occurrences | Shared constraint |
| --- | --- | --- |
| XA | p155 D position 89; p169 B position 47 | The unknown in wagon label `2?` is the same label as the unknown in train label `S11?2`. |
| VF | p169 B positions 107, 108 and 110 | All three unknowns in `1B1??1?` are the same label, and differ from XA. |

VF and XA carry the two remaining labels `{5, 6}` bijectively. There are therefore two global assignments, not five independent numerical guesses. Neither assignment is established as the historical numbering.

## Evidence and credit

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier unreviewed repository candidates are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro. No universal first-decipherment priority is asserted.

The certificates replay every coordinate alteration, compare the independent column/domain reconstruction with the cipher implementation, and re-encrypt every complete edited output. For a partial output, an injective global completion of the square and residual source masks supplies an explicitly nonhistorical roundtrip witness. Each readable passage preserves every nonseparator output label; literal protected fields are also checked without removing their internal separators. Source crops are bound to the original PDF by page, rectangle, scale, file digest and RGB-pixel digest.

Reproduce with `python experiments/nov7_derailment_and_trains/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to regenerate and compare the delivered source pixels.

A roundtrip proves compatibility with a stated reading. Editorial spelling repairs remain proposals, and literal number labels are not automatically historical dates, quantities or reference numbers.
