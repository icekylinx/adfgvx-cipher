# Osmanie unavailable: the November 6 marine-service notice

[Catalogue](../README.md) · [Reading conventions](../../docs/reading-conventions.md)

The telegram reports **Osmanie unavailable** and asks that all stations be
notified. Two source-mask fills complete the names **KIEW** and **OSMANIE**:
earlier telegrams independently supply both spellings from fully observed
coordinate pairs. Heeresgruppe Kiew appears among the recipients; the
literal address label **HZYU** has a separately priced **H. Qu.** proposal below.

## Completed reading

**Readable German — complete conditional reading with the two name fills:**

> Seekriegsleitung. Grosses HZYU. Admiral Berlin. Nachchef. Deutsche Marinevertr und Heeresgruppe Kiew. Osmanie ausgefallen. Alle Stellen benachrichtigen.

The reading has **143/143 fixed labels** in the existing conditional frame.
It requires **3 observed-coordinate substitutions, 6 source-mask fills and
1 added-slot fill**. The new name readings account for two of the source
fills and require no further change to an observed coordinate.

The frame treats a narrow stroke before `VAADA` as an extra mark and supplies
one coordinate at the end. These two assumptions remain necessary: the
native transcription and its different decoding are preserved below.

<details>
<summary>Completed stream and the two new mask values</summary>

**Edited output — completed conditional stream; 3 observed substitutions, 6 source-mask fills and 1 added-slot fill:**

```text
SEEKRIEGSLEITUNGGROSSESXHZYUXXADMIRALBERLINXXNACHCHEFXXDEUTSCHEXMARINEVERTRXUNDHEERESGRUPPEXKIEWXXOSMANIEAUSGEFALLENXALLESTELLENBENACHRICHTIGEN
```

All indices are zero-based and refer to the original 286-slot transcription.

| Field | Plaintext position | Native pair and domain | Added source fill | Independent name witness |
| --- | ---: | --- | --- | --- |
| `KIE?` → `KIEW` | 95 | `A?`: `17FHLW` | 44: printed `C` → `F` | [p110 B](../military/kiew_morning_and_pioneer_reports.md#p110-b), raw `HRG KIEW` |
| `O?MANIE` → `OSMANIE` | 99 | `?G`: `23BHSV` | 146: printed `O` → `X` | [p77 B](../context/radio_instructions.md#p77-b--call-sign-instruction-for-konia), raw `FUNKERABTLG OSMANIE` |

The witnesses use different period keys. Their complete name pairs are
recomputed in the [certificate](../../experiments/nov6_marine_service_notice/certificates.json);
they support these contextual selections from the native domains. Neither
source is a repeated copy of this notice.

</details>

The abbreviations `Nachchef` and `Marinevertr` are retained. The notice gives
no cause or duration for Osmanie's reported unavailability.

## Optional headquarters address

The address may read **Grosses H. Qu.** (Grosses Hauptquartier). Independent raw telegrams use `HXQU`; applying that abbreviation here changes `GROSSESXHZYUXX` to `GROSSESXHXQUXX`.

The [p102 B1 Orient report](../military/orient_south_slav_reports.md#p102-b1)
contains raw `GD X H X QU`; the [p86 A machine-gun enquiry](../military/mg08_inventory.md)
contains raw `GR X H X QU`. Both abbreviation spans are entirely observed
under earlier period keys. They show usage of the abbreviation, not another
copy of this notice.

| Proposed label change | Pair change | Additional observed substitution |
| --- | --- | --- |
| Position 25: `Z` → separator `X` | `FV` → `FD` | Source 104: `V` → `D` |
| Position 26: `Y` → `Q` | `GV` → `GF` | Source 121: `V` → `F` |

Both printed `V` values are clear observations. This interpretation therefore
costs **two further substitutions**, bringing the complete conditional reading
to **5 observed substitutions, 6 source-mask fills and 1 added-slot fill**.
It supplies a plausible recipient without adding fixed positions: the cheaper
143-label layer above still reads `HZYU`. The original frame alternatives and
all numeric labels are unchanged.

## p138 C

Childs's page is headed 6 November 1918. The reception and origin lines also
give 6 November; the cleartext ending follows the ciphertext.

<details>
<summary>Literal source transcription</summary>

**Source transcription — headers and cleartext ending:**

```text
6th November 1918.
C) UKS RAT v NKJ (10.32 p.m., November 6th, 1918.)
10.15 6/11 VON ASO KR
RICHI-286
Cleartext ending: B M K - UKS RAT v NKJ UM
```

</details>

**Reviewed source crops:** [p138_C_reviewed.png](../../experiments/nov6_marine_service_notice/sources/p138_C_reviewed.png) · [p138_stroke_detail.png](../../experiments/nov6_marine_service_notice/sources/p138_stroke_detail.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).

The [source transcription and crop recipes](../../experiments/nov6_marine_service_notice/inputs.json)
retain the three invalid `W` glyphs, one `C`, two `O` glyphs and the additional
narrow stroke. The cleartext ending is outside the coordinate stream.

### Native frame including the stroke

The narrow stroke is transcribed as `|` at source index 225, between `FADFF`
and `VAADA`. This records a visible mark without identifying it as a cipher
coordinate. Including it gives 286 slots: 279 valid coordinates and 7 masks,
matching the advertised `RICHI-286`.

<details>
<summary>Raw decoded text</summary>

**Raw output — native 286-slot frame including the stroke; 136/143 fixed positions:**

```text
SEEM??OGSLEATUMG?ROSSESCFZYU9XADM6RAL2ER9GNXXUAC1CSE?XCDEYTSCBKXM8RLNEV1RTEZ?NWWEEGE2G8U6PE79IE?XXO?MKNREDUSYZFANF1NZALLESTRLPENB1NAC1RLCWTNGE6
```

</details>

### Conditional frame and word repairs

The conditional model omits the masked stroke at original source 225 and
adds an unknown at original source boundary 286. The added coordinate has
model index 285, so the model retains 286 slots. The earlier word-repair layer
is preserved here with its two name masks still open.

<details>
<summary>Earlier conditional stream and word-repair layer</summary>

**Raw output — conditional stroke exclusion plus final-slot insertion; 136/143 fixed positions:**

```text
SEEK??EGSLEITUNG?ROSSESXHZYUXXADMIRALBERLINXXPACHCHEFXXDEUTSCHEXMARINEVERTRX?NDHEERESGRUPPEXKIE?XXO?MANIEAUSGEFALL1NXALLESTRLLENBENACHR?CHTIGEN
```

**Edited output — the same conditional frame; 3 observed-coordinate substitutions, 4 source-mask fills and 1 inserted-slot fill; 141/143 fixed positions:**

```text
SEEKRIEGSLEITUNGGROSSESXHZYUXXADMIRALBERLINXXNACHCHEFXXDEUTSCHEXMARINEVERTRXUNDHEERESGRUPPEXKIE?XXO?MANIEAUSGEFALLENXALLESTELLENBENACHRICHTIGEN
```

**Readable German — complete conditional edited stream, with unresolved labels retained:**

> Seekriegsleitung. Grosses HZYU. Admiral Berlin. Nachchef. Deutsche Marinevertr und Heeresgruppe KIE?. O?MANIE ausgefallen. Alle Stellen benachrichtigen.

</details>

## Separate frame and coordinate costs

The two new name fills extend the earlier word layer; all other costs are
unchanged. No observed coordinate is excluded or reordered.

| Operation | Source position | Result |
| --- | ---: | --- |
| Exclude ambiguous masked mark | 225 | Omitted only in the conditional model |
| Add unknown slot | Boundary 286 | Added model slot 285, filled with `V` |
| Observed-coordinate substitution | 13 `A`→`F` | `E` in `AUSGEFALLEN` |
| Observed-coordinate substitution | 98 `V`→`F` | `E` in `STELLEN` |
| Observed-coordinate substitution | 174 `D`→`X` | `N` in `NACHCHEF` |
| Invalid `W` fill | 18 `W`→`V` | `G` in `GROSSES` |
| Invalid `W` fill | 84 `W`→`V` | `R` in `SEEKRIEGSLEITUNG` |
| Invalid `W` fill | 110 `W`→`V` | `U` in `UND` |
| Invalid `O` fill | 135 `O`→`X` | `I` in `SEEKRIEGSLEITUNG` |
| Invalid `C` fill, new | 44 `C`→`F` | `W` in `KIEW` |
| Invalid `O` fill, new | 146 `O`→`X` | `S` in `OSMANIE` |
| Added-slot fill | Model 285 →`V` | `I` in `BENACHRICHTIGEN` |

The raw `1` in `AUSGEFALL1N` becomes `E` through the explicit source 13
substitution. The published square is unchanged.

## What the gap comparison establishes

After the stroke exclusion, the retained stream has 285 slots. The original
comparison prices all 286 single-gap alignments against the earlier partial
candidate, with its two unresolved names unconstrained. Adding the slot at
the end is the unique minimum in that family, at 3 observed substitutions.
The [certificate](../../experiments/nov6_marine_service_notice/certificates.json)
retains every price.

| Gap boundary in retained 285-slot stream | Observed substitutions |
| ---: | ---: |
| 280 | 6 |
| 281 | 5 |
| 282 | 4 |
| 283 | 4 |
| 284 | 4 |
| 285, at the end | 3 |

This comparison holds the stroke exclusion and selected body fixed. The
scan shows neither a cancellation through the stroke nor a blank proving a
final omission; other error models and plaintexts remain outside the test.

## Source restoration, attribution and reproduction

Earlier OCR had 279 slots: it omitted the final `FVAAA`, the invalid `W`
after `VXVX`, and the narrow stroke. The [prior-work record](../../experiments/nov6_marine_service_notice/prior_candidates.json)
preserves that input and its unchanged-key output.

Source edition and verification: **icekylinx and GPT-6 Astra Pro**. Childs
supplies the historical collection. The Nov4–6 period key retains the credit
of George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker, with its published
provenance recorded in the inputs.

[Inputs](../../experiments/nov6_marine_service_notice/inputs.json),
[name-completion evidence](../../experiments/nov6_marine_service_notice/label_completion.json),
[certificates](../../experiments/nov6_marine_service_notice/certificates.json),
and [reproduction instructions](../../experiments/nov6_marine_service_notice/README.md)
preserve the native frame, source mapping, earlier word repairs, independent
name witnesses and complete re-encryption of the conditional reading.
