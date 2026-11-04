# Osthoff's posting to Turkey is cancelled

To the Military Mission in Constantinople. Captain of the Reserve Osthoff's posting to Turkey and assignment to the Military Mission have been cancelled.

**Complete edition by printed page:** [p. 138](../pages/138.md) · [p. 148](../pages/148.md) · [p. 149](../pages/149.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[ADFGVX Cipher](../../README.md) · [All readings](../README.md) · [Source audit](../../experiments/corpus_attack/SOURCE_FAMILIES.md) · [Reading conventions](../../docs/reading-conventions.md)

Four receptions, p138 A1–A2 and p148 C1 / p149 A2, reconstruct the cancellation of Osthoff's posting to Turkey. Under the published **Nov4–6** key, they jointly support all **121 positions** of the first part and **115 of 118** in the second; three word repairs complete the proposed reading.

## Most likely reading

**Readable German:**

> Militärmission Konstantinopel. Kommando des Hptms. der Res. Osthoff nach der Türkei und seine Zuteilung zur Militärmission ist aufgehoben. Derselbe ist dem 1. Ers. Batl. Eisenbahn-Regmts. zu überweisen. AKO folgt. Auf Allerhöchsten Befehl: Chef Militärkabinetts, Frhr. Marschall.

**English meaning:** To the Military Mission in Constantinople. Captain of the Reserve Osthoff's posting to Turkey and assignment to the Military Mission have been cancelled. He is to be transferred to the first replacement battalion of the railway regiment. The cabinet order will follow. By supreme command: the Chief of the Military Cabinet, Baron Marschall.

The English expands the military abbreviations *Ers. Batl.* and *AKO*. The cancellation concerns Osthoff's assignment. His full identity and the regiment number remain unestablished.

## What the witnesses establish

| Part | Printed witnesses | Direct source evidence | Remaining editorial work |
|---|---|---|---|
| 1 | [p138 A1](../../experiments/corpus_attack/sources/childs_p138_A.png), [p148 C1](../../experiments/corpus_attack/sources/childs_p148_C1.png) | p148 fixes 120/121 positions. The other witness supplies the missing `R` in `DERRES`. All 121 candidate positions have complete coordinate-pair support in a witness. | The earlier p138 copy is five coordinates short. A unique best alignment among all 238 insertion positions supplies `XVAXX` before received index 140. Three other known-coordinate disagreements remain. |
| 2 | [p138 A2](../../experiments/corpus_attack/sources/childs_p138_A.png), [p149 A2](../../experiments/corpus_attack/sources/childs_p149_A2.png) | The two copies jointly support 115/118 proposed positions. p149 independently supplies the `N` in `KABINETTS` and the `C` in `HOECHSTEN`. | Both copies contain `UEM`, `ERSBKTL` and `REGM1S`. Reading `DEM`, `ERSBATL` and `REGMTS` requires three changes in p149 and four in the more damaged p138 copy. |

The literal p149 second part is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
DERSELBEISTUEM1XERSBKTLEISENBAHNREGM1SZUUEBERWEISENAKOFOLGTXAUFALLERHOECHSTENBEFEHLCHEFMILITAERKABINETTSFRHRMARSCHALLX
```

</details>

Two repairs form the adjacent coordinate exchange `VF → FV` at transmitted indices 210–211; the third changes index 31 from `A` to `X`. The [certificate](../../experiments/corpus_attack/source_pair_results.json) records the raw readings, source differences, coordinate maps and repair costs.

## Dates and provenance

The p138 header gives 5 November; the clearer p148–149 transmission was intercepted on 7 November and includes `0015 (6/11)`. Both parts use the unchanged published **Nov4–6** key. The later interception time therefore does not by itself require a new period key.

The historical records are from J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed pp. 138, 148–149 in the [source scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view). The period-key work is credited to **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**, with the public key also given by George Lasry in the [2017 discussion](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1).

Source comparison, reconstruction and edition: **icekylinx and GPT-6 Astra Pro**.

## Reproduce

```sh
python3 experiments/corpus_attack/build_source_pairs.py --verify
python3 experiments/corpus_attack/verify_source_pairs.py
```

The second implementation independently reconstructs the columns, checks all 238 missing-group positions and re-encrypts the candidate readings. The [full source audit](../../experiments/corpus_attack/SOURCE_FAMILIES.md) retains the exact raw texts and unresolved source disagreements.

</details>
<!-- CASE-EDITION:END -->
