# Roesler: leave and departure on the next ship

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

The native p102 D frame concerns leave, the arrival of Rittm. Roesler, and departure on the next ship. It ends with **HOENIGSCHMID** and the abbreviation **S.M.St.Pers.** The complete body already appears in the earlier OCR screen; this edition adds source verification and a reproducible certificate without changing any coordinate.

Prepared by **icekylinx and GPT-6 Astra Pro**. Source: J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed p102 (PDF page105). The Nov1–3 square and column ranks are the published key credited to George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker. Earlier OCR bodies are retained in [prior evidence](../../experiments/nov1_ammunition_and_leave/prior_evidence.json); this is not a claim of first historical body recovery.

## p102 D

### Source and frame

**Source transcription — literal cleartext header:**

```text
D) FÜR COS, ÖST v NKJ (0.24 a.m., November 3rd)
UNG MISSION BARON FRANKENSTEIN FÜR HPTM BENEDIKT 0730 (1)
RICHI-258
```

The [full page](../../experiments/nov1_ammunition_and_leave/sources/p102_full.png) and [native C/D detail](../../experiments/nov1_ammunition_and_leave/sources/p102_C_D_detail.png) show all 258 coordinates, matching the advertised length. The source frame contains no masks, added slots or excluded coordinates.

| Layer | Fixed plaintext positions | Observed substitutions | Source fills | Added / excluded coordinates |
| --- | ---: | ---: | ---: | ---: |
| Raw output, native 258-coordinate frame | 129 / 129 | 0 | 0 | 0 / 0 |
| Edited output | Same as raw | 0 | 0 | 0 / 0 |

### Raw output

**Raw output — published Nov1–3 key, native source frame:**

```text
AUFEXHXNR109XXURLAUBNACHEINTREFFENRITTMXROESLERXROESLERBEWILLIGTXGEHTMITNAECHSTEMSCHIFFDORTHINABXXOBSTXHOENIGSCHMIDXSXMXSTXPERSXX
```

### Readable German

**Readable German — spacing and punctuation only; umlauts display their literal two-letter equivalents:**

> Auf E. H. Nr. 109. Urlaub nach Eintreffen Rittm. Roesler. Roesler bewilligt. Geht mit nächstem Schiff dorthin ab. Obst. Hoenigschmid. S. M. St. Pers.

`ROESLER` occurs twice, separated by `X`; both occurrences remain in the display. The punctuation around “Roesler bewilligt” is editorial and does not settle the repeated name’s grammatical attachment. `HOENIGSCHMID`, `109`, and `SXMXSTXPERS` are unchanged. The displayed name Roesler is not normalized to another spelling.

The source header names `BARON FRANKENSTEIN` and `HPTM BENEDIKT`; they are cleartext addressing evidence, not additional recovered ciphertext names. `UNG` and the station label `ÖST` remain as printed. The old OCR ciphertext and plaintext agree exactly with the native reading in this edition.

### Evidence and limits

The [input transcription](../../experiments/nov1_ammunition_and_leave/inputs.json) preserves every source row, the published key and the exact readable display. The [certificate](../../experiments/nov1_ammunition_and_leave/certificates.json) maps each plaintext position to its two source coordinates, preserves all numeral labels, and checks every non-`X` label in the displayed German. The [standalone verifier](../../experiments/nov1_ammunition_and_leave/verify.py) re-encrypts the native plaintext to the full observed ciphertext. Its optional PDF mode also reproduces the source images exactly.

No historical inference changes the source, key, numerals or personal-name spellings. Punctuation and abbreviation segmentation are editorial choices, so grammatical attachment and full abbreviations may remain uncertain even when all cipher labels are fixed.
