# Kremp's request for a departure date — p131, p149 and p159

[Case guide](../README.md) · [ADFGVX Cipher](../../README.md) · [Reading conventions](../../docs/reading-conventions.md)

Kremp reports his recovery and asks the military mission's transport section to set his departure date. The unlettered final message on p159 reads completely under the published **Nov7–9** key: **98 positions, with no source correction**. Its different-key reception also repairs the earlier p131 B / p149 B version.

## Reading

**Readable German:**

> Coeln 11. Ab. 1. S. Milmiss., Transp.-Abt. 1b, Constantinopel.
> Bin wiederhergestellt. Bitte Abfahrtstag bestimmen. Kremp.

**Meaning:** Kremp reports that he has recovered and asks the transport section
of the military mission in Constantinople to specify his departure date.
The opening `COELN11XAB1XSX` is directly decoded; its administrative meaning remains unknown. The displayed spacing and abbreviation breaks are editorial.

The complete p159 plaintext is:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
COELN11XAB1XSXMILMISSTRANSPABT1BCONSTANTINOPELXBINWIEDERHERGESTELLTBITTEABFAHRTSTAGBESTIMMENXKREMP
```

</details>

All 196 source coordinates re-encrypt exactly using established square cells.

## Three source witnesses

| Witness | Source heading and receipt | Key | Directly fixed positions |
| --- | --- | --- | ---: |
| [p131 B](../../experiments/open_targets_continuation/sources/childs_p131_selected.png) | 5 November, continued; received 6 November at 02:36 | `Nov4-6` | 82/84 |
| [p149 B](../../experiments/open_targets_continuation/sources/childs_p149_selected.png) | 6 November, continued; received 7 November at 08:59; internal `0110 (6/11)` | `Nov4-6` | 84/84 |
| [p159, final unlettered item](../../experiments/open_targets_continuation/sources/childs_p159_selected.png) | 9 November; received at 06:12; internal `NR 17 (9/11)` | `Nov7-9` | 98/98 |

The last item follows a fresh **9 November** heading below the three messages
under 8 November. The machine-readable identifier `p159_D` is a local label
for the fourth item; the source itself does not print a `D` beside it.

The p131 and p149 ciphertexts differ at three slots: two p131 dashes correspond to p149 `A`s, and one `D` corresponds to `V`. The p159 reception uses a different transposition, square and address prefix. Its 51-character body matches **48 of 51** directly decoded characters in p149 and **45 of 51** in p131.

## Exact repairs to the earlier version

The p149 source decodes literally as:

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
MILMISTRANSPABT1BKONSTANTINOPELXBINWIEDERHER4ESTELLTBITTEABFA7ETSTAGBESTIMMENXKREMPX
```

</details>

The independently readable p159 body supports `WIEDERHERGESTELLT` and
`ABFAHRTSTAG`. The resulting p149 reconstruction requires precisely three
changes to valid source coordinates, with no insertions or erasure fills:

| Source index, zero based | Printed | Proposed | Plaintext effect |
| ---: | :---: | :---: | --- |
| 134 | X | V | `4` becomes `G` in `WIEDERHERGESTELLT`. |
| 26 | D | G | `7` becomes `H` in `ABFAHRTSTAG`. |
| 106 | F | V | The following `E` becomes `R`. |

The remaining **165 printed coordinates** and the earlier address forms `MILMIS` and `KONSTANTINOPEL` are retained. The 84-position reconstruction re-encrypts to this three-change witness.

For p131, the same body additionally fills its two dashes and changes source
index 145 from `D` to `V`, yielding `BITTE` followed by `ABFAHRTSTAG`.
Its complete repair cost is **four known-coordinate substitutions and two erasure fills**.

## Verification and credit

The [source inputs](../../experiments/open_targets_continuation/inputs.json)
retain all three transcripts, exact headers and image hashes. The
[certificates](../../experiments/open_targets_continuation/certificates.json)
record every plaintext-to-source pair, the independent inverse, all edits and
the two cross-key body alignments.

```sh
python3 experiments/open_targets_continuation/verify.py --verify
```

The source identification, comparison and edition are by **icekylinx and GPT-6 Astra Pro**. Period-key recovery retains [George Lasry's published attribution](../../data/keys.json).
