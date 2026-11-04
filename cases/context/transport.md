# Transport traffic — p185/p189 and parallel messages

These transport messages concern trucks, a request for vehicles and trailers, readiness to depart, and orders to wait. Their partial readings keep the damaged destinations and equipment designations visible.

**Complete edition by printed page:** [p. 185](../pages/185.md) · [p. 189](../pages/189.md) · [p. 193](../pages/193.md) · [p. 194](../pages/194.md) · [p. 196](../pages/196.md) · [p. 197](../pages/197.md) · [p. 198](../pages/198.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Case index](../README.md) · [ADFGVX Cipher](../../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Status: source-preserving partial reading under a plausible, unproved gap geometry.** This supplementary **p185 D** intercept is outside the 22-message challenge. Its header reads `CM v CZ (20.15 p.m., November 13th), 21.00, RIZI-198`, but the body contains 193 slots: 192 valid ADFGVX coordinates and one literal `Y`. The raw `Y` is retained in the source layer and treated as one unknown coordinate in analysis.

**Current transcription, comparison and verification:** icekylinx and GPT-6 Astra Pro. Historical keys and source witnesses retain the provenance recorded in the certificate.

## Most likely readings

| Record | Readable German text | Meaning and uncertainty |
|---|---|---|
| p185 D, conditional word completion | […] marschiert Lastautos morgen 1500 ueber DHFN. Abmarschbereit sein. […] Seifert. | The reconstructed clause concerns trucks moving tomorrow via `DHFN` and orders readiness to depart. Three coordinate substitutions and three fills complete the words; the opening and closing instruction remain damaged. |
| p193 E | Kleiner Federwagen zu[m] Anhaengen hier. Kommt Auto. | A small sprung cart for attachment is available; the message mentions a car. Punctuation and the `M` are editorial. |
| p194 A / p196 B composite | Abtransport in verabredeter Weise Freitag DHFN 1?00. Wagen bereithalten. Marschziel Hanau. Seifert. | Departure as arranged on Friday; keep vehicles ready; Hanau is the destination. Every selected coordinate is attested in one of the two witnesses, but one time digit remains unknown. |
| p197 E / p198 C | Lastauto 1?00 abgefahren. Ich bleibe mit ? Mann bis Sonntag. Alles Gute, auf Wiedersehen. [Seifert]. Gruss Bocho. | The truck has departed; the sender remains with an unknown number of men until Sunday. The signature is normalized editorially; neither witness spells it exactly this way. |
| p189 E, conditional shared digit | Ja, Hebepumpe aus Blech. Kommen 2 Autos. Hier 2 Anhaenger. | Two vehicles and two trailers; VG=2 and one invalid-coordinate fill complete the short message. |

Brackets mark editorial interpretations; `?` retains an unresolved character. `DHFN`, `STATMET` and `BOCHO` are not expanded or geographically identified. The exact readings and witness disagreements follow below.

### Two vehicles and two trailers — p189 E

**Readable German — conditional shared VG=2, with one invalid-coordinate fill:**

> Ja, Hebepumpe aus Blech. Kommen 2 Autos. Hier 2 Anhaenger.

The [award-class interpretation](../../experiments/nov13_joint_completion/README.md#the-award-class)
supplies **VG=2** to both count fields, at plaintext positions **26 and 37**.
The word `ANH?ENGER` has the partial pair `V?`, with the invalid printed `B`
at source position **81**. Filling it as **V** gives `ANHAENGER`. This takes
the native 94-slot message from **44 to 47/47** fixed positions: two digits
from the shared square and one ordinary-word fill, with **no observed-coordinate
substitution**. The source's `B` remains visible in the literal transcription.
Indices are zero-based. [Exact completion and source mapping](../../experiments/nov13_joint_completion/transport_certificate.json).

## p185 D source and gap model

![Literal p185 D source excerpt](../../sources/excerpts/childs_p185_D.png)

We enumerated all 194 possible positions for a contiguous block of five missing coordinates under the audited November 13–15b key. Every valid received coordinate remains unchanged and in its original order. No missing coordinate or unknown square cell is filled.

## Conditional result

Inserting five erasures before source index **55**, a printed group boundary, gives this exact partial plaintext:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional five-coordinate gap before source index 55:**

```text
STATMETXMARSCHIERTLCST?UT?SMORGEN1500UEBERDHFNXAB?A6SCHBE?EITSEIN?VS6GROV?AN?IERE?XBITTEF6EXSEIFERT
```

</details>

Under this geometry, **91 of 99 characters are fixed**. The eight unresolved positions consist of six positions touched by uncertain coordinates and two positions using unassigned square cells. The fixed portions include `MARSCHIERT`, `MORGEN1500UEBERDHFN`, and `SEIFERT`; malformed portions are retained literally. `DHFN` and `STATMET` are not expanded into place or station names.

This is a conditional result. The strongest composite language score selects position 55, but a conventional plaintext quadgram score selects position 57:

| Gap before source index | Composite ranking score | Plaintext quadgram mean |
|---:|---:|---:|
| 55 | 24.910328 | -6.041730 |
| 56 | 22.691041 | -6.070230 |
| 57 | 22.641029 | -5.987314 |

These are heuristic scores, not confidence probabilities. All 194 positions are arithmetically compatible with the received symbols. Positions 159 and 160 produce the same masked ciphertext because the inserted gap can exchange places with the existing unknown `Y` slot. There are 193 distinct masked ciphertexts. No plaintext character is fixed across all 194 geometries. The three leading composite-score candidates share 89 fixed characters, but that selected subset is not a confidence set.

### Truck movement and readiness

The [word-completion certificate](../../experiments/p185_readiness_completion/README.md)
restores the vehicle noun and readiness instruction within the existing gap-55
frame:

**Readable German — conditional excerpt; the ellipses omit the damaged opening and closing instruction:**

> […] marschiert Lastautos morgen 1500 ueber DHFN. Abmarschbereit sein. […] Seifert.

The wording concerns trucks moving the following day via `DHFN` and instructs
the recipient to be ready to depart. `STATMET`, the transmitted `1500` and the
closing command remain unexpanded in the exact text. The unusual word order
is preserved.

`LCST?UT?S → LASTAUTOS` costs two observed-coordinate substitutions and a fill
of the printed `Y`. `AB?A6SCHBE?EITSEIN → ABMARSCHBEREITSEIN` costs one
substitution and two fills inside the five-coordinate gap. The edition fixes
**95/99 positions**, up from 91; three inserted coordinates remain unknown.
The same conversation has native `LASTAUTO` in p198 C, `ABMARSCH` in p193 C
and `BEREIT` in p196 B. These support the vocabulary without establishing an
identical sentence in another reception.

<details>
<summary>Exact conditional word completion</summary>

**Edited output — gap 55, three observed-coordinate substitutions, one printed-glyph fill and two missing-slot fills:**

```text
STATMETXMARSCHIERTLASTAUTOSMORGEN1500UEBERDHFNXABMARSCHBEREITSEIN?VS6GROV?AN?IERE?XBITTEF6EXSEIFERT
```

</details>

A separate lexical check masks the numerical field, opening designation and
closing instruction. Among all 194 gap positions, **52–55** tie at the minimum
of three observed substitutions. The readable clause therefore remains
conditional on the retained gap-55 frame; the word repairs do not prove its
geometry.

```sh
python experiments/p185_readiness_completion/verify.py --verify
```

## Independent transport context

Six additional source-checked intercepts decrypt directly with the same historical key. They retain every literal garble and unresolved square cell:

- **p193 E, November 14:** `KLEINERFEDERWAGENZU?ANHAENGENHIERXKOMMTAUTOX`
- **p194 A, November 14, header `CM v CZ`:** `ABTRANSPORTINVERABREDETERWEISEFREITCGDHFN1?00XWAGENBERE?THALTENXMARSCHZIELHANAUXSEIFERT`
- **p196 B, November 15, header `CM v CZ`:** `ABTRANSPORTINVERABREDETERWEISEFREITAGDHFN1?00XWAGENBEREITHALTENXMARSCHZIELHANAUXSEI?ERT`
- **p197 E, November 15, header `CM v CZ`:** `LASTAUTO1?00A?GEFAHRENXICHBLEIBEMIT?MANNBISSOHNTAGXALLESGUTEAUFWIEDERSEHENXSE?FERTXGRUSSBOCHO`
- **p198 C, November 15, header `CM v CZ`:** `LASTAUTO1?00ABGEFAHRENXICHBLEIBEMIT?MANNBISSONNTAGXALLESGUTEAUFWIEDERSEHENXSEHFERTXGRUSSBOCHO`
- **p189 E, November 15, header `CZ v CM`:** `JAHEBEPUMPEAUSBLECHXKOMMEN?AUTOSXHIER?ANH?ENGER`. This is a different intercept from the p189 challenge target.

The p194/p196 pair repeats `DHFN` and names `HANAU` as the march destination. It has 171 of 174 raw coordinates in common; disagreements are at indices 82 (`K/X`), 167 (`X/V`), and 173 (`D/G`). The p197/p198 pair agrees at 183 of 186 coordinates, differing at indices 59 (`V/A`), 63 (`A/V`), and 67 (`G/A`). Neither lorry-message copy supplies an exact `SEIFERT` signature; `SEHFERT` is not silently corrected.

For the transport-order pair, a separately labelled source-supported composite takes `X` at index 82 and `V` at index 167 from p196 while retaining p194's `D` at index 173. It reads:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional source-supported composite of the p194 and p196 witnesses:**

```text
ABTRANSPORTINVERABREDETERWEISEFREITAGDHFN1?00XWAGENBEREITHALTENXMARSCHZIELHANAUXSEIFERT
```

</details>

This composite fixes 86 of 87 characters. It makes an editorial choice
between disagreeing source witnesses, with every chosen value attested in
at least one. The certificate retains all four combinations of the two
disagreements between valid coordinates. The planned-time cell `FV`
remains unassigned.

Under the separate shared VG=2 interpretation, the reported-hour cell
`AF` cannot also be 2. If the departure occurred on the report's date
before its `13.45` origin time, `1?00` therefore becomes **13:00**. That
chronological assumption is kept separate from the source-supported
composite. The [linked-field comparison](transport_197_198.md#linked-number-fields)
also shows why this reading cannot be combined with the earlier extra
assumption that the reported departure was no earlier than the planned one.

The [certificate](../../data/certificates/p185_D_transport.json) contains every gap geometry, its full plaintext domains, exact source-to-plaintext mapping, all six direct context readings, both near-parallel comparisons, and the conditional composite. The [standalone verifier](../../adfgvx/transport.py) recomputes all 194 constraint sets and exact coordinate roundtrips without a language model. It checks the consistency of the stored ranking order but does not recompute the heuristic scores. The [portable ranking script](../../experiments/known_key/README.md) reproduces both complete rankings from a pinned upstream model; every stored score matched exactly in the recorded environment.

```sh
python3 -m adfgvx.transport
```

This analysis does not fully solve p189 and does not add a solved item to the 22-message total.

Four [additional p197/p198 witnesses](transport_197_198.md) now connect the
conversation with equipment for Darmstadt, a lorry, a trailer and a petrol
pump. Their duplicate-group and missing-coordinate hypotheses have separate
source and arithmetic certificates.

Source images: [p189](../../sources/excerpts/childs_p189_context.png), [p193](../../sources/excerpts/childs_p193_context.png), [p194](../../sources/excerpts/childs_p194_context.png), [p196](../../sources/excerpts/childs_p196_context.png), [p197](../../sources/excerpts/childs_p197_context.png), [p198](../../sources/excerpts/childs_p198_context.png). Header order is `recipient v sender`; see [source conventions](../../sources/README.md).

</details>
<!-- CASE-EDITION:END -->
