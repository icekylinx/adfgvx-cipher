# Two additional witnesses to the armistice-planning traffic

**Source comparison and edition: icekylinx and GPT-6 Astra Pro.**

Printed p137 preserves two fragments already represented in the
[pp125–126 armistice-planning edition](armistice_transit_planning.md).
Their actual coordinate strings distinguish an independently supported
source-mask fill from two corrupt words repeated by both copies.
Neither case changes the published **Nov4–6** key.

## p137 B4

The source explicitly labels this block `4 TL RICHI-212`; `LP v NKJ`
appears after its final `GV`. All 212 observed coordinates give:

```text
XDIEBESTIMMUNGXDASSENTENTERECHTZURBEFOERDERUNGIHRERTRUPPENASAEMTLICHENEISENBAHNENUNDRECHTDERBESETZUNGALLER
```

This is the clause about Entente rights to transport troops on the railways
and occupy places described in the following part. Its literal
`TRUPPENASAEMTLICHEN` is retained; the edition does not add missing letters
to make that phrase smoother.

Compared with p125 A4, **211 coordinates are identical**. At source index
30, p125 has a noncoordinate 2/Z-shaped glyph that the earlier edition
masked; p137 plainly has X. That observed X independently supplies the
earlier fill and gives the N in `BEFOERDERUNG`. This new physical witness
fixes all **106 plaintext positions without any source repair**.

The preceding p137 B `RIZI-138` block has a different layout and surrounding
call signs. It is not silently treated as part 3 of the p125 message.

## p137 C

The header reads `LP v NKJ 464 (12.01 November 5th), RICHI-134`.
Its **134 coordinates are exactly identical** to p126 B, including the
two values responsible for the damaged words:

```text
OXHXL0XDRBHTUNGRM1XAX11118XOPGEH02XANGXORHALTENXOXK0M0RM1A011232XOP
```

The same conservative ordinary-word candidate remains available:

```text
OXHXL0XDRAHTUNGRM1XAX11118XOPGEH02XANGXERHALTENXOXK0M0RM1A011232XOP
```

It changes source indices **27 and 56, both G→F**, giving `DRAHTUNG` and
`ERHALTEN`. Because both copies repeat the same corrupt values, the new
witness **does not independently confirm those repairs**. All numerical
and reference labels remain untouched.

## Scope and sources

The p137 page heading says November 6 while both receiving timestamps
refer to November 5. These labels are preserved. The earlier source texts,
repairs and catalogue rows remain intact; this adds two physical witnesses,
not two new unique message bodies or a new decipherment of the period key.

| New physical record | Source slots | Raw fixed labels | Observed-coordinate substitutions | Source fills or geometry changes |
|---|---:|---:|---:|---:|
| p137 B4 | 212 | 106 / 106 | 0 | 0 |
| p137 C | 134 | 67 / 67 | 2 | 0 |

See the [source page](../../experiments/retrieved_copy_editions/sources/p137.png),
[transcribed inputs](../../experiments/retrieved_copy_editions/inputs.json),
and [independent certificate](../../experiments/retrieved_copy_editions/certificates.json).
The page is from Childs,
[complete scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).

```sh
python experiments/retrieved_copy_editions/verify.py --verify
```
