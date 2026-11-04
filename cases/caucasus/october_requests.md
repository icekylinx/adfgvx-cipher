# October routing, weather and personnel requests

The records ask Westernhagen to return for an urgent discussion of market conditions, transmit requests concerning weather and an inspector, and preserve an exact Sofia service message. The purchasing request stresses that reliable local information is needed before buying begins.

**Complete edition by printed page:** [p. 62](../pages/062.md) · [p. 63](../pages/063.md) · [p. 65](../pages/065.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[All cases](../README.md) · [ADFGVX Cipher](../../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Status:** Four source-reviewed records under the previously published
**Oct4–6 key**, with different levels of certainty. The Sofia record is an
exact reading. The Westernhagen request uses five explicit coordinate repairs.
The weather instruction depends on two unmarked source deletions. The
inspector request is only partially edited; a difficult 21-character expression
remains unassigned. Source review: **icekylinx and GPT-6 Astra Pro**. Earlier
key credit: **J. Rives Childs, George Lasry, and Lasry–Niebel–Kopal–Wacker**.

The [source package](../../experiments/october_requests/README.md) preserves
842 literal slots, every invalid glyph and header, all coordinate domains,
costed editorial changes and re-encrypted witnesses. No new key or first
historical decipherment is claimed.

## p62 A — Sofia leaves the Ringbahnverkehr

Header: `ASO v LP (04.50 p.m., October 4th); 1030 (4.10); RICHI-124`.
The heading is October 4, 1918. All 62 plaintext positions are directly fixed:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
SOFIAXAUSRINGBAHNVERKEHRAUSGESCHIEDENXXNACHRICHTENCHEF4BX49287
```

</details>

**Readable German:**

> Sofia. Aus Ringbahnverkehr ausgeschieden. Nachrichtenchef 4B. 49287.

The notice says that Sofia has left the `Ringbahnverkehr`. The radio-traffic
context suggests a circuit-service meaning, but an independent contemporary
definition of the term has not been established here. The German token is
therefore retained without a definite technical expansion. The reference
`4BX49287` is literal and is not expanded into an unprinted formation or date.
There is no coordinate substitution, erasure fill or layout change.

The source separately prints `QUITTUNG VON WAU` and `NKJ OSM ASO LP UM`.
These are clear service annotations, outside the encrypted body. They are
preserved without inferring an unprinted acknowledgment time.

Source: [p62 A](../../experiments/october_requests/sources/childs_p62_A.png).

## p65 A — Accelerate Westernhagen's return

Header: `COS v NKJ (3.18 a.m., October 5th); DEUTSCHE DELEGATION 2355 (4/10);
RICHI-260`. The heading is October 4, 1918.

**Readable German — editorial reading:**

> Hptm. v. Westernhagen. [0] Bitten Rückkehr beschleunigen, da über dortige
> Marktlage dringend Bericht benötigen, mit Einkauf beginnen wollen.
> Deutkauf.

The request asks the captain to return sooner because an urgent report on
the local market is needed before purchases begin. The `0` after the
addressee remains the literal source-derived symbol; it is not silently
converted to punctuation. `DEUTKAUF` is retained as the signature token.

The raw 130-character inverse is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
HPTMXVXWESTERNHA5ENX0BITTENRUECLKEHRBESCHLEUNIGENDAUEBERDOUTIGEHARKTLAGEDRINGENDBERICHTBENOETIGENMITEINLAUFBEGINNENWOLLENXDEUTKAUF
```

</details>

Five single-coordinate substitutions give `WESTERNHAGEN`, `RUECKKEHR`,
`DORTIGE`, `MARKTLAGE` and `EINKAUF`. All five printed glyphs were checked
against the scan; they are explicit editorial repairs, not corrected manual
transcription errors. The source independently fixes the rank and `V` before
the surname. The later [p70 A1/A2 request](october_caucasus.md) supplies a
separate Westernhagen surname and market-report witness. No forename or
identity beyond the source is assigned.

| Source index, zero-based | Printed group / character | Coordinate repair | Resulting word |
| ---: | --- | --- | --- |
| 132 | 27 / 3 | `X→V` | `RUECKKEHR` |
| 170 | 35 / 1 | `G→F` | `DORTIGE` |
| 202 | 41 / 3 | `G→X` | `WESTERNHAGEN` |
| 222 | 45 / 3 | `X→V` | `EINKAUF` |
| 242 | 49 / 3 | `A→F` | `MARKTLAGE` |

Source: [p65 A](../../experiments/october_requests/sources/childs_p65_A.png).

## p62 B — Date groups before weather-observation telegrams

**Readable German — conditional two-deletion frame; reference field unresolved:**

> Frontwetterwarte. Bitte Obs. Telegr. stets Datumgruppen voranzustellen,
> sonst Meldg. wertlos. FEWEWA?10.

The instruction asks for date groups to precede observation telegrams,
warning that the reports are otherwise worthless. The closing label
`FEWEWA?10` retains one unknown character.

The source is headed `COS v NKJ (03.40 a.m., October 6th); 1540 (5);
RICHI-186`, beneath the October 5 page heading. It contains **188 slots**.
The reading retains the two established conditional layouts: delete either
index 79 or 80, one of the adjacent `FF` across `FFDGF FGAFRG`, and the
final `X` at 187. Both give the same 186-coordinate frame.

### Corrected glyph position and reference uncertainty

The second source group reads **`FVFEF`**, correcting the earlier
transcription `FVEFF`. The printed `E` is at source index **8**, not 7.
Consequently the `L` in `WERTLOS` is directly observed, while the first
character of the closing `?10` is not. The source's `R` in the six-character
`FGAFRG` group remains a separate mask.

The reference unknown has pair `?F` and domain **`018MRV`**. A decimal-only
interpretation still permits **`010`, `110` or `810`**. The previously
printed `FEWEWA110` is one compatible completion; the current edition
leaves the field open. It fixes **92/93 proposed positions**, with two
observed-coordinate substitutions and one mask fill. The conditional raw
frame fixes **91/93**.

<details>
<summary>Raw reading, source changes and layout comparison</summary>

**Raw output — conditional deletion of source 79 or 80, and final source 187:**

```text
FRONTWETTERWARTEXLITTEOBSXTELEGRXSTETKDATUMGRUPPENVORANZUSTELLENSONSTME?DGXWERTLOSXXFEWEWA?10
```

`LITTE→BITTE` changes source 45 from `F` to `G`; `STETK→STETS` changes
157 from `V` to `G`. Filling the `R` mask at 84 with coordinate `F` supplies
the `L` in `MELDG`. The `E` mask at 8 stays unfilled.

| Operation | Original source index | Printed location |
| --- | ---: | --- |
| Delete one adjacent `F` | 79 or 80 | Group 16 / 5 or group 17 / 1 |
| Delete final `X` | 187 | Group 38 / 2 |
| `F→G` for `BITTE` | 45 | Group 10 / 1 |
| `V→G` for `STETS` | 157 | Group 32 / 2 |
| Fill literal `R` as coordinate `F` | 84 | Group 17 / 5 |
| Retain literal `E` as an unfilled mask | 8 | Group 2 / 4 |

The verifier checks all **17,578** ways to delete two source slots against
this partial template and the published key. The two layouts above remain
the only minima at two observed substitutions. The source marks neither
deletion. The comparison leaves the reference character unasserted; it
also preserves all six source-compatible completions and their exact
additional one-mask-fill cost.

Printed locations follow the actual six-character group rather than
uniform groups of five. The [input review](../../experiments/october_requests/inputs.json)
retains the earlier transcription and reference proposal.

</details>

Source: [p62 B](../../experiments/october_requests/sources/childs_p62_B.png).

## p63 A — A partially readable inspector request

Header: `LP v NKJ (12.53 p.m., October 6th); 1754 (5.10) POT FÜR OHL AN
DEUTSCHEN FEZDEIRENBAHNCHEF (4.10); RICHI-54`. The heading is October 4, 1918.
The literal spelling `FEZDEIRENBAHNCHEF` is preserved. The body has **54
groups of five slots**, or 270 slots; the source field remains `RICHI-54`.

The raw inverse is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
E?BITTEUEBER?EID5OGJEEINESBESRIEBSUNDVASCHIWNENMECH8ISCHENKONTROLLEWRSGENERALVSNKRESSEINVERSTAODENDEUTSCHEDELXKASKXABTXZXNRX474DG1MOOLX
```

</details>

A limited editorial reading, costing **12 known-coordinate substitutions
and two erasure fills**, is:

**Readable German:**

> Erbitte Übersendung je eines Betriebs- und [21-character technical
> expression unresolved] Kontrolleurs. General von Kress einverstanden.
> Deutsche Del. Kauk. Abt. Z. Nr 474D. Gemoll.

The request concerns inspectors, states Kress's agreement, and carries a
German Caucasus delegation reference. The middle raw span,
`VASCHIWNENMECH8ISCHEN`, suggests a technical qualification, but normalizing
it to `MASCHINENMECHANISCHEN` would raise the total to **28** known-coordinate
substitutions. That full normalization is not accepted. All 21 positions are
left as `?` in the published partial template, and no witness filler is
presented as recovered text.

The proposed surname `GEMOLL` has an independent clear-header witness in
**p69 B1/B2**, which explicitly addresses `HPTM GEMOLL`. Here the raw ending
is `474DG1MOOLX`; the two letter repairs are costed. The proposed division
`474D | GEMOLL` is retained as an editorial division; it does not create a
first initial or expand the reference.

Source: [p63 A](../../experiments/october_requests/sources/childs_p63_A.png).

A [separately priced technical-word proposal](../../experiments/p63_optional_technical_reading/README.md)
reads `MASCHINENTECHNISCHEN` after treating one raw W as a surplus interim
pair. It keeps both printed D coordinates in the full transmitted witness
and adds three observed substitutions to the existing twelve. The optional
model therefore costs 15 substitutions, two dash fills and two surplus
interim coordinates. Its unique minimum is conditional on a retrospective
word template; the primary 21-position unresolved span above remains unchanged.

## Attribution and limits

These source editions use an earlier published period key. The adjacent p64
Hagelin/Nobel body is explicitly interpreted in Lasry and colleagues' §6.6
and Table 5 and is not part of this package. Absence of an individually
printed interpretation of the four records above is not a first-decipherment
claim. The differing headings, origin fields and reception dates remain
separate source fields. None of these records establishes p73's date,
plaintext or key.

</details>
<!-- CASE-EDITION:END -->
