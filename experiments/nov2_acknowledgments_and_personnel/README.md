# 2 November acknowledgment copies and personnel orders

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Seven physical records on Childs pp104–106 contain **1,175 typed source
slots** and **1,172 valid coordinates**. Their declared frames contain
**1,176 coordinates** and **588 plaintext positions**, with **584 fixed raw
positions**. The edited candidates fix **587/588**, using **3 observed
coordinate substitutions**, **2 printed-mask fills**, and **1 fill in an
added slot**. One battalion position remains unresolved. The published
Nov1–3 key is unchanged.

The [Meier order](../../cases/pages/104.md#edition-cases-people-meier-berlin-order) recovers a complete
75-position instruction from the visibly short four-coordinate group ADAG.
Adding A gives ADAAG with no observed-coordinate substitution. Two adjacent
gap alignments produce the identical ciphertext and text; both are retained.
The certificate prices all five local alignments, without claiming a unique
historical loss position.

The [acknowledgment edition](../../cases/pages/104.md#edition-cases-radio-nov2-telegram-acknowledgments)
assembles the native three-part p105 C1 / p106 A2–A3 message. All 318 positions
read without repair. A fourth physical witness, p104 A3, preserves the
conflicting source date and one-coordinate/reference-digit difference.
The [UKS service message](../../cases/pages/104.md#edition-cases-radio-nov2-uks-connection) retains
literal 5UKS, NSM and 6NKJ. The [Sevastopol transfer consent](../../cases/pages/104.md#edition-cases-people-sevastopol-transfer-consent)
keeps its unknown unit field.

`inputs.json` freezes literal rows, annotations, headers, all geometry,
unchanged key and six inspected crop bindings. `certificates.json` supplies
independent transposition indices, every coordinate pair/domain, exact
repair prices, equivalent gap witnesses and the near-copy difference.
All full proposed texts re-encrypt exactly; the one remaining partial text
has its fixed coordinate-pair constraints checked instead. Complete readable
German quotes preserve every nonseparator label, including the unknown.
`prior_candidates.json` credits earlier unreviewed repository body candidates;
this is a source-audited edition and local reconstruction, not a first-solution
claim.

## Reproduce

```sh
python experiments/nov2_acknowledgments_and_personnel/verify.py --verify
python experiments/nov2_acknowledgments_and_personnel/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The optional PDF check verifies the original file hash and byte count and
compares all six regenerated crops pixel for pixel. It requires PyMuPDF and
Pillow; the normal check uses only the standard library and checked-in
modules. No scratch file is a runtime dependency.
