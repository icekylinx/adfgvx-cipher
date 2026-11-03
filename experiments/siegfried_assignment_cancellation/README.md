# Siegfried assignment cancellation: conditional surplus coordinate

Source edition and verification by **icekylinx and GPT-6 Astra Pro**.

The [p135 A edition](../../cases/people/siegfried_assignment_cancellation.md)
preserves **401 source slots**, including **397 observed coordinates** and
**four printed masks**, exactly matching RICHI-401. Its original odd-frame
raw reading and orphan coordinate remain available.

A conditional extra X before transposition explains the pairing-phase change.
Excluding interim 230 or 231 after the original 401-slot inverse transposition
produces one identical 400-coordinate stream. The two source origins, 296 or 84,
remain distinct aliases. The 200-position conditional raw stream fixes 196
positions; **seven observed substitutions**, **four source-mask fills** and
**one expressly accounted surplus-X exclusion** give the complete proposal.
The received frame remains 401 slots in the exact forward witness.

The closing 58 letters are independently fixed by the raw p149 A2 Osthoff
record. All 58 pairs are rechecked without importing that message's identity
or surrounding body. The older record is not counted as new. Reference 45610
and all abbreviations remain literal.

`certificates.json` includes the native odd frame, both surplus aliases,
all 802 single-exclusion prices at the interim and transmitted stages,
every edit and fill, both source-shaped forward witnesses, the complete
closing comparison and the readable-quote correspondence. The conditional
model has minimum 7 substitutions; excluding one transmitted coordinate under
the same target has minimum 144. These are bounded compatibility results,
not proof of historical causation or uniqueness among arbitrary error models.

## Reproduce

```sh
python experiments/siegfried_assignment_cancellation/verify.py --verify
python experiments/siegfried_assignment_cancellation/verify.py --verify --pdf /path/to/adfgvx-childs.pdf
```

The optional PDF check verifies its byte count/hash and regenerates both the
new p135 crop and earlier p149 crop for pixel comparison. It requires
PyMuPDF/Pillow. The normal check uses only the checked-in standard-library
code and pinned source evidence, without external scratch caches.
