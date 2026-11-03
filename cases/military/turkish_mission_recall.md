# Recall of contract-bound military-mission members from Turkey

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source:** J. Rives Childs, *General Solution of the ADFGVX Cipher System*,
printed p130 A1–A2 and p131 A3–A4, PDF pp133–134.
**Edition:** icekylinx and GPT-6 Astra Pro.

The four parts share `OSM v OUI (8.25 p.m., November 5th)` and
`#12 2015 4 TEILE`. The order recalls contract-bound members of the
military mission, including those already under notice of termination,
and directs arrangements for return and reporting after arrival in
Germany. One received office abbreviation remains unresolved; the
edition preserves it visibly alongside the readable instructions.

The unchanged Nov4–6 square and ranks produce all 645 plaintext labels.
The [experiment](../../experiments/turkish_mission_recall/README.md)
retains exact source crops, coordinates, domains and repair costs.

## p130 A1

The source advertises and prints **394 valid coordinates**. The second
group, `VGVVF`, is complete in the source but was omitted by earlier OCR.
The raw 197-position reading needs no coordinate change:

```text
MILITAERMISZIONKONSTANTINOPELXZURM2NR46873XSEMAJDERKAISERUKOENIGHABENBEFOHLENXSAEMTLICHEVERTRAGLICHVERPFLICHTETENMITGLIEDERDERMILMISZIONEINSCHLISZLICHDERJENIGENWELCHENDERVERTRAGBEREITSGEKUENDIGTIST
```

The text addresses the military mission at Constantinople, retains the
raw reference `ZURM2NR46873`, and states an order of the Emperor and King
concerning all members bound by contract, including those whose
contracts had already been given notice. The transmitted `SZ` forms and
`EINSCHLISZLICH` remain exactly as received.

## p130 A2

The source advertises and prints **330 valid coordinates**. The raw text is:

```text
WERDENAUFGRUNDMESIRTIKELS10DESMITGENERALDERKAVLIMANVONSANDERSABESCHLOSZENENVERTRAGSMITDEMTAGEDERVEROEFFENTLICHUNGDESWAFFENSTILLSTANDESDERTUERKEIZUMHEEREZURUCKBERUFEN
```

The conservative candidate makes only two ordinary-letter changes:

```text
WERDENAUFGRUNDDESARTIKELS10DESMITGENERALDERKAVLIMANVONSANDERSABESCHLOSZENENVERTRAGSMITDEMTAGEDERVEROEFFENTLICHUNGDESWAFFENSTILLSTANDESDERTUERKEIZUMHEEREZURUCKBERUFEN
```

These require source-coordinate **156 X→D** and **176 X→F**, both
zero-based. They repair `MESIRTIKELS` to `DESARTIKELS`. The article label
`10`, the name `LIMANVONSANDERS`, and all other pairs remain unchanged.

The text says the members are recalled to the army, under the cited
article of the contract with General der Kav. Liman von Sanders,
effective upon publication of Turkey's armistice. The received
`ABESCHLOSZENEN` and `ZURUCKBERUFEN` are not lengthened by supplying
an unseen `G` or `E`. The underlying contract is not independently
authenticated by this edition.

## p131 A3

The source advertises and prints **396 valid coordinates**, separately
from the following fourth part. Earlier OCR merged the two frames.
The 198-position raw reading is:

```text
DIEMILMISZIONVERANLASZTZUGEGEBENENENZEITPUNKTDIEHEIMSENDUNGUWEISTDIEHEIMKEHRENDENANIHRENAUFENTHALTSORTSOGLEICHNACHEINTREFFENINDEUTSCHLANDDEMMILIGRHYUBEZWDENKRIEGSMINISTERIENDERBUNDESSTAATENZUDRAHTEN
```

No coordinate change is proposed. The mission is to arrange the return
at the relevant time and instruct those returning to telegraph their
whereabouts immediately after arriving in Germany. The recipients are
the unresolved received **`MILIGRHYU`** and, in the following `BEZW`
clause, the war ministries of the federal states.

The nine letters at plaintext indices **140–148** all have complete
observed pairs, but the office word is not resolved. It is not silently
replaced with a plausible Military Cabinet abbreviation. The apparent
duplication in `ZUGEGEBENENEN` also remains. Thus 198 fixed square labels
do not mean that every word has been editorially identified.

## p131 A4

The source advertises and prints **170 valid coordinates**. The raw text is:

```text
LETZTERESINDBENACHRICHTIGTXWUFALLERHOECHSTENBEFEHLCHEFMILITAERKABINETTSFRHRMARSCHALLX
```

The candidate changes only **source index 133 A→V**, giving `AUF`
instead of `WUF`:

```text
LETZTERESINDBENACHRICHTIGTXAUFALLERHOECHSTENBEFEHLCHEFMILITAERKABINETTSFRHRMARSCHALLX
```

It reports that the latter recipients have been notified and closes
with the received title and signature. With editorial spacing:

> Letztere sind benachrichtigt. Auf allerhöchsten Befehl, Chef Militärkabinetts, Frhr. Marschall.

The complete 58-character closing beginning `AUF` is independently
observed in the raw reading of already-reviewed
[p149 A2](../people/osthoff.md). The verifier compares all 58 coordinate
pairs and keeps the earlier source hash and crop. This is support for
the repaired closing; the other message concerns Osthoff and is not
treated as an exact retransmission of this entire order. The earlier
record is not counted again, and no independent identity is assigned
to the received `FRHR MARSCHALL` signature.

## Attribution, costs and limits

The four records contain **1,290 valid source coordinates** and **645
fixed raw labels**. The candidate costs **three observed-coordinate
substitutions**, with no erasure fills, source insertions, deletions,
key changes or rank changes. All numeric labels remain unchanged.
The nine-letter office field remains unresolved despite its complete
coordinates.

The key is previously published. Part two was already readable in the
earlier unreviewed repository screen; defective OCR and merged frames
obscured the other parts. Frozen earlier outputs distinguish source
correction from prior body availability. Bounded paper, dissertation
and comment-thread checks did not locate an explicit treatment of this
body, without establishing historical priority.

The text records a recall order and reporting instructions. It does not
establish that each person returned, that each report was sent or that
the cited contract has been independently verified.

```bash
python experiments/turkish_mission_recall/verify.py --verify
python experiments/turkish_mission_recall/verify.py --verify --pdf /path/to/childs.pdf
```
