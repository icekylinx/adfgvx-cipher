# Existing personnel and agreed radio transmissions

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[Case index](../README.md) · [ADFGVX Cipher](../../README.md)

## p127 B1

**Status:** 76/80 native raw positions fixed; 1 observed-coordinate substitution and 3 source-mask fills in the proposal. No frame change. Key: Nov4-6.

**Source and dates:** Page heading: 4th NOVEMBER, 1918; B) LP v NKJ (9.45 p.m., November 5th); 2200 2 TLE; 1 TL RIZI-160.

![Source p127 B1](../../experiments/early_radio_and_leave_records/sources/p127_B1.png)

**Raw output:**

```text
?I?RNOCHALTESPERSONAFXWIRSENDENWIEVERABREDETXWENNNICTMEHRDANNISTOS?AUSGESCHIE?EN
```

**Edited output — counted proposal:**

```text
HIERNOCHALTESPERSONALXWIRSENDENWIEVERABREDETXWENNNICTMEHRDANNISTOS?AUSGESCHIEDEN
```

**Readable German — the same candidate labels with spacing and punctuation:**

> Hier noch altes Personal. Wir senden wie verabredet. Wenn NICT mehr, dann ist OS? ausgeschieden.

**Meaning:** The sender says the previous personnel are still present and transmissions continue as agreed. The final sentence contains the literal defect NICT and an unresolved OS? label. If NICT is intended as NICHT, it conditionally links ceased transmissions with the departure of OS?; that missing H is not inserted into the cryptographic reading.

**Conditional interpretation and source details:** The first source group is AXVFF; ALTES is already present in the complete raw reading. The later group VFFGF contains a clear F, not an out-of-alphabet T; neither visual correction is a historical ciphertext edit. The proposal changes one observed coordinate and fills three printed masks. The fourth mask leaves OS? unresolved. NICT is retained without adding H. Only the first of two announced parts is included.

### Explicit source changes

All indices are zero-based. Printed masks retain their original slots.

| Source index | Printed | Proposed | Cost |
|---:|---|---|---|
| 2 | `V` | `X` | Observed-coordinate substitution |
| 55 | `-` | `A` | Source-mask fill |
| 93 | `-` | `D` | Source-mask fill |
| 94 | `-` | `A` | Source-mask fill |

### Optional OSM field completion

The unresolved position 66 has domain `4CMNST`, from `X?` at source 44 and
111. Reading the station call sign **OSM** fills the remaining printed mask
111 with **F**, giving `XF=M`. This adds one source-mask fill, with no new
observed-coordinate change: the optional total is **one substitution and
four printed-mask fills**, fixing 80/80 positions under the same native frame.

**Edited output — optional OSM identification, one mask fill beyond the preceding proposal:**

```text
HIERNOCHALTESPERSONALXWIRSENDENWIEVERABREDETXWENNNICTMEHRDANNISTOSMAUSGESCHIEDEN
```

**Readable German — same optional labels, retaining NICT:**

> Hier noch altes Personal. Wir senden wie verabredet. Wenn NICT mehr, dann ist OSM ausgeschieden.

This is a conditional identification, supported by the separate
[OSM/OUI staff query](p137_station_staff_query.md) and an independent diary
notice. The [published 2016 study, section 6.5](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf)
identifies OSM with Osmanie. In his entry headed **5 November**, Albert Hopman records at
`11h 30m N` the notice “FT-Station Osmanie von uns aufgegeben”.
[Original diary image, Baumgart edition (1971), p636 / scan646](https://api.digitale-sammlungen.de/iiif/image/v2/bsb00042051_00646/full/1800,/0/default.jpg).
The notice does not quote this telegram. The source's 4 November page heading,
5 November receipt and undated `2200` field remain distinct; no reply relation
or clock reconciliation is asserted. The second announced part remains unread.

[Exact optional-field witness and documentary metadata](../../experiments/early_radio_and_leave_records/osmanie_field_certificate.json)
· [Optional-field verifier](../../experiments/early_radio_and_leave_records/verify_osmanie.py).

### Reproducibility and attribution

The [input](../../experiments/early_radio_and_leave_records/inputs.json) binds each literal source to exact PDF crops. The [certificate](../../experiments/early_radio_and_leave_records/certificates.json) records each raw paired-coordinate domain and every proposed source change. The [verifier](../../experiments/early_radio_and_leave_records/verify.py) checks the live German quotation against the same candidate labels, preserving every digit and unknown position.

This source edition is by icekylinx and GPT-6 Astra Pro (2026). Childs supplies the historical collection. The published reconstruction and unchanged key provenance credit Lasry, Niebel, Kopal and Wacker, with Lasry's published period-key list. Earlier repository OCR input is frozen in the [attribution record](../../experiments/early_radio_and_leave_records/prior_candidates.json); no first-decipherment priority is claimed.
