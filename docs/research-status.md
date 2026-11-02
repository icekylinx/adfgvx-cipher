# Research status

[ADFGVX Cipher](../README.md) · [Case guide](../cases/README.md) · [Methods](methods.md) · [Experiments](../experiments/README.md)

**icekylinx and GPT-6 Astra Pro · 2 November 2026**

The edition contains 22 challenge entries and 62 other source-reviewed
records in the [two reading tables](../cases/README.md). **p73, p170 and p198 D remain
wholly open.** Other entries range from complete prior readings to partial
recoveries and source-linked reconstructions; they are not all independently
solved original ciphertexts. [Each case](../cases/README.md) states its own
status and supplies its most likely readable interpretation where one is
defensible.

## What the latest work establishes

| Result | Evidence gained | What remains unresolved |
|---|---|---|
| [Osthoff](../cases/other/osthoff.md) and [Glatz](../cases/other/glatz.md) | Six witnesses recover readable military-mission messages; 403/407 candidate positions have complete pair support in a witness. | Three shared source garbles require editorial emendation; one Glatz letter needs a damaged-glyph reading. |
| [p205 finance](../cases/other/p205_A.md) and [naval reporting](../cases/other/p205_B.md) | Six source parts fix 750/757 raw positions and give two complete readable bodies. | Four coordinate substitutions and six unresolved reference positions remain explicit. |
| [Seifert and station traffic](../cases/other/seifert.md) | Source-checked reports distinguish records destroyed from cipher keys kept in personal custody, alongside short service messages and duplicates. | The missing hundreds digit and personal identity are not inferred; earlier station-report readings keep their authorship. |
| [Feigenhaus instruction](../cases/other/p120_p123.md) | Three parts are assembled; a second intercept confirms an exact 164-coordinate suffix. | One deletion, five substitutions and nineteen fills remain conditional; special-vocabulary referents are unknown. |
| [Kress/Tiflis notice](../cases/other/p218_A.md) | Three parts concern Article XII and the German guard; an independent treaty text identifies the provision. | The readable version uses sixteen substitutions and three fills; the damaged article number is not raw recovery. |
| [p146 duplicate group](../cases/p146.md) | A literal five-coordinate duplicate can be removed while preserving every retained coordinate; 117/122 positions are fixed before filling the missing group. | The supplied group and resulting call-sign interpretation remain explicit hypotheses. |
| [p187b adjacent swap](../cases/p187b.md) | One `AD → DA` swap explains both of Norbert's earlier word corrections. All 141 adjacent boundaries were checked. | The seven ending unknowns remain; the historical origin of the reversal is not identified. |
| [p109 near-parallel](../cases/p109.md) | An additional source supports the body; exact multi-witness optimization exposes alternatives and their edit costs. | Language ranking does not resolve every word or the `SAVE`/`SAVA` choice. |
| [p153 shared fields](../experiments/p153_extension/README.md) | Existing partial recovery is extended into linked date, serial and footer constraints; the repaired part-6 template fixes 50/54 positions conditionally. | Numerical labels, three erased coordinates and the repair assumptions are not replaced with guessed values. |
| [p198 exact count frontier](../experiments/p198_category_frontier/README.md) | Across every completion of one partial key and every five-loss/fill witness, three digits require at least thirteen Q/Y positions. | The actual key, damage pattern and historical counts remain unknown. |
| [p198 six-gram calibration](../experiments/p198_joint_six/README.md) | One planted full text, exact loss mask and fills are recovered. | A second true-key control still has a superior wrong candidate; the historical six-gram optimum remains unreadable. |

## Highest-value next directions

### 1. Add independent source constraints

The wider-corpus work now supplies readable positive examples of this route:
repeat transmissions can recover missing groups and individual coordinate
pairs, and multipart assembly can recover the body without changing a key.
Continue searching for both direct ciphertext repeats and re-encrypted
copies whose plaintext overlaps under different published keys. Only
image-reviewed witnesses enter the reading catalogue.

For p198, the [constructive domain proof](../experiments/p198_letter_bounds/domain_witnesses.json)
shows that each individual position can contain any alphabet symbol in some
five-loss witness under either frozen complete-key hypothesis. A separate
witness may be used for each choice; this does not make every entire plaintext
possible. Additional constraints need to act jointly: an authenticated
same-key transmission, source-supported loss locations or a sufficiently long
independent plaintext passage could remove whole families of reconstructions.

For p73, a longer same-key companion or an original dated radiogram is more
informative than another topical guess. The date layers remain inconsistent.
The [archival access follow-up](../experiments/p73_primary_followup/ARCHIVE_ACCESS.md)
identifies an official digitization and catalogue route for existing literature
leads, without treating an uninspected file as evidence. For p170, a trustworthy
original length or an overlapping transmission would directly reduce the
currently unconstrained truncation geometry.

### 2. Calibrate word structure before accepting language scores

The exact four-/six-gram experiments already remove search incompleteness
under their fixed keys and damage models. More stochastic searches over those
same exhausted spaces cannot improve the exact optimum. The remaining issue
includes how the objective ranks texts: the wrong Nov13b candidate also wins
under [independent held-out books](../experiments/open_targets/HELDOUT_CONTROLS.md).

A useful next method experiment is an explicit word/segmentation objective
combined with source-preserving decoding. Fix fresh control messages, keys,
numerals, abbreviations and damage patterns before selecting model settings.
Measure actual text recovery and false preferences. A higher model score, or
agreement between models trained on the same books, is insufficient evidence
for a historical reading. This experiment is proposed here, not reported as
already implemented or successful.

### 3. Constrain p153's shared unknown cells

The [date/serial/footer analysis](../experiments/p153_extension/README.md)
records equality relations across both parts. An independently established
field value or companion part can constrain one square assignment in several
places at once. Propagate only such supported assignments, retain alternatives
and verify both ciphertexts. Formatting conventions and plausible dates alone
do not establish numerical labels.

The [keyword and construction study](../experiments/p153_key_structure/README.md)
records its bounded negative searches and successful controls. Further keyword
or phrase searching should introduce a justified construction family or fresh
calibration, rather than treating a larger unstructured budget as new evidence.

## Acceptance rule

A new reading must state its source, exact key and geometry, every alteration
to a received coordinate, unresolved positions and prior attribution. Full
re-encryption verifies the declared reconstruction. Independent source or
constraint evidence is still needed wherever that reconstruction depends on
an editorial assumption. Search failures remain bounded by their recorded
scope and control performance.
