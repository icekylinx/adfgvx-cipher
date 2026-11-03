# p152 A2: a conditional report on crossing attempts

**Source review and partial word edition: icekylinx and GPT-6 Astra Pro.**

[Read the edition](../../cases/military/p152_crossing_fragment.md) · [Exact certificate](certificates.json) · [Independent place attestation](place_attestation.json)

The native **128-slot** source gives **61/64 fixed raw labels** under the unchanged Nov4–6 key. A priced partial word proposal reads **BIS VARC8IORO?A KEINE UEBERGANGSVERSUCHE** and preserves the complete closing field. It makes **seven observed-coordinate substitutions and two printed-mask fills**, fixing **63/64 positions**. The negative KEINE belongs to this proposed word edition; it is not a native source-fixed conclusion.

The primary place label remains **VARC8IORO?A**, with literal 8 and one source-mask uncertainty. The missing position has exactly six compatible values **{2,3,B,H,S,V}**; full re-encryption witnesses retain them all. The footer **A O0Q 17 ROED 1Q NR V054** is unchanged.

| Edition | Observed substitutions | Printed-mask fills | Fixed positions |
|---|---:|---:|---:|
| Native raw | 0 | 0 | 61/64 |
| Primary word proposal; opaque name | 7 | 2 | 63/64 |
| Optional VARCSIOROVA | 9 | 3 | 64/64 |
| Optional VERCSIOROVA | 11 | 3 | 64/64 |

An independently inspected **1896 primary source** at the National Széchényi Library prints **VERCSIOROVA** on printed p159 / PDF p6. It supplies historical place vocabulary with the rare CS sequence. It does not attest VARCSIOROVA's A vowel or the telegram's proposed negative report. The optional spelling layers therefore retain their complete additional prices. A separate Romanian National History Museum postcard record, inventory 385510, uses Verciorova and dates the object to 1901–1915.

All editions retain native source order, length, period key and square. There is no block move, inserted coordinate, dropped source glyph or free numeric relabelling.

```sh
python experiments/p152_crossing_fragment/verify.py --verify
python experiments/p152_crossing_fragment/verify.py --verify --pdf /path/to/childs.pdf
python experiments/p152_crossing_fragment/verify.py --verify --attestation-pdf /path/to/EPA02181_Termeszettudomanyi_kozlony_1896_154-160.pdf
```

The verifier checks actual Markdown strings, every native source mask and altered coordinate, all three exact prices, the untouched footer, six full remaining-mask witnesses and optional name re-encryption. The original Childs PDF check reproduces the reviewed crop pixels. The separate attestation check pins the historical PDF bytes and confirms the actual printed-page text.

Published-key and earlier source-review credits are retained in the inputs. This is a conditional lexical edition with exact source compatibility and independent historical name vocabulary, not a claim of uniquely forced historical wording.
