# Late-November cipher and routing instructions — p225–228

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source reading and verification: icekylinx and GPT-6 Astra Pro. Published period keys: George Lasry and collaborators.**

Five ciphertext records and one cleartext notice describe missing December key tables, proposed sharing of keys, a fragment of a numerical-code instruction, and direct routing to an army station. All ciphertext below is read with the unchanged published **Nov28–Dec1** key. These messages give evidence about specific communications arrangements; they do not assign a key to an unresolved challenge.

| Record | Received slots | Fixed raw positions, including garbles | Content |
|---|---:|---:|---|
| p225 A | 232 | 110/116 | UKS to use a November key from 1 December because December tables have not arrived |
| p226 B2 | 208 | 104/104 | Surviving continuation about reading numerical sequences backwards |
| p227 B | 152 | 76/76 | Send messages for the army and subordinate formations directly to ZOEN |
| p228 C1 | 176 | 88/88 | Agreement involving UKS, ZOEN and BSL about the December key |
| p228 C2 | 144 | 72/72 | BSL and UKS should use the same key; UKS agrees |
| p227 C | Cleartext | Not a decipherment | ITOCHI parts cannot be deciphered; request RICHI or plaintext |

## November key reused because December tables are missing

p225 A is headed `BSL v UKS (09.24 p.m., November 28th)`, `2200 (28/11)`, `RIZI-232`. Its raw text is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
STATI?NUKSCHIFFRABERSTENDEZMITNSLNOVYD?DEZTAFELNNOCHNICGTEINGEGANG?NYBITTE?EL?GDANUNSEBENFALLSMITNSLNOVSCHLUES?ELNYY
```

</details>

The readable content is an instruction that station UKS should encipher from 1 December using the November material, because the December tables have not yet arrived. It requests reciprocal use of that material. The raw string **`NSL` occurs twice** and is preserved: interpreting it as another call sign or replacing it with `BSL` would be an additional assumption.

The literal invalid `R` in `DFGVR` and all five printed dashes remain source slots. The unenciphered annotation following the 232-slot message is not appended to its cipher stream. [Source image](../../experiments/corpus_extension/sources/p225_A.png).

## An explicit agreement to use the same key

p228 C is headed `BSL v ZON` (the O has two marks), `04.47 a.m., December 1st`, `0420 (11/30) 2 TLE`. Both parts are directly readable without any coordinate repair:

<details>
<summary>Raw decoded text</summary>

**Raw output — two separate source parts under the unchanged key:**

```text
p228 C1
MITYUKSYVEREINBARTEYZOENYDEZEMBERSCHLUESSELWIEYBSLYZWISCHENYBSLYUNDYZOENYVORGESCHLAGENYY

p228 C2
IMVERKEHRYBSLYUNDYUKSYGLEICHENSCHLUESSELVERWENDENYYUKSYISTEINVERSTANDENY
```

</details>

The first part reports an arrangement with UKS concerning the December key as proposed between BSL and ZOEN. The second is explicit: use the same key in BSL–UKS traffic, and UKS agrees. Together, the two source streams retain **320/320 coordinates** and directly fix **160/160 plaintext positions**. This does not establish which particular November day's key the parties subsequently used. [Source image](../../experiments/corpus_extension/sources/p228_C.png).

## Numerical-code fragment and army routing

p226 B2 says that its first part is missing. The surviving continuation directly gives:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ZAHLENREIHENVONRUECKWAERTSGELESENYSODASSXYXSZ8HLEN3Y5Y9YX5YX0YUYSYWYYBENUTZENSIEGLEICHESMITUNFYANTWORTYY
```

</details>

The beginning says that numerical sequences are read backwards; the end asks the recipient to use the same procedure in communication with the sender and to answer. `Z8HLEN → ZAHLEN` and `MITUNF → MITUNS` cost two coordinate substitutions. The central examples, including `XYXS` and `3Y5Y9YX5YX0`, remain literal. The missing first part and those garbles prevent reconstruction of a complete numerical-code rule. [Source image](../../experiments/corpus_extension/sources/p226_B2.png).

p227 B directly reads:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
BITTEFUNKSPRUECHEANXXYARMEEUNDUNTERSTEL6TEFORMATIONENUNMITTELBARANZOENGEBENY
```

</details>

Restoring `UNTERSTELLTE` costs one coordinate substitution. The raw army field **`XX`** is retained, without silently treating it as an Arabic number or Roman numeral. [Source image](../../experiments/corpus_extension/sources/p227_B.png).

## Separate historical interpretation of the army field

The later [unit-based key-label review](../../experiments/late_key_interpretation/README.md) applies the optional p230 map to p227 B. Baseline `X→1` and the separate `Y→X` separator convention give **11th Army**; with the already counted one-coordinate repair of `UNTERSTELLTE`, the instruction asks for telegrams to the 11th Army and subordinate formations to be sent directly to ZOEN. The baseline text above remains the unchanged-key result. Applying the same declared layers to p226 B2 leaves its numerical examples damaged and does not recover the missing code rule.

## A cleartext request to avoid an unreadable cipher

p227 C, headed `BSL v UKS`, `2316 (11/28) K. M. BERLIN`, says that parts 3 and 4 of a referenced War Department message in **ITOCHI** cannot be deciphered. It requests **RICHI or plaintext**, then asks that ciphering be avoided if possible in future. This is a directly visible unencrypted source notice, not a new cryptanalytic result. The literal misspellings and the trailing forwarding annotation are retained in the input record. [Source image](../../experiments/corpus_extension/sources/p227_C.png).

## Evidence

[Literal inputs](../../experiments/corpus_extension/inputs.json) preserve every coordinate, invalid glyph and header. The [certificate](../../experiments/corpus_extension/certificates.json) checks the independent inverse, each raw domain and every stated word repair.

```sh
python experiments/corpus_extension/verify.py --verify
```
