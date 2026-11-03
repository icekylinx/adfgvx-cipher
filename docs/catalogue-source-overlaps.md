# Catalogue editions and physical sources

Prepared by **icekylinx and GPT-6 Astra Pro** on 3 November 2026.

The catalogue keeps separate useful editions of one source visible while
counting the physical source once. The
[explicit overlap register](../data/catalog_source_overlaps.json) currently
contains one exact relation:

| Catalogue entry | Edition | Physical source |
| --- | --- | --- |
| [p132](../cases/p132.md) | Original challenge; Thomas's 2017 fragment and Norbert's fuller reading and sender-error model | Childs p132 B, PDF p135 |
| [p132_B](../cases/radio/p132_radio_service.md#b-repeat-the-fourth-period-telegram-in-the-fifth) | Later source and geometry audit of the same record | The same Childs p132 B |
| **Combined** | **Two reviewed entries** | **One physical source** |

Their complete 155-slot literal ciphertexts are identical: 153 valid
coordinates and printed dashes at source indices 103 and 104. Their source
location, reception header, advertised length and published key also agree.
The later edition adds an explicit comparison of four equivalent
intermediate-coordinate removals and a directly priced ordinary-word
proposal. It adds no second reception or physical source. The earlier
readers' contributions and alternatives remain credited in the challenge
case; both case pages and the generated tables link the editions.

No catalogue row, original identifier, proposal row, source transcript or
certificate is rewritten for this correction. The register preserves the
shared literal-source digest and two explicit evidence selectors. The
loader verifies both literal strings and both independently stored source
locations before accepting the relation.

## Counting rules

A **reviewed entry** is one catalogue row. A **physical source** is the
record at its printed-page and source-section location, with any shared
identity explicitly reviewed. Repeated transmissions and numbered parts at
different locations remain separate physical sources even when their
bodies agree. Similar text alone is never used to merge records.

Every duplicate source location must match the register. A new, unregistered
alias is rejected instead of being silently admitted or automatically
merged. For example, a proposed `p153_C5` entry duplicates the existing
challenge `p153a` at p153 C5 and fails this guard. Registering a relation
requires matching literal source evidence as well as matching location.

The page and topic tables count **reviewed entries**. They separately report
unique physical sources and sources additional to the original challenge
set. The p132_B row stays visible, carries a link to the original p132
credit, and contributes zero additional physical sources beyond that set.

## Cumulative inventory fields

The cumulative review output uses schema
`adfgvx-post-publication-review-v2` to distinguish these units:

| Field | Meaning |
| --- | --- |
| `catalogue.other_reviewed_entries_before/after` | The preserved earlier and later counts of non-challenge catalogue rows |
| `catalogue.added_catalogue_entries` | Added rows, including a later edition of an existing source |
| `catalogue.unique_physical_sources_before/after` | Unique sources across challenge and other entries together |
| `catalogue.additional_physical_sources_before/after` | Sources beyond those already in the challenge set |
| `catalogue.new_physical_records` | Sources present at the end but absent from the complete starting catalogue |
| `catalogue.added_editions_of_existing_sources` | Added entries whose source was already catalogued; p132_B contributes one |
| `added_catalogue_entry_ids` | All added edition identifiers |
| `new_physical_source_ids` | Only the canonical identifiers of genuinely new sources |
| `later_edition_ids_for_existing_sources` | Added editions of previously catalogued sources |

The underlying package summaries remain unchanged. A package can review an
already catalogued source, so its raw/model coverage remains useful without
being called new physical coverage. `coverage_totals.reviewed_record_entries`
retains the sum of those package record counts; separate fields report
`unique_reviewed_physical_sources`, `new_physical_sources` and
`previously_catalogued_physical_sources`. Coordinate and plaintext coverage
continue to describe the reviewed package scope. Their sum does not claim
that every position comes from a newly encountered source.

A package can also distinguish fixed labels in its unfilled source frame
from labels completed by an independently received copy. The cumulative
`fixed_raw_label_positions_under_stated_geometry` uses the unfilled count
for the reviewed one-coordinate parallel. Its
`source_linked_additional_fixed_label_positions` reports the extra fixed
position separately, with zero as the default for packages without that
explicit field. The underlying package's source-linked baseline and all
its certificate bytes remain unchanged.

The original start/end catalogue rows and all earlier metadata preservation
checks remain in force. The new relation corrects source-count claims;
it does not weaken preservation checks or change the cryptographic results.

## Verification

The ordinary catalogue and navigation checks include this register:

```sh
python -m adfgvx.catalog --check
python -m adfgvx.navigation --check
python data/reviews/verify_catalog_source_overlaps.py
```

The dedicated read-only check accepts the registered p132 overlap, rejects
that same overlap when its registration is removed, and rejects a proposed
p153_C5 alias. Its modified catalogues and register exist only in a temporary
directory; the actual catalogue, proposals and evidence remain unchanged.
