# Reproducible searches

These bounded searches have produced **no accepted plaintext for the five open challenge entries**. A failed heuristic search does not exclude a key or corruption model. The source and edit certificates in `../data/` remain separate from language-ranked candidates.

| Experiment | Scope | Calibration and limit |
|---|---|---|
| [Fixed-rank and dictionary searches](fixed_search/README.md) | 144 fixed-rank cases, 1,352 dictionary-selected cases, 136 p198 refinements; completed counts are timestamped in the ledger | Exact input layers, model hashes, warm starts, and legacy limitations are retained. The dictionary run is updated as cases finish. |
| [Coordinate and geometry screen](fixed_search/README.md) | 20,666,880 evaluations across known squares, label permutations and readout conventions | A planted control ranks first; unchanged targets produce no accepted reading. |
| [p153 joint search](joint_search/README.md) | All 900,900 width-16 and 18,564 width-18 length-class segmentations; bounded pairing and language searches | Both width-16 controls preserve all 225 observed coordinates after exact-domain refinement. Width-18 ordering and pruning failures are retained. Enumeration of segmentations is not enumeration of keys. |
| [Known-key truncation](known_key/P170_TRUNCATION_NOTE.md) | 1,291,584 p170 placements over 21 keys | Two implementation controls; upstream training overlaps a control body. A long-suffix control fixes no plaintext letters, so truncation is not excluded. |
| [p215 conditional completions](p215_completion/README.md) | Exact top ten under each of three additive language objectives | All 237 known source coordinates preserved; the 6^21 source-compatible strings remain cryptographically unresolved. |
| [p185 D gap ranking](known_key/README.md) | All 194 positions of a five-coordinate gap | Both complete rankings reproduce; their preferred positions differ. The arithmetic certificate retains every geometry. |
| [p153 alternative geometry](geometry/README.md) | 48 concatenation cases and 48 continued-column-phase cases over 24 reported keys | Source coordinates preserved; direct known-square checks only. One square has no attested cells and supplies no reading. |

Search budgets describe completed computations, not confidence levels. Models, controls, seeds, source hashes, exact solver versions, and dependencies are documented beside each experiment. Large corpora, generated model binaries, executables, and candidate dumps are excluded. The independent model builder reproduces its recorded hashes; the earlier upstream model is pinned separately because it contains previously solved traffic.
