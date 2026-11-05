# p212 A4: a conditional medical fragment from 197 surviving coordinates

**ADFGVX Cipher · icekylinx and GPT-6 Astra Pro**

A new 302-coordinate missing-prefix hypothesis yields connected wording about institutions where patients can remain, transport, personnel and medicines. The literal source says **4 TL (Missed start)** and prints 197 valid coordinates; it gives no total length. The published **Nov22–24** square and ranks remain unchanged.

The raw baseline fixes **46/151 positions** and leaves all 105 added coordinate slots unassigned. Five explicit lexical stencils fill **83 missing halves**, yielding **129/151 primary positions**. They change **zero observed coordinates**. The other 22 positions remain `?`; no complete historical message or unique completion is claimed.

Read the [partial source edition](../../pages/212.md#edition-cases-military-p212-medical-fragment). The [inputs](inputs.json) preserve the source, frame and compact retrieval/control evidence; the [certificate](certificates.json) maps every coordinate and fill.

```sh
python experiments/p212_medical_fragment/verify.py --verify
python experiments/p212_medical_fragment/verify.py --verify --pdf /path/to/childs.pdf
```

Default verification uses only the standard library and independently reconstructs the source mapping, all 151 domains, the 83 fills, unchanged-source re-encryption witnesses and the control fixtures. The optional PDF check uses PyMuPDF/Pillow and reproduces the already archived source crop. No new image is added. Retrieval scores and finite shuffle results are frozen diagnostics; default verification does not replay their external language model or full scan.

Historical key credit: George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker (2016), and George Lasry (2017 key list). Source review, new coordinate-pattern retrieval, lexical stencils and exact certificates: icekylinx and GPT-6 Astra Pro. Earlier source editions remain unchanged and retain their credits.

An [optional hospital-support-staff extension](optional_underpersonal.json) adds six missing-half fills without changing the primary layer: **135/151 positions**, **89 total fills**, **16 unresolved**, zero observed substitutions. Period sources attest *Unterpersonal* as auxiliary/support staff; they do not authenticate this telegram. Check it separately with `python experiments/p212_medical_fragment/verify_optional_underpersonal.py --verify`.

The optional [search replay](replay_search.py) reconstructs the exact hybrid model and checks the **6,300 frames, three length controls (ranks 1, 1, 2), and 100 same-key shuffles**. It requires NumPy and the external [upstream `data/quad.bin` at commit `083921732d7c18e52424336ab4160fada5c61b4b`](https://raw.githubusercontent.com/0wwafa/adfgvx-1918/083921732d7c18e52424336ab4160fada5c61b4b/data/quad.bin), SHA-256 `a39714514cd2884605b1b04a2f65565fcf33aec1f7162bcd1b472c7108601009`. [Search provenance](search_provenance.json) pins every input and the float32 quantization step; no model binary or full search log is bundled. Exact reproduction starts from that distributed binary; its original corpus downloads were not pinned. These scores do not authenticate the inferred total or give an all-key probability of correctness.

```sh
OPENBLAS_NUM_THREADS=1 python experiments/p212_medical_fragment/replay_search.py \
  --book-quad26 /path/to/quad.bin --replay
```

Omit `--replay` to check model reconstruction alone. The primary verifier remains independent of NumPy and the external model. Upstream model credit: the 0wwafa/adfgvx-1918 contributors; replay implementation: icekylinx and GPT-6 Astra Pro.

A [further optional transport-and-doctor clause](optional_transport_extension.json) adds 13 missing halves while preserving the earlier layers: **148/151 positions**, **102 total fills**, three positions after LAZARETT unresolved. Its separate global numeric+J interpretation reads “Zu jedem Transportzug 1 Arzt …”; all baseline labels remain unchanged. Check with `python experiments/p212_medical_fragment/verify_optional_transport_extension.py --verify`.
