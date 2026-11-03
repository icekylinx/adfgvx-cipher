# Osthoff's posting to Turkey is cancelled

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[ADFGVX Cipher](../../README.md) · [All readings](../README.md) · [Source audit](../../experiments/corpus_attack/SOURCE_FAMILIES.md)

**Records:** p138 A1–A2 and p148 C1 / p149 A2. **Result:** a two-part message reconstructed from four printed witnesses under the published Nov4–6 key. The first part has complete coordinate-pair support for all 121 letters. The second has support for 115 of 118 letters; three proposed emendations remain explicit.

## Most likely reading

> Militärmission Konstantinopel. Kommando des Hptms. der Res. Osthoff nach der Türkei und seine Zuteilung zur Militärmission ist aufgehoben. Derselbe ist dem 1. Ers. Batl. Eisenbahn-Regmts. zu überweisen. AKO folgt. Auf Allerhöchsten Befehl: Chef Militärkabinetts, Frhr. Marschall.

**English meaning:** To the Military Mission in Constantinople. Captain of the Reserve Osthoff's posting to Turkey and assignment to the Military Mission have been cancelled. He is to be transferred to the first replacement battalion of the railway regiment. The cabinet order will follow. By supreme command: the Chief of the Military Cabinet, Baron Marschall.

Spacing, punctuation and capitalization are editorial. The expansions of *Ers. Batl.* and *AKO* are interpretations of the military abbreviations. The text concerns Osthoff's assignment; it does not say that the Military Mission itself was abolished. No specific biographical identity for Osthoff or additional regiment number is established.

## What the witnesses establish

| Part | Printed witnesses | Direct source evidence | Remaining editorial work |
|---|---|---|---|
| 1 | [p138 A1](../../experiments/corpus_attack/sources/childs_p138_A.png), [p148 C1](../../experiments/corpus_attack/sources/childs_p148_C1.png) | p148 fixes 120/121 letters. The other witness supplies the missing `R` in `DERRES`. All 121 candidate letters have complete coordinate-pair support in a witness. | The earlier p138 copy is five coordinates short. A unique best alignment among all 238 insertion positions supplies `XVAXX` before received index 140. Three other known-coordinate disagreements remain. |
| 2 | [p138 A2](../../experiments/corpus_attack/sources/childs_p138_A.png), [p149 A2](../../experiments/corpus_attack/sources/childs_p149_A2.png) | The two copies jointly support 115/118 proposed letters. p149 independently supplies the `N` in `KABINETTS` and the `C` in `HOECHSTEN`. | Both copies contain `UEM`, `ERSBKTL` and `REGM1S`. Reading `DEM`, `ERSBATL` and `REGMTS` requires three changes in p149 and four in the more damaged p138 copy. |

The literal p149 second part is:

```text
DERSELBEISTUEM1XERSBKTLEISENBAHNREGM1SZUUEBERWEISENAKOFOLGTXAUFALLERHOECHSTENBEFEHLCHEFMILITAERKABINETTSFRHRMARSCHALLX
```

Two of its three changes form one adjacent coordinate exchange, `VF → FV`, at transmitted indices 210–211; the other is `A → X` at index 31. These are hypotheses about source errors, not assignments to unknown square cells. The complete raw readings, all differences, every plaintext-to-source map and exact candidate costs are in the [certificate](../../experiments/corpus_attack/source_pair_results.json).

## Dates and provenance

The p138 header gives 5 November; the clearer p148–149 transmission was intercepted on 7 November and includes `0015 (6/11)`. Both parts use the unchanged published **Nov4–6** key. The later interception time therefore does not by itself require a new period key.

The historical records are from J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed pp. 138, 148–149 in the [source scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view). The period-key work is credited to **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**, with the public key also given by George Lasry in the [2017 discussion](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1).

Source comparison, assembly, exact repair costs and this edition: **icekylinx and GPT-6 Astra Pro**. No first historical decipherment priority is claimed.

## Reproduce

```sh
python3 experiments/corpus_attack/build_source_pairs.py --verify
python3 experiments/corpus_attack/verify_source_pairs.py
```

The second implementation independently reconstructs the columns, checks all 238 missing-group positions and re-encrypts the candidate readings. The [full source audit](../../experiments/corpus_attack/SOURCE_FAMILIES.md) retains the exact raw texts and unresolved source disagreements.
