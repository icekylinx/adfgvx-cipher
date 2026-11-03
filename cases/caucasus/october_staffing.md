# October staffing, manganese purchases and service traffic

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[All cases](../README.md) · [ADFGVX Cipher](../../README.md)

**Status:** Six source-reviewed records under the previously published
**Oct4–6 key**. The principal result is a two-part Bavarian personnel order;
four other records concern Tiflis unit information, medical retransmission,
manganese purchases and a telegram acknowledgment. Source review:
**icekylinx and GPT-6 Astra Pro**. Earlier key credit belongs to **J. Rives
Childs**, **George Lasry**, and **Lasry–Niebel–Kopal–Wacker**.

All six printed frames have their advertised lengths. Across 1,264 received
slots, the raw key inverse fixes 630 of 632 plaintext positions. The edition
uses **four explicit known-coordinate substitutions and two erasure fills**;
626 proposed characters need neither. The
[reproducible source package](../../experiments/october_staffing/README.md)
contains every source row, domain, coordinate origin, edit and re-encryption.
There is no new key claim or proposed p73 plaintext.

## p66 C1 and p67 A2 — Bavarian command appointments

The source explicitly joins these parts: both carry `NR40 DEUTSCHE DELEGATION
KAUKASUS1723(5)2TLE`, with `1TL RICHI-286` on p66 and `2TL RICHI-220` on p67.
Both travel `COS v NKJ`; the reception times are 03.15 and 03.21 a.m. on
October 6. The page heading is October 5, and the shared origin field is
`1723(5)`.

**Most likely German reading, with abbreviation and reference fields retained:**

**Readable German:**

> Oberst und Kdeur des 4. bayr. Chev.-Regt., Graf von Seyboltstorff, als
> Kdeur der 4. bayr. Kav.-Brig. bestimmt, ist sofort zu dieser Brig. zu
> beordern. Abreisetag umgehend drahten.
>
> Als Ersatz ist bereits Oberstlt. Karl von Grundherr, röm.I, des 4.
> Chev.-Regts dorthin beordert. Bayr. Kriegsministerium Nr 249774P.

**Display notes:** Abbreviations remain abbreviated. The displayed `röm.I` renders the literal name discriminator `ROEM1`; it is a formatting interpretation, not an additional unit number or a new personal identification.

The order directs the named colonel to the 4th Bavarian Cavalry Brigade and
requests the departure date. The second part says that the named lieutenant
colonel has already been ordered there as the replacement. Both brigade and
regiment numerals **4**, `KARLVONGRUNDHERR`, and the name discriminator `ROEM1`
are directly fixed by the received coordinates. The text alone does not locate
the brigade or identify a later telegram's unknown brigade numeral.

The raw first part spells the surname `SEYBOLTSTORF0`; its final `0` becomes
`F` through one coordinate substitution. The second part has `BEORSERT`;
`BEORDERT` costs one coordinate substitution. The reference `249774P` is
preserved without adding punctuation or interpreting its final character.

The institutional
[SLUB catalogue](https://katalog.slub-dresden.de/en/id/0-165780514X) records a 1922
history of the 4th Chevaulegers with contributors **Karl von Grundherr** and
**August Graf von Freyen-Seyboltstorff**. This supplies bibliographic support
for the names. Its linked WLB scan was unavailable to automated access during
this review; no command date or troop movement from that book is asserted.
The telegram's shorter surname form remains the form used in the reading.

Sources: [p66 C1](../../experiments/october_staffing/sources/childs_p66_C1.png)
and [p67 A2](../../experiments/october_staffing/sources/childs_p67_A2.png).

## p67 B — Suspend further manganese-ore purchases

Header: `COS v NKJ (10.32 p.m., October 5th); NR48 1916(5); RICHI-224`.

**Readable German:**

> An BV.K.M.KA Tiflis. Weitere Käufe Manganerze bis auf Weiteres
> unterlassen. Rittm.[F]ischer, Comm[i]ssar des Kriegsministeriums.

**Display notes:** `[F]` in the surname and `[i]` in `Comm[i]ssar` are proposed fills of two printed erasures. They are not abbreviation expansions. The former remains a name proposal; the latter is an ordinary-word completion. Their different evidential force is retained below.

The instruction to stop further manganese-ore purchases is directly fixed;
it requires no known-coordinate substitution. The address abbreviation
`BVXKXMXKA` remains unexpanded. The two printed dashes are in one source group,
`AAG--`, and affect separate plaintext positions.

The first signature letter has raw domain **`0BDFXZ`**. `[F]ISCHER` is the
proposed surname, not a uniquely recovered or independently identified person.
The other domain is **`3CIRUW`**, filled with `I` for `COMMISSAR`. Both are
explicit erasure fills. The raw signature is
`RITTMX?ISCHERCOMM?SSARDESKRIEGSMINISTERIUMS`.

Source: [p67 B](../../experiments/october_staffing/sources/childs_p67_B.png).

## p66 B — Repeat the garbled medical telegram

Header: `--- v NKJ (3.11 a.m., October 6th); DEUTSCHE DELEGATION KAUKASUS
1812(5); RICHI-284`.

**Readable German:**

> An leitenden Sanitätsoffz. Dortiges Telegr. Nr 131X232 ist verstümmelt.
> Bitte nochmals drahten. Armeearzt Oberkommando Besatzungsheeres Rumänien
> Nr 8586X3.

The recipient is asked to retransmit a garbled message. The raw text has
`DORTIGZS` and `BESATZUNGSHEERZS`; the edition changes each `Z` to `E`, costing
one received-coordinate substitution each. All numerals are directly fixed.
`131X232` and `8586X3` remain literal reference fields; the edition does not
turn the former into a date.

Source: [p66 B](../../experiments/october_staffing/sources/childs_p66_B.png).

## p66 A — An abbreviated Tiflis unit response

Header: `ASO v NKJ (9.27 p.m., October 5th); COS1615(5); RICHI-190`.

This record is fully determined, with no edit or fill:

**Raw output:**

```text
KDTURXTIFLISXXZUDORTXNRX80XREITXABTLGXBAYRX5OHNEERSTEBATTXBEIBXKXBXGEGENXKIEWXXGXUVXSEWASTOPOLX
```

A conservative division into words is:

**Readable German:**

> Kdtur. Tiflis. Zu dort Nr 80. Reit. Abtlg. Bayr. 5 ohne erste Batt. bei
> B.K.B. gegen Kiew. G.U.V. Sewastopol.

It addresses the Tiflis commandant's office, cites No. 80, and connects an
abbreviated mounted unit and battery exception with Kiew and Sewastopol. The
literal `5`, `BEIBXKXBX`, and `GXUVX` are preserved. No exact regiment, expanded
brigade designation, added verb or movement order is inferred from these
abbreviations.

Source: [p66 A](../../experiments/october_staffing/sources/childs_p66_A.png).

## p67 C — Telegram acknowledgment and a separate clear instruction

Header: `NKJ v OSM (--.-- October 7th); 2030; RICHI-60`. The sheet remains
headed October 5; no origin day is printed in this record's own `2030` field.

The 60 coordinates directly fix all 30 plaintext characters:

**Raw output:**

```text
TELXREISENOX1AVOM20X9XERHALTEN
```

A conservative reading is “Tel. Reise No. 1A vom 20.9. erhalten.” The exact token
`REISENO` and the reference `1A` remain visible; the interpretation does not
add an unprinted destination or sender.

The source separately prints **`BITTE JETZT ODER RAT ZU QUITTIEREN`** beneath
the ciphertext. This is a clear service instruction asking for acknowledgment;
it is not the plaintext of the 60-coordinate body. `RAT` remains unexpanded.

Source: [p67 C](../../experiments/october_staffing/sources/childs_p67_C.png).

## Explicit repair ledger

Source indices below are zero-based; group and character numbers are one-based.
The complete certificate also gives the plaintext positions and both received
coordinate origins.

| Record | Source index | Printed group / character | Proposed coordinate | Purpose |
| --- | ---: | --- | --- | --- |
| p66 B |11 |3 /2 |`G→F` |`HEERZS→HEERES` |
| p66 B |41 |9 /2 |`G→F` |`DORTIGZS→DORTIGES` |
| p66 C1 |251 |51 /2 |`F→V` |Final surname `0→F` |
| p67 A2 |106 |22 /2 |`F→G` |`BEORSERT→BEORDERT` |
| p67 B |118 |24 /4 |`?→V` |Proposed `[F]ISCHER` |
| p67 B |119 |24 /5 |`?→X` |Proposed `COMM[I]SSAR` |

The literal source is unchanged in every record. The proposed texts and their
re-encrypted witnesses are separate certificate fields.
