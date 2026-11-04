# November 6 notice: Osmanie unavailable

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The [p138 C edition](../../cases/pages/138.md#edition-cases-radio-nov6-marine-service-notice-completed-reading)
now reads **KIEW** and **OSMANIE**. Both names have independent native-source
witnesses: p110 B closes with `HRG KIEW`; p77 B names `FUNKERABTLG OSMANIE`.
The new letters fill source masks 44 and 146 without changing an observed
coordinate. The completed proposal has 143 fixed labels. A separately priced `HZYU` →
`H X QU` address proposal uses two more observed substitutions, supported by
raw `HXQU` spans in p102 B1 and p86 A.

| Layer | Fixed positions | Observed substitutions | Source-mask fills | Added-slot fills |
| --- | ---: | ---: | ---: | ---: |
| Native 286-slot source | 136/143 | 0 | 0 | 0 |
| Conditional frame, before word repairs | 136/143 | 0 | 0 | 0 |
| Earlier word layer | 141/143 | 3 | 4 | 1 |
| Completed names | 143/143 | 3 | 6 | 1 |
| Optional headquarters address | 143/143 | 5 | 6 | 1 |

The conditional frame excludes one ambiguous masked stroke and adds one
final coordinate. The source does not visibly establish either operation.
The new names are contextual choices within six-symbol native domains;
[the completion record](label_completion.json) separates them from the
unchanged native and earlier word layers in [the inputs](inputs.json).

## Reproduce

```sh
python experiments/nov6_marine_service_notice/verify.py --verify
python experiments/nov6_marine_service_notice/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The verifier rebuilds the four source/name layers and the optional address,
checks the observed name and abbreviation spans in their independent donors,
prices the original 286 single-gap alignments and checks the live readings. The conditional complete stream re-encrypts
exactly under the published Nov4–6 key.

The two reviewed source crops are included:
[p138_C_reviewed.png](sources/p138_C_reviewed.png) and
[p138_stroke_detail.png](sources/p138_stroke_detail.png).
The default command verifies their PNG bytes and RGB hashes. With `--pdf`,
it also checks the pinned scan and compares both crops with the rendered
source pixels.

Childs supplies the historical collection. The period key and earlier
cryptanalytic work retain the credit of Lasry, Niebel, Kopal and Wacker;
the previous repository readings remain in [prior candidates](prior_candidates.json).
