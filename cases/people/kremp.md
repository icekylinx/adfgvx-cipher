# Kremp's request for a departure date — p131, p149 and p159

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

[Case guide](../README.md) · [ADFGVX Cipher](../../README.md)

**Status:** The unlettered final message on p159 is completely readable under
the unchanged published `Nov7-9` partial key: all **98 plaintext positions**
use established cells and all **196 source coordinates** re-encrypt exactly.
Its body supplies a second-key witness for the more damaged p131 B / p149 B
version. **Source assembly, comparison and edition:** icekylinx and GPT-6
Astra Pro. Period-key recovery retains [George Lasry's published
attribution](../../data/keys.json); no first-decipherment priority is claimed.

## Reading

> Coeln 11. Ab. 1. S. Milmiss., Transp.-Abt. 1b, Constantinopel.
> Bin wiederhergestellt. Bitte Abfahrtstag bestimmen. Kremp.

**Meaning:** Kremp reports that he has recovered and asks the transport section
of the military mission in Constantinople to specify his departure date.
The opening `COELN11XAB1XSX` is directly decoded, but its administrative
meaning is not established. Spaces, punctuation and the displayed abbreviation
breaks are editorial. The person's identity and the cause of his earlier
incapacity are not inferred.

The complete p159 plaintext is:

```text
COELN11XAB1XSXMILMISSTRANSPABT1BCONSTANTINOPELXBINWIEDERHERGESTELLTBITTEABFAHRTSTAGBESTIMMENXKREMP
```

No source correction, missing-coordinate guess or unused square assignment is
needed for this reading. The two unassigned digits in the published `Nov7-9`
square are not used by this message.

## Three source witnesses

| Witness | Source heading and receipt | Key | Directly fixed positions |
| --- | --- | --- | ---: |
| [p131 B](../../experiments/open_targets_continuation/sources/childs_p131_selected.png) | 5 November, continued; received 6 November at 02:36 | `Nov4-6` | 82/84 |
| [p149 B](../../experiments/open_targets_continuation/sources/childs_p149_selected.png) | 6 November, continued; received 7 November at 08:59; internal `0110 (6/11)` | `Nov4-6` | 84/84 |
| [p159, final unlettered item](../../experiments/open_targets_continuation/sources/childs_p159_selected.png) | 9 November; received at 06:12; internal `NR 17 (9/11)` | `Nov7-9` | 98/98 |

The last item follows a fresh **9 November** heading below the three messages
under 8 November. The machine-readable identifier `p159_D` is a local label
for the fourth item; the source itself does not print a `D` beside it.

The p131 and p149 ciphertexts differ at only three slots: p131 has two printed
dashes where p149 has `A`, and one printed `D` where p149 has `V`. They are
therefore close ciphertext witnesses, rather than two independent keys.
The p159 message uses a different transposition, square and address prefix.
Its 51-character body aligns with **48 of 51** directly decoded characters in
p149 and **45 of 51** in p131.

## Exact repairs to the earlier version

The p149 source decodes literally as:

```text
MILMISTRANSPABT1BKONSTANTINOPELXBINWIEDERHER4ESTELLTBITTEABFA7ETSTAGBESTIMMENXKREMPX
```

The independently readable p159 body supports `WIEDERHERGESTELLT` and
`ABFAHRTSTAG`. The resulting p149 reconstruction requires precisely three
changes to valid source coordinates, with no insertions or erasure fills:

| Source index, zero based | Printed | Proposed | Plaintext effect |
| ---: | :---: | :---: | --- |
| 134 | X | V | `4` becomes `G` in `WIEDERHERGESTELLT`. |
| 26 | D | G | `7` becomes `H` in `ABFAHRTSTAG`. |
| 106 | F | V | The following `E` becomes `R`. |

The remaining **165 printed coordinates** are unchanged. Re-encryption of
the 84-position reconstruction reproduces precisely this three-change
witness. The original `MILMIS` and `KONSTANTINOPEL` spellings are retained;
the later message's `MILMISS` and `CONSTANTINOPEL` do not justify changing
the earlier address.

For p131, the same body additionally fills its two dashes and changes source
index 145 from `D` to `V`, yielding `BITTE` followed by `ABFAHRTSTAG`.
Its complete repair cost is **four known-coordinate substitutions and two
erasure fills**. The literal source remains preserved separately in every
case.

## Verification and credit

The [source inputs](../../experiments/open_targets_continuation/inputs.json)
retain all three transcripts, exact headers and image hashes. The
[certificates](../../experiments/open_targets_continuation/certificates.json)
record every plaintext-to-source pair, the independent inverse, all edits and
the two cross-key body alignments.

```sh
python3 experiments/open_targets_continuation/verify.py --verify
```

This is a supplementary corpus reading, outside the 22 challenge targets.
The period keys are prior work; the source checks and comparison here are by
**icekylinx and GPT-6 Astra Pro**.
