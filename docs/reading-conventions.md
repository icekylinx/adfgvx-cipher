# Reading conventions

The cases distinguish what the source prints, what a stated cipher model
returns, and what an editor proposes. The presentation rules below do not
change the literal transcriptions, keys, repair certificates or earlier
authors' quoted readings.

## The four reading layers

| Layer | What it contains | What must accompany it |
|---|---|---|
| **Raw output** | The exact decoded stream under the stated key and analysis frame, before the additional word repairs shown in that case. | The key and frame assumptions. A missing-group, truncation, reordered-group or other conditional frame must remain explicitly conditional beside the output. |
| **Edited output** | An exact proposed stream after the stated coordinate changes and fills. It preserves that candidate's positions, separators and unresolved characters. | A repair account that distinguishes observed-coordinate changes, fills of source masks, and changes to the frame. Exact re-encryption establishes compatibility with that proposal; it does not prove unique historical wording. |
| **Readable German** | A reading with word spacing, capitalization and punctuation, sometimes with explicitly marked expansions or proposed wording. | Its basis in the raw, edited or conditional layer. Display changes must not silently supply missing words, resolve names or turn square labels into historical numbers. |
| **Conditional interpretation** | A separately identified key-cell assignment, numeral interpretation, historical identification or common-message assumption. | The precise assumptions, supporting evidence and remaining alternatives. It does not replace the baseline raw or edited stream. |

A case may lead with the readable text and discuss its evidence afterward.
Some records support only a fragment or no accepted plaintext. The layers
need not all be present, and their absence is not an invitation to invent a
complete reading. **Meaning** labels an explanatory translation or summary;
an English quotation is not labelled Readable German.

Earlier authors' readings retain their author, date, original wording and
status. A quoted earlier raw reading or editorial completion is not renamed
as this review's Edited output. Later verification and source repair are
credited separately.

Supporting material keeps its own labels. **Source transcription** identifies
literal headers, ciphertext and cleartext source annotations; **Re-encryption
witness** identifies a constructed ciphertext used to check a proposal.
**Earlier attributed reading** and **Recomputed prior reading** retain the
earlier author and the recorded reconstruction. **Search diagnostic** marks
a candidate segment used to evaluate a search, without promoting it to an
accepted decipherment. These labels are not additional levels of historical
certainty.

## Symbols and unresolved positions

| Notation | Convention |
|---|---|
| `?` in a decoded stream | Exactly one unresolved plaintext position. Its cause may be a masked source coordinate, an inserted missing coordinate, an unassigned square cell, or a combination; the source/repair account distinguishes those causes. |
| `?` in an analysis ciphertext | Exactly one unresolved coordinate slot, not one plaintext character. The literal source transcription remains available separately. |
| A dash or invalid glyph in a literal source transcription | A printed source observation. Preserve the original glyph or the declared conservative transcription; do not replace it in the literal record merely to improve the reading. |
| `?` in ordinary readable prose | It can be editorial question punctuation. An unresolved field should be shown as a literal token, such as `???`, or explained locally so that it cannot be mistaken for a question mark ending a sentence. |
| `[word]` in readable text | Editorial material: a conjecture, repair, normalization or abbreviation expansion. A nearby note or repair account states which kind. Brackets do not by themselves establish whether a coordinate was changed or a key assumption was made. |
| `[…]` in readable text | A passage omitted from that presentation. State whether it is unread, outside the quoted excerpt, or missing from the source. It makes no positional-length claim. A complete decoded stream must retain its actual positions instead. |
| A domain such as `{5, 6}` | The allowed symbols at the stated position or cell under the stated model. Domain membership is not a selected reading. |
| A linked label such as `<gamma>` | A named unresolved value whose repeated occurrences are coupled. Keep its definition and cross-message links; replacing every occurrence by an independent `?` would hide evidence. |
| `X` in a decoded stream | A literal output label. It is often interpreted as a separator, but is never removed or converted globally. A readable version may replace a justified separator with spacing or punctuation. |
| Digits and labels such as `J`, `Q`, `Y` | Literal results under the displayed square. They are not automatically authenticated historical numerals, punctuation or rare letters. Any relabeling is a separately stated conditional interpretation. |

Square-cell uncertainty is global. Repeated occurrences of one unknown cell
share a value, and different cells must respect the square's injectivity.
Per-position domains do not permit choosing each occurrence independently.
For example, the named fields in [p153a](../cases/p153a.md) and
[p153b](../cases/p153b.md) retain cross-part equalities that a row of unrelated
question marks would conceal.

Abbreviations, repeated words, unusual spellings and transmitted terms such
as `FRAGEZEICHEN` remain visible. A readable version may explain them, but
does not silently modernize a name, identify an office, remove a repetition
or replace a word with punctuation. Spelling changes that affect the encoded
letters belong to an explicitly identified proposal, even when the intended
word appears obvious.

## Counts and repair prices

| Term | Counting unit |
|---|---|
| **Source slots** | Positions in the declared literal transcription, including printed dashes and noncoordinate or uncertain glyphs. The source's advertised length is a separate field. |
| **Valid coordinates** | Observed slots accepted as `A`, `D`, `F`, `G`, `V` or `X` in the stated transcription. This describes the alphabet and observation, not proof that transmission was error-free. |
| **Analysis-frame slots** | Positions in the coordinate stream used for the stated decryption, including unknown slots and any explicitly inserted or excluded positions. The frame can differ from the source count. |
| **Plaintext positions** | Positions after pairing the analysis coordinates. A complete even-length frame has half as many plaintext positions as coordinate slots. An odd remainder must be reported separately. |
| **Fixed output positions** | Positions with a singleton output domain under the stated model. This includes separator and numeral labels; it is not a count of independently authenticated words or historical digits. |
| **Observed-coordinate substitutions** | Changes from one accepted source coordinate to a different coordinate. One repaired plaintext letter can require one or two such changes. |
| **Source-mask fills** | Proposed coordinate values supplied at already present masked source slots. These are separate from changes to an observed coordinate. |
| **Inserted-slot fills** | Values supplied in hypothesized missing slots added to the frame. Report these separately from fills of printed dashes or ambiguous glyphs. |
| **Excluded or deleted source slots** | Literal source positions omitted from the analysis frame. State how many contain observed coordinates and how many are masks, and whether the source visibly marks a cancellation. |
| **Other frame operations** | Group movement, adjacent-coordinate swap, intermediate-stream deletion or other transformation. State its stage and exact positions; do not fold it into a generic count of “repairs.” |

An OCR omission is not an omission in the received source. Restoring an
actually printed row to a machine transcript does not count as adding
historical coordinates. Conversely, a visually cancelled duplicate remains
part of the literal transcription and its exclusion is recorded explicitly.
If a visible mark has alternative interpretations, its price can remain
conditional rather than being forced to zero.

Counts of raw and edited fixed positions always state their denominator.
Use **positions**, rather than **letters**, when the count includes digits,
separators or other square labels. Use **source slots** or **analysis-frame
slots** when masks are included; reserve **valid coordinates** for the
accepted alphabet symbols. Existing machine-certificate field names are
preserved even where older names abbreviate these distinctions.

Generated page and topic tables apply a finite [status display register](../data/catalog_status_display.json)
for older count-unit and spacing corrections. It records the exact prior
and displayed status for each affected source identifier. The generator
checks the prior wording and preserves every numerical token; the original
catalogue rows and frozen review snapshots stay unchanged. These corrections
do not alter reading qualifications, credits or evidence links.

The [p188 edition](../cases/military/armistice_provisions_requests.md)
illustrates a separately priced extra-mark exclusion, word substitutions
and source-mask fills. The [ruble companions](../cases/finance/ruble_rate_companions.md)
separate printed-mask fills from a fill in an added slot. Neither kind of
arithmetic establishes the historical error mechanism by itself.

## Positions, source headers and exact strings

Source, frame and plaintext indices are different coordinate systems.
State which is used. Newly presented machine indices are zero-based; printed
group or part numbers remain as printed. Earlier one-based references are
kept with their explicit convention instead of being silently renumbered.
When the frame changes, the certificate maps it back to the original source.

Dates, intercept times, lengths, call signs and part labels are transcribed
as evidence, including disagreements. A readable date or historical unit
identification must not overwrite a conflicting header or baseline field.
Missing earlier/later parts are marked as missing; a grammatical continuation
in another telegram is a possible relation until separately established.

Fenced literal source, raw-output and edited-output strings retain their
characters, order, punctuation and positional marks. A shortened display
must be explicitly called an excerpt and point to the full string. A
presentation-only edit does not rewrite these strings, their certificates,
or an earlier author's quotation. Captions and local notes clarify the layer
without changing existing section anchors.

English explanatory prose separates words from quantities: write “all 336
coordinates,” “source 62” and “November 5.” This rule does not split source
identifiers such as `p117`, key identifiers such as `Nov1–3`, transmitted
reference strings, URLs, code, or quoted earlier readings. Numerical values
remain unchanged by a spacing edit.

## Applying the conventions

Cases include a brief link to this guide. Their detailed topical structure
can vary, but the labels above keep the evidence levels recognizable.
Presentation audits record each touched file and compare the complete
contents of its fenced blocks before and after the edit. Any change to a
source or cryptographic claim requires its own review and certificate; it
is not treated as typography.

The [presentation coverage record](reading-conventions-coverage.md) links
the reviewed classification of every current substantive case and the
portable checks. The coverage check scans the current `cases/` tree, so a
new case or an unclassified display is reported rather than silently left
outside an old snapshot. Its labels are editorial classifications; source
and cipher verification remain separate.

Prepared by **icekylinx and GPT-6 Astra Pro**. The convention standardizes the
present edition's display and preserves the separately credited work of
earlier readers and key recoverers.
