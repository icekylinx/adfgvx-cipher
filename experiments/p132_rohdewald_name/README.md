# A source-attested surname proposal for p132 A

[Reading conventions](../../docs/reading-conventions.md)

**Source comparison and verification: icekylinx and GPT-6 Astra Pro.**

The request for a wartime officer-register extract in [p132 A](../../cases/radio/p132_radio_service.md)
can be read with the surname **Rohdewald**, conditional on four additional
observed-coordinate substitutions. This replaces `RHYDEWALD` with `ROHDEWALD`
after `GENERALMAJ`. The complete optional reading costs **ten observed
substitutions and one printed-dash fill**; the existing six-substitution,
one-fill edition remains unchanged.

**Readable German — complete optional surname proposal; literal addressee and footer:**

> Militärmiszion `KOSJOII`. Übersendung eines Kriegsranglistenauszuges des Generalmaj. Rohdewald
> erbeten. Feldeisenbahnchef `PAFR53540`.

`MISZION`, `KOSJOII` and `PAFR53540` are retained as read. The separate
[KOSPOLI proposal](../p132_optional_address/README.md) remains an independent
two-substitution address proposal and is not applied here. The surname is
a historically supported editorial candidate, not an additional directly
fixed plaintext span or a unique identification of the officer.

## Contemporary evidence

The *Deutscher Reichsanzeiger*, 21 April 1913, no. 94, p. 4, records a Major
Rohdewald moving from the Great General Staff's railway department to a
battalion command in Infantry Regiment 159. The
[Mannheim University Library transcription](https://digi.bib.uni-mannheim.de/reichsanzeiger/ocr/film/tesseract-4.0.0-20181201/126-9532/0243.hocr)
prints the surname `Rohdewald` under **Personalveränderungen / Königlich
Preußische Armee / Im aktiven Heere**. The exact OCR context is:

> Als Bats. Kommandeure verseßt: die Majore: Rohdewald in der Cisenbahnabteil. des Großen Generalstabes, în das 8. Lothring. Inf. Negt. Nr. 159

OCR spellings such as `Cisenbahnabteil.` and `Negt.` are retained in that
quotation. The railway context is relevant to the telegram's literal
`FELDEISENBAHNCHEF` sender. The notice supports the surname spelling; it
does not establish that the 1913 officer and the general in this November
1918 message are the same person.

The library's [official issue record](https://digi.bib.uni-mannheim.de/urn/urn:nbn:de:bsz:180-digper-134203),
[page 4 viewer](https://digi.bib.uni-mannheim.de/en/werksansicht/72009/4?cHash=3c5878d7087c8401b4d1afd6b768877a&tx_dlf%5Baction%5D=main&tx_dlf%5Bcontroller%5D=Navigation&tx_dlf%5Bdouble%5D=0)
and [page-image download](https://digi.bib.uni-mannheim.de/periodika/fileadmin/data/DeutReunP_856399094_19130421/default/856399094_1913_094_04.jpg)
are identified for checking. **The OCR context was independently checked;
the page-image pixels were not independently inspected.** No first name,
birth date, promotion date or Ottoman assignment is adopted from later
biographical accounts. The ciphertext itself fixes neither this candidate
nor a unique personal identity.

## Incremental cipher evidence

The unchanged `Nov4-6` key gives raw `RHYDEWALD`. Only its second and third
letters change. Both halves of each printed coordinate pair must be
replaced; this is four coordinate substitutions, not two mask fills.
All source and plaintext indices in this table are zero-based.

| Plaintext index | Letter | Observed pair → proposed pair | Source indices and changes |
| ---: | --- | --- | --- |
| 78 | `H` → `O` | `AG` → `GA` | 194: `A` → `G`; 37: `G` → `A` |
| 79 | `Y` → `H` | `GV` → `AG` | 152: `G` → `A`; 223: `V` → `G` |

The [original p132 A source crop](../november_radio_service/sources/childs_p132_A.png)
shows ordinary coordinate glyphs at all four positions. This proposal
does not reinterpret them as uncertain source marks. No source slot,
transposition order or square cell changes. The original dash fill and
all numerical labels are preserved.

## Reproduction

The compact [input](inputs.json) pins the existing source input, key and
source crop; it adds only the name replacement, incremental changes and
historical citation. The [certificate](certificate.json) rebuilds the
121-position proposal and its complete forward witness directly from
the 242 literal source slots. It also checks the unchanged baseline
cost and disjointness of the four extra changes. Raw coverage remains
120/121, with no new physical record or decipherment claim.

The published period key remains credited to **George Lasry, Ingo Niebel,
Nils Kopal and Arno Wacker**; its provenance is preserved in the existing
[source edition](../november_radio_service/README.md).

```sh
python experiments/p132_rohdewald_name/verify.py --verify
python experiments/november_radio_service/verify.py --verify
python experiments/p132_optional_address/verify.py --verify
```
