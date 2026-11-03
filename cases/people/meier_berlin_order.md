# Batum: Lieutenant Meier ordered to Berlin

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

The source advertises **RICHI-150** but contains **149 typed coordinates**. The fifth group in row 3 is visibly `ADAG`, containing four symbols. Supplying one **A** produces `ADAAG` and a complete **75-position** reading without changing any observed coordinate. The recovery is conditional on that local missing-coordinate model.

## p104 D

Childs p104, PDF p107; [reviewed source crop](../../experiments/nov2_acknowledgments_and_personnel/sources/p104_D.png). Key: unchanged published **Nov1–3**.

**Source transcription — literal received header:**

```text
D) POT v NKJ (8.36 a.m., November 4th)
POT ZUR UBERMITTLUNG NACH BATUM (2) 1650
RICHI-150
```

**Raw output — conditional 150-slot frame, inserting one unknown coordinate at source boundary 103; 74/75 fixed positions:**

```text
LTXMEIERXBATUMXSO?ORTBERLINABREISENXBEIMERSXBATLX2XGARDEREGTXMELDENXMILMISS
```

**Edited output — 0 observed-coordinate substitutions; 0 source-mask fills; 1 fill in the hypothesized added slot; same conditional frame; 75/75 fixed positions:**

```text
LTXMEIERXBATUMXSOFORTBERLINABREISENXBEIMERSXBATLX2XGARDEREGTXMELDENXMILMISS
```

The full edited stream re-encrypts exactly under the declared frame and listed changes.

**Readable German — complete edited stream, with spacing and punctuation only:**

> Lt. Meier. Batum. Sofort Berlin abreisen. Beim Ers. Batl. 2. Garderegt. melden. Milmiss.

**Meaning:** The conditional reading orders Lieutenant Meier at Batum to leave immediately for Berlin and report to the replacement battalion designated 2. Garderegt. It does not prove that the journey occurred or establish a biographical identity.

## Two compatible locations for the same missing A

All five insertion boundaries within the short group are checked against the complete proposed text:

| Source boundary | Added value | Observed-coordinate substitutions |
|---|---|---:|
| 100 | A | 2 |
| 101 | D | 1 |
| 102 | A | 0 |
| 103 | A | 0 |
| 104 | G | 1 |

The two zero-substitution alignments produce **the same complete ciphertext and the same plaintext**. Their raw uncertainty differs: boundary 102 leaves the last letter of `MEIER` unresolved; boundary 103 leaves a letter of `SOFORT` unresolved. Neither alignment is preferred as the exact historical loss location. The displayed raw stream uses boundary 103, with the alternative retained in the certificate. The finite comparison concerns this local short-group model and proposed wording, not every imaginable corruption mechanism.

The unit number 2 remains the published-square label, and `ERS`, `BATL`, `GARDEREGT` and `MILMISS` are not silently expanded in the complete German display. No specific biography of Meier is asserted.

## Attribution and reproducibility

Earlier unreviewed repository candidates already identified these bodies. This edition reviews the source images, retains their literal observations and publishes the exact repair or frame account; it makes no first-decipherment claim. The key keeps its earlier published provenance.

[Inputs](../../experiments/nov2_acknowledgments_and_personnel/inputs.json), [full certificates](../../experiments/nov2_acknowledgments_and_personnel/certificates.json), [earlier candidates](../../experiments/nov2_acknowledgments_and_personnel/prior_candidates.json), and [reproduction instructions](../../experiments/nov2_acknowledgments_and_personnel/README.md) preserve the evidence.
