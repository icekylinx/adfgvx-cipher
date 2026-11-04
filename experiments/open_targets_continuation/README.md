# Cross-key witnesses and conditional shared-square recovery

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

This continuation recovered readable source material by comparing plaintext
under different published keys and by assembling multipart source records.
Fourteen source-checked parts preserve **3,084 coordinate slots** and directly
fix **1,490 of 1,542 plaintext positions** before any editorial repair or new
key inference. No open challenge is claimed solved.

## Readable results

| Source family | Result | Evidence |
| --- | --- | --- |
| [Kremp, p131 / p149 / p159](../../cases/other/kremp.md) | A recovered man asks the military mission to specify his departure date. | p159 is wholly fixed: 98/98 letters, 196/196 coordinates. Its 51-character body repairs earlier witnesses under another key. |
| [Warsaw query, p181 / p214](../../cases/other/mackensen_warsaw.md) | The Soldiers' Council asks whether Mackensen is advancing on Warsaw; a later message quotes the query. | 85/92 directly decoded quote positions match across different keys; complementary evidence resolves the query with exact repair costs. The p181 interpretation is prior published work. |
| [p211 lower B](../../cases/other/p211_key_schedule.md) | Keep the November Ringbahn key; use 10 November for 1 December through 30 November for 21 December. | Three parts, 265/266 fixed positions. The schedule is directly readable and its historical execution is not assumed. |
| [p204 A](../../cases/other/p204_A.md) | Local radio station to be handed over on Monday 1?. | 69/70 fixed positions. The November calendar conditionally identifies 18 and square cell FD=8. |
| [p201 B / p206 A](../../cases/other/p201_p206_orders.md) | Report reached positions; confirm receipt of seven earlier orders. | Matching reference 11{FA}{VV}2 and subject, together with the clear origin date 15/11, conditionally give VA=5. |

The two conditional digit assignments are not added to `data/keys.json`.
Their assumptions and every propagated consequence appear separately in the
certificate. Together they add seven fixed positions in the local p204/p206
readings and exactly one in the existing p205 package, A4 position 86 = `5`.
The remaining digit cells share one injective square and are never treated as
independent wildcard choices.

## Retrieval and source review

An initial all-key screen of the existing 788 OCR blocks, plus adjacent block
joins, ranked language only to select pages for inspection. Comparing shared
plaintext phrases across different key IDs found the Kremp and Warsaw pairs;
direct ciphertext-similarity methods would not expose those different-key
relationships. The already established p186/p187 CHI pair provided a known
positive retrieval check.

No OCR or language score establishes a character in the released readings.
The complete source pages and enlarged crops were visually inspected. The
literal transcripts keep printed non-coordinate glyphs, dashes and one
overtyped unresolved glyph. Rejoining OCR blocks at source line breaks and
correcting OCR length mistakes are separate from proposed changes to the
historical transmission. The preserved inputs identify every earlier OCR
block so these differences can be inspected mechanically.

The earlier p73/p198 known-key and length probes did not produce a defensible
reading. They are not the contribution of this package. This package records
the productive corpus pivot and does not promote a language-ranked diagnostic
to plaintext.

## Files and verification

- [inputs.json](inputs.json): source rows, complete headers, published key
  snapshots, source image hashes, editorial proposals, cross-key alignments
  and historical assumptions.
- [certificates.json](certificates.json): every raw letter domain and source
  pair, all exact repair costs, the quote/body alignments, and a distinct
  conditional key layer.
- [sources](sources/): nine focused source crops from the hash-pinned Childs
  scan; the full book is not redistributed.
- [verify.py](verify.py): an explicit column-offset implementation, compared
  with the project's separate inverse and domain functions. It reproduces
  the complete certificate and checks exact full re-encryption whenever a
  candidate has no remaining unknown characters.

```sh
python3 experiments/open_targets_continuation/verify.py --verify
```

Across the fourteen parts, the separate reader-facing proposals cost **16
known-coordinate substitutions and 19 erasure fills**. Those totals are not
changes to the stored source. Unresolved digits and the damaged p214 closing
reference remain unresolved. Calendar and repeated-reference inferences can
be accepted or rejected without changing any base-source reading.

## Credit and limits

George Lasry and the other original researchers retain the key and earlier
decipherment attributions documented in the main repository. In particular,
the p181 Warsaw query is already discussed by Lasry, Niebel, Kopal and Wacker
in section 6.4 of their 2017 paper. The new source comparison preserves the
paper's 13 November versus source's 12 November date discrepancy.

The present work—retrieval, source assembly, cross-key comparison, exact
repair certificates, conditional inference and readable editions—is by
**icekylinx and GPT-6 Astra Pro**. It makes no first-historical-decipherment
claim. An exact inverse or re-encryption establishes arithmetic consistency
relative to the stated transcription and key; it cannot by itself prove that
the historical copy or inferred date was correct.

## Optional completion of the p214 quotation boundary

The current [Warsaw case](../../cases/military/mackensen_warsaw.md) presents
the complete forwarding introduction and quoted request. One additional
source-mask fill, source **3** `–→A`, reads the erased position after
`FUNKSPRUCHX` as a second separator. This is an editorial punctuation choice
within the retained domain `1GJKWX`; no source word or valid coordinate is
changed. The p214 edition reaches **145/146** positions, with **three
observed substitutions and four fills** in total. Its footer erasure remains.

```sh
python experiments/open_targets_continuation/verify_p214_completion.py --verify
```

[Boundary inputs](p214_completion_inputs.json) · [Live quotation and coordinate certificate](p214_completion_certificate.json).
