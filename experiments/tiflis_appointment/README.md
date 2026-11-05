# Tiflis appointment: source loss and a historical name constraint

**Source edition, recovery and historical comparison: icekylinx and GPT-6 Astra Pro.**

The two unheaded parts at the top of Childs p192 appoint a representative of
the Polish government for Georgia, Armenia and Azerbaijan, based in Tiflis.
Part 3 says the appointment and instructions have already been dispatched
through a person whose damaged name is `T?DE?SKI`. The independently attested
surname **TYDELSKI** supports a conditional recovery of **Nov13–15b FX = Y**.
The geometry is determined first, with both the courier name and the final
signature excluded from its scoring stencil.

A separately recovered **p199 unlettered part 1** provides a strongly matching
forwarding preamble: General von Kress in Tiflis is asked to pass the Polish
Foreign Ministry's telegram to **Waclaw v. Ostrowski**. Its floating `FGFFF`
group has a unique third-group placement under an ordinary-word stencil that
masks all relevant names and reference symbols. This source supplies the
recipient independently of the historical study. The cross-page association
retains the conflicting headings of 14 and 15 November explicitly.

See the [readable case](../../pages/192.md#edition-cases-caucasus-tiflis-appointment),
[literal inputs](inputs.json), and [exact certificate](certificates.json).

## Separate evidence layers

| Layer | Evidence and result |
| --- | --- |
| Source frame | Part 2 has 230/230 coordinates. Part 3 has 227 valid coordinates against RICHI-232. |
| Preamble layout | All 262 p199 letters are present. Moving the five observed floating letters to the third-group position gives the unique minimum among 258 placements, with two ordinary-word coordinate changes. Names and the reference are masked. |
| Missing-group geometry | All 228 boundaries are tested for one five-coordinate gap. Excluding all eight courier-name letters and all seven signature letters, gap 150 is the unique minimum with one observed-coordinate change. |
| Ordinary-word repair | Four of the five missing coordinates are supplied by ordinary words; correcting E to T in TIFLIS gives 114/116 fixed positions in part 3, retaining `T?DE?SKI`. |
| Historical name | The independent TYDELSKI identification fills the missing L half-coordinate and assigns the unchanged observed FX pair to Y. The complete 116-letter candidate reencrypts exactly. |

The last layer is an explicit historical identification assumption. It does
not modify the published key. Reencryption alone also permits seven other
unused symbols at FX; the certificate checks every one.

Across all three records there are **719 printed coordinate letters**, a
declared 724-coordinate frame after the missing group, and **354/362 fixed raw
positions** before repairs. The ordinary-word layer raises this to 358/362;
the conditional name layer reaches 360/362. The two remaining positions are
in the preamble's `?1?` reference. The p192 subset retains its original
225/231, 229/231 and 231/231 counts. Fixed raw totals include garbles, and the
exact country-name spelling is kept separately from its interpretation.

## Consequences kept visible

Direct FX=Y affects two complete pairs in this package and the 14 November
source edition: p192 part 3 position 61 and p190 A position 37. The latter's
name becomes `FRYE`. Transferring Y to Nov13–15a DG additionally requires the
same-correctly-copied-name assumption for the p190 A / p194 B pilot notices.
That transfer affects p194 B and its exact interrupted suffix p193 B.

The certificate lists the complete before/after raw texts, every newly fixed
raw position and every changed marginal domain. Its inventory covers all
ten source records in these two packages. The p199 preamble adds two narrowed
reference domains and no newly fixed raw letter under FX=Y. Other records are outside this
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
gap-search minimum, conditional re-encryption and local key-layer effect is
independently recomputed.
