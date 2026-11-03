# Recall of the Turkish military mission

ADFGVX Cipher — **icekylinx and GPT-6 Astra Pro**.

This edition covers **p130 A1–A2 and p131 A3–A4**, a four-part order with
the shared header `OSM v OUI (8.25 p.m., November 5th); #12 2015 4 TEILE`.
It concerns contract-bound military-mission members, including those
already under notice of termination, and cites a contract provision for
their recall to the army upon publication of Turkey's armistice. The
mission is to arrange return and require arrivals to report their
whereabouts. The [case](../../cases/military/turkish_mission_recall.md)
retains the complete received text.

One received office field, **`MILIGRHYU`**, remains unresolved. All its
square labels are fixed, but a fixed label is not a resolved word. The
edition makes no forced expansion to `MILIKABT` or another abbreviation.

## Source recovery and conservative edits

The source has **394, 330, 396 and 170 valid coordinates**, exactly matching
the four indicators. Earlier OCR omitted the complete `VGVVF` group from
A1 and merged A3 with A4. Correcting those source readings and following
the printed boundaries yields **645 fixed plaintext labels**.

| Part | Plaintext positions | Observed-coordinate substitutions | Erasure fills |
|---|---:|---:|---:|
| p130 A1 | 197 | 0 | 0 |
| p130 A2 | 165 | 2 | 0 |
| p131 A3 | 198 | 0 | 0 |
| p131 A4 | 85 | 1 | 0 |

The two A2 changes repair `MESIRTIKELS` to `DESARTIKELS`. The single A4
change repairs `WUF` to `AUF`. No coordinate is inserted, deleted or
filled, and no key cell or rank is changed.

The received forms `MILITAERMISZION`, `EINSCHLISZLICH`, `ABESCHLOSZENEN`,
`ZURUCKBERUFEN` and `ZUGEGEBENENEN` remain untouched. Apparent omitted
letters and duplicated syllables are documented, not silently supplied.
The article label `10` and all reference digits are unchanged.

## An earlier closing as independent support

The entire **58-character** A4 candidate closing is identical to the
fully observed raw closing of already-catalogued **p149 A2**:

```text
AUFALLERHOECHSTENBEFEHLCHEFMILITAERKABINETTSFRHRMARSCHALLX
```

The verifier independently decrypts that earlier source and checks every
pair in the shared closing. It also verifies the earlier crop hash and,
with `--pdf`, its pixels. This supplies a witness for the one-letter
`WUF→AUF` repair. The rest of p149 A2 concerns Osthoff; the whole messages
are not assumed to be retransmissions, and the old record contributes
**zero** new catalog entries. `FRHR MARSCHALL` remains a received
signature without an independent personal identification.

## Attribution and limits

The unchanged Nov4–6 key is previously published. A2 already had a
readable unreviewed repository candidate; A1 had a defective OCR length,
and A3/A4 were merged. Prior outputs are frozen in the inputs. Bounded
paper, dissertation and cached comment-thread checks did not locate an
explicit discussion of this body; no first historical decipherment
claim is made.

The message cites article 10 of a contract associated with Liman von
Sanders. This edition reproduces that citation; it does not authenticate
the underlying contract or prove completed return of the personnel.

## Reproduce

```bash
python experiments/turkish_mission_recall/verify.py --verify
python experiments/turkish_mission_recall/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier checks independent transposition mappings, all repairs,
exact re-encryption, unchanged odd words and numbers, source assembly
and the earlier closing witness. The optional PDF check reproduces the
crop pixels. The four proposed catalog rows are separate from the
shared catalog.
