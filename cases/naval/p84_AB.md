# p84 A/B — Release of oil and Black Sea shipping safety

[ADFGVX Cipher](../../README.md) · [All readings](../README.md) · [Coordinate certificate](../../experiments/corpus_recovery/certificates.json) · [Reading conventions](../../docs/reading-conventions.md)

**Two complete, unchanged-source readings.** The published October 28–31 key
deciphers all **223 plaintext positions** from **446 received coordinates**.
Neither record needs a source correction, missing-coordinate fill or new key
assignment. The page is headed **30 October 1918**, while both reception
headers explicitly say **1 November**; these date layers remain distinct.

## A: Has the order to release the oil succeeded?

**Readable German:**

> Drahtet, ob erneuter Befehl Izzet Pascha — Izzet Pascha — zur Freigabe
> der Oele Erfolg gehabt hat. Kriegsamt, Kriegsrohstoffabtlg.
> Nr. 0, roem. 1.

**Meaning:** Telegraph whether Izzet Pasha's renewed order to release the
oil has been successful. The signature names the War Office's raw-materials
department. The clear routing names Captain Gerlach at Batum as the
representative of the Prussian War Ministry.

The name **IZZETPASCHA** occurs twice in the decrypted text, separated by
`X`; both occurrences are preserved. Its repetition is not repaired by
deleting ciphertext. The footer is literally **0ROEM1**. Its intended
administrative notation is not independently established.

The [source](../../experiments/corpus_recovery/sources/p84_A.png) gives
`FUER POT v NKJ (4.17 a.m., November 1st)` and `RICHI-244`. A time before
`(30)` is partly illegible. All 244 ciphertext coordinates are legible.

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
DRAHTETOBERNEUTERBEFEHLIZZETPASCHAXIZZETPASCHAZURFREIGABEDEROELEERFOLGGEHABTHATXXKRIEGSAMTKRIEGSROHSTOFFABTLGXNRX0ROEMX1XX
```

</details>

All **122/122** positions follow directly from the stated source and key.
The displayed prose adds spacing and punctuation only.

The [p83 A source edition](gerlach_oil_release_query.md) preserves the same
244-coordinate body. Its clearer internal heading reads `1830 (30)`; the
partly illegible p84 time remains transcribed as such. The p83 edition also
retains a conservative five-overprint mask branch, for which the clear p84
coordinates supply the five fills.

## B: Request daily reports on Black Sea shipping

**Readable German:**

> Erbitten fuer Truppenkdo. Kaukasus, wenn moeglich taeglich, kurze
> Mitteilung, ob Schwarze-Meerschiffahrt gefaehrdet.

**Meaning:** The Caucasus troop command requests a short daily report,
if possible, on whether shipping in the Black Sea is at risk. The message
asks for the assessment; it does not itself report that shipping is unsafe.

The [source](../../experiments/corpus_recovery/sources/p84_B.png) gives
`OSM v NKJ (3.30 a.m., November 1st)`, the clear routing
`316 15/10 V POT 1021 FUER OSM UND COS (30) VON POT`, and `RICHI-202`.
The body has exactly 202 valid coordinates.

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ERBITTENFUERTRUPPENKDOXKAUKASUSWENNMOEGLICHTAEGLICHKURZEMITTEILUNGOBSCHWARZEMEERSCHIFFAHRTGEFAEHRDETX
```

</details>

All **101/101** positions are fixed with no source edit.

## Source, verification and credit

J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed
p84 / PDF p87 in the [public scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [source package](../../experiments/corpus_recovery/README.md) retains
every literal coordinate, source-image hash and plaintext-coordinate pair.
Both plaintexts independently re-encrypt to the complete, unchanged source.

```sh
python3 experiments/corpus_recovery/verify.py --verify
```

The published period key keeps the historical and modern researchers'
attribution in [the key register](../../data/keys.json). Source inspection,
exact verification and this edition: **icekylinx and GPT-6 Astra Pro**.
No first historical decipherment priority is claimed.
