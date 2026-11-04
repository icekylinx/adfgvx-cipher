# Radio-control, internment and cipher-service source editions

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Fourteen source-checked ciphertext records contain **2,873 printed slots**, of which **2,852** are valid ADFGVX coordinates. One additional record is a cleartext service notice. The package publishes three readable source editions:

- [Kiel radio-control order and its repeat](../../cases/pages/140.md#edition-cases-radio-kiel-radio-control): four original parts plus a damaged repeat. A five-slot deletion gives an exact alignment model for the repeat; 55/56 proposed first-part letters have a direct witness across the two copies.
- [Mackensen internment letter](../../cases/pages/226.md#edition-cases-military-mackensen-internment): a previously published four-part message, now with the literal source and an exact two-group repair of part 3. Two equivalent aliases recover the readable candidate at a cost of four further coordinate substitutions and one supplied coordinate.
- [Cipher and routing instructions](../../cases/pages/225.md#edition-cases-radio-late-november-cipher-instructions): five ciphertexts plus a cleartext ITOCHI notice. The two-part p228 key agreement is fully direct: 320 unchanged coordinates give 160 fixed plaintext positions.

The 12 records using the identity source geometry fix **1,193/1,209 raw positions**. The two separately modeled damaged records fix **219/225**. These counts include garbled symbols and describe consequences of the stated key and geometry, not a count of historically correct letters. No source model or readable-word proposal alters the published key.

## Source and prior credit

Every record was checked against the [Childs scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view), with enlarged [source crops](sources/) retained here. Literal non-coordinate glyphs and printed dashes keep their slots. The complete book is not redistributed.

Lasry, Niebel, Kopal and Wacker already describe the p140/p146 radio-control order in section 6.4 of their [2017 paper](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf); its Table 4 already publishes the p226/p227 internment letter. Their discussion also credits Childs's original decipherments. Present contributions are the literal source editions, arithmetic verification, explicit damage models and repair costs, and preservation of wording that remains uncertain.

The prior `SITUATIONEN` reconstruction in the letter has eleven characters, while its source-derived position span contains nine (`SMUTIONEN`). The certificate retains this length discrepancy and prices same-length alternatives without promoting one to certainty.

## Files and verification

| File | Purpose |
| --- | --- |
| [inputs.json](inputs.json) | Literal rows, headers, source locators and hashes, unchanged key snapshots, local models and readable candidates |
| [certificates.json](certificates.json) | Every raw domain and source coordinate, edit lists, repeated-copy alignment and all 30 local part-3 layouts |
| [verify.py](verify.py) | Independent column-offset inverse, checked against the separate project functions, plus exact proposal verification |

```sh
python experiments/corpus_extension/verify.py --verify
python experiments/corpus_extension/verify.py --verify --pdf /path/to/childs.pdf
```

The first command requires only the Python standard library and the repository. The second additionally checks the full source-PDF hash. The verifier does not rely on a language score. Source alignment and minimum repair statements are explicitly scoped to the local models and declared candidate; they do not prove that every historical copying error occurred in that form.
