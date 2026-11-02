#!/usr/bin/env python3
"""Verify p170 result arithmetic and provenance without rerunning annealing.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro.
The default verification uses the standard library and local repository data.
Optional binary models also check scores and the complete group-move ranking.
"""
from array import array
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from adfgvx.cipher import decrypt, encrypt

AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
CO = "ADFGVX"
COUNTERS = ("completed_restarts", "annealing_slots", "annealing_fitness_calls",
            "polish_fitness_calls", "total_fitness_calls")


def load(name):
    return json.loads((HERE / name).read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def independent_read(cipher, ranks, square):
    """Inverse physical-column reconstruction, independent of the core helper."""
    width = len(ranks)
    lengths = [len(range(column, len(cipher), width)) for column in range(width)]
    columns = [""] * width
    cursor = 0
    for column in sorted(range(width), key=lambda column: ranks[column]):
        columns[column] = cipher[cursor:cursor + lengths[column]]
        cursor += lengths[column]
    assert cursor == len(cipher)
    stream = "".join(columns[i % width][i // width] for i in range(len(cipher)))
    return "".join(square[6 * CO.index(stream[i]) + CO.index(stream[i + 1])]
                   for i in range(0, len(stream), 2))


def result(record, case, model=None):
    assert record["case"] == case
    best = record["best"]
    cipher, square, ranks = case["ciphertext"], best["square"], best["ranks"]
    anchor = case.get("partial_square", case.get("full_square"))
    assert len(cipher) == 106 and set(cipher) <= set(CO)
    assert len(square) == 36 and set(square) == set(AL)
    assert len(ranks) == case["width"] and sorted(ranks) == list(range(1, len(ranks) + 1))
    assert all(a == "?" or a == b for a, b in zip(anchor, square))
    assert best["known_square_cells"] == len(anchor.replace("?", ""))
    assert len(best["plaintexts"]) == 1 and len(best["plaintexts"][0]) == 53
    plain = best["plaintexts"][0]
    assert independent_read(cipher, ranks, square) == decrypt(cipher, ranks, square) == plain
    assert encrypt(plain, ranks, square) == cipher
    assert math.isfinite(best["score"])
    if model is not None:
        assert abs(score(plain, model) - best["score"]) < 1e-7
    if "evaluation_only" in case:
        truth = case["evaluation_only"]
        truth_square = truth.get("square", case.get("full_square"))
        assert all(a == "?" or a == b for a, b in zip(anchor, truth_square))
        assert encrypt(truth["plaintext"], truth["ranks"], truth_square) == cipher
        expected = {"correct_plaintext_positions": sum(a == b for a, b in zip(truth["plaintext"], plain)),
                    "plaintext_positions": 53, "exact_plaintext": truth["plaintext"] == plain,
                    "exact_ranks": truth["ranks"] == ranks}
        for key, value in expected.items():
            assert record["control_evaluation"][key] == value
        if "truth_score" in record["control_evaluation"] and model is not None:
            evaluation = record["control_evaluation"]
            assert abs(evaluation["truth_score"] - score(truth["plaintext"], model)) < 1e-7
            assert abs(evaluation["winning_candidate_score"] - score(plain, model)) < 1e-7
            assert abs(evaluation["truth_score_minus_winner"] -
                       (score(truth["plaintext"], model) - score(plain, model))) < 1e-7
        if "structural_evaluation" in record:
            expected = encrypt(truth["plaintext"], ranks, truth_square) == cipher
            assert record["structural_evaluation"]["truth_encrypts_under_returned_ranks_and_true_square"] == expected
            if model is not None:
                assert abs(record["structural_evaluation"]["planted_objective"] - score(truth["plaintext"], model)) < 1e-7
                assert abs(record["structural_evaluation"]["returned_objective"] - score(plain, model)) < 1e-7
    if "accepted_historical_plaintext" in record:
        assert record["accepted_historical_plaintext"] is False
    return {"id": case["id"], "baseline_square_fixed_plaintext_positions_at_returned_ranks":
            len(independent_read(cipher, ranks, anchor).replace("?", ""))}


def recipe(value, inputs, runner):
    assert value["inputs_sha256"] == sha(HERE / inputs)
    assert value["runner_sha256"] == sha(HERE / runner)
    if "engine_source_sha256" in value:
        assert value["engine_source_sha256"] == sha(HERE / "counted_anchored_joint.c")


def counts(record, complete_square=False):
    values = record["actual_search_counts"]
    settings = record["recipe"]["settings"]
    assert set(values) == set(COUNTERS)
    assert all(isinstance(value, int) and value >= 0 for value in values.values())
    assert values["completed_restarts"] == settings["restarts"]
    assert values["annealing_slots"] == settings["restarts"] * settings["iterations_per_restart"]
    assert values["annealing_fitness_calls"] <= values["annealing_slots"]
    if complete_square:
        assert values["annealing_fitness_calls"] == values["annealing_slots"]
    assert values["total_fitness_calls"] == (values["completed_restarts"] +
           values["annealing_fitness_calls"] + values["polish_fitness_calls"])


def total_counts(records):
    return {key: sum(record["actual_search_counts"][key] for record in records) for key in COUNTERS}


def score(text, model):
    v = [(AL + "?").index(c) for c in text]
    return sum(model[((a * 37 + b) * 37 + c) * 37 + d]
               for a, b, c, d in zip(v, v[1:], v[2:], v[3:])) / (len(v) - 3)


def read_model(path, expected):
    assert sha(path) == expected
    model = array("f")
    model.frombytes(path.read_bytes())
    if sys.byteorder == "big":
        model.byteswap()
    assert len(model) == 37 ** 4
    return model


def moves(cipher):
    groups, tail = [cipher[i:i + 5] for i in range(0, 105, 5)], cipher[105:]
    values = {cipher: [{"identity": True}]}
    for source in range(21):
        for target in range(21):
            if source == target:
                continue
            changed = groups.copy()
            changed.insert(target, changed.pop(source))
            values.setdefault("".join(changed) + tail, []).append({
                "received_group_0based": source,
                "insert_index_after_removal_0based": target})
    assert sum(map(len, values.values())) == 421
    return values


def group_row(row, possibilities, key, model=None):
    cipher = row["ciphertext"]
    assert row["operation_aliases"] == possibilities[cipher]
    plain = independent_read(cipher, key["column_rank_order"], key["square"])
    assert row["raw_plaintext"] == plain
    assert row["raw_fixed_positions"] == len(plain.replace("?", ""))
    if model is not None:
        assert abs(score(plain, model) - row["score"]) < 1e-7
    if "global_witness_not_used_in_ranking" in row:
        witness = row["global_witness_not_used_in_ranking"]
        assert witness["is_proposed_reading"] is False
        assert witness["ciphertext"] == cipher
        assert set(witness["square"]) == set(AL) and len(witness["square"]) == 36
        assert all(a == "?" or a == b for a, b in zip(key["square"], witness["square"]))
        assert encrypt(witness["plaintext"], key["column_rank_order"], witness["square"]) == cipher


def verify_groups(inputs, archived, keys, models):
    assert archived["inputs_sha256"] == sha(HERE / "group_move_inputs.json")
    dependency = inputs["source_dependency"]
    assert sha(ROOT / dependency["path"]) == dependency["sha256"]
    for key in inputs["keys"]:
        assert key["square"] == keys[key["id"]]["square"]
        assert key["column_rank_order"] == keys[key["id"]]["column_rank_order"]
    possibilities = moves(inputs["p170_ciphertext"])
    assert len(possibilities) == 401
    expected_jobs = {(key["id"], model) for key in inputs["keys"] for model in inputs["models"]}
    assert len(archived["historical"]) == len(expected_jobs) == 48
    assert {(r["key_id"], r["model"]) for r in archived["historical"]} == expected_jobs
    for record in archived["historical"]:
        key, model = keys[record["key_id"]], models.get(record["model"])
        assert record["operation_descriptions"] == 421
        assert record["distinct_candidate_ciphertexts"] == len(possibilities)
        assert record["accepted_plaintext"] is False and len(record["leaders"]) == 3
        for row in record["leaders"]:
            group_row(row, possibilities, key, model)
    controls = {case["id"]: case for case in inputs["controls"]}
    assert len(archived["controls"]) == 6
    assert {(record["id"], record["model"]) for record in archived["controls"]} == {
        (case_id, model) for case_id in controls for model in inputs["models"]}
    for record in archived["controls"]:
        case, key = controls[record["id"]], keys[record["key_id"]]
        possibilities = moves(case["received_ciphertext"])
        assert record["operation_descriptions"] == 421
        assert record["distinct_candidate_ciphertexts"] == len(possibilities)
        for row in (record["true_geometry"], record["leader"]):
            group_row(row, possibilities, key, models.get(record["model"]))
        assert record["true_geometry"]["ciphertext"] == case["true_ciphertext"]
        assert record["true_geometry"]["raw_plaintext"] == case["plaintext_evaluation_only"]
        assert record["exact_geometry_and_plaintext_leader"] == (record["leader"]["ciphertext"] == case["true_ciphertext"])
    assert archived["summary"] == {
        "fixed_key_pairs": 24, "models": 2,
        "historical_operation_descriptions_per_model": 10104,
        "historical_distinct_candidate_frames_per_model": 9624,
        "historical_score_evaluations": 19248, "controls": 3,
        "control_model_pairs": 6, "exact_control_leaders": 5,
        "accepted_historical_plaintexts": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book-model", type=Path)
    parser.add_argument("--radio-model", type=Path)
    parser.add_argument("--write-summary", action="store_true")
    args = parser.parse_args()
    inputs = load("cross_period_inputs.json")
    ri = load("radio_rank_inputs.json")
    hi = load("radio_historical_inputs.json")
    gi = load("group_move_inputs.json")
    models = {}
    for name, path in (("book", args.book_model), ("radio_mixture", args.radio_model)):
        if path:
            models[name] = read_model(path, ri["models"][name]["sha256"])
    keys = {key["id"]: key for key in json.loads((ROOT / "data/keys.json").read_text())["keys"]}
    source = next(m for m in json.loads((ROOT / "data/messages.json").read_text())["messages"] if m["id"] == "p170")
    cipher = source["transcript"]["analysis_ciphertext"]
    assert hashlib.sha256(cipher.encode()).hexdigest() == inputs["source_sha256"] == hi["source_ciphertext_sha256"]
    assert gi["p170_ciphertext"] == cipher
    for case in inputs["historical"] + inputs["controls"] + hi["cases"]:
        assert case["partial_square"] == keys[case["key_id"]]["square"]
        if "evaluation_only" not in case:
            assert case["ciphertext"] == cipher
    assert sha(ROOT / ri["dataset_path"]) == ri["dataset_sha256"]
    assert sha(HERE / "radio_rank_results.json") == hi["calibration_results_sha256"]
    prior = load("prior_scope_inventory.json")
    expected_prior = {(key, width) for key in inputs["scope"]["prior_completed_five_anchors"]
                      for width in inputs["scope"]["prior_five_widths"]}
    expected_prior |= {("CHI-Nov8-2026-recovery", width)
                       for width in inputs["scope"]["prior_scratch_chi8_widths"]}
    assert len(prior["records"]) == len(expected_prior) == 48
    assert {(record["key_id"], record["width"]) for record in prior["records"]} == expected_prior
    for record in prior["records"]:
        assert record["partial_square"] == keys[record["key_id"]]["square"]
        assert record["ciphertext_sha256"] == inputs["source_sha256"]
        assert record["configured_restarts"] == 1000
        assert record["configured_iterations_per_restart"] == 100000
        assert record["roundtrip_checked_at_inventory"] is True
        assert record["no_new_plaintext_accepted_by_this_inventory"] is True

    cross = load("cross_period_results.json")
    cross_summary = {}
    for section, cases, runner, restarts in (
        ("initial_controls", inputs["controls"], "run_cross_period.py", 1000),
        ("selected_failure_repeats", [inputs["controls"][i] for i in (3, 5)], "repeat_failed_controls.py", 5000),
        ("historical", inputs["historical"][:54], "run_cross_period.py", 1000)):
        campaign = cross[section]
        assert len(campaign["records"]) == len(cases)
        assert len(campaign["runtime_log_inventory"]) == len(cases)
        for record, case, log in zip(campaign["records"], cases, campaign["runtime_log_inventory"]):
            result(record, case, models.get("book"))
            provenance = record["provenance"]
            recipe(provenance, "cross_period_inputs.json", runner)
            assert provenance["restarts"] == restarts and provenance["iterations"] == 100000
            assert provenance["model_sha256"] == ri["models"]["book"]["sha256"]
            seed_suffix = "__independent_stronger_repeat" if section == "selected_failure_repeats" else "__fresh_20261102"
            assert record["seed"] == int(hashlib.sha256((case["id"] + seed_suffix).encode()).hexdigest()[:15], 16)
            assert log["case_id"] == case["id"] and log["improving_checkpoints"] >= 1
            assert log["final_checkpoint_is_archived_best"] is True
            assert len(log["sha256"]) == 64
            if "run" in campaign:
                assert record["provenance"] == campaign["run"]["recipe"]
                assert record["recipe_fingerprint"] == campaign["run"]["recipe_fingerprint"] == canonical(provenance)
        expected = {"completed": len(cases), "configured_proposal_slots": len(cases) * restarts * 100000}
        if section == "selected_failure_repeats":
            expected["exact_plaintexts"] = 1
        else:
            expected.update(controls=section == "initial_controls", accepted_historical_plaintexts=0)
            assert campaign["run"]["selected_cases"] == [case["id"] for case in cases]
            if section == "initial_controls":
                expected["exact_control_plaintexts"] = 4
        assert campaign["summary"] == expected
        if section != "historical":
            assert sum(record["control_evaluation"]["exact_plaintext"] for record in campaign["records"]) == (4 if section == "initial_controls" else 1)
        cross_summary[section] = expected

    rank = load("radio_rank_results.json")
    recipe(rank["run"]["recipe"], "radio_rank_inputs.json", "run_radio_rank.py")
    assert rank["run"]["recipe"]["settings"] == ri["settings_frozen_before_search"]
    assert rank["run"]["recipe"]["model_sha256"] == {
        name: value["sha256"] for name, value in ri["models"].items()}
    expected_jobs = [case["id"] + "__" + name for case in ri["controls"] for name in ri["models"]]
    assert rank["run"]["selected_jobs"] == expected_jobs
    assert len(rank["records"]) == 12
    for record, job in zip(rank["records"], expected_jobs):
        case = next(case for case in ri["controls"] if job == case["id"] + "__" + record["model"])
        result(record, case, models.get(record["model"]))
        assert record["recipe"] == rank["run"]["recipe"]
        assert record["recipe_fingerprint"] == rank["run"]["recipe_fingerprint"] == canonical(record["recipe"])
        counts(record, complete_square=True)
    per_model = {name: {"exact_plaintexts": sum(r["control_evaluation"]["exact_plaintext"] for r in rank["records"] if r["model"] == name), "control_count": 6} for name in ri["models"]}
    assert rank["summary"] == {"completed_jobs": 12, "per_model": per_model,
        "total_actual_counts": total_counts(rank["records"]), "historical_plaintexts_tested": 0}

    historical = load("radio_historical_results.json")
    recipe(historical["run"]["recipe"], "radio_historical_inputs.json", "run_radio_historical.py")
    assert historical["run"]["recipe"]["settings"] == hi["settings_frozen_before_historical_search"]
    assert historical["run"]["recipe"]["model_sha256"] == hi["model_sha256"]
    assert historical["run"]["selected_jobs"] == [case["id"] for case in hi["cases"]]
    assert len(historical["records"]) == len(hi["cases"]) == 28
    raw_known = []
    for record, case in zip(historical["records"], hi["cases"]):
        raw_known.append(result(record, case, models.get("radio_mixture")))
        assert record["recipe"] == historical["run"]["recipe"]
        assert record["recipe_fingerprint"] == historical["run"]["recipe_fingerprint"] == canonical(record["recipe"])
        counts(record)
    assert historical["summary"] == {"completed_jobs": 28, "accepted_historical_plaintexts": 0,
                                     "actual_search_counts": total_counts(historical["records"])}

    groups = load("group_move_results.json")
    verify_groups(gi, groups, keys, models)
    if args.book_model and args.radio_model:
        # Optional deterministic enumeration checks every ranking and tie, not
        # only the archived leaders. NumPy is needed by the original runner.
        from run_group_moves import run
        overrides = json.loads(json.dumps(gi))
        overrides["models"]["book"]["path"] = str(args.book_model.resolve())
        overrides["models"]["radio_mixture"]["path"] = str(args.radio_model.resolve())
        assert run(overrides) == groups

    summary = {"schema": "p170-new-methods-verification-v1",
               "prepared_by": "icekylinx and GPT-6 Astra Pro",
               "result_files_sha256": {name: sha(HERE / name) for name in (
                   "cross_period_results.json", "radio_rank_results.json",
                   "radio_historical_results.json", "group_move_results.json")},
               "prior_scope_inventory_sha256": sha(HERE / "prior_scope_inventory.json"),
               "prior_scope_jobs_excluded_from_new_campaign_budgets": 48,
               "cross_period": cross_summary, "radio_rank_controls": rank["summary"],
               "radio_historical": historical["summary"], "group_moves": groups["summary"],
               "group_move_control_score_evaluations": sum(
                   record["distinct_candidate_ciphertexts"] for record in groups["controls"]),
               "radio_historical_raw_known_counts": raw_known,
               "accepted_p170_plaintexts": 0,
               "limits": ["Arithmetic and provenance checks do not authenticate a historical reading.",
                          "No search nonrecovery excludes a key, width or damaged-source model.",
                          "Archived full-square witnesses do not fill the historical partial keys.",
                          "Exact recorded fitness-call counts are not distinct evaluated states.",
                          "The legacy configured_proposal_slots fields count loop slots, not exact fitness calls."]}
    path = HERE / "verification_summary.json"
    if args.write_summary:
        path.write_text(json.dumps(summary, indent=2) + "\n")
    else:
        assert load(path.name) == summary
    print(json.dumps({"verified": True, "optional_score_models": sorted(models),
                      "full_group_ranking_recomputed": bool(args.book_model and args.radio_model),
                      **{key: summary[key] for key in ("cross_period", "radio_rank_controls", "radio_historical", "group_moves", "accepted_p170_plaintexts")}}, indent=2))


if __name__ == "__main__":
    main()
