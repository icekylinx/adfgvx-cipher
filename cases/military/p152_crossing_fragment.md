# p152 A2 — Proposed report on crossing attempts

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source review and partial word edition: icekylinx and GPT-6 Astra Pro.** The unchanged 128-slot frame gives 61/64 fixed native labels. Seven observed-coordinate substitutions and two printed-mask fills give a proposed 63/64-position reading about crossing attempts. The negative KEINE is part of that proposed repair, not a native source-fixed statement.

## p152 A2

**Readable German — conditional word edition; name and complete footer retained literally:**

> Bis VARC8IORO?A keine Uebergangsversuche. A O0Q 17 ROED 1Q NR V054.

The proposed wording means that no crossing attempts are reported as far as the place encoded VARC8IORO?A. Its 8 and unresolved position remain literal. The entire closing field A O0Q 17 ROED 1Q NR V054 is retained, without changing it to a familiar headquarters signature or historical numeral.

**Source transcription — all 128 printed slots, including E and two dashes:**

```text
GEAFD AFFVX VVGAF AADVF DADVF FAVDX DAAXD GAVGF
DFDFD VXA-- DDGVA FXAFF DAFAV FVXGG XXDGF GGGXF
AAAXV AVGGA FFVGF DFDXV AVGFD DXFVA FAVFA FGFAG
VDVVD AFD
```

**Raw output — unchanged Nov4–6 key, native order and length:**

```text
BIHVARC8IORO?AK1ILEPEVERG?NGVXERSU?HEXXAXO0QX17XROEDX1QXNRXV054X
```

**Edited output — seven observed substitutions and two printed-mask fills; native frame and opaque name retained:**

```text
BISVARC8IORO?AKEINEUEBERGANGSVERSUCHEXXAXO0QX17XROEDX1QXNRXV054X
```

The changed observed source indices are 15, 31, 39, 40, 47, 78 and 79. The two printed dashes at 48–49 are filled. Printed E at source 1 remains an unresolved coordinate; it produces one of {2,3,B,H,S,V} at name position 12. All six complete re-encryption witnesses remain in the certificate.

## Place spelling: separately priced alternatives

An independent 1896 primary source prints **VERCSIOROVA**, supplying a rare CS spelling for comparison with the opaque place label. The inspected National Széchényi Library scan is *Természettudományi Közlöny*, printed p159 / PDF p6, a report of the botanical section's January 8 meeting. Its short locality statement reads “1885-ben pedig Vercsiorova alatt szedte.” The Romanian National History Museum also catalogues a 1901–1915 postcard under Verciorova, inventory 385510.

The 1896 source supports the place-name comparison; it does not attest the exact A-vowel spelling VARCSIOROVA or the proposed telegram's negative statement. The two alternatives below therefore keep their own complete coordinate prices.

**Edited output — optional VARCSIOROVA spelling; nine total observed substitutions and three total mask fills:**

```text
BISVARCSIOROVAKEINEUEBERGANGSVERSUCHEXXAXO0QX17XROEDX1QXNRXV054X
```

**Edited output — optional attested VERCSIOROVA spelling; eleven total observed substitutions and three total mask fills:**

```text
BISVERCSIOROVAKEINEUEBERGANGSVERSUCHEXXAXO0QX17XROEDX1QXNRXV054X
```

Supplying S for literal 8 and V for the masked name position adds two observed substitutions and one mask fill to the primary reading. Changing VARCSIOROVA to the independently attested VERCSIOROVA costs two further observed substitutions. The primary edition leaves both normalizations unselected.

[1896 primary scan, p6](https://epa.oszk.hu/02100/02181/00319/pdf/EPA02181_Termeszettudomanyi_kozlony_1896_154-160.pdf#page=6) · [MNIR postcard inventory 385510](https://imagoromaniae.ro/produs/gara-in-verciorova/) · [Attestation metadata](../../experiments/p152_crossing_fragment/place_attestation.json).

## Source and credit

Childs printed p152 / PDF p155, section A2, RICHI-128. Literal header: `A) UKS v ZON (--- November 7th); 2 TL; RICHI-128`. A first part is not supplied by this edition.

[Original Childs scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view) · [Source package](../../experiments/p152_crossing_fragment/README.md) · [Exact certificate](../../experiments/p152_crossing_fragment/certificates.json).

The period key retains the Lasry-team credit. Earlier source inspection and unchanged-key outputs are prior work. The present contribution is an explicitly priced partial word edition, preserving its uncertain place label, raw footer and complete source, with an independently inspected historical place-spelling comparison.

## Reproduce

```sh
python experiments/p152_crossing_fragment/verify.py --verify
python experiments/p152_crossing_fragment/verify.py --verify --pdf /path/to/childs.pdf
python experiments/p152_crossing_fragment/verify.py --verify --attestation-pdf /path/to/EPA02181_Termeszettudomanyi_kozlony_1896_154-160.pdf
```
