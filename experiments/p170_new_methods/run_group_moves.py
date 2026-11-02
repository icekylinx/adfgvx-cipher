#!/usr/bin/env python3
"""Transfer p191's single printed-group displacement to p170.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
Ranks and known square cells are fixed; unknown cells remain unknown.
"""
from pathlib import Path
import argparse
import json
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt
from experiments.withdrawal_recovery.verify import reading, sha
from experiments.operational_recovery.verify import global_witness

AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?"


def enumerate_moves(cipher):
    assert len(cipher) == 106
    groups = [cipher[i:i + 5] for i in range(0, 105, 5)]
    tail = cipher[105:]
    outputs = {cipher: [{"identity": True}]}
    operations = 1
    for source in range(21):
        for target in range(21):
            if source == target:
                continue
            g = groups.copy()
            g.insert(target, g.pop(source))
            changed = "".join(g) + tail
            assert sorted(changed) == sorted(cipher)
            outputs.setdefault(changed, []).append({"received_group_0based": source,
                                                    "insert_index_after_removal_0based": target})
            operations += 1
    assert operations == 421
    return outputs


def score(text, model):
    n = [AL.index(c) for c in text]
    return sum(float(model[((a * 37 + b) * 37 + c) * 37 + d])
               for a, b, c, d in zip(n, n[1:], n[2:], n[3:])) / (len(n) - 3)


def ranked(cipher, key, model):
    cases = enumerate_moves(cipher)
    rows = []
    for changed, aliases in cases.items():
        plain = decrypt(changed, key["column_rank_order"], key["square"])
        rows.append({"ciphertext": changed, "operation_aliases": aliases,
                     "raw_plaintext": plain, "raw_fixed_positions": len(plain) - plain.count("?"),
                     "score": score(plain, model)})
    rows.sort(key=lambda r: (-r["score"], r["ciphertext"]))
    return rows


def run(inputs):
    dependency = inputs["source_dependency"]
    assert sha(ROOT / dependency["path"]) == dependency["sha256"]
    models = {}
    for name, definition in inputs["models"].items():
        path = Path(definition["path"])
        assert sha(path) == definition["sha256"]
        models[name] = np.fromfile(path, dtype="<f4")
        assert len(models[name]) == 37 ** 4
    keys = {k["id"]: k for k in inputs["keys"]}
    current = {k["id"]: k for k in json.loads((ROOT / "data/keys.json").read_text())["keys"]}
    for key in keys.values():
        assert key["square"] == current[key["id"]]["square"]
        assert key["column_rank_order"] == current[key["id"]]["column_rank_order"]
    historical = []
    controls = []
    for name, model in models.items():
        for key in keys.values():
            rows = ranked(inputs["p170_ciphertext"], key, model)
            leaders = rows[:3]
            for row in leaders:
                value = reading(row["ciphertext"], key["column_rank_order"], key["square"])
                assert value["plaintext"] == row["raw_plaintext"]
                row["global_witness_not_used_in_ranking"] = global_witness(
                    row["ciphertext"], key["column_rank_order"], key["square"], value)
            historical.append({"key_id": key["id"], "model": name,
                               "operation_descriptions": 421,
                               "distinct_candidate_ciphertexts": len(rows),
                               "leaders": leaders,
                               "identity_score": next(r["score"] for r in rows if r["ciphertext"] == inputs["p170_ciphertext"]),
                               "accepted_plaintext": False})
        for control in inputs["controls"]:
            key = keys[control["key_id"]]
            rows = ranked(control["received_ciphertext"], key, model)
            truth = next(r for r in rows if r["ciphertext"] == control["true_ciphertext"])
            assert truth["raw_plaintext"] == control["plaintext_evaluation_only"]
            rank = 1 + sum(r["score"] > truth["score"] for r in rows)
            controls.append({"id": control["id"], "key_id": key["id"], "model": name,
                             "operation_descriptions": 421,
                             "distinct_candidate_ciphertexts": len(rows),
                             "true_geometry_rank_with_ties": rank,
                             "score_ties_at_true_geometry": sum(r["score"] == truth["score"] for r in rows),
                             "true_geometry": truth, "leader": rows[0],
                             "exact_geometry_and_plaintext_leader": rows[0]["ciphertext"] == control["true_ciphertext"]})
    return {"schema": "p170-single-group-move-results-v1", "prepared_by": inputs["prepared_by"],
            "inputs_sha256": sha(HERE / "group_move_inputs.json"),
            "summary": {"fixed_key_pairs": len(keys), "models": len(models),
                        "historical_operation_descriptions_per_model": 421 * len(keys),
                        "historical_distinct_candidate_frames_per_model": sum(
                            r["distinct_candidate_ciphertexts"] for r in historical if r["model"] == "book"),
                        "historical_score_evaluations": sum(r["distinct_candidate_ciphertexts"] for r in historical),
                        "controls": len(inputs["controls"]),
                        "control_model_pairs": len(controls),
                        "exact_control_leaders": sum(r["exact_geometry_and_plaintext_leader"] for r in controls),
                        "accepted_historical_plaintexts": 0},
            "historical": historical, "controls": controls}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    inputs = json.loads((HERE / "group_move_inputs.json").read_text())
    result = run(inputs)
    target = HERE / "group_move_results.json"
    if args.verify:
        assert result == json.loads(target.read_text())
    else:
        target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, **result["summary"]}, indent=2))
    for row in result["controls"]:
        print(json.dumps({k: row[k] for k in ["id", "model", "true_geometry_rank_with_ties", "exact_geometry_and_plaintext_leader"]}))


if __name__ == "__main__":
    main()
