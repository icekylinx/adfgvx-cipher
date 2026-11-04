# p168 C — Full Munich routing witness for order 11338

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[All cases](../README.md) · [ADFGVX Cipher](../../README.md)

**Source-frame recovery and review: icekylinx and GPT-6 Astra Pro, 4 November 2026.**
The full p168 C retransmission now has a **139/140-position raw certificate**.
The irregular six-coordinate and four-coordinate groups require an explicit
frame repair: exclude one repeated D and add one unknown coordinate. A V
observed in the corresponding p159 B group supplies that gap, producing a
**140/140-position source-linked stream**. These fixed counts retain the
message's word garbles and numerical labels.

The p168 observation also reads **GEN KDO**, supporting one coordinate repair
of the p159 component's `GEN HDO`. This extends the [p158 component edition](../p158.md);
it is a full witness certificate for an existing record, not a newly found
message or a claim to first decipherment of order 11338.

## Source and frame

Childs, printed p168 / PDF p171, section C:
`RVV v N4 (9.03 p.m., November 9th); 1803 VON SY ZU CHI 156 U 69; RICHI-280`.
The separate `1803` field is retained literally. The [original page crop](../../sources/excerpts/childs_p168_CD.png)
also shows the following section D.

**Source transcription — all 280 observed coordinates, with irregular groups retained:**

```text
GDDFV DXFDD AVVFG XXVDD XVADD VVFGV VDDVV DVAXV
XVGVV GVXDD XVVVG VVVGV DDGDX VAVGG AAAXG AVFAD
VDADDD VAXVD VVDDD GADAX FAXXF GFFXF XDVVD DXDGD
DAXVA VDXVV XDVDV DXDGD XGVFV VGGVD FVVAV DFDAD
VDFXV XDAXG VXVVD DDAGX DVDGD DDGDX DXXXD VVVG
VGVXV VVVFA DDXVD XGXDX AVFDX VGVXV VVVVG VVXDV
VXADX VXDDV GXAVV GDVAA DGDVF VXFVX GFAXD DGDFA
```

Rows 3 and 5 contain 41 and 39 coordinates respectively. The six-coordinate
`VDADDD` is source[80:86]; the four-coordinate `VVVG` is source[196:200]. Their
length discrepancies cancel, so the literal body already has the advertised
280 coordinates. Treating both as regular five-coordinate groups without an
explicit operation would conceal the source error.

The primary frame excludes the D at source 83 and inserts one unknown at
boundary 195 of the remaining 279-slot stream, at the start of the short group.
All other 279 observations remain unchanged and in source order. This is a
conditional reconstruction, not an OCR correction. All indices here are zero
based; ranges are half open.

There are **12 tied descriptions**: exclude any of source 83,84,85 and insert
at any boundary 195,196,197,198. A source-directed comparison checks all 30
choices within the six-coordinate and four-coordinate groups. The twelve
leaders have six disagreements against the independently observed coordinates
of the p159 B component; coordinates already supplied from another copy are
excluded from that comparison. The comparison establishes correspondence,
not a unique historical error mechanism.

## Raw and source-linked readings

**Raw output — primary frame, unchanged Nov7–9 key; 139/140 positions fixed, no coordinate substitutions or fills:**

```text
UEBER2HBAYRXGENXKDOXMUENCXENXXAN7XRSSXDIVXXLA3DSBERGEAN0EECHXXNICH2DURCH1ABELXARMEESCHLUESSELDORPELTXEMPFANGBESTXXOXHXLXRMX1ANRX11338G?HXORX
```

The four insertion boundaries give four different unfilled streams, each
fixing 139 positions. They agree at 136 positions. The repeated-D exclusions
change ownership only. The certificate retains every alias rather than pooling
its known letters into a falsely complete raw message.

Original p159 B coordinates 195–198 all read V. Under the inherited component
correspondence, the relevant V fills the added coordinate in each alias. Every
alias then produces the same completed ciphertext:

**Edited output — one inserted-slot V supplied by p159 B, no changes to retained p168 coordinates; 140/140 positions fixed:**

```text
UEBER2HBAYRXGENXKDOXMUENCXENXXAN7XRSSXDIVXXLA3DSBERGEAN0EECHXXNICH2DURCH1ABELXARMEESCHLUESSELDORPELTXEMPFANGBESTXXOXHXLXRMX1ANRX11338GEHXORX
```

**Readable German — literal word excerpts from that source-linked stream; omitted passages are outside the quotation:**

> […] Gen. Kdo. […] Armeeschluessel […] Empfang best. […] O.H.L. […]

The associated order concerns routing through the Bavarian command at Munich,
army-key treatment and acknowledgment. The original contemporary reading and
later scholarly discussion are credited in the [component history](../p158.md#earlier-historical-reading-of-a-component).
The stream above retains `MUENCXEN`, `RSS`, `LA3DSBERG`, `DORPELT` and the other
remaining garbles; no new place, unit or numeral correction is supplied here.

## New coordinate support for KDO

At plaintext position 16, p168 C has the fully observed pair **VG = K**.
Its model indices 113 and 169 come from source 114 and 170. The corresponding
p159 B component has **VX = H**. Thus its `GEN HDO` can be repaired to `GEN KDO`
using the observed G from p168 source 170:

| Receiving source | Source index | Printed | Parallel-supported replacement |
|---|---:|:---:|:---:|
| p159 B | 169 | X | G |

This is one observed-coordinate substitution in p159 B, supported by a separate
printed observation. It changes exactly one plaintext letter and preserves all
other text in the established `p159B_supported_V` component layer.

**Edited output — earlier p159 B supported-V component plus the single X→G substitution at source169; all other inherited repairs and garbles retained:**

```text
UEBER2XBAYRXGENXKDOXMUENCXENXXAN7XRSSXDIVXXLA3DSBERGXAN0LECHXXNICHTDURCHKABELXARMEESCHLUESSELDOWPELTXEMPFANGBESTXXOXHXLXRMX1ANRX11338GEHXORX
```

## Joint-source reconciliation

The last displayed stream also has an explicit reconciliation of the p168
witness. It follows the established p159 component at the remaining source
disagreements and uses the new p168 observation for KDO. Each selected
coordinate has a printed donor; these are recorded choices between differing
observations, not word guesses or an automatic majority vote.

| Reconciliation | p168 observed substitutions | p168 added-slot fills | p159 additional observed substitutions | Cable word |
|---|---:|---:|---:|---|
| p159 B and p168 C | 5 | 1, V from p159 B | 1, G from p168 C | `1ABEL` retained |
| Add p158 D as third witness | 6 | 1, V from p159 B | 1, G from p168 C | `KABEL` |

The three-witness version is exactly the p159 B + KDO stream displayed above.
Its six substitutions in the primary p168 frame have the following donors:

| p168 source index | Printed | Selected | Original donor |
|---:|:---:|:---:|---|
| 5 | D | V | p159 B source 5 |
| 7 | F | V | p158 D source 7 |
| 169 | X | V | p159 B source 168 |
| 174 | V | D | p159 B source 173 |
| 175 | D | V | p159 B source 174 |
| 247 | D | X | p159 B source 247 |

At model 7, original p159 B has invalid `R`; its earlier V reconstruction must
not be counted as an independent p159 observation. The V here comes directly
from p158 D source 7, in its established prefix correspondence. The two-witness
layer therefore keeps p168's F at that position and retains `1ABEL`. Both layers
keep `DOWPELT` unchanged; no P is invented to make `DOPPELT`. The native sources,
primary raw reading and one-V source-linked layer above remain separate.

## Reproduction and credit

The [certificate](../../experiments/p168_munich_routing_witness/certificates.json)
records the literal source, every coordinate origin, all raw character domains,
the twelve ownership aliases, the copied V and the separate KDO repair. The
original PDF and a fresh source crop are authenticated by SHA-256. Two fresh
same-shape controls recover their complete source-linked streams. Both global
5/6 square completions pass full re-encryption; no choice between them is made.

**Reproduction command — verifies both source-linked streams and all frame alternatives:**

```sh
python experiments/p168_munich_routing_witness/verify.py --verify
```

Order 11338 has a wartime reading by **J. Rives Childs**, published in 1935.
**George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), §6.4**, discuss
the p168 C/D bodies. The p158 composite-source relationship, this full p168 C
source-frame certificate and the coordinate support for KDO are reviewed by
**icekylinx and GPT-6 Astra Pro**. Earlier wording and key credit remain intact.
