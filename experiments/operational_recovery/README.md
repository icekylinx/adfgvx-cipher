# Source-checked operational dispatches on pp180, 217 and 230

<a id="source-checked-operational-dispatches-on-pp-180-217-and-230"></a>

Prepared by **icekylinx and GPT-6 Astra Pro**. The transposition and square
snapshots are the published Lasry-team period keys, credited in
`data/keys.json`. This package supplies reproducible source readings and
explicit editorial proposals; it does not claim that these dispatches were
never deciphered before.

## What is recovered

Eight surviving parts contain 1,632 coordinate slots, representing 816
plaintext positions. The source-checked transcription has one printed dash.
With the published baseline key labels, 815 positions have singleton domains.
That count includes numerical labels and visibly erroneous letters, so it is
not a count of correctly recovered German characters.

| Record | Source slots | Raw fixed / positions | Proposed coordinate substitutions | Dash fills |
| --- | ---: | ---: | ---: | ---: |
| p180 A, part 3 | 156 | 77 / 78 | 9 | 1 |
| p217 A, part 1 | 228 | 114 / 114 | 0 | 0 |
| p217 A, part 2 | 240 | 120 / 120 | 0 | 0 |
| p217 A, part 3 | 228 | 114 / 114 | 0 | 0 |
| p217 A, part 4 | 196 | 98 / 98 | 2 | 0 |
| p217 A, part 5 | 122 | 61 / 61 | 2 | 0 |
| p230 A, part 3 | 232 | 116 / 116 | 7 | 0 |
| p230 A, part 4 | 230 | 115 / 115 | 1 | 0 |

The source images, their hashes, literal rows, header readings, and the
individual edit positions are included. All eight source frames agree with
their printed lengths. OCR restoration is distinct from editorial repair:
for example, the p217 fifth part restores a whole source-visible `VVXFX`
group and final `VA` that the OCR omitted. Those are not invented coordinates.

### Page 180: a short withdrawal report

The surviving third part reads, after the ten explicit coordinate decisions:

```text
BEIGIURGIUFOLGTFEINDLANGSAMXBRAILAXFOCSANIGERAEUMTX11XARMEEKEINEEREIGNISSEXOKM
```

In ordinary prose: near Giurgiu, the enemy follows slowly; Braila and Focsani
have been evacuated; no events are reported for the 11th Army. The sender
abbreviation is OKM. The source date is uncertain and remains so. The `11`
proposal includes a coordinate repair to the already known `1` cell; it is
not a second assignment of `1` to an unresolved square cell.

### Page 217: five connected parts of the 24 November report

The source gives a 24 November, 22:30 origin time and an intercept at 01:36
on 26 November. The first three parts decrypt without coordinate repairs.
Their numerical labels require the separately stated historical hypothesis
below. Under that hypothesis the dispatch reports:

* No news from an unresolved command designation; O.K. Scholtz's 16th
  Landwehr and 226th Infantry divisions are marching into the assembly area,
  with the latter's rearguard south of Rimnic Valcea.
* The 11th Army and Alpenkorps situation is unchanged. There was no outward
  transport on the 22nd because of coal shortages. The 6th Reserve Division
  is southeast of Oroshaza. The following formation label is damaged and
  remains `21?6 D` under the partial interpretation.
* A.O.K. is at Szolnok. One battalion of R.I.R. 21 has arrived at the
  damaged place name `POEST?EN`; the whereabouts of other battalions are
  unknown. The phrase describing those battalions is damaged too.
* The battalions were apparently misdirected. The Czechs refuse their stay
  and intend to permit passage only after disarmament.
* Massow in Budapest has been asked to clarify those last questions.

The last two parts need two coordinate substitutions each to read
`FEHLGELEITET`, `CECHEN`, `ERSUCHT`, and `KLAEREN`. The historical spelling
`CECHEN` is preserved. Part 1's `KEENNE` is retained in the certificate;
normalizing it to *keine* would shorten the plaintext and is outside this
same-length edition. Footer labels are preserved rather than guessed.

### Page 230: the surviving third and fourth parts

The source explicitly says that the first and second parts are missing. The
page is dated 30 November; the surviving intercept header gives 1 December.
With the stated local repairs and optional label interpretations, the main
body locates the 226th Infantry Division northwest of Hermannstadt, the
16th Landwehr Division around Muehlbach, and the 218th Division in the
Hatszeg–Livazeny area. A third numbered section places General Command 63
at Kronstadt. The next part places the 89th Division and a damaged `3L3`
division field around Kronstadt, a Bavarian cavalry brigade of unresolved
number around Fogaras, and announces an OKM headquarters move to Muehlbach.

These numbers are historically interpreted, not cipher-only identifications.
The cavalry brigade's raw `0` is left unassigned. The damaged `3L3` field
has not been replaced with `303`. `LIVAZENY` combines a counted source
repair (`C` to `Z` in baseline plaintext) with a separate lexical `7` to `Y`
label interpretation. A final, separate lexical layer reads the surviving
`Q` in `QUART` as ordinary `Q`. The numeric-only and separator layers do not
silently assume that letter assignment.

## Optional, injective label interpretations

The published squares remain unchanged. Each hypothesis first clears all
potentially arbitrary labels in its defined set and then assigns only the
specified cells. Thus two cells never receive the same symbol, and the
remaining cells share one pool of unused symbols. A baseline `7`, for
example, is not assumed to be a true digit 7 merely because its cell has
not yet been identified.

| Period | Baseline labels treated as unresolved | Optional assignments |
| --- | --- | --- |
| Nov 22–24 | `0123456789JQY` | `Y→1`, `J→2`, `2→6` |
| Nov 28–Dec 1 | `0123456789JQXY` | Historical layer: `X→1`, `J→2`, `8→6`, `4→8`, `5→9`, `2→3` |
| Nov 28–Dec 1 | Same | Additional separator convention: `Y→X` |
| Nov 28–Dec 1 | Same | Additional lexical inference: `7→Y` |
| Nov 28–Dec 1 | Same | Separate lexical inference: `Q→Q` |

For Nov 22–24 the unchanged fields `YYARME`, `Y2LDW`, `JJ2ID`, and `2RD`
simultaneously support 11th Army, 16th Landwehr, 226th Infantry, and 6th
Reserve Division. The same assignment turns `AMJJ` into *am 22* and
`RIRJY` into R.I.R. 21. In particular, interpreting both baseline `Y` and
baseline `J` as 1 would violate the bijection and is not allowed.

The historical source is the contemporary telegram by Franchet d'Esperey,
19 November 1918, 22:40, reporting formations as of 11 November: document
39, printed p79 (PDF page 153), in *Documents diplomatiques français sur
l'histoire du Bassin des Carpates, 1918–1932*, volume I, edited by Magda
Ádám, Akadémiai Kiadó, Budapest, 1993. The book reproduces the telegram with
archive reference AG. 4N 58, c/63, d/10. Its provenance and PDF hash are
recorded in `experiments/p170_continuation/military_context.json`.

The document lists the four Nov 22–24 formations and also 218th Infantry,
89th Infantry, and 303rd Infantry divisions. Its entry for the 89th reads
`89e D.I.?`: the contemporary source itself marks this identification as
tentative. Consequently, the proposed baseline `5→9` assignment is weaker
than the clean unit identifications and remains tentative within the optional
map. This provides contemporary
support for the later-period interpretation; it does not independently
establish every unit's later location. The General Command 63 parallel in
the p163 withdrawal edition is corroboration under that edition's own
explicit contextual and editorial assumptions. The `Y→X` step is a display
convention for separators, not proof that the original encipherer literally
used `X`. The `7→Y` step is a lexical inference from `BA7R` and the proposed
place spelling. The `Q→Q` step comes from unchanged p230 A4 plaintext
position 80, square cell `DF`, read from source coordinates 10 and 96 (all
positions here one-based). It is not affected by the neighboring
`HEUPT`-to-`HAUPT` repair. The certificates keep these layers separate.

## Reproduction and limits

```bash
python experiments/operational_recovery/verify.py --verify
python experiments/operational_recovery/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

The verifier checks the stored published keys, source-crop hashes, complete
coordinate rows, frame lengths, and the historical-context dependency. It
reuses the independent column-offset inverse in `withdrawal_recovery` and
cross-checks every domain against the project cipher reader. Editorial
recipes operate in baseline-label space, and the certificates separately
enumerate each known-coordinate substitution and dash fill. Conditional
square interpretations are then applied to both the unchanged source and
the proposed edition.

Every reading also has a globally consistent complete-square and source
filling witness that re-encrypts exactly. The witness fills unknown cells
and residual coordinates deterministically; it is **not** a proposed
historical plaintext. Per-position domains should not be mistaken for
independent choices: the same square cell must retain one value throughout
all messages under that key.

No missing first or second part of p230, missing other part of p180, or
damaged p217 numerical field has been supplied by these certificates. No
language-model score is used as proof, and no baseline key is changed.
