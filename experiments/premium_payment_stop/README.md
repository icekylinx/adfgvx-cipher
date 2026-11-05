# End-of-October premium-payment order

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

The two source-labeled parts on Childs p78, PDF page 81, have native lengths
**240** and **170**. The message is dated `29/10 0940`; the receiving
header is 31 October. Both parts decode directly under the unchanged
published **Oct28–31** key. No coordinate substitution, fill, insertion,
deletion, length repair or key change is needed.

The [reading case](../../pages/078.md#edition-cases-finance-premium-payment-stop) gives the
complete raw and identical edited streams, followed by spaced German.
The order says to stop all premium payments `AUSLANDESMITTELN` with
`ABLAUFOKTOBER18`, and immediately inform every subordinate office.
The reading separates **aus Landesmitteln**; it does not silently change
the spelling to **Auslandsmitteln**. All references are literal. An order
is evidence of the instruction, not of its implementation.

## Frozen evidence

`inputs.json` holds literal rows, the complete key with provenance,
headers, crop geometry and hashes. `certificates.json` independently
reconstructs the transposition map, every coordinate pair and every fixed
plaintext position. Both unchanged streams re-encrypt to the exact visible
ciphertext. There are **410 / 410 valid coordinates** and **205 / 205 fixed
plaintext positions** in two physical records.

`prior_candidates.json` preserves the earlier exact unreviewed repository
body candidates and a bounded paper/thesis/comment keyword check. This is
a source-audited edition of those candidates, not a first-solution claim.
`catalog_proposal.json` contains only these two physical records.

## Reproduce

From the repository root:

```sh
python experiments/premium_payment_stop/verify.py --verify
```

This uses the standard library and the checked-in cipher module. To
verify both crops against the original PDF as well, install PyMuPDF and
Pillow and supply the PDF path:

```sh
python experiments/premium_payment_stop/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The byte count and SHA-256 are checked before both source crops are
regenerated and compared pixel for pixel. Scratch caches are not runtime
dependencies.
