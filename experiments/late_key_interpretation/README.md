# Propagating late-period numeral interpretations

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The source-reviewed [p217 and p230 operational reports](../operational_recovery/README.md)
support optional, globally consistent interpretations of several labels in
the published late-period squares. This small certificate applies exactly
those hypotheses to four other source records. It adds no ciphertext edit
and does not replace the baseline keys.

## Why the printed square labels require care

Lasry, Niebel, Kopal and Wacker explain in [section 5.4 of their author
manuscript](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf)
that their algorithm does not determine the positions of the ten digits;
identifying unit numbers requires additional traffic or historical evidence.
The four keys covering 19 November to early December are not supplied by
Childs's historical key table. A complete 36-character algorithmic square
therefore does not authenticate every numeral label.

The present optional layers clear the stated potentially arbitrary labels
before assigning selected cells. Ordinary letters kept as anchors, the
precise cleared-label set, the unit identifications and the weaker lexical
assumptions are all listed in the operational package. In particular, the
French contemporary source itself queries the 89th Division: the Nov28
`5→9` identification retains that extra uncertainty.

## Results outside the reports used to propose the maps

| Record | Baseline field | Conditional interpretation | Additional source decisions here |
| --- | --- | --- | --- |
| Challenge p215 | Closing `3Y52` | `?1?6` under Nov22 `Y→1`, `J→2`, `2→6` | None; Norbert's two inserted groups remain unknown |
| p214 B | `AOKYY` | `AOK11` under the same Nov22 map | None; the rest of the closing reference stays damaged |
| p227 B | `XXYARMEE` | `11XARMEE` under Nov28's numeric map plus the separator convention | None for the number; the earlier one-coordinate `UNTERSTELLTE` repair is separately retained |
| p226 B2 | Damaged numerical examples | Still damaged after applying every declared Nov28 layer | None; the missing first part and three example digits remain unresolved |

These are consequences of the stated maps, not independent proofs that the
maps are historically correct. The p214 army-headquarters field and p227
army field are consistent checks outside the messages used to propose them.

### p215's reference remains a coupled field

The four ending coordinate pairs are all observed under Norbert's unchanged
geometry. The inferred ending is **`a1b6`**, where `a` and `b` are different
members of **`0345789JQY`**. The same square cell must keep one value throughout
the message. There are exactly **90** possible ending fields under this
partial interpretation, and the verifier constructs a full source-preserving
square/erasure witness for each one.

If the entire field is additionally assumed to be numerical, **42** values
remain, allowing a leading zero. That assumption is not established by the
cipher. No particular serial or reference number is selected. The original
21 unknown coordinates, the conditional two-gap geometry and the earlier
editorial body repairs remain unresolved in precisely their original form.

### The p227 routing instruction

With the separate numeral and separator hypotheses and the already
published one-coordinate ordinary-word repair, the complete readable body is:

```text
BITTEFUNKSPRUECHEAN11XARMEEUNDUNTERSTELLTEFORMATIONENUNMITTELBARANZOENGEBENX
```

Meaning: send telegrams for the 11th Army and its subordinate formations
directly to ZOEN. The digit interpretation and the ordinary-word correction
have different evidence and can be assessed separately.

### A numerical-code rule is still not recoverable

Applying the same assignments to p226 B2 does not make its example coherent.
After its two earlier ordinary-word repairs, the middle still includes
`SODASS1X1SZAHLEN?X9X?X19X1?XUXSXW`. Those garbles are retained rather than
being used to invent further key labels or a complete numerical-code rule.

## Reproduce

```sh
python experiments/late_key_interpretation/verify.py --verify
```

The standard-library verifier checks the frozen dependency hashes, constructs
the inverse column geometry independently, compares every partial-square
domain with the project reader, and re-encrypts a globally consistent witness
for every displayed layer. It also checks all 90 ending fields for p215 and
the exact earlier source edits for p226/p227. Arbitrary witness completions
are marked as consistency examples, never proposed historical plaintexts.

The [certificate](certificate.json) preserves the baseline output alongside
every optional reading and the source indices of the propagated assignments.
The original transcripts, keys and earlier interpretation certificates remain
unchanged.
