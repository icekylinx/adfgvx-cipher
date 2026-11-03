# Newspaper sacks arriving via Orsova

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition: icekylinx and GPT-6 Astra Pro.**

This two-part telegram tells the **Oberpostdirektion in Breslau** that sacks
of Berlin newspapers arrived yesterday and today via **Orsova**, and asks
for immediate postal dispatch by the same route. It gives priority to two
references, `7?3` and `308`, without spelling out their exact administrative
meaning.

The source is Childs, *General Solution of the ADFGVX Cipher System*,
[printed p171 B, PDF p174](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [two parts](../../experiments/newspaper_dispatch/sources/p171_B.png)
have this header:

**Source transcription — clear header and/or literal source record:**

```text
B) NKJ v LP (1.01 a.m., November 10th)
1858 (9/11) 2 TLE
```

The page heading says `9th NOVEMBER, 1918.`; the receiving timestamp is
November 10. Both are retained. The source lengths are exactly 200 and
186 coordinates, using the unchanged published Nov7–9 square and ranks.

## Exact readings and separately priced repairs

**Raw output:**

```text
OBERPOSTDIREKTIOKBRESLAUXGESTERNUNDHEUTEBERLINERZEITUNGSSAECKEUEBERO?SOVAHIERE?NGEGANGENXVERANLASSET
```

One observed-coordinate substitution repairs `DIREKTIOK→DIREKTION`, and
two fills of printed dashes give:

**Edited output:**

```text
OBERPOSTDIREKTIONBRESLAUXGESTERNUNDHEUTEBERLINERZEITUNGSSAECKEUEBERORSOVAHIEREINGEGANGENXVERANLASSET
```

**Raw output:**

```text
S8FORT3OSTBEFOERDERUNGAUFSELTEMWEGEXVOUZUGSWEISE7?3UND308XXXEUTSCHEFELDPOSTDIREKTIONRUMAENIEN
```

Five observed-coordinate substitutions repair ordinary words:

**Edited output:**

```text
SOFORTPOSTBEFOERDERUNGAUFSELBEMWEGEXVORZUGSWEISE7?3UND308XXDEUTSCHEFELDPOSTDIREKTIONRUMAENIEN
```

The signatory is the German field-post directorate in Romania. The doubled
`XX` before `DEUTSCHE` is retained, as are both reference fields.

| Part | Actual slots | Raw fixed labels | Edition fixed labels | Known-coordinate changes | Printed-erasure fills |
|---|---:|---:|---:|---:|---:|
| B1 | 200 | 98 / 100 | 100 / 100 | 1 | 2 |
| B2 | 186 | 92 / 93 | 92 / 93 | 5 | 0 |
| **Total** | **386** | **190 / 193** | **192 / 193** | **6** | **2** |

There are no inserted, deleted or reordered source coordinates. Both bodies
were already recognizable in earlier unreviewed OCR-derived computations;
the present contribution is the source edition and exact repair accounting.

## What remains unknown, and what an earlier hypothesis would imply

The unknown in `7?3` is **not a printed erasure**. Its two coordinates are
fully observed: source positions **172 and 32** form **`XA`**, one of the two
unassigned cells in the published Nov7–9 square. Its baseline domain is
**`56`**. Both the original and edited ciphertext retain that exact pair.

The earlier [military-context certificate](../../experiments/p170_continuation/military_context.json)
separately proposes `VF→6` and consequently `XA→5`, under its independent
French-telegram unit identification. If that existing conditional layer is
adopted, this field becomes **`753`**. The new postal message supplies no
independent confirmation of that digit assignment; `7?3` remains the baseline
reading. No specific field-post office or unit is identified here.

## Attribution and verification

The period key is credited to **George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker**. This B telegram is physically separate from the p171 A1
challenge, whose body was read by **Norbert in 2017** and is retained in
[its canonical case](../p171.md). Nothing here changes that priority.

The [inputs](../../experiments/newspaper_dispatch/inputs.json) and
[certificate](../../experiments/newspaper_dispatch/certificates.json)
retain all source rows, raw and edited strings, global witness completions,
exact source changes and the separately marked conditional numeric field.
The bounded discussion/paper check is recorded; no universal priority claim
is made.

```sh
python experiments/newspaper_dispatch/verify.py --verify
```

The optional `--pdf` argument verifies the pinned source digest and compares
the regenerated source-crop pixels. Re-encryption certifies consistency and
cost, not uniquely original wording.
