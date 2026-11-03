# p137 B — Query about the station's former staff

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Recovery and source review: icekylinx and GPT-6 Astra Pro.** A conditional
group-movement and three-loss reconstruction exposes a query about whether
the station is still staffed by its former personnel, followed by a request
to answer and the closing name Eilvese.

## p137 B

**Readable German — conditional 138-slot frame; three observed substitutions, two printed-mask fills and two inserted-slot fills; time unresolved:**

> Ist dortige Station noch vom alten Personal besetzt? Antwortet um `17?0`. Eilvese.

The question mark after *besetzt* is editorial punctuation. The question mark
inside `17?0` is one unresolved plaintext position, retained literally.

**Raw output — primary conditional 138-slot frame, before substitutions and fills; 64/69 fixed positions:**

```text
ICTDORTIGEVTATIONN?CHVOMALT?NPERSONALBESETZTXANTWO?TETUM17?0XEILBES?X
```

The source prints **135 slots**, including two dashes, against `RIZI-138`.
The primary model moves the last printed group `VDF--` (source 130–134) to
retained-stream boundary 105, the beginning of the final printed row. It
then appends three unknown coordinates to reach the advertised length.
All 135 source slots remain represented once; none is excluded. The movement is part of the stated reconstruction.

For the fixed 69-position proposal, exact integer pricing compares **481,032
maps**: each of 27 printed groups, each of 131 destinations after removal,
and each of 136 boundaries for the three missing coordinates. The minimum
is three observed substitutions. Exactly **five maps** attain it: source
group 130 moves to boundary 103, 104, 105, 106 or 107, and all three missing
slots follow the resulting 135-slot stream. Every minimum gives 64/69 fixed
raw positions and the same 68/69-position edited proposal. The certificate
retains all five alternatives; boundary 105 is the primary display because
it coincides with a printed group and row boundary.

**Edited output — same primary frame; three observed substitutions, two printed-mask fills and two inserted-slot fills; 68/69 fixed positions:**

```text
ISTDORTIGESTATIONNOCHVOMALTENPERSONALBESETZTXANTWORTETUM17?0XEILVESEX
```

| Primary repair or frame operation | Exact account, zero-based indices |
|---|---|
| Source group movement | Source 130–134 to retained-stream boundary 105 |
| Missing coordinates | Three unknown slots appended at model 135–137 |
| Observed substitutions | Source 130 `V→F`, 131 `D→G`, 132 `F→X` |
| Existing printed-mask fills | Source 133 `-→A`, 134 `-→F` |
| Inserted-slot fills | Model 135 `?→V`, 137 `?→F` |
| Retained uncertainty | Model 136 unassigned; plaintext 58 has domain `036OQY` |

The three changes include all three observed coordinates of the moved group
in this primary layout; the movement does not conceal their price. The
other 130 observed coordinates remain unchanged. Each of the six possible
labels at plaintext 58 has a complete exact re-encryption witness under the
same unchanged global key. The primary edition retains `17?0`.

The independent [p127 personnel notice](nov4_personnel_transmission_notice.md)
contains `HIER NOCH ALTES PERSONAL` and says transmission continues as
agreed. Its subject is compatible with this query. Its LP/NKJ route differs
from OSM/OUI here, and neither source explicitly identifies the other: this
is topical context, with no copied coordinates or proved reply relationship.

## Source and reproduction

Childs, printed p137 / PDF p140, section B. The page heading is
`6th NOVEMBER,1918`; the receipt line instead says November 5. The clear
continuation, advertised length and footer below are contextual annotations,
outside the 135 ciphertext slots.

**Source transcription — full header, all 135 cipher slots and clear footer:**

```text
B) OSM v OUI (14.58 November 5th)
CONTD HIER SS NR 10 - 11.00
RIZI-138
FVGDG XVAVX AAFAG AXGXA ADXAV AGAXA AGAGF
XAGDX GFFXF XXXVV XXXVX DFXAG AVAFD AVAVG
AAFXF XXXXA FDAXD XXVAV VAVGX AGGAX GFAXF
FFAFX XXAFF AADAA XVFDX XXFGA VDF--
OSM
V OUI
```

[Original source PDF, p140](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)
· [Reproduction and source recipe](../../experiments/p137_station_staff_query/README.md)
· [All minimum maps, domains and repair ledgers](../../experiments/p137_station_staff_query/certificates.json).

The **Nov4–6** square and column ranks remain exactly as published by George
Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and Lasry's 2017 key
list. The earlier unreviewed `p137_ocr_block4` is preserved separately. This
source review, new query reading, frame reconstruction and independent
verification are by **icekylinx and GPT-6 Astra Pro**.
