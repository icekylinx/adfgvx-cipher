# p212 A2 / p218 A2: a truncated copy across conflicting page dates

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro**

The 160 coordinates printed as p212 A2 are a close copy of the beginning of the already edited 284-coordinate p218 A2. **157 of the 160 source glyphs are identical**; two valid coordinates disagree and p212 supplies one coordinate where p218 has a printed dash. This identifies a strong source relationship that the earlier date-based screen missed.

The relationship is preserved in a new, independent package. The earlier medical and p218 source data and certificates remain unchanged. The [reading edition](../../cases/pages/212.md#edition-cases-caucasus-p212-p218-crosscopy), [inputs](inputs.json), [certificates](certificates.json) and [source crops](sources/) distinguish the literal fragment, the borrowed tail and the remaining ordinary-word correction.

## The date and message-assembly conflict is unresolved

p212 lies under 22 November and a nominal seven-part medical header. p218 lies under 25 November, with `NKJ v LP (02.10 p.m., November 25th); FUER COS 0950 (11/25) 3 TLE`; that page also says “INTERCEPTED BY BRITISH STATIONS.” The matching ciphertext uses the published `Nov25-28` key.

We do not infer that the p212 block was historically transmitted three days early, that the key date is wrong, or that a particular compiler made an error. The conflicting headings and the close source copy coexist. This fragment is not used to complete the medical message around it.

## Three complementary differences

All indices are zero-based.

| Source index | p212 A2 | p218 A2 | Effect in the aligned 284-coordinate frame |
|---:|:---:|:---:|---|
| 46 | F | G | p212 supplies E in `DEN`; p218 has P in `DPN` |
| 67 | A | Printed dash | p212 supplies the missing coordinate for K in `BERUECKSICHTIGUNG` |
| 103 | G | X | p212 has 7 in `ALLIIERTE7`; p218 supplies N |

The E at plaintext index 109 is determined by two coordinates visible in p212. The K at plaintext index 70 combines p212's A at index 67 with p218's visible X at index 166. That distinction matters: the latter is complementary-source evidence, not a complete letter independently decrypted from the short fragment.

p212 advertises 284 coordinates but prints only 160. Comparing all **161 possible placements of one contiguous 124-coordinate loss** against p218's actual coordinates gives a unique minimum at gap 160, the tail. Its two valid-coordinate disagreements are exactly indices 46 and 103; the old printed dash is not scored as a disagreement. This is uniqueness within a specified copy/loss comparison, not a proof that the unseen historical tail must equal p218.

## Layers and every borrowed coordinate

1. **Literal fragment in the advertised frame:** append 124 erasures, preserving all 160 observed coordinates. Only 30 of the 142 plaintext positions have both coordinates in p212.
2. **Pure source-copy layer:** append p218's 124 literal tail coordinates. All 142 labels become fixed, but `ALLIIERTE7` and `JNNEREN` remain. No observed p212 coordinate changes.
3. **Complementary consensus:** use p218's X at source index 103. The text now has `ALLIIERTEN`; the p212 F/A at indices 46/67 supply `DEN` and `BERUECKSICHTIGUNG`. The shared `JNNEREN` remains.
4. **Optional ordinary-word candidate:** change borrowed p218 coordinate 217 from X to F, giving `INNEREN`. This is a local word repair, explicitly separate from literal copying. `RUSZLAND` remains in its received spelling.

The certificate gives all 284 coordinate origins. Relative to the newly edited p212 fragment, the final candidate has **one observed-coordinate substitution and 124 missing-coordinate fills**. Of those fills, **123 exactly match p218's literal tail**; the remaining one is the separately priced `INNEREN` correction. The pure-copy layer uses all 124 literal witness values unchanged.

| Plaintext-position contribution | Count |
|---|---:|
| Both coordinates observed in p212 | 30 |
| One coordinate from p212, one from p218 | 100 |
| Both coordinates borrowed from p218 | 12 |
| **Total** | **142** |

These are not 142 letters deciphered from the short fragment alone, and they are not a new unique historical message. They are a newly recognized physical copy with a conditional tail restoration and useful complementary evidence for an earlier source edition.

## Bounded search for the still-unread p212 A4

The verifier indexes all **788 blocks** in the frozen whole-Childs OCR corpus, joining groups within each block and indexing only all-ADFGVX windows of ten coordinates. It excludes only each query's own OCR block(s), and does not join separate blocks.

For p212 A2, p218's block contributes 121 aligned ten-coordinate matches at offset zero; all other nonzero hits are also retained. For the 197-coordinate p212 A4 fragment, there are **no nonself exact ten-coordinate matches** in that scope. Its literal source is preserved as contextual unread evidence and contributes no restored reading. The negative result does not exclude a differently enciphered copy, heavy corruption, or an unmodelled frame.

## Counts and reproduce

Only **p212 A2** is newly proposed for the reading catalog: 160 observed coordinates, a 284-coordinate conditional frame and 142 plaintext positions. The previously catalogued p218 A2 and the unread p212 A4 are explicitly outside those counts.

From the repository root, using Python 3.10 or later:

```sh
python experiments/p212_p218_crosscopy/verify.py --verify
python experiments/p212_p218_crosscopy/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The standard check uses the standard library and repository cipher module. It verifies frozen dependencies, independently reconstructs every position/domain, exhausts the 161 gap placements, re-encrypts the copy layers, checks every borrowed coordinate and reruns the 788-block comparison. The optional PDF check additionally needs PyMuPDF and Pillow and reproduces each crop pixel for pixel.
