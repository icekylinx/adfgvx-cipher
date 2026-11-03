# Horses for a cavalry brigade: Poti shipment and handover inquiry

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p59 A, PDF p62, contains three numbered parts under the header
`SSD, COS v ASO (07.50 a.m., September 22nd)`, followed by
`2250 (21.9) 3 TLE`. The second and third parts recover coherent passages
about a shipment at Poti for a cavalry brigade, an abteilung ordered
elsewhere, horses handed over at Poti, and an urgent request for a reply.
The incomplete preceding clause leaves the precise assertion or question
about the handover uncertain.

The **Sep19–21** key is unchanged. This edition counts **two** physical
records, with **225 plaintext positions**. The first part is preserved as
uncounted context because its 225 visible source slots disagree with its
printed length of 220. It is not silently forced into the continuation.

## p59 A2

The [source crop](../../experiments/poti_horse_delivery/sources/p59_A2.png)
has **220 slots**, including seven printed dashes, exactly matching
`2 TL RICHI-220`.

**Raw output — native 220-coordinate frame:**

```text
POTIXVERLADEBXDIEFUER7GBA8?BRIGXBE7THMMTXXDAABTEILUNGKNDERSHINBEO4DHGTXDRING?NDDRAHTEO?ERBRTVEXO0?NDWME??EL?XX
```

**Edited output — 11 observed-coordinate substitutions and three printed-dash fills:**

```text
POTIXVERLADENXDIEFUER7XKAVXBRIGXBESTIMMTXXDAABTEILUNGANDERSHINBEORDERTXDRINGENDDRAHTEODERBRTVEXO0?NDWME??EL?XX
```

**Readable German — spacing of the conservative partial candidate, with its opaque ending retained:**

> ... Poti verladen, die für 7. Kav. Brig. bestimmt. Da Abteilung
> andershin beordert. Dringend drahte oder BRTVE. O0?NDWME??EL? ...

The leading ellipsis marks missing syntactic context from the unresolved
first part, not an added coordinate gap in A2. The closing ellipsis marks
the unfinished syntax; it does not hide further decoded A2 labels. This reading fixes
**106 / 110 positions** after the disclosed edits. The abbreviation
`KAV` is an editorial word repair; its leading **7** is the unchanged
raw label. The final fragment remains unresolved and is not polished into
a complete sentence.

### Conditional interpretation of the opaque ending

One contextually plausible extension is shown below. It requires **25
observed substitutions and seven dash fills in total**, or **14 additional
substitutions and four additional fills** beyond the conservative candidate.

**Conditional interpretation — costly full A2 hypothesis, excluded from the main reading counts:**

```text
POTIXVERLADENXDIEFUER7XKAVXBRIGXBESTIMMTXXDAABTEILUNGANDERSHINBEORDERTXDRINGENDDRAHTEODERBRIEFXOBUNDWEMDIESEXX
```

This would produce “... Brief ... ob und wem diese ...” before the next
part. It is guided by the following part and by language, with substantial
changes to observed source coordinates. It is not independent evidence
for the damaged letters. Its final `DIESE` and the next part's initial
`DIESE` are both retained; neither is deleted to smooth the join. The
certificate records its exact round trip and all additional costs separately.

## p59 A3

The [source crop](../../experiments/poti_horse_delivery/sources/p59_A3.png)
contains **230 slots**, with **31 printed dashes**, matching
`3 TL RICHI-230`. Restoring the dash groups omitted by the earlier OCR
is essential to preserving the source's frame.

**Raw output — native 230-coordinate frame:**

```text
D?ES?4?FER1E??X???I?EBERGE?E?WUGWE?XF?R?ERBALQIG?T?ANTWIRTA??UNSE?ZNFU??S1RZCH?79??7070V9?15X?XXXGEN?DOX?2XTBXP?47?
```

**Edited output — nine observed-coordinate substitutions and 23 printed-dash fills:**

```text
DIESEXPFERDEINXPOTIUEBERGEBENWURDENXFERNERBALDIGSTXANTWORTAUFUNSERENFUNKSPRUCH?79??7070V9?15X?XXXGENKDOX?2XTBXP?47?
```

**Readable German — spacing and punctuation, with the unresolved reference fields kept literal:**

> ... diese Pferde in Poti übergeben wurden. Ferner baldigst Antwort
> auf unseren Funkspruch ?79??7070V9?15X?XXX. Gen. Kdo. ?2. TB. P?47?

The ellipsis marks the unfinished preceding clause. The fragment can be
part of a question about delivery; it does not independently prove that
the delivery occurred. The main reading fixes **107 / 115 positions**.
All eight unresolved positions are in the reference/footer portion. The
literal `V`, repeated `70`, and other surviving labels are preserved;
there is no guessed date, time, corps number or reference.

## Domains, source costs and first-part conflict

The [certificate](../../experiments/poti_horse_delivery/certificates.json)
lists every source-coordinate pair, raw domain, substitution, fill and
changed plaintext position. Raw fixed-position totals count single-symbol
algebraic domains, including erroneous received letters; they are not an
accuracy score for the historical reading.

The four remaining A2 erasures independently allow **1,296** complete
plaintexts. The eight remaining A3 erasures independently allow
**1,679,616**. These are exact factorized counts under the unchanged
complete square and the stated main edits, with finite re-encryption
witnesses retained. No completion is selected as historical.

The [first-part crop](../../experiments/poti_horse_delivery/sources/p59_A1.png)
shows **225 slots** under `RICHI-220`. All **221** possible consecutive
five-slot deletions are retained as diagnostic frames. Two illustrative
placements expose transport-related fragments, but neither establishes
a complete clean reading or a unique historical geometry. A1 therefore
remains outside the catalog and all counts in this edition.

The counted two records use **450 source slots**, **412 valid source
coordinates**, **20 observed-coordinate substitutions** and **26 dash
fills**, with **12 dashes still unfilled**. There is no length change,
source deletion or key change in these two records.

The published key and the earlier partial A2 repository candidate retain
their credit. No historical first-solution claim is made. The
[inputs](../../experiments/poti_horse_delivery/inputs.json),
[earlier candidates](../../experiments/poti_horse_delivery/prior_candidates.json)
and [reproduction instructions](../../experiments/poti_horse_delivery/README.md)
preserve the full source and the limits of this reading.
