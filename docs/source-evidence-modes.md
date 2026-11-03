# Source-evidence verification modes

Prepared by **icekylinx and GPT-6 Astra Pro**.

`adfgvx.source_evidence.verify_source_evidence(pdf, source, crops, base)` checks
source-image evidence and returns an explicit report of the checks it actually
performed. It reads evidence only and does not create, download, or upload files.

| Crop storage | Without the original PDF | With the original PDF |
|---|---|---|
| `embedded_png` (default) | Requires the local PNG, its exact file SHA-256, dimensions, and decoded RGB SHA-256. Its derivation from the PDF remains unchecked. | Performs the local checks, verifies the PDF byte count and SHA-256, then requires the rendered crop to match the RGB digest and the local PNG pixels. |
| `external_pdf_reference` | Retains a source-page/crop reference and expected digests. It opens no PNG and verifies no source pixels. | Requires the original PDF byte count and SHA-256, renders the declared crop, and verifies its dimensions and RGB digest. No PNG is required or opened. |

External mode can retain an old `path` as provenance metadata, use `reference` or
`id`, or omit all three. In the last case the report generates a descriptive
`pdf:<page>:crop:<rectangle>` label. That label is never treated as a local file.
The report separates expected digests from actual computed digests; actual values
stay `null` when that evidence was not read.

The source mapping requires `pdf_bytes` and `pdf_sha256` (aliases: `bytes` and
`sha256`). Every crop requires `pdf_page_1based`, a rectangle, a positive scale,
`width`, `height`, and an RGB digest. `channels` defaults to three. Embedded mode
also requires `path` and a PNG file digest.

| Field | Accepted names |
|---|---|
| Rectangle in PDF points | `crop_pdf_points`, `clip_points`, `crop_rectangle_pdf_points`, `clip_pdf_points` |
| Scale | `render_scale`, `scale` |
| PNG file SHA-256 | `sha256`, `png_sha256` |
| RGB pixel SHA-256 | `rgb_sha256`, `rgb_pixel_sha256` |

Conflicting aliases, unknown storage modes, missing required metadata, missing
embedded PNGs, and byte/pixel mismatches raise `SourceEvidenceError`. A failed
required check never silently switches to external-reference mode. If the crop
recipe declares `fresh_render_cache: true`, the helper clears the MuPDF store
immediately before rendering, matching that recorded rendering condition.

```python
from adfgvx.source_evidence import verify_source_evidence

report = verify_source_evidence(pdf_path_or_none, source_metadata, crops, package_dir)
print(report["summary"])
```

The report is runtime-dependent: passing the PDF changes which checks were
performed. It should remain separate from a deterministic cryptanalytic
certificate unless the verified mode is intentionally part of that artifact.
The report confirms file and pixel evidence, not a transcription, cipher key,
word repair, or historical interpretation.

The isolated mode and failure tests use a temporary generated PDF:

```bash
python -m unittest discover -s tests -p test_source_evidence.py -v
```
