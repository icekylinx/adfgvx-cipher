# Romanian ultimatum and the crossing near Rustschuk

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition: icekylinx and GPT-6 Astra Pro.**

Three newly source-edited parts belong to Childs's six-part message
on printed pp175–176, PDF pp178–179. The repeated header is
`LP v NKJ (5.40 p.m., November 10th); VON UKS KR 0915 (10/11) 6 TLE`.
Its fourth part is the existing [p176a challenge](../p176a.md), whose
breakthrough proposal retains prior credit to **Norbert and Max Baertl
in 2017**. This frozen three-record companion edition left two other
surviving parts unread; separate later editions now address C3 and A6.
Those parts remain excluded from its original three-record count.

The message reports that the Romanian government has presented an
ultimatum to evacuate its territory or lay down weapons. It then reports
French troops beginning to cross the Danube near Rustschuk and fighting
in progress. A later part discusses sending messages and material first
to Hermannstadt. These are statements in the intercepted report, not
independent confirmation of the events or their timing.

## p175 C1

The [first-part source](../../experiments/romanian_ultimatum_companions/sources/p175_C1.png)
has 212 printed slots, including three dashes. Its direct reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ANXOHLXOPXJUDORTX1XAX11212OMXXRUM4ENISCHE?EGI2RUN?STELLTS?EBENULTIMATUMXGEBIETBINNEN24X24XSTUNDENZURAEUMEN
```

</details>

Two observed-coordinate substitutions and three printed-dash fills give:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
ANXOHLXOPXJUDORTX1XAX11212OMXXRUMAENISCHEREGIERUNGSTELLTSOEBENULTIMATUMXGEBIETBINNEN24X24XSTUNDENZURAEUMEN
```

</details>

The body says that the Romanian government has just issued an ultimatum
to clear the territory within the repeated literal `24X24` hours. The
prefix `JUDORTX1XAX11212OM` remains unidentified and unchanged. The
two copies of `24` are not summed or replaced by another duration.

## p175 C2

The [208-coordinate continuation](../../experiments/romanian_ultimatum_companions/sources/p175_C2.png)
directly reads:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ODERWAFFENNIEDE0ZULEGENXFRANZOSENHABENHEUTE?X?XVORMXMITDONAUUEBERGANGBEIXRUSTSCHUKBEGONNENXKAMPFIMGANGEX
```

</details>

One observed-coordinate replacement gives this candidate:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
ODERWAFFENNIEDERZULEGENXFRANZOSENHABENHEUTE?X?XVORMXMITDONAUUEBERGANGBEIXRUSTSCHUKBEGONNENXKAMPFIMGANGEX
```

</details>

It completes the ultimatum with the alternative of laying down weapons,
then reports that French troops began crossing near Rustschuk that
morning and that fighting is in progress. The two unknown time digits
are both the same square cell **GF**, so they must agree if the key is
unchanged. Their value remains in **56789**. All 120 injective square
completions preserve the candidate ciphertext and give five equal-digit
possibilities, each in 24 completions. No historical hour is chosen.

## p176 A5

The [fifth-part source](../../experiments/romanian_ultimatum_companions/sources/p176_A5.png)
contains 168 printed slots, including a full five-dash group. It reads:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
NAC?RICHTEN?NDMATER?ALZUN1E?HSTN4CHXHERMANNSTADTXXKANNMITZUSUEHRUNGVONVERPFLEG?ZXUND
```

</details>

Three observed-coordinate substitutions and four dash fills give:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output:**

```text
NACHRICHTENUNDMATERIALZUNAECHSTNACHXHERMANNSTADTXXKANNMITZUFUEHRUNGVONVERPFLEG?ZXUND
```

</details>

The beginning directs messages and material first to Hermannstadt. The
following provisioning phrase is incomplete in this edition. The ending
`VERPFLEG?ZXUND`, including its anomalous `Z`, remains unchanged; the
last unknown has domain **56789JQSUZ**. Neither that letter nor an
unseen grammatical continuation is supplied from context.

## Optional VERPFLEGSZ completion

The later [A6 coal-train proposal](p176_coal_train_fragment.md) supplies
`KOHLENZUEGEN … GERECHNETWERDEN` after A5's `KANNMITZUFUEHRUNGVON…UND`.
This context motivates **S** in the provision-train abbreviation `VERPFLEGSZ`.
The optional word layer fixes **84/84 positions** by filling the remaining
printed dash, source **50**, as `D`; with source **136 G**, its pair is `DG=S`.
The price above the primary A5 proposal is **one mask fill and zero observed
substitutions**, giving totals of **three observed substitutions and five
printed-mask fills**. No square cell or historical digit is assigned.

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — optional A5 completion conditioned on the A6 continuation; the primary 83/84 reading above remains unchanged:**

```text
NACHRICHTENUNDMATERIALZUNAECHSTNACHXHERMANNSTADTXXKANNMITZUFUEHRUNGVONVERPFLEGSZXUND
```

</details>

The A6 routing field and later tail remain unread. The [supplementary
certificate](../../experiments/p176_verpflegs_joint_completion/certificates.json)
checks the single-event delta and full A5 round trips under all 120 square
completions. [Reproduce the supplement](../../experiments/p176_verpflegs_joint_completion/README.md).
The optional completion is by **icekylinx and GPT-6 Astra Pro**.

## Surviving unread parts and the earlier challenge

The source sequence is C1, C2, C3 on p175, followed by A4, A5, A6 on
p176. C3 has **217** printed slots against a stated length of **222**;
the missing five coordinates have no selected location. A6 has **160**
printed slots, of which **86** are dashes. Both are retained as source
context within this frozen companion edition, with no contribution to its
three-record totals. The later [conditional C3 withdrawal edition](p175_c3_withdrawal_followup.md)
now supplies a readable candidate while preserving all tied loss layouts.
The separate [conditional A6 coal-train fragment](p176_coal_train_fragment.md) now proposes 48/80 positions through 44 printed-mask fills and no observed-coordinate changes; its routing field and later tail remain raw.

A4 is already cataloged as p176a. Its earlier reconstructed text and
missing-block assumptions remain separate from these native-frame
companions. Being part of the same source-labeled message does not
independently prove the earlier reconstructed letters.

## Exact scope of the edition

The three new records contain **588 printed slots**, **580 observed
coordinates**, and **294 plaintext positions**. Their raw readings fix
**284** positions; the separately recorded candidates fix **291** after
**six known-coordinate substitutions and seven printed-dash fills**.
One printed dash and two occurrences of an unknown key label remain.
There is no modeled gap, deletion or key change in those three records.

Earlier unreviewed screening already contained the readable C2 and A5
bodies; C1 was garbled in a shorter OCR-derived frame. The present
contribution is exact source transcription, the full arithmetic and
uncertainty record, and a transparent assembly with prior credit.
No first historical decipherment claim is made.

The [package](../../experiments/romanian_ultimatum_companions/README.md),
[inputs](../../experiments/romanian_ultimatum_companions/inputs.json) and
[certificate](../../experiments/romanian_ultimatum_companions/certificates.json)
preserve all coordinates, domains, repairs, source crops, unread context,
and complete compatibility witnesses for the unresolved fields.

### Header transcription correction

The enlarged [C3 header](../../experiments/romanian_ultimatum_companions/sources/p175_C3_heading_detail.png)
reads **RICHI-222**. An initial reading of 232 was rejected. With 217
literal slots, the unlocated shortage is **five coordinates**. The former
15-coordinate estimate is retained only as a transcription-error note,
not as a source model or an alternative restored body. The three readable
records and their repair counts are unchanged.
