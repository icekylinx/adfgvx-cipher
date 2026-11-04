# November 14 cross-key notices: an arriving pilot and a backup radio station

[Case index](../README.md) · [ADFGVX Cipher](../../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and cross-key comparison: icekylinx and GPT-6 Astra Pro.**

Seven intercepts on Childs's printed pages 190, 193 and 194 preserve three
message families. Two radio-service requests were sent under different
keys. Two notices about a pilot's arrival in Berlin describe the same
apparent event, with changed wording. A third interrupted arrival notice
matches a complete source exactly: that witness restores **85 missing
coordinates and 85 additional raw plaintext positions** without changing any
of the fragment's 195 received coordinates.

## Which station can replace NKJ?

The p190 B and p190 E messages read, with the separately certified repairs:

**Readable German:**

> Welche Station kann NKJ bei Betriebsstoerung vertreten? Vielleicht
> [Sewastopol]. Dring[end] Bescheid an LP.

**Display notes:** `[Sewastopol]` marks a coordinate-priced word proposal; `Dring[end]` expands the literal abbreviation and supplies prose letters only. Neither bracket form by itself asserts direct source support.

**Meaning:** Which station can replace NKJ during an interruption of service?
Perhaps Sevastopol; send an urgent reply to LP. The full city spelling
`SEWASTOPOL` is the candidate reading, and its S is an editorial repair.
The source abbreviation `DRING` is retained in the exact template; the
expanded word above is explanatory.

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
WELCHESTATIONKANNNKJBEIBETRIEBSSTOERUNGVERTRETENXXVIELLEICHTSEWASTOPOLXDRINGBESCHEIDANLP
```

</details>

Both ciphertexts have 176 source slots, giving 88 plaintext positions. Their
published keys have different transposition widths: 16 columns for p190 B
and 20 for p190 E. This is an aligned re-encryption comparison, not simply
another message about the same subject.

The literal source decryptions are:

| Source | Unmodified published-key decryption |
|---|---|
| p190 B | `WELC?ESTATIO?KANNNKJ?EIBETRI?BSSTOERUNGVERTRETENXXVIELLEICHTSEWAVTOP?LXDRINPBESE?IIDANLP` |
| p190 E | `WELCHE?TATION?ANNNKJBEIBETRIEBSTTOERUNG?ERTRETENXXVIELLEICHTSEWA?TOPOLXDRINGB?SCHEI?ANLP` |

**87/88 preferred positions have a complete pair in at least one source.**
The exception is the S at plaintext index 64 in `SEWASTOPOL`. The earlier
copy has raw V; the other copy has a damaged half-pair whose domain includes
S. The city reading remains a separately priced editorial choice.

The p190 B candidate costs five observed-coordinate substitutions and five
fills for a printed `-----` group. The p190 E candidate costs one
observed-coordinate substitution and six uncertain-slot fills. One of those
six slots is a visible A/X overstrike: the certificate preserves and decrypts
both readings, and the candidate's X is among them. The invalid printed
letters Q and T are also retained in the literal transcription.

## Does NKJ relay messages for Mackensen?

The p190 D and p193 A notices have the following source-supported reading:

**Readable German:**

> Vermittelt NKJ Funksprueche fuer Mackensen? Habt ihr Verbindung, und wie?
> Dring[end] Bescheid an FUGROSTA. LP.

**Display notes:** `Dring[end]` is the same prose-only abbreviation expansion here. The two witnesses retain their distinct `FUR` and `FUER` spellings in the exact outputs below.

**Meaning:** Is NKJ relaying radio messages for Mackensen? Do you have
contact, and how? Send an urgent reply to FUGROSTA; signed LP. `FUGROSTA`
is retained as transmitted. The transmitted abbreviation is `DRING`.

The longer exact candidate is:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
VERMITTELTXXNKJXXFUNKSPRUECHEFUERMACKENSENHABTIHRVERBINDUNGUNDWIEXXDRINGBESCHEIDANFUGROSTAXXLP
```

</details>

The p190 D text uses `FUR`, giving 93 characters and 186 ciphertext
coordinates. The p193 A text uses `FUER`, giving 94 characters and 188
coordinates. After this one explicitly identified wording difference is
aligned, **every letter of the 94-character candidate has a complete pair
in at least one original source**. Neither ciphertext is padded or trimmed
to make their lengths agree.

The literal decryptions are:

<details>
<summary>Raw decoded text</summary>

**Raw output — separate literal witnesses under their stated period keys:**

```text
p190 D:
VERMITTELTXXNKJXXFUNKSPRUECHEFURMACKENSENHABTIHRV?RBINDUNOUNDWIEXXDRINGBESCHEIDANFUGROSTAXXLP

p193 A:
LERMITTE?T0XDKRX5FUNKS0RUECHZF?ERMACTENSENHA?TIHRVERBINDUNGUNDWIEXXDRINGBE5CIE?DANFU?R0STA?XLP
```

</details>

The p190 D candidate requires two observed-coordinate substitutions. The
p193 A candidate requires 15 substitutions and three fills for printed
dashes. Their full candidate reencryption checks are separate. The large
number of garbles in p193 A does not obscure the independent support from
the cleaner p190 D copy, while p193 A supplies the latter's damaged E and G
in `VERBINDUNG` and the extra E in `FUER`.

## A Warsaw soldiers' council representative reaches Berlin

The p190 A and p194 B notices say, with their certified ordinary-word repairs:

**Readable German:**

> Zitadelle [Warschau], fuer Soldatenrat. Flieger / Flugzeugfuehrer
> FR?E, Bevollmaechtigter [des] Soldatenrats, in Berlin wohlbehalten
> eingetroffen. Auswaertiges Amt.

**Display notes:** This is a composite readable presentation, not a third recovered source. `[Warschau]` is present in the fuller p194 B witness; `[des]` is supplied grammar absent from both exact wordings. The slash in `Flieger / Flugzeugfuehrer` displays the two witnesses' different words. `FR?E` retains one unresolved name position and is not a proposed surname.

**Meaning:** To the citadel's soldiers' council: the pilot FR?E, a council
representative, has arrived safely in Berlin. The fuller p194 B wording
explicitly includes Warsaw. The raw texts omit the grammatical article
inserted in brackets above. No personal identity is assigned.

The literal decryptions are:

<details>
<summary>Raw decoded text</summary>

**Raw output — separate literal witnesses under their stated period keys:**

```text
p190 A:
ZITADELLEXFUERSOLDATENRXTXXFLIEGERMFR?EXBEVOLLMAECHTIGTERSOLDATENRATSINBERLINWOHLBEHALTENEINGETROFFENXXAUSWAERTCGESAMT

p194 B:
ZITADELLEXWARSCHAUXFUERXSOLDATENRATXFLUGZEUGFUEHRERXFR?EXBEVOLLMAECHTIGTERXSOLDLTENRATSXINXBERLINXWOHLBEHALTENXEINGETROFFENXAUSWAERTIGESAMTX
```

</details>

The p190 A readable template changes three source coordinates to obtain
`RAT`, the separator after `FLIEGER`, and `AUSWAERTIGES`. The p194 B template
changes one coordinate to obtain `SOLDATENRATS`. Both name fields remain
`FR?E`. These notices share a long message body but differ in their opening
words, separators and length; no whole-message ciphertext alignment is used.

### The interrupted p193 B copy

The p193 B record is headed `WAU v LP (4.15 p.m., November 14th)` and
`RICHI---`, with 195 printed coordinates. All 195 are identical to the suffix
of p194 B beginning at ciphertext index 85. The complete p194 B record has
the same call signs, a `4.14 p.m.` interception time and a `RICHI-280` length.

The certificate first retains the fragment as a 280-position source model
with **85 unknown prefix slots**, which fixes only **54/140 raw positions**.
It then fills those 85 positions from the independently printed beginning
of p194 B. No received coordinate of p193 B is changed. The restored stream
equals p194 B exactly and fixes **139/140 raw positions**: **85 additional
positions** are recovered from the overlapping source, with an exact witness
index for every supplied coordinate.

This restoration preserves the complete copy's literal `SOLDLTENRATS`
garble and its unresolved name cell. The separate A-for-L word repair is
not passed off as part of the observed missing prefix. The 195-coordinate
fragment, its odd length and its unknown printed length label are all
retained in the input record.

### What the shared surname does and does not constrain

| Witness | Key | Unknown name position | Square cell | Original symbol domain |
|---|---|---:|---|---|
| p190 A | Nov13–15b | 37 | FX | 234789QY |
| p194 B | Nov13–15a | 54 | DG | 0123456789QY |

Indices are zero-based. If both fields contain the same correctly copied
name, the two cells must represent the same symbol, with intersection
**234789QY**. This eliminates four possible assignments from the second
field, but does not identify the symbol. A further letter-only assumption
leaves **Q or Y**.

`FRYE` is a plausible surname proposal. It is not uniquely established by
the domain intersection, and no independent historical identification has
been found. The certificate checks all eight common symbols: each one
reencrypts the edited templates exactly under the corresponding conditional
cell assignments. Accordingly neither published square is filled.

## Evidence and exact reproduction

- [Source inputs, headers and published keys](../../experiments/nov14_retransmissions/inputs.json)
- [Per-letter coordinate domains and repair certificates](../../experiments/nov14_retransmissions/certificates.json)
- [p190 A source](../../experiments/nov14_retransmissions/sources/p190_A.png)
- [p190 B source](../../experiments/nov14_retransmissions/sources/p190_B.png)
- [p190 D source](../../experiments/nov14_retransmissions/sources/p190_D.png)
- [p190 E source](../../experiments/nov14_retransmissions/sources/p190_E.png)
- [p193 A source](../../experiments/nov14_retransmissions/sources/p193_A.png)
- [p193 B source](../../experiments/nov14_retransmissions/sources/p193_B.png)
- [p194 B source](../../experiments/nov14_retransmissions/sources/p194_B.png)
- [Experiment and verification instructions](../../experiments/nov14_retransmissions/README.md)

The seven records contain **1,437 printed source slots**. Their declared
frames fix **654/761 raw positions** before filling the interrupted prefix,
or **739/761** after the independent witness supplies it. The denominator
includes p193 B's explicitly restored 280-coordinate frame. Fixed positions
include literal garbles; they are not all claimed as correct historical
letters. Published keys are credited in the input provenance. This edition
provides source review and exact comparison, without a claim to first
decipherment of every underlying text.
