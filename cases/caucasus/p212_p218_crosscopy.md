# A truncated copy of the Tiflis armistice notice

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source edition and cross-copy analysis: icekylinx and GPT-6 Astra Pro.** Newly edited record: Childs p212 A2. Earlier full witness: p218 A2, already in the [Tiflis armistice edition](p218_A.md). Published `Nov25-28` key, unchanged. [Inputs](../../experiments/p212_p218_crosscopy/inputs.json), [exact certificate](../../experiments/p212_p218_crosscopy/certificates.json), [method and limits](../../experiments/p212_p218_crosscopy/README.md).

The fragment is part of the previously known notice concerning withdrawal from territory that belonged to Russia before the war and the Allies' assessment of its internal situation. Its role is established by the close ciphertext correspondence with the complete p218 part, not by joining it to the medical passages printed around p212.

**The date conflict remains unresolved:** p212 is headed 22 November, while p218's full witness is headed and received 25 November. The edition changes neither date and makes no claim about the cause of the discrepancy.

## p212 A2

[Short-fragment source crop](../../experiments/p212_p218_crosscopy/sources/p212_A2.png); [full p218 A2 witness](../../experiments/p212_p218_crosscopy/sources/p218_A2.png). The p212 source advertises 284 coordinates but prints 160. Of those, 157 are identical to the corresponding p218 prefix. The differences are source indices 46 (`F/G`), 67 (`A/printed dash`) and 103 (`G/X`).

In the 284-coordinate frame, with the absent tail left as 124 erasures, only 30 plaintext positions have both source coordinates visible:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional 284-slot frame with 124 absent tail coordinates left unknown:**

```text
?????????K??E????U??L?N?????????N??A????S??A?D?????????R??7????R??R?E?????????U??D????N??E?L?????????G??I????E??U?E?????????R??K????N??A?H????
```

</details>

### A conditional tail from the full printed witness

Borrowing p218's 124 literal tail coordinates, while preserving every p212 coordinate, gives:

<details>
<summary>Raw decoded text</summary>

**Raw output — conditional cross-copy tail completion from p218:**

```text
DIEVORDEMKRIEGZURUSZLANDGEHOERTENXHABENXSOBALDDIEALLIIERTE7UNTERBERUECKSICHTIGUNGDERJNNERENLAGEDIESERGEBIETEDENAUGENBLICKFUERGEKOMMENERACHTENX
```

</details>

This is a **source-copy reconstruction**, not a reading derived from the fragment alone. All borrowed coordinates have individual provenance in the certificate. Exhausting the 161 possible positions of one contiguous 124-coordinate loss gives the tail placement a unique minimum of two valid-coordinate disagreements. That supports the alignment under the copy assumption; it does not prove that an unseen historical tail was identical.

The copies are complementary. p212's F at index 46 independently supports the earlier `DPN → DEN` correction. Its A at index 67 supplies the missing coordinate in p218's `BERUEC?SICHTIGUNG`. In the other direction, p218's X at index 103 corrects p212's `ALLIIERTE7 → ALLIIERTEN`.

### Conservative readable candidate

Using that one p218 witness correction in the observed p212 prefix, then separately changing borrowed coordinate 217 `X → F` for `JNNEREN → INNEREN`, gives:

<details>
<summary>Proposed text and exact labels</summary>

**Edited output — conditional cross-copy tail completion, followed by the stated repairs:**

```text
DIEVORDEMKRIEGZURUSZLANDGEHOERTENXHABENXSOBALDDIEALLIIERTENUNTERBERUECKSICHTIGUNGDERINNERENLAGEDIESERGEBIETEDENAUGENBLICKFUERGEKOMMENERACHTENX
```

</details>

The received `RUSZLAND` spelling is retained. This is a continuation: “… die vor dem Krieg zu Russland gehörten, haben, sobald die Alliierten unter Berücksichtigung der inneren Lage dieser Gebiete den Augenblick für gekommen erachten …”. The surrounding withdrawal context belongs to the earlier complete three-part p218 notice; no complete p212 medical message is inferred.

Relative to p212's actual source, the candidate uses one observed-coordinate substitution and 124 missing-coordinate fills. Of those fills, 123 are literal p218 values; one is the explicitly separate ordinary-word correction. Thirty plaintext positions use two p212 coordinates, 100 use one coordinate from each copy, and 12 use only borrowed coordinates.

## Still-unread neighboring fragment

p212 A4 remains unread. A bounded comparison of its 197 source coordinates against all 788 frozen OCR blocks found no nonself exact ten-coordinate window. The comparison does not span OCR block boundaries and cannot exclude a re-encrypted or more heavily corrupted copy. This negative control and its literal source are retained in the certificate, outside the restored-reading count.

## Attribution and scope

The full p218 A2 body was already edited and catalogued; its earlier work is not recounted as a new message or a new physical record. The present contribution is recognition of the truncated p212 copy, a conditional tail restoration, and complementary source evidence for earlier repairs. Only p212 A2 is newly proposed for the catalog. No first historical decipherment or changed key/date is claimed.
