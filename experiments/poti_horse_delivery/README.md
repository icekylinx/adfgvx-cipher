# Poti horse-delivery continuations

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.**

This edition restores the native source frames of **p59 A2 and A3**. It keeps
the associated first part, **p59 A1**, as uncounted literal context. The shared
header says `SSD, COS v ASO (07.50 a.m., September 22nd)`, followed by
`2250 (21.9) 3 TLE`. The two edited continuations use the unchanged published
**Sep19–21** key; the receiving date does not override the message's 21.9 field.

The substantive reading concerns a shipment at Poti for `7XKAVXBRIG`, an
abteilung ordered elsewhere, horses handed over at Poti, and a request for an
urgent reply to an earlier radio message. The syntax of the handover clause is
incomplete in the conservative reading: it does not by itself establish that
the horses were actually handed over. The source is error-heavy, and the exact
editorial costs are central to the edition.

| Counted record | Source slots | Valid coordinates | Plaintext positions | Raw fixed | Main edited fixed | Observed substitutions | Printed-dash fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| p59 A2 | 220 | 213 | 110 | 103 | 106 | 11 | 3 |
| p59 A3 | 230 | 199 | 115 | 85 | 107 | 9 | 23 |
| Total | 450 | 412 | 225 | 188 | 213 | 20 | 26 |

“Fixed” means that the algebraic domain contains one symbol; it does not mean
that an erroneous received symbol is historically correct. The main edition
leaves **four** A2 positions and **eight** A3 reference positions unresolved.
There is no insertion, deletion, frame change or key change in these two records.

## Conservative reading and costly contextual hypothesis

The main A2 edition retains the opaque ending **BRTVEXO0?NDWME??EL?XX**.
Reading it as **BRIEFXOBUNDWEMDIESEXX**, encouraged by the following A3 wording,
requires **14 additional observed-coordinate substitutions and four additional
dash fills**. The resulting complete A2 hypothesis therefore costs **25
observed substitutions and seven fills** from the literal source. It is fully
reversible, but that arithmetic does not make it the historical text. It is
preserved in `optional_contextual_extension`, outside all main counts.

The optional hypothesis ends in `DIESE`, and A3 independently begins in
`DIESEXPFERDE...`. Both occurrences remain. No word or source coordinate is
deleted to make the joined sentence smoother. The brigade label `7` and all
remaining numerical/reference labels stay as produced by the published square.

## First-part frame conflict

The A1 heading explicitly prints **RICHI-220**, while the body has **225
visible slots**, including eight dashes. This is a source-level disagreement,
not an omitted OCR row that can simply be reinserted. The native stream has odd
length and is not accepted as a decryptable frame.

The certificate retains **all 221** conditional models formed by deleting one
consecutive block of five visible slots. It records the excluded source indices,
literal glyphs, known-coordinate deletion cost, exact ciphertext and raw reading
for each. Positions **200** and **201** happen to yield the same conditional
ciphertext; they are shown as illustrations of readable fragments, not a unique
solution. Even those frames retain an unresolved and implausible opening. No A1
plaintext is included in the catalog proposal or the counts above. Broader loss,
addition, reordering and transcription explanations remain open.

## Remaining domains and exact compatibility counts

For A2, the four unfilled source dashes affect four separate plaintext positions,
each with a six-symbol domain. For A3, the eight unfilled dashes likewise affect
eight separate positions. The complete fixed square is bijective, so these give
exactly **6^4 = 1,296** and **6^8 = 1,679,616** distinct complete plaintexts
compatible with the respective main edited coordinates. This is mathematical
counting, not a claim to have enumerated all completions or to know their digits.

The verifier supplies six single-coordinate witnesses for each remaining
erasure while holding all other unfilled coordinates at A. Every witness is
decrypted and re-encrypted exactly. The A-valued baseline is only a reproducibility
convention; it does not select a historical completion. Full raw domains and
source-index pairs remain in the certificate, including all inconvenient letters
and digits in the reference fields.

## Reproduction and attribution

```bash
python experiments/poti_horse_delivery/verify.py --verify
python experiments/poti_horse_delivery/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The default command uses the Python standard library and repository cipher
module. It independently reconstructs the transposition map, checks every domain
and editing operation, verifies the finite completion witnesses, and regenerates
all 221 A1 diagnostic frames. The optional PDF command requires PyMuPDF and Pillow
and verifies the source PDF hash, byte length and three crop images pixel for
pixel. No external language model or temporary screen file is required.

[Inputs](inputs.json), [certificates](certificates.json),
[earlier candidates and bounded attribution checks](prior_candidates.json),
[catalog proposal](catalog_proposal.json), and the
[readable case](../../cases/pages/059.md#edition-cases-caucasus-poti-horse-delivery) form the complete
edition. A2 already had a partially readable repository candidate. The earlier
A3 OCR fragments omitted many dash slots and did not yield this native-frame
reading. Bounded paper, thesis and comment searches found no explicit separate
body discussion; that is not proof of priority. The published key retains its
original credit. No historical first-solution claim is made.
