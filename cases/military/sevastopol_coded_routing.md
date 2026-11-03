# Sevastopol routing amendment with twelve opaque code groups

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p139 A1/A2/A3, PDF p142, form the message headed
`NKJ v LP (5.57 a.m., November 6th)` and `SSD FUER ASO 1940 3 TLE`.
The consecutive source labels give native lengths **200 / 220 / 212**.
All three parts use the unchanged published **Nov4–6** key.

The opening and distribution are readable German routing text. Part 2
contains **CUJOMAREMO** followed by twelve five-figure groups. The outer
ADFGVX cipher yields those labels, but their possible inner code or
codebook meaning remains unresolved. They are preserved exactly rather
than translated or treated as known quantities.

## p139 A1

The [first-part crop](../../experiments/sevastopol_coded_routing/sources/p139_A1.png)
contains **200 valid coordinates**, giving **100 / 100 fixed positions**.
The [enlarged heading](../../experiments/sevastopol_coded_routing/sources/p139_A1_length.png)
confirms `RICHI-200`; an initial page-scale impression of 300 was rejected
before publication. There is no inferred 100-coordinate gap.

**Raw output — native 200-coordinate frame:**

```text
NATEKOXSEWASTOPOLXVONSEEKRIEGSLTGXGRXHXYUXSLX4475XINABAENDERUNGXFECHX3XGROSSXBXFRX53083XSINDGEMAESSX
```

**Edited output — unchanged, with zero substitutions or fills:**

```text
NATEKOXSEWASTOPOLXVONSEEKRIEGSLTGXGRXHXYUXSLX4475XINABAENDERUNGXFECHX3XGROSSXBXFRX53083XSINDGEMAESSX
```

**Readable German — spacing, punctuation and umlauts; abbreviations remain literal:**

> NATEKO, Sewastopol. Von Seekriegsltg. Gr. H. YU. SL. 4475.
> In Abänderung FECH. 3. Gross B. FR. 53083 sind gemäß

The sentence continues in part 2. **YU** is retained without converting
it to a more familiar headquarters abbreviation. The raw 3 and all
reference numbers remain unchanged.

## p139 A2

The [second-part crop](../../experiments/sevastopol_coded_routing/sources/p139_A2.png)
contains **220 visible slots**. Its first glyph is B in **BVAGD**, which
is outside the ADFGVX coordinate alphabet. That occupied source slot is
masked without deletion.

**Raw output — native 220-coordinate frame:**

```text
XAX?RX11120XGEHOPXCUJOMAREMOX36117X59000X13814X39800X42097X85206X82520X51933X32342X28215X38105X04376XZULEITENX
```

**Edited output — one invalid-glyph fill, with zero observed-coordinate substitutions:**

```text
XAXNRX11120XGEHOPXCUJOMAREMOX36117X59000X13814X39800X42097X85206X82520X51933X32342X28215X38105X04376XZULEITENX
```

Source **0 B→X** supplies N in **NR**. The raw unknown is plaintext
position **3**, pair **X?**, domain **4CMNST**, with source indices **194**
and **0**. N is a contextual editorial selection for “Nr.”; the
certificate retains all six complete raw alternatives. The edited
candidate fixes **110 / 110 positions** and re-encrypts exactly.

**Readable German — spacing and punctuation, with the opaque groups copied literally:**

> A. Nr. 11120 Geh. Op. CUJOMAREMO
> 36117 59000 13814 39800
> 42097 85206 82520 51933
> 32342 28215 38105 04376
> zuleiten.

The marker and twelve groups are retained in their source order, including
the initial 0 of **04376**. This reading does not supply their underlying
meaning. In particular, **316 fixed plaintext positions** across the
message would not mean 316 recovered German letters or a solved inner
code.

## p139 A3

The [third-part crop](../../experiments/sevastopol_coded_routing/sources/p139_A3.png)
contains **212 valid coordinates**, giving **106 / 106 fixed positions**.

**Raw output — native 212-coordinate frame:**

```text
GLEICHESSXETRAXSUEDOSTXEZXKIEWXBVGXRUMXSXMXSTXDEUTSCHERSTABXNACARXRXMXAXADMIRALSTABFECH2XGROSZXBXERX53689X
```

**Edited output — unchanged, with zero substitutions or fills:**

```text
GLEICHESSXETRAXSUEDOSTXEZXKIEWXBVGXRUMXSXMXSTXDEUTSCHERSTABXNACARXRXMXAXADMIRALSTABFECH2XGROSZXBXERX53689X
```

**Readable German — spacing, punctuation and umlaut, with opaque fields and spelling retained:**

> Gleiches S. Etra Südost. Ez. Kiew. BVG. Rum. S. M. St. Deutscher
> Stab. NACAR. R. M. A. Admiralstab. FECH2. Grosz B. ER. 53689.

The extra S after **GLEICHES** is retained as a separate S. field.
**EZ** is displayed as “Ez.”, **NACAR** is not changed into an assumed
notification abbreviation, and **GROSZ / ER** remain literal. No
organization or reference is supplied to smooth the distribution.

## Conditional interpretation and source recovery

The earlier OCR omitted the X at A1 source **11**, giving 199 coordinates
instead of the scan's 200. The
[frozen OCR snapshot](../../experiments/sevastopol_coded_routing/ocr_snapshot.json)
and [certificate](../../experiments/sevastopol_coded_routing/certificates.json)
verify that single source-visible difference. The old corpus is unchanged.
Restoring the visible X repairs the transcript; it is not an insertion
into the historical ciphertext.

Across the three records there are **632 visible slots**, **631 valid
source coordinates**, and **316 plaintext positions**. The raw layers
fix **315 / 316**; the edited layers fix **316 / 316**, with **zero known
coordinate substitutions and one invalid-glyph fill**. All source frames
and the published key remain unchanged, and every complete edited stream
re-encrypts exactly. The message is an instruction and distribution list,
not proof that a shipment or transmission actually occurred.

Earlier repository candidates and published key provenance remain
explicit, including the previously readable distribution. The edition
makes no historical first-solution claim. See the
[inputs](../../experiments/sevastopol_coded_routing/inputs.json) and
[reproduction instructions](../../experiments/sevastopol_coded_routing/README.md).
