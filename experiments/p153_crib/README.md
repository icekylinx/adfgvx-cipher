# p153: exact validation conditional on the recovered first-part text

**At width 18, the sixty ordinary-letter positions recovered in part 5 admit
exactly two partial-key representations. They are equivalent by reversing each
adjacent column pair and transposing the substitution square.** Both require
the same two printed-coordinate changes to read the proposed part-6 body.

This calculation uses the discovered reading as a crib. It validates its
internal constraints; it is not an independent blind recovery or a proof that
no other reading, width, or corruption model exists.

## Inputs and exhaustive scope

`historical_input.txt` contains four lines: the 66-position first-part crib,
the unchanged 132-coordinate source, the 42-letter proposed second-part body,
and its unchanged 108-slot source including fifteen erasures. The date and
number positions in the first crib are all `?`; no digit is assumed.

```text
ANORDNUNGENVOM?TEN??TENNR???BEZIEHENLASSENSOWEITNOCHNICHTGESCHEHEN
MUNITIONSBESTANDDERNACHHUTARTILLERIEMELDEN
```

The first rectangle has six columns of length eight and twelve of length
seven. The program enumerates all C(18,6) = **18,564** ways to place those long
columns in transmission order. For every segmentation it considers all ordered
column pairs compatible with each plaintext column, enforcing one injective
36-cell square globally. A depth-first search covers every surviving assignment
of the eighteen distinct ciphertext columns. Unknown square cells are free.

The second crib does not prune that enumeration. After a complete first-crib
key is found, it is used to count disagreements with the second source. Thus
the two emendations are an output of the comparison, not an input constraint.

## Result

Only four segmentations survive the local pair constraints. Exhaustive global
search visits 28 nodes and returns two equivalent partial keys:

```text
16 7 13 4 15 8 17 3 1 12 14 2 5 9 10 18 11 6
 7 16 4 13 8 15 3 17 12 1 2 14 9 5 18 10 6 11
```

Both fix the same nineteen ordinary letters in equivalent square coordinates.
Both disagree with the proposed second-part body only at **source positions
3 and 4, A to X**. Seventy other observed coordinates constrained by that body
agree. The unchanged printed `AXVAA` remains the source record.

This establishes a narrow result: with the specified width, reset convention,
injective square and sixty-letter first crib, changing the transposition cannot
remove those two disagreements. It does not establish whether they arose in
transmission, reception, copying, printing, or the proposed reading.

## Reproduce

```sh
cc -O3 -std=c11 -Wall -Wextra -Werror -o /tmp/p153-enumerate enumerate.c
/tmp/p153-enumerate historical_input.txt
python3 verify_and_control.py --engine /tmp/p153-enumerate
```

The Python checker independently reencrypts every returned partial key, verifies
the equivalence, and runs two seeded synthetic cases with zero and two deliberate
coordinate errors. An impossible constant-letter crib supplies a negative
control. All three controls pass. The historical output, control inputs and
verification record are included; CPU timing is incidental and not compared
when reproducing the output.

Implementation and review: **icekylinx and GPT-6 Astra Pro**, 2 November 2026.
