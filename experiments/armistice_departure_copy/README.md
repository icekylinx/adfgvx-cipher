# Armistice-departure report: explicit p151/p157 copy reconstruction

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Read the [source comparison and edition](../../pages/157.md#edition-cases-military-armistice-departure-copy).
The new physical record is p157 A1. Its 83 surviving slots can be aligned
conditionally to the 190-slot p151 A1 frame, with 105 missing prefix slots
and one gap in each short group. The p157 evidence alone fixes **0/95**
plaintext positions in this model. Copied values are never counted as raw
recovery.

The primary reconstructed reading needs five observed p157 substitutions,
five printed-mask fills and 107 absent-coordinate fills. Its STURZFSS
closing retains an unresolved textual problem. A surviving p157 F supports
changing p151's 3 to Z, with the other paired coordinate supplied by p151;
the two additional letters for STURZ DES are separately priced contextual
proposals whose p157 counterpart positions are absent.

The verifier preserves all 25 local gap alignments, the four equal minimum
alignments, all six paired disagreement effects, and all 64 conflict-choice
witnesses for the displayed alignment. All 64 have the same combined
six-substitution cost across both sources; the readable choice also uses
lexical judgment. Both original editions, their inputs, certificates and
attribution files are frozen by digest and remain unchanged.

| Primary p157 scope | Count |
| --- | ---: |
| New physical records | 1 |
| Printed slots / valid coordinates | 83 / 78 |
| Conditional modeled coordinates | 190 |
| Fixed raw labels / proposed labels | 0 / 95 |
| Observed-coordinate substitutions | 5 |
| Printed-mask fills | 5 |
| Missing-prefix fills / short-group fills | 105 / 2 |
| Deletions or reordering of observed coordinates | 0 |

The already cataloged p151 witness is excluded from these new-record
totals. Original source crops are reused through repository-relative links;
the optional PDF check verifies their pixels against the original scan.

## Reproduce

```sh
python experiments/armistice_departure_copy/verify.py --verify
python experiments/armistice_departure_copy/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary verifier uses the standard library and existing repository
helpers. Optional crop verification uses PyMuPDF and Pillow. It checks the
original PDF digest and exact crop pixels. Position domains are checked
against the cipher implementation; every complete displayed candidate and
all 64 source-choice witnesses re-encrypt exactly.

The certificate establishes compatibility under declared source and copy
assumptions. It does not establish a unique historical reading, the
identity of a ministry, or the occurrence of a proposed event. Published
key recovery and earlier source editions retain their credit.
