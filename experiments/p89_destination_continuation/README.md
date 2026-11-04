# p89 A3: the destination continuation

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

This extends the [conditional guard-battalion reading](../p89_guard_battalion_extension/README.md)
of Childs p89 A3 by **ten plaintext positions**, from **166/179 to 176/179**.
Each new position retains one observed coordinate half and fills its missing
half. The extension makes **no additional observed-coordinate substitution**
and fills no additional printed mask. It remains a conditional reading in
the source-declared 358-coordinate frame.

The proposed wording is now:

> Zweitens. Nach Braila geht nichts. Dorthin unterwegs befindliche Dampfer
> abdrehen. Drittens. Weiterleitung in geschlossenen Zügen. Ziel für
> MILI? DIENSTELLEN: Ers. Batl. 2 Garderegts. z. F?sz? Berlin.

The unresolved question marks each denote one plaintext position. Spacing,
case and punctuation are editorial. The spelling **DIENSTELLEN** is retained
literally: it is a proposal for a shortened spelling of **DIENSTSTELLEN**,
with one of the adjacent `ST` repetitions omitted. It does not recover the
standard spelling or change the cipher frame. The source page presents the
[whole five-part order](../../cases/pages/089.md#edition-cases-military-black-sea-evacuation-routes-p89-a3).

## What the new evidence contributes

The office word has a raw corpus witness. **p78 A2** decrypts to
`DIENSTSTELLEN` at plaintext positions 21–33, using **26 originally observed
coordinate halves**. Collapsing its adjacent `STST` to `ST` gives the proposed
11-character `DIENSTELLEN` at p89 A3 positions 132–142. That target interval
contains **16 observed coordinate halves**; every proposed character has at
least one. Six of its eleven positions are newly filled by this extension.
The earlier raw letters and half-coordinate domains constrain the spelling.
The collapse remains a textual hypothesis, rather than an independently
transmitted copy of this order.

The new `L` in `MILI`, the separator following `DIENSTELLEN`, the `S` after
`GARDEREGT`, and the separator after `Z` are also half-supported. The raw
`MILIT` in **p95 A1**, positions 9–13, confirms use of that abbreviation in
the corpus. It does not determine p89 position 131: both coordinates of
that final label are missing.

A contemporary **1918 Berliner Adreßbuch** lists **2. Garderegiment zu Fuß**
in Berlin. The retained [directory evidence](HISTORY.md) documents the
volume, page, image provenance and exact unit entry. It supports the unit
name and city associated with the conditional tail. It supplies no missing
plaintext labels and does not identify the November replacement battalion
or establish that this evacuation order was carried out.

## Exact change and cost

All indices are **zero-based**. These are the only new assignments:

| Plaintext index | Label | Observed pair | Compatible labels before this extension |
|---:|:---:|:---:|---|
| 129 | L | `A?` | `9FILOU` |
| 133 | I | `A?` | `9FILOU` |
| 134 | E | `V?` | `EHJKMP` |
| 135 | N | `G?` | `58BDNW` |
| 139 | L | `?F` | `1GHLWZ` |
| 140 | L | `A?` | `9FILOU` |
| 141 | E | `?G` | `7AENOV` |
| 143 | X | `?X` | `569PTX` |
| 164 | S | `?V` | `3BFKQS` |
| 167 | X | `D?` | `CRSVXZ` |

The prices below are cumulative. “Fixed” means fixed under the stated
conditional layer, including proposed letters, separators and numerical
labels.

| Layer | Fixed positions | Observed substitutions | Printed-mask fills | Lost-coordinate fills |
|---|---:|---:|---:|---:|
| Raw source-declared frame | 81/179 | 0 | 0 | 0 |
| Earlier prefix | 151/179 | 1 | 1 | 69 |
| Guard designation and Berlin | 166/179 | 1 | 1 | 85 |
| Present destination proposal | **176/179** | **1** | **1** | **95** |

The inherited substitution is **source 243 A→G**, giving the W of
`UNTERWEGS`; **source 242** is the printed dash filled with A. The hundred
lost coordinate slots are inserted at **source boundary 200**, where the
page prints `(missed 20 groups)`. Neither the gap nor its location is
selected by the proposed wording.

<details>
<summary>Exact current candidate</summary>

```text
ZWEITENSNACHXBRAILAXGEHTNICHTSXDORTHINUNTERWEGSBEFINDLICHEDAMPFERABDREHENXXDRITTENSXWEITERLEITUNGINGESCHLOSSENENZUEGENXZIELFUERMILI?DIENSTELLENXERSXBATLX2XGARDEREGTSXZXF?SZ?BERLIN
```

</details>

### Three positions remain unresolved

| Plaintext index | Pair | Compatible labels | Frame coordinates |
|---:|:---:|---|---|
| 131 | `??` | All 36 letters and digits in the key | 257, 201 |
| 169 | `??` | All 36 letters and digits in the key | 261, 205 |
| 172 | `X?` | `1346AY` | 75, 281 |

Five coordinate slots remain unknown. The current layer therefore permits
exactly **6^5 = 7,776** complete strings under the published square and
transposition. This is the algebraic completion count, not a count of
plausible German messages.

The certificate separately prices optional completions. Choosing T, X or Z
at position 131 and U at 169 adds **four lost-coordinate fills**, producing
178/179 fixed positions. These alternatives are not accepted in the primary
candidate. The earlier T in `BATL` also remains a fully missing, conditional
letter, while the numeral 2 retains one observed coordinate half.

A separator immediately before `BERLIN` cannot be supplied as a free fill:
X at position 172 would require **one additional observed substitution at
source 75**, together with one lost-coordinate fill. Likewise, spelling out
`ZU` instead of `Z X` requires another observed substitution at source 17.
Replacing the category with `MILITAERPERSONENX` costs thirteen additional
observed substitutions. These costs are retained to make the editorial
boundary reproducible.

## Bounded retrieval check

The [replay](replay_search.py) tests one retrospective proposal: deleting
one adjacent repeated two-character block from a native raw donor stream.
It does not search arbitrary German paraphrases. Its frozen corpus has
**484 distinct raw streams and 51,327 characters**; every entry with
same-message provenance is excluded, including aliased entries. The
110 eligible collapsed variants contain 14,379 characters.

The target window is positions **127–143**, the minimum match length is
ten, and a match must cross the collapsed repetition. The highest-ranked
result is `NDIENSTELLEN`, from p78 A2, with **16 observed target halves**.
Its initial N falls at the wholly missing position 131 and is deliberately
excluded from the accepted assignments; the proposed word starts at 132.

All **128 deterministic coordinate shuffles** have no match of ten or more
characters in that bounded search. Three planted fragments are recovered
under the same geometry. The [frozen report](search_report.json) records the
seeds, donor provenance, exact ranking and controls. Because the spelling
operation and target window were chosen retrospectively, the control
frequency is not a probability that this historical reading is correct.

The underlying [guard-designation replay](../p89_guard_battalion_extension/README.md)
uses the same complete exclusion of same-message aliases. Its independent
raw donor supports `ERSXBATLX2XGARDEREGT` with 27 observed recipient halves;
the fully missing T and the separately proposed Berlin completion retain
their earlier qualifications.

## Reproduce

Run from the repository root:

```sh
python experiments/p89_guard_battalion_extension/verify.py --verify
python experiments/p89_guard_battalion_extension/replay_search.py
python experiments/p89_destination_continuation/verify.py --verify
python experiments/p89_destination_continuation/replay_search.py
```

With the original Childs PDF available:

```sh
python experiments/p89_destination_continuation/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks the source and dependency hashes, published Nov1–3 key,
raw frame, all new assignments, complete re-encryption, remaining domains,
separately priced alternatives, native donor coordinates, and the following
part's exact category clause. It also verifies that the retained directory
region is an exact pixel crop of the full source image. The optional PDF
check reproduces five source crops byte for byte. The original prefix and
its separate certificate remain in
[black_sea_evacuation_routes](../black_sea_evacuation_routes/README.md).

The auditable record is [inputs.json](inputs.json),
[certificates.json](certificates.json), [verify.py](verify.py),
[search_report.json](search_report.json), and [HISTORY.md](HISTORY.md).
