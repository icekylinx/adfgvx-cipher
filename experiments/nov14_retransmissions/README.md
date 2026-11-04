# 14 November traffic under two different keys

**Source edition, alignment and verification: icekylinx and GPT-6 Astra Pro.**

Seven physical intercepts preserve three message families. The p190 B/E
backup-station request has the same 88-position wording under the distinct
13 November–15a and 13 November–15b keys. The p190 A / p194 B pilot-arrival
notices describe the same apparent event but use different wording. Their
four-position `FR?E` name fields support a conditional equality between two
unknown square cells; they do not determine a unique surname or digit.
The interrupted p193 B source is an exact 195-coordinate suffix of p194 B,
which restores 85 missing prefix coordinates and 85 further raw letters.
The p190 D / p193 A relay request supplies a complete 94-letter comparison
after explicitly aligning its `FUR` / `FUER` wording difference.

See the [readable case](../../cases/pages/190.md#edition-cases-radio-nov14-radio-retransmissions),
[literal inputs and key provenance](inputs.json), and
[full coordinate certificate](certificates.json).

## Exact scope

| Record | Published key | Printed slots | Fixed raw positions | Editorial coordinate changes / fills |
| --- | --- | ---: | ---: | ---: |
| p190 A | Nov13–15b | 236 | 117/118 | 3 / 0 |
| p190 B | Nov13–15b | 176 | 82/88 | 5 / 5 |
| p190 E | Nov13–15a | 176 | 82/88 | 1 / 6 |
| p194 B | Nov13–15a | 280 | 139/140 | 1 / 0 |
| p190 D | Nov13–15a | 186 | 92/93 | 2 / 0 |
| p193 A | Nov13–15b | 188 | 88/94 | 15 / 3 |
| p193 B | Nov13–15a | 195 | 54/140 before witness; 139/140 after | 0; 85 prefix slots supplied by p194 B |

The total is **1,437 printed source slots**, **1,423 valid coordinate letters**
and **654/761 fixed raw positions** before the p193 B prefix restoration.
The 761-position total includes that fragment's explicitly modelled full
280-coordinate frame. The independent copy adds 85 fixed raw positions,
bringing this total to **739/761**. These totals include the garbled letters
that appear in the unmodified decryption. The 195-slot interrupted source
remains intact; its 85 absent prefix slots have their own witness map.
No historical square is completed or relabelled.

Five printed dashes in p190 B form a whole received group; they are not
silently dropped. In p190 E, three unreadable glyphs, a visible A/X overstrike,
and the invalid printed letters Q and T are preserved as uncertain slots.
Both A/X alternatives are decrypted in the certificate. The displayed
candidate uses X, which is one of those visible alternatives.

## Cross-key findings

For the backup-station request, **87 of 88 candidate letters** have a complete
observed coordinate pair in at least one copy. Only the S in `SEWASTOPOL`
remains an editorial choice: p190 B directly decrypts V there; p190 E retains
one coordinate half but has an invalid Q as the other source glyph. The
readable candidate encrypts exactly to each separately repaired ciphertext.

For the relay request, **all 94 letters** of the longer readable template
have complete observed pairs in at least one source. The shorter text's
`FUR` is aligned with the longer text's `FUER`; both ciphertext lengths are
retained. The complete pilot notice matches all 195 received coordinates of
the interrupted p193 B source, beginning at source index 85 of p194 B. Only
the preceding 85 coordinates are supplied from the complete witness. The
literal `SOLDLTENRATS` garble and the unresolved name cell are preserved.

For the arrival notices, the uncertain name symbol is cell `FX` under
Nov13–15b and cell `DG` under Nov13–15a. Assuming the same correctly copied
name reduces their common domain to **234789QY**. Restricting the name to
letters still leaves **Q or Y**. The plausible spelling `FRYE` is recorded as
a proposal, with no independent identification and no key assignment.
All eight common-domain choices re-encrypt exactly under their corresponding
conditional cell fills, so re-encryption cannot choose between them.

## Reproduction

```sh
python experiments/nov14_retransmissions/verify.py --verify
python experiments/nov14_retransmissions/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier independently inverts columns by their offsets, cross-checks the
project cipher implementation, checks each raw domain, reconstructs every
declared coordinate repair, and verifies the cross-key comparisons and exact
suffix restoration. The
optional PDF argument checks its byte count and SHA-256 and rerenders every
saved crop for pixel equality. It requires PyMuPDF and Pillow; the ordinary
verification uses only the Python standard library.
