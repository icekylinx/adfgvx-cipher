# September radio instructions: Tiflis routing and key destruction

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Four newly reviewed physical parts contain **798 source slots / 399 plaintext
positions**. Their native lengths match the printed RICHI/RIZI numbers. The
unchanged Sep19–21 key fixes **389 raw positions**. Baseline edited proposals
fix **398/399 positions** with **10 observed-coordinate substitutions** and
**9 printed-mask fills**, without inserting or deleting coordinates.

The [p57 three-part routing order](../../pages/057.md#edition-cases-radio-september-tiflis-radio-routing)
becomes readable when the original part boundaries are restored from the
scan. It concerns direct blind transmissions to Tiflis, reception of NKJ
and ASO by COS, rapid forwarding and advance notice of traffic. A visible D
above a typed A directly supports the one-coordinate correction supplying
ANKUENDIGEN. Repeated call signs and all reference digits remain literal.

The [p61 key-destruction instruction](../../pages/061.md#edition-cases-radio-september-key-destruction-order)
retains a masked first label 77?77 and a direct second 77777. One conditional
repetition fill is separately priced and excluded from the baseline totals.
The proposed HIER/SOFORT/ZU VERNICHTEN restorations are exact compatible
editorial readings, without a corroborating second copy or a claim that
the instructed destruction occurred.

`inputs.json` preserves source rows, headers, the unchanged published key,
annotation geometry and five crop bindings. `certificates.json` independently
checks the transposition, every pair domain, all repairs, the annotated D,
the optional number completion and complete readable-quote mappings. The
prior unreviewed OCR screens are frozen with cache hashes and retained
attribution; this work makes no external first-solution claim.

## Reproduce

```sh
python experiments/september_radio_instructions/verify.py --verify
python experiments/september_radio_instructions/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The PDF option checks the original byte count and SHA-256 and regenerates
all five crops for exact pixel comparison. It requires PyMuPDF and Pillow;
the normal verification uses checked-in code and the standard library.
