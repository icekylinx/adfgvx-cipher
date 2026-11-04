# Warsaw control markers and radio forwarding instructions

The messages request commercial news from Bucharest, define LP forwarding duties, discuss Army Group Kiev’s march route, and distinguish the FRANZ and EMIL markers used for Warsaw traffic.

**Complete edition by printed page:** [p. 192](../pages/192.md) · [p. 194](../pages/194.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**ADFGVX Cipher — icekylinx and GPT-6 Astra Pro**

Four previously uncatalogued messages can be read with the published
`Nov13-15b` partial square. They describe commercial reporting from Bucharest,
LP's forwarding responsibilities, Army Group Kiev's march route, and the
`FRANZ`/`EMIL` markers used for Warsaw messages. The physical source, unresolved
symbols and exact price of each proposed repair are retained separately.

Primary evidence: J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, printed pp. 192 and 194 (PDF pp. 195 and 197). The corresponding crops,
PDF hash and literal transcriptions are in
[the source edition](../../experiments/warsaw_service_messages/inputs.json).
The published square's unknown cells and numerical labels are not changed.

## p192 A: request to Kretzschmar in Bucharest

The source header is `NKJ FUER UKS`, receipt `06.45 p.m., November 14th`,
origin `22.55 (15/11)`, and `RICHI-350`. The incompatible dates are preserved.
The 350 printed slots include an `E`-like overstrike at source index 120,
inside the group `EXAXF`. It is outside the six-coordinate alphabet and is
treated as an erasure.

Raw decryption, 171 fixed positions out of 175:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ANXOBLT0KRETZSCHMARBEIXOKMXWIRTSCHAFTSSTABABTX1XBUKARESTXNRX???XERBITTENNACHRICHTUEBERLAGENUN?AUSSICHTENSOWIEBEZUEGLICHUNSERERINTERESSENGEFASSTEBESCHLUESSEXDEUTKAUF5AUSWAERTIG
```

</details>

Filling that overstrike as `F` restores `UND`, with no change to an observed
valid coordinate:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
ANXOBLT0KRETZSCHMARBEIXOKMXWIRTSCHAFTSSTABABTX1XBUKARESTXNRX???XERBITTENNACHRICHTUEBERLAGENUNDAUSSICHTENSOWIEBEZUEGLICHUNSERERINTERESSENGEFASSTEBESCHLUESSEXDEUTKAUF5AUSWAERTIG
```

</details>

The message asks Oberleutnant Kretzschmar, attached to the OKM economic staff,
department 1, in Bucharest for news about the situation and prospects, and
decisions affecting the sender's interests. The literal forms `OBLT0`,
`LAGEN`, and `DEUTKAUF5` are not normalized inside the ciphertext model.
The three reference symbols after `NRX` occupy cells `VG`, `AF`, `AF`.
The [shared conditional VG=2 reading](../../experiments/nov13_joint_completion/README.md#the-award-class)
gives **`2??`**, with the two unknowns still equal. This adds one label to the
existing edition, reaching **173/175**, without another source edit.

## p192 B: LP relays traffic in both directions

The header reads `NKJ v LP (06.56 p.m., November 14th)` and
`NKJ FUER ZO'N 17.30 (15/11)`. Although it advertises `RICHI-268`, the source
has **267** coordinate letters: the 22nd printed group is only `FVGA`.

Inserting one unknown coordinate immediately after that group gives this raw
reading, with 131 fixed positions out of 134:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional insertion immediately after the short printed group:**

```text
KWHXLPXUEBERMITTELTALLEVORLIEGENDENWICHTIGENNACHRICHTENFUERHEIMATDIENSTSTE?LENSOWIEXOHLXUNDUMGEKEHRTXKMXALLGXKRIEGSDEPXNRX?5?1115XANCH
```

</details>

The ordinary-word candidate is:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — same conditional missing-slot frame, with the stated repairs:**

```text
KWHXLPXUEBERMITTELTALLEVORLIEGENDENWICHTIGENNACHRICHTENFUERHEIMATDIENSTSTELLENSOWIEXOHLXUNDUMGEKEHRTXKMXALLGXKRIEGSDEPXNRX?5?1115XANCH
```

</details>

Its meaning is direct: LP transmits all available important messages for home
offices and OHL, and conversely. The ending names `KM`, the general war
department and a reference that remains literally `?5?1115` under the
published partial square.

An exhaustive check of all 268 possible insertion boundaries finds exactly
two zero-substitution fits to that ordinary-word stencil: source gaps **109**
and **110**. Both insert `F` next to the same observed `F`, producing the same
repaired ciphertext. The alternative unfilled gap moves the single erased
plaintext letter from `DIENSTSTE?LEN` to `SOWI?`; both complete to the same
candidate. No other source coordinate is altered. The two baseline unknown
reference symbols are at cells `GD` and `VG`. Applying the shared conditional
VG=2 assignment gives **`?521115`**, taking this edition to **133/134** fixed
labels; GD remains unknown. Both gap alternatives are retained.

## p194 C: which march route will Army Group Kiev choose?

The header is `IWE v WAU (2.31 a.m., November 16th)`, origin `2300 (15)`,
`RICHI-224`. All 224 printed coordinates are valid.

Raw reading, 111 fixed positions out of 112:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
HEERESGRUPPEXKIEWXXWELCHENC?MARSCNWEGWAEHLTUEERESGRUPPEKIEWXXDRINGENDBALDIGSTBESCHEIDFUNKENXPRESSEXSXRXWARSCHAUX
```

</details>

Changing source index 5 from `X` to `A`, and source index 60 from `V` to `A`,
restores the two clear ordinary words:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
HEERESGRUPPEXKIEWXXWELCHENC?MARSCHWEGWAEHLTHEERESGRUPPEKIEWXXDRINGENDBALDIGSTBESCHEIDFUNKENXPRESSEXSXRXWARSCHAUX
```

</details>

The message asks which march route the army group will choose, requesting an
urgent prompt reply by radio, and ends with the Warsaw soldiers' council's
press designation. The `C?` segment after `WELCHEN` is still unexplained.
Reading it as `XX` would require **three additional observed-coordinate
changes**; that complete but editorial candidate is priced separately in the
certificate and is not promoted to the conservative raw text.

## p194 E: FRANZ and EMIL control markers

The source is `LP v WAU (---- November 16th)`, `SSDD 2256 (15)`,
`RICHI-240`. Its first group is literally `XFYGF`, so the `Y` at source
index 2 is treated as an erasure. The other 239 coordinates are valid.

Raw reading, 119 fixed positions out of 120:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ZUKUENFTIGWERDENUNK?NTOLLIERTETELSDESXSXRXWARSCHAUDURCHXXFRANZXXXKONTROLLIERTEDURCHXXEMILXXGEKENNZEICHNETXXSXRXWARSCHAUX
```

</details>

Filling the invalid coordinate as `X` yields this complete, exactly
reencryptable candidate without changing any valid source coordinate:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
ZUKUENFTIGWERDENUNKONTOLLIERTETELSDESXSXRXWARSCHAUDURCHXXFRANZXXXKONTROLLIERTEDURCHXXEMILXXGEKENNZEICHNETXXSXRXWARSCHAUX
```

</details>

Future unchecked telegrams from the Warsaw soldiers' council are to be marked
`FRANZ`; checked telegrams are to be marked `EMIL`. The source plaintext spells
the first adjective **UNKONTOLLIERTE**, omitting the expected `R` from the
ordinary German word. It also puts three `X` separators after `FRANZ`. Neither
irregularity is silently changed to make the sentence look cleaner.

## Reproducibility and limits

The [verifier](../../experiments/warsaw_service_messages/verify.py) checks the
published key against `data/keys.json`, independently rebuilds the
transposition indices, records every plaintext domain, reconstructs every
candidate ciphertext from its listed edits, and exhaustively retains the two
p192 B gap minima. Its optional PDF check verifies source-crop pixels.

The four records contain 1,081 literal slots, of which 1,079 are valid
coordinates. After the one declared insertion, their models have 541 plaintext
positions, 532 fixed before repair and 535 in the conservative candidates.
The shared VG=2 interpretation adds **two** reference digits, reaching
**537/541**, as checked in the
[shared-traffic certificate](../../experiments/nov13_joint_completion/traffic_certificates.json).
The remaining reference symbols, the published `0` and `5`, and the
inconsistent source dates are retained.

</details>
<!-- CASE-EDITION:END -->
