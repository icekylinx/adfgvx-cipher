# Post-publication source-recovery review

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

**State: in progress.** The initial remote publication was confirmed at
2026-11-02 23:27:19 UTC. The requested additional two-hour work period
runs until at least 2026-11-03 01:27:19 UTC. No completed duration is
claimed by this checkpoint.

## Current preserved inventory

This snapshot compares **195 → 264 other physical source records**, with all
22 challenge entries preserved. It adds **69 physical records across 15 source
packages** and keeps every earlier record. The separate November25
interpretation audit adds no physical record.

The new source packages account for **16,586 printed coordinate slots** and
**8,313 modeled plaintext positions**, of which **8,114 have fixed raw labels**
under their stated frames. These are coverage counts. They include repeated
copies, previously identified bodies, conditional geometry and unresolved
historical numeral meanings; they are not a count of first decipherments or
universally correct original letters. All 112 observed-coordinate substitutions
are recorded locally, separately from source erasures and inserted values.

## Source packages

| Package | Physical records | Printed slots | Modeled positions | Fixed raw labels | Observed substitutions |
|---|---:|---:|---:|---:|---:|
| [Crown airlift and an interrupted banknote instruction](../crown_airlift/README.md) | 3 | 371 | 195 | 175 | 1 |
| [Repeated ZITAG stop-order and contract cancellation](../zitag_purchase_orders/README.md) | 5 | 1068 | 534 | 531 | 14 |
| [Military meal allowances and a refused supplement](../military_allowances/README.md) | 4 | 1760 | 880 | 877 | 10 |
| [Six-part Orient intelligence report](../orient_intelligence/README.md) | 6 | 2020 | 1010 | 1009 | 4 |
| [Liman troop-report request, p222 A](../liman_troop_reports/README.md) | 2 | 414 | 207 | 207 | 1 |
| [Military-intendant addresses and responsibilities, p202 B](../military_intendant_remit/README.md) | 4 | 877 | 441 | 421 | 10 |
| [Neuhof demobilization instruction, p228 B](../neuhof_demobilization/README.md) | 3 | 696 | 348 | 298 | 10 |
| [Recall of the Turkish military mission](../turkish_mission_recall/README.md) | 4 | 1290 | 645 | 645 | 3 |
| [Hungary transport warning: a witnessed missing group](../hungary_transport_warning/README.md) | 6 | 877 | 441 | 405 | 2 |
| [September radio listening and acknowledgment procedure](../september_radio_procedure/README.md) | 3 | 556 | 278 | 275 | 3 |
| [Rail, motor and air transport on 30 November](../late_transport_dispatches/README.md) | 6 | 1442 | 721 | 677 | 14 |
| [Armistice transit and withdrawal planning, pp125-126](../armistice_transit_planning/README.md) | 7 | 1537 | 769 | 764 | 10 |
| [DEUTZITAG dispatch inquiries and an adjacent Tiflis order](../deutzitag_dispatch_inquiries/README.md) | 4 | 1018 | 509 | 509 | 1 |
| [Constanza naval-radio and telephone connections](../constanza_radio_connections/README.md) | 6 | 1308 | 654 | 654 | 5 |
| [Mackensen armistice appeal: six-part source edition](../mackensen_armistice_appeal/README.md) | 6 | 1352 | 681 | 667 | 24 |

The [complete inventory](inventory.json) preserves every added identifier,
package summary, case path and counting limit. The [inputs](inputs.json)
pin both catalogues and 187 package/case artifacts. Earlier statuses, subjects
and credits are unchanged; 164 old path fields follow the explicit topic-migration map.

## Independent source-image binding

All **84 delivered source images** have normalized PDF-page, rectangle, scale,
file-hash, RGB-hash and dimension metadata. The optional PDF verification
regenerates each crop from the pinned original and compares every RGB pixel.
This authenticates the crop location; it does not automate manual glyph
judgments or prove an editorial plaintext.

The original PDF SHA-256 is
`157e41a12374c6c1f464f52f587fbf6be6e0e08706ac35f7f4b0d66dc798ad06`.

## Reproduce

```sh
python experiments/post_push_review/verify.py --verify
python experiments/post_push_review/verify.py --verify --pdf /path/to/childs.pdf
```

Default verification uses the standard library. PDF pixel checking needs
PyMuPDF and Pillow. Individual cryptographic and geometry verifiers remain
beside their packages and run in CI.

The review uses preserved start/end catalogues, so a later live catalogue
can grow without rewriting its historical count. The earlier
[87-to-195 review](../session_review/README.md) remains separate and unchanged.
When this work period is complete, its authoritative completion timestamp
will be recorded and the verifier will require at least 7,200 seconds after
the confirmed initial push.

For readable messages, use the [case guide](../../cases/README.md); for the
reorganized layout, use the [repository map](../../docs/repository-map.md).
