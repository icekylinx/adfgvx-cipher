# Ringbahn instruction to the Caucasus delegation in Tiflis

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Childs p146 section C contains a differently worded two-part witness of the
November/December Ringbahn key schedule. Read the
[complete edition](../../cases/radio/nov6_tiflis_ringbahn_instruction.md).

| Scope | Count |
| --- | ---: |
| Physical records | 2 |
| Printed source slots | 365 |
| Valid observed coordinates | 359 |
| Conditional model slots | 368 |
| Plaintext positions | 184 |
| Fixed raw positions | 175 |
| Fixed edited positions | 184 |
| Observed-coordinate substitutions | 1 |
| Printed-source mask fills | 6 |
| Added-slot fills | 3 |
| Deleted/reordered source slots | 0 |

The full candidate for part 1 has a unique zero-substitution alignment among
all 15,400 fixed-text two-gap alignments. Part 2 has three equal minima
(boundaries 37, 38 and 39) among all 192 single-gap alignments. All three are
retained. This is uniqueness within a fixed-candidate family, not a claim
of unique historical wording or a first decipherment.


**Reviewed source crops:** [p146_C_reviewed.png](sources/p146_C_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## Reproduce

```sh
python experiments/nov6_tiflis_ringbahn_instruction/verify.py --verify
python experiments/nov6_tiflis_ringbahn_instruction/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary check uses Python's standard library and the pinned existing
repository verification helper. It independently reconstructs transposition
indices, source-mask domains, complete re-encryption, all fixed-text gap
costs and exact raw support from p145 B3 and p211 lower B2. It also checks the
live case's raw/edited blocks and complete readable German against the
verified strings. The optional source-image check uses PyMuPDF and Pillow
and compares every RGB pixel against a render of the pinned public PDF.

Published key recovery and earlier Ringbahn editions retain their separate
credit. Literal `4B47857`, date layers and all invalid printed glyphs remain
unchanged in the source evidence. The final `NACHRICHTENCHEF` repair is
lexical; the supporting dispatches print the abbreviation `NACHRCHEF`.
