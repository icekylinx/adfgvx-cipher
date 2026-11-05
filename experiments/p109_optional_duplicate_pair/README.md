# A literal duplicate-pair alternative for p109 D

[Reading conventions](../../docs/reading-conventions.md)

**Source comparison and verification: icekylinx and GPT-6 Astra Pro.**

The original p109 challenge has a simple alternative source repair: remove
one of the two consecutive copies of **XXAXA DDVVV**. This retains 248 of
D's 258 printed coordinates, makes no substitution or fill, and gives a
complete 124-label raw reading under **Nov1–3**. The independently received
B witness then agrees at **204 observed coordinates** and disagrees at
**38**, compared with 200 agreements and 42 disagreements under the earlier
D repair.

The gain is narrow. Two ordinary-word labels improve, while the river's
last label and the footer also change. The complete older editorial
candidate still costs **23** observed-coordinate changes in D under either
geometry. This supplement does not turn p109 into an unedited historical
plaintext or replace its [earlier credited edition](../../pages/109.md#edition-cases-p109).

## The two sources and the retained older reading

[Childs, printed p109](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)
contains two related reports with different headers. The existing
[B image](../../sources/excerpts/childs_p109_B.png) prints `UKS v ZÖN`,
`11.03 p.m., November 3rd`, `VEVE 1715 AN LP UD 2130` and `RICHI-248`.
Its 248 slots contain six printed erasures. The
[D image](../../sources/excerpts/childs_p109_D.png) prints the same station
route, `0.35 a.m., November 3rd`, `Beginning jammed` and `RIZI-258`.
All 258 D coordinates are visibly present.

Both images and the complete p109 page were inspected. D's groups 14–17
read **XXAXA DDVVV XXAXA DDVVV**, at original coordinates 65–84. Neither
copy is visibly cancelled. The complete source strings and header snapshots
are retained in [inputs.json](inputs.json). The repeated pair provides a
physical reason to test this geometry; it does not prove a historical
transmission or transcription duplication.

**Raw output — unchanged native B, including every unresolved position:**

```text
OX?XMXABENDM?LUNGXSAV?5UEB0RG4V?LA5ZTERXALLEBEENDETXHNEITAREFDLXD?VXIMEARSCHAUFBML7RADERKANNTXSONSTKEIVMEREIGNIXSE?XAXOXKX16
```

[Norbert's 2017 reading](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1#comment-852658)
reduces original source 75:95 from `XXAXADDVVVXXFXVDVDDG` to
`XXAVVXXDDG`. Its 248-coordinate result and all earlier published wording
remain unchanged in the primary case and original certificate.

**Recomputed prior reading — unchanged body under Norbert's recorded repair:**

```text
OXKXMXABECDPELUNGXS4V4XUMBJRGA8GLETZTEVTVILEBEEVUETX1WEITEDEFDUXNIV5IMMARSCH4UFBELGRADERKAVV2XSONSTKEINEEDMILNISSEXXASOXK511
```

## Duplicate-only geometry

The representative alternative excludes source **65:75**. Excluding
**75:85**, the other complete copy, gives the same retained ciphertext.
The ranges are zero-based and end-exclusive. Both complete-copy maps and
all ten excluded observed coordinates are retained separately.

**Raw output — optional duplicate-only D frame, with no coordinate substitution or fill:**

```text
OXKXMXABECDMELUNGXS4VMXUMBJRGA8GLETZTEVTVILEBEEVUETX1WEITEDEFDUXNIV5IMMARSCH4UFBELGRADERKAVV2XSONSTKEINEEDMIGNISSEXXAXOXK511
```

Only four labels differ from the earlier D raw body:

| Plaintext index | Earlier raw | Duplicate-only raw | Consequence |
| ---: | --- | --- | --- |
| 11 | `P` | `M` | `ABECDPELUNG` becomes `ABECDMELUNG`. |
| 21 | `4` | `M` | The damaged river field becomes `S4VM`; no vowel is directly recovered. |
| 108 | `L` | `G` | `EDMILNISSE` becomes `EDMIGNISSE`. |
| 117 | `S` | `X` | The literal closing becomes `AXOXK511`. |

The earlier `ASOXK511` and the B closing `AXOXKX16` remain distinct.
No closing is expanded into an office, serial or calendar interpretation.
Because adjacent equal symbols extend the identical-stream ambiguity,
**13** consecutive ten-coordinate deletion starts, 65 through 77, produce
this same retained ciphertext. The two complete duplicate-copy deletions
are the clearest physical descriptions, not a uniquely identified error.

## Selection from B's coordinates, with no German target

A dynamic program compares every ten-exclusion ordered subsequence of
original D with B's known coordinates. Erasures in B cost zero, but their
surviving partner coordinates remain in the comparison. No proposed German
word, dictionary or target plaintext participates in this optimization.

| Comparison scope | Earlier repaired D disagreement | Exact minimum | All tied source descriptions | Distinct raw D streams |
| --- | ---: | ---: | ---: | ---: |
| Every known B coordinate | 42 | 38 | 118 | 4 |
| B body only, plaintext 6:114 | 39 | 36 | 318 | 32 |

Both complete-copy deletions attain each minimum. The body-only run excludes
the leading fields and the distinct closings before selecting D geometry.
It therefore supplies a check that the improvement is not entirely due to
forcing the endings to agree. All minimum descriptions, complete raw
streams and their exact consensus are stored in
[certificates.json](certificates.json); none is discarded for sounding
ungrammatical.

The four full-B minimum raw streams differ at plaintext position 41,
where the word fragment can be `TVILE`, `TVULE`, `TV9LE` or `TVFLE`.
Their counts are respectively 66, 22, 24 and 6 source descriptions. The
common-plaintext comparison is conditional: different timestamps and
endings leave the exact historical relationship of B and D unresolved.

## SAVE and SAVA under this geometry

The same-key, separately received [p99 B1 report](../../pages/099.md#edition-cases-military-sava-crossing-evening-report)
contains the exact native token **SAVE**, with no source exclusion, fill
or coordinate change. Its [source image](../nov1_contact_mail_and_sava/sources/p99_B1.png)
was inspected again. The four pairs and their original-source positions are
redecoded in this supplement. It attests the spelling in this traffic,
without identifying p99 as a copy of p109 or importing its unit numbers.

| Proposed river spelling | Changes in B | Changes in older repaired D | Changes in duplicate-only D |
| --- | ---: | ---: | ---: |
| `SAVE` | 0 | 3 | 2 |
| `SAVA` | 1 | 2 | 3 |

The older geometry gives equal combined cost, three, for either spelling.
The duplicate-only geometry instead gives combined costs **two for SAVE**
and **four for SAVA**. This is a geometry-conditioned preference, not a
direct observation of the final `E`. `SAVE` still spends one change above
the local common-source minimum. The two earlier spellings remain visible.

## A separately priced full reading

The following optional edition reuses the ordinary words of the existing
p109 editorial candidate, selects `SAVE`, and retains this frame's literal
`AXOXK511` closing. It preserves the raw leading field, the raw numeral `1`
and every closing label. Its source-like spelling `ABENDMELUNG` remains;
no additional `D` is inserted to normalize it to *Abendmeldung*.

It requires **21 observed-coordinate substitutions in D**, beyond the ten
source exclusions. Comparing the same complete candidate with B requires
21 substitutions and six printed-erasure fills. These B fills are a
candidate comparison, not additional received evidence. All changes have
exact original-source maps in the certificate.

**Edited output — optional 124-label reading under ten explicit source exclusions and 21 further D substitutions:**

```text
OXKXMXABENDMELUNGXSAVEXUEBERGANGLETZTERTEILEBEENDETX1WEITEREFDLXDIVXIMMARSCHAUFBELGRADERKANNTXSONSTKEINEEREIGNISSEXXAXOXK511
```

**Readable German — complete optional edition, preserving every literal separator and reference:**

> O X K X M X Abendmelung X Save X Uebergang letzter Teile beendet X 1 weitere fdl X Div X im Marsch auf Belgrad erkannt X sonst keine Ereignisse XX A X O X K511.

**Conditional interpretation:** The proposed body reports completion of the
last elements' crossing of the Save/Sava, another enemy division moving
toward Belgrade, and no other incidents. These are the earlier credited
body interpretations under a different explicitly recorded source repair.
The numeral and command/reference labels remain literal; the new geometry
does not independently establish their historical meanings.

The candidate's combined known-coordinate cost is 42, four above the
minimum 38 for this pair of frames. The extras are one for `SAVE`, two for
`UEBERGANG` and one for `TEILE`. Thus the familiar fluent reading still
requires choices beyond combining the two witnesses. The original full
`SAVA`/`ASOXK511` candidate remains at 23 changes in D under both geometries;
this alternative must not be described as a blanket reduction of every
old editorial cost.

## Reproduce and preserve the earlier edition

The verifier binds the unchanged core data, earlier p109 record and primary
case displays; replays both complete-copy exclusions; checks all B-only
minima and both complete roundtrips; verifies the 21-change ledger, all six
B fills and the native p99 word witness; and retains every uncertain
numerical/reference field. Its optional PDF check recreates the reviewed
full-page pixels and the p99 witness crop. No new image or physical-source
count is introduced.

```sh
python experiments/p109_optional_duplicate_pair/verify.py --verify
python experiments/p109_optional_duplicate_pair/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

The current work is an alternative source reconstruction and conditional
comparison by **icekylinx and GPT-6 Astra Pro**. Norbert retains the original
target-reading credit, and the earlier editorial proposals and the prior
multi-witness decoder retain their existing attribution and limits.
