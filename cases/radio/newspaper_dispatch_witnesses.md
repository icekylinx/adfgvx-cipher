# p166 — a second witness of the newspaper-dispatch request

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Status:** Two newly source-reviewed physical parts, compared with the already published p171 B1/B2 edition. The first part is fully supported by observed coordinate pairs across the copies. In the second, three letter choices remain editorial and one numeral cell remains unassigned.

Source edition and comparison: **icekylinx and GPT-6 Astra Pro**. The unchanged **Nov7–9** key is credited to Lasry, Niebel, Kopal and Wacker. The earlier [newspaper-dispatch edition](newspaper_dispatch.md), its underlying unreviewed body candidates and its repair accounting remain prior work. The p171 records are not added again or altered.

## Source and message

The message tells the Oberpostdirektion Breslau that Berlin newspaper sacks have arrived via Orsova and requests immediate dispatch along the same route, with priority references left as raw `7?3` and `308`.

Childs printed page166 / PDF page169 labels the two parts `B) NKJ v UKS (9.27 p.m., November 9th)`, `AN LP1858 2 TLE`, `RICHI-200` and `RICHI-186`. The page identifies the intercepts as British-station traffic. The p171 witness has a later interception heading; no particular relay chronology is inferred.

Both p166 native frame lengths are preserved. B1 contains a Q-shaped noncoordinate glyph at index174. B2 contains49 printed dashes at indices137–185. Those slots are in the source; filling them is not an insertion of missing coordinates.

## p166 B1

Literal decryption:

```text
OBERPOBTDIREKTIONBRESLAUXGESTERNUNDHEUTEBERLI?ERZEITUNGSSAECKEUEBERORSOVAHIEREINGEGANGENXVERANLASSET
```

Common proposed body:

```text
OBERPOSTDIREKTIONBRESLAUXGESTERNUNDHEUTEBERLINERZEITUNGSSAECKEUEBERORSOVAHIEREINGEGANGENXVERANLASSET
```

p166 needs one observed-coordinate substitution and one mask fill. The p171 copy directly supports both proposed letters. Conversely, p166 supplies complete source pairs for p171's previously repaired N in `DIREKTION` and the two previously erased letters in `ORSOVA` and `EINGEGANGEN`.

All100 common candidate pairs are complete in at least one received copy. The two copies disagree at two observed coordinates; the common candidate costs two substitutions in total and reaches the fixed-frame coordinate-only minimum. This does not prove that their historical common source had no earlier error.

## p166 B2

Literal decryption, with its printed erasures retained:

```text
SQF?Y?3???BEF?E?D???NGA?F?E???MWE?S?V???UES?E?S???3UN?3?8???E?T?C?E???D?O?T?I???T?O?R?J???I?N
```

The previously published p171 edition is the declared comparison target:

```text
SOFORTPOSTBEFOERDERUNGAUFSELBEMWEGEXVORZUGSWEISE7?3UND308XXDEUTSCHEFELDPOSTDIREKTIONRUMAENIEN
```

Applying that target to p166 costs **seven observed-coordinate substitutions and49 fills**. Of the49 filled coordinates,48 are directly present in the raw p171 copy. The remaining fill at173 follows the prior editorial D in `DEUTSCHE`; it is not independently observed in either copy.

| Support for a common pair in part2 | Positions | What it establishes |
|---|---:|---|
|Complete pair in at least one received copy|88|Direct pair evidence, including the still-unassigned XA numeral cell|
|Observed halves from different copies|2|B in `SELBEM` and R in `VORZUGSWEISE`|
|Still editorial pair choices|3|O in `SOFORT`, P in `POST`, D in `DEUTSCHE`|

The mixed B and R pairs are `GX` and `AD`, respectively. For B, p166 observes `?X` and p171 observes `GV`; for R, p166 observes `?D` and p171 observes `AV`. This strengthens those two earlier letter proposals using received coordinates, while retaining the actual contrary coordinates and their costs.

The three unsupported choices are explicit:

| Plaintext position, zero-based | Proposed letter/pair | p166 raw pair | p171 raw pair |
|---:|---|---|---|
|1|O / FX|FV|FA|
|6|P / AA|DA|DA|
|59|D / XV|?V|VV|

For part2, the coordinate-only minimum under the fixed common-frame assumption is eight substitutions across the two copies; this readable target costs twelve. The difference is retained as evidence that language interpretation is doing work. No minimum-cost or unique-original claim is made.

## Numeral and count limits

The priority field remains **`7?3`**, with the XA cell constrained to5 or6 by the unchanged published square. A missing p166 coordinate is supplied from the directly observed p171 XA pair; this recovers a coordinate, not its numerical label. The earlier optional753 historical interpretation remains a separate conditional layer and gains no independent digit evidence from this copy.

The two new p166 records total **386 source slots /193 plaintext positions**:143 raw fixed positions and192 after the declared edition, with eight observed substitutions and50 mask fills. The193-position common body is counted once in the support analysis, while both physical copies contribute evidence. Across the common body,188 pairs occur completely in a received copy, two are supported by mixed observed halves, and three remain editorial.

The existing p171 costs are unchanged. Combining both old and new witnesses gives14 substitutions for the selected common stream, compared with the coordinate-only minimum10. There are no added or deleted coordinates, reordered blocks, key changes or new numerical assignments.

The earlier p171 edition selected the comparison target, so this is **not a blind prediction test**. [The certificate](../../experiments/newspaper_dispatch_witnesses/certificates.json) records every candidate pair, both raw pairs, all source indices, each fill's source support and the conditional minimum. [Inputs](../../experiments/newspaper_dispatch_witnesses/inputs.json) retain the literal glyphs and source images; [the README](../../experiments/newspaper_dispatch_witnesses/README.md) provides reproduction commands.
