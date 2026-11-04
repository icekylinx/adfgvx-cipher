# Rail, motor and air transport on 30 November

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

This package source-reviews all six physical parts of three telegrams on
Childs p229, using the unchanged published Nov28–Dec1 key. The
[readable case](../../cases/pages/229.md#edition-cases-military-late-transport-dispatches) gives the
full conditional texts and preserves all unit, quantity and reference labels.

## What is recovered

The three-part evening report records an advance to `TISZAFOELDVAR`, halted
transport on the proposed Arad–Szolnok route, and the resulting failure to
carry out the day's loadings. The two-part motor-transport request asks
whether the army can release more columns. Its corrupted `OH40` is separately
read as the proposed office `OHL` followed by an **unassigned raw quantity
label `0`**, not “40 columns.”

The final aviation message is the largest source-recovery gain. The earlier
OCR stream contained 323 slots and did not yield this coherent Nov28-key
body. Visual retranscription gives the source's exact 330 slots, with 33
printed dashes and one masked, Q-shaped glyph. It directly fixes 131 of 165 label
positions. Three observed-coordinate substitutions and 31 erasure fills
support a 162-position conditional edition: a flight detachment is queried,
the proposed destination is Craiova, a park is being established, and
aviation formations are to be replenished as prescribed. The destination
field `HK?`, a boundary and a reference position remain unresolved. The
unit's raw `24` is not historically numbered.

## Exact scope

| Part | Source slots | Raw fixed labels | Edition fixed labels | Substitutions | Fills |
| --- | ---: | ---: | ---: | ---: | ---: |
| p229 A1 | 228 | 114 / 114 | 114 / 114 | 1 | 0 |
| p229 A2 | 192 | 95 / 96 | 96 / 96 | 1 | 1 |
| p229 A3 | 176 | 88 / 88 | 88 / 88 | 2 | 0 |
| p229 B1 | 268 | 131 / 134 | 133 / 134 | 1 | 2 |
| p229 B2 | 248 | 118 / 124 | 123 / 124 | 6 | 5 |
| p229 C | 330 | 131 / 165 | 162 / 165 | 3 | 31 |
| **Total** | **1,442** | **677 / 721** | **716 / 721** | **14** | **39** |

There are 43 printed dashes and one invalid glyph; five source-erasure positions
remain unknown. No source coordinate is inserted, deleted or reordered. The
source images also recover two earlier OCR-erased visible coordinates in B1
and B2. Those corrections of OCR are distinct from the priced source repairs.

The edition retains literal `AKKS`, `TELRAMM` and the six-character `KONNEN`.
No missing letters are silently inserted. Numerals, `J/Q/Y` labels, complete
raw texts, all repair positions, protected fields and residual domains appear
in [certificates.json](certificates.json). The earlier A/B candidates are
preserved in [prior_candidates.json](prior_candidates.json), and the prior
published key remains credited to Lasry, Niebel, Kopal and Wacker. The bounded
publication check is documented; no universal first-decipherment claim is made.

## Reproduce

```sh
python experiments/late_transport_dispatches/verify.py --verify
```

Default verification uses the Python standard library and existing independent
column/domain/re-encryption helpers. It checks source-image and prior-candidate
hashes, exact received lengths, unchanged keys, every protected field and
coordinate edit, and complete global round-trip witnesses. Witnesses are
marked nonhistorical consistency examples.

Optional source authentication with PyMuPDF:

```sh
python experiments/late_transport_dispatches/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

This checks the pinned PDF digest and independently regenerates all four
delivered source crops, comparing their dimensions, channels and pixels.
The full source page, crop rectangle and scale are recorded in `inputs.json`.
