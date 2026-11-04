# Wire communications, return instructions and the Tiraspol continuation

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source collation and edition: icekylinx and GPT-6 Astra Pro.**

The two surviving copies supply complementary evidence. The short first
part on printed p162 overlaps the end of the longer first part on p166,
and their second parts differ at only two source positions. This edition
adds three physical records: **p162 C1, p166 C1 and p166 C2**. The earlier
[p162 C2 edition](../military/tiraspol_border_report.md) remains a supporting
witness, with its original displays unchanged.

The primary unfilled frames fix **205 of 362 plaintext positions** across
the three records. Copying the independently observed p166 prefix to the
p162 model supplies 156 further labels; supplying one missing p166 `X`
from p162 supplies one more. Those **157 source-linked completions are
counted separately**, because p162 by itself fixes no complete plaintext
pair in the restored 312-coordinate frame. Six distinct observed-source
substitutions produce the optional complete edition: three supported by
the other copies and three lexical choices in the shared p166 prefix.

The [Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)
prints p162 C at `09.45 a.m., November 9th`, with an unread recipient
identifier and `v NKJ`, followed by `missed first part of this message`.
The p166 C header reads `UKS v NKJ`, `9.47 a.m., November 9th`,
`0920 (9) 2 TLE`. These receipt times remain distinct. Both full pages and
the enlarged C crops were directly inspected. The exact PDF, pages,
rectangles, dimensions and RGB digests are preserved in
[the source inputs](../../experiments/nov9_wire_return_source_family/inputs.json);
no unpublished image asset is needed to reproduce the evidence.

## p162 C1

The printed body contains **117 coordinates**, and its first-part header
gives no recoverable total length. In the source-linked 312-coordinate
frame, all **195 absent prefix coordinates remain unknown in the primary
layer**. There are 117 half-pairs with one observed p162 coordinate and 39
pairs with neither coordinate present. No complete pair is fixed by this
fragment alone. Its literal odd-length 117-coordinate inverse, including
the unpaired final coordinate, is retained as a diagnostic in the
certificate; it is not used as a readable message or included in the
fixed-position total.

<details>
<summary>Raw decoded text</summary>

**Raw output — 195 unassigned prefix slots followed by all 117 observed p162 coordinates; zero fixed labels out of 156:**

```text
????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
```

</details>

The next layer copies only p166's **original source coordinates 0:195**.
Every complete pair retains both source origins. Of the resulting 156
pairs, 117 combine a p162 coordinate with a p166 prefix coordinate; 39
come entirely from the p166 prefix. None is independently observed as a
complete p162 pair.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — source-linked comparison, with the 195-coordinate prefix copied from p166 and no alteration to the 117 p162 coordinates:**

```text
AKONACH18XMITTEILTOBDRAHTVERKEHRODESSAXODELSAMITDORTBGERHGRXMOGGLICHXSTOERUNGSPOSTENACKERMANNSOLLVONBRAILAZURRUECKKEHRANGEWIESENSEINXSTOERUNGSPOSTENTIRASPOL
```

**Edited output — three lexical substitutions at borrowed p166 prefix origins; zero substitutions to the observed p162 fragment:**

```text
AKONACH18XMITTEILTOBDRAHTVERKEHRODESSAXODESSAMITDORTIGERHGRXMOEGLICHXSTOERUNGSPOSTENACKERMANNSOLLVONBRAILAZURRUECKKEHRANGEWIESENSEINXSTOERUNGSPOSTENTIRASPOL
```

</details>

**Readable German — complete conditional source-linked edition, preserving the literal wording, separators and labels:**

> Akonach 18 X mitteilt ob Drahtverkehr Odessa X Odessa mit dortiger Hgr X moeglich X Stoerungsposten Ackermann soll von Braila zur Rueckkehr angewiesen sein X Stoerungsposten Tiraspol.

**Conditional interpretation:** The collated text concerns whether wire
communication involving Odessa and the local `Hgr` is possible. It says
that the post labeled Ackermann should have been instructed to return
from Braila, and then names a Tiraspol post. The awkward `MITTEILT`, repeated
`ODESSA`, and `AKONACH18` are retained. This reading does not determine a
person's identity, a precise organizational expansion of `Hgr`, or the
technical duties of a `Stoerungsposten`.

## p166 C1

The header advertises **RICHI-312**, but the reviewed body contains
**311 valid coordinates**. The four-character group **XVGD** is visibly
short. Its comparison with p162 supports one inserted `X`, with two exact
aliases: insertion before original source 225 or 226 produces the same
`XXVGD` sequence. The location of the missing copy within the adjacent
`XX` cannot be distinguished. Before the fill, the two aliases place the
unknown at different plaintext positions; both raw streams are retained.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — all 311 original coordinates plus one unassigned slot before source 225; 155 of 156 labels fixed:**

```text
AKONACH18XMITTEILTOBDRAHTVERKEHRODESSAXODELSAMITDORTBGERHGRXM?GGLICHXSTOERUNGSPOSTENACKERMANNSOLLVONBRAILAZURRUECKKEHRANGEWGESENSEINXOTOERUNGSPOSTENTIRASPOL
```

**Raw output — equally valid unfilled alias before source 226; 155 of 156 labels fixed:**

```text
AKONACH18XMITTEILTOBDRAHTVERKEHRODESSAXODELSAMITDORTBGERHGRXMOGGLICHXST?ERUNGSPOSTENACKERMANNSOLLVONBRAILAZURRUECKKEHRANGEWGESENSEINXOTOERUNGSPOSTENTIRASPOL
```

</details>

In the first alias the unresolved label is plaintext 61; in the second
it is plaintext 71. Both have pair `F?` and domain **178COQ**. The p162
copy provides `X` at source 30 or 31, respectively, fixing `O`. This fill
is independently supported by a received coordinate, not chosen solely
to spell a German word.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — source-linked missing-X fill only; both observed-copy disagreements and the three lexical defects remain visible:**

```text
AKONACH18XMITTEILTOBDRAHTVERKEHRODESSAXODELSAMITDORTBGERHGRXMOGGLICHXSTOERUNGSPOSTENACKERMANNSOLLVONBRAILAZURRUECKKEHRANGEWGESENSEINXOTOERUNGSPOSTENTIRASPOL
```

**Edited output — the source-supported missing-X fill, two copy-supported observed substitutions and three optional lexical substitutions:**

```text
AKONACH18XMITTEILTOBDRAHTVERKEHRODESSAXODESSAMITDORTIGERHGRXMOEGLICHXSTOERUNGSPOSTENACKERMANNSOLLVONBRAILAZURRUECKKEHRANGEWIESENSEINXSTOERUNGSPOSTENTIRASPOL
```

</details>

**Readable German — complete optional p166 C1 edition, preserving every literal label:**

> Akonach 18 X mitteilt ob Drahtverkehr Odessa X Odessa mit dortiger Hgr X moeglich X Stoerungsposten Ackermann soll von Braila zur Rueckkehr angewiesen sein X Stoerungsposten Tiraspol.

**Conditional interpretation:** This longer copy supports the same reading
as the source-linked p162 first part. The full result depends on the stated
one-coordinate loss model and six operations on p166 C1: one insertion/fill
and five observed substitutions. The 195-coordinate prefix supplies the
p162 restoration; that shared evidence is counted once at its source origins.
The labels `18` here and `17` in the continuation remain different.

## p166 C2

The second part is independently labeled **2 TL RICHI-100** and contains
exactly 100 observed coordinates. Its native frame gives all 50 plaintext
labels under the unchanged published **Nov7–9** key.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — all 100 printed source coordinates, with no fill or changed key:**

```text
TIRASPOLERHIELTMXGXFEUERANDERGRENZEXAKONACH17ROZM4
```

**Edited output — one observed substitution at source 84, supported by the p162 C2 copy:**

```text
TIRASPOLERHIELTMXGXFEUERANDERGRENZEXAKONACH17ROEM4
```

</details>

**Readable German — complete optional second part, with every separator and closing label retained:**

> Tiraspol erhielt M X G X Feuer an der Grenze X Akonach 17 Roem 4.

**Conditional interpretation:** The continuation reports `M G FEUER` at a
border for the place or post labeled Tiraspol. It ends with the literal
`AKONACH17ROEM4`. No exact border, incident, unit, administrative number
or outside historical referent is supplied.

The p162 and p166 second parts differ only at two positions: p162 source
36 is a printed dash where p166 prints `G`; p162 source 84 is `V` where
p166 prints `F`. Thus p166 independently supports the earlier p162 fill
in `ERHIELT`, while p162 independently supports the optional p166 change
from `ROZM` to `ROEM`. Both coordinates of each relevant pair are recorded
in the certificate. The previously accepted p162 C2 record is not added
to the new-record or new-position counts.

## Source-only alignment and exact costs

All indices are zero-based. The geometry is selected from source
coordinates, before introducing a German word target. In each unfilled
p166 gap alias, all **196 contiguous 117-position windows** are compared
with the p162 fragment. Offset **195** is uniquely best at two observed
coordinate disagreements. At that suffix, all **117 possible locations**
for a single absent coordinate are compared: only local gaps **30 and 31**
attain the same two-disagreement minimum.

The overlap contains **114 independently agreeing observed coordinates,
two disagreements and one absent p166 coordinate**. Once the absent
coordinate is copied from p162, the filled strings agree at 115 positions;
one of those matches is supplied from the other copy and is not a 115th
independent agreement. These exact comparisons establish the best match
within the declared single-loss model, without excluding every possible
alternative error history.

| Origin of operation | Original source position | Operation | Plaintext effect | Evidential role |
| --- | ---: | --- | --- | --- |
| p166 C1 | Gap before 225 or 226 | Insert `X` from p162 C1 source 30 or 31 | Completes one raw `O` | Independent source-linked fill; aliases preserved |
| p166 C1 | 246 | `D` → `G` | `ANGEWGESEN` → `ANGEWIESEN` | Supported by p162 C1 source 52; other half of the pair still comes from p166 |
| p166 C1 | 247 | `F` → `D` | `OTOERUNGSPOSTEN` → `STOERUNGSPOSTEN` | Supported by p162 C1 source 53; other half of the pair still comes from p166 |
| p166 C1 | 160 | `D` → `X` | `ODELSA` → `ODESSA` | Optional lexical correction; the earlier `ODESSA` is already raw |
| p166 C1 | 161 | `X` → `G` | `DORTBGER` → `DORTIGER` | Optional lexical correction in borrowed prefix |
| p166 C1 | 162 | `G` → `V` | `MOGGLICH` → `MOEGLICH` | Optional lexical correction in borrowed prefix |
| p166 C2 | 84 | `F` → `V` | `ROZM` → `ROEM` | Supported by the complete raw p162 C2 pair |

The three prefix corrections appear in both readable first parts, but
there are only **three distinct corrected received coordinates**, all
from p166. Counting them a second time as p162 edits would confuse a
copied reading with independent evidence. The entire 117-coordinate p162
fragment remains unchanged throughout.

| New physical record | Printed coordinates | Modeled coordinates | Primary fixed labels | Source-linked labels added | Optional fixed labels |
| --- | ---: | ---: | ---: | ---: | ---: |
| p162 C1 | 117 | 312 | 0 / 156 | 156 | 156 / 156 |
| p166 C1 | 311 | 312 | 155 / 156 | 1 | 156 / 156 |
| p166 C2 | 100 | 100 | 50 / 50 | 0 | 50 / 50 |
| Total | 528 | 724 | **205 / 362** | **157** | **362 / 362** |

## Reproduction and credit

The [certificate](../../experiments/nov9_wire_return_source_family/certificates.json)
contains the primary unfilled records, both gap aliases, every complete
pair's two coordinate origins, all source-only costs, the six unique
observed substitutions, the independent gap witness, native odd-frame
diagnostics and preserved OCR comparisons. Earlier OCR counted 307
coordinates for p166 C1; the actual printed source has 311. Restoring
misread digital transcription is kept separate from the one still absent
manuscript coordinate. Neither the published key nor the core challenge
messages are changed.

```sh
python experiments/nov9_wire_return_source_family/verify.py --verify
python experiments/nov9_wire_return_source_family/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

Without the PDF argument, the verifier explicitly reports that source
pixel reproduction is skipped; all source, alignment, origin, cipher,
round-trip and display assertions still run. With the PDF argument, both
reviewed crop RGB digests are reproduced from the pinned source.

The manuscript source is **J. Rives Childs**. Published period-key credit
remains with **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker** (2016)
and George Lasry's 2017 disclosure, as recorded in the unchanged key
metadata. This is source restoration and explicit editorial collation by
**icekylinx and GPT-6 Astra Pro**, with prior OCR and the earlier p162 C2
edition preserved.
