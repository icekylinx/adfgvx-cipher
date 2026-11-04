<a id="the-interrupted-banknote-instruction-a-complete-later-witness"></a>

# The small-note instruction: the complete banknote witness

The instruction asks for the money in the smallest possible banknotes. A complete later reception restores the ending of the daily crown-airlift request and corrects an earlier conjecture about the missing text.

**Complete edition by printed page:** [p. 195](../pages/195.md)

<!-- CASE-EDITION:START -->
<details>
<summary>Full source edition and evidence</summary>


[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

Childs p195 A2 preserves the complete 98-coordinate reception of the instruction interrupted after 79 coordinates in p174 A3. The copy restores the ending of the [daily crown-airlift request](crown_airlift.md), fixes the gap's position and corrects one earlier conjecture. Both use the published **Nov10–12** key.

**Readable German — one-repair later witness; reference labels retained:**

> IN MOEGLICHST KLEINEN SCHEINEN SENDEN X X OKM1A4A11333OP

The instruction asks for the money in the smallest possible notes. The earlier parts request one million crowns daily, alternately to Kronstadt and Hermannstadt. The closing reference `OKM1A4A11333OP` remains unexpanded.

## What the second source establishes

The two records share 78 of their first 79 observed coordinates. The single
disagreement is at zero-based index 65: p174 has A and p195 has X. Selecting
the complete copy’s X changes the earlier L after `SENDEN` into a second X.

The nineteen newly observed tail coordinates raise the earlier frame from **30 to 48 fixed positions out of 49**. Eleven of the twelve previously conjectured values agree with the complete copy; one requires correction.

<details>
<summary>Unchanged raw stream, literal tail and gap comparison</summary>

**Raw output:**

```text
INMOEGLICHSTKLEINENSCHEINEN?ENDENXXOKM1A4A11333OP
```

**Source transcription — tail coordinates supplied by the complete witness:**

```text
AVDVVDFDAFXVADADXDA
```

Among all eighty placements of a contiguous nineteen-coordinate gap, boundary 79 uniquely minimizes source disagreements. The earlier word-based comparison retained boundaries 77–79. The selected boundary leaves the one prefix disagreement described above.

</details>

## One ordinary word still requires a source repair

The first label of `?ENDEN`, at plaintext position 27, has square domain **56789**. Since S is assigned elsewhere, `SENDEN` requires the observed-coordinate change **p195 source 95, X→D**.

This is also where the full copy contradicts an earlier conjectural fill.
The common edited tail retains eighteen source values literally and changes
one. The p195 record has no printed erasures and needs no added, removed or
reordered coordinate. Its own 49-position frame has 48 raw fixed labels and
49 in the one-repair proposal.

## Preserve the conflicting headers

| Source | Page heading and receiving time | Reference and part marker | Observed slots |
|---|---|---|---:|
| p174 A3 | November 10; 7.24pm on November 10 | 17.50; third part of a three-part message | 79 |
| p195 A2 | November 15; 1.17am on November 15 | 1750; `2 TL` | 98 |

The close source match coexists with different dates and part numbers. Their original placement within a larger multipart sequence remains unresolved.

## Source and exact verification

The [p195 image](../../experiments/retrieved_copy_editions/sources/p195.png)
is from Childs, *General Solution of the ADFGVX Cipher System*,
[scanned volume](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The [inputs](../../experiments/retrieved_copy_editions/inputs.json) and
[certificate](../../experiments/retrieved_copy_editions/certificates.json)
retain the original-coordinate comparison, all eighty gap costs, the contradicted fill, raw domains and exact re-encryption witnesses. Partial-square completions serve only as arithmetic witnesses.

The second-copy identification, comparison and edition are by **icekylinx and GPT-6 Astra Pro**. The Nov10–12 key retains its [published attribution](../../data/keys.json).

```sh
python experiments/retrieved_copy_editions/verify.py --verify
python experiments/retrieved_copy_editions/verify.py --verify --pdf /path/to/childs.pdf
```

</details>
<!-- CASE-EDITION:END -->
