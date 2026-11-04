# p178: source edition of the naval armistice order

**Prior body identification and historical interpretation:** George Lasry,
Ingo Niebel, Nils Kopal and Arno Wacker, *Deciphering ADFGVX messages from
the Eastern Front of World War I*, published online in 2016 and in
*Cryptologia* 41(2), 101–136 (2017),
[DOI](https://doi.org/10.1080/01611194.2016.1169461).
Their author manuscript, printed p23, explicitly discusses Childs p178 A
and B, including the cease-fire, U-boat instructions, self-defense and
requested passage through neutral waters. No new body-discovery priority
is claimed here.

**Current contribution:** a complete source-level German edition,
two explicit short-group insertion hypotheses, exact coordinate-repair
costs, unresolved numeric domains and a reproducible certificate, by
**icekylinx and GPT-6 Astra Pro**. The published Nov10–12 key is unchanged.

## What the order says

The two addressee labels are `MMD` and `SDOKOMMANDO`, followed by
`VONSKLSKL`. The first instruction directs immediate transmission to all
forces by every available means. The body states that the armistice comes
into force at noon on 11 November, orders the cessation of all war actions,
and instructs naval forces to assemble at their bases according to the
orders of their commanders.

The next section orders an enciphered notice to all U-boats: the armistice
has been concluded, but enemy attacks must still be anticipated because
not all opposing naval forces may know of it. Weapons are to be used only
in self-defense. Permission for surfaced passage through neutral
territorial waters has been requested from neutral governments. The third
section calls for acknowledgments of receipt. The closing reference
numbers remain partly unresolved.

The period-key edition, with source spellings preserved, is:

```text
2XADRESZENX1XXMMDX2XXSDOKOMMANDOXVONSKLSKLXX1XSOFORTANALLESTREITKRAEFTEMITALLENVERFUEGBARENVERKEHRSMITTELNUEBERMITTELNX
AM11X11X12UHRMITTAGSTRITTANALLENFRONTENDERWAFFENSTILLSTANDINKRAFTXMITDIESEMZEITPUNKTSINDALLEKRIEGSHANDLUNGENEINZUSTELLENXALLESEESTREITKRAEFTEBESCHLEUNIGTIN
STUETZPUNKTENSAMMELNNACHANWEISUNGDERIMMEDIATBEFEHLSHABERX2XXANALLEUBOOTEISTBISAUFWEITERESGESCHLUESSELTZUGEBENXWAFFENSTILLSTANDABGESCHLOSSENX
DANICHTDAMITZURECHNENISTDASZALLEFEINDLICHENSEESTREITKRAEFTEHIERVONKENNTNISHABENXWEITERMITFEINDLICHENANGRIFFENRECHNENXWAFFENGEBRAUCHNURZURNOTWEHR
XGENEHMIGUNGZUMBEFAHRENNEUTRALERHOHEITSGEWAESSERUEBERWASZERISTBEINEUTRALENREGIERUNGENERBETENXX3XXEMPFANGSBESTAETIGUNGENXADMIRALXGGXXOP1A?44XXADMIRALSTAB1?340ZWEI
```

`ADRESZEN`, `DASZ`, and `WASZER` are retained exactly in the coordinate
edition. Ordinary readable prose can normalize these spellings without
claiming that extra coordinate repairs have been established. The addressee
and sender labels are also retained rather than expanded into new
institutional identifications.

## Source and framing decisions

There are **1,436 visible ADFGVX coordinates** in five numbered parts.
Two groups have only four printed letters. Supplying one missing
coordinate inside each of those groups gives **1,438 frame coordinates /
719 plaintext positions**. The framed baseline reading has 712 fixed
positions, including visibly erroneous letters. Fourteen known-coordinate
substitutions and the two inserted values yield **717 fixed positions**.
The only remaining unknowns are two reference digits.

| Part | Received coordinates | Used frame | Proposed known-coordinate substitutions | Proposed insertions | Raw fixed / plaintext positions |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 238 | 238 | 1 | 0 | 119 / 119 |
| 2 | 309 | 310 | 3 | 1 | 154 / 155 |
| 3 | 279 | 280 | 3 | 1 | 137 / 140 |
| 4 | 288 | 288 | 5 | 0 | 144 / 144 |
| 5 | 322 | 322 | 2 | 0 | 158 / 161 |

Part 2's thirteenth printed group is `VXDX`. The proposed missing `D`
is inserted after those four letters, yielding `VXDXD`. Part 3's fourteenth
group is `AFGA`; its proposed missing `D` is inserted before the group.
A separate counted substitution then changes the original final `A` to
`F`, yielding the edited group `DAFGF`. The missing letters are editorial
values, not source-visible glyphs.

For each short group, the verifier compares all five possible one-symbol
insertion boundaries against the fixed proposed plaintext. The selected
boundary uniquely minimizes changes to known coordinates within that
specified five-position family. This is evidence for the stated local
frame, not an exhaustive result over every possible text or damage model.

There are no printed dashes or declared source erasures in this record.
OCR omissions, duplicates and letter errors were corrected only by reading
the page. They are separate from the two proposed missing source symbols
and fourteen explicit known-coordinate edits.

## The two unresolved digits are coupled

In part 5, plaintext position 137 is cell `XA`, appearing in `OP1A?44`.
Position 154 is cell `XG`, appearing in `ADMIRALSTAB1?340`. Positions here
are one-based. Both cells have the baseline domain `56789`, but they are
different cells and therefore must receive different digits in an injective
square. The certificate supplies one full-square witness for each of the
**20 possible ordered digit pairs**. It does not choose a historical pair.

The apparent ordinary-letter defects in other positions have not been used
to assign duplicate letters to those numeric cells. They are counted as
coordinate repairs to already known letter cells.

## Source layout and dates

The source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, printed p178 / PDF page 181, in the
[public scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The full page and five enlarged record crops are stored in `sources/`.

The page heading literally gives **11 November 1916**, while the message
header explicitly gives **11 November 1918**:
`A) NKJ v VLP (07.06 p.m. November 11, 1918); 1430 (11) 5 TLE`.
Both source dates are retained. The body gives 11 November and noon
without a year. No unstated time-zone conversion is used in the edition.

The page prints `B)` next to `2 TL`, although no new route or timestamp
accompanies it. The sequential part numbers and the text joins are
preserved. Part 3's length label is retained as `RICHI-2[6/8]0` (260 or
280), and part 4's as `RICHI-2[6/8][6/8]` (266, 268, 286 or 288). The
damaged upper loops are not resolved by choosing the value that agrees
with the body. Independently, part 3 contains 279 visible coordinates
and one four-letter group, motivating the conditional 280-coordinate
frame; part 4 contains 288 visible coordinates and is used at that
literal length without an insertion or deletion. The header alternatives
remain unresolved after the cryptographic verification.

## Reproduce the certificate

```sh
python experiments/naval_armistice_order/verify.py --verify
python experiments/naval_armistice_order/verify.py --verify \
  --pdf /tmp/adfgvx-childs.pdf \
  --prior-paper /tmp/adfgvx-p170-continuation/lasry_author.pdf
```

`inputs.json` freezes the literal rows, image rectangles and hashes,
published key, editorial recipes and prior credit. `certificates.json`
contains raw domains, every source-coordinate pair, exact insertions and
substitutions, all ten short-group comparisons, and consistent global
square witnesses. The first four editions re-encrypt with the unchanged
partial square; the fifth re-encrypts under every recorded numeric-pair
witness. The arbitrary witness digits are not accepted reference numbers.
