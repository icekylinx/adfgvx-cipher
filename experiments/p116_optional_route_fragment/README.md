# Optional route vocabulary in the jammed p116 A13

[Reading conventions](../../docs/reading-conventions.md)

**Source comparison and verification: icekylinx and GPT-6 Astra Pro.**

The [primary withdrawal-report edition](../../cases/military/mackensen_withdrawal_report.md#p116-a13)
leaves the final part raw-only. This separate supplement tests five German
word spans suggested by the surviving coordinates and the already published
historical translation. They produce **75 fixed labels out of 111** under
the unchanged length and key, using **zero observed-coordinate changes,
five printed-mask fills and 32 lost-tail fills**. The primary edition stays
unchanged, with 38 directly fixed labels and no fills.

These are explicitly conditional word choices. Every one of the 37 proposed
letters keeps one observed coordinate and supplies its missing partner;
none completes a pair whose two coordinates are both absent. The surviving
half-pair still permits six labels, so this compatibility does not make the
proposed letters direct observations.

## The same source and loss model

The [already published page image](../mackensen_withdrawal_report/sources/p116.png)
prints `13 TL`, `RICHI-222`, four rows totaling **160 slots**, and the note
“Balance jammed.” Of those slots, 144 are valid observed coordinates and
16 are printed dashes. The existing edition appends 62 unknown coordinates
after the final row and uses the published **Nov1–3** square and column ranks.
This supplement retains that model, every source glyph and the full
source-to-plaintext map. It introduces no extra deletion, insertion,
reordering, key change or visual transcription correction.

**Raw output — unchanged primary reading under the existing 222-slot frame:**

```text
??????DERX?????MEED??M???CHDU?????GARN??F???R?CH??????A?Z??????N?EI?????T??N??????R?ET?????XK????M???A?1G?????X
```

The native 160-slot inverse and the conditional 222-slot inverse are both
included in the certificate. The readable pattern belongs to the latter
model; it must not be attributed to the unextended 160-slot ciphertext.

## Five optional spans and their exact cost

All indices in this supplement are zero-based. The spans do not change any
already decoded label.

| Plaintext positions | Proposed span | Raw fixed labels in span | Added labels | Printed-mask fills | Lost-tail fills |
| --- | --- | ---: | ---: | ---: | ---: |
| 0–5 | `TEILEN` | 0 | 6 | 1 | 5 |
| 13–17 | `ARMEE` | 3 | 2 | 0 | 2 |
| 18–37 | `DENMARSCHDURCHUNGARN` | 10 | 10 | 0 | 10 |
| 38–53 | `AUFOBERSCHLESIEN` | 4 | 12 | 2 | 10 |
| 54–63 | `ANZUTRETEN` | 3 | 7 | 2 | 5 |
| **Total** | | **20** | **37** | **5** | **32** |

**Edited output — separate optional lexical completion; 75/111 fixed labels:**

```text
TEILENDERX???ARMEEDENMARSCHDURCHUNGARNAUFOBERSCHLESIENANZUTRETEN?EI?????T??N??????R?ET?????XK????M???A?1G?????X
```

**Readable German — complete optional stream, retaining all 36 unresolved positions:**

> Teilen der X `???` Armee den Marsch durch Ungarn auf Oberschlesien anzutreten`?` `EI?????T??N??????R?ET?????XK????M???A?1G?????X`.

The initial noun fragment continues the preceding part. Under this proposal,
the surviving passage concerns a proposed march through Hungary toward
Upper Silesia. It does not establish that the march occurred. The army label,
the following damaged clause and the footer remain unresolved in this route
layer; no signature or approval formula is supplied here.

The five printed-dash fills are source indices **5→G, 70→A, 76→D, 155→V and
156→G**. The 32 additional fills fall in the already modeled unprinted run.
Every fill has its exact model index, source origin, pair and affected label
in [the certificate](certificates.json). Eleven printed dashes and 30
lost-tail coordinates remain unknown. All 144 observed coordinates remain
byte-for-byte unchanged.

## What the prior translation supports

[Lasry, Niebel, Kopal and Wacker, Table 3, row 13](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf#page=21)
does not print a reconstructed German body for this part. Its English column
supplies a partial historical translation attributed to Childs. That topic
guided selection of the route vocabulary tested here. It is **not an
independent coordinate witness or a full German plaintext source**.

This route layer does not import the translation's army designation or approval statement.
The surviving three-position field before `ARMEE` is left as `???`:

| Plaintext index | Surviving pair | Literal label domain |
| ---: | --- | --- |
| 10 | `?F` | `1GHLWZ` |
| 11 | `??` | All 36 labels |
| 12 | `D?` | `CRSVXZ` |

The directly decoded numeral **1 at position 103** stays in the footer.
No historical unit number or abbreviated office is inferred from it.

## Bounded placement check

The verifier places each of the five chosen spans at every possible offset
in the unchanged 111-position model: **503 comparisons** in total. Each
chosen span has a unique zero-observed-substitution placement, respectively
0, 13, 18, 38 and 54. All other starts and their exact costs are retained.

This comparison is conditioned on those particular word choices and the
existing frame. It does not compare every possible German alternative, and
it is not a blind test: the words were chosen after the historical translation
and raw domains were read. An exact low-cost fit cannot independently
authenticate missing letters, original spelling or the historical event.

**Further reading.** The [approval-request extension](APPROVAL.md) adds 15
conditional letters to this route layer, reaching 90/111 positions with no
observed-coordinate changes; two of those letters are wholly missing.

**Optional footer fields.** The [footer extension](FOOTER.md) adds seven
half-supported labels through overlapping original fields, reaching 97/111.
A separate historical-closing proposal reaches 101/111; all eleven new
labels retain an observed half and change no observation. Exact prices and
the unfilled intervening fields remain in its [certificate](footer_extension.json).

## Reproduce and preserve the primary edition

[Inputs](inputs.json) pin the original record, the unchanged published key,
the existing source image and all primary case display hashes. The
[verifier](verify.py) recomputes both frame readings, every fill, all 37
half-pair constraints, all 36 unresolved domains and the 503 placement costs.
It also checks that the original case headings and every fenced and quoted
display remain unchanged. Its arbitrary complete roundtrip witnesses are
mathematical validation examples, not historical plaintext.

```sh
python experiments/p116_optional_route_fragment/verify.py --verify
python experiments/p116_optional_route_fragment/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

The optional PDF check recreates the existing p116 image and compares pixels.
The default verification uses only the standard library and repository data.
No new image asset or newly counted physical record is added.

The source remains J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed p116](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The report's historical decipherment belongs to **J. Rives Childs**. The
published keys and later report reconstruction retain the credit of
**George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**,
[2016, DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461).
This supplement is an explicitly priced source-based proposal, with no
claim to first decipher the already known report.
