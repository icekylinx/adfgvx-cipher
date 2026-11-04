# November 7: Danube crossings and short message reports

Source-reviewed native-frame edition by **icekylinx and GPT-6 Astra Pro**.

The [case study](../../cases/pages/152.md#edition-cases-military-nov7-danube-and-message-reports) adds five distinct physical records:
`p152_B2`, `p152_C`, `p152_D`, `p153_A3`, and `p153_B1`. It does not
recount the original challenge bodies `p153a`/`p153b` elsewhere on page 153.


**Reviewed source crops:** [p152_reviewed.png](sources/p152_reviewed.png) · [p153_reviewed.png](sources/p153_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## Result

The five bodies contain **778 native source slots**, of which **773 are
valid printed coordinates** and five are source dashes. No source slot is
inserted, deleted or reordered. The unchanged published keys produce
**384/389 fixed raw positions**. The explicit editorial proposals make
**14 observed-coordinate substitutions** and fill **four source masks**,
leaving **388/389 edited positions** fixed. The remaining `EB?Q` character
has the exact domain `4FGUYZ`; six full ciphertext/plaintext witnesses retain
every alternative without selecting a historical value.

The readings concern a security force attacked after a crossing near
Belgrad, a morning report of no special events, receipt of a message, a
prescribed line and headquarters field, and Danube crossing traffic.
Literal `219`, `21B`, `SEMUM`, `NOORDL`, `EINSA11205BM4`, `1189`, `35`, and
internal `9.11`/`10.11` labels remain in the earlier word layer. The page-153 reception headers retain
November 7 and the visible marked `ZÖN` spelling. No missing multipart
context, exact reference/time parsing, unit identity or modern place-name
is supplied by that layer.

`p152_C` has a dash-only printed length field, not an advertised 108.
Its 108-slot count comes from the body. Earlier OCR appended five mask
slots; those remain visible in the frozen prior artifact, not in the
physical-source transcription. Page-153 OCR also added one mask to each
of the two native bodies; source review restores 180 and 160 slots.

## The 219th Infantry Division proposal

The parallel **p164 C1** passage supports reading p153 B1's `21B I D` as
**219 I D**. From DONAU to VERKEHR, both native passages contain 63
nonseparator labels; 56 agree, and the remaining seven include two p164
erasures and the differing unit character. At that position, p164 supplies
an observed `GF` pair for **9**, against p153's observed `GX` for **B**.

The proposal makes one additional substitution: p153 source **98**, `X` →
`F`. Its full text therefore costs **six observed substitutions and no
fills**, with all 80 labels fixed. This adds a supported unit reading;
it does not increase the number of fixed positions. The native and earlier
word layers still display `21B`.

The certificate's `records[4].unit_proposal` contains the full native
alignment, the donor's source hash and coordinate origins, the separate
repair ledger and exact re-encryption. The inference is that the two
crossing passages preserve the same unit reference. Their different
headings and openings remain separate, and `SEMUM` is unchanged.

## Files

- `inputs.json`: native source rows, literal headers, unchanged published
  keys and credit, full raw/edited/readable displays, costs and limits.
- `sources/`: reviewed source crops, with byte and RGB hashes and exact PDF
  coordinates recorded in the input.
- `ocr_snapshot.json` and `prior_candidates.json`: frozen prior OCR and
  recomputed unchanged-key diagnostics, separate from the reviewed edition.
- `certificates.json`: all source/model mappings, repair ledgers, position
  domains, exact roundtrip witnesses and aggregate counts.
- `verify.py`: portable regeneration and comparison, including live case
  source/header/display checks and optional exact PDF-pixel verification.
- `catalog_proposal.json`: five entries for root integration; no global
  catalogue is modified by this package.

## Reproduce

```bash
python experiments/nov7_danube_and_message_reports/verify.py --verify
python experiments/nov7_danube_and_message_reports/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

Run the script by its absolute path from any other working directory. The
verifier uses its own file location to find repository inputs.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.
