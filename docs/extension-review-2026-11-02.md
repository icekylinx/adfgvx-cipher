# Extension review: source readings and calibrated recovery methods

**icekylinx and GPT-6 Astra Pro · 2 November 2026**

This extension adds substantial readable source material and several new,
reproducible recovery methods. **p73, p170 and p198 D remain wholly open.**
No high language score or successful source roundtrip has been promoted to
a historical plaintext without the required supporting evidence.

## Scope and attribution

The baseline is commit `ffc0c91e75b80e628524d665af9507f123fd664c`.
The two reader tables grow from 22 challenge entries and 87 other reviewed
physical records to **22 and 195**, respectively: **108 additional source
records**, with none removed. The [complete inventory](../experiments/session_review/inventory.json)
lists every addition, its actual status and credit, and all revisions to
older rows. It is independently regenerated from the preserved baseline.

These are physical source records, including multipart segments, repeated
intercepts, prior readings and conditional editions. They are not 108 new
independent decipherments. The p153 partial decipherment already existed at
the baseline and is not a new recovery in this extension. The published key
catalogue and challenge-message data are byte-identical to that baseline;
new historical interpretations live in separate, explicitly conditional layers.

The [Lasry attribution audit](../experiments/p170_new_methods/lasry_attribution_audit.md)
distinguishes 23 checked references to prior bodies, headers or keys. It led
to corrections for the Feigenhaus, Seifert, supply and repeated Warsaw
material. Kiel, internment and naval-armistice bodies likewise retain their
earlier credits. The p187 C body keeps Ayush Agarwal's prior attribution;
its new contribution here is an exact source/edit audit. Later source editions
also acknowledge earlier automatic OCR-derived candidate texts. Failure to
find a prior body discussion is not treated as a universal priority claim.

## Readable source gains

### Ship sales, transport and evacuation

The [Corcovado sale terms](../cases/other/corcovado_sale_terms.md) and
[proposed Turkish purchases](../cases/other/turkish_tonnage.md) cover nine
parts. They describe price and payment terms, seizure risk, interest, German
resale rights, evacuation use, Turkish manning, and an instruction to sell
additional tonnage only in an extreme emergency with prior authority and
immediate payment. Dates, part numbers, ship-name variants and garbled
references remain visible in the source layer.

The six Corcovado parts fix 1,051/1,060 raw positions and give 1,056 candidate
positions after 17 coordinate substitutions and five erasure fills. The three
additional tonnage parts fix 490/500 raw positions and give 496 after nine
substitutions, one invalid-symbol fill and one missing-coordinate fill.
The different kinds of change are never collapsed into a single recovery count.

A later Marineamt telegram spells its office number as `SECHS`. Under the
stated same-office/correct-copy assumptions, this supports a conditional
Nov10 square value and corroborates an earlier Nov7 interpretation. The
Bundesarchiv's institutional catalogue independently describes the maritime
transport office A VI S. The underlying archival business plan was not
inspected. Propagating the condition retains an inconvenient raw-word garble
as well as useful reference information; it is not selected only where helpful.

### Civilians and the diplomatic appeal

The four [Constantinople civilian-enquiry parts](../cases/other/constantinople_civilians.md)
ask the Swedish legation to verify reported departures, request information
on troop transports, and describe an appeal to allow German civilians to
remain in Turkey. Contemporary official U.S. diplomatic texts independently
corroborate the appeal and referral to the Supreme War Council. They do not
establish the reported departure, the headcount, the source geometry, or a
separate personal act by Wilson.

The selected raw models fix 624/628 positions. The headcount remains **0YY**,
whose three complete original coordinate pairs were excluded from the first
part's geometry score. A source-local final-part loss model competes with
six cheaper broader body fits; all seven survive in the certificate. The
edition provides readable wording with 17 substitutions, two printed-erasure
fills, two added-coordinate fills and one explicitly identified valid-coordinate
deletion in B2. These changes are separately priced; the edition does not uniquely
establish where the original loss occurred.

### Personnel, cash and military supplies

The [October Caucasus](../cases/other/october_caucasus.md),
[staffing](../cases/other/october_staffing.md) and
[routing/weather](../cases/other/october_requests.md) editions cover 22 parts.
They supply readable correspondence on Kress personnel and funding,
Westernhagen's return, Tiflis equipment, Violetta cargo, the 4th Bavarian
Cavalry Brigade and Grundherr's replacement assignment. A difficult technical
expression and the heavily damaged procurement material remain unasserted
or provisional instead of receiving costly silent normalizations.

The [Breslau personnel order](../cases/other/breslau_staff_transfer.md)
retains the raw rank/name/corps labels while recovering ordinary wording.
A visually inspected decree in the *Waldenburger Wochenblatt*, 18 July 1917,
names the VI Army Corps deputy general command at Breslau. It is sixteen
months earlier than the intercept. It supports older institutional context,
not a confirmed officer identity or a silent numeral assignment. The separate
[boots request](../cases/other/p191_A.md) has a useful one-group displacement:
196/200 positions follow after four substitutions and twelve erasure fills.
The older decree supports only an optional extra D→G source repair to read 6;
the received unknown cell itself cannot be assigned 6 under the unchanged key.

Six [lei-note redemption](../cases/other/lei_note_exchange.md) and
[crown-cash](../cases/other/crown_cash_requests.md) parts describe stamping,
bank arrangements, an Arad advance request, partial remittances and severe
banknote shortage. Complete amount and reference pairs are preserved as raw
labels. No exchange rate, round amount or date is assigned by plausibility.
Complementary office/place readings support two within-message repairs;
they are not called independent retransmissions, and the separate cash report
is not assumed to answer the preceding request.

### Repeated messages and source constraints

The [November 14 retransmissions](../cases/other/nov14_radio_retransmissions.md)
restore 85 missing prefix coordinates and 85 raw plaintext positions using
a complete witness. Differently keyed request pairs support 87/88 and 94/94
candidate positions. The [proposed three-part Tiflis grouping](../cases/other/tiflis_appointment.md)
associates a forwarding instruction with Waclaw v. Ostrowski's appointment.
Text, part counts and key support the association, but the source headings do
not establish it and the November 14/15 heading conflict remains unresolved.
Masks excluding the personal names help locate a displaced group and a missing group.
An independently attested Tydelski identity supplies a separate conditional Y
constraint, with an additional assumption needed to transfer it to another key.

Other additions include courier and Helsinki traffic, Siedlce withdrawal,
Warsaw service markers, headquarters movements and late cipher instructions.
Two BSL–UKS key-agreement parts preserve all 320 received coordinates. Their
existence does not identify an unresolved challenge key or prove compliance
with every later key-reuse instruction.

## New methods and what their controls establish

The [word/loss campaign](../experiments/p198_word_search/README.md) adds a
trie-based word-segmentation objective, capped word-pair association bonuses,
and a joint source-preserving search over missing positions, fills and free
square cells. All **49 declared jobs completed**: 18 control runs and 31
historical settings, with **2,055,765,000 completed mutation proposals** and
zero pending cases. Every result was collected after its process exited
cleanly; final counters remain separate from best-candidate discovery counters.

The 18 controls use nine distinct bodies, with adaptive reuse stated. Twelve
runs recover the exact text; five wrong incumbents score above truth, while
one fails to find a better true solution. A fresh numerical control gets the
wording right but changes company 3 to 2, day 17 to 18 and time 0800 to 0300. The
word and original quadgram objectives share the same ten public books, so
their agreement is not independent language evidence.

The [frozen radio model](../experiments/radio_domain_model/README.md) excludes
whole test-message families. Its improvement is specific to one regime:
for six 53-character controls with the **full true square supplied** and
hidden ranks, radio scoring recovers 5/6 versus 2/6 for book scoring. In the
partial-square, five-loss regime, both recover only 1/6 exactly. Four further
source families and four fresh deliberately numerical texts expose remaining
word, numeral and geometry errors. None of the four tested objectives recovers
a complete literal numerical text on the latter four-body sample.

The [exact digit-symmetry proof](../experiments/radio_domain_model/digit_symmetry/README.md)
explains a limitation that more search cannot remove. With a candidate's
letters, ranks, loss positions and fills fixed, permuting its `k` unanchored
digits preserves ciphertext and class score. If `r` such digits occur in its
text, that family contains exactly `k!` squares and `k!/(k-r)!` literal texts.
One perfect-class candidate has 360 such texts, including truth. Two others
have 3,628,800 each, yet exclude truth because their repeated digits have the
wrong equality pattern. Perfect class agreement is weaker than correct
numerical structure, which is itself weaker than correct digit values.

The [p73 package](../experiments/p73_new_methods/README.md) completes 255 new
runs across square-component reuse, spacing models, hidden-square word
search and a gated radio/rank follow-up. It independently checks 47,819
reported optimal substitution assignments for corpus retrieval. The best
historical overlap is 31/62, against 32/63 in a finite frequency-preserving
shuffle comparison. That is not a significance test or an exclusion of all
other keys, source collections or damage models.

The [p170 package](../experiments/p170_new_methods/README.md) completes 102
optimization jobs, including 54 book historical settings and 28 radio
historical settings. The older engine's 7 billion configured loop slots are
kept distinct from 3,902,267,094 instrumented fitness calls across the matched
controls and radio historical campaign. A
separate finite group-move screen tests 401 distinct frames under 24 fixed
key/rank pairs and two models. Its failed control shows that wildcard
marginalization can favor a less informative wrong frame. None yields an
accepted p170 plaintext.

The [conditional p198 category frontier](../experiments/contextual_key_constraints/README.md)
is exact under its stated Nov13b ranks and five-loss model. The Y condition
reduces 40,320 square completions to 5,040; at least four digits are then
required, or thirteen if no Q/Y occurs. This is a conditional structural
bound, not evidence identifying the actual key, loss pattern or plaintext.

## Verification and reproducibility

The repository retains source crops, complete coordinate maps, raw and
candidate readings, injective square witnesses, model provenance, actual
final counters and failed controls. Default checks are designed to run from
the supplied files without original working-directory paths. Optional PDF
checks compare the primary file hash and crop pixels. Optional model checks
recompute the full objective and finite rankings.

The word score is also checked by an independent backward memoized substring
implementation. All six radio/class tables are independently reconstructed;
the published lexicon builder reproduces its complete byte-identical output.
The digit audit exhausts 1,684 small-orbit permutations and checks 38 generators,
then checks every one of 3,359,232 entries across the two class tables. Its
two 10! counts are mathematical counts, not purported full enumerations.

A [portable p170 log audit](../experiments/p170_new_methods/audit_original_logs.py)
matches all 102 original result sidecars and independently re-encrypts 761
logged incumbents. Ninety raw logs had earlier hash pins; twelve control-log
hashes were first recorded in the final audit. Instrumented counts survive
in the original parsed sidecars, while the separate stderr bytes were not
retained. The [p73 source-snapshot audit](../experiments/p73_new_methods/results/retrieval_provenance_audit.json)
also records two unavailable earlier full-file snapshots: all 25 selected
naval text-field references match the current edition and remain frozen for
replay, but the old files' complete metadata bytes cannot be rechecked.

Local execution of the existing workflow commands passed 17 check groups;
new source supplements and method archives have additional recorded checks.
The archived environment and individual command outputs accompany the
delivery. Local results are distinguished from a remote GitHub Actions run.
The source-extension inventory prevents additions, prior readings and old
p153 progress from being counted as new independent solutions.

## Next experiments selected by the observed limitations

These are proposed next experiments, not additional completed searches.

| Priority | Concrete experiment | Evidence and calibration needed before a historical claim |
|---|---|---|
| 1 · p73 | Inspect the existing `RZ*11061` and `RZ*11064` [archival leads](../experiments/p73_primary_followup/ARCHIVE_ACCESS.md) for an independently sourced Kress-message body, retaining both date hypotheses. Fit any supported parallel jointly for column order and an injective substitution square, preserving all 176 received coordinates and both erasures. | Require identifying time, route, reference or reply evidence beyond the recipient alone. Fix normalization rules before testing, then validate on a fresh attested parallel and matched nonmatching messages. Preserve every compatible layout/key witness; reception proximity to p155 does not identify the key. |
| 2 · p198 | Fit a newly identified partial retransmission or reference-bearing parallel jointly with the target. Use observed overlap to constrain losses and independently read numerical fields to constrain digit labels. Retain Nov13b/five-loss as one conditional branch. | Establish message association independently of its language score. Test fresh numerical controls with hidden geometry and partial squares, including wrong repeated-digit patterns. Require correct literal truth membership and equality structure, and report all remaining digit-permutation families. Perfect digit-class agreement alone is insufficient. |
| 3 · p170 | Calibrate the currently uncovered combination of a 106-coordinate contiguous fragment and unknown column order. Earlier truncation trials fixed ranks; the newer rank trials assumed a complete 106-coordinate frame. | An original length indicator, continuation or identified parallel must justify historical full-length/window bounds. Use fresh prefix, middle and suffix controls, including width 22 and low-information cases. Require recovery where identifiable and explicit ambiguity otherwise; increased wildcard uncertainty must not itself improve a frame's ranking. |

An independent same-key long message, a repeated or re-encrypted passage,
an original source fixing damage geometry, or an authenticated reference
value can reduce these specific ambiguities. The controls show why a larger
language-search budget alone cannot supply those constraints.
