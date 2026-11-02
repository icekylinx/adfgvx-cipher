# ADFGVX 1918

**IceKylin and GPT-6 Astra (OpenAI)** · [Contributors](AUTHORS.md) · [Sources](sources/registry.json)

A unified edition of the **22 German radio cryptograms** in Klaus Schmeh and George Lasry's challenge: original source transcription, earlier decipherments, corrections, new source relationships, and reproducible verification.

## Results

- **p152:** the damaged challenge fragment matches the fuller p136 transmission. The parallel recovers the body and continuation; every supplied or changed coordinate is recorded.
- **p158:** the challenge combines portions of two separate messages. An exhaustive alignment identifies the split; repaired component copies decrypt and re-encrypt exactly.
- **p189:** a clearer p185 near-parallel supports a conditional partial reading. All ten optimal source-preserving alignments are retained.
- **Earlier results remain part of the edition.** The 2017 readings and September 2026 p176b/p217 publications retain their original authorship. Raw decipherment, conjectural repair, and historical interpretation are distinguished.

Five entries remain wholly open: **p73, p153a, p153b, p170, p198**. A source-linked recovery or contextual reading is not counted as an independently solved original ciphertext.

| Entry | Reviewed state | First reading or present contribution |
|---|---|---|
| `p73` | Open | — |
| [p100](cases/p100.md) | Prior body reading; source audit | Armin (2017 comment author) |
| [p105](cases/p105.md) | Prior body reading; source audit | Norbert (2017 comment author) |
| [p109](cases/p109.md) | Prior body reading; source audit | Norbert (2017 comment author) |
| [p132](cases/p132.md) | Prior body reading; source audit | Thomas (fragment), Norbert (body) |
| [p146](cases/p146.md) | Prior body reading; source audit | Norbert (2017 comment author) |
| [p152](cases/p152.md) | Source-linked body | This review, 2026 |
| `p153a` | Open | — |
| `p153b` | Open | — |
| [p158](cases/p158.md) | Composite sources identified | This review, 2026 |
| [p164a](cases/p164a.md) | Prior partial; constraint audit | Norbert (2017 comment author) |
| [p164b](cases/p164b.md) | Prior partial; constraint audit | Norbert (2017 comment author) |
| `p170` | Open | — |
| [p171](cases/p171.md) | Prior body reading; source audit | Norbert (2017 comment author) |
| [p176a](cases/p176a.md) | Prior body reading; source audit | Norbert (2017 comment author) |
| [p176b](cases/p176b.md) | Prior contextual reading; constraint audit | Prinz (2026 publication) |
| [p215](cases/p215.md) | Prior partial; constraint audit | Norbert (2017 comment author) |
| [p187](cases/p187.md) | Prior body reading; source audit | George Lasry, Norbert (2017 comment author) |
| [p187b](cases/p187b.md) | Prior body reading; source audit | George Lasry, Norbert (2017 comment author) |
| [p189](cases/p189.md) | Conditional partial | This review, 2026 |
| `p198` | Open | — |
| [p217](cases/p217.md) | Prior body reading; correction verified | Prinz (2026 publication), Christian Horvat (later correction) |

## Verify

Python 3.10 or later; standard library only:

```sh
python3 -m adfgvx.verify
python3 -m adfgvx.verify --json
```

The verifier checks independent ADFGVX arithmetic, seven exact source roundtrips, the p152 suffix alternatives, the p158 splice and glyph variants, every p189 source-preserving alignment and plaintext domain, and 25 explicit reconstructions of 14 earlier-readable entries. The p164/p215 checks also reproduce uncertainty counts and contradictions in later completions. Odd-length ciphertext cannot silently lose a coordinate.

## Contents

| Path | Contents |
|---|---|
| `cases/` | Readings, qualifications, original credits, and source links |
| `data/messages.json` | All 22 source records, legacy transcriptions, and conservative analysis layers |
| `data/keys.json` | 24 historical, comparison, or reported keys; provenance and unknown cells retained |
| `data/prior_readings.json` | 34 attributed earlier readings/fragments and 25 recomputed repair variants |
| `data/certificates/` | Machine-readable source, edit, and plaintext evidence |
| `adfgvx/` | Independent cipher and verification code |
| `sources/` | Bibliography and selected source excerpts |

Identifiers use the printed page number. `p187` and `p187b` are the two parts listed separately in the original challenge. A question mark means unresolved evidence, never an arbitrary completed square cell. Original German text is preserved as data; editorial material is in English.

## Credit and reuse

The present review is by **[IceKylin](https://github.com/icekylinx) and GPT-6 Astra (OpenAI)**. Historical records, prior decipherments, key recovery, and later corrections have separate attribution in each case and the source catalog. New code and editorial material use the [MIT license](LICENSE); third-party source material retains its own status.
