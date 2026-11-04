# A second-part instruction on security measures at own discretion

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

A complete native second-part body directs security measures according to one’s own discretion. Its first part is not supplied. Six explicitly priced coordinate changes recover the ordinary-word clause while the opening label, two irregular spellings and three coupled reference positions remain literal or unresolved.


**Reviewed source crops:** [p184_reviewed.png](../../experiments/group_security_measures_fragment/sources/p184_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed p184 excerpt — source-PDF reference](../../experiments/group_security_measures_fragment/inputs.json) · [Inputs](../../experiments/group_security_measures_fragment/inputs.json) · [Position and change certificates](../../experiments/group_security_measures_fragment/certificates.json)

The published `Nov13-15b` key is unchanged. [Original OCR records](../../experiments/group_security_measures_fragment/ocr_snapshot.json) and [reproducible comparisons with that earlier evidence](../../experiments/group_security_measures_fragment/prior_candidates.json) are preserved separately. The present edition supplies checked source framing, exact costs and readable passages; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p184 A2](#p184-a2) | 202 | 96 / 101 | 6 | 0 |

## p184 A2

**Source transcription — header:** `Page heading 13th November 1918; A) 2 TL; RICHI-202`

<details>
<summary>Source and cipher evidence</summary>

**Raw output — every native source slot in printed order, with non-coordinate glyphs masked:**

```text
HIFUERUALLEFUERDIESIMHERHEITDE6GRUPPENOTIGENMASSREGLNNACHEIG?NEMERMASSENZUTR?FFENXOHLRM1ANR11???GEHOP
```

**Edited output — 6 observed-coordinate substitutions and 0 source-mask fills; no insertion, deletion or reordering:**

```text
HIFUERUALLEFUERDIESICHERHEITDERGRUPPENOTIGENMASSREGLNNACHEIGENEMERMESSENZUTREFFENXOHLRM1ANR11???GEHOP
```

</details>

**Readable German — exact nonseparator labels of the edited output:**

> HIFUERU. Alle fuer die Sicherheit der Gruppe NOTIGEN MASSREGLN nach eigenem Ermessen zu treffen. OHL RM1A NR11??? GEH OP.

**Meaning:** The surviving second part calls for taking the necessary measures for the security of the group according to one’s own discretion. The opening HIFUERU remains unexplained, and the particular group and reference number are not identified. This is an instruction fragment, not evidence that the measures were carried out.

**Editorial limits.**

- The printed second-part body has 202 valid source coordinates and matches its RICHI-202 header. High-resolution inspection confirms five glyphs in the last complete five-coordinate group FXVFA, followed by DG and a clear final G in DXGFG. No source erasure, insertion or deletion is introduced.
- The first part is not supplied. HIFUERU remains a literal unexplained opening, rather than being shortened or rewritten into a familiar introductory word.
- NOTIGEN and MASSREGLN are retained exactly; missing vowel letters in familiar spellings are not silently inserted.
- The proposal repairs SIMHERHEIT, DE6 to DER, EIG?NEM, ERMASSEN and ZUTR?FFEN at six observed-coordinate substitutions. The 6 in DE6 is a known label and its change is paid for. The two question marks in EIG?NEM and ZUTR?FFEN come from the fully observed unassigned AF square cell; proposing E at each position is separately paid for by coordinate changes, not by changing the key.
- The first and third unknowns in the final NR11??? field are the same fully observed GA square cell, at plaintext 93 and 95. The middle unknown is the distinct GD cell at 94. The two cells must receive different members of {2,3,4,7,8,9,Q,Y}; no assumption that the labels are digits is imposed.

## Evidence, credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The certificates independently reconstruct column positions and domains, compare them with the cipher implementation, replay every priced change, and check all readable nonseparator labels. Partial readings have one consistent injective square/source-mask completion witness that re-encrypts exactly; those witness choices are not historical identifications. Source images are bound to the original PDF by page, rectangle, scale, file digest and pixel digest.

Reproduce with `python experiments/group_security_measures_fragment/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and exact source-crop pixels.
