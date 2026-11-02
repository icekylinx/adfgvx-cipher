# Internment letter to Mackensen's soldiers' council — p226 C / p227 A

**Prior reading: J. Rives Childs; George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker. Source edition and exact repair audit: icekylinx and GPT-6 Astra Pro.**

The four-part letter says that efforts to avoid internment have failed, asks the soldiers to maintain order, and expresses the hope of their return to Germany. This body is already published in [Lasry et al., Table 4](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf), printed p. 22, and in [Lasry's dissertation, Table 6.4](https://www.uni-kassel.de/upress/online/OpenAccess/978-3-7376-0458-1.OpenAccess.pdf), p. 108. The new work here explains a two-location source defect in part 3 and makes the source costs and unresolved wording inspectable.

## Meaning

Addressed to the soldiers' council of the Mackensen army, the letter reports that the Entente insists on internment. It says that maintaining the marching order would be treated as a breach of the armistice, giving the Entente grounds to enter Germany. The sender promises to seek tolerable internment conditions and a safe return home after peace is concluded, then urges calm and order to avoid internal disintegration.

The closing names the executive council of the workers' and soldiers' councils of Greater Berlin. The raw signatures are `SOLKENBUHR` and `MNELLER`; the prior reading gives Müller. `MOLKENBUHR` is separately costed as a plausible surname repair, with no first name assigned.

The source is headed `ZON v BSL` (the O has two marks), `04.20 a.m., December 2nd`, with origin field `NR 132 2200 (11/29) 4 TLE`. Parts 1–3 appear on printed p226 and part 4 on p227. These are different date fields, not an interchangeable date of composition. All four parts use the unchanged published **Nov28–Dec1** key.

| Part | Printed coordinates | Fixed raw positions, including garbles | Additional readable-text repairs |
|---|---:|---:|---|
| p226 C1 | 344 | 172/172 | 6 substitutions with the damaged word retained; 8 if `STATIONEN` is proposed |
| p226 C2 | 324 | 162/162 | 11 known-coordinate substitutions |
| p226 C3 | 338 | 168/169 under the explicit group-restoration model | 4 substitutions and 1 supplied coordinate |
| p227 A4 | 392 | 196/196 | 12 substitutions; 13 if `MOLKENBUHR` is also proposed |

## Part 3: restoring two malformed groups

The source visibly prints a six-letter group **`VFFGDV`** at group 34 and a four-letter group **`XFVA`** at group 56. The total remains the advertised 338 coordinates. Decrypting those coordinates in their printed sequence gives a garbled result; that identity result is retained in the certificate.

A separate model restores five-letter grouping at those two locations: remove one coordinate from group 34 and add one slot inside group 56. Among all **30** local layouts, the readable 169-position candidate needs the fewest further known-coordinate substitutions in two equivalent cases:

- Remove either of the adjacent `F` characters in group 34, producing `VFGDV`.
- Supply `V` after the initial `X` of group 56, producing `XVFVA`.

The two deletion indices are aliases of one reconstructed stream. Before supplying the new coordinate or changing any remaining source symbol, its raw plaintext is:

```text
ESIVTUNSE?BEMUEHENEUREINTERNIERUNGSOZUGESTALTENDASSIHRWEDERNHTNOCHMANGELLEIDETUNDNACHDEMMOJGLICHSTRASCHENFRIEDENSCHLUSSGLUECKLICHUNDGESUNDINDIEHEIMATZUJUECKKEHRENKOENNTY
```

Four explicit coordinate substitutions and the one supplied `V` give:

> Es ist unser Bemühen, eure Internierung so zu gestalten, dass ihr weder Not noch Mangel leidet und nach dem möglichst raschen Friedenschluss glücklich und gesund in die Heimat zurückkehren könnt.

The source-length spelling `FRIEDENSCHLUSS` is retained in the exact candidate; the additional S of modern `FRIEDENSSCHLUSS` is not silently inserted. The local optimum is conditional on this candidate and the stated two-group model. It establishes a small exact repair certificate, not historical certainty about every error.

## A word in part 1 remains unsettled

The directly decrypted token after `INBEDRACHTKOQMENDEN` is **`SMUTIONEN`**, occupying nine positions. The prior publication prints **`SITUATIONEN`**, which has eleven. That normalization therefore requires two extra plaintext positions and is not an unchanged or same-length decryption.

The present certificate prices two same-length alternatives. `STATIONEN` adds two coordinate substitutions to the six otherwise proposed in part 1; `INSTANZEN` raises that total to seventeen. The lower-cost word is not adopted as certain solely from this comparison. The conservative editorial candidate retains the damaged token, and the English interpretation refers only to the relevant bodies or offices.

## Literal source and reproducibility

The complete raw strings, source-index maps and every proposed edit are in [inputs.json](../../experiments/corpus_extension/inputs.json) and [certificates.json](../../experiments/corpus_extension/certificates.json). The focused source images are [part 1](../../experiments/corpus_extension/sources/p226_C1.png), [part 2](../../experiments/corpus_extension/sources/p226_C2.png), [part 3](../../experiments/corpus_extension/sources/p226_C3.png) and [part 4](../../experiments/corpus_extension/sources/p227_A4.png).

```sh
python experiments/corpus_extension/verify.py --verify
```

Raw `X`, `Y`, `J` and digits remain labels from the published square. Ordinary spelling proposals and source layout repairs do not change that square.
