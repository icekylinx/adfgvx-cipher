# Request for a position on a Dobrudscha report

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p142 C asks for a response to an Entente report of renewed Romanian
occupation of the Dobrudscha. The message is addressed to the literal
`N.O. MACKENSEN` field and closes with `ABT FREMDE HEERE`. This edition
recovers the report's wording; it does not independently establish the
military event or expand the abbreviated addressee's office.

## Source and reading

The primary source is J. Rives Childs, *General Solution of the ADFGVX Cipher
System*, [printed p142, PDF p145](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [C crop](../../experiments/radio_contacts_and_keys/sources/childs_p142_C.png)
is under a November 6 heading:

```text
C) NKJ v LP (09.00 p.m., November 6th)
FUER UKS 1915 (6/11)
RICHI-242
```

The 242-slot source contains two printed dashes. The unchanged published
`Nov4-6` key fixes 119 of 121 raw positions:

```text
?NXNXOXMACKENSENXENTENTEMELDETX5011XERNEUTRUMAENISCHE?ESETZUNGDERXDOBRU2SCHAXSTELLUNGSNAHMEERBETENXABTXFREMDEHEERED17U560
```

One known-coordinate substitution and two dash fills give:

```text
ANXNXOXMACKENSENXENTENTEMELDETX5011XERNEUTRUMAENISCHEBESETZUNGDERXDOBRUDSCHAXSTELLUNGSNAHMEERBETENXABTXFREMDEHEERED17U560
```

Readable core, with the reference retained literally:

> An N.O. Mackensen. Entente meldet `5011` erneut rumänische Besetzung
> der Dobrudscha. Stellungnahme erbeten. Abt. Fremde Heere `D17U560`.

The numerical/reference labels **`5011`** and **`D17U560`** remain as read.
They are not normalized into dates or message numbers. The raw `2` within
`DOBRU2SCHA` is retained in the raw reading and explicitly repaired locally
to `D`; this does not reassign the square's digit `2`.

| Source index, zero-based | Printed group / position, one-based | Change | Treatment |
| ---: | --- | --- | --- |
| 8 | 2 / 4 | `G` → `F` | Known-coordinate substitution: `2` → `D` in the place name |
| 34 | 7 / 5 | printed dash → `V` | Source-erasure fill: `B` in `BESETZUNG` |
| 84 | 17 / 5 | printed dash → `V` | Source-erasure fill: initial `A` in `AN` |

The source length, transposition and full published square are unchanged.
The [certificate](../../experiments/radio_contacts_and_keys/certificates.json)
includes every source-coordinate origin and the exact reconstructed witness.

```sh
python experiments/radio_contacts_and_keys/verify.py --verify
```

The key is prior work by **George Lasry, Ingo Niebel, Nils Kopal and Arno
Wacker**, [DOI 10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461),
with provenance in the [inputs](../../experiments/radio_contacts_and_keys/inputs.json).
Earlier unreviewed OCR-derived candidates existed. The bounded paper review
does not establish universal first-decipherment priority; exact arithmetic
does not prove unique historical wording or independent truth of the report.
