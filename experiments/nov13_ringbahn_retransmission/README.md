# p187 B1: the truncated Ringbahn-key instruction

**Source recovery and edition: icekylinx and GPT-6 Astra Pro.**

The printed 13 November reception repeats the 6 November key instruction
already received on p145 and p211. The matching `2230 (6/11)` header,
`RICHI-214` length and long exact coordinate runs identify the source family.
This edition restores the truncated reception through an explicit
copy-origin map and retains its disagreements.

[Read the source edition](../../cases/pages/187.md#edition-cases-radio-nov13-ringbahn-retransmission)
· [Source and assumptions](inputs.json)
· [Per-position certificate](certificates.json)
· [Original PDF, p190](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view)

## Reconstruction

| Evidence layer | Exact account |
| --- | --- |
| Printed source | 140 slots: 139 observed coordinates and one dash |
| Conditional frame | 214 slots; excludes two duplicated five-groups and adds 5 prefix, 5 interior and 74 tail slots |
| Unfilled primary reading | 33/107 fixed labels; all 84 missing coordinates unassigned |
| Source-linked reading before repairs | 106/107 fixed labels; 83 supplied coordinates from p145 B1 and one from p211 B1 |
| Complete candidate | 107/107 fixed labels; five observed substitutions and one printed-mask fill |

Each duplicated group has two identical printed occurrences. All four
combinations of exclusion origins yield the same frame, raw reading and
candidate. They enumerate the aliases of this stated group model; the model
depends on identifying the common 214-coordinate source body.

The candidate says not to destroy the November Ringbahn key and begins the
clause deferring the December key. The original reference `B848727` and the
unfinished clause remain literal. Later independently received parts supply
the continuation. The copied 84 coordinates and their 73 newly fixed labels
are kept outside the 33-position raw total.

The five changes to observed p187 coordinates are **26 X→V, 75 X→D,
76 D→A, 77 X→D, 78 V→X**. The dash at **79** is filled as `V`.
All six replacement values have observed p145 source witnesses. The
`FXDFF` group at p187 source 25 agrees with p211 but disagrees with p145's
`FVDFF`; that raw disagreement is retained and priced. Among copied frame
slots, model 46 instead uses the p211 `V`, which differs from p145's `A`.
No key cell or numeral value is changed.

## Provenance

The earlier [p145 source edition](../nov6_ringbahn_key_witnesses/README.md)
and [p211 source edition](../open_targets_continuation/README.md) retain their
complete body and key credits. `inputs.json` pins both source records and the
earlier unreviewed p187 OCR block. The source crop is an external PDF reference:
its page, rectangle, render scale, dimensions and RGB hash are retained,
and `--pdf` reproduces the reviewed pixels from the authenticated scan.

## Reproduce

```sh
python experiments/nov13_ringbahn_retransmission/verify.py --verify
python experiments/nov13_ringbahn_retransmission/verify.py --verify --pdf /path/to/childs.pdf
```

The verifier independently checks the column-offset inverse against the shared
cipher implementation, all four alias maps, every original and donor coordinate,
all repair prices, full re-encryption, and the actual Markdown source, raw,
edited and German displays. `catalog_proposal.json` contains one new physical
source entry; it adds no new first-decipherment credit for the earlier body.
