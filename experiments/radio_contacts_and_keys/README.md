# Radio contacts, key availability and neighboring source records

Prepared by **icekylinx and GPT-6 Astra Pro**. Seven manually reviewed
records provide readable source editions under unchanged published keys:

- [Four radio records](../../cases/pages/100.md#edition-cases-radio-radio-contacts-and-keys): direct
  communication during a wire interruption, an unavailable OSKACHI key,
  exact calling/listening times, and a receiving station in the embassy.
- [p100 B](../../cases/pages/100.md#edition-cases-military-budapest-wire-break): bridges and the
  interrupted wire lines through Budapest.
- [p142 B](../../cases/pages/142.md#edition-cases-caucasus-representative-retention): the Caucasus
  `BEV K.M.` representative is to remain.
- [p142 C](../../cases/pages/142.md#edition-cases-military-dobrudscha-report): a request for a
  position on an Entente report about the Dobrudscha.

## Accounting

| Record | Source slots | Valid coordinates | Raw fixed labels | Substitutions | Printed-dash fills |
| --- | ---: | ---: | ---: | ---: | ---: |
| p100 B | 194 | 194 | 97 / 97 | 2 | 0 |
| p100 C | 158 | 158 | 79 / 79 | 0 | 0 |
| p137 D | 102 | 102 | 51 / 51 | 1 | 0 |
| p142 A | 128 | 128 | 64 / 64 | 0 | 0 |
| p142 B | 286 | 286 | 143 / 143 | 3 | 0 |
| p142 C | 242 | 240 | 119 / 121 | 1 | 2 |
| p150 A2 | 180 | 179 | 89 / 90 | 6 | 1 |
| Total | 1290 | 1287 | 642 / 645 | 13 | 3 |

All seven source lengths match their printed labels. No coordinate is
inserted, deleted or reordered, and no square label is reassigned. The
source key is `Nov1-3` for p100 B/C and `Nov4-6` for the other five.

The older OCR lengths of **195 for p100 B** and **280 for p142 B** were
incorrect; manual reading yields the printed 194 and 286. Their newly
readable bodies come from correcting the source transcription before
decryption. They are not observations of historical phase loss. The old
corpus and search ledgers remain unchanged.

## Details deliberately left visible

`inputs.json` retains full diplomatic rows, source headers and page-image
hashes. `certificates.json` retains every raw label domain, source-coordinate
origin, numerical field and repaired forward witness.

- p100 C is an exact unchanged reading but keeps `BRSLAU` and `MEGLICH`.
  Reader interpretation supplies no inserted plaintext letters.
- p137 D's first sender letter is overprinted and conservatively represented
  by `?` in the header. This is not a ciphertext erasure. The direct
  `OSKACHI` wording is a key-availability statement, not a newly recovered
  key, operating period, or identification of a challenge's cipher.
- p142 A's `0430`, `10 MIN VVV` and `0645` are unchanged labels. No day or
  time zone is invented.
- p142 B preserves both `BEVXKMX` and `BEVXKXM` separator patterns and the
  complete footer `NRXZXROEMX1XAX23X11X18XKRA`. It does not silently turn the
  latter into an asserted calendar date.
- p142 C preserves `5011` and `D17U560`. Its report does not independently
  verify Romanian occupation or identify the abbreviated addressee's office.
- p150 is explicitly **A2**. No first part is attached or reconstructed.
  `NAMEXQZXX` retains its uncertain name/separator boundary, and `CHIFFRIREN`
  and `PERIDEN` retain their literal spellings. Two coordinate substitutions
  are needed for the single `E`→`F` word repair in `EMPFGSSTAT`; both are
  counted.

Raw digits inside damaged ordinary words are retained and explicitly priced:
p137 D `3`→`S`; p142 B `9`→`I` and `4`→`M`; p142 C `2`→`D`. These local
coordinate changes leave every square digit assignment unchanged. Actual
numerical/reference fields are unchanged.

## Reproduction

```sh
python experiments/radio_contacts_and_keys/verify.py --verify
```

The standalone verifier uses only Python's standard library. It imports no
shared cipher implementation or language model. Its separate sorted-column
inversion checks variable column heights, raw marginal domains, repair
ledgers, numerical exceptions, source length and every complete forward
witness. Default verification passed.

Optional PDF verification requires PyMuPDF and regenerates all eleven images
from the recorded page numbers, rectangles and scales:

```sh
python experiments/radio_contacts_and_keys/verify.py --verify \
  --pdf /path/to/adfgvx-childs.pdf
```

PDF SHA-256:
`157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.
Printed pp100, 137, 142 and 150 are PDF pp103, 140, 145 and 153. Each image
has both a PNG-file hash and a raw-pixel hash. Full PDF pixel regeneration
passed. Running without `--verify` regenerates the certificate from the
frozen input.

## Attribution and limits

J. Rives Childs's collected intercepts are the primary source. The published
keys are prior work by **George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker**,
[DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
also given in George Lasry's 2017-02-24 key comment. Full provenance is kept
with each key. The separate p100 challenge remains credited to **Armin,
2017 comment 13**; no challenge body is duplicated as a new source recovery.

Earlier unreviewed OCR-derived candidates existed. A bounded author-paper
check found no explicit examples of these seven bodies, which does not
establish universal first-decipherment priority. Exact re-encryption verifies
the stated arithmetic and prices, not unique historical wording, station
identities or the independent truth of the reports.
