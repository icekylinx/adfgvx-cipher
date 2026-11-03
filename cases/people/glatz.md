# An enquiry about Glatz's whereabouts

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[ADFGVX Cipher](../../README.md) · [All readings](../README.md) · [Source audit](../../experiments/corpus_attack/SOURCE_FAMILIES.md)

**Records:** p140 B and p149 C. **Result:** 167 of 168 proposed positions have complete coordinate-pair support in a printed witness under the published Nov4–6 key. One damaged glyph needs an explicit reading to complete `KONSTANTINOPEL`.

## Most likely reading

**Readable German:**

> Militär-Mission Konstantinopel. Drahtnachricht über Verbleib Reg. Bmstr. Glatz vom Straßenbau-Sonderkommando 1 erbeteten [wohl: erbeten]. Milverkehr, röm. II A 100166 Ko, durch Admiralstab, Kz. 95537.

**Display notes:** The bracketed `[wohl: erbeten]` is a proposed ordinary-German normalization of the literal `ERBETETEN`. It is a gloss, not a deletion in either exact output. Abbreviation expansions in the meaning below remain interpretations; the following notes distinguish the uncertain institutional terms.

**English meaning:** To the Military Mission in Constantinople. A telegram is requested reporting the whereabouts of Government Master Builder Glatz of Road Construction Special Detachment 1. The closing contains routing and reference information, including transmission through the Admiral Staff and reference 95537.

*Reg. Bmstr.* is probably *Regierungsbaumeister*. The precise institutional meanings of `MILVERKEHR`, `ROEM 2 A 100166 KO` and `KZ 95537` are not established here. The source-supported wording is **ERBETETEN**, with an extra `TE` compared with ordinary **ERBETEN**. The readable edition marks this irregularity; the fixed-length candidate retains all its letters.

**Edited output:**

```text
MILITAERXMISSIONKONSTANTINOPELXDRAHTNACHRICHTUEBERVERBLEIBREGXBMSTRXGLATZVOMSTRASSENBAUSONDERKOMMANDO1ERBETETENXMILVERKEHRXROEMX2XAX100166XKOXDURCHADMIRALSTABXKZX95537X
```

## Source support and remaining repair

Both printed copies contain 336 coordinate slots. In [p140 B](../../experiments/corpus_attack/sources/childs_p140_B.png), the last character of group 64, `VDAF?`, is visibly damaged. All other **335 legible coordinates** directly yield the candidate above. Reading the damaged slot as `G` supplies the `I` in `KONSTANTINOPEL`.

The [p149 C](../../experiments/corpus_attack/sources/childs_p149_C.png) copy has a clear final `G` in that group, but four other coordinate disagreements produce `KONSTANTBNOPEL`, `STRKSSENBAU`, `ERBETETRN` and `4ILVERKEHR`. The proposed candidate costs zero known-coordinate substitutions in p140 and four in p149, plus the one p140 damaged-glyph reading. It is not the absolute minimum-disagreement candidate: retaining `KONSTANTBNOPEL` would lower the combined cost from four to three. The preference for the normal place-name is therefore explicit editorial reasoning.

The [certificate](../../experiments/corpus_attack/source_pair_results.json) records both raw texts, the four substitutions and the source coordinates supporting every proposed letter. The [source inputs](../../experiments/corpus_attack/source_pairs.json) preserve the literal transcriptions and complete headers.

## Dates and provenance

Both headers give **6 November 1918**: 4.00 p.m. in p140 and 7.54 p.m. in p149. The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed pp. 140 and 149 in the [complete scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).

The unchanged **Nov4–6** period key retains the credit recorded in [data/keys.json](../../data/keys.json): **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**, with the public key also supplied by George Lasry in the [2017 discussion](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1). Source comparison, reconstruction, repair analysis and this edition are by **icekylinx and GPT-6 Astra Pro**. No first historical decipherment priority is claimed.

## Reproduce

```sh
python3 experiments/corpus_attack/build_source_pairs.py --verify
python3 experiments/corpus_attack/verify_source_pairs.py
```
