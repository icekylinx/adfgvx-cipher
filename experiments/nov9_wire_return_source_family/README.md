# 9 November wire-return source family

**Source restoration and verification: icekylinx and GPT-6 Astra Pro.**

This package collates three newly reviewed physical records, p162 C1,
p166 C1 and p166 C2, with the already accepted p162 C2 witness. It uses
the unchanged published Nov7–9 key. The companion
[reading](../../pages/162.md#edition-cases-radio-nov9-wire-return-source-family) presents
the full primary, source-linked and optionally edited streams.

## Reproduce

Run from the repository root:

```sh
python experiments/nov9_wire_return_source_family/verify.py --verify
python experiments/nov9_wire_return_source_family/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

The first command checks the source strings, exact geometry searches,
all pair maps, copy origins, distinct edit costs, native odd diagnostics,
full candidate round trips and complete display mappings. It explicitly
reports that pixel verification was skipped. The optional PDF command
also checks the pinned full-file digest and reproduces the two reviewed
source crops' dimensions and RGB digests. The delivered crops and their
file/pixel checks are linked below.

To regenerate `certificates.json` after an intentional local input change,
omit `--verify`. Verification is read-only.

## Source geometry and evidence limits

The p162 C1 source has 117 coordinates and an explicit missing-first-part
note. The p166 C1 header advertises 312, but its reviewed body has 311
coordinates, including the four-character group `XVGD`. Insertion before
original source 225 or 226 yields the same filled `XXVGD`; both unfilled
aliases are preserved.

The 117-coordinate p162 fragment matches p166 model positions 195:312.
Before filling the absent p166 coordinate, there are 114 independent
agreements, two disagreements and one gap. All 196 possible windows of
this length and all 117 possible one-coordinate insertion locations in
the terminal suffix are enumerated from source coordinates. Offset 195
and the two adjacent gap aliases attain the unique declared minima.
These searches do not use a German target and do not claim to exclude
every possible historical error process.

The p162 prefix restoration copies 195 observed p166 coordinates. It is
not an independent plaintext recovery from p162. The primary p162 model
therefore keeps all 195 prefix slots unassigned: 117 pairs contain one
p162 coordinate and 39 contain neither. Zero complete labels are fixed.
The certificate preserves both origins of every pair in every layer.

## Count contract

`normalized_counts` is the aggregate contract; the corresponding
`per_record_normalized_counts` rows are additive. The primary models and
all their pair/domain/source maps are stored in `primary_unfilled_records`.

| Record | Printed coordinates | Primary fixed labels | Source-linked fixed labels added | Distinct substitutions originating in this record |
| --- | ---: | ---: | ---: | ---: |
| p162 C1 | 117 | 0 / 156 | 156 | 0 |
| p166 C1 | 311 | 155 / 156 | 1 | 5 |
| p166 C2 | 100 | 50 / 50 | 0 | 1 |
| Total | 528 | 205 / 362 | 157 | 6 |

The 195 copied prefix coordinates and one inserted, independently
supported `X` are separate fields. Three substitutions are supported
by other-source coordinates; three are lexical choices in the shared
p166 prefix. Those three shared-prefix changes occur in two displayed
readings but are counted once at their received p166 origins. There are
no exclusions, changed key cells or source reordering.

The already accepted p162 C2 record is retained only as a witness. Its
native raw pair independently supports `ROEM` in p166 C2; p166 C2 in turn
supplies a received-coordinate witness for its existing dash fill in
`ERHIELT`. It does not increase the three-record count.

## Files

- `inputs.json`: reviewed rows, headers, immutable key/core-data hashes,
  PDF/crop/RGB evidence references, explicit operations and limitations.
- `prior_snapshot.json`: earlier p166 OCR, the previous p162 C1 context,
  accepted p162 C2 witness, and its original case-display fingerprint.
- `certificates.json`: independently recomputable primary, source-linked,
  collated and optional layers; every pair's origins; exact geometry
  costs; edit ledgers; native odd-frame diagnostics; retained OCR comparison.
- `catalog_proposal.json`: three proposed physical catalogue entries.
  This file does not modify the global catalogue.

The literal `MITTEILT`, `AKONACH18`, `AKONACH17ROEM4` and all separators
remain unchanged. The source-language labels do not identify a particular
person, organization, border or historical incident. The period key and
earlier solver contributions retain their published attribution; this
package asserts source restoration and collation, not universal
first-decipherment priority.

**Reviewed source crops:** [p162_reviewed.png](sources/p162_reviewed.png) · [p166_reviewed.png](sources/p166_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
