# Romanian ultimatum and Danube crossing: companions of p176a

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Three readable parts of a six-part message are source-edited here:
**p175 C1**, **p175 C2**, and **p176 A5**. They report a Romanian-government
ultimatum, French forces beginning a Danube crossing near Rustschuk, and
messages and material being directed first to Hermannstadt. Read the
[case](../../cases/pages/175.md#edition-cases-military-romanian-ultimatum-companions) for the raw
and candidate texts and the limits of the historical interpretation.

The complete source-defined sequence is preserved without treating
every surviving part as readable:

| Source part | Status | Included in the new readable-record total? |
|---|---|---|
| p175 C1 | Native 212-slot frame; readable candidate | Yes |
| p175 C2 | Native 208-slot frame; two occurrences of one unknown time digit | Yes |
| p175 C3 | 217 literal slots against advertised 222; loss location unknown | No |
| p176 A4 | Existing **p176a** challenge; prior Norbert/Max Baertl reconstruction | No |
| p176 A5 | Native 168-slot frame; one printed erasure remains | Yes |
| p176 A6 | 160 printed slots, including 86 dashes; body unread | No |

Childs explicitly continues p175 onto p176. Both headers read
`LP v NKJ (5.40 p.m., November 10th); VON UKS KR 0915 (10/11) 6 TLE`.
The part numbers and headers establish the source assembly. They do
not independently establish every letter of the prior p176a proposal
or provide the unknown content of C3 and A6.

## Source certificate and exact costs

[inputs.json](inputs.json) preserves every literal row, including the
unread parts, the original PDF identity, and seven crops with their PDF
page numbers, rectangles and hashes. Printed pp175–176 correspond to
PDF pp178–179. The published **Nov10–12** square and ranks are unchanged.
Each printed dash occupies one source coordinate; no gap, deletion or
reordering is added to the three readable parts.

| Part | Printed slots | Valid coordinates | Plaintext positions | Raw fixed | Candidate fixed | Known substitutions | Printed-dash fills |
|---|---:|---:|---:|---:|---:|---:|---:|
| p175 C1 | 212 | 209 | 106 | 103 | 106 | 2 | 3 |
| p175 C2 | 208 | 208 | 104 | 102 | 102 | 1 | 0 |
| p176 A5 | 168 | 163 | 84 | 79 | 83 | 3 | 4 |
| **New readable records** | **588** | **580** | **294** | **284** | **291** | **6** | **7** |

The remaining printed dash is A5 source index **50**. Fixed counts are
published-square labels under the stated frame and candidate repairs;
they are not counts of independently established historical characters.
The candidate wording is an editorial choice. Exact reproducibility
and a low edit count do not prove that it is the only possible original.

All indices below are zero-based:

| Part | Observed-coordinate substitutions | Printed-dash fills |
|---|---|---|
| p175 C1 | 136 A→D; 191 V→X | 137→F; 138→D; 139→A |
| p175 C2 | 1 X→A | None |
| p176 A5 | 58 G→F; 108 X→D; 120 A→D | 51→F; 52→G; 53→D; 54→A |

[certificates.json](certificates.json) maps every plaintext pair to its
literal source coordinates, gives its full domain, preserves the raw
reading, and records every changed pair. An independent column-offset
inverse is compared with the project cipher implementation. The complete
C1 candidate re-encrypts exactly. The partial candidates receive the
finite compatibility checks below.

## What the unresolved fields allow

C1 retains `JUDORT`, `1XAX11212OM` and the repeated `24X24` exactly. No
reference number is normalized, and the repeated hour-like field is
not added together to manufacture a different duration.

In C2, plaintext positions **43 and 45** are both pair **GF**, each with
domain **56789**. The two time digits therefore agree under one unchanged
key. Enumerating all **120** injective completions of the five unknown
square cells gives **five** literal candidate plaintexts, with **24**
completions for each equal-digit pair. It does not give 25 independent
hour combinations or select a historical hour.

A5 ends in `VERPFLEG?ZXUND`. Position **78** has pair **?G**, using the
unfilled printed dash at source **50** and observed source **136**.
Its domain is **56789JQSUZ**. The anomalous following `Z` is retained.
No grammatical continuation or expansion of the abbreviation is
supplied. Enumerating six possible values for the missing coordinate
under all 120 square completions gives **720** complete cipher/key
witnesses and **10** distinct literal plaintexts. Each complete witness
re-encrypts to its explicitly completed candidate ciphertext. These
are compatibility witnesses, not additional source observations or
historical completions.

The certificate records counts, an ordered enumeration digest and one
complete witness per distinct literal plaintext. No baseline key cell
or remaining printed erasure is selected from these alternatives.

## Unread context and earlier credit

`contextual_unread_records` in the inputs, and
`contextual_unread_records_excluded_from_summary` in the certificate,
hold C3 and A6 outside all readable-record, coordinate and character
totals above. C3's five-coordinate arithmetic shortage has no selected
location or full frame. A6 has only 74 observed coordinates and receives
an unfilled native-frame domain diagnostic; no readable body is claimed.

Part A4 is the existing [p176a case](../../cases/pages/176.md#edition-cases-p176a), with earlier
credit to **Norbert, 2 March 2017, comment 26**, and **Max Baertl,
11 March 2017, comment 39**. Its proposed breakthrough text, block
repairs and extra editorial corrections remain distinct. The new
companions do not independently validate its absent coordinates.

The paper and thesis discuss a different thirteen-part Mackensen report
from 3 November. Shared geographical context does not establish an
identical plaintext. The bounded explicit-body check is documented in
`inputs.json`; its negative result is not a priority claim.
[prior_candidates.json](prior_candidates.json) freezes the earlier
unreviewed C2 and A5 readings and C1's shorter, garbled OCR-derived frame.

## Reproduce

From the repository root:

```sh
python experiments/romanian_ultimatum_companions/verify.py --verify
python experiments/romanian_ultimatum_companions/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The first command uses the standard library and repository code. The
optional PDF check requires PyMuPDF and Pillow, checks the full PDF
size and hash, and verifies each saved crop against the exact rendered
RGB pixels. Temporary screening caches are not needed for replay.

### Header transcription correction

The enlarged [C3 header](sources/p175_C3_heading_detail.png)
reads **RICHI-222**. An initial reading of 232 was rejected. With 217
literal slots, the unlocated shortage is **five coordinates**. The former
15-coordinate estimate is retained only as a transcription-error note,
not as a source model or an alternative restored body. The three readable
records and their repair counts are unchanged.

The separate [C3 withdrawal follow-up](../p175_c3_gap_followup/README.md) now
provides a conditional reading and compares contiguous-block and arbitrary-loss
models. This package retains its original three-record scope and unchanged
source/certificate files; A6 remains unread.
