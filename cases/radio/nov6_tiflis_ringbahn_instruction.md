# November 6 Ringbahn-key instruction to Tiflis

Keep the November Ringbahn keys; use the November 10 key for December 1, and continue in the stated sequence.

**Complete edition by printed page:** [p. 146](../pages/146.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

The two-part **section C on Childs p146** tells the Caucasus delegation at
Tiflis to retain November Ringbahn keys and use them for the beginning of
December. Its schedule agrees with independently readable spans in the
[p145 instruction](nov6_ringbahn_key_witnesses.md) and
[p211 lower-B instruction](p211_key_schedule.md), but this dispatch has its
own wording, address and part boundaries. The original
[p146 challenge](../p146.md) is section B; these are two different physical
records.

The literal source contains **365 slots**, including six masked coordinates,
against **368 advertised**. The conditional frames insert three unknown
coordinate slots and produce **184 plaintext positions, 175 fixed before
word repairs**. The complete proposed reading uses **1 observed-coordinate
substitution, 6 source-mask fills and 3 inserted-slot fills**. No printed
slot is deleted or reordered and the published **Nov4–6** key is unchanged.
The insertion positions and complete wording remain stated hypotheses.


**Reviewed source crops:** [p146_C_reviewed.png](../../experiments/nov6_tiflis_ringbahn_instruction/sources/p146_C_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## Source and date layers

[Reviewed source image — source-PDF reference](../../experiments/nov6_tiflis_ringbahn_instruction/inputs.json).

<details>
<summary>Literal source transcription</summary>

**Source transcription — headers and cleartext annotation:**

```text
Page heading: 6th NOVEMBER, 1918.
C) COS v LP (06.46 a.m., November 7th)
FUER COS 2040 (6/11) AN NACHRICHTENKOMMDR KAUKASUS DELEGATION
TIFLIS 2 TLE
1 TL RICHI-176
2 TL RICHI-192
Cleartext ending after part 2: NKJ v LP UM
```

</details>

The dispatch date in the heading and address line is November 6; the
intercept line says November 7. These layers are retained. The separately
printed `NKJ v LP UM` follows the second ciphertext and is not an extra
coordinate group. Exact grouped ciphertext, including every dash and the
invalid printed `W`, is preserved in the
[inputs](../../experiments/nov6_tiflis_ringbahn_instruction/inputs.json).

## p146 C1

Part 1 prints **174 valid coordinates** and advertises **176**. Its `XAAF`
group at source indices 65–68 is visibly short. The displayed frame inserts
one unknown at **source boundary 66** and another at **source boundary 173**.
A boundary is before the original source index of that number. Consequently,
the inserted slots have **model indices 66 and 174**; original source indices
do not shift in the transcription.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 176-slot frame; 86/88 fixed positions:**

```text
RINGBAHNNOVEMBERSCHLUESSELNICHTVERNICHTENX?CHLUESSELERSTERDEZEMBERWIEZEHNTE?NOVEMBERUSWX
```

**Edited output — the same conditional frame; 0 observed-coordinate substitutions, 0 source-mask fills and 2 inserted-slot fills; 88/88 fixed positions:**

```text
RINGBAHNNOVEMBERSCHLUESSELNICHTVERNICHTENXSCHLUESSELERSTERDEZEMBERWIEZEHNTERNOVEMBERUSWX
```

</details>

| Added source boundary | Model index | Supplied coordinate | Plaintext position supplied |
| --- | ---: | --- | --- |
| 66 | 66 | G | 42, S in SCHLUESSEL |
| 173 | 174 | A | 75, R in ZEHNTER |

The first fill changes the short group from `XAAF` to `XGAAF` in the model.
The second adds a coordinate before the final printed `D`; that location is
inferred from the cipher comparison, not a visible blank. Neither fill is
counted as a change to an observed coordinate.

**Readable German — complete edited stream, with spacing and punctuation only:**

> Ringbahn-Novemberschluessel nicht vernichten. Schluessel erster Dezember wie zehnter November usw.

**Meaning:** Keep the November Ringbahn keys; use the November 10 key for
December 1, and continue in the stated sequence.

The exact complete candidate is encrypted and compared against the literal
174-slot source under **all 15,400 ways of inserting two slots**. There is
exactly **one zero-substitution alignment** for that fixed candidate: source
boundaries 66 and 173. The certificate records the cost histogram and the
minimum. This establishes a precise compatibility result within the declared
family. It does not prove that every possible plaintext has been excluded,
or identify when the historical omissions occurred.

## p146 C2

Part 2 prints **191 source slots**, of which **185 are valid coordinates**,
and advertises **192**. The first-line group `VF--` at source indices 35–38
is visibly four slots long. For the displayed raw output, one unknown slot
is inserted at **source boundary 37**. The literal two dashes, the two dashes
in the following `VF--X`, the `W` in `FXXDW`, and the dash in `-DGVD` all
remain source observations.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 192-slot frame; 89/96 fixed positions:**

```text
BISEINUNDZWANZIGSTERDEZEMBERWI?DREISSIG?TERNO?E?BERXEMPFANGS?ESTAETIGUNGX?A8HRICH?ENCHEF4B47857X
```

**Edited output — the same conditional frame; 1 observed-coordinate substitution, 6 source-mask fills and 1 inserted-slot fill; 96/96 fixed positions:**

```text
BISEINUNDZWANZIGSTERDEZEMBERWIEDREISSIGSTERNOVEMBERXEMPFANGSBESTAETIGUNGXNACHRICHTENCHEF4B47857X
```

</details>

The sole observed-coordinate substitution is **source 132 V→X**, supplying
`C` in the proposed word `NACHRICHTENCHEF` where the raw output has `8`.
No numeral elsewhere is relabeled. The complete repair account for the
boundary-37 display frame is:

| Kind | Source index or boundary | Model index | Value supplied |
| --- | ---: | ---: | --- |
| Added-slot fill | Boundary 37 | 37 | A |
| Printed dash fill | 37 | 38 | X |
| Printed dash fill | 38 | 39 | F |
| Printed dash fill | 41 | 42 | X |
| Printed dash fill | 42 | 43 | A |
| Invalid printed W fill | 108 | 109 | V |
| Observed-coordinate substitution | 132 | 133 | V→X |
| Printed dash fill | 174 | 175 | G |

**Readable German — complete edited stream, with spacing and punctuation only:**

> Bis einundzwanzigster Dezember wie dreissigster November. Empfangsbestaetigung. Nachrichtenchef 4B47857.

**Meaning:** Continue through December 21 using the November 30 key, and
acknowledge receipt. The trailing reference **4B47857** is literal under the
published square; its historical numerical assignment is not independently
established here.

### Equal-cost gap alternatives

The verifier tests **all 192 single-gap positions** against the same complete
candidate. Three positions tie at the minimum cost of one observed-coordinate
substitution:

| Source boundary | Added coordinate | Observed substitutions | Source-mask fills | Inserted-slot fills |
| ---: | --- | ---: | ---: | ---: |
| 37 | A | 1 | 6 | 1 |
| 38 | X | 1 | 6 | 1 |
| 39 | F | 1 | 6 | 1 |

All three produce the same displayed raw and edited plaintext. They differ
in which part of the restored `VFAXF` group is attributed to the missing slot
and which to the two printed masks. The certificate preserves each mapping
and its complete repair events. **Boundary 37 is the presentation choice;
the evidence does not distinguish these three gap positions.**

## Independent support and limits

The verifier independently decodes pinned source rows from the earlier
editions, rather than treating their edited prose as direct evidence:

| New proposed span | Independently fixed raw source |
| --- | --- |
| SCHLUESSELERSTERDEZEMBERWIEZEHNTERNOVEMBERUSW | p211 lower B2 |
| BISEINUNDZWANZIGSTERDEZEMBER | p211 lower B2 |
| WIEDREISSIGSTERNOVEMBER | p145 B3 |
| EMPFANGSBESTAETIGUNG | p145 B3 |

These matches directly support the missing schedule letters in C1 and the
schedule/acknowledgment fills in C2. The final `NACHRICHTENCHEF` is a separately
priced lexical restoration from `?A8HRICH?ENCHEF`; the other dispatches print
the shorter `NACHRCHEF` and do not by themselves supply this expanded word.
All three repairs in that word remain editorial.

The new instruction begins `RINGBAHNNOVEMBER` and does not reproduce the
other dispatch's separate sentence postponing the December key. These
records are not merged into one purported identical copy. The agreement
supports the transmitted schedule, without demonstrating that every
station followed it or assigning a key to any particular December message.

## Attribution and reproduction

The source is J. Rives Childs's *General Solution of the ADFGVX Cipher
System*. Published period-key recovery by George Lasry, Ingo Niebel, Nils
Kopal and Arno Wacker, Lasry's 2017 key list, and the already published p145
and p211 editions retain their original credit. Earlier repository OCR is
frozen with recomputed unchanged-key outputs: it separated the first row
of C1 and then merged the remainder of C1 with C2. The current work restores
the physical source frames and makes the word repairs reviewable. It makes
**no first-decipherment claim**.

[Inputs and literal source](../../experiments/nov6_tiflis_ringbahn_instruction/inputs.json),
[certificates](../../experiments/nov6_tiflis_ringbahn_instruction/certificates.json),
[prior OCR comparison](../../experiments/nov6_tiflis_ringbahn_instruction/prior_candidates.json),
and [reproduction instructions](../../experiments/nov6_tiflis_ringbahn_instruction/README.md)
provide every position domain, source/model map, exact re-encryption,
independent supporting span and gap-search boundary.

</details>
<!-- CASE-EDITION:END -->
