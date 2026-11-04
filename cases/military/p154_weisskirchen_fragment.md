# p154 A2 — Weisskirchen halt and security fragment

[All cases](../README.md) · [ADFGVX Cipher](../../README.md) · [Reading conventions](../../docs/reading-conventions.md)

**Recovery and review: icekylinx and GPT-6 Astra Pro, 4 November 2026.**
A newly reviewed frame recovers the phrases **Weisskirchen angehalten** and
**Sicherungen an den** from the previously unframed second part. The unchanged
published November 4–6 key fixes **36/81 raw positions**; a separately priced
word layer fixes **56/81**. The preceding passage remains incomplete.

## Reading

**Readable German — excerpts from the explicitly repaired word layer; absent passages remain omitted:**

> […] Weisskirchen angehalten. […] Sicherungen an den […]

**Meaning:** The surviving phrases mention a halt involving Weisskirchen and
security arrangements at locations whose description is incomplete. They do
not identify who was halted or establish the missing geographical endpoints.
The opening `21` is retained as an uninterpreted square-label field.

## Source and frame

Childs, printed p154 / PDF p157, gives `A) UKS v ZON (11.55 p.m., November 7th); 2 TL; RICHI-162`.
The [other message on the same page](airfield_german_troop_fragment.md) also
uses the November 4–6 key successfully. The two records have different station
directions and times; they are not joined as parts of one report.

<details>
<summary>Literal source transcription</summary>

**Source transcription — all 118 observed coordinates, including the six-character group VDFDVD:**

```text
FXFXF AADVX XDDAV DFGXX DAAXV VDFDVD XXFVA
DAFXA FGVFV AFXFV XXVDV XVAXV DVVVG XXFAD
DVDXF AFXXA FAGFV VFXFF GGVFA XGXVF GAFAA
AFVGX ADGVA VF
```

</details>

The source contains 118 observed coordinates and no printed masks, against
its advertised 162. The primary frame makes two explicit assumptions:

1. Exclude the `D` at zero-based source index 28, the fourth character of
   `VDFDVD`, leaving the five-coordinate group `VDFVD` in the analysis stream.
2. Prepend 45 unknown transmitted slots to the remaining 117 observations.

The literal source is unchanged. One observed coordinate is excluded; all
other 117 observations retain their values and relative order. The source
prints no 45-coordinate gap. This frame reconciles the six-character group
and header length, but does not establish how the text was historically lost.

## Raw and edited output

<details>
<summary>Source and cipher evidence</summary>

**Raw output — conditional 162-slot frame and unchanged key; 36/81 fixed positions; one excluded observation, no coordinate substitutions or fills:**

```text
21??X??B?I?A??B??AR??X??R?G?R??U??ED??W??S?K?R??E??NG??A??E?X?T??HE?UN??N?ND?N?U?
```

**Edited output — the same frame; 2 observed-coordinate substitutions and 20 inserted-slot fills; 56/81 fixed positions:**

```text
21??X??B?I?A??B??AR??X??R?G?R??U??ED??WEISSKIRCHENANGEHALTENX?SICHERUNGENANDEN?U?
```

</details>

| Proposed fragment | Zero-based plaintext start | Observed substitutions | Added-slot fills |
|---|---:|---:|---:|
| WEISSKIRCHENANGEHALTEN | 38 | source 94 `F→V` | 13 |
| SICHERUNGENANDEN | 62 | source 106 `A→G` | 7 |

The excluded source 28 `D` is separate from these two substitutions. Each of
the 20 newly fixed word positions has one observed half-coordinate; none is
wholly unobserved. Twenty-five plaintext positions remain unresolved. No
opening word, numeral value, intervening heading or final destination is
supplied from context.

An independent contemporary spelling witness appears in the U.S. War
Department's *Histories of Two Hundred and Fifty-One Divisions of the German
Army* (compiled in 1919, published in 1920), Alpine Corps history, printed p10.
It records **Weisskirchen** in a 1915 movement narrative. This supports the
name's spelling, not this telegram's unit, event or unique geographical
identification; [source metadata](../../experiments/p154_weisskirchen_fragment/historical_context.json)
keeps the distinction explicit.

## Search and review

The discovery tested each of the six characters in `VDFDVD` as the surplus
coordinate, with a single 45-coordinate loss at every shortened-stream boundary:
**708 models**. The primary ranked first in that family. Three fresh controls
gave planted-frame ranks 5, 1, 1; the first control's leader shifted the gap by one
position and produced one wrong fixed letter. The other two recovered the
correct fixed text. Exact loss placement remains conditional.

The [replay and comparison details](../../experiments/p154_weisskirchen_fragment/README.md)
retain the separate length diagnostic, shuffled controls and more complex
two-gap alternatives. A separate length diagnostic ranked the advertised 162
first. The simpler one-prefix frame remains primary; the incomplete opening
is not filled from language-model suggestions.

[Complete coordinate and edit certificate](../../experiments/p154_weisskirchen_fragment/certificates.json)
· [Search scope, controls and replay](../../experiments/p154_weisskirchen_fragment/README.md).
The source crop is authenticated against the original PDF. Independent column
arithmetic reproduces the raw domains, all repairs and complete re-encryption
witnesses; arbitrary residual witness fills are not historical text.

## Credit

Historical source: J. Rives Childs. Published November 4–6 key: George Lasry,
Ingo Niebel, Nils Kopal and Arno Wacker (2016), and Lasry's 2017 key list.
Source-frame discovery, word review and edition: **icekylinx and GPT-6 Astra Pro**.
