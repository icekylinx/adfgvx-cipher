# The Warsaw query and its later quotation — p181 A / p214 B

The Warsaw Soldiers' Council asks for an immediate report on whether the rumor of Mackensen's advance on Warsaw is true. The query does not itself establish that such an advance occurred.

**Complete edition by printed page:** [p. 181](../pages/181.md) · [p. 214](../pages/214.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Case guide](../README.md) · [ADFGVX Cipher](../../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Status:** A 92-character query on p181 is quoted inside a later message on
p214 under a different key. The two direct readings agree at **85 of 92**
aligned positions; their complementary evidence supports a complete query
with every proposed source change recorded. **Source comparison and edition:**
icekylinx and GPT-6 Astra Pro. This is a supplementary message, not a new
solution to an open challenge.

## Reading

**Readable German:**

> Erbitten umgehend Nachricht, ob Geruecht vom Anmarsch Mackensens auf
> Warschau wahr. Soldatenrat Warschau.

**Meaning:** The Warsaw Soldiers' Council asks for an immediate report on
whether the rumor of Mackensen's advance on Warsaw is true. The query does
not itself establish that such an advance occurred.

The later message includes the query in its forwarding body:

**Readable German — earlier cross-key repairs, with one additional separator fill:**

> An OKM. Hier einging folgender Funkspruch: Erbitten umgehend Nachricht, ob Geruecht vom Anmarsch Mackensens auf Warschau wahr. Soldatenrat Warschau.

The address and introductory sentence are directly decoded. The display
treats the erased character after `FUNKSPRUCHX` as a second separator,
filling source **3** with **A** to make **AX=X**. This adds one mask fill
to the earlier cross-key edition and completes the 130-position introduction
and quotation. The whole source now has **145/146** fixed labels, at **three
observed substitutions and four mask fills**. The remaining erasure is in
the closing reference.

The boundary fill is editorial: the source permits `1GJKWX`, so X is not
cipher-forced. [Exact fill, quotation mapping and retained footer domain](../../experiments/open_targets_continuation/p214_completion_certificate.json).

## Prior publication and date discrepancy

Lasry, Niebel, Kopal and Wacker already discuss the Warsaw query in section
6.4 of [*Deciphering ADFGVX messages from the Eastern Front of World War I*](https://www.apprendre-en-ligne.net/crypto/bibliotheque/PDF/adfgvx.pdf),
DOI [10.1080/01611194.2016.1169461](https://doi.org/10.1080/01611194.2016.1169461).
Their narrative assigns it to **13 November**. The inspected p181 page heading
and intercept header both print **12 November**. The source date is retained
here; the discrepancy is not silently resolved.

The present contribution is the cross-key quotation link, direct source
transcription and exact repair accounting. It does not claim first
decipherment of the query or treat the previously published interpretation
as independent cryptographic evidence.

The same prior body credit applies to the quoted query within **p214 B**.
Its forwarding introduction, cross-key source relationship and damaged footer
are assessed separately in this edition.

## Sources and direct readings

| Witness | Source header | Published key | Direct reading |
| --- | --- | --- | ---: |
| [p181 A / PDF p184](../../experiments/open_targets_continuation/sources/childs_p181_selected.png) | `NKJ v LP (06.43 p.m., November 12th); 15.50; RICHI-184` | `Nov10-12` | 91/92 positions fixed |
| [p214 B / PDF p217](../../experiments/open_targets_continuation/sources/childs_p214_selected.png) | `--- v UKS (07.05 p.m., November 22d); 1630 (11/22); RICHI-292` | `Nov22-24` | 141/146 positions fixed |

The unmodified p181 reading is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ERBITTENUMGEHENDNACHRICHTOBGERUECHTVOMANMARSCHMACKEN?ENSAUFWARSCHAUWAHRXSOLDATENRATWARSCHAUX
```

</details>

Its only unknown plaintext position comes from the printed invalid coordinate
`C` in group `AACDD`. The later quote supplies the missing `S` in
`MACKENSENS`. Filling source index **17** with `G` preserves all **183 valid
coordinates**; the resulting 92-character text re-encrypts exactly. No
unknown square cell is assigned.

The p214 source decodes as:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ANOKMXHIEREINGINGFOLGENDERFUNKSPRUCHX?ERBI3TENUM?EHEN?NACHRICHTOBGERUECHT?OMANMARSCHMACKENSENSAUFWARACHAUWAHRXSOLDATENRATWARSCHA8XXAOKYYXRMYAQY?5X
```

</details>

Its 92-position quotation starts at plaintext index **38**. The p181 text
supports three changes to fixed p214 characters and three erasure fills:

| Quote position, zero based | p181 | Direct p214 | Consequence |
| ---: | :---: | :---: | --- |
| 4 | T | 3 | One known-coordinate substitution in p214. |
| 10 | G | ? | One p214 erasure fill. |
| 15 | D | ? | One p214 erasure fill. |
| 35 | V | ? | Fill the invalid printed `S` coordinate in p214. |
| 52 | ? | S | Fill the invalid printed `C` coordinate in p181. |
| 62 | S | A | One known-coordinate substitution in p214. |
| 90 | U | 8 | One known-coordinate substitution in p214. |

The p214 substitutions are source indices **242: F→V**, **208: X→D** and
**170: X→V**. The fills are **4: –→G**, **56: –→G** and **165: S→V**.
The earlier quote reconstruction changes no other source slot. Of its two
remaining erasures, the optional boundary completion above fills source 3;
source 78 in the ending `XAOKYYXRMYAQY?5X` remains unknown. The questionable
fixed closing labels are retained.

## Verification

The [input package](../../experiments/open_targets_continuation/inputs.json)
contains the literal groups, prior-publication note, headers and source image
hashes. The [certificate](../../experiments/open_targets_continuation/certificates.json)
reproduces the quote alignment and each coordinate cost with an independent
column-offset inverse, checked against the project decoder.

```sh
python3 experiments/open_targets_continuation/verify.py --verify
```

George Lasry's period-key publication is credited separately from this source
review and comparison by **icekylinx and GPT-6 Astra Pro**.

## Later conditional reading of the p214 closing label

The independent [late-key interpretation](../../experiments/late_key_interpretation/README.md) applies the p217-derived Nov22–24 numeral hypothesis to the unchanged p214 B source. Its baseline `AOKYY` becomes `AOK11`, consistent with the 11th Army headquarters. The remaining reference stays damaged, and this optional map does not alter the earlier quoted body or its repair costs.

</details>
<!-- CASE-EDITION:END -->
