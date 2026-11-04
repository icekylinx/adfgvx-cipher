# 3 November medical, radio and withdrawal source editions

Prepared by **icekylinx and GPT-6 Astra Pro**.

Five physical records contain **921 printed source slots**, of which 918 are
valid coordinates. Four native frames and one explicitly conditional
112-slot frame model **458 plaintext positions**: 455 raw fixed and 458 after
three observed-coordinate substitutions and three source-mask fills.
A separate frame operation remains: **five observed coordinates are excluded**
from the source 117-slot p117 C4 record. No source positions or key cells are
silently changed.

| Source | Literal slots | Analysis-frame slots | Raw fixed | Edited fixed | Substitutions | Mask fills | Observed exclusions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| p117 A | 320 | 320 | 157 | 160 | 1 | 3 | 0 |
| p117 B | 256 | 256 | 128 | 128 | 1 | 0 | 0 |
| p117 C3 | 160 | 160 | 80 | 80 | 0 | 0 | 0 |
| p117 C4 | 117 | 112 | 56 | 56 | 0 | 0 | 5 |
| p117 D | 68 | 68 | 34 | 34 | 1 | 0 | 0 |

## Read the messages

- [Medical-company inquiry](../../cases/pages/117.md#edition-cases-people-medical-company-inquiry): three source-mask fills and one word repair; receipt/date conflict and all unit/reference labels preserved.
- [Ringbahn listening notice](../../cases/pages/117.md#edition-cases-radio-nov3-ringbahn-notice): one word repair; NACHRCEF, YS, WDH and NURNOCHITOCHI remain literal.
- [Withdrawal and night reports](../../cases/pages/117.md#edition-cases-military-nov3-withdrawal-and-night-report): the actual 160-slot C3 source yields an unchanged 80-position body; C4 has a transparent conditional exclusion model; D reports a quiet night after one repair.

## Conditional C4 frame and completed arithmetic

The actual 117-slot source and printed 112 length are both preserved.
All 113 contiguous five-slot exclusions are priced. Starts 16–22 give the
same completed stream at zero observed-substitution cost. The displayed
whole-group start 20 is a presentation convention. Allowing arbitrary five
exclusions gives 14 zero-substitution layouts for that fixed candidate;
all 678 dynamic-program states and every minimizing layout are retained.

The dynamic program represents all choose(117,5) five-exclusion layouts;
it does not claim to visit them individually. Six separate brute-force
controls explicitly enumerate 66 small layouts and agree on both cost and
all minimizing position sets. The archived language screen reconstructs
230 candidates (117 one-coordinate and 113 five-coordinate exclusions).
Only transmitted-stage exclusions were screened. A minimum for the chosen
text or a high language score does not establish unique historical wording,
frame or error mechanism.

All digit/reference labels, the shortened NACHRCEF, the odd VIERTEN11 field
and missing earlier parts remain visible. The medical query's receipt line
says 5 November while its page and origin point to 3 November; this does not
extend the published key label. The existing Nov1–3 key retains its prior
Lasry/Niebel/Kopal/Wacker credit. Earlier OCR candidates are frozen in
[prior_candidates.json](prior_candidates.json); no first-decipherment claim
is made.

An [independent source and arithmetic audit](independent_source_audit.json)
reads every C3/C4 group separately and reproduces all contiguous exclusions
and all fourteen zero-substitution arbitrary layouts with another algorithm.
It identifies the old C3 OCR group `AAF?` versus source `AAFVV`: one omitted
coordinate and one OCR mask. Its 233 visited states are separate from the
main optimization verifier's 678 states.

## Reproduce

```sh
python experiments/nov3_medical_radio_withdrawal/verify.py --verify
python experiments/nov3_medical_radio_withdrawal/independent_source_audit.py --verify
python experiments/nov3_medical_radio_withdrawal/verify.py --verify --pdf /path/to/childs.pdf
python experiments/nov3_medical_radio_withdrawal/verify.py --verify --book-model /path/to/german_military37_quad_marginal.bin
```

Default verification uses the Python standard library for inverse/forward
transposition, domains, every edit and source origin, all exclusion prices,
exact dynamic programming and the independent small controls. Optional PDF
verification checks the full source hash and every crop pixel. Optional model
verification checks the binary hash and all 230 archived scores, allowing only
1e-12 absolute arithmetic tolerance across Python summation versions.

[Inputs](inputs.json), [certificates](certificates.json), and
[exploratory screen](exploratory_deletion_screen.json) preserve the separate
source, analysis and editorial layers.
