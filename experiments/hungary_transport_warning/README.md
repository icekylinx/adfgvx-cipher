# Hungary transport warning: a witnessed missing group

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro**

This edition covers six physical parts on Childs printed p184 (PDF p187): B1–B3 and C1–C3. Two three-part transmissions warn the Mackensen command's mineral-oil department against letting transports from Romania enter Hungary. The source says they would be completely lost there. That is the message's warning, not an independently established outcome.

The useful restoration is **B2's missing five-coordinate group `DXDVA`**. The source advertises 192 coordinates but prints 187. An alignment containing 92 directly readable positions from the uncorrected C2 body singles out gap 35, before the eighth printed group, among all 188 possible placements of one contiguous five-coordinate gap. It restores five plaintext letters with **zero changes to observed B2 coordinates**. The uniqueness claim is conditional on this explicit gap model and alignment.

The [reading edition](../../cases/military/hungary_transport_warning.md) gives all six raw strings, the conservative candidates and the source differences. The principal evidence is [inputs.json](inputs.json), [certificates.json](certificates.json), and the [source crops](sources/).

## What is and is not identical

Both source headers say from LP for UKS, origin `13.40 (13/11)`, three parts. B is received as `NKJ v LP (02.51 a.m., November 13th)` and C as `ZO'N v NKJ (02.15 a.m., November 13th)`. These morning receipts precede the stated origin time on the same printed date. We preserve that inconsistency and do not repair the date or time.

The address parts differ in length and received spelling. B1 has `MACKENSEN`, `MINERALOEL` and `BUCKAREST`; C1 has `MKENSEN`, `MINERALOL` and `BUMAREST`. These differences are not silently normalized.

The body parts also differ. C2 has an extra unresolved position in `HE?REIN`, omits the separator between `RESTLOS` and `VERLOREN`, and ends with one X where B2 ends with two. Two ordinary-letter repairs in C2, `TRANSTORTE → TRANSPORTE` and `TIND → SIND`, are witnessed by unchanged B2 letters. Those two witness positions were excluded from the gap-selection mask, avoiding circular support.

B3 and C3 have exactly the same coordinate pairs for all 54 C3 plaintext positions. B3 adds one terminal X. This exact pair agreement includes 15 unresolved reference positions per copy; it does not supply their labels. The faint C3 groups `AXADX` and `DFVGA` have a separate eight-times-scale crop documenting the literal source reading.

## The missing-group certificate

All indices are zero-based. Five coordinates are absent before source index 35. The screen constructs its masked plaintext **from C2's uncorrected raw text**, using these correspondence ranges:

| B2 start | C2 start | Matching positions |
|---:|---:|---:|
| 0 | 0 | 5 |
| 6 | 6 | 39 |
| 45 | 46 | 35 |
| 81 | 81 | 9 |
| 91 | 91 | 4 |

B2 positions 5, 80, 90 and 95 are excluded. All 188 gap scores are frozen. Gap 35 alone needs zero observed-coordinate substitutions; gaps 34, 36 and 37 each need one. The five missing stencil coordinates are all determined by the mask and equal `DXDVA`.

| Restored B2 plaintext position | Character | Uncorrected C2 witness position |
|---:|:---:|---:|
| 8 | T | 8 |
| 18 | A | 18 |
| 28 | H | 28 |
| 79 | S | 80 |
| 89 | X | 89 |

Full re-encryption of the restored B2 plaintext reproduces every printed coordinate in order and the inserted group. The verifier separately derives the inserted group from the C2 mask, before using the full B2 candidate.

## Counts and limits

The package preserves 877 printed coordinates and models 882 after the five-coordinate gap. There are 441 plaintext positions: 405 fixed under the source-aligned models, 410 after the witnessed fills and two C2 substitutions. Thirty-one positions remain unresolved: 30 footer positions and C2's extra word position.

The last position has received pair `DX`, source indices 90 and 137, and unchanged domain `0123456789QY`. The footer domains are also retained in full. No partial-square cell, digit, rank, address length or date is changed.

Earlier unreviewed repository screens already contained recognizable address, warning and footer material; their relevant candidate records and hashes are frozen. A bounded check of the Lasry–Niebel–Kopal–Wacker paper, Lasry dissertation and cached 2017 discussion found no explicit discussion of this body. This is not proof of historical priority. The contribution is a source edition, a new source-supported missing-group certificate and a fully auditable distinction between exact matches and received differences.

## Reproduce

From the repository root, using Python 3.10 or later:

```sh
python experiments/hungary_transport_warning/verify.py --verify
python experiments/hungary_transport_warning/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The first command uses the standard library and the repository's cipher module. It recomputes the inverse permutation independently, checks every position and domain against the cipher module, reruns all 188 gap models, verifies the complete pairwise footer comparison, and checks the frozen certificate and crop hashes. The optional PDF check additionally requires PyMuPDF and Pillow; it checks the PDF hash and reproduces every crop pixel for pixel.
