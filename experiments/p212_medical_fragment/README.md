# p212 A4: a conditional medical fragment from 197 surviving coordinates

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

A new 302-coordinate missing-prefix hypothesis yields connected wording about institutions where patients can remain, transport, personnel and medicines. The literal source says **4 TL (Missed start)** and prints 197 valid coordinates; it gives no total length. The published **Nov22–24** square and ranks remain unchanged.

The raw baseline fixes **46/151 positions** and leaves all 105 added coordinate slots unassigned. Five explicit lexical stencils fill **83 missing halves**, yielding **129/151 primary positions**. They change **zero observed coordinates**. The other 22 positions remain `?`; no complete historical message or unique completion is claimed.

Read the [partial source edition](../../cases/military/p212_medical_fragment.md). The [inputs](inputs.json) preserve the source, frame and compact retrieval/control evidence; the [certificate](certificates.json) maps every coordinate and fill.

```sh
python experiments/p212_medical_fragment/verify.py --verify
python experiments/p212_medical_fragment/verify.py --verify --pdf /path/to/childs.pdf
```

Default verification uses only the standard library and independently reconstructs the source mapping, all 151 domains, the 83 fills, unchanged-source reencryption witnesses and the control fixtures. The optional PDF check uses PyMuPDF/Pillow and reproduces the already archived source crop. No new image is added. Retrieval scores and finite shuffle results are frozen diagnostics; default verification does not replay their external language model or full scan.

Historical key credit: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Source review, new coordinate-pattern retrieval, lexical stencils and exact certificates: icekylinx and GPT-6 Astra Pro. Earlier source editions remain unchanged and retain their credits.

An [optional hospital-support-staff extension](optional_underpersonal.json) adds six missing-half fills without changing the primary layer: **135/151 positions**, **89 total fills**, **16 unresolved**, zero observed substitutions. Period sources attest *Unterpersonal* as auxiliary/support staff; they do not authenticate this telegram. Check it separately with `python experiments/p212_medical_fragment/verify_optional_underpersonal.py --verify`.
