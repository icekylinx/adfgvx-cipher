# Munich couriers carrying radio operating documents

[ADFGVX Cipher](../../README.md) · [All readings](../README.md) · [Source and certificate](../../experiments/courier_recovery/README.md)

**Records:** the repeated first part p153 E1 / p162 A1 and second parts
p151 D2 / p153 D2 / p158 C2, intercepted on 9 November 1918.
**Result:** a direct continuation with **67 of 68 plaintext positions fixed**,
plus a qualified **134-position reconstruction** of the damaged first part,
using the unchanged published Nov7–9 key. The unit number remains
**GRUKONACH{5,6}02** in the published-key layer. A separately supported
historical condition gives **GRUKONACH602**, as recorded below.

## Most likely reading

The first part is an editorial reconstruction with the source costs below:

> An Ingenieurinspektion Muenchen. Gefr. Geraus und Feldgr. Mahrer als
> Kurier mit Funkbetriebsunterlagen fuer Grukonach{5,6}02 7 Uhr abds.
> nach dort abgefahren.

The best-preserved second-part witness, p158 C2, reads directly without any
source-coordinate change:

> Grukonach{5,6}02 benachrichtigen. Eintreffen hierher drahten.
> Nachrchef 4 B 49909.

**Meaning:** The proposed first part tells the Engineer Inspectorate in
Munich that the two named men left at 7 p.m. as couriers carrying radio
operating documents for `GRUKONACH?02`. The continuation instructs the
recipient to notify that unit and telegraph the arrival back to the sender.

The reconstruction retains the name-like strings `GERAUS` and `MAHRER`;
neither name is independently identified. Their `U` and `H`, respectively,
are not among the positions supported under every fit of both alignment
models. `FELDGR` is retained as an unexpanded abbreviation. The singular
`ALS KURIER` is also retained. Spacing, capitalization and punctuation are
editorial; the reading does not add letters to regularize these expressions.

## What is directly supported

All three second-part records contain exactly 136 coordinates. Under the
known partial square, each fixes 67 of 68 plaintext positions. The p158 C2
text is:

```text
GRUKONACH?02BENACHRICHTIGENEINTREFFENHIERHERDRAHTENXNACHRCHEF4B49909
```

The p151 D2 repeat has `GRU1ONACH` at the beginning, and p153 D2 has
`BENACHWICHTIGEN`; the source edition preserves both. The unaltered p158
witness independently supplies the readable forms of both words.

The `?` is coordinate pair **VF**, still an unassigned square cell with
domain **5 or 6**. It is not a missing or illegible source coordinate.
No spelling or grammatical repair can settle that digit.

### A separately linked conditional reading: GRUKONACH602

The [November 9 operational reports](nov9_operational_reports.md#historical-identification-most-likely-the-6th-reserve-division)
use the same unknown **VF** cell for a reserve-division number. A contemporary
French operational telegram identifies the matching formation as the
**6th Reserve Division**. Accepting that historical identification gives
**VF=6** in the shared Nov7–9 square. The source, its date limits and the
earlier p176b use are documented in the linked edition and its
[context certificate](../../experiments/p170_continuation/military_context.json).

Under exactly that assumption, the courier instruction reads
**“Grukonach602 benachrichtigen”** with no source-coordinate changes.
The first-part reconstruction's matching field also becomes 602 at no
additional coordinate cost. This is propagation of one independently
recorded historical assumption through a shared cipher cell; the courier
message is not a second proof of the digit. Its base domain remains 5/6,
and the damaged first part and proposed part association retain their
separate qualifications.

## First-part damage and explicit reconstruction cost

The first parts both advertise 268 coordinates but actually preserve 259
and 264 slots. Both visibly contain the six-letter group `VXDVDD`, which
the transcription retains. One overstruck glyph in p162 A1 is masked as a
source erasure; its displayed reading is kept separately.

Comparing the two sources without the key finds a five-slot relative gap:
all 260 possible gap starts were tested, and seven tied starts, 151–157,
leave only two known-coordinate disagreements. This does not locate the
other four slots missing from the longer witness.

For the **stated 134-position candidate**, exact alignment gives:

| Alignment model | p153 E1 | p162 A1 |
|---|---|---|
| Retain every source coordinate | Insert 9 slots; change 6 known coordinates; 32 tied minimum fits | Insert 4 slots; change 8 known coordinates; 2 tied minimum fits |
| Delete one received coordinate | Delete 1, insert 10; change 4 known coordinates; 192 tied minimum fits | Delete 1, insert 5; change 6 known coordinates; 14 tied minimum fits |

All source-deletion positions were tested for the second model, and every
tied optimum is preserved. The alternatives have different source assumptions;
neither is silently selected as the true transmission history. Any proposed
fill of the overstruck p162 glyph is accounted for separately from substitutions
of valid source coordinates.

Under the first model, **123/134 proposed positions** have a complete
unchanged coordinate pair in at least one witness for every choice of their
minimum fits. Requiring that support across both models reduces the count
to **118/134**. These are conditional checks of the candidate and the stated
models, not proof that its wording or missing-slot geometry is unique.
The [certificate](../../experiments/courier_recovery/certificate.json)
contains every raw masked-frame reading before the editorial fills and
changes, including garbles such as `MU?NCSEN` and `ALLKURIER`.

## Association, source and credit

The two first-part records explicitly say first part of two, and all three
continuations say second part. The p153 D/E headers both read `RVV v N4` on
the same morning; the first-part `2120 (SY)` field also fits the p151 D
`SY v N4` continuation. Both bodies use the same unresolved `GRUKONACH?02`
field, and the instruction to report arrival follows naturally from the
departure notice. These facts support the association, but the typed log
does not explicitly cross-reference the parts as one original transmission.
The direct continuation remains readable independently of that association.

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, printed pp. 151, 153, 158 and 162 / PDF pp. 154, 156, 161 and 165,
in the [public scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [source inputs](../../experiments/courier_recovery/inputs.json) give
literal rows, headers and reproducible image rectangles. The Nov7–9 key
retains its historical and George Lasry / coauthor attribution in
[the key register](../../data/keys.json).

Source inspection, duplicate recovery, exact candidate accounting and this
edition: **icekylinx and GPT-6 Astra Pro**. No first historical decipherment
priority is claimed.

```sh
python3 experiments/courier_recovery/build.py --verify
python3 experiments/courier_recovery/verify.py
```
