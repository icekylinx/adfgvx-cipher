# A director-departure inquiry with an unresolved reference

The message follows up an earlier telegram and asks whether the director should travel under current conditions, requesting a wired reply. The baseline surname-like token and date field remain literal; the closing reference has two unresolved positions.

**Complete edition by printed page:** [p. 123](../pages/123.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

## p123 B

Childs p123, PDF p126; [source crop](../../experiments/nov4_radio_and_departure_queries/sources/p123_B.png). Key: unchanged published **Nov4–6**.

<details>
<summary>Source and cipher evidence</summary>

**Source transcription — literal received header:**

```text
B) NKJ v LP (04.50 p.m., November 4th)
FUER UKS 1550 (4.11) OBERKOMMANDO BESATZUNGSHEERES VERWALTUNGSSTAB BUKERAST
RICHI-340
```

**Raw output — native 340-slot frame; 160/170 fixed positions:**

```text
ANSCHLIESSENDXTELEGRAMMXROEMISCHX3XDX8511XVOM027XOKTOAERXISTXAUSREISEXDIREKTORSXT4SCHASCHELXUNOERXJETZIGENXVERHMEL4NISSENXRWTRAM?DR?HTAN?WOR?XAUS?AE?TIGX?OEM?SCHX?XD?8698
```

**Edited output — 7 observed-coordinate substitutions and 8 source-mask fills; 168/170 fixed positions:**

```text
ANSCHLIESSENDXTELEGRAMMXROEMISCHX3XDX8511XVOM027XOKTOBERXISTXAUSREISEXDIREKTORSXT4SCHASCHELXUNTERXJETZIGENXVERHAELTNISSENXRATSAMXDRAHTANTWORTXAUSWAERTIGXROEMISCHX?XD?8698
```

</details>

Observed source changes, with zero-based indices: **94 A→G**, **113 V→A**, **114 A→V**, **191 G→X**, **193 X→V**, **206 F→G**, **294 V→X**.

Source-mask fills: **115→F**, **116→X**, **117→A**, **118→V**, **195→F**, **196→A**, **197→A**, **198→A**.

The fixed candidate positions satisfy their exact coordinate pairs. The two unresolved positions remain masked; a complete plaintext re-encryption is not claimed.

**Readable German — complete edited stream, with spacing and punctuation only:**

> Anschliessend Telegramm roemisch 3 D 8511 vom 027 Oktober: ist Ausreise Direktors T4SCHASCHEL unter jetzigen Verhaeltnissen ratsam? Drahtantwort. Auswaertig, roemisch ? D?8698.

**Meaning:** The message follows up an earlier telegram and asks whether the director should travel under current conditions, requesting a wired reply. The baseline surname-like token and date field remain literal; the closing reference has two unresolved positions.

## Name and reference alternatives

The complete baseline reading retains the source-derived token **T4SCHASCHEL** and the date field **027**. The closing **ROEMISCH ? D?8698** contains two unresolved positions, which remain in the readable text. The question mark after *ratsam* is editorial punctuation; the two question marks in the closing reference represent the two unresolved decoded positions.

**Conditional interpretation — optional surname proposal:**

The plausible spelling **TISCHASCHEL** would require two additional observed-coordinate changes: source **69 V→X** and **249 X→V**. Its full conditional stream and exact coordinate witness are included separately in the certificate. This is a local name proposal, not an independently established identity, and it does not change the baseline status or its count of fixed positions. No name assignment is propagated to another message.

The two printed five-dash groups remain visible in the source transcription. Eight source masks are filled for ordinary words; the two reference positions remain unresolved. The clear trailing `LP` lies outside the 340 ciphertext slots.

## Attribution and evidence

Earlier unreviewed repository candidates already suggested these bodies. This edition checks the primary images, preserves conflicting source labels and publishes every frame operation, coordinate substitution and fill. Prior published key recovery keeps its original credit; no first-solution priority is claimed.

[Inputs](../../experiments/nov4_radio_and_departure_queries/inputs.json), [certificates](../../experiments/nov4_radio_and_departure_queries/certificates.json), [earlier candidates](../../experiments/nov4_radio_and_departure_queries/prior_candidates.json) and [reproduction](../../experiments/nov4_radio_and_departure_queries/README.md) provide complete source and positional evidence.

</details>
<!-- CASE-EDITION:END -->
