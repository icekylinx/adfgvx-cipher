# Eilvese/OUI traffic schedule

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Read the [complete p113 D1 edition](../../cases/pages/113.md#edition-cases-radio-nov3-eilvese-traffic-schedule).
The source has 362 slots against RIZI-352, with FAGVD DG--- FAGVD in row 5.
A conditional ten-slot exclusion exposes a complete 176-position radio
schedule; two ordinary-word repairs cost three observed substitutions.

| Scope | Count |
| --- | ---: |
| Printed source slots | 362 |
| Valid observed coordinates | 359 |
| Conditional model slots | 352 |
| Plaintext positions | 176 |
| Fixed raw and edited positions | 176 each |
| Observed-coordinate substitutions | 3 |
| Coordinate fills | 0 |
| Excluded observed coordinates | 7 |
| Excluded printed masks | 3 |
| Insertions or reorderings | 0 |

The full native 362-slot decode remains separately available. All 353
contiguous ten-slot exclusions and all 2,556 pairs of complete five-slot
groups are priced against the fixed edited candidate. Every minimum is
retained, including alternatives needing additional source-mask fills.
Eight contiguous no-fill aliases and two whole-group no-fill aliases yield
the same primary raw stream. The comparison does not establish a unique
historical deletion, and the scan marks no cancellation.


**Reviewed source crops:** [p113_D1_reviewed.png](sources/p113_D1_reviewed.png) · [p113_D1_repetition_detail.png](sources/p113_D1_repetition_detail.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).

## Reproduce

```sh
python experiments/nov3_eilvese_traffic_schedule/verify.py --verify
python experiments/nov3_eilvese_traffic_schedule/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The verifier checks the published key, native and conditional source maps,
word costs, every bounded comparison, numerical-label preservation, full
re-encryption and live case displays. The optional PDF check compares every
pixel of the complete crop and repeated-group detail using PyMuPDF/Pillow.

Literal 3X13 is not interpreted as a date; wavelength and time labels are
not independently authenticated or assigned unstated units. The first of
two announced parts is recovered here. Prior key and repository work retain
credit; this source restoration does not claim first-decipherment priority.
