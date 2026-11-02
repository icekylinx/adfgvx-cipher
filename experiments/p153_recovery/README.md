# Page 153: substantial partial recovery

**A shared 18-column transposition and a coherent partial reading have been
recovered for the two previously unresolved CHI fragments on printed page 153.**
The result leaves numeral identities, the trailing text, three erased letters,
and two printed-coordinate anomalies unresolved. It is not a complete solution.

The source heading dates these fragments to **November 8, 1918**, with `FKR v
CGH`, 11.55 p.m. and transmission 2250. The printed labels are `5 TL` and
`6 TL`, so this is multipart traffic with at least six parts; the header does
not give an explicit total. The surviving fragments are parts 5 and 6, with
132 and 108 coordinates. Part 6 contains 15 explicitly
missing coordinates at zero-based positions 5 through 19. The source
transcription is preserved unchanged in [the certificate](../../data/certificates/p153.json).

## What is recovered

The transposition ranks, indexed by physical column, are:

```text
16 7 13 4 15 8 17 3 1 12 14 2 5 9 10 18 11 6
```

The conservative substitution square fixes **19 letters**. Question marks are
unassigned cells, not guessed digits:

| Row / column | A | D | F | G | V | X |
| --- | --- | --- | --- | --- | --- | --- |
| A | ? | T | ? | U | G | I |
| D | ? | ? | ? | ? | ? | ? |
| F | ? | W | O | ? | C | M |
| G | B | ? | ? | S | Z | ? |
| V | ? | N | D | H | ? | V |
| X | E | A | ? | ? | L | R |

Interpreting cell `AF` as the usual `X` separator gives an optional twentieth
cell. The certificate keeps this interpretation separate from the 19-letter
core. Reversing every adjacent column pair and transposing the square gives an
equivalent representation of the same cipher.

The first fragment has 60 resolved ordinary-letter positions and six
numeric-looking positions. Its readable pattern is:

```text
ANORDNUNGEN VOM <alpha>TEN <beta><beta>TEN NR <gamma><delta><gamma>
BEZIEHEN LASSEN SOWEIT NOCH NICHT GESCHEHEN
```

The opening belongs to a longer order whose preceding four parts are missing.
The final phrase means approximately “have [it/them] taken up or occupied,
insofar as this has not yet been done”; the missing context supplies its object.

The four labels represent **four distinct square cells**. Reading the repeated
month cell as `11` is a contextual hypothesis. If adopted, the serial-number
cell `<gamma>` cannot also be `1`. The optimizer's raw rendering `NR121` is
therefore not a recovered literal number. The date and serial are deliberately
left unassigned.

## Second fragment: separate source reading and reconstruction

The first 42 characters strongly suggest:

```text
MUNITIONSBESTAND DER NACHHUTARTILLERIE MELDEN
```

This means “Report the ammunition inventory of the rearguard artillery.” It
requires two different kinds of qualification:

- Twelve letters lie at source erasures. Each proposed letter agrees with its
  surviving coordinate and the 19-letter square. Their positions and inferred
  coordinate values are enumerated in the certificate.
- Two known printed coordinates disagree. The `G` in the raw `ARTI?G?RIE` and
  the unassigned cell in `MEL?{AA}?` arise from source positions **3 and 4**, the
  final two `A` characters of the initial group `AXVAA`. Replacing those two
  coordinates with `X` gives `ARTI?L?RIE` and `MEL?E?`.

The primary scan prints **AA unambiguously**. These replacements are explicit
emendation hypotheses, not transcription corrections. Their position directly
before the 15-coordinate erasure burst is suggestive, but it does not establish
the historical cause. The untouched and emended branches remain separate.

The proposed 42-letter body constrains 72 surviving coordinates. Seventy match
the unchanged source and two disagree exactly as listed above. It also fills
twelve erased coordinates. Three erased letters and the twelve trailing
characters remain unresolved; no signature, unit, date or number is invented for
them.

## How the candidate was found

The search visited all **18,564** possible joint length-class segmentations at
width 18. Pairing and square searches remained bounded heuristics. The eventual
segmentation had zero-based rank 5 (sixth in the list). A second pass retained
twenty distinct pairing candidates from each of the ten leading segmentations.
The successful candidate was pairing rank 3 within segmentation rank 5,
flattened index 103.

An initial unknown-square fit and fixed-pair refinement still produced an
unreadable string. Allowing individual component columns to move within their
shared height class then recovered the coherent text at restart 49. That fit
used 100 restarts of 100,000 proposals and seed **322283886**. The full lineage,
all stage budgets, model hash, engine hash, input hash and archived-engine
qualification are recorded in `lineage.json`.

The models were trained on independent German books. No challenged message,
synthetic control plaintext or candidate text was used to train them. Military
domain weighting had been introduced earlier in response to control failures.
The discovery preceded the proposed `AA` to `XX` emendation.

Two later exact-domain refinements preserve every surviving half-coordinate.
Their outputs are retained in `exact_refinements.json`. They do not resolve the
numeric ambiguity: the unrestricted objective can even damage clear wording
while trying to interpret numeric-looking cells as ordinary letters. The
original warm candidate and conservative 19-letter mask remain the primary
recovery record.

## Verification and replay

```sh
python3 experiments/p153_recovery/verify_certificate.py
```

The verifier independently reconstructs the transposition, checks every source
coordinate mapping, checks the complete first-fragment round trip, preserves
all surviving half-coordinates in the second fragment, and verifies the exact
twelve-erasure/two-emendation accounting. It does not prove historical
authenticity from arithmetic alone.

`warm_replay.in` reproduces the decisive component-column stage. It contains the
preceding blind fit's ranks and square as a warm start, not the recovered key or
control truth. From the portable research-suite directory, after rebuilding
the recorded models:

```sh
bin/joint_rectangle_warm < PATH_TO_THIS_DIRECTORY/warm_replay.in > work/p153_warm_replay.jsonl
```

## Sources and attribution

The ciphertext source is the inspected public scan of *General Solution of the
ADFGVX Cipher System*, printed page 153. The parent repository includes the
source crop, edition notes and independent source audit.

Norbert explicitly suggested attacking the `VFVAX` and `AXVAA` CHI fragments
jointly and separately on September 17, 2017, in
[comment 56](https://scienceblogs.de/klausis-krypto-kolumne/2017/02/23/the-top-50-unsolved-encrypted-messages-46-unsolved-adfgvx-cryptograms-from-world-war-1/?all=1#comment-918886).
That suggestion supplied neither a key nor a plaintext. The present work
credits it rather than claiming the joint-analysis idea as new.

Column-pair methods, coincidence statistics and heuristic transposition search
have modern precedent in Lasry, Niebel, Kopal and Wacker,
[*Deciphering ADFGVX messages from the Eastern Front of World War I*](https://doi.org/10.1080/01611194.2016.1169461).
This implementation and its new partial recovery are by **icekylinx and GPT-6 Astra Pro**. A targeted review of the archived discussions, current public
solver material and primary-source text found no previous matching reading;
that bounded search is not a proof of worldwide priority.

## Exact conditional validation

The [post-discovery exhaustive check](../p153_crib/README.md) holds only the sixty ordinary-letter positions in part 5 fixed, leaving all six date/number positions unassigned. At width 18 it finds exactly two equivalent partial-key representations. Both require the same two part-6 coordinate emendations for the proposed forty-two-letter body. This is validation under an explicit crib, not another blind recovery.
