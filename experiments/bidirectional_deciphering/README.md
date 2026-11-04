# An instruction to decipher from opposite ends

Prepared by **icekylinx and GPT-6 Astra Pro**. The new
[p138 B source edition](../../cases/pages/138.md#edition-cases-radio-opposite-end-deciphering)
reads, conditionally: **“Erste Hälfte von vorne, zweite Hälfte von hinten
lösen.”** Two equally priced variants share that instructional body and
differ in the internal closing, `NKJ` or `NMJ`. The separate printed
`NKJ 472` footer favors `NKJ`, without proving a unique extra-coordinate
position.

This package contains one new physical source record, a reproducible
8,892-candidate stage comparison, and a limited 78-split comparison with
the already reviewed p132 B. It does not add p132 B again to the catalog or
alter that earlier source package.

## Source result and exact costs

- Printed/source length: **105 slots**, including one invalid `R` glyph.
- Working cipher: **104 coordinates**, using the unchanged published
  `Nov4-6` key, with one received coordinate conditionally extraneous.
- Conditional raw reading: **51/52 labels fixed**.
- Each accepted variant: **2 known-coordinate substitutions, 1 invalid-glyph
  fill, 1 separately charged extraneous transmitted coordinate**.
- All 105 received slots are retained in the full forward witness. The same
  repaired witness supports both variants.

The original 105-slot raw reading, its unpaired coordinate, and both complete
52-character proposals remain in `certificates.json`. The source's advertised
105 length is not silently replaced by 104. Its page heading says November 6,
while its reception line says 00.15 November 5; both dates remain literal.

The preferred variant excludes final received `X` at zero-based index 104.
The alternative excludes preceding `F` at index 103. Both require received
substitutions **76 V→F** and **94 A→F**, plus the printed-`R` fill **8 ?→F**.
Both produce the same instructional body. Only the retrospective template
that already fixes the closing to `NKJ` has a unique minimum at 104; no
unconditional uniqueness claim is made.

## Completed phase comparison

| Stage | Operation | Geometric locations | Completed candidate records |
| --- | --- | ---: | ---: |
| Received/transmitted stream | Insert one coordinate | 106 | 3816 |
| Received/transmitted stream | Remove one extra coordinate | 105 | 630 |
| Intermediate stream after untransposition | Insert one coordinate | 106 | 3816 |
| Intermediate stream after untransposition | Remove one extra coordinate | 105 | 630 |
| Total | | 422 | 8892 |

Each inserted coordinate and the one printed erasure range over all six
values. When the erased source slot itself is removed, repeated fill-value
records remain present. The counts are **actual completed candidate records**,
not distinct strings or a global search bound. Two unchanged frozen
37-symbol quad objectives produced **17,784 score evaluations**. Both tied
the raw `NMJ` and `NKJ` endings at the top; the source footer supplies a
separate reason to prefer `NKJ`.

The exact original driver, its source transcription and every original
result are preserved in `search/`, with hashes in `inputs.json`. The original
driver contains the original scratch paths. The portable `phase_audit.py`
uses the bundled inputs and independent verifier implementation instead;
it checks every original string and stage witness. Optional pinned model
paths recompute every score. Earlier poor intermediate-stage candidates
remain in the original archive.

## Limited p132 comparison

The p138 header `SSD ZU 14.10 (5)` refers to the same internal time/day as
p132 B's `SSD EILT SOFORT LOESEN 1410 (5)`. Both have the route `LP v NKJ`;
the same direction must not be presented as a reversed reply. The match
supports a related instruction, with the unresolved p138 date contradiction
retained.

`search/header_inventory.json` preserves all 622 available OCR-header rows
and the three matching `1410` records. Only p132 and p138 use day `(5)`;
the third, p177, has `(11/11)`. The full original OCR-screen hash is pinned,
and an optional CLI argument can check those extracted headers against its
original bytes. This is a finite source inventory, not universal historical
uniqueness.

For a defined interpretation of opposite-end deciphering, `verify.py` keeps
the p132 155-slot untransposition unchanged, forms its forward pair phase
and backward pair phase, and tries all 78 joins. Joining 27 leading and 50
trailing labels, or 28 leading and 49 trailing labels, gives the prior
conditional raw reading at three substitutions and two source fills.
It leaves an unpaired V at index 54 or 56, within the old four-identical-V
ambiguity at indices 54–57.

Literal balanced 38/39 and 39/38 splits need **20 and 22 substitutions**
for that prior proposal. Flexible opposite-end pairing is the existing
one-extra-intermediate-coordinate hypothesis in another form; it does not
reduce the number of assumptions or establish that the instruction used
this exact procedure. The comparison uses frozen snapshots of the earlier
p132 inputs and certificate. No model is trained or tuned, no prior source
bytes change, and no unrelated challenge status changes.

## Reproduce

Both default checks use the Python standard library:

```sh
python experiments/bidirectional_deciphering/verify.py --verify
python experiments/bidirectional_deciphering/phase_audit.py --verify
```

The first reconstructs the independent source witnesses, both equally
priced variants, all 105 fixed-template removal prices and all 78 p132
joins. The second rebuilds all 8,892 original phase candidates and the
bounded header inventory. Without model paths it does not recompute the
language scores; it verifies their archived candidates and preserved ties.

To recompute scores and, optionally, write a fresh portable replay:

```sh
python experiments/bidirectional_deciphering/phase_audit.py --verify \
  --book-model /path/to/german_military37_quad_marginal.bin \
  --radio-model /path/to/radio_book37_quad_marginal.bin \
  --original-ocr-screen /path/to/corpus-harvest-screen-initial.json \
  --output /tmp/p138-phase-replay.json
```

Both models are mandatory only when writing a replay. Their hashes must
match the original archive. The original result cannot be overwritten.
The full portable replay completed and every score matched the original
on the execution environment; recomputation accepts only a `1e-12` floating
point summation tolerance. Candidate strings, counts, coordinates and
source hashes remain exact.

Optional PDF regeneration requires PyMuPDF:

```sh
python experiments/bidirectional_deciphering/verify.py --verify \
  --pdf /path/to/adfgvx-childs.pdf
```

PDF SHA-256:
`157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.
The full p138 page, p138 B detail and p132 B detail have fixed PDF rectangles,
scales, PNG hashes and raw-pixel hashes. The source verifier and full PDF
regeneration passed. Printed pp132/138 are PDF pp135/141.

## Prior work and limits

Childs's collected intercepts are the primary source. The published period
key is credited to **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**,
[DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
and Lasry's 2017 key comment; their full key provenance is retained. Earlier
unreviewed OCR and insertion-only candidates existed. No explicit p138 B
body example was located in the bounded author-paper review. That does not
establish universal first-decipherment priority.

The source now supplies an instructional sentence worth preserving, together
with a concrete likely reference and a finite mathematical comparison. It
does not make the internal closing unique, prove intentional padding, prove
an exact balanced-half algorithm, or identify the cipher of another message.
