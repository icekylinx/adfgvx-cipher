# p97: wireless routing, repetition and supplies

Prepared by **icekylinx and GPT-6 Astra Pro**. The
[reader case](../../cases/pages/097.md#edition-cases-radio-hungary-connection-and-supplies) presents
three separately headed records on Childs printed p. 97 / PDF p. 100,
1 November 1918.

| Record | Native source slots | Fixed raw / total plaintext positions | Observed-coordinate substitutions | Source fills or geometry changes |
|---|---:|---:|---:|---:|
| p97 A | 196 | 98 / 98 | 0 | 0 |
| p97 B | 246 | 123 / 123 | 0 | 0 |
| p97 C | 196 | 98 / 98 | 6 | 0 |
| **Total** | **638** | **319 / 319** | **6** | **0** |

A requests immediate repetition of a telegram, preserving its unexplained
code and reference fields. B reports that communication through Hungary is
disrupted and telegrams will go by wireless until further notice. Both read
under the unchanged published November 1–3 key with no repair. The reference
to `CHI` in A's body does not replace the source's `RICHI-196` marker.

C mentions tubes and oil in a numbered reply. Its proposed word correction
changes three plaintext labels, each through two observed-coordinate
substitutions. The six source symbols are legible; the edition does not
pretend they were erased. All raw numerals are unchanged. The original C
body remains visible and the fixed-position count is not a measure of the
proposed repair's certainty.

## Reproduce

```sh
python3 experiments/hungary_connection_and_supplies/verify.py --verify
python3 experiments/hungary_connection_and_supplies/verify.py --verify --pdf /path/to/childs.pdf
```

The default verifier is standard library only. It checks all literal source
rows and advertised lengths, reconstructs raw text with sorted intermediate
indices, independently re-encrypts by slicing original columns, verifies
every coordinate repair and numeral position, checks the frozen prior-evidence
and image hashes, and compares the result with `certificates.json`.

The optional PDF check requires PyMuPDF. It verifies the complete PDF SHA256
and re-renders all four source images with the recorded rectangles and scales,
clearing the image cache and checking exact pixel hashes. The PDF SHA256 is:

```text
157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06
```

[Full p97](sources/p97_full.png) · [A](sources/p97_A.png) ·
[B](sources/p97_B.png) · [C](sources/p97_C.png).

## Attribution and bounded contribution

The period key is prior Lasry-team work and retains its complete provenance
in `inputs.json`. `prior_evidence.json` preserves the three earlier unreviewed
OCR records and their original screen hash. C already had the same mostly
readable raw candidate. A/B had wrong 197/241 lengths; the source confirms
196/246. The complete native A/B bodies, source edition and priced C word
repair are this review's additions. No historical transmission insertion or
deletion is inferred from those OCR corrections, and no universal priority
claim is made.

The complete body, source, raw/edited distinction and local expansion notes
are preserved in the reader case. No reference string, numeral or historical
identity is silently filled.
