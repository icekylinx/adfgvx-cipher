# Reading the edition

[By page](../cases/pages/README.md) · [By subject](../topics/README.md) · [Historical studies](historical-studies/README.md) · [Methods](methods.md)

Each physical source has one catalogue entry. A source edition may assemble
several transmissions or successive parts while preserving their separate
identifiers. Readers reach the complete editions through two routes:

| Route | Purpose |
| --- | --- |
| [Printed pages](../cases/pages/README.md) | The home page offers eight ranges. Each opens a page-number table leading to the complete edition of a printed page. |
| [Subject exploration](../topics/README.md) | Six guides contain 50 curated summaries, each linking its sources directly to the complete numbered pages. |

Historical studies develop arguments across those sources. Their links also
lead to the full page editions. There is no intermediate standalone case view.

<a id="source-editions"></a>

## Page format

Each printed-page edition begins with its source table. A source link jumps
to the detailed reading and evidence on that page. The complete edition
presents readable German, English interpretation, reconstruction arguments
and source evidence. Shared editions identify companion receptions on other
pages so that the evidence for a cross-copy argument remains intelligible.

Raw decoded streams and literal transcriptions are expandable within the
full edition. The local passage states assumptions affecting its reading;
attribution and source comparisons stay with the text. The canonical archive,
`data/source_editions.json`, preserves 307 complete edition texts under their
original case-path identifiers. Those identifiers support research dependencies;
public source links use numbered pages and stable section anchors.

## Editorial style

| Element | Form |
| --- | --- |
| Printed page | `p153`; a range is `pp152–153`. |
| Source section | `p153 A3`. Original challenge identifiers such as `p153a` remain unchanged. |
| PDF pagination | `PDF page 155`, distinguished from the printed page. |
| Date | `7 November 1918`; `7–8 November` for a continuous interval, `7 and 9 November` for separate dates. |
| Time | The 24-hour form `15:00`; retain a source's literal time string in its transcription. |
| Counts | `80,000 men`, with commas in explanatory prose and numerical report tables; exact decoded digits remain literal. |
| Headings | Sentence case, with proper names and catalogue states such as `OPEN` preserved. |
| Emphasis | Bold reading labels; italics for vessel names and publication titles; code formatting for exact decoded strings and machine identifiers. |
| Navigation | **Page ranges**, **By subject**, **Historical research** and **Reading conventions** identify the same destinations throughout the reading guides. |

Use an en dash for page, date and position ranges. Keep qualifiers beside
the reading they govern. A translation, explanatory meaning and conditional
interpretation retain distinct labels. Historical quotations, source titles,
key identifiers and literal evidence preserve their recorded wording.

The page renderer applies these typographical conventions to editorial prose
after assembling the source sections. It preserves quoted text, code, link
destinations and existing section anchors; the archived edition texts remain
the inputs to the original research checks.

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
| --- | --- |
| **READING** | A documented substantive body reading is available. This label does not claim that every character, reference or historical identification is settled. |
| **PARTIAL** | Readable portions are established, with unresolved spans or fields. |
| **CONDITIONAL** | The principal proposed reading depends on a stated source frame, key interpretation or reconstruction assumption. It may also be incomplete. |
| **OPEN** | No accepted body reading. Source transcription and tested hypotheses are available. |

These are navigation labels. The full edition and certificate carry the exact result.
Adding an OPEN source completes the catalogue; it does not add a decipherment.
For physical-source identity, see the [source register](catalogue-source-identity.md).

## Text and evidence

| Label | What the reader is seeing |
| --- | --- |
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
A round-trip checks compatibility with a key and source model; the source and
historical argument establish why that particular reconstruction is credible.

## Unresolved text and editorial marks

| Mark | Interpretation |
| --- | --- |
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
fields in [p153](../cases/pages/153.md#source-p153a) illustrate why replacing every unknown by
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

<a id="maintain-the-edition"></a>

## Verification

The source-archive check verifies the complete texts and their SHA-256 hashes.
The page-edition check covers catalogue sources, page assignments, section
anchors, local links and evidence drawers. Navigation checks the two reading
routes and the curated topic selections. Live readable mappings compare
ordered German labels with decoded streams; research packages separately
replay cipher operations, repairs and source-image provenance.

Edit the canonical archive text and hash, or the topic summary and its
`source_ids`, then follow the
[regeneration sequence](repository-map.md#maintain-the-edition). Check the
public edition with:

```sh
python -m adfgvx.source_editions --check
python -m adfgvx.catalog --check
python -m adfgvx.navigation --check
python -m adfgvx.page_editions --check
```

Frozen research checks may still use the archived case paths as file inputs.
Materialize those paths for verification and clean them afterward:

```sh
python -m adfgvx.source_editions --materialize
python data/reviews/check_reading_presentation.py
python data/reviews/verify_live_readable_mappings.py
python -m adfgvx.verify
# Run affected source-specific checks from the verification workflow.
python -m adfgvx.source_editions --clean
```

Materialized files are temporary verification inputs. Persist intentional
changes in the canonical archive before cleanup; keep those temporary files
out of commits. Full plaintext, ciphertext, certificates and reconstruction
accounts remain in the archive and numbered page editions.

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.
