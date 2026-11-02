# Neuhof demobilization instruction, p228 B

**Source edition and recovery: icekylinx and GPT-6 Astra Pro.**
The published `Nov28-Dec1` square and ranks are credited to George Lasry,
Ingo Niebel, Nils Kopal and Arno Wacker. No numerical interpretation or
baseline-square change is applied here.

Exact source transcription restores B1's **246 slots**, compared with the
earlier 241-coordinate OCR stream, and produces a readable instruction
about a Flak unit's demobilization at **Neuhof, south of Fulda**. B2's
conditional 33-character opening specifies the Hanau-Fulda railway line.
B3 repeats that the relevant field-army items are to be sent to Neuhof.
The unidentified Flak unit's `?0` field and all reference labels remain open.

## Scope by physical source part

| Part | Actual slots | Printed dashes | Raw fixed labels | Edition fixed labels | Known-coordinate changes | Erasure fills | Language-reading scope |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| B1 | 246 | 6 | 117 / 123 | 122 / 123 | 5 | 5 | Readable body; references and unit field retained |
| B2 | 264 | 43 | 89 / 132 | 99 / 132 | 5 | 10 | **Only the first 33 positions** receive a proposed coherent reading |
| B3 | 186 | 1 | 92 / 93 | 93 / 93 | 0 | 1 | Readable direction; raw office/reference labels retained |
| **Total** | **696** | **50** | **298 / 348** | **314 / 348** | **10** | **16** | B2's final **99 positions** remain unasserted |

The 314-label total includes uninterpreted surviving labels in B2's
unread remainder. It must not be described as 314 recovered coherent
original-language characters. The proposed opening is:

```text
ANSTRECKEHANAUFULDADEMOBILGEMACHT
```

The source's B3 label is literally **`RICHI-196?`**, while the actual text
has **186 slots**. The working frame uses the counted source. The printed
question mark and length discrepancy remain explicit; no ten-coordinate
loss is inferred. B1's `NICHIN` and B3's `DARMSADT` remain in the edition.
Neither phrase receives an inserted `T` merely to regularize its spelling.

## Evidence and verification

- [Source, manual rows and proposed spans](inputs.json).
- [Exact source/reading/repair certificates](certificates.json).
- [Whole source section](sources/p228_B.png), with enlarged part images.
- [Readable edition](../../cases/military/neuhof_demobilization.md).

```sh
python experiments/neuhof_demobilization/verify.py --verify
```

The standard-library verification checks image hashes, the unchanged key,
the independent physical-column inverse, all repair prices and the absence
of any changes outside B2's declared opening. Complete source-fill witnesses
are retained to prove consistency and explicitly marked as arbitrary,
not original readings. An optional `--pdf` checks the complete scan hash.

B3 already existed as an unreviewed OCR-derived candidate. The present
contribution is source certification, the newly readable opening instruction,
the limited middle-part proposal and exact costs. The bounded prior-body
check found no explicit p228 B example; no universal priority claim is made.
