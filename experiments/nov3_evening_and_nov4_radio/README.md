# 3 November evening-report copies and 4 November radio notices

Prepared by **icekylinx and GPT-6 Astra Pro**.

Seven physical records on printed pp111–112 contain **1,258 literal source
slots**, of which 1,212 are valid coordinates. Six native frames and one
conditional 122-slot frame account for **635 plaintext positions**: **577 raw
fixed labels**, and **630** after the explicitly priced editorial operations.
The totals include **16 observed-coordinate substitutions**, **42 source-mask
fills** and **11 values filled into twelve unprinted-coordinate slots**.
Five plaintext positions remain unresolved. No published key is changed.

| Physical record | Literal slots | Analysis slots | Raw fixed | Edited fixed | Observed substitutions | Source fills | Unprinted fills |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| p111 A1 | 202 | 202 | 86 | 101 | 1 | 15 | 0 |
| p112 A1 | 202 | 202 | 99 | 101 | 1 | 2 | 0 |
| p112 A2 | 218 | 218 | 89 | 107 | 6 | 18 | 0 |
| p112 A3 | 108 | 108 | 47 | 53 | 1 | 6 | 0 |
| p112 B | 188 | 188 | 94 | 94 | 0 | 0 | 0 |
| p112 C | 110 | 122 | 49 | 60 | 1 | 0 | 11 |
| p112 D | 230 | 230 | 113 | 114 | 6 | 1 | 0 |

## Read the editions

- [Evening report and its first-part copy](../../cases/pages/111.md#edition-cases-military-nov3-evening-report): Save–Danube and Alpenkorps positions, damaged vehicle-traffic continuation, Bucharest flight notice and unresolved reference labels.
- [Telefunken personnel inquiry](../../cases/pages/112.md#edition-cases-radio-telefunken-staff-inquiry): all 94 positions read directly from the native 188-coordinate source, with no edits.
- [Conditional Constantza station closure](../../cases/pages/112.md#edition-cases-radio-constantza-station-shutdown): twelve unprinted coordinates, one observed repair and an unresolved `?400` field; all framing qualifications remain explicit.
- [Turkish armistice and straits notice](../../cases/pages/112.md#edition-cases-military-turkish-armistice-straits-notice): costed ordinary-word repairs; the source date-like label and opaque ending remain literal.

Every readable German passage has a [character-level mapping](readable_mapping.json)
to its edited stream. After removing X separators and normalizing only
spacing, case, punctuation, umlauts and sharp-s, every other label and every
unresolved-position question mark must match. The two grammatical question
marks in the zero-unknown Telefunken inquiry have separate explicit offsets. This makes accidental grammatical insertion,
reference loss or silent numeral interpretation detectable. It does not
establish the historical truth of an editorial template.

## Cross-copy support and coordinate conflicts

<a id="what-the-separate-first-part-witness-establishes"></a>

The p111 and p112 first parts share **183 observed coordinates**. They have
**seventeen one-sided erasures**, all supplied by the other copy, and **two
observed-coordinate conflicts** at zero-based positions 119 and 198.
Visible C/R in p112 remain literal invalid-coordinate glyphs; p111 supplies
G/F at those positions. The old p111 OCR also obscured a source-supported M.

All four common streams have the same minimum combined observed-edit cost
of two. The displayed candidate selects DONAU from p111 and UJVIDEK from
p112. A second UJVIDEK occurrence is unchanged within both bodies. The
certificate keeps every minimum stream, not just the favored one. The
three-part headers and receipt times are retained; a source copy is counted
as a physical witness, not another independently first-deciphered body.

A literal ten-coordinate substring screen against all 788 archived OCR
blocks located the p111 witness. Its [retained hits](literal_copy_retrieval.json)
are retrieval leads; manual source inspection supplies the authentication.

## A2 wording alternatives

The native A2 frame contains four five-dash groups. Earlier OCR omitted one
whole group, producing a misleading 213-slot frame. The first editorial
hypothesis used FLUGZEUG. Independent review identified **FAHRZEUG** as a
better-priced reading: **six rather than ten observed-coordinate substitutions**,
with the same eighteen source-mask fills and the same two reference unknowns.
Both full templates and all source changes remain in the [alternative ledger](editorial_alternatives.json).

The lower-cost reading still contains substantial editorial restoration;
its superiority within this comparison is not a uniqueness proof. The A
following TRETEN, source date/reference labels, and the repeated TLICH in
part A3 remain visible. No absent reporting verb or grammatical ending is
inserted to make the German smoother.

## Conditional C geometry and calibration

The source header clearly reads **122**, while its literal body has **110**
coordinates. `DVAX` and `AGFF` are visibly short groups. The declared bounded
family inserts one coordinate at each of their five possible local positions,
then inserts two five-coordinate blocks at any unordered pair of the 113
boundaries in the resulting temporary transmitted-coordinate frame. Thus
**25 × 6,441 = 161,025 parameter configurations** are actually evaluated.
They represent **155,400 distinct source-origin layouts**; 5,625 duplicate
configurations arise when inserted positions coalesce.

For the fixed candidate, the selected two-short-group layout plus a
10-coordinate prefix is the **only one-substitution optimum within that
bounded family**. Twelve arbitrary missing coordinates give **eight**
equally cheap optima. The exact dynamic program visits 1,443 states and
retains all eight minimizing layouts. Six separate tiny brute-force controls
check its minimum and complete set of minimizing insertions. This does not
claim that every one of the enormous arbitrary-layout space was visited.

The optional frozen-model language screen independently ranks all 161,025
historical parameter configurations. Four newly composed synthetic controls run the same full
screen, for **805,125 completed 122-slot parameter-configuration evaluations** in total.
Their best truth-compatible ranks are **1, 5, 1 and 27**. The two failures to
rank a truth-compatible layout first remain in the result. These controls
measure this bounded screen only; they do not assign a historical probability.
Fifty short-group-only 112-slot diagnostics under two known keys are also
retained without an accepted reading.

The clock-like `?400` position has domain `0578CX`; it is not silently replaced
by an assumed hour. The native odd spelling CONSTANTZA and abbreviated
NACHRCHEF remain. Neither source markers nor the language model independently
prove a missing prefix.

An [independent audit](independent_source_audit.json) uses separately
transcribed rows and a different column-oriented inverse, with no import
from the main verifier or shared cipher code. It reproduces all seven
source readings and costs, all four copy streams, both A2 candidates,
all 161,025 parameter configurations and their 155,400 distinct origin
layouts, and all eight broader-loss optima.

## Reproduce

```sh
python experiments/nov3_evening_and_nov4_radio/verify.py --verify
python experiments/nov3_evening_and_nov4_radio/independent_source_audit.py --verify
python experiments/nov3_evening_and_nov4_radio/verify.py --verify --pdf /path/to/childs.pdf
python experiments/nov3_evening_and_nov4_radio/screen_geometry.py --verify --book-model /path/to/german_military37_quad_marginal.bin
```

Default verification uses the standard library plus the repository's cipher
module. It recomputes an independent transposition map, exact domains,
forward witnesses, all edit ledgers, every bounded alignment price, the
broader loss optimum, all common-copy streams, both A2 alternatives and
all seven readable display mappings. Optional PDF checking binds all six
crops to the pinned source PDF and compares every RGB pixel. The optional
language screen needs NumPy and the separately pinned model, with 1e-12
absolute tolerance for floating-point arithmetic.

[Inputs](inputs.json), [certificates](certificates.json), [older OCR candidates](prior_candidates.json)
and the [complete language-screen report](language_screen.json) preserve the
separate evidence layers. Existing Nov1–3/Nov4–6 keys retain the attribution
to Lasry, Niebel, Kopal and Wacker. Earlier cached body readings are credited;
no universal first historical decipherment claim is made.
