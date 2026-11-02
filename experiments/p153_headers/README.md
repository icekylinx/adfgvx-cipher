# p153: bounded full-page header follow-up

**No additional early part or retransmission was found.** This follow-up
independently OCRs all 31 complete printed pages 140–170 of the Childs
collection. It searches the whole page rather than only the header context
retained beside extracted ciphertext blocks. It adds a documented coverage
check; it does not recover plaintext or prove that parts 1–4 are absent from
every surviving record.

Prepared by **icekylinx and GPT-6 Astra Pro**. The earlier source review and
fixed-key corpus search remain in [the p153 source record](../../data/reviews/p153_source_review.json)
and [p153_corpus](../p153_corpus/README.md).

## Retrieved and inspected headers

Every complete three-character alphanumeric OCR token was compared with
`FKR` and `CGH`, allowing at most one substitution. The clear field `2250`
was also searched exactly. Only p153 produced the actual target call signs
and clear field. Two approximate matches were visually excluded.

| Printed page | OCR lead or review | Finding from the original image |
|---:|---|---|
| 152 | Immediate preceding page | UKS/ZON and NKJ/LP traffic; no CGH/FKR continuation identified. |
| 153 | `FKR`, `CGH`, `2250` | Confirms the known parts 5 and 6, dated 8 November 1918. |
| 154 | `CHH` | Analyst initials at the top of the page; the traffic uses UKS/ZON. |
| 163 | `COH` | OCR artifact in the spaced `RICHI` title; the traffic header is `--- v UKS`. |
| 223 | Earlier corpus's `FHR` near-match | Separate visual check confirms `AN LP v FHR`, with `KOW v RVA` and 27 November. The letter is H, not K. |

The p153 control also shows the limits of OCR: this pass recognizes both call
signs but reads the date as `3th` and the first advertised length as `133`.
The images establish **8th** and **132**. Consequently, a missing OCR hit
cannot exclude a differently damaged, split or omitted header.

The [review record](review.json) includes the source PDF hash, each full-page
OCR hash, the exact matching lines, visual verdicts and all scope limits. Full
page images and full OCR remain research intermediates and are not included
in the repository. The primary source is the
[public Childs scan](https://drive.google.com/file/d/1_JiNMck7eUvdrOTrH7fsj1Yh44t-VSC6/view);
printed page `n` is PDF page `n+3` in this range.

## Reproduce

Supply that PDF, PyMuPDF, and Tesseract with English language data. The script
renders pages at scale 2 and uses Tesseract page segmentation mode 3 with one
OpenMP thread per worker. A source-hash binding protects against reusing the
same scratch directory with another PDF.

```sh
python experiments/p153_headers/review_headers.py \
  --pdf /path/to/childs.pdf \
  --work-dir /tmp/adfgvx-p153-headers \
  --output /tmp/adfgvx-p153-header-review.json
```

Different OCR versions or language data can change the extracted text. The
stored hashes describe the recorded pass; visual review remains the basis
for correcting the printed date, lengths and near-matches. No station, unit,
unresolved digit or source repair is inferred from this negative result.
