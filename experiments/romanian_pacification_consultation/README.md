# Romanian pacification consultation: p157 parts 2–5

**Source edition, exact repair certificates and verification: icekylinx and GPT-6 Astra Pro.**

This package preserves four native source frames on Childs p157 (PDF page 160),
under the unchanged published partial **Nov7–9** key. The page labels the
message **5 TLE**, but its first part is an incomplete 83-slot fragment.
Only source-defined parts **2–5** are cataloged here. They discuss a proposed
military pacification action in Siebenbürgen, request a plenipotentiary
general for a discussion at the literal BUKARST, and ask for early
information about the O.K.M. position under armistice agreements.
The decoded request does not establish that the proposed action occurred.

## Source and count boundaries

| Record | Native source slots | Raw fixed positions | Edited fixed positions | Observed substitutions | Printed-mask fills |
| --- | ---: | ---: | ---: | ---: | ---: |
| p157 A2 | 200 | 100 | 100 | 7 | 0 |
| p157 A3 | 218 | 109 | 109 | 2 | 0 |
| p157 A4 | 210 | 105 | 105 | 0 | 0 |
| p157 A5 | 128 | 63 | 64 | 2 | 1 |
| **Cataloged total** | **756** | **377** | **378** | **11** | **1** |

There are **755 valid source coordinates** and one occupied printed dash
at A5 source index **99**. No length change, deletion, missing-coordinate
insertion or key completion is adopted. The A5 unknown at plaintext
position **23** has the raw domain **02ACLR**; all six coordinate completions
are retained in the certificate. The candidate BALDIGE fills that printed
mask, not a previously unprinted slot. All indices are zero-based.

The separate `contextual_unread_records` section retains A1's **83 visible
slots: 78 valid coordinates and five printed dashes**. Its length heading
is blank and its beginning is absent. It is not included in any of the
four-record totals or in `catalog_proposal.json`. Its 33-coordinate exact
run with p151 A1 is source comparison evidence only: p157 A2 has 200
coordinates and a different body from p151 A2's 186-coordinate frame.
No missing part or opaque p151 closing is supplied by assumed adjacency.
The p151 comparison literal and certificate hash are frozen locally;
the verifier does not depend on a mutable external candidate.

## Source corrections and prior readings

<a id="what-the-source-correction-adds"></a>

Earlier OCR/cached candidates already revealed portions of these bodies;
their exact rows and hashes are retained in `ocr_snapshot.json` and
`prior_candidates.json`. The native source lengths are 200/218/210/128,
where the old OCR snapshots have 199/212/210/120. In particular A5's final
**VGXVF XFG** is present on the page and absent from the old 120-slot OCR.
Every old-to-source alignment is frozen and replayed. Those OCR repairs
are distinct from the eleven proposed changes to visible coordinates.
Published key and earlier body credit remain separate; this package makes
no historical first-solution claim.

The edited stream retains **ZIET**, **BUKARST**, all abbreviations and
**11291**. Readable German adds only two disclosed display letters,
`zie[h]t` and `Bukar[e]st`; it does not insert them into the ciphertext.
Removing these brackets and folding umlauts/punctuation reproduces every
edited non-X label exactly. The verifier checks that mapping.

## Reproduce

From the repository root:

```sh
python experiments/romanian_pacification_consultation/verify.py --verify
python experiments/romanian_pacification_consultation/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The normal check uses Python's standard library and the repository's
cipher implementation. It independently reconstructs the inverse column
permutation, compares it with the project implementation, verifies every
plaintext position/domain, replays each coordinate repair, and re-encrypts
every complete candidate. It also verifies frozen crop and snapshot hashes,
the six A5 completions, source count boundaries, the copy run and readable
mapping. The optional PDF check additionally uses PyMuPDF and Pillow to
compare all six crop pixels with the SHA-bound original PDF.

Full re-encryption establishes compatibility with the stated key/frame,
not the unique wording of a historical message. The earlier source
fragment and historical event identity remain explicitly limited.

See [the reading edition](../../pages/157.md#edition-cases-military-romanian-pacification-consultation),
[inputs](inputs.json), [certificates](certificates.json) and
[catalog proposal](catalog_proposal.json).
