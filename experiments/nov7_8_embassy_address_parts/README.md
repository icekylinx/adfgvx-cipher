# 7–8 November: embassy, legation and Etappe address parts

Research and editorial work: **icekylinx and GPT-6 Astra Pro**.

[Read the source edition](../../pages/156.md#edition-cases-radio-nov7-8-embassy-address-parts).

Seven native records contain **568 source coordinates / 284 plaintext
positions**, all fixed under the primary overstrike transcription.
Ordinary-word proposals cost **11 observed-coordinate substitutions**, with
no source-mask fills, insertion, deletion, reordering or key change. A
retained p156 A1 V/X overstrike alternative changes one raw plaintext letter
and raises the aggregate proposal cost to 12 substitutions. Both costs are
recomputed explicitly.

The faint p156 A1 header part count is retained as explicit 2/3 alternatives,
independent of its clear 84-coordinate body length.

These are address/signature parts, including the native French designation
`LEGATION ALLEMANDE`, the literal spelling `KONSTANTIOPEL`, and the
unexpanded `UPK3` prefix. Advertised absent parts are not reconstructed.

The existing p162 D1 source witness independently supports all four p158 A1
and both p158 A2 edited letters. The two new raw witnesses supply labels at
its three masks. The verifier compares actual raw outputs and records all
agreements and disagreements. Different headers, p158 A2's prefix and
separator difference remain explicit; a whole-message copy claim is not
made, and the earlier p162 record is not counted again.

```sh
python experiments/nov7_8_embassy_address_parts/verify.py --verify
python experiments/nov7_8_embassy_address_parts/verify.py --verify --pdf /path/to/childs.pdf
```

The PDF check pins the original scan hash and exactly reproduces RGB pixels
for the two new crops and existing p162 witness crop. `inputs.json` contains
the manual rows, headers, keys, variant and word proposals.
`certificates.json` contains every raw position, repair, variant ledger,
parallel support item and exact round-trip. `prior_candidates.json` and
`ocr_snapshot.json` preserve the earlier OCR and explicitly recomputed
comparisons. `catalog_proposal.json` lists seven new physical records for
integration. Published-key credit remains with Lasry, Niebel, Kopal and
Wacker; no universal first-decipherment priority is claimed.

**Reviewed source crops:** [p156_reviewed.png](sources/p156_reviewed.png) · [p158_reviewed.png](sources/p158_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
