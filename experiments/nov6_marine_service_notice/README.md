# Conditional November 6 marine-service notice

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Read the [complete p138 C edition](../../cases/radio/nov6_marine_service_notice.md).
The source includes a narrow stroke before VAADA. Counting it as a masked
slot gives the advertised 286 slots. Both that native reading and the
conditional reading that excludes the stroke and adds one final slot are
preserved. The source does not visibly establish either frame operation.

| Scope | Count |
| --- | ---: |
| Literal source slots, including the stroke | 286 |
| Valid observed coordinates | 279 |
| Native and conditional model slots | 286 each |
| Plaintext positions | 143 |
| Fixed conditional raw positions | 136 |
| Fixed edited positions | 141 |
| Observed-coordinate substitutions | 3 |
| Retained source-mask fills | 4 |
| Added-slot fills | 1 |
| Excluded masked mark | 1 |
| Excluded observed coordinates | 0 |

HZYU, KIE? and O?MANIE remain literal. No cause of the reported failure is
inferred. The word repairs and the source-frame proposal are editorial
hypotheses, and the fixed-candidate gap comparison is not a historical
uniqueness proof.


**Reviewed source crops:** [p138_C_reviewed.png](sources/p138_C_reviewed.png) · [p138_stroke_detail.png](sources/p138_stroke_detail.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## Reproduce

```sh
python experiments/nov6_marine_service_notice/verify.py --verify
python experiments/nov6_marine_service_notice/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The verifier retains the native frame, reconstructs the conditional mapping,
prices all 286 single-gap alignments after the declared exclusion, checks
every repair and live case display, and creates a nonhistorical completion
witness for the remaining masks. The optional PDF check compares every
pixel of both source crops using PyMuPDF and Pillow.

The unchanged published Nov4–6 key, previous key recovery and earlier
repository work retain their credit. The work is a source restoration and
explicitly priced reading, not a claim of first decipherment.
