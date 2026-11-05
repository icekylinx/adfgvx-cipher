# ADFGVX Cipher: new transport parallels on pages 197–198

**Source review and certificates: icekylinx and GPT-6 Astra Pro (2026).**
The cipher key is the previously published **Nov13–15b** key; its historical and modern attribution is retained in the certificate. This review adds source linkage, literal transcription, explicit geometry hypotheses, and an independently checked account of every uncertainty.

Two pairs of printed messages support useful new contextual readings. **They do not solve the separate p198 section D / `CHI-170` target.**

| Pair | Most likely subject | Evidence status |
| --- | --- | --- |
| p197 C / p198 B | Two `US` apparatuses to Darmstadt; station to remain ready; signed Seifert | Source-supported composite, with an unresolved designation and time/date; one letter needs an erasure fill and an additional known-coordinate change across the witnesses |
| p197 D / p198 E | A lorry is coming; load a trailer; prepare a petrol pump | Clear shared body after a literal duplicate-group repair and a conditional dash relocation; three letter positions need additional editorial emendation |

## 1. Equipment for Darmstadt

### Most likely reading

```text
NACHRCHEFXEINHAFENXZWEIUSGERAETENACHDARMSTADTVERLADENX
STATIONBLEIBTBIS16X0???BETRBEREITXSEIFERT
```

**German:** “Nachr.-Chef. [EINHAFEN: unclear designation]. Zwei US-Geräte nach Darmstadt verladen. Station bleibt bis [16X0???] betr.-bereit. Seifert.”

**English:** “Chief of signals. [EINHAFEN: unclear designation]. Load two US apparatuses for Darmstadt. The station remains operational until [16X0???]. Seifert.”

`NACHRCHEF` and `BETRBEREIT` are read as abbreviations for *Nachrichtenchef* and *betriebsbereit*. The expansions are editorial. `EINHAFEN` is the letter sequence supported by the combined witnesses; no place identification is established. `US` remains unexpanded. The time/date is not silently changed to 16:00.

### Printed source lengths and coordinate gaps

<a id="what-the-source-preserves"></a>

| Source | Printed label | Slots | Valid coordinates | Other slots |
| --- | ---: | ---: | ---: | --- |
| p197 C | `RIZI-190` | 185 | 178 | Six dashes and one literal `C` |
| p198 B | `RIZI-190` | 190 | 190 | None |

The raw p197 C reading is odd-length and cannot produce a complete paired-coordinate plaintext without a length hypothesis. Insert five unknown slots at each of its **186 boundaries** and compare it with p198 B. Positions **64 and 65** minimize known-coordinate disagreement, both with **18 disagreements**. Indices are zero-based. The two placements produce the **same masked ciphertext**, because the intervening source slot is the invalid `C`, also analyzed as one unknown slot. Both source maps are retained.

Under either geometry, p197 C gives:

```text
NAC?RCHEFXE?NHAFENXZWEIUSGERAETENACH?ARMSTAI??ERLAD?N?
STATION?L?IBTB??16X0?05?ETRBTRI?TXSEIF?R1
```

The complete literal p198 B gives:

```text
?ACHJCHEFXEI?HAFZNXZWEIUSGERAETENACHDA6MSKADTVERLCD?NX
STAKIONBLEIBTBIS16X0?XFBETR?EREITXSEIFEDT
```

Of the preferred reading's **92 specified characters**, **91** have their complete coordinate pair printed in at least one aligned witness. The remaining `E` in `VERLADEN`, plaintext position **51**, needs an erasure fill. It also costs **one known-coordinate change above the minimum across the two witnesses**. Thus “observed somewhere” does not mean that one clean witness contains the complete preferred reading.

## 2. Lorry, trailer, and petrol pump

### Most likely reading

```text
ESKOMMTEIN?TONNENAUTOXNURBESTENANHAENGERBELADENX
BENZINPUMPEBEREITHALTEN
```

**German:** “Es kommt ein [?]-Tonnen-Auto. Nur besten Anhänger beladen. Benzinpumpe bereithalten.”

**English:** “An [?]-ton lorry is coming. Load only the best trailer. Have the petrol pump ready.”

The tonnage remains unresolved. This review does not assign a digit to an unfilled square cell.

### Explicit geometry hypotheses

p198 E advertises **142** coordinates but prints **147** slots, including an invalid `K`. Its fourth and fifth groups are identical: `XAXVV XAXVV`. Deleting either identical copy produces the **same 142-slot stream**, preserves **141 valid coordinates**, and changes no surviving coordinate. The corresponding p197 D source has only one copy of `XAXVV`.

That repair alone gives:

```text
ESKOMMTEIN?TONNENAMTOXNURBEST5NANH?GNGERB?LADENX
BENEINPUMPEBEREITHALTEN
```

The literal p197 D has **142 slots**, one of which is a dash at source position **89**. Keeping every valid coordinate in its original order, remove only that dash slot and try reinserting it at all **142 boundaries**. Positions **74 and 75** tie at **eight known-coordinate disagreements** with repaired p198 E. Both alignments remain in the certificate; unlike the C-pair tie, they produce different masked readings.

Position 75 gives:

```text
ESKOMMTEIN?TONNENAUTOXNURBESTENANHLGNGERHC?ADENX
BCN?INPUMPEBEREITHALTEN
```

The preferred body has **70 specified characters out of 71**: **66 complete observed-pair supports**, **one pair assembled from observed halves**, and **three letter positions requiring an unattested coordinate emendation**. Those positions are **34 (`A`), 35 (`E`), and 51 (`Z`)**, zero-based. This is an editorial reading of the two sources, with its extra assumptions exposed.

## 3. Coordinate cost across both witnesses

Each altered valid coordinate is counted separately in its own witness. Unknown-slot fills, deleting the five-coordinate duplicate, and the stated dash/length geometry changes are tracked separately.

| Pair | Attainable minimum known-coordinate cost | Minimum cost with the preferred specified letters | Preferred specified-letter cost by witness |
| --- | ---: | ---: | --- |
| p197 C / p198 B | 18 | 19 | 6 in C and 11 in B, plus 2 at unresolved positions |
| p197 D / p198 E | 8 | 13 | 8 in D and 5 in E |

The certificate supplies every position's minimum-cost character domain, the preferred reading's cost, and explicit ciphertext witnesses attaining both totals. A minimum edit total is a geometric constraint, not a probability that a reading is historically correct.

## Linked fields and terminology

The [case page](../../cases/pages/197.md#edition-cases-context-transport-197-198) adds a primary-source
terminology note for `US` apparatuses and explains the shared unresolved number
fields. The lorry tonnage and planned departure hour use `FV`; the reported
departure hour uses `AF`, so they cannot be silently given the same digit.
The [linked-field certificate](linked_fields.json) separates this exact identity
from three conditional semantic scenarios. No digit is added to the historical
square.

```sh
python3 experiments/transport_followup/analyze_linked_fields.py --verify
```

## 4. Reproduce and inspect

From the repository root:

```bash
python experiments/transport_followup/build_transport_families.py
python experiments/transport_followup/verify_transport_families.py
```

The standalone verifier imports no repository cipher routines. It independently reconstructs every raw or modeled even-length text, its partial-square domains, the exact source maps, every alignment distance, all reported letter-support categories, and the attainable coordinate-cost witnesses.

- [Literal transcriptions](transport_sources.json)
- [Full certificate](../../data/certificates/p197_p198_transport.json)
- [Independent verification result](../../data/reviews/p197_p198_transport_independent.json)
- [p197 C and D source crop](../../sources/excerpts/childs_p197_CD.png)
- [p198 B source crop](../../sources/excerpts/childs_p198_B.png)
- [p198 E source crop](../../sources/excerpts/childs_p198_E.png)

These are unaltered crops of J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed pages 197–198, PDF pages 200–201 in the [source scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view). The callsigns and times remain literal even where they appear irregular. The first callsign of p197 D is read as `OM`, with the imperfect first glyph documented. Rendering commands and crop hashes are in [source_crops.json](source_crops.json).
