# Reval: expected steamers and further transport capacity

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition: icekylinx and GPT-6 Astra Pro.** Childs p213 A1–A3 (PDF p216), **23 November 1918**; published `Nov22-24` key, unchanged. [Inputs](../../experiments/reval_steamer_notice/inputs.json), [exact certificates](../../experiments/reval_steamer_notice/certificates.json), [method](../../experiments/reval_steamer_notice/README.md).

The header reads `KOW v LP (06.20 p.m., November 23rd); FUER RVA 20.00 (23/11) 3 TLE`. Its stated receipt precedes the origin time on the same printed date; the discrepancy is preserved. These parts belong to the lower, 23 November section, separately from the 22 November medical continuation above them.

The message reports arrangements for two steamers to serve troops and provisions at Reval by the end of November, with more tonnage and raw-material transport to follow. Contemporary shipping records now support three separately priced name readings in the second part: **Peter Benoit, Björn and Babylon**. The tonnage remains unresolved. The source reports intended movements; their completion and the port of departure are not established here.

## p213 A1

[Source crop](../../experiments/reval_steamer_notice/sources/p213_A1.png); [overprinted glyph enlargement](../../experiments/reval_steamer_notice/sources/p213_A1_g13.png). All 200 slots are retained. The primary source reading gives 100 fixed raw labels without repair:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
RPHAXREVALXBISENDENOVEMBERWERDENZWEIDAMPFERFUERTRUPPENUNDPROVIANTVONZUSAMMENXY5111XTONNENINREVALSEIN
```

</details>

Reading: by the end of November two steamers for troops and provisions, of a combined unresolved tonnage, are expected in Reval. `RPHAX` and `Y5111` remain raw labels.

Source index 62 is an overprinted glyph, read primarily as D in `GDDVF`. The retained V alternative changes the quantity to `YP111` and nothing else in the plaintext. Neither variant is normalized to a historical capacity.

## p213 A2

**Readable German — existing word repairs and shared J/Y interpretation, with three historical ship-name proposals:**

> Weitere Tonnage folgt baldigst. Ferner Rohstofftransport abging heute Peter Benoit. Folgt morgen Bjoern und Babylon.

The names can be compared with contemporary shipping sources. *Lloyd's
Register*, **1917–18**, lists **Peter Benoit** at PES–PET, entry P471, and
three vessels named **Björn** at BJE–BLA, entries B733–735. A shipping notice
in the *Hamburger Fremdenblatt*, **28 December 1915**, evening edition,
printed p3, names the steamer **Babylon**.

| Received field | Name proposal | Extra observed-coordinate changes under the existing J/Y layer |
|---|---|---:|
| `PETERXBENVIT` | **Peter Benoit** | 2 |
| `B9VERN` → conditional `BJVERN` | **Bjoern** | 2 |
| `BAC4LON` → conditional `BACYLON` | **Babylon** | 2 |

These sources establish the spellings, not the November transport identities.
The three Björn entries make a unique vessel identification especially
uncertain. No same-movement witness has been found. Accepting all three
proposals gives the quotation above at **nine observed substitutions and
one source-mask fill**, six substitutions beyond the earlier word edition.
It uses the existing **GD=J** and **DD=Y** hypotheses without another key
assignment. No previously unknown plaintext position is added to the count.

[Register and newspaper crops, exact name costs and source provenance](../../experiments/reval_ship_name_comparison/README.md).

[Source crop](../../experiments/reval_steamer_notice/sources/p213_A2.png). There are 208 printed slots, including C at index 181. Raw:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
WEITERETANNAGEFOL?TBALDIGSTFERNERROHSTOFFTRANSPHRTABGINGHE8TEXPETERXBENVITXFOLGTMORGENXB9VERNUNDBAC4LONX
```

</details>

Three observed-coordinate substitutions and one printed-glyph fill produce:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
WEITERETONNAGEFOLGTBALDIGSTFERNERROHSTOFFTRANSPORTABGINGHEUTEXPETERXBENVITXFOLGTMORGENXB9VERNUNDBAC4LONX
```

</details>

The earlier edition reports more tonnage and raw-material transport, with
`PETERXBENVIT` leaving today and `B9VERN` and `BAC4LON` following tomorrow.
Its literal fields remain in the streams above; the historical spelling
proposals are separately priced in the current reading.

## p213 A3

[Source crop](../../experiments/reval_steamer_notice/sources/p213_A3.png). There are 162 slots with three printed dashes. Raw:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
FUEREUCHWIRDMITALLENKRAEFTENGESORGTXROHAVALXXKMXALLGX?RIEFSDEPXN?YLY1XYYXYN?ANCHX
```

</details>

Filling source index 137 as F and changing index 159 F to X gives:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
FUEREUCHWIRDMITALLENKRAEFTENGESORGTXROHAVALXXKMXALLGXKRIEGSDEPXN?YLY1XYYXYN?ANCHX
```

</details>

Reading: “Für euch wird mit allen Kräften gesorgt.” The received `ROHAVAL` and the closing reference remain unexpanded. Two erased coordinates in that reference are still unresolved; no date or serial is guessed.

## Attribution

Earlier unreviewed repository screens already recognized the first two bodies. The present edition adds the source audit, exact repair costs, the separately retained glyph alternative and the closing source frame. It makes no first historical decipherment claim and changes no baseline key.
