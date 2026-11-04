# p170: source-family matching with unknown column order

Both exact matchers recover the 106-coordinate synthetic source control. The
partial-donor control also passes simultaneous re-encryption against its
original donor coordinates and the target fragment. **No historical p170
match or accepted plaintext is found within the frozen bounds.**

This branch tests a different reuse hypothesis from the earlier fixed-rank
substring screens: the same plaintext may have been transmitted using another
column order. A complete donor supplies physical column strings; the target
must fit one contiguous fragment of a permutation of those columns. The first
and last observed columns may be partial, and every column can be used only
once. A returned witness specifies a complete rank permutation and offset.
Unobserved outer columns can leave these values nonunique.

For a partial donor, each plaintext position retains its exact domain from
that donor's original coordinates and complete registered square. The search
intersects both target coordinate halves with the **same letter domain**.
It requires at least **90/106** observations to lie on donor positions already
fixed by complete original donor pairs. Up to 16 observations can involve
partial domains. All source and target squares are complete in each tested
assignment; no unknown key cell is assigned independently by position.

## Frozen scope

| Donors | Square hypotheses | Widths | Error budget | Projects |
|---|---:|---:|---:|---:|
| 291 complete source-derived strings | 11 | 12–24 | 0, then 1, then 2 observed substitutions | 41,613 per budget |
| 105 native partial source-domain families | 11 | 12–24 | 0, with the 90/106 support threshold | 15,015 |

The square hypotheses are nine complete recorded period squares and both
consistent global 5/6 assignments of the November 7–9 square. Complete donor
strings include raw and explicitly edited source layers; they are not all
independently authenticated historical wording. A hit would require source
review before acceptance. The partial branch omits partial source squares,
modified frames, insufficient native fixed positions and unsupported source
tokenizations. Its original half-coordinate evidence is retained exactly.

### Damaged-glyph dependency refresh

The p107 C source 45 and p77 A source 67 reviews changed one previously
definite coordinate in each donor to `?`. Their raw plaintexts therefore
cease to be complete: p107 C has 173/174 fixed labels, and p77 A has
156/157. The former complete-donor IDs **146** and **284** are removed
from that pool and represented as native partial-domain IDs **104** and
**105**, respectively. The ambiguous labels remain coupled to their
observed coordinate halves; neither old label is silently restored.

That first refresh is retained in `source_glyph_refresh` as history. Three
later corrections are recorded separately in `resumed_source_review`:

- The p62 B editorial reference remains `?10`; former complete donor **131**
  is excluded. Its edited template is not promoted to a native partial source.
- The p87 A1 glyph at source index 35 is **D**, producing native `X` at
  plaintext index 9. The same previously selected source now has **83/83**
  fixed labels, so partial family **87** becomes complete donor **293**.
- The p56 A glyph at source index 202 is **F**, improving partial family
  **101** from **109/111** to **110/111** fixed native labels. Its remaining
  invalid coordinate and exact domains are retained.

All other donor IDs, texts and origins remain unchanged. Vacated IDs are not
reused. These adjustments preserve the original source-family scope; target
observations, square hypotheses, width bounds, error budgets, the 90/106
support threshold, search engines and controls are unchanged.

Full replay of the refreshed pools gives:

| Branch | Projects | Histogram passes | DFS nodes | Hits |
|---|---:|---:|---:|---:|
| Complete, budget 0 | 41,613 | 13,572 | 47,446 | 0 |
| Complete, budget 1 | 41,613 | 14,911 | 369,694 | 0 |
| Complete, budget 2 | 41,613 | 16,224 | 753,976 | 0 |
| Partial, support at least 90/106 | 15,015 | 7,098 | 30,606 | 0 |

The changed counts follow from the explicit source corrections and donor
classification above. They do not produce a p170 reading.

These are finite donor-family checks, not an exclusion of other plaintexts,
keys, widths, damage or missing-length models. The original 106 count is
handwritten; it does not establish the transmitted length. No language score
or candidate p170 wording enters either matcher.

## Controls and verification

The complete-donor control retains 106 coordinates from a fresh 128-coordinate
technical message with hidden ranks. Its two-error version fails budgets 0
and 1 and succeeds at budget 2. Twelve small cases are independently checked
against every rank permutation and offset at all three budgets.

The partial control uses a separate source key and four erased donor
coordinates. Its returned witness has **99/106** directly fixed supports and
satisfies both sources. A false combination admitted by independent row/column
marginals is explicitly rejected. Eight more small cases are checked by
independent enumeration of all allowed plaintexts, ranks and offsets.

```sh
python experiments/p170_new_methods/followup/verify.py --verify
python experiments/p170_new_methods/followup/verify.py --verify --replay
python experiments/p170_new_methods/followup/verify.py --verify --pdf /path/to/childs.pdf
```

The default standard-library check verifies source provenance, native frames,
control witnesses, independent small-case results and the frozen certificate.
`--replay` needs a C++17 compiler and reruns every historical scope and control.
`--pdf` verifies the original PDF and source-crop pixels; the default reports
that external pixel comparison as unchecked. No PNG asset is included.

`extract.py --output /path/to/candidate.json` produces a new candidate donor
snapshot without replacing the tested inputs. New sources do not silently
expand the frozen scope.
Prepared by **icekylinx and GPT-6 Astra Pro**. Published key provenance and
prior source/body credits remain attached to the referenced source editions.
No historical first-decipherment claim is made.
