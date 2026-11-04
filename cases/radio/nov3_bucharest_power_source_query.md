# Bucharest dispatch enquiry and power-source specifications

[Case index](../README.md) · [ADFGVX Cipher](../../README.md) · [Reading conventions](../../docs/reading-conventions.md)


**Reviewed source crops:** [p109_A2.png](../../experiments/nov3_bucharest_power_source/sources/p109_A2.png) · [p109_A3.png](../../experiments/nov3_bucharest_power_source/sources/p109_A3.png). [File and pixel verification](../../sources/reviewed-crops.md#verify).
## p109 A2

**Status:** 81/81 native raw positions fixed; 4 coordinate substitutions and 0 source-mask fills. No frame change.

**Source and dates:** Page heading: 3rd NOVEMBER, 1918; A) UKS v OSM (2.09 a.m., November 3rd); VE; 2 TL RICHI-162.

[Source p109 A2 — source-PDF reference](../../experiments/nov3_bucharest_power_source/inputs.json)

<details>
<summary>Source and cipher evidence</summary>

**Raw output:**

```text
GLEICSTVOMOHNEKRAFTQELLEVEDSANDBERBITXBEINACHRCEFANGEFRAGTOBBUKARESTSENDENSOLLENX
```

**Edited output — counted proposal:**

```text
GLEICSTROMOHNEKRAFTQELLEVERSANDBEREITXBEINACHRCEFANGEFRAGTOBBUKARESTSENDENSOLLENX
```

</details>

**Readable German — the same candidate labels with spacing and punctuation:**

> Gleicstrom ohne Kraftqelle versandbereit. Bei Nachrcef angefragt, ob Bukarest senden sollen.

**Meaning:** The fragment reports readiness for dispatch without a power source and says that the office represented by NACHRCEF was asked whether the item should be sent to Bucharest. It does not confirm that dispatch took place. The exact item is not identified by this surviving part alone.

**Conditional interpretation and source details:** All 162 original coordinates are present, including the final VA omitted by the earlier OCR block. Four observed-coordinate substitutions propose GLEICSTROM, VERSAND and BEREIT for GLEICSTVOM, VEDSAND and BERBIT. The residual forms GLEICSTROM, KRAFTQELLE and NACHRCEF are retained exactly: no missing H or U is added to produce fluent modern spellings. This is the source-defined second part; the first part is outside this edition. The following third part supplies a direct power-source query but does not establish that equipment was obtained or transported.

### Explicit source changes

All indices are zero-based.

| Source index | Printed | Proposed | Cost |
|---:|---|---|---|
| 3 | `G` | `V` | Observed-coordinate substitution |
| 10 | `G` | `D` | Observed-coordinate substitution |
| 105 | `V` | `G` | Observed-coordinate substitution |
| 110 | `G` | `A` | Observed-coordinate substitution |

## p109 A3

**Status:** 114/114 native raw positions fixed; 0 coordinate substitutions and 0 source-mask fills. No frame change.

**Source and dates:** Same A heading and reception as p109 A2; 3 TL RICHI-228.

[Source p109 A3 — source-PDF reference](../../experiments/nov3_bucharest_power_source/inputs.json)

<details>
<summary>Raw decoded text</summary>

**Raw output:**

```text
ISTKRAFTQELLEMOTORETWA50PSMIT220VOLTGLEICHSTRDYNAMO25KWDORTBESCHAFFBARODERTRIEBWXKRAFTANLAGEVERWENDBARXFUNKANTWORT
```

</details>

**Readable German — the same candidate labels with spacing and punctuation:**

> Ist Kraftqelle, Motor etwa 50 PS mit 220 Volt Gleichstr. Dynamo 25 KW, dort beschaffbar oder Triebw. Kraftanlage verwendbar; Funkantwort.

**Meaning:** Asks whether a power source—a motor of about 50 PS with a 220-volt direct-current dynamo rated 25 kW—can be procured there, or whether the power installation denoted TRIEBW can be used. Requests a radio reply. The message asks about availability and does not establish that the equipment exists there or was sent.

**Conditional interpretation and source details:** All 228 observed coordinates yield 114 fixed plaintext positions without any substitution, fill, deletion or insertion. The quantities 50PS, 220VOLT and 25KW are direct raw labels. The source final group is FXX, whereas earlier OCR had FAX. KRAFTQELLE remains the literal spelling; GLEICHSTR and TRIEBW remain abbreviations, and TRIEBW is not expanded into a particular vehicle or plant type. The semicolon before FUNKANTWORT is editorial punctuation only.

### Explicit source changes

No source-coordinate substitution or source-mask fill is used.

### Reproducibility and attribution

The [input](../../experiments/nov3_bucharest_power_source/inputs.json) binds each literal source to exact PDF crops. The [certificate](../../experiments/nov3_bucharest_power_source/certificates.json) contains the raw paired-coordinate domains, each source change and the forward checks. The [verifier](../../experiments/nov3_bucharest_power_source/verify.py) checks the unchanged published keys and the live German quotations, retaining all numerical and letter labels.

Source edition and verification: icekylinx and GPT-6 Astra Pro (2026). Childs supplies the historical collection; published reconstruction and key provenance credit Lasry, Niebel, Kopal and Wacker. Earlier repository OCR and body readings are retained in the [attribution record](../../experiments/nov3_bucharest_power_source/prior_candidates.json).
