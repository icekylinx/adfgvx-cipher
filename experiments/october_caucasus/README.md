# October Caucasus source recovery

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

[Read the five exchanges](../../cases/other/october_caucasus.md).

Nine source-reviewed parts on printed pp. 69–72 recover messages about Kress's delegation, Westernhagen's economic work, equipment sent to Tiflis, Violetta's cargo for Poti and radio timings. They use the earlier published **October 4–6** square and 22-column rank. The present contribution is source assembly, explicit duplicate/short-group recovery and readable editions, not a new key or a claim to first historical decipherment.

The literal edition preserves **1,994 source slots** in the nine readable parts. Under the stated layout models, they have **968 plaintext positions**; **928 are fixed across every declared model** before editorial repairs. A fixed raw position may contain a historical garble: these counts do not say that 928 intended letters have been proved. The reader-facing templates have a minimum total of **37 known-coordinate substitutions**, plus **27 or 28 asserted erasure fills**, depending on the retained p72 A2 duplicate. Missing slots, duplicate removals and substitutions are recorded separately. Another **85 surviving coordinates** belong to the interrupted p71 A2 continuation; no plaintext is accepted for that fragment, and it is excluded from the readable-part totals.

## Productive source constraints

| Source | Constraint and recovery |
|---|---|
| p72 A1 | A repeated 25-coordinate run is visibly struck out. Applying the source's strikeout yields the readable delegation-reinforcement part. |
| p72 A2 | Two neighboring 25-slot runs agree at every observed coordinate; one contains a non-coordinate `S`. Removing either produces the same administrative-personnel text apart from one raw letter domain. Both alternatives remain. |
| p70 A1 | Two separate exact five-coordinate repeats occur at line boundaries. Removing one copy of each yields four source-index aliases but one normalized ciphertext, recovering the Westernhagen instruction. |
| p70 A2 | The header's 256 differs from the actual 246 slots. The actual-length inverse is readable and is retained without padding. |
| p69 B1/B2 | Each body is one coordinate short of its header and contains a four-letter group. Every insertion boundary within those groups is retained. The short continuation has two minimum-cost alignments. |
| p71 A1 | The exact 170-slot body decodes directly except for source erasures and one coordinate error. The proposed 20-kW rating requires a missing-digit fill, while 16 kW survives directly. |
| p71 A2 | The source explicitly records interference after 85 of 192 advertised slots. Padding the unavailable suffix fixes no complete plaintext character, so no reading is asserted. |

The p70 and p72 A2 duplicate deletions are reconstruction hypotheses, unlike the explicit p72 A1 strikeout. The p69 omission locations are also hypotheses. Word corrections, expansion of abbreviations and prose punctuation form a separate layer. The case page preserves unresolved numbers and office abbreviations instead of forcing a complete fluent quotation.

## Files

- `inputs.json`: literal image-reviewed rows, headers, frozen key and provenance, every layout alternative and proposed fixed-length editorial template.
- `certificates.json`: all raw letter domains and coordinate origins, minimum-cost aliases, every asserted substitution/fill and a full arithmetic re-encryption witness.
- `sources/`: five focused crops of the hash-pinned Childs scan. No full book is redistributed.
- `verify.py`: an independent column-offset inverse compared against the project implementation; checks image hashes, repeated runs, short-group boundaries, domains, repair costs and exact roundtrips.

```sh
python3 experiments/october_caucasus/verify.py --verify
python3 experiments/october_caucasus/verify.py --verify --pdf /path/to/childs.pdf
```

Python's standard library suffices. An arithmetic witness may fill an otherwise unasserted erased coordinate with `A` only to make a complete roundtrip; those arbitrary filler letters are explicitly identified and are never promoted to plaintext. The verifier's per-position records link each proposal back to its literal source slot or an explicitly inserted slot.

## Attribution and relevance

The key retains the original Childs / George Lasry / Lasry, Niebel, Kopal and Wacker references from `data/keys.json`. The new reading and source-repair work is by **icekylinx and GPT-6 Astra Pro**. The Kress traffic is useful historical context, but it does not recover the separate open p73 ciphertext or resolve that message's inconsistent dates.
