# November 6 marine-service notice, with an unresolved station label

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

A conditional reading of Childs p138 section C reports **O?MANIE** as
unavailable and asks that all stations be informed. Its address-like opening
names the Seekriegsleitung, Admiral Berlin and other recipients, while
**HZYU**, **KIE?** and **O?MANIE** remain literal. The edition does not supply
the missing place or station letters or infer the reason for the failure.

The source includes a narrow extra stroke immediately before `VAADA`.
Counting that visible mark as one masked slot gives **286 source slots**,
matching `RICHI-286`. The native reading is preserved below. The clearer
proposal explicitly **excludes that one masked mark and inserts one unknown
slot at the end**. This is a conditional frame, with a stronger assumption
than simply restoring a visibly missing printed group.

In that declared frame the **143 plaintext positions** have **136 fixed
raw** and **141 fixed edited**. The ordinary-word proposal needs **3
observed-coordinate substitutions, 4 retained source-mask fills and 1
inserted-slot fill**, in addition to the separate masked-mark exclusion.
The published **Nov4–6** key and the order of every retained source slot are
unchanged.


**Reviewed source crops:** [p138_C_reviewed.png](../../experiments/nov6_marine_service_notice/sources/p138_C_reviewed.png) · [p138_stroke_detail.png](../../experiments/nov6_marine_service_notice/sources/p138_stroke_detail.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## p138 C

[Complete reviewed crop — source-PDF reference](../../experiments/nov6_marine_service_notice/inputs.json)
and [high-resolution stroke detail — source-PDF reference](../../experiments/nov6_marine_service_notice/inputs.json).

**Source transcription — headers and cleartext ending:**

```text
6th November 1918.
C) UKS RAT v NKJ (10.32 p.m., November 6th, 1918.)
10.15 6/11 VON ASO KR
RICHI-286
Cleartext ending: B M K - UKS RAT v NKJ UM
```

The final `B M K - UKS RAT v NKJ UM` is a cleartext annotation after the
ciphertext. It is not absorbed into the coordinate stream. The complete
[source transcription](../../experiments/nov6_marine_service_notice/inputs.json)
retains the three invalid `W` glyphs, the invalid `C`, both invalid `O`
glyphs and the additional narrow stroke.

### Native frame including the stroke

The narrow stroke is conservatively transcribed as **`|` at source index
225**, between `FADFF` and `VAADA`. This token identifies a visible mark;
it is not a claim that the historical character was a pipe or a valid
coordinate. Including it gives **286 slots**, **279 valid coordinates** and
**7 masked marks**.

**Raw output — native 286-slot frame including the stroke; 136/143 fixed positions:**

```text
SEEM??OGSLEATUMG?ROSSESCFZYU9XADM6RAL2ER9GNXXUAC1CSE?XCDEYTSCBKXM8RLNEV1RTEZ?NWWEEGE2G8U6PE79IE?XXO?MKNREDUSYZFANF1NZALLESTRLPENB1NAC1RLCWTNGE6
```

This remains the source-preserving baseline. Its partly recognizable text
is not silently presented as the clearer proposal.

### Conditional frame and word repairs

The proposed frame omits only the masked stroke at **original source 225**
and adds one unknown after the final source slot, at **original source
boundary 286**. The resulting model still has **286 slots**. The added slot
has **model index 285** because one earlier source mark was excluded.

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

The abbreviation-like forms **Nachchef** and **Marinevertr** remain as
encoded after the stated repairs. The `1` in raw `AUSGEFALL1N` becomes E
through an explicit observed-coordinate change; the published square is
not relabeled. The edition preserves **HZYU**, **KIE?** and **O?MANIE**
without modernizing, identifying or completing them.

**Meaning:** The proposed message reports the named but incompletely read
entity as unavailable and requests that all stations be notified. It does
not establish the cause, duration or consequences of the failure, identify
an individual recipient, or verify that the notification occurred.

## Separate frame and coordinate costs

All source indices below refer to the full 286-slot transcription, including
the narrow stroke.

| Operation | Source position | Result |
| --- | ---: | --- |
| Exclude ambiguous masked mark | 225 | The visible stroke stays in the literal source and is omitted only in the conditional model |
| Add unknown slot | Boundary 286 | Added model slot 285, later filled with V |
| Observed-coordinate substitution | 13 A→F | E in AUSGEFALLEN |
| Observed-coordinate substitution | 98 V→F | E in STELLEN |
| Observed-coordinate substitution | 174 D→X | N in NACHCHEF |
| Invalid W fill | 18 W→V | G in GROSSES |
| Invalid W fill | 84 W→V | R in SEEKRIEGSLEITUNG |
| Invalid W fill | 110 W→V | U in UND |
| Invalid O fill | 135 O→X | I in SEEKRIEGSLEITUNG |
| Added-slot fill | Model 285 →V | I in BENACHRICHTIGEN |

The two remaining active source masks are left unresolved. A complete
re-encryption witness mechanically supplies their values and is explicitly
marked **nonhistorical**; it does not identify KIE? or O?MANIE. No observed
coordinate is discarded, and no source group is reordered.

## What the gap comparison establishes

After the stroke exclusion, the retained stream has **285 slots**. The
verifier encrypts the fixed partial candidate, treating its two `?` labels
as unconstrained pairs, and prices **all 286 single-gap alignments**. The
unique minimum within this family is an added slot at the end, requiring
three changes to observed coordinates.

| Gap boundary in retained 285-slot stream | Observed substitutions |
| ---: | ---: |
| 280 | 6 |
| 281 | 5 |
| 282 | 4 |
| 283 | 4 |
| 284 | 4 |
| 285, at the end | 3 |

The complete vector of all 286 prices is in the certificate. This comparison
is conditional on **both** the stroke exclusion and the selected body
proposal. It does not establish that the stroke was extraneous, that a
coordinate was historically lost at the end, or that every other possible
plaintext has been excluded. The scan shows neither a cancellation through
the stroke nor a blank proving a final omission. Both source and model
remain available for a different interpretation.

## Source restoration, attribution and reproduction

Earlier repository OCR contained **279 slots**: it omitted the final
`FVAAA`, omitted the invalid W after `VXVX`, and did not record the narrow
stroke. Restoring these actual source observations is distinct from the
conditional exclusion and insertion above. The earlier input and its
recomputed unchanged-key output are preserved in
[prior candidates](../../experiments/nov6_marine_service_notice/prior_candidates.json).

The historical source is J. Rives Childs's scan. Published period-key work
by George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker, Lasry's 2017 key
list, and earlier repository work retain their separate credit. This is a
conditional source edition and explicit word restoration; **no
first-decipherment claim** is made.

[Inputs](../../experiments/nov6_marine_service_notice/inputs.json),
[certificates](../../experiments/nov6_marine_service_notice/certificates.json),
and [reproduction instructions](../../experiments/nov6_marine_service_notice/README.md)
preserve the native frame, both source images, exact conditional source
mapping, all repair events, every gap price and live-display checks.
