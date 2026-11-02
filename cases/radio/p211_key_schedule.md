# p211, lower B — an explicit November/December key schedule

[Case guide](../README.md) · [ADFGVX Cipher](../../README.md)

**Status:** Three source-checked parts form a readable key-handling
instruction. The unchanged published `Nov4-6` key fixes **265 of 266 raw
plaintext positions** from **532 printed coordinate slots**. **Source
assembly and edition:** icekylinx and GPT-6 Astra Pro. Period-key recovery
retains the attribution in [data/keys.json](../../data/keys.json); no first
historical decipherment priority is claimed.

## Reading

> November-Ringbahnschluessel nicht vernichten. Nachr.-Chef X4, B848727.
> Dezember-Ringbahnschluessel tritt vorlaeufig nicht in Kraft. Dafuer
> Schluessel erster Dezember wie zehnter November usw. bis
> einundzwanzigster Dezember wie dreissigster November.
> Empfangsbestaetigung. Nachr.-Chef Z4, B47857.

**Meaning:** Do not destroy the November Ringbahn key. The December Ringbahn
key will not yet take effect. Instead, use the 10 November key for 1 December,
continuing through the 30 November key for 21 December, and acknowledge
receipt.

The schedule itself is directly decoded in part 2 and the beginning of part
3. Three source-coordinate substitutions restore spelling in part 1; one
invalid source glyph is filled in `DREISSIGSTER` in part 3. Word spacing,
punctuation, abbreviation breaks and the omission of doubled separator `X`
characters in the reading above are editorial. The first reference
`B848727` and the difference between `NACHRCHEFX4` and `NACHRCHEFZ4` remain
literal; they are not regularized to each other.

## What this establishes

This message records an explicit reuse instruction:

| Intended December date | November key named by the instruction |
| --- | --- |
| 1 December | 10 November |
| Continuing dates (`USW`) | Corresponding continuation of the November sequence |
| 21 December | 30 November |

The first and last mappings are explicit; the intermediate daily mapping is
the ordinary interpretation of `USW` (“and so on”). This is evidence of what
was instructed. It is not independent proof that every station followed the
instruction or that a particular December intercept uses a specified key.

The earlier [p189 C instruction](../context/p189_C.md), including the raw word
`IRRTUM`, remains a separate source. The new schedule does not establish what
the earlier “error” meant. It does provide a concrete reason to examine
November/December key reuse without changing the wording of either message.

## Source identity and dates

The [source crop](../../experiments/open_targets_continuation/sources/childs_p211_selected.png)
is printed p211 / PDF p214. That page contains two different `B` labels under
different headings. This case concerns the **lower B**, following a new
**19 November 1918** heading:

```text
POT v NKJ (09.48 a.m., November 22d)
FUER POT COS VON LP SS DD 2230 3 TLE
1 TL: RICHI-214
2 TL: RICHI-184
3 TL: RICHI-134
```

The page heading, the 22 November receipt and the undated `2230` internal
time are all preserved. The later receipt does not justify relabelling the
published `Nov4-6` key, which directly decodes all three parts. These records
are locally named `p211_B_lower1`, `p211_B_lower2` and `p211_B_lower3` to avoid
confusing them with the upper B.

## Literal plaintext and exact repair costs

Part 1, 214 slots / 107 fixed plaintext positions:

```text
NOVEMBERXGINGBAHNSC7LUESSELNICHTVERNICHTENXNACHRCHEFX4XB848727XXDEZRMBERXRINGBAHNSCHLUESSELTRITTVORLAEUFIGX
```

The proposed `GINGBAHN→RINGBAHN`, `SC7LUESSEL→SCHLUESSEL` and
`DEZRMBER→DEZEMBER` each cost one known-coordinate substitution:
source indices **89: V→A**, **128: D→G** and **209: V→F**.
All other 211 coordinates stay unchanged.

Part 2, 184 slots / 92 fixed positions, needs no repair:

```text
NICHTINKRAFTXDAFUERSCHLUESSELERSTERDEZEMBERWIEZEHNTERNOVEMBERUSWBISEINUNDZWANZIGSTERDEZEMBER
```

Part 3, 134 slots / 66 of 67 fixed positions:

```text
WIEDREISSI?STERNOVEMBERXXEMPFANGSBESTAETIGUNGXXNACHRCHEFZ4XBX47857X
```

The printed `R` in `FRXXX` is outside the coordinate alphabet. Filling that
one slot, source index **16**, with `V` supplies the `G` in `DREISSIGSTER` and
preserves every one of the 133 valid coordinates. The three reconstructed
parts then re-encrypt exactly to the explicitly stated repaired witnesses.

## Verify

The [source inputs](../../experiments/open_targets_continuation/inputs.json)
and [certificates](../../experiments/open_targets_continuation/certificates.json)
retain the three separate geometries, all source indices, invalid glyphs and
proposed repairs.

```sh
python3 experiments/open_targets_continuation/verify.py --verify
```

The source checks and readable edition are by **icekylinx and GPT-6 Astra Pro**.
