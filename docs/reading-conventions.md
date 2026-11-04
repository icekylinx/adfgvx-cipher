# Reading the edition

[Catalogue](../cases/README.md) · [Historical studies](historical-studies/README.md) · [Methods](methods.md)

Each source has one catalogue entry. A case may bring together several
transmissions or successive parts of a message, but their source identifiers
remain separate. The edition has two principal parts:

| Part | Purpose |
|---|---|
| [Ciphertext pages](../cases/pages/README.md) | A dedicated Markdown edition for every printed page: its sources, German readings, English interpretations, explanations and evidence. Every page number in the home-page table opens that page directly. |
| [Historical research](historical-studies/README.md) | Studies organized around historical questions, supported by the source editions, a dated chronology and comparisons with contemporary records. |

## Page format

Each printed-page edition begins with its source table. **Reading** jumps to
the detailed source section; **Case** opens the short account of the message.
The complete page presents readable German, English interpretation,
reconstruction arguments and source evidence. A shared edition names the
companion receptions from other pages so that a cross-copy argument remains
intelligible.

Raw decoded streams and literal transcriptions are expandable within the
full edition. The local passage states any assumption that affects its
reading. Attribution and source comparisons stay with the text. Existing
case files preserve the full source body and earlier section citations,
with a short English account at the top.

## Historical studies

Organize a study around a historical question and the relationship between
its sources. Quote the relevant passage, explain what it contributes, and
link the complete numbered page. Keep orders, requests, reported actions
and externally documented events distinct. Give an event or origin date
separately from a reception date when the distinction affects the sequence.

Use references, repeated wording and multipart joins to establish connections
between messages. Contemporary maps, diaries, registers and documents may
corroborate a location, movement or textual variant; explain the specific
relationship. Thematic classification may connect sources from different
parts of the archive without changing their catalogue identities.

## Catalogue states

| State | Meaning |
|---|---|
| **READING** | A documented substantive body reading is available. This label does not claim that every character, reference or historical identification is settled. |
| **PARTIAL** | Readable portions are established, with unresolved spans or fields. |
| **CONDITIONAL** | The principal proposed reading depends on a stated source frame, key interpretation or reconstruction assumption. It may also be incomplete. |
| **OPEN** | No accepted body reading. Source transcription and tested hypotheses are available. |

These are navigation labels. The case and certificate carry the exact result.
Adding an OPEN source completes the catalogue; it does not add a decipherment.
For physical-source identity, see the [source register](catalogue-source-identity.md).

## Text and evidence

| Label | What the reader is seeing |
|---|---|
| **Readable German** | The reading with editorial spacing, case and punctuation. Its caption identifies an excerpt or conditional proposal when necessary. |
| **Meaning** / **English meaning** | A translation or explanatory summary. Abbreviation expansions and historical interpretation belong here when they are not literally decoded. |
| **Raw output** | The exact decoded labels under the stated key and frame, before the additional word repairs. A conditional frame remains identified locally. |
| **Edited output** | An exact proposed stream with a reproducible account of substitutions, fills and frame operations. |
| **Conditional interpretation** | A separately justified numeral, key-cell assignment, identification or common-message hypothesis. |
| **Source transcription** | Literal ciphertext, header or cleartext annotation from the source. |
| **Re-encryption witness** | A constructed ciphertext checking a proposal against its stated source model. |
| **Earlier attributed reading** / **Recomputed prior reading** | Earlier work, with its author and original evidence status retained. |
| **Search diagnostic** / **Geometry alternatives** | Search or model-comparison evidence; not an accepted reading by itself. |

Only show layers that add information. An unedited message needs one exact
stream, not identical “raw” and “edited” copies. When a literal display is
shortened, label it as an excerpt and link the complete source or certificate.
A roundtrip checks compatibility with a key and source model; the source and
historical argument establish why that particular reconstruction is credible.

## Unresolved text and editorial marks

| Mark | Interpretation |
|---|---|
| `?` in decoded text | One unresolved plaintext position. In a coordinate model, it instead denotes one unknown coordinate slot. |
| Printed dash or unusual glyph | A source observation, preserved in the literal transcript. Its treatment in the analysis is recorded separately. |
| `[word]` | Editorial material; the local note says whether it is a proposed repair, expansion or normalization. |
| `[…]` or an ellipsis | Omitted passage or continuation, with the reason stated. It does not specify the number of missing positions. |
| `{5, 6}` | An unresolved domain, not a choice of the more plausible digit. |
| `<alpha>`, `<beta>` | Named unknown square cells. Repeated occurrences share one value. |
| `X` | A literal output label, often a separator. Readable text may render an established separator as punctuation or spacing. |
| Digits, `J`, `Q`, `Y` | Literal labels until a separate argument supports their historical interpretation. |

Unknown square cells are globally coupled: one cell has one value, and two
cells cannot independently take the same symbol. The linked date and serial
fields in [p153](../cases/p153a.md) illustrate why replacing every unknown by
an unrelated question mark loses evidence.

Keep transmitted repetitions, abbreviations, unusual spellings and numerical
strings in the exact layer. Explain a name or office in prose; do not silently
substitute it into the decoded text. A question mark used as ordinary sentence
punctuation is distinct from a literal unresolved token such as `???`.

## Counts and repair accounts

**Source slots** count the literal transcription, including printed masks.
**Valid coordinates** count its accepted A/D/F/G/V/X symbols. The advertised
header length is a separate observation. **Analysis-frame slots** include any
hypothesized additions or exclusions. Pairing an even frame produces half as
many **plaintext positions**; report an odd remainder explicitly.

A fixed position is a singleton under the stated model, including separators
and numerical labels. It can still contain a transmission error. Give the
denominator, such as `60/66 positions`, rather than calling all fixed labels
“recovered letters”.

A repair account distinguishes:

- substitutions of observed coordinates;
- fills of printed masks or invalid source glyphs;
- fills of hypothesized absent slots;
- exclusions of received coordinates or masks;
- swaps, group movements or other frame operations, with their stage stated.

Restoring a row actually present in the source repairs an OCR transcription;
it does not create historically missing coordinates. A word whose two
coordinates are absent has no direct letter evidence and must be identified
as such. State whether positions refer to source, frame or plaintext; new
machine indices are zero-based.

## Attribution and historical claims

Credit key recovery, earlier readings, source reconstruction and historical
interpretation separately. We state our own results directly: a new recovered
key, a restored reception, an independently supported repair or a connected
historical edition. Earlier work is cited where it contributes to the result.

A claim of first documented recovery specifies the public sources checked and
the date of review. The absence of a matching published reading can support a
bounded priority claim; it does not establish that nobody ever read the
message. A historical statement also distinguishes an order from its
execution, a request from receipt, and a contemporary report from a verified
event. Those distinctions belong beside the affected passage, once.

## Verification

The [current structure check](../data/reviews/check_reading_presentation.py)
checks case titles, convention links, evidence labels and expandable blocks.
The page-edition check verifies coverage of every catalogue source, page
assignment, section anchors, local links and evidence drawers. Concise case
views preserve the complete source body when regenerated.
Live readable mappings compare ordered German labels with decoded streams;
source packages separately replay the cipher, repairs and image provenance.

After editing an edition or its English summary, follow the
[regeneration sequence](repository-map.md#maintain-the-edition), then run:

```sh
python -m adfgvx.case_views --check
python -m adfgvx.catalog --check
python -m adfgvx.navigation --check
python -m adfgvx.page_editions --check
python data/reviews/check_reading_presentation.py
python data/reviews/verify_live_readable_mappings.py
python -m adfgvx.verify
```

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.
