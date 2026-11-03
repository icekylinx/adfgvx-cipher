# Eilvese, setup, boat-sale and director-departure source records

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

Four new physical records preserve **887 source slots** and **875 valid
coordinates**. Their stated frames total **886 slots / 443 plaintext
positions**, with **432 fixed raw positions**. The baseline edited proposals
fix **441/443 positions**, with **17 observed-coordinate substitutions** and
**9 printed-mask fills**. No key change or numeral relabeling is made.

The [Eilvese and setup edition](../../cases/radio/nov4_eilvese_and_setup.md)
preserves a six-slot overprinted group XXFTVA in p120 A: there are 237 source
slots against RICHI-236. A conditional exclusion of the T-like masked slot
retains every valid coordinate. All six local single-exclusion cost vectors
are retained; the scan alone does not prove cancellation intent. The
short p120 C notice has no source mask or added slot, and its location-like
label remains literal.

The [boat-sale order](../../cases/naval/motorboat_sale_attempt.md) repairs two
words but retains the raw identifier Q5, refusing to inherit the OCR 35.
The [director-departure inquiry](../../cases/people/director_departure_query.md)
keeps T4SCHASCHEL and 027 in its baseline and retains two unresolved closing
reference positions. A separate optional TISCHASCHEL interpretation costs
two additional coordinate substitutions and is not counted in the baseline.

`inputs.json` holds literal rows, all headers, the unchanged Nov4–6 key,
source counts and five crop bindings. `certificates.json` contains independent
transposition and coordinate-pair checks, exact repairs, all local exclusion
prices and the optional name witness. Complete readable quotes preserve all
nonseparator labels; their two editorial question marks are explicitly
distinguished from the two unresolved decoded positions.

The earlier unreviewed repository candidates and published key retain their
credits. Lexical restoration and exact compatibility do not independently
establish every proposed historical word or a completed action.

## Reproduce

```sh
python experiments/nov4_radio_and_departure_queries/verify.py --verify
python experiments/nov4_radio_and_departure_queries/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The optional PDF check verifies its pinned byte count and SHA-256 and
regenerates all five crops for pixel comparison. It requires PyMuPDF and
Pillow; the normal check uses only checked-in modules and the standard
library. No scratch cache is needed.
