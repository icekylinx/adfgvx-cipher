# November 6 Ringbahn-key instruction: a second three-part witness

The schedule itself is the already established instruction to reuse November key dates for the beginning of December. These p145 witnesses provide independent character-level support for the text, recover a short source group, and expose the differing date and reference layers.

**Complete edition by printed page:** [p. 145](../pages/145.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Third reception restored.** The [p187 B1 fragment](nov13_ringbahn_retransmission.md) adds a separately received witness with an exact origin map for every restored coordinate.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p145 supplies three additional physical witnesses of the instruction
already read in the [p211 lower-B edition](p211_key_schedule.md). They say to
keep the November Ringbahn keys, postpone the December keys, and use the
10 November key for 1 December through the 30 November key for 21 December.
These are the stated instructions; implementation by every station is not
inferred.

The source has **531 typed coordinates**, with a visibly four-symbol group
in part 2 against its advertised length. The declared 532-slot frames give
**266 positions**, **265 fixed raw**. The complete candidates use **5 observed
coordinate substitutions** and **1 fill in the hypothesized added slot**.
Every proposed changed plaintext position is directly supported by a fixed
raw position in the independently inspected p211 source. Conversely, the
p145 raw text directly supports all four earlier p211 word repairs.

## Dates and source identity

<details>
<summary>Literal source transcription</summary>

**Source transcription — literal p145 headers:**

```text
6th NOVEMBER, 1918.
B) WAU (KOW RVA) NKJ (IWE RTS) ASO v LP (02.53 a.m., November 7th)
SS DD 2230 (6/11) 3 TEILE
1 TL RICHI-214
2 TL RICHI-184
3 TL RICHI-134
```

</details>

The [p211 source crop](../../experiments/open_targets_continuation/sources/childs_p211_selected.png)
instead has a **19 November** heading and **22 November** receipt, with
`FUER POT COS VON LP SS DD 2230 3 TLE`. Both copies decode under the unchanged
published **Nov4–6** key. The date layers remain as printed. No date is
rewritten to fit the cipher period or the December instruction.

## p145 B1

[Reviewed source crop](../../experiments/nov6_ringbahn_key_witnesses/sources/p145_B1.png).

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 214-slot frame; 107/107 fixed positions:**

```text
NOVEMBERXRINGBAHNSCHLUESSELNICHTVERNICHTENXNACHRCHEFXGXB848727XXDEZEMBERX1INGBAHNSCHLUESSELTRITTVORLAEUFIGX
```

**Edited output — 1 observed-coordinate substitution; no fills; 107/107 fixed positions:**

```text
NOVEMBERXRINGBAHNSCHLUESSELNICHTVERNICHTENXNACHRCHEFXGXB848727XXDEZEMBERXRINGBAHNSCHLUESSELTRITTVORLAEUFIGX
```

</details>

Observed source changes, using zero-based indices: **46 A→V**.

**Readable German — complete edited stream, with spacing and punctuation only:**

> November-Ringbahnschluessel nicht vernichten. Nachrchef G B848727. Dezember-Ringbahnschluessel tritt vorlaeufig

## p145 B2

[Reviewed source crop](../../experiments/nov6_ringbahn_key_witnesses/sources/p145_B2.png).

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 184-slot frame: one unknown slot inserted at source boundary 33; 91/92 fixed positions:**

```text
NICHTINKRAFTX?MFUERSCHLDESSELERSTERDEZEMBERWIEZEHNTERNOVEMBERUSWBISEINUNDZWKNZIGSTERDEZEMBER
```

**Edited output — 3 observed-coordinate substitutions and 1 inserted-slot fill, under the same conditional frame; 92/92 fixed positions:**

```text
NICHTINKRAFTXDAFUERSCHLUESSELERSTERDEZEMBERWIEZEHNTERNOVEMBERUSWBISEINUNDZWANZIGSTERDEZEMBER
```

</details>

Observed source changes, using zero-based indices: **44 F→V**, **87 X→V**, **127 F→V**.

The visibly short `XFVA` at source positions 30–33 becomes `XFVFA` by adding **F at source boundary 33**. This added value is not counted as a fill of a printed dash. The resulting complete ciphertext is **identical to the unedited p211 lower-B part 2**.

**Readable German — complete edited stream, with spacing and punctuation only:**

> nicht in Kraft. Dafuer Schluessel erster Dezember wie zehnter November usw. bis einundzwanzigster Dezember

## p145 B3

[Reviewed source crop](../../experiments/nov6_ringbahn_key_witnesses/sources/p145_B3.png).

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 134-slot frame; 67/67 fixed positions:**

```text
WIEDREISSIGSTERNOVEMBERXXEMPFANGSBESTAETIGUNGXXNKCHRCHEFX4XBX47857X
```

**Edited output — 1 observed-coordinate substitution; no fills; 67/67 fixed positions:**

```text
WIEDREISSIGSTERNOVEMBERXXEMPFANGSBESTAETIGUNGXXNACHRCHEFX4XBX47857X
```

</details>

Observed source changes, using zero-based indices: **68 F→V**.

**Readable German — complete edited stream, with spacing and punctuation only:**

> wie dreissigster November. Empfangsbestaetigung. Nachrchef 4 B47857.

## Cross-copy repair support and preserved disagreements

All five possible insertions within the short `XFVA` group are priced against
the independently read p211 part 2:

| Source boundary | Observed-coordinate substitutions | Added value |
|---|---:|---|
| 30 | 6 | X |
| 31 | 5 | F |
| 32 | 4 | V |
| 33 | 3 | F |
| 34 | 4 | A |

The boundary-33 frame has the least observed-coordinate cost within this
explicit five-alignment family. The three substitutions concern source
indices **44, 87 and 127**. This comparison uses an actual copy, not a text
selected solely for a higher language score; it still does not identify the
historical stage at which the coordinate was lost.

The reverse support is also exact. In p145 part 1, the unedited letters at
plaintext indices **9, 19 and 67** support the p211 proposals `RINGBAHN`,
`SCHLUESSEL` and `DEZEMBER`. In p145 part 3, unedited position **10** supports
the p211 `DREISSIGSTER` fill. Both source transcriptions remain available;
these observations do not merge the physical records.

The reference labels remain different. p145 has literal `NACHRCHEFXG` in
part 1 and `NACHRCHEFX4` in part 3; the p211 outputs have `NACHRCHEFX4` and
`NACHRCHEFZ4`. Those labels are **not regularized**, even though the schedule
words agree. The numerical fields `B848727` and `47857` likewise stay literal.

**Meaning:** The schedule itself is the already established instruction to
reuse November key dates for the beginning of December. These p145 witnesses
provide independent character-level support for the text, recover a short
source group, and expose the differing date and reference layers. They add
no claim about the behavior of any station or the key of a particular
December ciphertext.

## Attribution and verification

The previously published p211 edition and prior published period-key recovery
retain their separate credit. An earlier unreviewed repository candidate
already read the p145 ending; the new source edition reconstructs all three
printed parts and prices their correspondence to p211. No first-decipherment
priority is claimed.

[Inputs](../../experiments/nov6_ringbahn_key_witnesses/inputs.json),
[certificates and mutual source support](../../experiments/nov6_ringbahn_key_witnesses/certificates.json),
[prior attribution](../../experiments/nov6_ringbahn_key_witnesses/prior_candidates.json),
and [reproduction instructions](../../experiments/nov6_ringbahn_key_witnesses/README.md)
preserve exact source and frame indices, every raw domain, all five local
alignments and full re-encryptions.

</details>
<!-- CASE-EDITION:END -->
