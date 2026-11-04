# Benzol-pump inquiry with an explicit missing-coordinate model

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Source review and edition: icekylinx and GPT-6 Astra Pro.**

The p189 D reading asks whether a benzol pump is available and requests a prompt answer. Its 102-coordinate analysis is conditional: the printed body contains 101 occupied positions, including one non-coordinate glyph, and the first row ends with a four-coordinate group. Every missing-slot assumption and textual repair is priced below.

## Source and context

[Childs source](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Reviewed query and neighboring reply](../../experiments/benzol_pump_query/sources/p189_reviewed.png) · [Inputs](../../experiments/benzol_pump_query/inputs.json) · [Position certificates and all 102 insertion prices](../../experiments/benzol_pump_query/certificates.json)

**Source transcription — header:** `D) CM v CZ (9.30 a.m., November 15th); RIZI-102`

The source says RIZI-102 but has **101 occupied slots**, with `XVGF` as the four-coordinate last group of the first row. The K-like final glyph of `DXXGK` occupies a separate source slot; it is masked, not discarded. All other observed coordinates stay in order.

The neighboring p189 E reverses the direction to `CZ v CM`, is timed 10.00 a.m. after D's 9.30 a.m., and begins with an answer about a pump. Its [existing edition](transport.md#independent-transport-context) supports the topic. It is not a parallel ciphertext and cannot supply D's missing coordinate or certify the exact closing surname.

## p189 D

<details>
<summary>Raw decoded text</summary>

**Raw output — native 101-position diagnostic, before any length change:**

```text
ISEEIDEBENNOLPUMPE?OR1XBESKHLE?NIGTEANTWORTXSSIF??
```

</details>

This odd-length diagnostic has one unpaired intermediate coordinate. The certificate retains its intermediate position, source index and literal coordinate; it is not silently removed from the source account.

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 102-coordinate frame with one masked insertion at source boundary 38; 47/51 fixed positions:**

```text
IS?EIDEBENZOLPUMPEDOR1XBESAHLE?NIGTEANTWORTXSSIF??T
```

**Edited output — the same conditional frame; six observed-coordinate substitutions, one source-glyph fill and one inserted-coordinate fill:**

```text
ISTEINEBENZOLPUMPEDORTXBESCHLEUNIGTEANTWORTXSEIFERT
```

</details>

**Readable German — labels from the edited output, with editorial word spacing and punctuation:**

> Ist eine Benzolpumpe dort. Beschleunigte Antwort. Seifert.

**Meaning:** The sender asks whether a benzol pump is available there and requests an expedited answer. The closing is the explicitly reconstructed surname Seifert, with no first name or biographical identification added.

The first sentence is a question by its wording. Its raw numeral-like `1` in DOR1 is not silently treated as T: that change is part of the recorded substitution cost. Unknown square labels in the raw body are not freely assigned letters to obtain familiar words.

## Local and global insertion alternatives

All indices are zero-based. The five boundaries around XVGF have these costs for the displayed complete word proposal:

| Insertion boundary | Observed substitutions | Existing source-mask fills | Inserted-slot fills |
| --- | ---: | ---: | ---: |
| 35 | 8 | 1 | 1 |
| 36 | 7 | 1 | 1 |
| 37 | 6 | 1 | 1 |
| 38 | 6 | 1 | 1 |
| 39 | 7 | 1 | 1 |

All 102 boundaries in the entire received stream were also tested against the same disclosed candidate. Only **37 and 38** attain the minimum of six observed substitutions. Both choices produce the same completed ciphertext under the fixed key, but their source-to-model maps and missing-slot values differ. The primary display uses boundary 38; the alternative is not suppressed. This is a conditional minimum within the 102-coordinate model and chosen wording, not an exhaustive proof over other message lengths or plaintexts.

For the primary frame, the exact observed substitutions are source **31 V→F, 32 F→V, 34 D→X, 37 G→X, 53 V→X and 79 D→X**. The K-like source glyph at **24** is filled with X; the additional coordinate at boundary **38** is D. At the equal boundary-37 alternative, the inserted value is X, with its different observed repair map retained in the certificate.

| Primary scope | Count |
| --- | ---: |
| New physical source records | 1 |
| Occupied source slots / valid coordinates | 101 / 100 |
| Modeled coordinates / plaintext positions | 102 / 51 |
| Fixed conditional raw / edited labels | 47 / 51 |
| Observed substitutions | 6 |
| Source-glyph fills / additional-coordinate fills | 1 / 1 |
| Observed-coordinate deletions or moves | 0 |

The source and candidate permit the restored question, but the edition does not add a first name for Seifert, identify a historical person, specify the pump's later use, or establish that it was delivered.

## Credit and reproduction

Published period keys: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Earlier repository OCR and unchanged-key outputs are retained separately. Source review and explicit editorial work: icekylinx and GPT-6 Astra Pro.

The earlier OCR body and its unchanged-key decoding remain in [separate provenance files](../../experiments/benzol_pump_query/prior_candidates.json). The missing coordinate is a source-length issue, not a claim that the earlier OCR simply omitted a visible fifth glyph. Verification replays all insertion prices, every source/model mapping and edit, the complete roundtrip, and exact readable-label preservation.

```sh
python experiments/benzol_pump_query/verify.py --verify
python experiments/benzol_pump_query/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The optional PDF check verifies the original scan digest and exact crop pixels. Successful re-encryption proves compatibility with the stated source model and proposed wording; it does not establish a unique historical loss location.
