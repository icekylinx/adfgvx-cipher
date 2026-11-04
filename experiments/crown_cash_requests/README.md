# Crown-cash requests and banknote shortage

ADFGVX Cipher — **icekylinx and GPT-6 Astra Pro**.

A source edition of Childs p219 A1–A2 and B. A requests an advance for
Arad after an arrangement with the German military mission at Budapest;
B separately reports partial crown remittances and a severe banknote
shortage. The full [case](../../cases/pages/219.md#edition-cases-finance-crown-cash-requests) keeps
every raw reading, exact candidate and interpretation limit.

All **918 source coordinates** are valid and the advertised lengths
334, 230 and 354 match exactly. The unchanged published square fixes all
**459 raw-label positions**. The candidates make six observed-coordinate
substitutions: one in A1, three in A2 and two in B. No geometry changes,
erasure fills or key assignments are needed.

A1's `FDDFX` is fully observed; its final `X` was uncertain only in earlier
OCR. The other word repairs and complementary `MGD`/`ARAD` support are
separately certified. The office abbreviation is not expanded, and the
received names `FIALA` and `KUDEL` are not identified as historical people.

## Raw amount and reference fields

- A1: `JJ FIALA`, `6 MIL KRONEN`, `3YYYYY KRONEN`.
- B: `A O K JJ`, `J3Y20`, `ROEM4BJ411XJYJ2`.

Every pair in these fields is complete and unchanged by the candidates.
All numeral and `J/Q/Y` occurrences are inventoried: 27 in the raw texts,
25 in the candidates. The separately repaired raw `0` in `MG0` and raw `9` in
`MOEGLICHK9IT` remain visible. No amount is normalized by plausibility.

The two parts of A are explicitly numbered in one message. B has a
separate header: receipt November 27, origin November 25. It is not assumed
to answer A merely because both concern crown liquidity. The dates are
preserved, and partial remittance is not described as completed payment.

All three bodies predate this edition as unreviewed repository OCR
retrieval candidates. The new contribution is source transcription,
exact mapping, priced repairs and complete raw-label audit. Published key
provenance and bounded prior-body checks are included.

## Reproduce

```bash
python experiments/crown_cash_requests/verify.py --verify
python experiments/crown_cash_requests/verify.py --verify --pdf /path/to/childs.pdf
```

The optional PDF check verifies the full source hash and all retained
crop pixels. The three-entry `catalog_proposal.json` is for parent
integration; this package changes no shared catalog or key.
