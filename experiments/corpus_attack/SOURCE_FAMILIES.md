# Two military-mission messages, six source witnesses

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro · 2026**

[Osthoff reading](../../cases/other/osthoff.md) · [Glatz reading](../../cases/other/glatz.md) · [All readings](../../cases/README.md)

This follow-up supplies **407 likely plaintext positions** in two messages:
the two-part Osthoff posting order (121 + 118 positions) and the Glatz enquiry
(168 positions). It uses the published **Nov4–6** key, independently read page
images, and parallel printed witnesses. It does not recover a new key or claim
first historical priority for these plaintexts.

The period key is credited to **George Lasry's 24 February 2017 comment** and
the earlier work of **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**.
Their complete provenance remains in [the frozen key](key_snapshot.json).
The source is J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
printed pages 138, 140, 148–149, in the [complete source scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The JSON input records the scan hash, page numbers, crop coordinates and exact
literal transcriptions. The output also retains the original corpus OCR so a
reader can distinguish a transcription correction from a proposed change to
a printed coordinate.

## 1. Osthoff's posting to Turkey is cancelled

### Most likely German reading

> Militärmission Konstantinopel. Kommando des Hptms. der Res. Osthoff nach der
> Türkei und seine Zuteilung zur Militärmission ist aufgehoben. Derselbe ist
> dem 1. Ers. Batl. Eisenbahn-Regmts. zu überweisen. AKO folgt. Auf
> Allerhöchsten Befehl: Chef Militärkabinetts, Frhr. Marschall.

**English:** To the Military Mission in Constantinople. The posting of Captain
of the Reserve Osthoff to Turkey and his assignment to the Military Mission
have been cancelled. He is to be transferred to the 1st replacement battalion
of the railway regiment. The cabinet order will follow. By supreme command:
the Chief of the Military Cabinet, Baron Marschall.

Spacing, punctuation, capitalization and the expansions of abbreviations are
editorial. *Ers. Batl.* is read as *Ersatz-Bataillon*; *AKO* is interpreted as
*Allerhöchste Kabinettsorder*. The ciphertext alone does not establish a
specific biographical identity for Osthoff or add a regiment number absent
from the message. The source's historical spelling **KONSTANTINOPEL** is
preserved. The phrasing *Kommando … ist aufgehoben* concerns this posting and
assignment; it does not say that the Military Mission itself was abolished.

The exact normalized candidate is:

```text
MILITAERMISSIONKONSTANTINOPELXKOMMANDODESHPTMSDERRESOSTHOFFNACHDERTUERKEIUNDSEINEZUTEILUNGZURMILITAERMISSIONISTAUFGEHOBEN
DERSELBEISTDEM1XERSBATLEISENBAHNREGMTSZUUEBERWEISENAKOFOLGTXAUFALLERHOECHSTENBEFEHLCHEFMILITAERKABINETTSFRHRMARSCHALLX
```

### Part 1: a missing group supplied by the other witness

The first part appears as p138 A1 and p148 C1. Both are labelled **RICHI-242**,
but p138 contains only **237 printed slots**. Its group 32 ends in an invalid
**H**, which remains literal in the transcription and becomes an explicit
analysis erasure. No received coordinate is deleted to improve the result.

Trying each of the **238 locations** for one missing consecutive group of 5
gives a unique best alignment **before received index 140**. At that location,
the other witness supplies **XVAXX**. There are only three disagreements
between valid coordinates after this alignment. These are retained in the
source, and the machine-readable certificate lists their exact positions.

The p148 witness has one printed dash. Its direct decryption is:

```text
MILITAERMISSIONKONSTANTINOPELXKOMMANDODESHPTMSDE?RESOSTHOFFNACHDERTUERKEIUNDSEINEZUTEILUNGZURMILITAERMISSIONISTAUFGEHOBEN
```

The other witness supplies a complete pair for the missing **R**. Thus every
one of the **121 candidate letters** has a complete coordinate-pair witness.
The candidate changes **zero known coordinates in p148** and **three in
p138**, in addition to the declared missing-group and erasure fills. This is
the attainable minimum combined known-coordinate cost. Complete pair support
across witnesses does not mean that either literal witness is globally clean.

### Part 2: three shared errors require editorial emendation

The p138 A2 and p149 A2 witnesses both contain 236 slots. The clearer p149 witness
decrypts directly as:

```text
DERSELBEISTUEM1XERSBKTLEISENBAHNREGM1SZUUEBERWEISENAKOFOLGTXAUFALLERHOECHSTENBEFEHLCHEFMILITAERKABINETTSFRHRMARSCHALLX
```

The three proposed readings are explicit, source-costed emendations:

| Plaintext index | Literal in both witnesses | Likely reading | Reason |
|---:|---|---|---|
|11|`UEM`|`DEM`|The dative article in “ist dem … zu überweisen”.|
|20|`ERSBKTL`|`ERSBATL`|The military abbreviation “Ers. Batl.”.|
|36|`REGM1S`|`REGMTS`|The abbreviated genitive “Eisenbahn-Regmts.”.|

The indices are zero-based. These proposals require exactly **three
coordinate changes in p149**: transmitted index31 `A→X`, index210 `V→F`,
and index211 `F→V`. The latter two are an adjacent `VF→FV` exchange. The same
three errors occur in p138, which additionally has `KABIIETTS` where p149
provides `KABINETTS`. The resulting p138 cost is four known-coordinate
changes; its dash in `HOE?HSTEN` is separately filled.

The pair supplies complete coordinate-pair support for **115 of 118 letters**.
The other three are not concealed as a key change or an OCR fix. The
candidate's combined known-coordinate cost is **7**, whereas the unconstrained
minimum across the two witnesses is **1**. The six extra changes are the
three emendations charged separately to each witness.

## 2. An enquiry about Regierungsbaumeister Glatz

### Most likely German reading

> Militär-Mission Konstantinopel. Drahtnachricht über Verbleib Reg. Bmstr.
> Glatz vom Straßenbau-Sonderkommando 1 erbeteten [wohl: erbeten].
> Milverkehr, röm. II A 100166 Ko, durch Admiralstab, Kz. 95537.

**English:** To the Military Mission in Constantinople. A telegram is
requested reporting the whereabouts of Government Master Builder Glatz of
Road Construction Special Detachment 1. The message then gives an
administrative routing/reference ending with transmission through the
Admiral Staff and reference 95537.

*Reg. Bmstr.* is probably *Regierungsbaumeister*. The exact significance of
the reference blocks **MILVERKEHR ROEM 2 A100166 KO** and **KZ95537** is not
established here, so they are preserved rather than given a speculative
institutional expansion. The source-supported text actually reads
**ERBETETEN**, an extra `TE` compared with ordinary **ERBETEN**. The readable
edition marks that irregularity; the normalized candidate does not silently
delete two plaintext letters or invent a different transposition length.

```text
MILITAERXMISSIONKONSTANTINOPELXDRAHTNACHRICHTUEBERVERBLEIBREGXBMSTRXGLATZVOMSTRASSENBAUSONDERKOMMANDO1ERBETETENXMILVERKEHRXROEMX2XAX100166XKOXDURCHADMIRALSTABXKZX95537X
```

### Source fit

Both p140 B and p149 C have 336 printed slots. After correcting OCR against the
images, p140 decrypts directly to this text except for **KONSTANT?NOPEL**.
The last glyph in p140 group64 is damaged; it remains `?` in the literal
transcription. Supplying **X** gives pair **VX** = **I** at plaintext position
24; the parallel's observed **G** gives **VG** = **B** instead. The normal
place-name therefore remains an editorial choice. All **335 legible p140
coordinates** are unchanged.

The p149 witness instead reads `KONSTANTBNOPEL`, `STRKSSENBAU`, `ERBETETRN`
and `4ILVERKEHR`. Four coordinate substitutions would give the candidate.
These remain identified as disagreements with p149; they are not retroactive
changes to its transcription. Of 168 letters, 167 have a complete pair in a
witness and one requires the stated damaged-glyph reading. The candidate's
combined cost is 4, compared with an unconstrained minimum of 3. The extra
cost prefers **KONSTANTINOPEL** over the lower-cost but misspelled
**KONSTANTBNOPEL**.

## Reproduce and inspect

```bash
python experiments/corpus_attack/build_source_pairs.py --verify
python experiments/corpus_attack/verify_source_pairs.py
```

The second command independently splits transmitted columns, reconstructs
the intermediate pairs, re-encrypts the candidates, exhausts the missing-group
locations and recomputes every position's minimum source cost. It imports
neither the project cipher implementation nor the certificate builder. It
does not claim to automate the visual reading of the source images.

| Artifact | Purpose |
|---|---|
|[source_pairs.json](source_pairs.json)|Exact source groups, headers, image crop coordinates and explicit uncertain glyphs.|
|[source_pair_results.json](source_pair_results.json)|Raw plaintext, OCR/source differences, source maps, every correction and every letter's support.|
|[key_snapshot.json](key_snapshot.json)|Fixed complete Nov4–6 square/ranks with external key attribution.|
|[p138A](sources/childs_p138_A.png)|Both parts of the earlier Osthoff witness.|
|[p148 C1](sources/childs_p148_C1.png) and [p149 A2](sources/childs_p149_A2.png)|The later two-part witness.|
|[p140 B](sources/childs_p140_B.png) and [p149 C](sources/childs_p149_C.png)|The Glatz enquiry witnesses.|

The candidate texts are interpretations of the printed records. Shared
transmission or transcription errors can survive in every witness; a
language-plausible repair therefore remains an editorial proposal even when
its coordinate cost is small.
