# p185 D: a conditional transport-context reading

**Status: source-preserving partial reading under a plausible, unproved gap geometry.** This supplementary intercept is outside the 22-message challenge. Its header reads `CM v CZ (20.15 p.m., November 13th), 21.00, RIZI-198`, but the body contains 193 slots: 192 valid ADFGVX coordinates and one literal `Y`. The raw `Y` is retained in the source layer and treated as one unknown coordinate in analysis.

![Literal p185 D source excerpt](../../sources/excerpts/childs_p185_D.png)

We enumerated all 194 possible positions for a contiguous block of five missing coordinates under the audited November 13–15b key. Every valid received coordinate remains unchanged and in its original order. No missing coordinate or unknown square cell is filled.

## Conditional result

Inserting five erasures before source index **55**, a printed group boundary, gives this exact partial plaintext:

```text
STATMETXMARSCHIERTLCST?UT?SMORGEN1500UEBERDHFNXAB?A6SCHBE?EITSEIN?VS6GROV?AN?IERE?XBITTEF6EXSEIFERT
```

Under this geometry, **91 of 99 characters are fixed**. The eight unresolved positions consist of six letters touched by uncertain coordinates and two letters using unassigned square cells. The fixed portions include `MARSCHIERT`, `MORGEN1500UEBERDHFN`, and `SEIFERT`; malformed portions are retained literally. `DHFN` and `STATMET` are not expanded into place or station names.

This is a conditional result. The strongest composite language score selects position 55, but a conventional plaintext quadgram score selects position 57:

| Gap before source index | Composite ranking score | Plaintext quadgram mean |
|---:|---:|---:|
| 55 | 24.910328 | -6.041730 |
| 56 | 22.691041 | -6.070230 |
| 57 | 22.641029 | -5.987314 |

These are heuristic scores, not confidence probabilities. All 194 positions are arithmetically compatible with the received symbols. Positions 159 and 160 produce the same masked ciphertext because the inserted gap can exchange places with the existing unknown `Y` slot. There are 193 distinct masked ciphertexts. No plaintext character is fixed across all 194 geometries. The three leading composite-score candidates share 89 fixed characters, but that selected subset is not a confidence set.

## Independent transport context

Six additional source-checked intercepts decrypt directly with the same historical key. They retain every literal garble and unresolved square cell:

- **p193 E, November 14:** `KLEINERFEDERWAGENZU?ANHAENGENHIERXKOMMTAUTOX`
- **p194 A, November 14, header `CM v CZ`:** `ABTRANSPORTINVERABREDETERWEISEFREITCGDHFN1?00XWAGENBERE?THALTENXMARSCHZIELHANAUXSEIFERT`
- **p196 B, November 15, header `CM v CZ`:** `ABTRANSPORTINVERABREDETERWEISEFREITAGDHFN1?00XWAGENBEREITHALTENXMARSCHZIELHANAUXSEI?ERT`
- **p197 E, November 15, header `CM v CZ`:** `LASTAUTO1?00A?GEFAHRENXICHBLEIBEMIT?MANNBISSOHNTAGXALLESGUTEAUFWIEDERSEHENXSE?FERTXGRUSSBOCHO`
- **p198 C, November 15, header `CM v CZ`:** `LASTAUTO1?00ABGEFAHRENXICHBLEIBEMIT?MANNBISSONNTAGXALLESGUTEAUFWIEDERSEHENXSEHFERTXGRUSSBOCHO`
- **p189 E, November 15, header `CZ v CM`:** `JAHEBEPUMPEAUSBLECHXKOMMEN?AUTOSXHIER?ANH?ENGER`. This is a different intercept from the p189 challenge target.

The p194/p196 pair repeats `DHFN` and names `HANAU` as the march destination. It has 171 of 174 raw coordinates in common; disagreements are at indices 82 (`K/X`), 167 (`X/V`), and 173 (`D/G`). The p197/p198 pair agrees at 183 of 186 coordinates, differing at indices 59 (`V/A`), 63 (`A/V`), and 67 (`G/A`). Neither last-car copy supplies an exact `SEIFERT` signature; `SEHFERT` is not silently corrected.

For the transport-order pair, a separately labelled source-supported composite takes `X` at index 82 and `V` at index 167 from p196 while retaining p194's `D` at index 173. It reads:

```text
ABTRANSPORTINVERABREDETERWEISEFREITAGDHFN1?00XWAGENBEREITHALTENXMARSCHZIELHANAUXSEIFERT
```

This composite fixes 86 of 87 characters. It makes an editorial choice between disagreeing source witnesses, with every chosen value attested in at least one. The certificate also retains all four combinations of the two disagreements between valid coordinates. The time cell `FV` remains unassigned; no numerical time is inferred. These messages support a transport context for the p185/p189 traffic but do not supply p185 D's missing five coordinates or prove a new square-cell assignment.

The [certificate](../../data/certificates/p185_D_transport.json) contains every gap geometry, its full plaintext domains, exact source-to-plaintext mapping, all six direct context readings, both near-parallel comparisons, and the conditional composite. The [standalone verifier](../../adfgvx/transport.py) recomputes all 194 constraint sets and exact coordinate roundtrips without a language model. It checks the consistency of the stored ranking order but does not recompute the heuristic scores. The [portable ranking script](../../experiments/known_key/README.md) reproduces both complete rankings from a pinned upstream model; every stored score matched exactly in the recorded environment.

```sh
python3 -m adfgvx.transport
```

This analysis does not fully solve p189 and does not add a solved item to the 22-message total.

Source images: [p189](../../sources/excerpts/childs_p189_context.png), [p193](../../sources/excerpts/childs_p193_context.png), [p194](../../sources/excerpts/childs_p194_context.png), [p196](../../sources/excerpts/childs_p196_context.png), [p197](../../sources/excerpts/childs_p197_context.png), [p198](../../sources/excerpts/childs_p198_context.png). Header order is `recipient v sender`; see [source conventions](../../sources/README.md).
