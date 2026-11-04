# p187 D1: aircraft connection unavailable for technical reasons

Prepared by **icekylinx and GPT-6 Astra Pro**. The Nov13–15a period key is
the published Lasry-team key; its attribution remains in `data/keys.json`.
No first historical decipherment priority is claimed.

## Recovered message and its qualification

The surviving first part addresses **O.K. Mackensen**. Its final 76
plaintext positions have the following coherent proposed reading:

```text
VERBINDUNGXMITXRXODERXGXFLUGZEUGENXZXZTXAUSXTECHNISCHENXGRUENDENXUNMOEGLICHX
```

In ordinary prose: *Verbindung mit R- oder G-Flugzeugen z. Zt. aus
technischen Gruenden unmoeglich.* A connection using R or G aircraft is
currently impossible for technical reasons. The letters R and G are
retained exactly; no aircraft model or operational purpose is inferred.

This is a conditional frame reconstruction. The source prints `RICHI-252`
but has **247 ADFGVX coordinates**, plus a small dash-like mark before the
complete group `GFVVV`. Treating that mark as non-coordinate and supplying
one absent five-coordinate group gives a 252-coordinate frame. The full
suffix then requires **two known-coordinate substitutions** and the five
inserted coordinate values. The literal source, excluded mark, inserted
group and substitutions are all separately recorded.

The baseline output before the two letter repairs and inserted-value
completion is:

```text
OXKXMACKENSENXZUXWORTXRMX?XDX?????XUXRMX?XAX?????XVERBINDUNGXMIT?RXODERXGX?LUGZEUGIN?ZXZTXAUSX?ECHNISCHE?XGRUENDENXUEMOEGLICHX
```

The proposed completed edition is:

```text
OXKXMACKENSENXZUXWORTXRMX?XDX?????XUXRMX?XAX?????XVERBINDUNGXMITXRXODERXGXFLUGZEUGENXZXZTXAUSXTECHNISCHENXGRUENDENXUNMOEGLICHX
```

There are 126 plaintext positions: the framed raw reading fixes 109, and
the edition fixes 114. The **12 unresolved positions** are all in the
opening reference fields. Their coordinate pairs occupy five distinct
unassigned square cells. They are not 12 independent free characters: a
single global injective square must respect all repeated cells. The
published unused-symbol pool is `0123456789QY`; no numerical values have
been assigned by this package. The raw `WORT` and `RM` are retained without
expansion or silent repair.

## Why the missing-group position is plausible

The primary candidate inserts `DDDVV` after 245 received coordinates, at
the printed group boundary between the final complete group `DDDAA` and
the partial group `DG`. Thus it fills a whole absent group at a natural
typesetting boundary. Inserting `DDVVD` one coordinate later gives the
**identical completed ciphertext**. These are source-equivalent placement
aliases, not two independently recovered messages.

The two changes to received coordinates are:

| Received coordinate position, one-based | Observed | Proposed | Plaintext consequence |
| ---: | --- | --- | --- |
| 25 | `X` | `V` | `UEMOEGLICH` becomes `UNMOEGLICH` |
| 223 | `A` | `X` | `FLUGZEUGIN` becomes `FLUGZEUGEN` |

The alternative of treating the mark as one coordinate erasure and
inserting only four missing coordinates was also examined. For this same
76-character suffix, all 249 possible contiguous insertion boundaries
require at least **28** changes to received coordinates, compared with
two under the excluded-mark/five-loss model. All 248 boundaries of the
latter model were evaluated; only the source-equivalent boundaries 245
and 246 achieve the two-substitution minimum.

This is a comparison of two specified frame families for a suffix proposed
after inspection. It is not an exhaustive proof about every original text,
square, column order, or damage model. The five missing symbols remain an
editorial reconstruction, not observed source glyphs.

## Source and remaining limits

J. Rives Childs, *General Solution of the ADFGVX Cipher System*, printed
p187 / PDF page 190, in the
[public scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view).
The enlarged crop in `sources/childs_p187_D.png` includes the complete
record and header. The header reads `D) NKJ v LP (03.04 a.m., November
13th); FUER UKS 20.12 (13/11)`, followed by a multipart-total glyph left
unasserted here, and `1 TL RICHI-252`. It ends `(Continued)`.

The apparent same-day ordering of the origin/intercept times is preserved
as printed. No chronological correction, missing continuation, complete
reference number, aircraft model, or broader evacuation purpose is supplied.

## Verify

```sh
python experiments/aviation_connection/verify.py --verify
python experiments/aviation_connection/verify.py --verify --pdf /tmp/adfgvx-childs.pdf
```

`inputs.json` freezes the literal rows, crop rectangle/hash, source PDF
hash, published key and proposed suffix. `certificate.json` retains both
gap aliases, the exact domains, all edits and all 497 fixed-suffix geometry
comparisons. The reader independently computes physical-column offsets
and checks the project cipher implementation. A completed square witness
re-encrypts to every candidate coordinate; its arbitrary assignments to
unresolved cells are consistency witnesses, **not accepted reference
numbers**.

## Companion p187 C: request to check the connection

**Original reading:** [Ayush Agarwal (@AyushAg1002), 28 October 2026](https://github.com/dbourdeau/cyphersolver/issues/181).
This body and its source transcription were already reviewed in the
canonical `cases/supplementary/p187_C.md` and
`data/supplementary_readings.json`. The present addition supplies the exact
four-coordinate repair cost and same-length re-encryption certificate. It
does not claim a new body reading or source transcription.

The separately certified message C on the same page reads:

```text
BITTEXSOFORTXBESCHEIDXOBXVERBINDUNGXMITXARMEEXMAKENSENXEINWANDFREIX
```

It requests an immediate report on whether the connection with Mackensen's
army is satisfactory. The raw spelling `MAKENSEN` is retained. The 134
source coordinates agree with the printed length, with no erasure or
insertion. Four known-coordinate substitutions repair `BE?CHEID`,
`VERPINDUNG`, `MIS`, and `EINWA?DFREI`, taking the baseline reading from
65 fixed positions to a complete 67-character edition. The two unknown
square cells are not assigned duplicate S/N values; their source
coordinates are explicitly repaired to the existing S/N cells.

The separate files `companion_inputs.json`, `companion_certificate.json`,
and `sources/childs_p187_C.png` preserve the evidence and original credit.
The verifier also compares its literal ciphertext, unchanged key, raw
plaintext and exact domains against the prior canonical record. Run:

```sh
python experiments/aviation_connection/verify_companion.py --verify
```

Message C's header is `NKJ v LP (16.09 p.m., November 13th); FUER UKS
12.45 (13/11)`. These headers do not establish that C and D1 form a
chronologically ordered request and reply.
