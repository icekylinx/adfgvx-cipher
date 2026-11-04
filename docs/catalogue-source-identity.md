# One source, one catalogue entry

[Catalogue](../topics/README.md) · [Evidence coverage](whole-material-coverage.md) · [Reading conventions](reading-conventions.md)

The catalogue contains one canonical entry for each of the **679 physical
ciphertext bodies** in the reviewed Childs log. A separately printed part or
received copy has its own source location. An alternative reading, improved
repair model or spelling supplement belongs to the existing source’s case.
It does not create another entry.

Every entry carries an explicit **READING**, **PARTIAL**, **CONDITIONAL** or
**OPEN** state. These are navigation labels, with their limits explained in
the [state definitions](reading-conventions.md#catalogue-states). The seven
OPEN cases are included in the catalogue on the same basis as the other
sources; their inclusion does not add a decipherment.

## The canonical p132 case

[Challenge p132](../cases/pages/132.md#edition-cases-p132) is Childs printed p132, section B. The
later source package calls this same record `p132_B`. Both inputs have the
same header, source location and complete **155-slot** ciphertext, including
the same two printed erasures. Its literal SHA-256 is:

```text
66115bd2941724f227aa9b34651f977127c0bf27bc4b2aee3dd876f804ce79a1
```

The canonical case combines Thomas’s initial fragment, Norbert’s fuller
sender-error reading and `VORHER` alternative, Max Baertl’s related editorial
proposal, and the subsequent source and arithmetic review by **icekylinx and
GPT-6 Astra Pro**. It also retains the four equivalent intermediate-`V`
positions and the explicit three-substitution/two-erasure-fill account.

`p132_B` remains an identifier inside the existing evidence files. The
[source-record alias register](../data/source_record_aliases.json) binds
that spelling only to those specific files and canonical `p132`. It does
not authorize a second live catalogue row. The old
[radio-service B anchor](../cases/pages/132.md#edition-cases-radio-p132-radio-service-b-repeat-the-fourth-period-telegram-in-the-fifth)
now points to the consolidated case. The independent A and C sources on
that page retain their own entries.

## Machine checks

The catalogue loader requires every reviewed census location exactly once,
retains all 22 original challenge identifiers, checks case/evidence paths,
and rejects every duplicate page/section location. The restricted evidence
lookup additionally verifies the entire literal ciphertext and its digest;
it cannot merge two records merely because their wording resembles one
another.

```sh
python data/reviews/verify_catalog_source_identity.py
python -m unittest discover -s tests -p 'test_catalog_source_identity.py'
python data/reviews/verify_childs_material_coverage.py --verify
```

The dated census and earlier experiment records remain historical evidence.
Current navigation and coverage are computed from the canonical catalogue.
