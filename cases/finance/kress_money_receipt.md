# Receipt addressed to General von Kress in Tiflis

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p58 B, PDF p61, records a short receipt routed `COS v NKJ`, received
at 2.05 p.m. on September 21, with `1130 (VON SFA)` in the heading. Its
body addresses General von Kress at Tiflis and ends with the naval attaché
at Sofia. These are readings of this message, without a new independent
identification of the participants or confirmation of the payment.

## p58 B

The [source crop](../../experiments/september_receipt_and_front_inquiry/sources/p58_B_full.png)
contains **148 slots**, matching `RICHI-148`. The unchanged published
**Sep19–21** key gives the following native-frame reading.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — native 148-coordinate frame:**

```text
GENERALVONKRECSTIFLISXXMARKXSECHUENHUNDERZXERHALTENXXMARINE?TTA?HEXSOTIAXX
```

**Edited output — four observed-coordinate substitutions and two damaged-glyph fills:**

```text
GENERALVONKRESSTIFLISXXMARKXSECHZENHUNDERTXERHALTENXXMARINEATTACHEXSOFIAXX
```

</details>

**Readable German — spacing and punctuation, with the one spelling expansion bracketed:**

> General von Kress, Tiflis. Mark [sechzehnhundert] erhalten.
> Marineattaché, Sofia.

The edited stream itself says **SECHZENHUNDERT**. The bracketed German
normalization adds an H for readability; it is not a recovered plaintext
position. Interpreting that word as sixteen hundred is a linguistic
interpretation, not a new numerical-square assignment.

## Source cost and conditional interpretation

The four substitutions are source **62 G→F, 87 F→V, 97 D→G and 104 G→F**.
The rightmost glyphs at **39** and **119** look respectively C-like and
L-like in the [detail crop](../../experiments/september_receipt_and_front_inquiry/sources/p58_B_glyphs.png).
Their coordinate identities are uncertain. They remain `C` and `L` in the
literal transcription and become `?` only in the cipher model. The candidate
fills them with **G** and **D**.

Before editing, plaintext position **59** has domain **24AGRX** and
position **63** has domain **0CLQSX**. The phrase `MARINEATTACHE` selects A
and C, respectively. That language-based choice is disclosed in the ledger.
No source position is inserted or removed, and no key cell is changed. The
source fixes **72 / 74** positions; the edited candidate fixes **74 / 74**
and re-encrypts exactly with those six stated coordinate operations.

The body was already present in an earlier unreviewed repository screen.
The new edition credits the published key and makes its source and editing
assumptions independently checkable. The separate p58 A stubs remain
uncounted context in the evidence package.

[Inputs](../../experiments/september_receipt_and_front_inquiry/inputs.json),
[certificates](../../experiments/september_receipt_and_front_inquiry/certificates.json)
and [reproduction instructions](../../experiments/september_receipt_and_front_inquiry/README.md)
provide the exact source rows and position ledger.
