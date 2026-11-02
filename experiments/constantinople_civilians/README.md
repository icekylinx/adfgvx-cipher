# Constantinople civilian-departure enquiry

ADFGVX Cipher — **icekylinx and GPT-6 Astra Pro**.

Four source-edited parts recover an enquiry about German civilians,
principally women and children, reportedly leaving Constantinople. The
message asks for verification through the Swedish legation, requests news
about troop transports, describes an appeal to allow German civilians to
remain in Turkey, and says that transport through Ukraine is currently
impossible. It reports an unconfirmed departure; it is not itself proof
that the departure occurred.

The [case](../../cases/other/constantinople_civilians.md) gives all four
raw and proposed readings. The source is J. Rives Childs, *General Solution
of the ADFGVX Cipher System*, printed p221 B, PDF p224. The page heading
says November 25, 1918; the origin line is `1300 (25/11)`, and receipt is
November 26 at 06.14 a.m. The four literal crops, source rows and headers
are preserved in `inputs.json` and `sources/`.

| Record | Printed slots | Valid coordinates | Modeled length | Raw fixed | Candidate fixed | Valid-coordinate changes | Source-erasure fills | Added-coordinate fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| p221 B1 | 297 | 297 | 298 | 148/149 | 149/149 | 1 | 0 | 1 |
| p221 B2 | 345 | 344 | 344 | 171/172 | 172/172 | 4 | 1 | 0 |
| p221 B3 | 348 | 347 | 348 | 173/174 | 174/174 | 3 | 1 | 0 |
| p221 B4, source-local model | 265 | 265 | 266 | 132/133 | 133/133 | 9 | 0 | 1 |
| **Total** | **1,255** | **1,253** | **1,256** | **624/628** | **628/628** | **17** | **2** | **2** |

B2 additionally removes one explicitly identified valid coordinate from
a six-letter group. Counts describe the primary source models and include
raw numerical labels and received garbles. In particular, the three
headcount symbols `0YY` are not interpreted as a conventional number.
No published key cell is changed.

## Geometry and the quantity

B1's four-letter `ADDG` group is restored by a one-coordinate model at
boundary 227. All 298 boundaries are checked, with all three headcount
positions masked; 227 is the unique one-substitution optimum for the
ordinary words. Its three headcount symbols are complete original pairs:

| Position | Pair | Original source coordinates | Raw label |
| --- | --- | --- | --- |
| 71 | `AF` | 123, 251 | `0` |
| 72 | `DG` | 6, 200 | `Y` |
| 73 | `DG` | 226, 84 | `Y` |

The reading therefore preserves **`0YY`**, not the earlier OCR/frame
artifact `0Y5`. The quantity contributes no constraint to frame selection.

B2 has the six-letter `AXDGXF` group. Removing source index 134 uniquely
minimizes the declared ordinary-word stencil over all 345 deletions.

B4 has a four-letter `XDXG` group at source 190–193. Its source-local
best model inserts at 190 and needs nine observed-coordinate changes
for the full proposed text. A broader body-only search, with `PARIS`,
`UKRAINE` and the footer masked, gives six tied minima at **181–186**,
outside that deficient group. Their full proposed-text costs are
8, 7, 7, 6, 6, 6. All six broader raw views and the source-local view are
retained with reversible coordinate maps and separately priced repairs.
The complete proposed text and corrected ciphertext are the same across
all seven. The better word score does not silently override the physical
group evidence, and no unique original loss position is claimed.

## Independent historical corroboration

`historical_context.json` cites two contemporary diplomatic texts in the
official U.S. *Foreign Relations* source edition. Lansing's November 15,
1918 note to the Swiss minister states that the German radio appeals
will be sent to the associated governments and the Supreme War Council.
His November 16 telegram to House reproduces Solf's request that German
civilians be permitted to remain in Turkey and forwards it for that
council. These sources were found after the source readings and geometry
analysis; they corroborate the subject and routing, not the headcount,
departure, or any source-frame choice. The underlying archival manuscripts
were not inspected.

The source message credits President Wilson. The independent texts record
Lansing's official actions; they do not establish a separate personal act
by Wilson.

## Attribution and verification

The period key retains its published attribution in `inputs.json`.
Lasry and colleagues discuss the neighboring p221 A Mackensen message;
this edition covers B1–B4 only. The bounded paper/dissertation/comment
check located no explicit discussion of this B body and makes no universal
historical-priority claim.

```bash
python experiments/constantinople_civilians/verify.py --verify
python experiments/constantinople_civilians/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier independently reconstructs the transposition and domains,
checks all three exhaustive frame screens, retains every declared tied
view, verifies all coordinate repairs by exact reencryption, and confirms
that the quantity was masked during geometry selection. The PDF option
checks the full primary scan hash and every crop pixel. Numerical
relabelling is deliberately outside this source edition.
