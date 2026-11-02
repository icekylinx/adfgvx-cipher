# Tiflis appointment: source loss and a historical name constraint

**Source edition, recovery and historical comparison: icekylinx and GPT-6 Astra Pro.**

The two unheaded parts at the top of Childs p192 appoint a representative of
the Polish government for Georgia, Armenia and Azerbaijan, based in Tiflis.
Part 3 says the appointment and instructions have already been dispatched
through a person whose damaged name is `T?DE?SKI`. The independently attested
surname **TYDELSKI** supports a conditional recovery of **Nov13–15b FX = Y**.
The geometry is determined first, with both the courier name and the final
signature excluded from its scoring stencil.

See the [readable case](../../cases/other/tiflis_appointment.md),
[literal inputs](inputs.json), and [exact certificate](certificates.json).

## Separate evidence layers

| Layer | Evidence and result |
|---|---|
| Source frame | Part 2 has 230/230 coordinates. Part 3 has 227 valid coordinates against RICHI-232. |
| Missing-group geometry | All 228 boundaries are tested for one five-coordinate gap. Excluding all eight courier-name letters and all seven signature letters, gap 150 is the unique minimum with one observed-coordinate change. |
| Ordinary-word repair | Four of the five missing coordinates are supplied by ordinary words; correcting E to T in TIFLIS gives 114/116 fixed positions in part 3, retaining `T?DE?SKI`. |
| Historical name | The independent TYDELSKI identification fills the missing L half-coordinate and assigns the unchanged observed FX pair to Y. The complete 116-letter candidate reencrypts exactly. |

The last layer is an explicit historical identification assumption. It does
not modify the published key. Reencryption alone also permits seven other
unused symbols at FX; the certificate checks every one.

Across both records there are **457 printed coordinate letters**, a declared
462-coordinate frame after the missing group, and **225/231 fixed raw
positions** before repairs. The ordinary-word layer raises this to 229/231;
the conditional name layer reaches 231/231. Fixed raw totals include garbles,
and the exact country-name spelling is kept separately from its interpretation.

## Consequences kept visible

Direct FX=Y affects two complete pairs in this package and the November 14
source edition: p192 part 3 position 61 and p190 A position 37. The latter's
name becomes `FRYE`. Transferring Y to Nov13–15a DG additionally requires the
same-correctly-copied-name assumption for the p190 A / p194 B pilot notices.
That transfer affects p194 B and its exact interrupted suffix p193 B.

The certificate lists the complete before/after raw texts, every newly fixed
raw position and every changed marginal domain. Its inventory covers all
nine source records in these two packages. Other records are outside this
local inventory; no claim of corpus-wide consistency is made here.

## Reproduction

```sh
python experiments/tiflis_appointment/verify.py --verify
python experiments/tiflis_appointment/verify.py --verify \
  --pdf /path/to/childs.pdf \
  --historical-pdf /path/to/madzik_poland_georgia.pdf
```

The standard verification uses only Python's standard library. Optional PDF
checks use PyMuPDF and Pillow to verify document hashes and byte counts,
rerender every saved crop for pixel equality, and check the short historical
name quotation against the research PDF. Every source map, repair operation,
gap-search minimum, conditional reencryption and local key-layer effect is
independently recomputed.
