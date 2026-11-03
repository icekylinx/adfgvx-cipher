# November 22: reverse key use and an Aufbau date correction

**Reading layers:** [Raw output · Edited output · Readable German · Conditional interpretation](../../docs/reading-conventions.md). In decoded streams, `?` marks one unresolved position; `X` and numeral/letter labels remain literal.

**Source edition and verification: icekylinx and GPT-6 Astra Pro.**

Two records on Childs p214 preserve instructions about retaining keys and
correcting date-like labels. The unchanged published **Nov22–24** key gives
**133/134 fixed raw positions** from **268 native source slots**. The proposed
complete reading fills **one invalid source glyph**, with **no change to an
observed coordinate** and no inserted, deleted or reordered source slot.
Published period-key recovery retains the credit to George Lasry and
collaborators recorded in the [key inventory](../../data/keys.json).


**Reviewed source crops:** [p214_reviewed.png](../../experiments/nov22_reverse_keys_and_date_correction/sources/p214_reviewed.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## p214 A1

[Reviewed source image — source-PDF reference](../../experiments/nov22_reverse_keys_and_date_correction/inputs.json).

**Source transcription — literal headers:**

```text
22nd NOVEMBER, 1918.
A) ZOEN v BSL (04.25 a.m., November 23d)
1600 (11/22) 2 TLE
1 TL RIZI-180
```

`ZOEN` represents the O with two marks in the call sign. The November 22
heading and internal date are kept separately from the November 23 receipt.
The header advertises two parts, but this section prints only the first.

**Raw output — native 180-slot frame; 90/90 fixed positions:**

```text
BISAUFWEITERESSAEMTLICHESSCHLUESSELABJJXAUFBEWAHRENXFUERDEZEMBERDANNXRUECKWAERTSVERWENDENX
```

**Readable German — complete raw stream, with spacing and punctuation only:**

> Bis auf weiteres saemtliches Schluessel ab JJ aufbewahren. Fuer Dezember dann rueckwaerts verwenden.

The grammatical form **`SAEMTLICHES SCHLUESSEL`** is deliberately retained.
Changing it to a smoother form would alter the decoded stream. **`JJ`** is
kept as two literal square labels rather than converted into a date.

The message says to retain the keys from the stated label and then use them
backwards for December. **`RUECKWAERTS` is directly decoded.** This part does
not supply a complete schedule or explain every detail of the reversal, and
a transmitted instruction alone does not establish actual subsequent use.
The [p145/p211 Ringbahn schedule](nov6_ringbahn_key_witnesses.md) and the
[later BSL–UKS arrangement](late_november_cipher_instructions.md) remain
separate source statements; their rules are not silently substituted here.

The earlier OCR omitted the printed final group **`AAVXA`** and transcribed
the five-slot **`VVXAF`** as six characters. Restoring those visible groups
produces the printed 180-slot stream. These corrections repair the machine
transcript; they do not add or remove coordinates from the source.

## p214 C

**Source transcription — literal header:**

```text
C) BSL v ZOEN (06.09 p.m., November 22d)
RIZI-88
```

The printed date is **November 22d**, unlike the earlier OCR's November 23d.
The ciphertext contains the Y-like invalid initial glyph in **`YXAFF`**;
that literal observation remains in the transcription and is masked for the
raw decryption.

**Raw output — native 88-slot frame; 43/44 fixed positions:**

```text
A?FBAUNICHTJ8XODERJ7XSONDERNJ7XODERJ3XNOVXXX
```

**Edited output — one source-mask fill; no observed-coordinate substitution; 44/44 fixed positions:**

```text
AUFBAUNICHTJ8XODERJ7XSONDERNJ7XODERJ3XNOVXXX
```

Supplying **V** at **source index 60** gives the U in `AUFBAU`. The index is
zero-based. This is a fill of an already present invalid source slot, not an
inserted coordinate or a change to an accepted coordinate.

**Readable German — complete edited stream, with spacing and punctuation only:**

> Aufbau nicht J8 oder J7, sondern J7 oder J3 Nov.

The two occurrences of **`J7`** remain, as do **`J8`** and **`J3`**. The message
corrects date-like alternatives associated with `Aufbau`; it does not itself
identify a unit or an installation. Adjacency alone does not establish that
this is the missing second part of A or a correction of a particular other
telegram.

## Evidence and verification

The [source inputs](../../experiments/nov22_reverse_keys_and_date_correction/inputs.json)
retain the complete literal groups, headers, published key and reading
proposals. The [certificates](../../experiments/nov22_reverse_keys_and_date_correction/certificates.json)
check each output position, the single mask fill, exact re-encryption and
the complete readable-label mapping. The original OCR and its unchanged-key
outputs remain available as separately labelled comparisons.

```sh
python experiments/nov22_reverse_keys_and_date_correction/verify.py --verify
python experiments/nov22_reverse_keys_and_date_correction/verify.py --verify --pdf /path/to/childs.pdf
```

The optional PDF check compares the saved crop with the original source
pixels. These source editions preserve earlier key and repository credits;
no universal first-decipherment priority is asserted.
