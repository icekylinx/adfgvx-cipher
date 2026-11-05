# Shared Hungarian Y: an additional constraint on original p215 C

Prepared by **icekylinx and GPT-6 Astra Pro**.

**An optional shared place-spelling inference narrows the original p215 C closing field from 72 to 56 possibilities when added to the existing J hypothesis.** The separate Y-only layer gives 72, compared with 90 under the earlier numeral layer alone. The 42 all-numerical candidates remain unchanged. This is **not a recovered serial number** or a complete decipherment; the opening remains unresolved.

The new inference assigns coordinate pair **DD**, published baseline label `4`, to **Y**. It keeps the earlier optional `Y→1`, `J→2`, `2→6` numeral assignments and, in the joint layer, the independently proposed `9→J` inference. All unproved labels `0123456789JQY` are cleared before assigning any of them. The baseline key and every source observation remain unchanged.

## Two source bodies support the same cell

| Source | Retained field | Optional place spelling | Y position and original coordinate indices |
| --- | --- | --- | --- |
| p217 A3, operational report | `POEST4EN` | `POESTYEN` | plaintext 57 ← source 139, 222: observed DD |
| p215 B2, inherited 13-mask-fill word layer | `NAG4BANHEG4ES` | `NAGYBANHEGYES` | plaintext 105 ← 268, 23; plaintext 112 ← 187, 296: observed DD |

The two Y positions in B2 need no source fills or substitutions. Its complete place word uses the existing 13-mask-fill candidate, rather than being fully observed natively. P217 A3 has 228 valid native coordinates and no masks. These are separate messages; matching historical place spelling remains a lexical inference.

The [1913 Lutheran directory](https://medit.lutheran.hu/files/nevtar_1913_az_ag_hitv_ev_egyh_egyet.pdf), printed page 37 / PDF page 55, prints **Nagybánhegyes** and **Hódmező-Vásárhely**. The [booksellers’ yearbook volume labeled 1905](https://epa.oszk.hu/02500/02548/00002/pdf/EPA02548_magyar_konyvkereskedok_evkonyve_1905_213-290.pdf), printed page 283 / PDF page 73, prints **Pöstyén**. Removing accents and explicitly expanding Ö to OE gives the compared cipher spellings. These primary references establish spellings, not troop positions or this telegram’s content. The second volume includes 1906 business updates; its 1905 label is not asserted as its publication date.

## Original challenge p215 C

The 248-slot source has 237 observed coordinates and 11 printed masks. Norbert’s inherited two five-coordinate insertions at original offsets 30 and 215 give 258 slots with 21 unknown coordinates. No new insertion, source correction or erased-coordinate fill is adopted here.

**Baseline raw output under that inherited frame:**

```text
ABSXMI?I5XNA6M?LD?XS4NXS4?XN?R?DAKER?SC?XBRINGTENT?N?EFLHTTEZWO?IVI?IONENX?EUSRELAEND?RXENGLXUXF?ATZ?XMITXN??OHLXKOR1S??OSCHX3Y52
```

**Conditional output under the joint numeral/J/Y layer:**

```text
ABSXMI?I?XNA?M?LD?XSYNXSY?XN?R?DAKER?SC?XBRINGTENT?N?EFLHTTEZWO?IVI?IONENX?EUSRELAEND?RXENGLXUXF?ATZ?XMITXN??OHLXKOR?S??OSCHX?1?6
```

The newly assigned Y positions are the two observed DD cells in the opening `S4N`/`S4?` fields. `SYN` is retained as an unidentified field, without claiming a call sign or a corrected opening. The closing pairs are FD,FA,XD,AV, with all eight underlying source coordinates observed.

| Assumptions | Remaining values for a,b in `a1b6` | Ordered distinct closing fields | All-numerical subset |
| --- | --- | ---: | ---: |
| Earlier numeral layer | `0345789JQY` |90|42|
| Numerals + inherited GD=J | `0345789QY` |72|42|
| Numerals + new DD=Y | `0345789JQ` |72|42|
| Numerals + both lexical inferences | `0345789Q` |56|42|

Every closing field has a complete injective square and full source-preserving re-encryption witness. Each witness uses **one square jointly across all 61 certified source/word variants**, rather than assigning a repeated cell separately at each occurrence. The arbitrary witness fills are consistency examples, not proposed historical letters.

## Global checks and retained damage

The package checks 26 certified physical bodies: the 25 other-body raw inventory plus original challenge p215 C. Their nine primary observed DD positions are all listed, including `BAC4LON` in p213 A2. The 54 inherited source/word variants from the J package and the newly included models total 61 variants; they are not 61 independent messages.

The joint layer retains **VASARHE1Y, VASARTELY, BATTREYA and BACYLON**. It does not silently normalize those fields. The earlier J package’s adverse `NIKOLA3EW` observation is also retained; FD cannot simultaneously be J when GD is J.

A separately costed B2 geographical proposal can be re-encoded with Y at DD: **8 observed substitutions + 14 printed-mask fills**, versus the earlier baseline-square proposal’s 18 + 14. Its ten-coordinate reduction simply restores five Y pairs to the original observed DD coordinates. It remains an additional geographical word hypothesis, with all other repairs priced explicitly.

Operational p217 A1–A5 belong to this key cohort. **Original challenge p217 C is a separate 170-slot, 19-column TRUPPENVERSCHIEBUNG message and is not included.** Unknown-key or unframed bodies are not treated as recovered here. Prior authors and geometry credit remain in the [original p215 case](../../pages/215.md#edition-cases-p215), [J constraint](../nov22_nikolajew_constraint/README.md), [operational report](../operational_recovery/README.md) and [B2 source edition](../southern_hungary_positions_part2/README.md).

## Reproduce

[Inputs and source maps](inputs.json), [all closing witnesses and source-cell links](certificates.json), [25-body raw inventory](known_body_inventory.json).

```sh
python experiments/p215_hungarian_y/verify.py --verify
```

Add `--pdf /path/to/childs.pdf` for the two original-source page pixel checks. Add `--directory-1913-pdf /path/to/lutheran_directory_1913.pdf --yearbook-pdf /path/to/booksellers_directory_1905_213-290.pdf` to authenticate both primary references, quote locations and crop pixels. Without supplied PDFs the report explicitly marks their pixels unchecked. No new source images are distributed.
