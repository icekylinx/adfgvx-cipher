# The Danube field report: two companion parts, 10–11 November

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and exact repair audit: icekylinx and GPT-6 Astra Pro.**

Childs printed p176 B, PDF p179, labels a three-part message
`LP v ZÖN (3.38 a.m., November 11th); 2305 (10) 3 TLE`.
Its first part is the existing [p176b challenge](../p176b.md), credited
to **Prinz and GPT-6 Astra, 19 September 2026**. The two parts below
complete the source-labeled sequence; they do not solve the first
part's reconstructed 20-coordinate shortage or unknown unit digits.
Only these two physical records are new catalog entries.

These texts report French forces, a Danube crossing near the literal
place-name `RUSTUK`, and reserves north of `SLOBOZIE`. The edition treats
those statements as the sender's report; it does not independently
establish that the reported movements occurred. The two parts retain
their native source lengths and the unchanged published **Nov10–12**
square and ranks.

## p176 B2

The [252-coordinate source](../../experiments/nov10_delegates_and_field_report/sources/p176_B2.png)
directly reads:

**Raw output:**

```text
FEHERTEMPLOMXFOLGENFRANZOSENXXBESATZUNSHEERXFEINDVORFUEHLTEGEGENNEUESTELLUNGENDONAUKNIEXSAMVITXNACHAGENTENSTARKMITENGLAEN?ERNX
```

A single observed-coordinate replacement gives:

**Edited output:**

```text
FEHERTEMPLOMXFOLGENFRANZOSENXXBESATZUNSHEERXFEINDVORFUEHLTEGEGENNEUESTELLUNGENDONAUKNIEXSAMVITXNACHAGENTENSTARKMITENGLAENDERNX
```

The final word becomes `ENGLAENDERN`, in a report attributed to agents.
The source-derived `BESATZUNSHEER`, unusual order `FEINDVORFUEHLTE`, and
`SAMVIT` remain untouched. No extra letter is inserted into the first
word, no phrase is reordered, and no place-name is silently modernized.

The original question mark is pair `FD`, whose domain is **56789** in
the partial square. Source coordinate **108** changes **F→G**, turning
that pair into a known `D`. This is an explicit ciphertext repair, not
a fill of an erased coordinate or an assignment of an unknown key cell.

## p176 B3

The [272-coordinate source](../../experiments/nov10_delegates_and_field_report/sources/p176_B3.png)
directly reads:

**Raw output:**

```text
MAROKANERNBELEG1XXSISTOWXZUGVERKEHRXXBEIXRUS2UKXSETZTENFRANZOSENRUMAENISCHUFERUEBERXXRESERVENBRACHTENSNENOERDLNCHXSLOBOZIEXZUMSTEHENXOKM
```

Four observed-coordinate replacements give:

**Edited output:**

```text
MAROKANERNBELEGTXXSISTOWXZUGVERKEHRXXBEIXRUSTUKXSETZTENFRANZOSENRUMAENISCHUFERUEBERXXRESERVENBRACHTENSIENOERDLICHXSLOBOZIEXZUMSTEHENXOKM
```

This part mentions Moroccan troops and train traffic at `SISTOW`, then
reports French forces crossing to the Romanian bank near `RUSTUK` and
being stopped by reserves north of `SLOBOZIE`. Its opening depends on
the preceding part for context; no missing introductory phrase is
supplied. The spellings `MAROKANERN`, `RUSTUK`, `RUMAENISCHUFER` and
`SLOBOZIE` are left exactly as the candidate decodes.

The enlarged [five-letter group](../../experiments/nov10_delegates_and_field_report/sources/p176_B3_group.png)
confirms `VDVAV`. There is no source deletion or uncertain final frame.
The four replacements change `BELEG1`, `RUS2UK`, `SNE` and `NOERDLNCH`
as displayed. Both numerical-looking pre-repair labels remain in the
certificate; no global interpretation of `1` or `2` is imposed.

## Scope and attribution

These two parts total **524 observed coordinates**, **262 plaintext
positions**, **261 raw fixed labels**, and **262 candidate fixed labels**.
Their cost is **five observed-coordinate substitutions**, with no
coordinate fill, loss model, deletion or key change. All candidate
characters re-encrypt to the exact explicitly repaired streams.

Earlier unreviewed whole-corpus screening already produced readable
bodies for both parts. The contribution here is source transcription,
the complete coordinate and domain ledger, and verification of the
parts' printed relationship. A bounded review of the paper, thesis
and cached comments found no separate explicit discussion of these
two bodies; that absence does not establish historical priority.

The report shares geographical context with the already reviewed
Nov9 operational messages and the Nov3 Mackensen report. It is not
presented as an exact copy of either. The old p176b unit interpretation
also remains an independent conditional layer.

[Inputs](../../experiments/nov10_delegates_and_field_report/inputs.json),
[certificates](../../experiments/nov10_delegates_and_field_report/certificates.json)
and [verification instructions](../../experiments/nov10_delegates_and_field_report/README.md)
provide the literal source rows, all edits, historical-credit checks,
and the source-header crop.
