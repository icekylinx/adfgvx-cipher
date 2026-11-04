# A parallel car enquiry with an explicit extra-coordinate model

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

The p183 D source is almost identical to the independently readable car enquiry in p183 E, but it has an extra observed coordinate and one other disagreement. This edition preserves D's native odd-length diagnostic and separately prices a parallel-copy proposal. The wording was already obtained directly from E; D adds another physical witness with explicit limitations.

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed D/E image](../../experiments/car_query_parallel_frame/sources/p183_D_E.png) · [Inputs](../../experiments/car_query_parallel_frame/inputs.json) · [All position and exclusion certificates](../../experiments/car_query_parallel_frame/certificates.json) · [Native E edition](nov12_arrival_departure_and_car.md#p183-e)

## The three lengths remain distinct

| Evidence layer | Coordinate slots | Treatment |
| --- | ---: | --- |
| D's printed RIZI header | 27 | Retained literally as printed |
| D's actually occupied source body | 37 | Every observed coordinate retained in the native diagnostic |
| E's native body | 36 | Directly decodes the complete car enquiry |
| Conditional D comparison model | 36 | Excludes one observed final X; not a free erasure fill |

D's literal header is `D) CZ v CM (17.20 p.m., November 12th); 12.40; RIZI-27`.

<details>
<summary>Literal source transcription</summary>

**Source transcription — the complete 37-coordinate printed body:**

```text
AAXDF AVDFA AADAG FVVAG DDAGV DDVFF VGDVG DX
```

</details>

The following `CM UM` is printed transmission control outside that body. D and E retain their different routing directions and time expressions. No unrecorded historical retransmission or cancellation is asserted.

## Raw output — all 37 observed coordinates retained

Undoing the published Nov10–12 transposition gives 18 complete pairs and one unpaired coordinate. The complete-pair diagnostic is:

<details>
<summary>Raw decoded text</summary>

**Raw output — complete pairs of the unchanged 37-coordinate source; the unpaired coordinate is recorded separately:**

```text
AUPOXKRAMMTGIUTRF?
```

</details>

The unpaired coordinate is **V at native source index 6**, occupying intermediate index 36. It is retained explicitly in the certificate. It is not the final printed X later excluded in the comparison model. The final question mark in this diagnostic comes from an unassigned square cell, not from a missing printed glyph.

## Raw output — conditional 36-coordinate comparison frame

The native E source supplies the independently fixed target `WOBLEIBTAUTOXKRAMM`. Against that target, excluding each of D's 37 observed positions in turn gives a unique lowest substitution cost when excluding **final source index 36, X**. In that frame, before any coordinate substitution, D reads:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional 36-coordinate frame excluding observed source 36 (X):**

```text
WOBLEIBTAUTODKRAMM
```

</details>

The exclusion is a hypothesis based on the parallel source. The printed X is not visually canceled, and its exclusion is not justified merely by the existence of an odd count or by the printed 27 header.

## Edited output — one observed-coordinate exclusion and one substitution

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — conditional exclusion of observed source 36 (X) and substitution at retained source 3 (D→X):**

```text
WOBLEIBTAUTOXKRAMM
```

</details>

**Readable German — exact nonseparator labels of the conditional edited output:**

> Wo bleibt Auto. KRAMM.

**Meaning:** The conditional reading asks where the car is or why it has not arrived. KRAMM remains a literal closing label. The text is an enquiry, not proof that a car was dispatched. The question uses a period in the exact reading so that `?` remains reserved for an unresolved plaintext position.

| Model | Observed-coordinate exclusions | Further observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: |
| Native E source | 0 | 0 | 0 |
| D: exclude final source 36 | 1 | 1 | 0 |
| D: exclude source 35 | 1 | 2 | 0 |
| D: exclude source 34 | 1 | 3 | 0 |

All **37** exclusion positions, their retained-source maps, raw results and exact substitution vectors are in the certificate. The unique minimum is relative to this fixed E target and the single-exclusion model; it does not prove the historical cause of D's discrepancy. The fully observed E witness is evidence and is not counted again as a new record in this package.

## Evidence, credit and reproduction

The unchanged period key retains the credit to George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry's 2017 key list. The directly readable E witness is frozen separately in [native_witness.json](../../experiments/car_query_parallel_frame/native_witness.json), with its earlier artifact hash and edition credit. This package adds a literal D transcription, the unpaired-coordinate provenance, and a completely priced parallel-source model. No first historical decipherment is claimed.

The verifier independently reconstructs the native odd-length column map, checks the project decoder, exhausts every one-coordinate exclusion, replays all proposed changes and verifies a globally injective full-square completion. It binds the D/E crop to the original PDF by file hash, page, rectangle, scale and exact pixels.

```sh
python experiments/car_query_parallel_frame/verify.py --verify
python experiments/car_query_parallel_frame/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```
