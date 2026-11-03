# November 9: a crown airlift request and an urgent embassy address

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

[Read the source edition](../../cases/finance/nov9_crown_airlift_and_embassy.md).

Four physical records on Childs p167 contain **624 source slots** and **312
plaintext positions**. The unchanged published Nov7–9 key fixes **311 raw
positions**. The proposals use **1 observed-coordinate substitution** and
**1 source-mask fill**, with no insertion, exclusion, reordering or key
change.

B1–B3 form a complete request for thirty million crowns for pay and
purchases in Hungary, transported by giant aircraft to Brasso, with large
and small banknotes. The transmitted `VORAT`, `4A` and `41942` remain
literal. B2's final source-visible `DX` corrects an OCR omission; B3's
following `NKJ DD` is source control, with the earlier OCR's mistaken
inclusion of `DD` retained in the comparison artifact.

E1 is a separate complete address/urgency/signature part naming the German
embassy at Constantinople and Stumm. An enlarged source inspection resolves
`XGGVX` as five valid coordinates; no fill is needed. Its advertised second
part is absent from this section and no substantive body is invented.

```sh
python experiments/nov9_crown_airlift_and_embassy/verify.py --verify
python experiments/nov9_crown_airlift_and_embassy/verify.py --verify --pdf /path/to/childs.pdf
```

`inputs.json` preserves the literal groups, headers, published key and
readable proposals. `certificates.json` verifies each raw domain, both priced
changes, complete readable-label preservation and exact re-encryption.
The two `sources/` crops are bound by file and pixel hashes; the optional
PDF check reproduces them from the identified original. Earlier OCR and
explicitly recomputed comparison outputs remain in `ocr_snapshot.json`
and `prior_candidates.json`. `catalog_proposal.json` lists the four new
physical records.

The direct reading of the amount is spelled-out language, not an assigned
numerical label. A request and contemporary shortage report do not establish
that delivery occurred. Published-key and earlier repository credits remain
separate from this source review; no universal first-decipherment priority
is asserted.

**Source-evidence delivery.** This text-only edition links the original public PDF and retains its page/crop coordinates, dimensions and pixel hashes. No new scan-image file is distributed. The default verifier checks the text and arithmetic; source pixels are checked only when the original PDF is supplied with `--pdf`.
