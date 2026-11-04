# p59 A1: three conditional transfers between repeated vessel-like labels

**Source comparison and verification: icekylinx and GPT-6 Astra Pro.**

The [existing first-part edition](../../cases/pages/059.md#edition-cases-caucasus-poti-first-part-conditional)
has 105/110 proposed positions after five observed-coordinate substitutions,
two mask fills and five conditional source exclusions. Its two `AUF DAMPFER`
clauses each contain a pair of similar labels. Treating each pair as a
repeated field, at minimum additional observed-coordinate cost, gives three
common missing letters: **N35, R40 and L81**. The common extension reaches
**108/110** with **four extra mask fills and zero extra observed substitutions**.
It leaves the conflicting observed vowels and the raw separator-like `4`
unchanged.

| Field starts | Raw copies in all 21 frames | Exact minimum equal-copy strings | Additional substitutions if full equality is enforced |
|---|---|---|---:|
| 32, 38; five labels each | `VUR?A`, `VA?NA` | `VARNA`, `VURNA` | 1 |
| 69, 76; six labels each | `BURDAL`, `BYRDA?` | `BURDAL`, `BYRDAL` | 1 |

Every index is zero-based. All **four** joint minimum equal-copy variants
remain in the certificate. Their total cost is seven observed substitutions
and six mask fills, besides the original five exclusions. No dictionary,
name list, historical identity or language score selects among them.
The less committal common layer costs only five substitutions and six fills;
it is deliberately not a claim that its conflicting whole labels are equal.

## Exact evidence

Each transferred letter appears directly in the corresponding position of
the other local field. N and R each fill one missing coordinate; L fills a
wholly absent pair. The verifier prices every one of the 36 labels at each
position against both received pairs. Because the complete square and frame
are fixed, these position costs factor exactly: the comparison covers all
36^5 and 36^6 equal-copy strings without assuming independent unknown key
assignments. The resulting common letters are the same for all 21 source
maps retained by the original word-stencil calculation.

The verifier independently reruns that original bounded alignment and
checks that its 21 maps and minimum five-substitution/two-fill cost remain
unchanged. It does not introduce a new source frame or reselect the frames
using the proposed names. It reconstructs both earlier and extended layers
for every map, compares a second decoder, retains source-coordinate ledgers,
and re-enciphers an explicit complete witness. The two opening unknowns
still allow 36 complete plaintexts per map; the witness does not select one.

The 225 literal slots, printed `RICHI-220`, unchanged Sep19–21 key, eight
original erasures and all previously protected numbers remain intact. Raw
103/110 is a count **under the conditional 220-slot frame**, not a claim
that the unmodified 225-slot stream reads that way. No physical record is
added.

## Historical context has a separate role

[Navigation Maritime Bulgare's own history](https://navibulgar.com/en/company/history/index.php)
records a prewar steamer named *Varna*. This supports that spelling as a
period vessel name, but neither the September shipment nor a particular
hull follows from it. The public caption
[*Poti, Ship Varna*](https://www.flickr.com/photos/39631091@N03/15359293270/)
attributes its photograph to a German officer in winter 1918. Only the
caption metadata was inspected; no image is redistributed or treated as
verified evidence of the September voyage. `VURNA` remains tied under the
exact coordinate-cost model. The second label has not been identified, and
is not normalized to *Burgas*.

## Related command-number context

The later part of the Poti exchange retains `GENKDOX?2`, with decimal
candidates 12, 32, 52 and 62. Baumgart's published quotation of Hopman's
16 September 1918 diary names General Command 52 in the decision to hold
the *Corcovado* transport: [*Das Kaspi-Unternehmen*, first part, p103,
note 285](https://openscience.ub.uni-mainz.de/server/api/core/bitstreams/19e5318f-7b9b-4ab1-ba90-5be25c049b40/content).
This establishes relevant shipping context, but does not identify the
command in the p59 request. All four candidates remain; no coordinate is
filled. The [bounded source check](command_context.json) records the
inspected scope and the evidence still needed to connect the messages.

## Reproduce

```sh
python experiments/p59_repeated_vessel_labels/verify.py --verify
python experiments/p59_repeated_vessel_labels/verify.py --verify --pdf /path/to/childs_original.pdf
```

The original source package's input and certificate hashes are bound in the
new inputs. Its case display checks remain attached to the original
105/110 section; this package verifies the separate new display and all
its literal labels. Existing Childs/key credits and earlier source/frame
work remain unchanged. No first historical decipherment claim is made.
