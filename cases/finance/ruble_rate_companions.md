# Ruble prices and payments above par: companions to p171 A1

**Companion source editions: icekylinx and GPT-6 Astra Pro.**

The second and third parts of the telegram whose first part was read by
**Norbert in 2017** report prices for Tsar rubles in Kiev and Warsaw, then
recommend allowing more than par for `BONS` if necessary. They complete
the subject of the earlier first-part reading without changing its priority
or its source accounting. The second part requires a substantial, explicitly
conditional layout reconstruction; the third part needs only two printed
erasure fills.

The source is Childs, *General Solution of the ADFGVX Cipher System*,
[printed p171 A2–A3, PDF p174](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [three-part section](../../experiments/ruble_rate_companions/sources/p171_A.png)
is headed:

```text
9th NOVEMBER, 1918.
A) COS v NKJ (1.58 a.m., November 10th)
COS POT FUR GENERAL VON KRESS 1425 (9/11) 3 TLE
```

Only A2 and A3 are new physical source records in this package. A1 remains
in [the canonical challenge case](../p171.md), credited to Norbert, with
Max Baertl's later editorial `KURSE STARK` separately identified.

## A2: what the telegram reports about ruble prices

Under the conditional layout described below, the direct reading is:

```text
GEMEINS0MXXINKIEWXKIEWW?RDENFUERHUNDERTZAYENRUBEL?UNDERTVIERZIGMARKGEZAHLTXINWARSCHAUSO2LENBISHUNDERTNEUNZINMAR?GEZAHATWE?XENX
```

Six observed-coordinate substitutions, three fills of retained printed
dashes, and one fill of the added unknown coordinate give:

```text
GEMEINSAMXXINKIEWXKIEWWURDENFUERHUNDERTZARENRUBELHUNDERTVIERZIGMARKGEZAHLTXINWARSCHAUSOLLENBISHUNDERTNEUNZIGMARKGEZAHLTWERDENX
```

The opening `GEMEINSAM` continues A1's reference to Germany and the Entente.
The message reports that **140 marks were paid for 100 Tsar rubles in Kiev**,
and that **up to 190 marks were reportedly being paid in Warsaw**. These
amounts are spelled out as words, so they do not require filling the period
key's unknown digit cells. They remain reports made by this telegram, not
independently verified market-price observations. The repeated `KIEW` is
preserved.

### The source is 261 slots; the working frame is 252

The [source crop](../../experiments/ruble_rate_companions/sources/p171_A2.png)
prints `RICHI-252`, but its literal transcription contains **261 slots**.
The adopted model makes three explicit layout decisions:

1. Exclude source group 6, **`---DD`**, at positions 25–29.
2. Exclude the visibly struck-through source group 19, **`G-VFA`**, at
   positions 90–94.
3. Add one unknown coordinate within the four-character group **`DVAX`**, at
   source positions 200–203, to make a five-coordinate group.

All indices here are zero-based. Both excluded groups remain visible in the
literal transcript. Their ten slots include **six observed coordinates and
four printed erasures**. The `G-VFA` cancellation is visible; excluding
`---DD` is a further model decision and is not claimed to be uniquely
required by the typography. The source itself does not certify the added
coordinate's exact boundary.

With those two exclusions held fixed, the verifier examines **all five
boundaries** in `DVAX`:

| Source boundary for the added unknown | Known-coordinate substitutions for the full proposed text | Substitutions with places and spelled quantities masked |
|---:|---:|---:|
| 200 | 8 | 6 |
| 201 | 7 | 6 |
| 202 | 6 | 5 |
| 203 | 6 | 5 |
| 204 | 7 | 5 |

The full text has two tied minima, **202 and 203**. Both produce the same
corrected ciphertext, since the supplied `A` can lie before or after an
already observed `A`. The record uses boundary 202 as a representative and
preserves boundary 203 equally. Removing the place and quantity words from
the stencil leaves **three** ties, 202–204. This is a local check of a model
selected after the earlier readable candidate was seen, not an independent
control or a global proof of the original geometry.

## A3: authorize more than par if necessary

The third part is source-exact at **152 slots** and has two printed dashes.
Its direct reading is:

```text
EMPFEHLEDAHERNOTFALLSFUE?BONSAUCHMEHRALSPARIXPARIB?WILLIGENXXWALLERXWALLERXX
```

Filling those two dashes, with no observed-coordinate change, yields:

```text
EMPFEHLEDAHERNOTFALLSFUERBONSAUCHMEHRALSPARIXPARIBEWILLIGENXXWALLERXWALLERXX
```

The sender, `WALLER` repeated, therefore recommends authorizing more than
par for `BONS` if needed. `Bons` is retained as the message's term; the
edition does not identify a particular issuer or financial instrument.
The duplicated **`PARI X PARI`** is also preserved, without deduplication.

## Exact accounting

| Part | Literal source slots | Working coordinates | Raw fixed labels | Edition fixed labels | Known-coordinate substitutions | Printed fills | Added-coordinate fills |
|---|---:|---:|---:|---:|---:|---:|---:|
| A2 | 261 | 252 | 122 / 126 | 126 / 126 | 6 | 3 | 1 |
| A3 | 152 | 152 | 74 / 76 | 76 / 76 | 0 | 2 | 0 |
| **Total** | **413** | **404** | **196 / 202** | **202 / 202** | **6** | **5** | **1** |

The table's substitutions are **additional to** A2's ten excluded slots,
six of which are observed coordinates, and its one added unknown. There
is no period-key change, source-group reordering or alteration of A1.

The [inputs](../../experiments/ruble_rate_companions/inputs.json) and
[certificate](../../experiments/ruble_rate_companions/certificates.json)
retain literal rows, all five local models, both minimizing placements,
every source exclusion and repair, complete raw/edited texts and explicit
global consistency witnesses. Re-encryption establishes costs and
compatibility, not unique historical wording.

## Prior credit

The period key is credited to **George Lasry, Ingo Niebel, Nils Kopal and
Arno Wacker**. Norbert's
[2017 comment 20](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1#comment-852668)
supplies A1's earlier body and repairs. Both companion bodies had already
appeared in unreviewed OCR-derived computations, and A3 was in the frozen
p73 retrieval corpus. The new work supplies source review and explicit
conditional editions; no universal first-decipherment claim is made.

```sh
python experiments/ruble_rate_companions/verify.py --verify
```

With `--pdf`, the verifier additionally checks the pinned source PDF and
regenerates all delivered crop pixels.
