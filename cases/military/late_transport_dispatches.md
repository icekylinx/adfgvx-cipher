# Rail stoppage, motor columns and aviation replenishment

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**

Three telegrams on Childs's printed p229 concern transport during the final
withdrawal period: halted railway traffic, a request for motor-transport
columns, and an aviation unit's destination and replenishment. Their six
physical parts provide **721 plaintext positions** under the unchanged
published Nov28–Dec1 key. The separate editorial readings require **14
observed-coordinate substitutions and 39 erasure fills**, leaving five
plaintext positions unresolved. Historical digit assignments remain outside
this source edition.

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
[printed p229, PDF p232](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view),
under `30th NOVEMBER, 1918.`. The page's parenthetical receiving times are
in December: **A, 04.59 p.m. on December 1; B, 01.50 a.m. on December 1;
C, 01.15 a.m. on December 1**. These differ from several earlier OCR header
guesses. The photographed callsign has two small marks over `ZON`; searchable
metadata uses `ZON` without making a new callsign identification.

## A: the evening report and halted railway transports

The [three-part source](../../experiments/late_transport_dispatches/sources/p229_A.png)
has the header `HP v ZON; 1930 (30/11) FUR OKM 3 TEILE` and exact part lengths
228, 192 and 176. The raw body was already recognizable in an earlier
unreviewed OCR-derived computation. The present work verifies every source
slot and records the limited word repairs explicitly.

Part A1, after the one-coordinate `M3T→MIT` repair:

**Edited output:**

```text
ABENDMELDGYVY26YXXYY8YRYDYISTMITANFANGBISTISZAFOELDVARAUFGERUECKTYUNTERBRINGUNGSRAUMDERJX5YUYJX0YIYDYUNVERAENDERTY
```

This is an evening report. It says that the leading element has advanced to
`TISZAFOELDVAR` and that the accommodation area of the subsequently named
formations is unchanged. The literal `26`, `8`, `JX5` and `JX0` remain
published-key labels, not certified dates or unit numbers.

Part A2, with one substitution proposing `SWOLNOK→SZOLNOK` and the printed
dash filled to give `ANGEHALTEN`:

**Edited output:**

```text
SEITJ5YXXYABENDSSINDALLETRANSPORTEAUFSTRECKEARADSZOLNOKAUFWEISUNGDERUNGYZYTYLYANGEHALTENWORDENYY
```

All transports on the proposed **Arad–Szolnok** route have been stopped on
the instruction of the Hungarian `Z T L`. The latter abbreviation remains
unexpanded. The evening date-like field `J5YXX` is not numerically interpreted.

Part A3, with two substitutions restoring `NICHT` and `GEFUNDEN`:

**Edited output:**

```text
DIEFUERHEUTEBEABSICHTIGTENVERLADUNGENHABENDAHERBISHERNICHTSTATTGEFUNDENYYAYOYKYXXYXYAYYY
```

As a consequence, the loadings intended for that day have not yet taken place.
The three parts form a continuous operational report. No missing part,
coordinate insertion or reordering is needed.

## B: how many motor columns can the army release?

The [two-part source](../../experiments/late_transport_dispatches/sources/p229_B.png)
has `ZON v BSL; NR 153 1900 (30/11) 2 TLE`, with exact lengths 268 and 248.
In B1, two previously uncertain words are filled from printed dashes, and
one observed coordinate repairs the office abbreviation `OH4→OHL`:

**Edited output:**

```text
AOKXXYOKMHATBEIOHL0KRAFTWAGENKOLONNENBEANTRAGTOHLDRAHTETMIRRMX?X63282ESWIRDGEBETENMITXXARMEEUNMITTELBARINVERBINDUNGZUTRETENOBVONDIESER
```

OKM has requested motor columns from OHL. OHL asks the sender to contact
the army directly to establish whether further columns can be made available.
The raw quantity is the single label **`0`** after the repaired `OHL`; the
source does **not** establish a request for “40 columns.” The army labels
`XX` and the damaged reference `RMX?X63282` remain unassigned.

B2 continues the question, after six substitutions and five erasure fills:

**Edited output:**

```text
NOCHWEITEREAKKSABGEGEBENWERDENKOENNENYTELRAMMSCHLUSSUMMITTEILUNGWIRDGEBETENWIEVIELKONNENABGEGEBENWERDENKOENNENYOKMRMXCX0?40Y
```

The body asks how many additional `AKKS` can be released. That abbreviation
is retained, as are the shortened **`TELRAMM`** and six-character **`KONNEN`**.
The edition does not silently add letters to make `TELEGRAMM` or a second
`KOENNEN`. The closing `OKM` is an explicitly priced office-label repair;
its context is supported by the unchanged `OKM` in B1. The final numerical
reference remains `0?40` in baseline labels.

Visual retranscription also resolves two earlier OCR erasures without changing
the source: B1 source index 195 is the first `F` of `FFGFD`, and B2 index 161
is the `F` of `GFDGG`. These source readings are distinct from editorial
coordinate substitutions.

## C: an aviation unit and a park at the proposed Craiova destination

The [aviation source](../../experiments/late_transport_dispatches/sources/p229_C.png)
has `ZON v BSL; NO 151 2100 (11/30)` and `RICHI-330`. Its **330 actual slots**
include **33 printed dashes** and a **Q-shaped glyph**, transcribed `Q` and
conservatively masked, at source index 154. A
[close view](../../experiments/late_transport_dispatches/sources/p229_C_glyph.png)
preserves that decision for review. The earlier unreviewed OCR candidate
stream contained only 323 slots.
Reading the omitted printed slots from the image restores the actual frame;
it is not a seven-coordinate insertion into the historical ciphertext.

The resulting direct reading under the published Nov28–Dec1 key is:

**Raw output:**

```text
K?FLXXYYW?BLEIBTF?IEGER???LY24Y?A?SCHZIEL?STC?0IO?ADA?IER?IGE?ERP?RKE?RIC?TET?IR??BIT?ENA??HK?VER?ETZ?EFLIEGE?VERBAEN?EBESTIM?UNGSGEM?ESSAUFF??LLENYK?FLMACKY?3X4OPYY
```

Three observed-coordinate substitutions and 31 erasure fills support this
separate conditional edition:

**Edited output — conditional partial-source reconstruction with the stated erasure fills:**

```text
KOFLXXYYWOBLEIBTFLIEGERABTLY24YMARSCHZIELISTCRAIOVADAHIEREIGENERPARKERRICHTETWIRD?BITTENACHHK?VERSETZTEFLIEGERVERBAENDEBESTIMMUNGSGEMAESSAUFFUELLENYKOFLMACKY?3X4OPYY
```

The proposed body asks where the flight detachment is, gives **Craiova** as
its march destination because a park of its own is being established there,
and asks for transferred aviation formations to be brought up to their
prescribed strength. `FLIEGERABTL` and the damaged ordinary words are
editorial restorations, with their costs recorded; the exact place reading
and wording are not independently witnessed by a second telegram.

Three positions remain unresolved:

| Position | Context | Baseline-key domain | Treatment |
|---:|---|---|---|
| 81 | `WIRD?BITTE` | `39WXYZ` | Boundary left unknown; no choice between possible separator labels |
| 93 | `NACHHK?VERSETZTE` | `BCKMSW` | Destination left as `HK?`; no silent repair to `OKM` |
| 157 | `MACKY?3X4OPYY` | `278GPY` | Closing reference remains incomplete |

The unit label **`24`**, the army label `XX`, the reference fields and raw `Y`
separators are preserved. Applying an already proposed late-key numerical
interpretation would be a separate hypothesis, not new historical evidence
from this message.

## Source accounting and reproducibility

| Part | Slots | Printed dashes / invalid glyphs | Raw fixed labels | Edition fixed labels | Known-coordinate changes | Erasure fills |
|---|---:|---:|---:|---:|---:|---:|
| A1 | 228 | 0 / 0 | 114 / 114 | 114 / 114 | 1 | 0 |
| A2 | 192 | 1 / 0 | 95 / 96 | 96 / 96 | 1 | 1 |
| A3 | 176 | 0 / 0 | 88 / 88 | 88 / 88 | 2 | 0 |
| B1 | 268 | 3 / 0 | 131 / 134 | 133 / 134 | 1 | 2 |
| B2 | 248 | 6 / 0 | 118 / 124 | 123 / 124 | 6 | 5 |
| C | 330 | 33 / 1 | 131 / 165 | 162 / 165 | 3 | 31 |
| **Total** | **1,442** | **43 / 1** | **677 / 721** | **716 / 721** | **14** | **39** |

There are no source-coordinate insertions, deletions, block moves or key
changes. Fixed-label totals do not authenticate historical numerals. The
[inputs](../../experiments/late_transport_dispatches/inputs.json) preserve
manual rows, full render metadata, protected fields and separate recipes;
the [certificate](../../experiments/late_transport_dispatches/certificates.json)
lists every change, its source and plaintext position, all numeral/`J/Q/Y`
occurrences, and global round-trip witnesses. Arbitrary witnesses certify
consistency, not original wording.

The published key is credited to **George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker**, [2016, DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461).
Earlier unreviewed A/B candidates are retained in the package, including
their use in the frozen p73 retrieval corpus. No explicit p229 body was
located in the bounded author-paper, supplementary-reading and catalog
check; this does not establish universal decipherment priority.

```sh
python experiments/late_transport_dispatches/verify.py --verify
```

With the pinned source PDF, the optional `--pdf` argument also regenerates
and compares the delivered crop pixels.
