# Childs: all twelve numbered instructional examples

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The twelve numbered exercises I–XII at printed pp 19–22 contain **2,058 printed ciphertext coordinates and 1,029 plaintext labels**. Each is fully decoded by the existing complete 17-column `Worked-example-VIKINGSCROWNHOTEL` key. These examples extend coverage of the technical paper and are counted separately from the 679 historical ciphertext bodies in Appendix B.

The primary edition makes **no source substitutions, fills, insertions, deletions or key changes**. Every plaintext label is tied to its two source coordinates, and each complete raw stream encrypts back to the exact printed transcription. The spelling `LAYLIGHT`, the label `I000`, and the incomplete endings of I and VIII are retained.

## Source and reproducibility

[Original Childs scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view), printed pp 11–12 for the instructional key and pp 19–22 for the exercises. Page-specific render rectangles, dimensions and RGB hashes are in `inputs.json`; no new scan images are distributed in this package. The default check verifies the text and arithmetic. Passing the original PDF additionally authenticates its complete file hash and the actual rendered source pixels.

```sh
python experiments/childs_instructional_examples/verify.py --verify
python experiments/childs_instructional_examples/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

## Exact raw and readable editions

### Exercise I · printed 19

Raw output — supplied instructional key, native 212-coordinate frame, no edits.

```text
AIRRECONNAISSANCEINDICATESAREDFORCEESTIMATEDASADIVISIONWITHTRACTORDRAWNARTILLERYWHICHMOVEDSOUTHFROMTHELINE
```

Readable English — spacing, case and punctuation only; all letters and numerical labels are preserved.

> Air reconnaissance indicates a red force estimated as a division with tractor drawn artillery which moved south from the line.

The printed exercise ends with a sentence fragment; no missing continuation is supplied.

### Exercise II · printed 19

Raw output — supplied instructional key, native 108-coordinate frame, no edits.

```text
NOINDICATIONSOFATTEMPTSTOORGANIZETHEGROUNDWEREOBSERVED
```

Readable English — spacing, case and punctuation only; all letters and numerical labels are preserved.

> No indications of attempts to organize the ground were observed.

### Exercise III · printed 19

Raw output — supplied instructional key, native 186-coordinate frame, no edits.

```text
FIRSTCAVALRYNOWATLITTLESTOWNWITHPATROLSALONGTHEINTERNATIONALBOUNDARYISATTACHEDTOFIRSTDIVISION
```

Readable English — spacing, case and punctuation only; all letters and numerical labels are preserved.

> First Cavalry now at Littlestown with patrols along the international boundary is attached to First Division.

### Exercise IV · printed 20

Raw output — supplied instructional key, native 110-coordinate frame, no edits.

```text
SERVICETRAINSWILLACCOMPANYALLMARCHCOLUMNSINREGULARORDER
```

Readable English — spacing, case and punctuation only; all letters and numerical labels are preserved.

> Service trains will accompany all march columns in regular order.

### Exercise V · printed 20

Raw output — supplied instructional key, native 202-coordinate frame, no edits.

```text
ATLAYLIGHTONEBATTERYOFLIGHTARTILLERYWASLOCATEDSOUTHOFCROSSROADS490ANDONEBATTERYSOUTHEASTOFGRANITEHILL
```

Readable English — spacing, case and punctuation only; all letters and numerical labels are preserved.

> At LAYLIGHT one battery of light artillery was located south of crossroads 490 and one battery southeast of Granite Hill.

The visible source has A at zero-based ciphertext index 23 and therefore decodes LAYLIGHT. DAYLIGHT is a separately priced one-coordinate editorial proposal, not a source transcription correction.

### Exercise VI · printed 20

Raw output — supplied instructional key, native 120-coordinate frame, no edits.

```text
NOOTHERREDTROOPSHAVEBEENREPORTEDSOUTHOFSTATEHIGHWAYNUMBER231
```

Readable English — spacing, case and punctuation only; all letters and numerical labels are preserved.

> No other red troops have been reported south of State Highway Number 231.

### Exercise VII · printed 20/21

Raw output — supplied instructional key, native 254-coordinate frame, no edits.

```text
TENTHDIVISIONWILLMARCHWITHOUTDELAYSECURETHEHIGHGROUNDSOUTHOFCONEWAGOCREEKNEARHUNTERSTOWNTOCOVERTHEADVANCEOFTHEREMAINDEROFTROOPS
```

Readable English — spacing, case and punctuation only; all letters and numerical labels are preserved.

> Tenth Division will march without delay secure the high ground south of Conewago Creek near Hunterstown to cover the advance of the remainder of troops.

### Exercise VIII · printed 21

Raw output — supplied instructional key, native 144-coordinate frame, no edits.

```text
THEFIRSTBRIGADEWITHONEPLATOONFIRSTTANKCOMPANYATTACHEDTOMAKEITSMAINEFFORT
```

Readable English — spacing, case and punctuation only; all letters and numerical labels are preserved.

> The First Brigade with one platoon First Tank Company attached to make its main effort.

The printed exercise ends with a sentence fragment; no missing continuation is supplied.

### Exercise IX · printed 21

Raw output — supplied instructional key, native 182-coordinate frame, no edits.

```text
ONEBATTALIONSECONDBRIGADETOPROCEEDTOTHEVICINITYOFJLILLYBY7AMANDAWAITORDERSINDIVISIONRESERVE
```

Readable English — spacing, case and punctuation only; all letters and numerical labels are preserved.

> One battalion Second Brigade to proceed to the vicinity of J. Lilly by 7 AM and await orders in division reserve.

### Exercise X · printed 21

Raw output — supplied instructional key, native 130-coordinate frame, no edits.

```text
ARTILLERYTOHAVEPRIORITYONROADSBETWEEN11PMAND12MIDNIGHT6DASH7APRIL
```

Readable English — spacing, case and punctuation only; all letters and numerical labels are preserved.

> Artillery to have priority on roads between 11 PM and 12 midnight 6 DASH 7 April.

DASH is a literal four-letter plaintext string and is retained in the readable text. No numerical labels are relabelled.

### Exercise XI · printed 21/22

Raw output — supplied instructional key, native 186-coordinate frame, no edits.

```text
ARMYAMBULANCESWILLEVACUATETHECASUALTIESOFTHEBRIGADEFROMTHEBRIGADEHOSPITALSTATIONVIAGETTYSBURG
```

Readable English — spacing, case and punctuation only; all letters and numerical labels are preserved.

> Army ambulances will evacuate the casualties of the brigade from the brigade hospital station via Gettysburg.

### Exercise XII · printed 22

Raw output — supplied instructional key, native 224-coordinate frame, no edits.

```text
ANIMALELEMENTSOFSERVICETRAINSWITHHEADOFCOLUMNI000YARDSNORTHWESTOF2TAVERNSAREFOLLOWINGFIELDTRAINSOFTHESOUTHCOLUMN
```

Readable English — spacing, case and punctuation only; all letters and numerical labels are preserved.

> Animal elements of service trains with head of column I000 yards northwest of 2 Taverns are following field trains of the south column.

The unedited label is I000, beginning with letter I. Changing it to 1000 requires two observed-coordinate substitutions; the readable edition keeps I000.

## Optional editorial proposals

Two proposals are priced separately and do not replace the source edition:

| Exercise | Primary label | Proposed label | Observed-coordinate cost |
|---|---|---|---|
| V | LAYLIGHT | DAYLIGHT |1 substitution: source index 23, A → X |
| XII | I000 |1000 |2 substitutions: source 31 A → G and 176 D → F |

The certificate retains the complete proposed streams, their exact source changes and their re-encryption witnesses. Linguistic or numerical plausibility alone does not turn a proposal into a printed-source correction.

## Credit and limits

Original exercises and instructional key: J. Rives Childs, printed pp 11–12 and 19–22. Independent transcription, source mapping and reproducible edition: icekylinx and GPT-6 Astra Pro.

- These are 12 numbered instructional examples, not twelve 1918 radio intercepts. They do not change the 679-body Appendix B denominator.
- All 1029 plaintext labels are fixed under the explicitly supplied complete instructional key; this is not a newly recovered historical key or a universal first-decipherment claim.
- Examples I and VIII end with the incomplete wording actually printed; no continuation is invented.
- The original spelling LAYLIGHT and the numerical-looking label I000 are preserved in every primary display.
