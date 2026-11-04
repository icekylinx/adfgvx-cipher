# Receipt request through Nikolajew: the other p105 telegram

The message requests radio confirmation through Nikolajew that Mackensen command received the two referenced communications. The raw reference strings A1118 and 111M7, and the final GEW designation, are preserved.

**Complete edition by printed page:** [p. 105](../pages/105.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Case index](../README.md) · [ADFGVX Cipher](../../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

This is the 300-slot **section A** on Childs p105, a request to confirm receipt of two communications to Mackensen command through Nikolajew. It is separate from the original [p105 challenge](../p105.md), which is the 290-slot section B. The complete native source yields 150 fixed output labels without changing any coordinate or square cell.


**Reviewed source crops:** [p105_reviewed.png](../../experiments/nov2_nikolajew_acknowledgment/sources/p105_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## Source and scope

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed source excerpt — source-PDF reference](../../experiments/nov2_nikolajew_acknowledgment/inputs.json) · [Literal inputs](../../experiments/nov2_nikolajew_acknowledgment/inputs.json) · [Position and repair certificates](../../experiments/nov2_nikolajew_acknowledgment/certificates.json)

The published `Nov1-3` key is unchanged. [Earlier OCR evidence](../../experiments/nov2_nikolajew_acknowledgment/ocr_snapshot.json) and its [recomputed decode](../../experiments/nov2_nikolajew_acknowledgment/prior_candidates.json) are retained. This edition adds checked framing, explicit reading limits and a readable display; it makes no first-public-decipherment claim.

| Record | Source slots | Fixed raw positions | Observed substitutions | Source-mask fills |
| --- | ---: | ---: | ---: | ---: |
| [p105 A](#p105-a) | 300 | 150 / 150 | 0 | 0 |

## p105 A

**Source transcription — header:** `A) FUER UKS v LP (5.10 p.m., November 2nd); 1530 (2/11); RICHI-300`

<details>
<summary>Raw decoded text</summary>

**Raw output — every native source slot in printed order:**

```text
ANXOBERKDOXMACKENSENXEMPFANGSBESTAETIGUNGXVONXRMX1XAXA1118XGEHXOPXUNDXRMX1XAX111M7XGEHXOPXUEBERXNIKOLAJEWXDURCHXFTXERBETENXOHLXRMX1XAXNOX104716XGEWXOP
```

</details>

**Readable German — the same nonseparator labels as the unchanged raw output:**

> An Oberkdo. Mackensen. Empfangsbestaetigung von RM. 1. A. A1118 GEH. OP. und RM. 1. A. 111M7 GEH. OP. ueber Nikolajew durch F. T. erbeten. OHL. RM. 1. A. No. 104716 GEW. OP.

**Meaning:** The message requests radio confirmation through Nikolajew that Mackensen command received the two referenced communications. The raw reference strings A1118 and 111M7, and the final GEW designation, are preserved.

### Editorial limits

- This physical record is section A; the original p105 challenge concerns the different 290-slot section B and retains its identifier and earlier attribution.
- All 300 source slots are retained in the printed order. The earlier 308-slot OCR block included seven characters from the next header and expanded printed DXXXX to six characters; correcting the machine transcription is not an alteration of the historical ciphertext.
- The primary readable display changes spacing and punctuation only. A1118, 111M7 and GEW are not silently converted to more familiar references.
- A separately priced interpretation compares the two references with independent p105 C1 and p106 A2; agreement of subject matter supports a reference-identification hypothesis, not an assertion that the telegrams are identical copies.

## Conditional interpretation of the reference fields

The different telegram on [p105 C1](nov2_telegram_acknowledgments.md#p105-c1) addresses A. O. K. Mackensen and prints `11118` and `11127` together in a request to acknowledge receipt. Its continuation [p106 A2](nov2_telegram_acknowledgments.md#p106-a2) again uses `11127`. Those native readings supply a concrete comparison for this section A’s `A1118` and `111M7`.

Identifying the communications mentioned here with that independently received reference pair is an **additional assumption**. The texts have different wording and their own outgoing references. Topic, addressee and date proximity do not prove that their serials must be identical. The native p105 A fields stay unchanged above.

| Proposed change | Extra observed-coordinate substitution | Source index, zero-based |
| --- | ---: | --- |
| `A1118` → `11118` | 1 | 194: `G` → `F` |
| `111M7` → `11127` | 1 | 260: `V` → `F` |
| Final `GEW` → `GEH` | 1 | 94: `G` → `V` |

The first two changes together cost **two substitutions**. The final abbreviation normalization is a separate, third substitution; the reference comparison does not authenticate that footer correction.

**Conditional interpretation — both reference identifications, two substitutions in total:**

```text
ANXOBERKDOXMACKENSENXEMPFANGSBESTAETIGUNGXVONXRMX1XAX11118XGEHXOPXUNDXRMX1XAX11127XGEHXOPXUEBERXNIKOLAJEWXDURCHXFTXERBETENXOHLXRMX1XAXNOX104716XGEWXOP
```

**Conditional interpretation — both references plus the separate footer normalization, three substitutions in total:**

```text
ANXOBERKDOXMACKENSENXEMPFANGSBESTAETIGUNGXVONXRMX1XAX11118XGEHXOPXUNDXRMX1XAX11127XGEHXOPXUEBERXNIKOLAJEWXDURCHXFTXERBETENXOHLXRMX1XAXNOX104716XGEHXOP
```

The verifier independently decodes the cited native records, checks their unchanged key and exact reference positions, and re-encrypts both optional p105 A streams. These alternatives count as no additional physical record and do not enter the primary zero-repair totals.

## Reproduction and credit

Run `python experiments/nov2_nikolajew_acknowledgment/verify.py --verify`. Add `--pdf /path/to/adfgvx-childs.pdf` to check the original PDF and the exact rendered pixels of the preserved source excerpt.

The verifier reconstructs source-coordinate pairs, checks raw domains, replays all priced changes, verifies the readable display without dropping unresolved labels, and checks a global completion witness where required. Such a completion is mechanical evidence, not a historical guess.

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

</details>
<!-- CASE-EDITION:END -->
