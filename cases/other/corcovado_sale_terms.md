# Corcovado: sale terms, Turkish crew and a conditional office number

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**

Six source records recover a detailed November 9, 1918 proposal for selling
Corcovado to Turkey, followed by a November 10 report that the vessel was
already operating with a Turkish crew and captain. The sale terms include
a directly decrypted price of **10 million**, with the currency unstated,
a separate valuation for inventory and materials, payment and risk
provisions, and restrictions on resale and use. These messages precede
the [November 15 order](black_sea_shipping.md) to stop the sale or
ownership transfer unless the payment condition was met.

The primary source is J. Rives Childs, *General Solution of the ADFGVX
Cipher System*, printed pp. 165 and 173, PDF pp. 168 and 176. The
[literal transcription and source crops](../../experiments/corcovado_sale_terms/inputs.json)
retain every coordinate and invalid glyph. The
[exact certificate](../../experiments/corcovado_sale_terms/certificates.json)
separates unchanged-key raw readings, individual coordinate repairs, and
the conditional office-number inference described below.

The square cells and transposition orders are prior published work.
Their provenance, including Lasry and colleagues' final key table and
the 2017 discussion, is preserved in the inputs. A bounded check found
no explicit discussion of these Corcovado bodies in the checked paper,
the corresponding dissertation chapter or the cached 55 comments. That
check does not establish universal historical priority. Lasry, Niebel,
Kopal and Wacker's prior identification of the separate p199 cargo
message is credited in its own edition.

## November 9: proposed sale conditions, p165 A

The source header reads `NKJ v LP (04.00 p.m., November 9th)`,
`1420 (9/11)`, `4 TEILE`. Its four physical blocks are labelled **1, 2, 3,
5 TL**, so the final block is called **A5** here. No absent fourth part is
invented. All four blocks use the published `Nov7-9` partial square.

### A1: price and the seller

All 380 printed coordinates are valid. The raw 190-position reading is:

```text
MITTELMEERDIVISIONXNICOLAJEFFXBEIVERKAUFXCORCOVAUOXMOEGLICHSTFOLGENDEBEDINGUNGENDURCHZUSETZENXXVERKAUFERFOLGTFUERHFMBURGAMERIKALINIEXKAUFPREISFESTX10XMILLXFUERSCHIFFOHNEINVENTARUNDMATERIALXX
```

Two observed-coordinate substitutions give this complete, exactly
reencryptable candidate:

```text
MITTELMEERDIVISIONXNICOLAJEFFXBEIVERKAUFXCORCOVADOXMOEGLICHSTFOLGENDEBEDINGUNGENDURCHZUSETZENXXVERKAUFERFOLGTFUERHAMBURGAMERIKALINIEXKAUFPREISFESTX10XMILLXFUERSCHIFFOHNEINVENTARUNDMATERIALXX
```

Addressed to the Mediterranean Division at Nicolajeff, it asks that the
following conditions be obtained if possible in the sale. The sale is for
the Hamburg-Amerika Line; the fixed purchase price for the ship without
inventory or materials is `10XMILL`. Both digits and every letter of that
price field come from complete observed coordinate pairs, with no repair
or unknown key label. The text does not name a currency.

The received name is `CORCOVAUO`. The following day's message independently
contains all nine letters of `CORCOVADO` under a different key. Conditional
on the two sale reports referring to the same vessel, this supplies a
source witness for the single `U` to `D` change at plaintext position 48.
It does not make the entire messages duplicate copies.

### A2: inventory, present condition and seizure risk

The printed length is 458. Source coordinate 239 is `C` in `GVGVC`, and
417 is `L` in `FALXX`; both are invalid ADFGVX coordinates. They remain
erasures in the raw 229-position reading:

```text
MATERIALUNDINVENTARZUMSELBSTKOSTENPAEISMINUFABNUT?UNGXXSCHIFFWIRDVERKAUFTINAUGENBLICKLICHEMZUSTANDXAUS?ESCHLOSSENPERGOENLICHESEIGENTPMKAPITAENSUNDBESATZUNGXAUSSCHLIESSLICHKOHLENXXUEBERNAHMERISIKOVONSEITENTUERKEIGEGENBESCHLAGNAHME
```

Four observed-coordinate substitutions and the two erased-coordinate
fills produce this complete candidate:

```text
MATERIALUNDINVENTARZUMSELBSTKOSTENPREISMINUSABNUTZUNGXXSCHIFFWIRDVERKAUFTINAUGENBLICKLICHEMZUSTANDXAUSGESCHLOSSENPERSOENLICHESEIGENTUMKAPITAENSUNDBESATZUNGXAUSSCHLIESSLICHKOHLENXXUEBERNAHMERISIKOVONSEITENTUERKEIGEGENBESCHLAGNAHME
```

Materials and inventory are to be valued at cost less wear. The ship is
sold in its current condition; the captain's and crew's personal property
and coal are excluded. Turkey is to assume the risk of seizure. The next
part states by whom and from what date.

The full source transcription also restores two five-letter groups and
the final `VDD` omitted by the earlier OCR extraction. Those coordinates
are visible source material, not a conjectural ciphertext insertion.

### A3: risk, interest and recovery for nonpayment

All 380 source coordinates are valid. The raw reading is:

```text
DURCHFEINDEDEUTSCHENREICHESVOMZEITPUNKTKAUFABSCHLUSSESABXXVERZINSUNGKAUFPREISESBEGINNTSPAETESTENSXSIEBENXUONATENACHKAUFABSCHLUSSXXBEINICHTZAHLUNGRUECKFORDERUNGSRECHTANDEMDAMPFERVORBEHALTENXX
```

One observed-coordinate change, `UONATE` to `MONATE`, gives:

```text
DURCHFEINDEDEUTSCHENREICHESVOMZEITPUNKTKAUFABSCHLUSSESABXXVERZINSUNGKAUFPREISESBEGINNTSPAETESTENSXSIEBENXMONATENACHKAUFABSCHLUSSXXBEINICHTZAHLUNGRUECKFORDERUNGSRECHTANDEMDAMPFERVORBEHALTENXX
```

The seizure risk is from enemies of the German Empire and begins at the
conclusion of the sale. Interest on the purchase price is to begin no later
than seven months after the sale. The right to recover the steamer in the
event of nonpayment is reserved.

### A5: resale, evacuation and encrypted forwarding

The printed `5 TL` has exactly 500 slots. The invalid glyphs are `J`, `L`
and `C`, at source positions 90, 147 and 199. The raw reading is:

```text
VORKAUFSRECHTDEUTSCHLANDSBEIETWAIGENWIEDERVERKAUFXVERBOTVERKAUFSANNICHTDEUTSCHEREEDEREIXVERWENDUNGDAMPFEASAUSSCHLIESSLICHODERINERSTERLINIEFUDRABTRANSPORTDERDEU?SCHENXWEITERGABEDIESESTELEGRAMMSNACHKONSTANTIYOPELNURGESCHLU?SSELTXMARINEAMTXAX?XSX8?3XGXG
```

Three observed-coordinate substitutions and two erased-coordinate fills
restore the ordinary words, leaving both numerical uncertainties intact:

```text
VORKAUFSRECHTDEUTSCHLANDSBEIETWAIGENWIEDERVERKAUFXVERBOTVERKAUFSANNICHTDEUTSCHEREEDEREIXVERWENDUNGDAMPFERSAUSSCHLIESSLICHODERINERSTERLINIEFUERABTRANSPORTDERDEUTSCHENXWEITERGABEDIESESTELEGRAMMSNACHKONSTANTINOPELNURGESCHLUESSELTXMARINEAMTXAX?XSX8?3XGXG
```

Germany is to retain a right of first refusal on resale. Sale to a
non-German shipping company is prohibited. The ship is to be used
exclusively or primarily to transport Germans away. The telegram is to
be forwarded to Constantinople only in enciphered form.

The signature is `MARINEAMT`; the office/reference ending is
`AX?XSX8?3XGXG`. Its first question mark is a complete observed pair at an
unfilled key cell, while the second includes an invalid printed source
glyph. Their uncertainty has different causes and is retained separately.

## November 10: Turkish crew and no radio contact, p173 A

The header reads `LP v NKJ (7.07 p.m., November 10th)`,
`VON NKJ AN LP MARINE AMT BERLIN 1710 (10)`, `2 TLE`.
Both blocks use the published `Nov10-12` partial square.

### A1: the division has left; Corcovado already has Turkish personnel

All 242 coordinates are valid. The raw 121-position reading is:

```text
ZUDORDXA?S?24GXGXX2ITTELMEXRDIVISIONODERVERTRETERNICHTMEHRINNIKOLAJEWXXCORCOVADOFAEHRTBEREITSMI2TUERKISOHERBESATZUNGUNTER
```

Six observed-coordinate substitutions restore ordinary words while
leaving both unknown reference digits unresolved:

```text
ZUDORTXA?S?24GXGXXMITTELMEERDIVISIONODERVERTRETERNICHTMEHRINNIKOLAJEWXXCORCOVADOFAEHRTBEREITSMITTUERKISCHERBESATZUNGUNTER
```

Referring to the recipient's `A?S?24 G G`, the report states that the
Mediterranean Division or its representative is no longer in Nikolaev.
Corcovado is already sailing with a Turkish crew under a captain whose
nationality appears in the next part. The ship name itself is completely
observed and needs no repair.

### A2: Turkish captain and failed contact with Constantinople

The 160-slot source begins with `AGAD-`. Its final dash is an erased
coordinate. The raw text is:

```text
TUERKXKAPITAENXMITKONSTANTINOPEOXKEINFU?KVERKEHRMEHRMOEGLXXGOUVERNEMENTXNKJX1XAX
```

One observed-coordinate change and the erased-coordinate fill give:

```text
TUERKXKAPITAENXMITKONSTANTINOPELXKEINFUNKVERKEHRMEHRMOEGLXXGOUVERNEMENTXNKJX1XAX
```

The captain is Turkish. Radio communication with Constantinople is no
longer possible. The ending reads `GOUVERNEMENT NKJ 1 A`.

## A separate conditional inference: the Marineamt A6S prefix

The November 15 p200 B2 order independently spells out `SECHS` in the raw
ending `MARIN?AMTXAXSECHSXS????0`. Its letters have complete observed
coordinate pairs under `Nov13-15b`; none requires a source repair or an
unknown square cell. The nearby erasure in `MARIN?AMT` does not affect the
word `SECHS`.

| Word letter | p200 B2 plaintext index | Pair | Original source indices |
| --- | ---: | --- | --- |
| S | 168 | `GF` | 88, 246 |
| E | 169 | `XF` | 111, 313 |
| C | 170 | `XV` | 201, 156 |
| H | 171 | `AA` | 358, 21 |
| S | 172 | `GF` | 269, 336 |

The hypothesis is that these three same-vessel reports use the same
stable Marineamt **A6S office/file prefix**, and that the earlier two
unknown prefix pairs are correctly copied. Under that explicit condition:

| Earlier key | Assignment | Earlier direct witness | Additional consequence |
| --- | --- | --- | --- |
| Nov7–9 | `VF=6` | p165 A5 plaintext 239, source pair 473/98 | `XA=5`, since 5 and 6 are the only unused symbols |
| Nov10–12 | `XX=6` | p173 A1 plaintext 8, source pair 121/167 | The four other unknown cells retain the symbols 5, 7, 8, 9 |

The pair in each earlier message is fully observed and unchanged by all
ordinary-word repairs. There is no direct local `XA` occurrence, so the
`XA=5` complement adds no local plaintext character. `VF=6` adds one
physical character, and `XX=6` adds one more. Each is displayed twice in
the certificate because both the source model and repaired candidate are
checked; those variant checks are not counted as distinct recoveries.

The **reference tails are not the same**: p165 ends `A?S8?3GG`, while p173
cites `A?S?24GG`. Neither equality nor consecutive numbering is assumed.
In particular, the source erasure in the first tail is not silently read
as `2`, and the later unknown hundreds digit is not silently read as `8`.

All effects of the two conditional key layers are retained:

| Record / variant | Position | Pair | Domain before | Domain after |
| --- | ---: | --- | --- | --- |
| p165 A2 raw only | 49 | `?F` | `5679JMZ` | `679JMZ` |
| p165 A5 raw and candidate | 239 | `VF` | `56` | `6` |
| p173 A1 raw and candidate | 8 | `XX` | `56789` | `6` |
| p173 A1 raw and candidate | 10 | `XG` | `56789` | `5789` |
| p173 A2 raw only | 39 | `?X` | `156789ENVX` | `16ENVX` |

No other marginal domain or raw character changes in the twelve checked
variants. After the conditional assignments, the raw models still retain
p165 A2 positions 49 (`679JMZ`) and 102 (`3EGLSZ`); p165 A5 positions 159
(`29BITV`), 220 (`DEQTUX`) and 244 (`02ACLR`); p173 A1 position 10 (`5789`);
and p173 A2 position 39 (`16ENVX`). Ordinary-word repairs resolve all but
the two reference positions, p165 A5 position 244 and p173 A1 position 10.

These conditional values disagree with the earlier published
complete-square hypotheses `VF=5`, `XA=6` and `XX=9`. The conservative
partial squares remain unchanged. The certificate enumerates both
possible Nov7 digit permutations and all five Nov10 values for `XX`:
all are compatible with the observed coordinates. The office-prefix
association supplies the distinguishing assumption, not reencryption.

The Nov7 result has an earlier independent line of support. The preserved
[military-context certificate](../../experiments/p170_continuation/military_context.json)
identifies the 6th Reserve Division from historical unit evidence and
therefore supports `VF=6`, with `XA=5` as its remaining-symbol consequence.
That layer has already been propagated to the corps, date and time fields
in [the withdrawal edition](../../experiments/withdrawal_recovery/README.md).
The Corcovado office prefix independently corroborates the same conditional
Nov7 assignment; it is not counted as discovery of a new Nov7 key cell.
The two evidence routes retain different assumptions and are not collapsed
into an unconditional key. The Nov10 `XX=6` inference remains a separate
conditional constraint.

## Exact scope and verification

The six records contain **2,120 printed slots**, of which **2,114** are
valid coordinates, and **1,060 plaintext positions**. The unchanged partial
keys fix **1,051** raw positions. Seventeen observed-coordinate
substitutions and five erased-coordinate fills produce readable candidates
with **1,056** fixed positions. The separate conditional office layer adds
two physical characters, giving **1,058/1,060** positions locally.

No source coordinate is inserted, deleted or reordered. Full candidates
without unknowns are checked by exact reencryption; partial candidates
are checked against their complete coordinate stencil and explicit
residual domains. Every source/model/plaintext coordinate is reversible.

```bash
python experiments/corcovado_sale_terms/verify.py --verify
python experiments/corcovado_sale_terms/verify.py --verify --pdf /path/to/childs.pdf
```

The second command checks the full primary PDF hash and rerenders each
crop pixel-for-pixel. The conditional layer also binds and rederives the
later `SECHS` witness from the independently preserved p200 source
transcription. It does not assume that the sale was completed or settle
the vessel's eventual history.
