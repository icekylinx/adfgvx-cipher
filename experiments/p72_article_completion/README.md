# p72 A1: a conditional article before the literal K.M.

**Source comparison and verification: icekylinx and GPT-6 Astra Pro.**

The source-reviewed first part of the [Kress delegation report](../../cases/caucasus/october_caucasus.md)
ends `OHNEBETEILIGUNGX?SKXMXANGEORDNET`. Interpreting its `X?S` as **DES**
gives the ordinary construction “ohne Beteiligung des K.M. angeordnet”.
This is a grammatical proposal with a small, explicit coordinate cost;
`K.M.` remains an unidentified abbreviation.

| Plaintext index | Existing evidence | Proposed letter | Additional source operation |
|---:|---|---|---|
| 72 | `GD` gives X | D, encoded `GG` | source 136: D → G |
| 73 | `F?` gives domain `1EKLOS` | E, encoded `FA` | source 185: invalid U → A |

The first operation changes one observed coordinate; the second fills one
non-coordinate glyph. No visual correction is claimed: the source still
reads D and U at those positions. The earlier `VERSTAER1UNG` →
`VERSTAERKUNG` word repair is retained at source 125 F → V.

The original has 203 literal positions, including the source-instructed
25-coordinate strikeout. The resulting 178-slot frame fixes **88/89** raw
labels. Its earlier edited layer also fixes 88/89, at one observed
substitution. The proposed complete layer reaches **89/89**, at **two
observed substitutions and one invalid-glyph fill in total**. The source
strikeout, published Oct4–6 key and all numeric fields remain unchanged.
No physical record is added and no historical completion is claimed for
the separate second-part references.

## Finite ambiguity comparison

The verifier compares all 36 possible labels at position 72 with all six
source-compatible labels at position 73. Every one of the resulting 216
complete first-part strings is re-enciphered exactly. Relative to the
existing word repair:

| Additional observed substitutions | Number of candidates | Additional invalid-glyph fills |
|---:|---:|---:|
| 0 | 6 | 1 |
| 1 | 60 | 1 |
| 2 | 150 | 1 |

`DE` is one of the 60 one-substitution candidates. The choice comes from
its grammatical fit before `K.M.`, not cryptographic uniqueness. All
candidate pairs, operations and costs remain in the certificate; the
other alternatives are not silently discarded. Neither an expansion of
`K.M.` nor an identity for `NATEKS` is part of this completion.

## Reproduce

```sh
python experiments/p72_article_completion/verify.py --verify
python experiments/p72_article_completion/verify.py --verify --pdf /path/to/childs_original.pdf
```

The package binds the existing October Caucasus inputs and certificate,
reconstructs the original source map, compares two decoding implementations,
prices each new operation, and verifies the exact conditional forward
witness and case display. Optional PDF checking reproduces the existing
p72 source crop. The original package's source inputs and certificate are
unchanged. Earlier source and key credits are preserved; no first historical
decipherment claim is made.
