# Berlin General Staff map-sheet request

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

Source edition and verification: **icekylinx and GPT-6 Astra Pro**.
The published Nov7–9 period key retains its original attribution.

## p162 B1

Childs printed p162 (PDF p165) has header `UKS v ZON`, reception
`03.40 a.m., November 9th`, and `1109 2 TLE`. The printed part label is
`1 TL`; its length field is literally `RICHI-182?`. That final question
mark belongs to the header, not to the encrypted body.

The [source image](../../experiments/nov8_map_and_boundary/sources/p162_B_detail.png)
contains **181 visible slots**. Its initial group is the four-character
`DGDD`. The primary **182-slot conditional frame** inserts one unknown
coordinate at source boundary 1, giving `D?GDD`; no observed glyph is
removed. The source identifies a short group but does not determine an
exact internal missing position. The other part of this physical
transmission is not identified here.

The [faded-glyph crop](../../experiments/nov8_map_and_boundary/sources/p162_B_faint.png)
needs a separate source qualification: source 110 is provisionally read F
in `VFGGD`, but an E-like reading remains possible. The primary arithmetic
uses the stated F and explicitly pays for changing it. The E/masked
sensitivity below retains the alternative; plaintext fluency is not used
to make the source glyph certain.

**Raw output — conditional 182-slot frame, with the explicitly provisional F transcription:**

```text
STELLVERTRXG?NERJLSTABBERLINXZUSENDUNG?ONJE?0BL??TTERNKAR2E1ZU7?000XB1B2B3C1C2C3D1D2D3E2E3X
```

**Edited output — same frame; two observed substitutions, three printed-mask fills and one missing-coordinate fill:**

```text
STELLVERTRXGENERALSTABBERLINXZUSENDUNGVONJE?0BLAETTERNKARTE1ZU7?000XB1B2B3C1C2C3D1D2D3E2E3X
```

The substitutions are **source 110 F→D** (`J`→`A` in `GENERAL`) and
**source 150 D→V** (`2`→`T` in `KARTE`). The first cost depends on the
provisional F source reading; it is not hidden as an ordinary erasure fill.
Printed source 84 `Z` is filled with A, source 85 dash with V, and source 149
dash with D. The extra model coordinate is filled with D. These are three
different operation classes, and all source offsets are zero-based.

Under that frame and transcription the raw reading fixes **85 / 91
positions**, and the edited layer fixes **89 / 91**.

**Readable German — exact nonseparator labels of the edited layer, with spacing, punctuation and conventional umlaut rendering:**

> Stellvertr. Generalstab Berlin. Zusendung von je ?0 Blättern Karte 1 zu 7?000. B1 B2 B3 C1 C2 C3 D1 D2 D3 E2 E3.

The letter-number sheet list remains literal, and `STELLVERTR` remains
abbreviated. No requested quantity or map scale is silently completed.

## Conditional interpretation: linked numbers and source sensitivity

Both unresolved numerical positions, plaintext 43 and 63, use the **same
missing square cell XA**. The two unused key labels are 5 and 6, so the
complete coupled alternatives are:

| XA label | Other missing cell VF | Quantity field | Scale field |
|---|---|---:|---:|
| 5 | 6 | 50 | 1:75000 |
| 6 | 5 | 60 | 1:76000 |

Both assignments decrypt and re-encrypt the complete edited witness.
Mixed quantity/scale pairings are unsupported by this key. No external map
history is used to select one of the two alternatives.

The independent fixed-target audit checks **all 182 insertion boundaries**
under the primary F transcription, retaining the two XA identities rather
than treating the numerical question marks as free independent characters.
Boundaries 0 and 1 tie at two observed substitutions and yield the same
completed ciphertext but different source-origin maps. The first five
boundary costs are **2,2,3,4,4**. Boundary 1 is the displayed convention,
not a unique historical loss location.

A second complete 182-boundary audit treats the doubtful source 110 glyph
as noncoordinate E, hence as a source mask. It has the same two optimum
origins and the same completed reading, with **one observed substitution,
four source-mask fills and one missing-coordinate fill**. The primary
summary retains the more explicit F-based substitution cost; it does not
silently switch to this cheaper interpretation.

The unaltered 181-slot diagnostic, its unpaired coordinate, all five
source-local group placements and both complete global key witnesses are
preserved in the [inputs](../../experiments/nov8_map_and_boundary/inputs.json)
and [certificates](../../experiments/nov8_map_and_boundary/certificates.json).
The [reproduction guide](../../experiments/nov8_map_and_boundary/README.md)
also records prior OCR and key credit. The bounded comparison prices a
supplied template; it is not a claim of blind or historical uniqueness.
