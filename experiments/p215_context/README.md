# p215: Corps Kosch and the limits of the naval context

**`KORPSXKOSCH` is a better supported editorial interpretation than
`KORPSFRISCH`, but it is not an exact decryption.** At the same eleven plaintext
positions, the Kosch reading needs two changes to known received coordinates;
the earlier Frisch reading needs five. Contemporary documents independently
place General Kosch and his command in Crimea. Neither consideration turns an
unobserved coordinate into source evidence.

Research, coordinate audit and presentation: **icekylinx and GPT-6 Astra Pro**.
The key, missing-group hypothesis and most of the recognizable body are prior
work: [Norbert, comment 32, 3 March 2017](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1#comment-853562),
followed by [Max Baertl, comment 39, 11 March 2017](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1#comment-858010).
The specific Kosch interpretation and its comparison are the present addition.

## Most likely readable segment

> […] [Kertsch]. Bringt [Ententeflotte] zwo [Divisionen] — [Neuseelaender],
> Engl. u. [Franzo] — mit. [Nur] OHL, [Korps Kosch]. 3Y52.

This is a **conditional editorial reading**, with words requiring an erased
letter or a changed known coordinate placed in brackets. Punctuation, spaces
and the division of clauses are editorial. The unresolved opening prevents a
secure explanation of the relationship between Kerch and the report. `Franzo`
is retained as an abbreviation rather than silently expanded. `OHL` most
plausibly means *Oberste Heeresleitung*; the proposed *nur OHL* may restrict
distribution. `3Y52` remains literal, even though the historical command was
numbered 52.

**Proposed meaning:** an incomplete report connected with Kerch says that the
Entente fleet brings two divisions, described as New Zealanders, English and
French. The closing words may restrict circulation to the Supreme Army
Command and Corps Kosch. This translates the proposed report; it does not
establish that those troops actually arrived or that the number and nationalities
were accurate.

The compact 92-character segment, occupying positions 33–124 inclusive, is:

```text
KERTSCHXBRINGTENTENTEFLOTTEZWODIVISIONENXNEUSEELAENDERXENGLXUXFRANZOXMITXNUROHLXKORPSXKOSCHX
```

It requires **nine known-coordinate substitutions and fifteen erasure fills**
under Norbert's geometry. Eight fills concern printed source erasures; seven
belong to the two hypothesized missing groups. The opening 33 characters and
the final four-character reference are not repaired by this proposal.

| Proposed span | Plaintext positions, zero-based | Known-coordinate changes | Erased-coordinate fills |
| --- | ---: | ---: | ---: |
| `KERTSCH` | 33–39 | 0 | 2 |
| `ENTENTEFLOTTE` | 47–59 | 2 | 2 |
| `ZWODIVISIONEN` | 60–72 | 0 | 3 |
| `NEUSEELAENDER` | 74–86 | 1 | 2 |
| `FRANZO` | 95–100 | 2 | 2 |
| `NUROHL` | 106–111 | 2 | 2 |
| `KORPSXKOSCH` | 113–123 | 2 | 2 |

The opening remains especially uncertain. `MI?I5` permits `MILI5` after one
inserted-coordinate fill, but no independent expansion of that identifier was
found. `MIDI5` would additionally require changing a known coordinate. The old
`EILMELDG` proposal needs five known-coordinate changes at positions 10–17.
Neither is adopted as established wording here.

## Exact cost of the Kosch interpretation

The reproduced raw span is `KOR1S??OSCH`. The following operations are all
required; indices refer to the unaugmented printed transcript unless stated
otherwise.

| Plaintext position | Required interpretation | Coordinate operation |
| ---: | --- | --- |
| 116 | `1` → `P` | Original coordinate 22: `X` → `V`; the other half stays `X` |
| 118 | Unknown → separator `X` | Original coordinate 193: `D` → `X`, plus `A` in augmented gap position 34 |
| 119 | Unknown → `K` | Fill augmented gap position 221 with `F`; original coordinate 51 remains `X` |

Position 118 has the original domain `3459NT`, so its proposed separator is
**not** a free choice within an erasure. Position 119 has domain `1GJKWX`,
which does permit `K`. The alternative `KORPSFRISCH` contradicts four plaintext
domains and five known coordinates, at original offsets 22, 193, 51, 98 and 40.
Both proposals fill two inserted gaps. The comparison concerns these eleven
positions only; it does not make the earlier 130-character full completion fit
the 129-character reconstruction.

[The machine-readable audit](interpretation_costs.json) records every changed
coordinate, every fill, the precise permitted domains and a partially
reencrypted witness for each span. Coordinates outside the chosen span stay
as received or erased.

<a id="what-the-documents-support"></a>

## Kosch identification and naval context

The source is Winfried Baumgart's 1971 edition of the Paquet, Groener and
Hopman papers, digitized by the Bayerische Staatsbibliothek. Its
[29 April 1918 naval directive, printed page 485, note 137](https://api.digitale-sammlungen.de/iiif/image/v2/bsb00042051_00495/full/1800,/0/default.jpg)
identifies Kosch as German commander in Crimea. The cited archive reference is
MGFA, PG 69257. The editor's separate
[biographical note, page 294, note 145](https://api.digitale-sammlungen.de/iiif/image/v2/bsb00042051_00300/full/1800,/0/default.jpg)
identifies him with General Command 52; that note is modern editorial context.

Hopman's diary places Kosch at a
[15 November meeting on German troop evacuation](https://api.digitale-sammlungen.de/iiif/image/v2/bsb00042051_00655/full/1800,/0/default.jpg),
and mentions [GK 52 on 20 November](https://api.digitale-sammlungen.de/iiif/image/v2/bsb00042051_00658/full/1800,/0/default.jpg).
His [22 November entry](https://api.digitale-sammlungen.de/iiif/image/v2/bsb00042051_00659/full/1800,/0/default.jpg)
records notice of expected British and Allied naval arrivals at Sevastopol on
24 and 26 November. None of these passages quotes p215 or confirms its proposed
two divisions and nationalities.

An independent contemporary document is the Australian War Memorial's
[fleet memorandum No. 51468, dated 24 November 1918](https://transcribe.awm.gov.au/transcription/item/rcdig0000179-4),
in the Cyril John Percy Hill papers, accession RCDIG0000179. The
[original first page](https://transcribe.awm.gov.au/sites/default/files/transcription-images/2025-07/61771-rcdig0000179-page51.jpg)
records the advance ships' departure on 23 November and the main fleet's
planned departure on 25 November. Its
[first enclosure](https://transcribe.awm.gov.au/sites/default/files/transcription-images/2025-07/61774-rcdig0000179-page54.jpg)
organizes destroyers in two divisions. This supplies naval context and an
independent check on the broad chronology relevant to [p217](../../cases/pages/217.md#edition-cases-p217).
It does **not** identify p215's proposed divisions as destroyers or establish a
New Zealand landing. The original images were checked because the site's
community transcription was still marked “Awaiting approval.”

## Scope and reproduction

[Source context and provenance](source_context.json) separates primary texts,
editorial annotations, visual inspections and bounded negative searches.
Official diary searches and a 788-block Childs OCR retrieval did not produce a
new source-verified p215 retransmission or an expansion of `MI?I5`. OCR hits
remain retrieval candidates; a short `MILI5` sequence inside p209 garble is not
accepted as evidence.

The current coordinate check is `python experiments/p215_context/audit_interpretation.py --check`.

**Historical commands — the second runner is retired.** The frozen transcript
below is retained for the earlier presentation audit. The unused OCR queue
and retrieval runner are available in the [archived experiment](https://github.com/icekylinx/adfgvx-cipher/tree/654039811795311ed967f11c97883ef2c3c8a736/experiments/p215_context).

```sh
python experiments/p215_context/audit_interpretation.py --check
python experiments/p215_context/retrieve_context.py
```

The coordinate audit independently rebuilds the column geometry from the
[existing p215 certificate](../../data/certificates/p215.json). It verifies
conditional costs and re-encryption witnesses, not the historical truth of a
reading. The retired retrieval evaluated 165,216 bounded models with 24 fixed
historical keys and supplied no accepted retransmission or expanded opening.
Its historical negative result does not exclude missing documents, different
geometry or other keys.
