# Kiel radio-control order — p140 A and p146 A

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Prior interpretation: J. Rives Childs; George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker. Source comparison and exact repair audit: icekylinx and GPT-6 Astra Pro.**

The four-part order instructs radio stations to come under an officer's immediate control, prevent the reception and distribution of messages from Kiel, and confiscate and destroy texts already received. Its historical interpretation and the p146 repeat were already described in [section 6.4 of Lasry et al.](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf), printed p. 23. The present edition adds literal source transcriptions, independently checked coordinate arithmetic, and an explicit repair of the repeated first part.

## Readable text

> Sämtliche Funkstellen sofort durch Offizier fest in Hand nehmen. Verhindern, dass Funksprüche aus Kiel, Kiel aufgenommen und verbreitet werden. Bereits aufgenommene Texte beschlagnahmen und vernichten. Größte Eile geboten. Nachrchef, röm. vier, V, 47?00, geh.

The wording is an editorial reading. The repeated **Kiel, Kiel** is retained. The reference `47?00` remains incomplete; the displayed uncertainty is not permission to choose any digit independently of its coordinate domain.

p140 A is headed `YZ NKJ v LP (3.52 p.m., November 6th)`, `1331 (6/11) 4 TEILE`. The first part reappears in p146 A, headed `ASO v NKJ (04.19 a.m., November 7th)` and `WH BIS 0025 30 GR 1331 (KR)`. Both use the published **Nov4–6** key. The later interception date does not imply that the repeat was re-encrypted under the next key.

| Record | Source slots / advertised | Fixed raw positions, including garbles | Changes for the displayed reading |
|---|---:|---:|---|
| p140 A1 | 112 / 112 | 56/56 | 2 known-coordinate substitutions |
| p140 A2 | 134 / 134 | 65/67 | 3 substitutions and 2 erasure fills |
| p140 A3 | 102 / 102 | 47/51 | 2 substitutions and 4 erasure fills |
| p140 A4 | 98 / 98 | 45/49 | 3 substitutions and 3 fills; number remains unresolved |
| p146 A | 117 / 112 | 51/56 after the declared five-slot deletion | 1 substitution and 5 fills |

p146 A is a separate record from the challenge's **p146 B**, whose duplicated `XAAXV` group has its [own case](../p146.md).

## Repeated first part: an extra group and a witnessed letter

p146 prints **117 slots** despite its `RICHI-112` label. Its twelfth group, `VAADX`, is absent from p140. Removing that group yields a 112-slot stream with only two disagreements at known coordinates against p140. Screening every contiguous five-slot deletion gives the same minimum at zero-based starts **54 and 55**; the two deletions produce an identical stream because of a repeated boundary `X`. Both aliases are preserved in the certificate.

The resulting literal decryptions are:

```text
p140 A1
SAEMTLICHEFUNKSTELLENSOFORTDURCHO1FIGIERFESTINHANDNEHMEN

p146 A after the declared deletion
SAEMTL?CHEFUNKS?ELLE?SOFORTDURCHOFFIFIERFEST?NHANDNE?MEN
```

Across the two copies, **55 of the 56 positions** in the readable first part are witnessed directly. The later copy supplies the first `F` in `OFFIZIER`, where p140 gives `1`. The letter `Z` remains an editorial correction: p140 gives `G` and p146 gives `F` at that position. Thus the repeat improves the text without turning every proposed letter into observed evidence.

## Other raw parts

```text
p140 A2
VERHIND1RNDASSF?NKSPRUEC?EAUSKIELKIELAUFGENOMMENUNDVEABREITETWRRDEN

p140 A3
BEREITSA?FGENOMM?NETEXTEB?SCHLAGN?WMENUNDVERNICHTEN

p140 A4
GROESSTEKILEGEBOTONNACHRC?EFXR?EMB?ERXVX47?00XGEH
```

The literal transcripts retain the dashes, the invalid `C` in p140's `FDCGF`, and the invalid `O` in p146's `VOVVX`. Neither invalid glyph is silently replaced by a valid coordinate.

## Evidence

- [p140 source](../../experiments/corpus_extension/sources/p140_A.png) and [p146 repeat](../../experiments/corpus_extension/sources/p146_A.png).
- [Literal inputs, key snapshots and proposed readings](../../experiments/corpus_extension/inputs.json).
- [Coordinate maps, domains, edit lists and alignment certificate](../../experiments/corpus_extension/certificates.json).

```sh
python experiments/corpus_extension/verify.py --verify
```

A close alignment supports the declared extra-group model; it cannot establish how the historical copying error happened. The original sources remain intact.
