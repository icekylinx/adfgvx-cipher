# Manual German reading-layer review

Prepared by icekylinx and GPT-6 Astra Pro.

## Implemented scope

Twelve exclusively assigned case pages now use the common reading-layer legend and local explanations of supplied text. Existing headings and anchors remain intact. All **42 existing fenced blocks**, **92 existing headings**, and **349 pre-existing inline-code tokens** were checked against the before snapshots and preserved. No source input, key, experiment certificate or prior author's quoted stream was edited by this pass.

The [manual audit](../data/reviews/reading_conventions_manual_audit.json) gives each path, before/after digest and concrete changes. The [before snapshot](../data/reviews/reading_conventions_manual_before.json) stores the twelve original Markdown texts as JSON. These are review artifacts, not replacement editions of the source data.

## The changes that matter to interpretation

| Case | Ambiguity addressed | Result |
|---|---|---|
| p205 B | Readable closing `1…` concealed a known one-position uncertainty. `[s]` could resemble an abbreviation expansion. | The closing displays literal `1?`; the note identifies `[s]` as the priced source-coordinate repair. |
| p164 B | `0{5/6}00` mixed raw position notation with human time notation. | Readable `[05:00 oder 06:00]` is explicitly tied to raw `0?00`, with the historical 05:00 selection kept separate. |
| October Caucasus | The repaired 4.10 date, conditional 10,000 grenades and conditional 20-kW rating looked unqualified in the leading quotation. Literal garbled fields used the same brackets as supplied names. | Conditional whole values are bracketed; unchanged uninterpreted fields use code formatting. Tellner remains an explicit name reconstruction; the added k in Rückkehr is marked. Missing continuation and unread remainder have distinct notices. |
| October staffing | `[F]ischer` and `Comm[i]ssar` used the same notation as expansions elsewhere. | Both are identified as source-erasure fills; the name proposal and ordinary-word completion remain separately qualified. `röm.I` is explained as display of literal `ROEM1`. |
| November 14 retransmissions | `[Sewastopol]`, `Dring[end]`, `[Warschau]`, `[des]` and a slash between pilot terms represented five different operations. | Notes distinguish a priced repair, abbreviation expansion, fuller-witness wording, supplied grammar and differing witness terms. `FR?E` retains one unresolved position. |
| Glatz | `[wohl: erbeten]` might be mistaken for the exact repaired plaintext. | The gloss is explicitly a prose normalization; `ERBETETEN` remains in the fixed-length output. |
| November 9 reports | Bracketed letters included both prose-only insertions and a coordinate fill; repeated 5/6 values could look independently selectable. | A local category table distinguishes abbreviation, grammar, prose normalization, source-erasure fill and linked cell alternatives. |
| p153a/b | Linked `<alpha>`/`<gamma>` and footer variables do not behave like independent `?` characters. The readable instruction and unrecognized footer were visually mixed. | The variables stay intact with explicit field structure; p153b now gives the conditional German instruction separately while retaining the entire symbolic template and coupling restrictions. |
| p176b | Bracketed 217/219/6 units could be mistaken for new raw cipher recovery. | The leading caption retains the earlier credited historical overlay and explains that only the raw unassigned portions are being selected. |
| p218 | `[12]` was both a priced damaged reference and an independently supported treaty identification. | Readable `[XII]` explicitly renders the edited `ROEM12`; no baseline numeral assignment is implied. |
| Tiflis appointment | Its leading “Readable meaning” was English and used the historically selected courier name. | A new German base reading preserves `?1?` and `T?DE?SKI`; the existing English translation is labeled as using the separate historical-name interpretation. |

## New Tiflis readable mapping

The new German paragraph was checked directly against these three preserved certificate fields, in this order:

1. `p199_B1` ordinary-word-repair template.
2. `p192_2` ordinary-word template, retaining `ASERBEJNZAN`.
3. `p192_3` ordinary-word template, retaining `T?DE?SKI`.

After word spacing, case, punctuation, the justified separator-X display omissions and the explicitly described rendering of `DOPPELPUNKT` as a colon, **all 330 nonseparator labels agree exactly**. No historical name completion or new reference value was used. The [Tiflis readable mapping](../data/reviews/tiflis_readable_mapping.json) preserves this comparison and the source-certificate hash. The missing grammatical S in `DESMINISTERIUM` and the transmitted country spelling remain visible.

## Rules for later manual editions

- Name the basis of a readable passage: raw output, edited output, or a stated conditional overlay. A fragment or no accepted reading is a valid result.
- Keep brackets as familiar editorial notation, and explain their category near the passage. A bracket's typography alone cannot distinguish a source fill from a prose-only expansion or a historical identification.
- Preserve the number of unknown positions when displaying an exact token. Use a descriptive omitted/unread/missing-part notice for a larger span; do not use an ellipsis to hide known digits or an exact one-slot uncertainty.
- Retain linked unresolved variables and global square constraints. Repeating an unknown cell does not create independent per-occurrence choices.
- Do not normalize all X labels, J/Q/Y labels or AE/OE/UE sequences with a global replacement. Word segmentation, separator interpretation, proper names and ordinary German orthography require the local source context.
- A spelled-out punctuation term such as `DOPPELPUNKT` may be rendered as punctuation only in the readable layer, with the operation stated. A transmitted `FRAGEZEICHEN` must not silently become the editor's own uncertainty marker.
- Preserve repeated names and malformed received words unless a separate prose normalization is marked. No apparent grammatical repair is allowed to masquerade as a new ciphertext character.
- Earlier attributed readings and exact raw/edited strings stay quoted as originally recorded. New explanatory captions do not transfer their credit to the present review.

The shared [reading conventions](reading-conventions.md) implement the site-wide vocabulary. This review supplies the manual cases that a heading or punctuation replacement cannot safely resolve.

## Read-only verification

From the repository root:

```bash
python data/reviews/verify_manual_readings.py
```

The standard-library checker recomputes the preserved blocks, headings and inline-code sequence from the before snapshots and current case pages. It also reconstructs the Tiflis readable mapping from the frozen source certificate. It writes no files. Later prose additions may change a page's whole-file hash; the recorded manual-pass digest remains a snapshot, while the protected original strings must still survive in order.
