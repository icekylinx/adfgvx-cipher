# Supply cargo at Nikolaev and the sale of Corcovado

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**

**Prior identification of the p199 A body: George Lasry, Ingo Niebel, Nils
Kopal and Arno Wacker (2016), §6.5.**

Five source records recover two distinct messages intercepted on November 15,
1918. The first reports on steamers and goods at Nikolaev and asks what the
recipient intends to do as circumstances change. The second orders that a
ship sale to Turkey, or the transfer of ownership following a sale, should
be stopped unless the stated payment condition is met.

Both messages use the published `Nov13-15b` partial square. They are separate
traffic, not overlapping copies of one plaintext. Literal source crops and
headers are in the [source edition](../../experiments/black_sea_shipping/inputs.json),
and each geometric choice and coordinate repair is in the
[exact certificate](../../experiments/black_sea_shipping/certificates.json).
The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, printed pp. 199–200, PDF pp. 202–203.

Lasry and colleagues already describe the p199 supply message in
[their paper](https://doi.org/10.1080/01611194.2016.1169461), §6.5, *A Code
within a Code* (author PDF p. 25, printed p. 24). The work added here for p199
is the exact source edition, the full set of frame alternatives and
coordinate-level repair certificates. Its body identification is credited
to that prior publication. Their approximate ten-ton paraphrase does not
settle the literal `1?0` field under the conservative partial key used here.

## The three-part supply message, p199 A

The common source header reads `XYZ v LP (06.01 p.m., November 15th)`,
`16.50 (15/11)`, `3 TLE`. It belongs to the correspondence using
`FEIGENHAUS`, `HERKULES` and `REICHSVERSORGUNG`, also seen in the earlier
[p120/p123 messages](p120_p123.md). The new reference is written out as
`SECHSHUNDERTACHTZEHN` (618); the earlier message has 617. This is further
correspondence, not a retransmission of the previously published text.

### A1: incoming steamers and a garbled cargo description

The source advertises `RICHI-292`, but prints **293 valid coordinates**.
Its tenth group is the six-letter `XAXADV`. Removing its final `V`, source
index 50, gives this 146-position raw decryption:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional removal of the final V in six-coordinate group XAXADV:**

```text
ANFEIGENHAUSSECHSHUNDERTACHTZEHNXHERKULESMELDETZWOEZFTENNOVEMBERDASSNIKOLAJEWMEHREREDAMPFERLEBERKAKAUPULSERAUSXOPERETTEXZIRKA1?0TONNENEINGELAUFENX
```

</details>

It addresses Feigenhaus and reports Herkules's news of November 12 about
several steamers entering Nikolaev. The cargo wording is damaged. Three
observed-coordinate substitutions support the same-length ordinary-word
repairs `ZWOELFTEN` and `KAKAOPULVER`:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — same conditional single-coordinate deletion, followed by word repairs:**

```text
ANFEIGENHAUSSECHSHUNDERTACHTZEHNXHERKULESMELDETZWOELFTENNOVEMBERDASSNIKOLAJEWMEHREREDAMPFERLEBERKAKAOPULVERAUSXOPERETTEXZIRKA1?0TONNENEINGELAUFENX
```

</details>

`LEBER` remains unexplained, and `OPERETTE` is retained without claiming its
referent. The amount remains the literal `1?0`; the middle symbol is at the
unfilled `VG` cell. Neither a cargo quantity nor a numerical label is supplied
from expectation.

The deletion is not called globally unique. When names, the `LEBER` segment
and the quantity are masked, deleting source index 50, 51 or 52 gives the same
minimum of three ordinary-word coordinate changes. Only index 50 lies inside
the visibly six-letter source group. The certificate retains all three
broader models, including the alternatives' changed code-name/quantity text.

### A2: goods remain aboard under military guard

All 344 source coordinates are valid. The raw 172-position reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
DASCHWALBENSCHWANZUNDABTRANVPORTABNIKO?AJEWELSEVORLAEUFIGUNMOEGLICHXWAREBLEIBTDAHERUNTERMILITAERISCHERBEWACHUNGANBORDXVERSUCHETDURCHVORZUGSKARTENDARUEBERNAEHERESZUERFAHRENX
```

</details>

Two observed-coordinate changes restore `ABTRANSPORT` and `NIKOLAJEW`,
giving a complete, exactly reencryptable candidate:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
DASCHWALBENSCHWANZUNDABTRANSPORTABNIKOLAJEWELSEVORLAEUFIGUNMOEGLICHXWAREBLEIBTDAHERUNTERMILITAERISCHERBEWACHUNGANBORDXVERSUCHETDURCHVORZUGSKARTENDARUEBERNAEHERESZUERFAHRENX
```

</details>

The plain passage says that the goods therefore remain aboard under military
guard, and asks the recipient to obtain more information through
`VORZUGSKARTEN`. The opening retains `SCHWALBENSCHWANZ` and `ELSE`, alongside
the statement that onward transport is temporarily impossible. These terms
may belong to the correspondence's additional vocabulary code. Recovering
their letters does not identify their operational meaning.

### A3: uncertainty about the recipient's plans

There are 205 printed slots under `RICHI-206`. The malformed group is
`VAYA`, and the next group has an overstruck first glyph recorded as `?`.
The certificate tests all 206 possible single-coordinate insertion boundaries
with the whole footer excluded from the stencil.

Five positions, **164–168**, tie at **zero changes to observed coordinates**
for the ordinary-word body. Gap 165 is a representative, not an established
unique location. Its raw reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional missing-slot placement at gap 165; equivalent alternatives retained:**

```text
SINDBEUNR?HIGTDANICHTWISS?NWASIHRINANBETRACHTLAGEBEGINNENWERDETXREICHSVERSORGUNGXADMIRALSTAB15?16DZWCIX
```

</details>

Filling two source erasures gives:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — same conditional gap model, with the two stated fills:**

```text
SINDBEUNRUHIGTDANICHTWISSENWASIHRINANBETRACHTLAGEBEGINNENWERDETXREICHSVERSORGUNGXADMIRALSTAB15?16DZWCIX
```

</details>

The sender is concerned because it does not know what the recipient will do
in view of the situation. The message ends with `REICHSVERSORGUNG` and
`ADMIRALSTAB`. All five tied models can be filled to this same **92-character
prefix**, without changing an observed coordinate. Their footer readings
differ and are all retained in the certificate.

A separate footer proposal reads `15X16DZWEIX`, filling the separator and
changing one observed coordinate to turn `ZWCI` into `ZWEI`. It is explicitly
editorial; the footer does not select the ordinary-body gap model and does
not establish a new digit assignment.

## The two-part ship-sale order, p200 B

The common source header is `NKJ v LP (08.19 p.m., November 15th)`,
`16.00 (15/11) FUER COS`, `2 TLE`. The received ship name is `CORCOWADO`.
The association with Corcovado is kept separate from that literal spelling.

### B1: stop the sale or ownership transfer

The first part has 394 source slots. The last glyph in group 7, `AAXFY`,
is an invalid coordinate `Y` and remains an erasure in the raw reading:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
MXMXDXNICOLAJEFFXWENNVERKAUFXCORCOWADOXANTUERKEINOCINICHTINORDNUNGSOLLVERKAUFNI?HTSTA?TFINDENXFALLSAUFGRUNDBEREITSGETAETIGTENVERKAUFSEIGENTUMSUEBERTRAGUNGNOCHWICHTERFOLGTISTHATSOLCHEZUUNTERBLEIBENX
```

</details>

Three observed-coordinate substitutions and one invalid-glyph fill give
this complete 197-position candidate:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
MXMXDXNICOLAJEFFXWENNVERKAUFXCORCOWADOXANTUERKEINOCHNICHTINORDNUNGSOLLVERKAUFNICHTSTATTFINDENXFALLSAUFGRUNDBEREITSGETAETIGTENVERKAUFSEIGENTUMSUEBERTRAGUNGNOCHNICHTERFOLGTISTHATSOLCHEZUUNTERBLEIBENX
```

</details>

Addressed to `M. M. D., Nicolajeff`, it says that if the sale to Turkey has
not yet been settled, it should not take place. If a sale has already been
made but ownership has not yet been transferred, that transfer must not
proceed. This is the message's historical instruction, not an inference
about what ultimately happened to the ship.

### B2: payment in Germany before ownership transfer

All 360 printed slots are retained. One glyph is unreadable and another is
an `E`-like overstrike, both preserved as source erasures. The raw text is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
TUERKEIGEGENUEBERKNNGELTENDGEMCHTWERDENXREED?REIWILLDAMPFERANTUEKEINICHTVERKAUFENESSEIDENNDASSKAUFPREISINDEUTSCHLANDVOREIGENTUMSUEBERTRAGUNGBARBEZAHLTWERDEXMARIN?AMTXAXSECHSXS????0
```

</details>

Filling those two erased coordinates recovers `REEDEREI` and `MARINEAMT`,
without changing any observed valid coordinate:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
TUERKEIGEGENUEBERKNNGELTENDGEMCHTWERDENXREEDEREIWILLDAMPFERANTUEKEINICHTVERKAUFENESSEIDENNDASSKAUFPREISINDEUTSCHLANDVOREIGENTUMSUEBERTRAGUNGBARBEZAHLTWERDEXMARINEAMTXAXSECHSXS????0
```

</details>

The message supplies the position to present to Turkey: the shipowner will
not sell the steamer unless the purchase price is paid in cash in Germany
before ownership transfers. The source omits letters in `KNN`, `GEMCHT` and
`TUEKEI`; those strings are not silently length-corrected in the candidate.
The footer's four unresolved symbols use cells `VG`, `VG`, `GD`, `AD`, so
the first two share a value. Their values remain unassigned.

## Exact scope and reproducibility

The five records have 1,596 printed slots, 1,591 valid coordinates and 798
modeled plaintext positions. The declared source models fix 785 positions
before repairs. Conservative candidates fix 792, with the remaining quantity
and reference symbols unresolved. Fixed counts include received garbles;
they are not a claim that every fixed letter is linguistically correct.

The [verifier](../../experiments/black_sea_shipping/verify.py) recomputes every
plaintext domain and source mapping, the broad and source-local deletion
results, all five gap ties, and each exact repair. It checks the separate
conditional `FX=Y` hypothesis against 21 variants, retaining all effects:
there are no newly fixed raw letters, only listed domain reductions. No
published key file is changed.
