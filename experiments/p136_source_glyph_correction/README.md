# A source glyph restores ZU DORT in the Gokieloff record

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

The fifth group in the fourth ciphertext row of p136 A1 reads **XAFFF**, not the
previous repository transcription **XAFFX**. Two independent inspections of the
pinned Childs PDF resolve the last letter as F: its vertical stem and horizontal
bars are visible beside the different X forms. Correcting source position 144
changes just plaintext position 2 from P to D. The raw opening is therefore
**ZUDORTPAT487LEO**, displayed as **Zu dort PAT487 Leo**.

The [current edition](../../cases/pages/136.md#edition-cases-people-gokieloff-return-payment-stop) includes
this correction. PAT487 remains a literal reference; the repeated Gokieloff name,
CZENNTOCHAU spelling, numbers, unknown Q-derived position and all other labels
retain their earlier interpretation limits. This is a correction to our source
transcription, with **zero additional historical substitution cost**. The four
previously proposed observed-coordinate changes and one source-mask fill are
unchanged. No new physical record or fixed-position gain is claimed.

## Exact before and after

The [audit input](inputs.json) names the single source change. The complete
previous input, certificate and case are preserved under `before/`, with their
original SHA-256 values. The [new certificate](certificates.json) binds both raw
streams and proves that the proposed ciphertexts differ at exactly that same
source position. The other printed part, p136 A2, is unchanged byte for byte as a
record and certificate object.

The existing [source excerpt](../gokieloff_return_payment_stop/sources/p136_A1.png)
contains the corrected group. No new image asset is needed for this review.
The original Childs source is printed p136, PDF page 139. Its published Nov4–6
key and the earlier authors' credit remain unchanged.

## Reproduce

```sh
python experiments/p136_source_glyph_correction/verify.py --verify
python experiments/p136_source_glyph_correction/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
python experiments/gokieloff_return_payment_stop/verify.py --verify
```

The correction verifier reconstructs the ragged column grid independently,
compares every source and output position, re-encrypts both complete proposals,
and binds the live readable display. The optional PDF check reproduces the
pixels of the existing source excerpt. Pixel identity establishes location and
provenance; the explicitly documented visual inspection establishes this glyph.
