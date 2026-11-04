# Two additional witnesses to the armistice-planning traffic

Parallel receptions preserve clauses of the armistice and their application to German forces in southeastern Europe. Their comparison supplies missing text while keeping the separate reception dates and source differences visible.

**Complete edition by printed page:** [p. 137](../pages/137.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


**Source comparison and edition: icekylinx and GPT-6 Astra Pro.**

Printed p137 preserves two fragments already represented in the
[pp125–126 armistice-planning edition](armistice_transit_planning.md). · [Reading conventions](../../docs/reading-conventions.md)
Their actual coordinate strings distinguish an independently supported
source-mask fill from two corrupt words repeated by both copies.
Neither case changes the published **Nov4–6** key.

## p137 B4

The source explicitly labels this block `4 TL RICHI-212`; `LP v NKJ`
appears after its final `GV`. All 212 observed coordinates give:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
XDIEBESTIMMUNGXDASSENTENTERECHTZURBEFOERDERUNGIHRERTRUPPENASAEMTLICHENEISENBAHNENUNDRECHTDERBESETZUNGALLER
```

</details>

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

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
OXHXL0XDRBHTUNGRM1XAX11118XOPGEH02XANGXORHALTENXOXK0M0RM1A011232XOP
```

</details>

The same conservative ordinary-word candidate remains available:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
OXHXL0XDRAHTUNGRM1XAX11118XOPGEH02XANGXERHALTENXOXK0M0RM1A011232XOP
```

</details>

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

</details>
<!-- CASE-EDITION:END -->
