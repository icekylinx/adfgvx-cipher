# p167 C1 — Mission and Nachrichtenchef service address

The surviving first part contains a mission address and a Nachrichtenchef routing or signature field. Damaged institutional labels prevent a more precise identification.

**Complete edition by printed page:** [p. 167](../pages/167.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Partial recovery and source review: icekylinx and GPT-6 Astra Pro.**
The native 132-coordinate first part addresses a mission and carries a
Nachrichtenchef routing/signature field. The opaque labels `MILB`, `0RM`
and `RELA` remain literal; no particular institution or location is identified.

## Conditional digit reading

The [shared Nov7–9 reference interpretation](../../experiments/nov7_9_joint_digits/README.md) reads **Roem 5; KR 130615**, completing **66/66 conditional edited labels**. The opposite assignment gives Roem 6; KR 130516. All three affected pairs are originally observed. The six word substitutions and two printed-mask fills are unchanged, and the labels MILB, 0RM and RELA remain literal.

## p167 C1

**Readable German — primary word proposal; six observed-coordinate substitutions and two printed-mask fills; three unresolved positions retained:**

> An MILB Mission. Abtlg 0RM. 10. RELA. Nachrichtenchef. Roem ?. KR 130?1?.

The readable content is an address/service fragment, with `MISSION`, `ABTLG`
and `NACHRICHTENCHEF` as explicitly priced word repairs. Only the first part
of the header's two-part transmission is identified here.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 132-slot frame, unchanged Nov7–9 key; 61/66 fixed labels:**

```text
ANMILBMIFLIONXA?TLG0RMX10XRELAXXNACHUIC0TENC?EAXROEMX?XKRX130?1?XX
```

**Edited output — same native frame; six observed substitutions and two printed-mask fills; 63/66 fixed labels:**

```text
ANMILBMISSIONXABTLG0RMX10XRELAXXNACHRICHTENCHEFXROEMX?XKRX130?1?XX
```

</details>

The six observed changes are source **20 D→X, 23 D→X, 83 V→D, 84 D→X,
114 V→X, 126 X→D**. Source **14** is a printed dash filled as `G`;
source **90** is the literal invalid `Z`, filled as `X`. The `B` proposal
in `ABTLG` therefore needs both a mask fill and an observed-coordinate change.
No slot is inserted, excluded or reordered, and the published square is
unchanged.

## Linked unknown fields

The three question marks use two distinct unknown square cells:

| Field | Exact dependency |
|---|---|
| After `ROEM` | alpha, pair `XA` |
| Reference `130?1?` | `130 beta 1 alpha`; beta is pair `VF` |

Under the published partial square, alpha and beta take `5` and `6` in
opposite orders. The two complete-square witnesses are `ROEM 5 / KR 130615`
and `ROEM 6 / KR 130516`. They prove compatibility of these literal label
assignments under the published partial square. The conditional reference
comparison above supplies a separate documentary basis for choosing 5/6.

An optional interpretation of the `B` in `MILB` as separator `X` costs two
further observed substitutions: **13 G→V** and **113 X→V**. Its total is eight,
with the same two mask fills. The primary edition retains `MILB`.

## Source

Childs, printed p167 / PDF p170, section C1, `RICHI-132`. The page heading is
`9th NOVEMBER, 1918.` The header reads
`C) NKJ, YZ, WAU v LP (03.21 a.m., November 10th)` and
`AS MOM 2015 NKJ AS 15 MINS. (9/11) 2 TLE; 1 TL`.
The literal `MOM` and the service notation are preserved.

<details>
<summary>Literal source transcription</summary>

**Source transcription — all 132 native slots; the dash and invalid Z are literal:**

```text
AXVXX VFGDD GVVG- VVDVV DDDDX AGVGD DAAXG AVGDV
XFAVD AVDXV FVVVA GAAXA XGDDD GFGVG GVGDG DVVVD
FVDVD DDDDD ZVVGX FVVFF GVFXF XXGDV GVVXV VXVGV
DVXVF DXDDF AF
```

</details>

[Original source PDF, p170](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)
· [Reproduction and provenance](../../experiments/p167_mission_address/README.md)
· [Per-position and global-completion certificate](../../experiments/p167_mission_address/certificates.json).

The unchanged period key comes from George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker, and Lasry's 2017 key list. The earlier unreviewed OCR block is
preserved. The source transcription, word proposals and linked-field audit
are by **icekylinx and GPT-6 Astra Pro**.

</details>
<!-- CASE-EDITION:END -->
