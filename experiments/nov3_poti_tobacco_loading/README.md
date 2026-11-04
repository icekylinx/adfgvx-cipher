# Poti tobacco loading inquiry

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

Read the [complete p113 C edition](../../cases/pages/113.md#edition-cases-naval-nov3-poti-tobacco-loading).
The reviewed native source has **212 valid coordinates**, **106 fixed raw
positions**, and a complete candidate requiring **one observed-coordinate
substitution**. There are no coordinate fills or frame changes. The first
`SCHIFFZAUSGL` is proposed as `SCHIFFSAUSGL`, supported by the unedited
closing occurrence of that exact abbreviation.


**Reviewed source crops:** [p113_reviewed.png](sources/p113_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## Reproduce

```sh
python experiments/nov3_poti_tobacco_loading/verify.py --verify
python experiments/nov3_poti_tobacco_loading/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The ordinary check verifies the published key, exact raw domains, source
indices, repair cost, complete re-encryption, internal word match and live
case displays. The optional source check compares every pixel of the
reviewed crop against the pinned public Childs PDF, using PyMuPDF and Pillow.

The earlier OCR mask in `ADV?D` is restored from the visible source `ADVXD`;
it is not counted as a historical fill. The raw R, WAN, VERLADG, K A and
quantity label 2400 remain literal. Earlier key recovery and repository
work retain their separate credit; no first-solution claim is made.
