# Sevastopol: consent to a personnel transfer

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

## p104 E3

Childs p104, PDF p107; [reviewed source crop](../../experiments/nov2_acknowledgments_and_personnel/sources/p104_E3.png). Key: unchanged published **Nov1–3**.

<details>
<summary>Source and cipher evidence</summary>

**Source transcription — literal received header:**

```text
E) POT v NKJ (9.06 a.m., November 4th)
0810 (2)
3 TL RICHI-140
```

**Raw output — native 140-slot frame; 68/70 fixed positions:**

```text
KOMDEURXRESXJ?EGXBATLX?ISTMITVERSETZGXEINRERSTANDEDXXGOUVXSEWASTOPOLXX
```

**Edited output — 2 observed-coordinate substitutions; 1 source-mask fill; 69/70 fixed positions:**

```text
KOMDEURXRESXJAEGXBATLX?ISTMITVERSETZGXEINVERSTANDENXXGOUVXSEWASTOPOLXX
```

</details>

Observed source changes, with zero-based indices: **41 A→G**, **130 A→G**.

Source-mask fills: **119 C→G**.

The coordinate-pair certificate verifies every fixed candidate position and retains the unresolved source mask. A complete plaintext re-encryption is not claimed for the remaining unknown position.

**Readable German — complete edited stream, with spacing and punctuation only:**

> Komdeur. Res. Jaeg. Batl. ? ist mit Versetzg. einverstanden. Gouv. Sewastopol.

**Meaning:** A surviving third part says that the commander of a reserve Jaeger battalion agrees to a transfer. The battalion field remains unknown. The signature gives the Sevastopol governor abbreviation; no officer identity is supplied.

## Unresolved unit and source glyphs

The source prints C-like noncoordinate glyphs in `GAAXC` and `GXAVC`, at source indices **39** and **119**. The latter is supplied as G to read `JAEG`; the former remains masked. Its resulting one-position battalion field is the literal `?` in both the edited stream and readable display. There is no assignment of an assumed battalion number.

The two observed-coordinate changes repair `EINRERSTANDED` to `EINVERSTANDEN`. The remaining abbreviations, including `KOMDEUR`, remain as transmitted. This source is explicitly part 3; the absent first two parts are not reconstructed.

## Attribution and reproducibility

Earlier unreviewed repository candidates already identified these bodies. This edition reviews the source images, retains their literal observations and publishes the exact repair or frame account; it makes no first-decipherment claim. The key keeps its earlier published provenance.

[Inputs](../../experiments/nov2_acknowledgments_and_personnel/inputs.json), [full certificates](../../experiments/nov2_acknowledgments_and_personnel/certificates.json), [earlier candidates](../../experiments/nov2_acknowledgments_and_personnel/prior_candidates.json), and [reproduction instructions](../../experiments/nov2_acknowledgments_and_personnel/README.md) preserve the evidence.
