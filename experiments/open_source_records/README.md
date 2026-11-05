# Four OPEN source records

Source transcription and verification: **icekylinx and GPT-6 Astra Pro**.

This package publishes the literal evidence for four physical bodies that
previously lacked canonical case pages. All four remain **OPEN**. It contains
no accepted key, plaintext, completed transposition frame or repaired source.

| Canonical source | Received slots | Observed coordinates | Printed erasures | Advertised length |
| --- | ---: | ---: | ---: | ---: |
| [p70 B1](../../pages/070.md#edition-cases-open-p70-b1) | 206 | 199 | 7 | 206 |
| [p127 B2](../../pages/127.md#edition-cases-open-p127-b2) | 152 | 104 | 48 | 152 |
| [p145 A](../../pages/145.md#edition-cases-open-p145-a) | 192 | 187 | 5 | Not printed |
| [p194 D1](../../pages/194.md#edition-cases-open-p194-d1) | 45 | 45 | 0 | 214 |

The [inputs](inputs.json) retain every field of the corresponding frozen
[21-source audit](../../data/reviews/source_gap_audit_20261103.json). The new
embedded PNGs reproduce its exact crop rectangles and RGB digests from the
authenticated Childs PDF. Clear header displays normalize spacing only;
the original audit’s header transcription remains separately preserved.

The cases explain the important boundaries: p70’s interruption annotations,
p127’s repeated groups and long erasures, p145’s left-margin designator and
missing-first-part note, and p194’s large difference between received and
advertised length. These are separate physical records, not a shared-key
family or a set of proposed decipherments.

```sh
python experiments/open_source_records/verify.py
python experiments/open_source_records/verify.py --pdf /path/to/childs.pdf
```

The default check verifies frozen audit equality, source hashes, coordinate
counts, case transcriptions, PNG bytes and RGB pixels. Supplying the original
PDF additionally authenticates its bytes and re-renders every crop. The
runtime report states which PDF comparisons were actually performed.

All 595 received slots remain native source evidence: 535 observed
coordinates and 60 printed erasures. No unprinted coordinate deficit is
added to these counts. In particular, p194’s conditional 169-coordinate
shortfall creates no raw plaintext labels.
