# Baku personnel inquiry: a duplicated-block reconstruction

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Childs p185 B contains a conditional reading of an inquiry about the fate of
army personnel in **Baku**, addressed through General von Kress in Tiflis.
The printed body has **279 slots** against an advertised **268**, including
an exact repeated ten-coordinate block. The reconstruction excludes one
occurrence of that block and one further coordinate. Its readable wording
requires **10 observed-coordinate substitutions** and **1 source-mask fill**
in addition to the **11 excluded observed coordinates**.

The unchanged published **Nov13–15a** key fixes **125/134 raw positions** in
the stated frame. The edited output fixes **129/134** and preserves five
unknown reference positions. Two equally priced frame alternatives give the
same displayed words but different relations among those unknown labels;
both remain part of the result. Period-key recovery retains the published
credit to George Lasry and collaborators.


**Source-evidence delivery.** This text-only edition links the original public PDF and retains its page/crop coordinates, dimensions and pixel hashes. No new scan-image file is distributed. The default verifier checks the text and arithmetic; source pixels are checked only when the original PDF is supplied with `--pdf`.
## p185 B

[Reviewed source image — source-PDF reference](../../experiments/baku_personnel_inquiry/inputs.json).

**Source transcription — literal header:**

```text
B) NKJ v LP (07.57 p.m., November 13th)
FUER COS
SS GENERAL V KRESS TIFLIS 19.59 (13/11)
RICHI-268
```

The source's final row is:

**Source transcription — final row, excerpt:**

```text
GGDAX XFVVF DXXVG XFVVF DXXVG VDDXA FXAVV DXXD
```

The two identical **`XFVVF DXXVG`** blocks occupy source ranges **245–254**
and **255–264**, using zero-based indices. They remain in the complete
literal transcription. The primary 268-slot model excludes the first block
and the final D at source index **278**. No visible cancellation or free OCR
correction is claimed. The full native 279-slot decode and its unpaired
coordinate remain in the certificate.

**Raw output — conditional 268-slot frame after the eleven-coordinate exclusion; 125/134 fixed positions:**

```text
FU?KUNFTXUEBERXSCHICKSALXHEIRESANGEHOERIGERXJNX?AKUXERBET?NXKRIEGSMINISTERIUMXABTGILUNGXFUERXVNRBDENDENEXHEEREXNR????STRIC?A?XGEHXAXWX
```

**Edited output — same conditional frame; ten observed-coordinate substitutions and one source-mask fill; 129/134 fixed positions:**

```text
AUSKUNFTXUEBERXSCHICKSALXHEERESANGEHOERIGERXINXBAKUXERBETENXKRIEGSMINISTERIUMXABTEILUNGXFUERXVERBUENDETEXHEEREXNR????STRICHA?XGEHXAXWX
```

The observed substitutions, in zero-based source coordinates, are
**74 V→X**, **90 X→D**, **92 G→A**, **94 D→F**, **112 A→X**, **136 A→X**,
**138 X→F**, **139 F→X**, **143 F→V**, and **274 V→X**. The literal invalid
**E** in `XGVEX`, at source index **228**, is masked in the raw frame and
filled with **F** in the proposal. These changes are additional to the
source exclusions and do not assign a missing square cell.

**Readable German — complete edited stream under the conditional frame:**

> Auskunft ueber Schicksal Heeresangehoeriger in Baku erbeten. Kriegsministerium, Abteilung fuer verbuendete Heere. Nr ????STRICHA?. Geh. A W.

The proposed text requests information; it does not explain what happened
to those people or identify particular individuals. **`????STRICHA?`**
remains literal. `STRICH` is a decoded word proposal, not a display instruction
to replace that substring by punctuation. `A W` and the reference's A are
not expanded into names or offices.

## Competing exclusions and reference relations

The verifier compares both possible exclusions of the identical printed
ten-coordinate block, followed by **each of the 269 remaining source
coordinates** as the additional exclusion. That is **538 labelled source
maps**, with overlap between the two duplicate-block branches; it is not
538 independent historical observations.

For the stated letter pattern, with its five question marks left as
wildcards, the minimum is **10 observed-coordinate substitutions**. It is
attained by precisely six maps:

| Removed ten-coordinate block starts at | Additional excluded source index | Distinct retained frame |
|---:|---:|---|
| 245 or 255 | 276 or 277 | The two adjacent X choices give one retained stream |
| 245 or 255 | 278 | Excluding the final D gives a second retained stream |

All six maps give the same displayed raw and edited text. They do **not**
give the same square-cell relations for the unknown reference. In the table
below, Greek letters name unknown values; they are not inserted plaintext.

| Additional exclusion | Linked reference pattern | Unknown cells |
|---|---|---|
| Source 276 or 277 | `α β γ α STRICH A δ` | `α=GG`, `β=DX`, `γ=GX`, `δ=GD` |
| Source 278 | `α β γ α STRICH A γ` | `α=GG`, `β=DX`, `γ=GX` |

Each of these cells has the domain **`0123456789QY`** under the published
partial square. Repeated use of one cell has one shared value; distinct
cells must receive distinct values. In particular, the last unknown is
equal to the third unknown in the second frame but distinct from it in the
first. The current evidence does not choose between them.

The minimum-cost statement is confined to one declared letter pattern and
the duplicated-block-plus-one-exclusion family. It does not prove unique
historical wording, identify the damage mechanism, or justify deleting any
other source coordinates without a new account.

## Evidence and verification

[Inputs](../../experiments/baku_personnel_inquiry/inputs.json) ·
[Certificates](../../experiments/baku_personnel_inquiry/certificates.json) ·
[Reproduction notes](../../experiments/baku_personnel_inquiry/README.md).

```sh
python experiments/baku_personnel_inquiry/verify.py --verify
python experiments/baku_personnel_inquiry/verify.py --verify --pdf /path/to/childs.pdf
```

The optional PDF check reproduces the inspected crop and compares its
pixels. The verifier checks the literal duplicate, every source exclusion,
independent coordinate costs for all 538 labelled maps, both surviving
reference relations, complete readable-label preservation and exact
re-encryption with globally injective square-completion witnesses. Those
completion witnesses are explicitly nonhistorical. Earlier OCR and its
unchanged-key output remain separate from the present source reconstruction;
no universal first-decipherment priority is asserted.
