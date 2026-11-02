#!/usr/bin/env python3
"""Audit cross-key readings and separately qualified square inferences.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro.
No language score establishes a source character. All offsets are zero based.
"""
from __future__ import annotations

import argparse
import datetime
import difflib
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt, plaintext_domains, untranspose

COORDS = "ADFGVX"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse(ciphertext, key):
    """Explicit column offsets, independent of the project permutation helper."""
    ranks, square = key["column_rank_order"], key["square"]
    width, length = len(ranks), len(ciphertext)
    assert sorted(ranks) == list(range(1, width + 1))
    assert length % 2 == 0 and len(square) == 36
    fixed = square.replace("?", "")
    assert len(set(fixed)) == len(fixed)
    unused = set(ALPHABET) - set(fixed)
    sizes = [length // width + (c < length % width) for c in range(width)]
    starts = [sum(sizes[d] for d in range(width) if ranks[d] < ranks[c])
              for c in range(width)]
    source_indices = [starts[p % width] + p // width for p in range(length)]
    interim = "".join(ciphertext[i] for i in source_indices)
    assert interim == untranspose(ciphertext, ranks)
    positions = []
    for p in range(length // 2):
        pair = interim[2*p:2*p+2]
        cells = [a*6+b for a in range(6) for b in range(6)
                 if pair[0] in ("?", COORDS[a])
                 and pair[1] in ("?", COORDS[b])]
        domain = set()
        for cell in cells:
            domain.update(unused if square[cell] == "?" else square[cell])
        positions.append({
            "plaintext_index": p,
            "source_indices": source_indices[2*p:2*p+2],
            "coordinate_pair": pair,
            "square_cells": cells,
            "domain": "".join(sorted(domain)),
            "raw": next(iter(domain)) if len(domain) == 1 else "?",
        })
    raw = "".join(p["raw"] for p in positions)
    assert raw == decrypt(ciphertext, ranks, square)
    assert [p["domain"] for p in positions] == plaintext_domains(ciphertext, ranks, square)
    rebuilt = [None] * length
    for i, c in zip(source_indices, interim):
        assert rebuilt[i] is None
        rebuilt[i] = c
    assert "".join(rebuilt) == ciphertext
    for p in positions:
        if p["raw"] != "?":
            cell = square.index(p["raw"])
            assert COORDS[cell//6] + COORDS[cell%6] == p["coordinate_pair"]
    return {"plaintext": raw, "fixed_positions": sum(p["raw"] != "?" for p in positions),
            "plaintext_positions": len(raw), "positions": positions,
            "all_source_slots_preserved": True,
            "independent_inverse_and_domains_agree": True}


def audit_message(message, key, corpus):
    literal = "".join("".join(message["source_rows"]).split())
    masked = "".join(c if c in COORDS else "?" for c in literal)
    assert len(literal) == message["declared_coordinate_length"]
    base = inverse(masked, key)
    assert base["plaintext"] == message["expected_raw"], message["id"]
    edited = list(masked)
    proposals = []
    seen = set()
    for proposal in message.get("editorial_patches", []):
        p, char = proposal["plaintext_index"], proposal["proposed_symbol"]
        assert p not in seen and char in key["square"] and char != "?"
        seen.add(p)
        original = base["positions"][p]
        cell = key["square"].index(char)
        desired = COORDS[cell//6] + COORDS[cell%6]
        edits = []
        for i, new in zip(original["source_indices"], desired):
            if masked[i] != new:
                edits.append({"source_index": i, "literal": literal[i],
                              "masked": masked[i], "proposed": new,
                              "kind": "erasure fill" if masked[i] == "?" else "known-coordinate substitution"})
                edited[i] = new
        proposals.append({**proposal, "raw": original["raw"],
                          "raw_domain": original["domain"],
                          "coordinate_edits": edits})
    edited = "".join(edited)
    candidate = inverse(edited, key)["plaintext"]
    for i, raw in enumerate(base["plaintext"]):
        if i not in seen:
            assert candidate[i] == raw
    if "?" not in candidate:
        assert encrypt(candidate, key["column_rank_order"], key["square"]) == edited
    ocr = "".join("".join(corpus[i]["groups"]) for i in message["ocr_blocks"])
    differences = [{"operation": op, "ocr_span": [a,b], "source_span": [c,d],
                    "ocr": ocr[a:b], "literal_source": literal[c:d]}
                   for op,a,b,c,d in difflib.SequenceMatcher(None, ocr, literal, autojunk=False).get_opcodes()
                   if op != "equal"]
    return {"id": message["id"], "key_id": key["id"],
            "literal_ciphertext": literal, "analysis_ciphertext": masked,
            "source_slots": len(literal), "observed_coordinates": sum(c in COORDS for c in literal),
            "source_erasures_and_invalid_glyphs": [{"source_index": i, "literal": c}
                                                   for i,c in enumerate(literal) if c not in COORDS],
            "ocr_comparison": differences, "direct": base,
            "editorial": {"plaintext": candidate, "ciphertext": edited,
                          "patches": proposals,
                          "known_coordinate_substitutions": sum(e["kind"] == "known-coordinate substitution"
                              for p in proposals for e in p["coordinate_edits"]),
                          "erasure_fills": sum(e["kind"] == "erasure fill"
                              for p in proposals for e in p["coordinate_edits"])}}


def check_links(inputs, results):
    rows = []
    for link in inputs["parallel_readings"]:
        a, b = results[link["a"]], results[link["b"]]
        ai, bi, length = link["a_start"], link["b_start"], link["length"]
        ar = a["direct"]["plaintext"][ai:ai+length]
        br = b["direct"]["plaintext"][bi:bi+length]
        ac = a["editorial"]["plaintext"][ai:ai+length]
        bc = b["editorial"]["plaintext"][bi:bi+length]
        assert len(ar) == len(br) == length and ac == bc
        rows.append({**link, "direct_a": ar, "direct_b": br,
                     "direct_equal_positions": sum(x == y and x != "?" for x,y in zip(ar,br)),
                     "editorial_parallel": ac,
                     "differences": [{"relative_index": i, "a": x, "b": y}
                                     for i,(x,y) in enumerate(zip(ar,br)) if x != y]})
    return rows


def conditional_square(inputs, results, keys):
    """Reproduce the consequences of explicitly supplied historical assumptions."""
    key = keys["Nov16-18"]
    square = list(key["square"])
    calendar = results["p204_A"]["direct"]
    assert calendar["plaintext"][33:43] == "MONTAGX1?X"
    pos = calendar["positions"][41]
    assert pos["coordinate_pair"] == "FD" and pos["square_cells"] == [13]
    days = [10+int(d) for d in pos["domain"]
            if datetime.date(1918, 11, 10+int(d)).weekday() == 0]
    assert days == [18]
    square[13] = "8"

    original = results["p201_B2"]["direct"]
    reference = results["p206_A2"]["direct"]
    op, rp = original["positions"][76:81], reference["positions"][154:159]
    assert original["plaintext"][76:81] == reference["plaintext"][154:159] == "11??2"
    assert [p["square_cells"] for p in op] == [p["square_cells"] for p in rp]
    assert original["positions"][78]["coordinate_pair"] == "FA"
    assert original["positions"][79]["coordinate_pair"] == "VV"
    assert reference["plaintext"][162:165] == "1?X"
    assert reference["positions"][163]["square_cells"] == [24]
    assert "OHL OP 15/11" in inputs["messages_by_id"]["p201_B1"]["header"]
    square[24] = "5"
    square = "".join(square)
    assert len(set(square.replace("?", ""))) == len(square.replace("?", ""))
    fixed_gain = []
    for rid in ("p204_A", "p201_B1", "p201_B2", "p206_A1", "p206_A2", "p206_A3"):
        base = results[rid]
        conditional = inverse(base["analysis_ciphertext"], {**key, "square": square})
        gained = [{"plaintext_index": i, "symbol": b, "coordinate_pair": base["direct"]["positions"][i]["coordinate_pair"]}
                  for i,(a,b) in enumerate(zip(base["direct"]["plaintext"], conditional["plaintext"]))
                  if a == "?" and b != "?"]
        fixed_gain.append({"id": rid, "conditional_plaintext": conditional["plaintext"], "gained_positions": gained})
    # A collateral package is treated as a checked local input, not a new source transcription.
    p205 = json.loads((ROOT / "experiments/corpus_joint/p205_inputs.json").read_text())
    collateral = []
    for record in p205["records"]:
        ct = "".join(record["source_groups"])
        base = inverse(ct, key)
        after = inverse(ct, {**key, "square": square})
        gained = [{"plaintext_index": i, "symbol": b, "coordinate_pair": base["positions"][i]["coordinate_pair"]}
                  for i,(a,b) in enumerate(zip(base["plaintext"],after["plaintext"])) if a == "?" and b != "?"]
        collateral.append({"id": record["id"], "conditional_plaintext": after["plaintext"], "gained_positions": gained})
    assert [(r["id"],p["plaintext_index"],p["symbol"]) for r in collateral for p in r["gained_positions"]] == [("p205_A4",86,"5")]
    return {"status": "conditional historical inference; published key remains unchanged",
            "key_id": key["id"], "published_square": key["square"], "conditional_square": square,
            "assumptions": inputs["conditional_inferences"],
            "calendar_possible_days_under_stated_month_and_weekday": days,
            "reference_number_square_cells": [p["square_cells"] for p in op],
            "local_consequences": fixed_gain, "p205_consequences": collateral,
            "unassigned_domain_after_two_inferences": "".join(sorted(set(ALPHABET)-set(square)))}


def build():
    inputs = json.loads((HERE / "inputs.json").read_text())
    keys = {k["id"]: k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]}
    corpus = {b["id"]: b for b in json.loads((ROOT / "experiments/p153_corpus/inputs.json").read_text())["blocks"]}
    for snapshot in inputs["keys"]:
        assert snapshot == keys[snapshot["id"]]
    for source in inputs["source_images"]:
        assert sha(HERE / source["path"]) == source["sha256"]
    results = {m["id"]: audit_message(m, keys[m["key_id"]], corpus) for m in inputs["messages"]}
    inputs["messages_by_id"] = {m["id"]: m for m in inputs["messages"]}
    return {"schema": "adfgvx-cross-key-source-audit-v1", "authors": "icekylinx and GPT-6 Astra Pro",
            "source_input_sha256": sha(HERE / "inputs.json"),
            "results": list(results.values()), "parallel_readings": check_links(inputs, results),
            "conditional_key_layer": conditional_square(inputs, results, keys),
            "summary": {"parts": len(results), "source_slots": sum(r["source_slots"] for r in results.values()),
                        "observed_coordinates": sum(r["observed_coordinates"] for r in results.values()),
                        "plaintext_positions": sum(r["direct"]["plaintext_positions"] for r in results.values()),
                        "directly_fixed_positions": sum(r["direct"]["fixed_positions"] for r in results.values()),
                        "editorial_known_coordinate_substitutions": sum(r["editorial"]["known_coordinate_substitutions"] for r in results.values()),
                        "editorial_erasure_fills": sum(r["editorial"]["erasure_fills"] for r in results.values())}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = build()
    target = HERE / "certificates.json"
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified" if args.verify else "written": True, **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
