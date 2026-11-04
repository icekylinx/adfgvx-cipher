# p170: bounded contiguous-fragment experiment

**Result: no newly accepted plaintext. A truncation explanation remains possible.** This experiment tests a specific interpretation of the source, rather than treating the handwritten count as a proved transmitted length.

Childs' printed p170, section A, has the header `--- v --- (11.24 p.m., November 9th)` and typed `RICHI` followed by handwritten `106`. The received text contains exactly 106 valid ADFGVX coordinates. Neither a typed transmitted length nor a part number survives. [The source scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) therefore permits, but does not establish, the hypothesis that 106 counts an intercepted fragment of a longer message.

## Exact search scope

For each of 21 audited historical or explicitly attributed comparison keys, we placed the **unchanged 106-coordinate fragment** at every contiguous offset inside every even complete length from **106 through 600**. All coordinates before and after that fragment were treated as unknown. Every observed value and its order were preserved. We did not guess missing coordinates, complete unknown square cells, substitute source glyphs, or insert internal gaps.

There are 248 candidate complete lengths. For lengths `106 + 2k`, there are `2k + 1` possible offsets. Summing these gives **61,504 placements per key**, or **1,291,584 target placements** across 21 keys. The exact squares and column ranks are included in [p170_experiment.json](p170_experiment.json); this includes the partial CHI square and the separately attributed `TRUPPENVERSCHIEBUNG` comparison key.

A marginal language score ranks the observed coordinate patterns while summing over missing coordinates. Each key retains four top-100 pools: all placements, received prefixes, received suffixes, and candidates with at least 12 fixed plaintext letters including a fixed run of at least five. The last pool helps expose candidates that contain more than scattered single-coordinate information. It does not define a statistical confidence set.

For the calendar-consistent 7–9 November key, the strongest candidate in that last pool uses complete length 128 and offset 10. It fixes 40 of 64 plaintext characters, with a longest fixed run of five:

```text
?1?8IXK???IY?NH24???4P?NI?I???PJ?PHKER??YP?V4SMU??WO?DKUEB??NY?4
```

This is a stored search candidate, not a proposed reading. It provides no persuasive coherent message. Several candidates with better unrestricted scores contain no fully determined letters at all.

## Synthetic controls and a concrete limitation

Two control fragments were made by encrypting portions of the previously verified p171 body with the 7–9 November key and retaining exactly 106 contiguous ciphertext coordinates. They were searched with the same geometry bounds and scoring function.

| Control | True full length | True offset | Fixed letters at the true geometry | Rank in unrestricted pool |
| --- | ---: | ---: | ---: | ---: |
| Short middle fragment | 128 | 10 | 42 of 64 | 1 |
| Long suffix fragment | 300 | 194 | 0 of 150 | 2 |

The first control recovered its true geometry at rank 1 and produced recognizable fixed spans. The second true geometry also ranked highly, but **did not fix even one complete plaintext letter**: the available fragment supplies only partial coordinate information at that placement. Consequently, failure to find a readable candidate does not rule out a correct but poorly determined long-message geometry.

These are implementation and sensitivity controls. A normalized version of the p171 body occurs 15 times in the upstream model's military vocabulary, so their ranks cannot be used as a blind performance estimate or as a statistical confidence measure for p170. Their exact plaintexts, ciphertexts, retained fragments and reported hits are preserved in the experiment record.

## Reproduction and limits

The [standard-library verifier](verify_p170.py) independently checks the geometric budget, the arithmetic of all 84 reported pool leaders, and exact encryption roundtrips for both controls. The [portable runner](run_p170.py) reproduces all rankings using the pinned upstream model. All 21 target output files and both control files reproduced byte for byte in the recorded environment.

The enumeration is exhaustive only for the stated keys, normal column-rank convention, lengths, and contiguous-fragment model. It does not test arbitrary unknown permutations, alternative coordinate alphabets, internal losses, source substitutions, or lengths above 600. Language ranking and candidate acceptance remain heuristic. Other branches of the investigation have separate reports; their budgets are not counted here.

The record supports a bounded negative search result and a useful sensitivity warning. It does not establish that p170 is a complete 106-coordinate message, prove that it was truncated, or exclude a longer-message explanation.
