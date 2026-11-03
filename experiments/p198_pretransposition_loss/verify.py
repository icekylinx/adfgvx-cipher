#!/usr/bin/env python3
"""Independently verify interim-loss witnesses, counts and tiny exact optima.

Prepared by icekylinx and GPT-6 Astra Pro. Default checks need only Python's
standard library. Optional frozen models additionally reproduce every stored
language score. No search is repeated by the default verifier.
"""
import argparse
from array import array
import hashlib
import json
from pathlib import Path
import sys

from validate_dp import enumerate_witnesses, label_score

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = "ADFGVX"
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse(cipher, ranks):
    # This uses sorted index traversal rather than run.py's column-height offsets.
    order = [position for column in sorted(range(len(ranks)), key=lambda c: ranks[c])
             for position in range(column, len(cipher), len(ranks))]
    stream, origins = [None] * len(cipher), [None] * len(cipher)
    for source, destination in enumerate(order):
        stream[destination], origins[destination] = cipher[source], source
    return "".join(stream), origins


def transpose(stream, ranks):
    return "".join(stream[position]
                   for column in sorted(range(len(ranks)), key=lambda c: ranks[c])
                   for position in range(column, len(stream), len(ranks)))


def decode(stream, square):
    assert len(stream) % 2 == 0
    return "".join(square[6 * CO.index(stream[i]) + CO.index(stream[i + 1])]
                   if stream[i] in CO and stream[i + 1] in CO else "?"
                   for i in range(0, len(stream), 2))


def encode(text, square):
    return "".join(CO[square.index(char) // 6] + CO[square.index(char) % 6] for char in text)


def edit_distance(a, b):
    row = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        next_row = [i]
        for j, cb in enumerate(b, 1):
            next_row.append(min(row[j] + 1, next_row[-1] + 1, row[j - 1] + (ca != cb)))
        row = next_row
    return row[-1]


def load_models(args, inputs):
    result = {}
    for name, path in [("book", args.book_model), ("radio", args.radio_model)]:
        if path is None:
            continue
        assert sha(path) == inputs["models"][name]["sha256"]
        model = array("f")
        model.frombytes(path.read_bytes())
        if sys.byteorder != "little":
            model.byteswap()
        assert len(model) == 37 ** 4
        result[name] = model
    return result


def inspect_run(job, row, models):
    result, key = row["result"], job["key"]
    assert row["key_id"] == key["id"] and row["square"] == key["square"]
    assert row["ranks"] == key["column_rank_order"]
    assert row["loss_count"] == job["loss_count"]
    assert row["received_ciphertext"] == job["received_ciphertext"]
    log = HERE / "results" / row["original_log"]
    assert sha(log) == row["original_log_sha256"] and json.loads(log.read_text()) == result
    assert result["completed"]
    observed, origins = inverse(job["received_ciphertext"], key["column_rank_order"])
    full, missing = result["full_interim"], result["missing_interim_indices"]
    assert len(full) == len(observed) + job["loss_count"]
    assert missing == sorted(set(missing)) and len(missing) == job["loss_count"]
    assert all(0 <= index < len(full) for index in missing)
    remaining = "".join(char for index, char in enumerate(full) if index not in missing)
    assert len(remaining) == len(observed)
    assert all(a == "?" or a == b for a, b in zip(observed, remaining))
    assert decode(full, key["square"]) == result["plaintext"]
    witness = row["witness"]
    assert witness["observed_interim"] == observed and witness["received_coordinate_origins"] == origins
    assert witness["reencrypted_received_witness"] == transpose(remaining, key["column_rank_order"])
    assert all(a == "?" or a == b for a, b in zip(job["received_ciphertext"], witness["reencrypted_received_witness"]))
    assert witness["valid_observations_unchanged"]
    assert result["states_expanded"] >= 1 and result["transitions_evaluated"] >= 1
    assert abs(result["score_sum"] / (len(result["plaintext"]) - 3) - result["score_mean"]) < 1e-12
    if row["model"] in models:
        assert abs(label_score(result["plaintext"], models[row["model"]]) - result["score_sum"]) < 1e-9
    truth = job.get("evaluation_only_truth")
    if truth:
        expected = truth["plaintext"]
        assert encode(expected, key["square"]) == truth["full_interim"]
        truth_remaining = "".join(char for index, char in enumerate(truth["full_interim"])
                                  if index not in truth["missing_interim_indices"])
        assert transpose(truth_remaining, key["column_rank_order"]) == job["received_ciphertext"]
        evaluation = row["evaluation"]
        assert evaluation["plaintext_exact"] == (result["plaintext"] == expected)
        assert evaluation["correct_characters"] == sum(a == b for a, b in zip(result["plaintext"], expected))
        assert evaluation["plaintext_positions"] == len(expected) == 85
        assert evaluation["full_interim_exact"] == (result["full_interim"] == truth["full_interim"])
        assert evaluation["loss_mask_exact"] == (missing == truth["missing_interim_indices"])
        assert evaluation["truth_not_supplied_to_optimizer"]
        if row["model"] in models:
            assert abs(label_score(expected, models[row["model"]]) - evaluation["truth_score_sum"]) < 1e-9
        assert result["score_sum"] + 1e-9 >= evaluation["truth_score_sum"]
        return {"id": row["id"], "model": row["model"],
                "mode": job["mode"], "plaintext_exact": evaluation["plaintext_exact"],
                "pointwise_correct": evaluation["correct_characters"],
                "levenshtein_distance": edit_distance(result["plaintext"], expected),
                "candidate_minus_truth_score": result["score_sum"] - evaluation["truth_score_sum"],
                "diagnosis": "exact text" if evaluation["plaintext_exact"] else "wrong candidate has strictly higher frozen-objective score",
                "loss_mask_exact": evaluation["loss_mask_exact"]}
    if "evaluation_only_conditional_target" in job:
        evaluation = row["evaluation"]
        expected = job["evaluation_only_conditional_target"]
        assert evaluation["reused_conditional_target_exact"] == (result["plaintext"] == expected)
        assert evaluation["agreement_with_conditional_target"] == sum(a == b for a, b in zip(result["plaintext"], expected))
        assert evaluation["selected_insertion"] == missing
        assert evaluation["reference_insertion"] == [job["reference_interim_insertion"]]
        assert evaluation["target_not_independent_truth"]
    return None


def rebuild(models):
    inputs = json.loads((HERE / "inputs.json").read_text())
    fixtures = []
    dataset_path = ROOT / "experiments/radio_domain_model/dataset.json"
    dataset = json.loads(dataset_path.read_text())
    training = dataset["training_records"]
    for fixture in inputs["source_fixtures"]:
        original = Path(fixture["source_path"])
        snapshot = HERE / "frozen_sources" / (original.parent.name + "_certificates.json")
        assert sha(snapshot) == fixture["source_sha256"]
        saved = json.loads(snapshot.read_text())
        record = next(r for r in saved["records"] if r["id"] == fixture["source_id"])
        text = record
        for field in fixture["source_field"].split("."):
            text = text[field]
        assert text[slice(*fixture["slice"])] == fixture["plaintext"]
        overlaps = [r["id"] for r in training if fixture["plaintext"] in r["plaintext_layer"]]
        assert not overlaps
        fixtures.append({"source_id": fixture["source_id"],
                         "snapshot": str(snapshot.relative_to(HERE)),
                         "sha256": sha(snapshot), "exact_85_character_radio_training_matches": overlaps})
    control_jobs = {r["id"]: r for r in inputs["controls"] + [inputs["reused_diagnostic"]]}
    target = inputs["historical"]
    for key in target["frozen_keys"]:
        assert sorted(key["column_rank_order"]) == list(range(1, len(key["column_rank_order"]) + 1))
        known = key["square"].replace("?", "")
        assert len(key["square"]) == 36 and len(known) == len(set(known))
        assert set(known) <= set(ABC[:-1])
    historical_jobs = {target["id"] + "__" + key["id"]: {
        "id": target["id"] + "__" + key["id"], "key": key,
        "received_ciphertext": target["received_ciphertext"], "loss_count": target["loss_count"]}
        for key in target["frozen_keys"]}
    reports, control_review = {}, []
    for stage, jobs, count in [("controls", control_jobs, 20), ("historical", historical_jobs, 50)]:
        saved = json.loads((HERE / "results" / (stage + ".json")).read_text())
        assert saved["inputs_sha256"] == sha(HERE / "inputs.json")
        assert saved["engine_source_sha256"] == sha(HERE / "interim_dp.cpp")
        assert saved["model_sha256"] == {name: item["sha256"] for name, item in inputs["models"].items()}
        assert saved["completed_jobs"] == len(saved["rows"]) == count and saved["pending_jobs"] == 0
        assert {(r["id"], r["model"]) for r in saved["rows"]} == {(id, model) for id in jobs for model in ["book", "radio"]}
        for row in saved["rows"]:
            review = inspect_run(jobs[row["id"]], row, models)
            if review:
                control_review.append(review)
        for field in ["states_expanded", "transitions_evaluated"]:
            assert saved[field] == sum(r["result"][field] for r in saved["rows"])
        reports[stage] = {field: saved[field] for field in ["completed_jobs", "pending_jobs", "states_expanded", "transitions_evaluated"]}
    assert len(control_review) == 18
    qualifying = [r["id"] + "__" + r["model"] for r in control_review
                  if r["mode"] != "one" and r["plaintext_exact"]]
    hist = json.loads((HERE / "results/historical.json").read_text())
    assert hist["qualifying_fresh_control_runs"] == qualifying and qualifying
    contiguous = json.loads((HERE / "results/contiguous.json").read_text())
    assert contiguous["inputs_sha256"] == sha(HERE / "inputs.json")
    assert contiguous["geometry_candidates"] == len(contiguous["rows"]) == 4150
    assert contiguous["score_evaluations"] == 8300
    by_key = {key["id"]: key for key in target["frozen_keys"]}
    assert {(r["key_id"], r["insert_before_interim_index"]) for r in contiguous["rows"]} == {
        (key, index) for key in by_key for index in range(166)}
    for row in contiguous["rows"]:
        key, index = by_key[row["key_id"]], row["insert_before_interim_index"]
        original, _ = inverse(target["received_ciphertext"], key["column_rank_order"])
        text = decode(original[:index] + "?" * 5 + original[index:], key["square"])
        assert text == row["partial_plaintext"] and row["fixed_label_positions"] == 85 - text.count("?")
        for name, model in models.items():
            assert abs(label_score(text, model) - row["score_sums"][name]) < 1e-9
    toy = json.loads((HERE / "results/toy_validation.json").read_text())
    assert toy["engine_source_sha256"] == sha(HERE / "interim_dp.cpp")
    synthetic = array("f", (-((index * 104729 + 17) % 9973) / 1000 for index in range(37 ** 4)))
    assert hashlib.sha256(synthetic.tobytes()).hexdigest() == toy["synthetic_model_sha256"]
    for record in toy["cases"]:
        count, best, example = enumerate_witnesses(record["observed_interim"], record["loss_count"], record["square"], synthetic)
        assert count == record["enumerated_witnesses"]
        assert best == record["independent_optimum_score"] == record["dp_result"]["score_sum"]
        assert example == record["independent_best_example"] and record["passed"]
        chosen = record["dp_result"]
        assert decode(chosen["full_interim"], record["square"]) == chosen["plaintext"]
        assert label_score(chosen["plaintext"], synthetic) == best
        mask = chosen["missing_interim_indices"]
        assert mask == sorted(set(mask)) and len(mask) == record["loss_count"]
        remaining = "".join(char for index, char in enumerate(chosen["full_interim"]) if index not in mask)
        assert len(remaining) == len(record["observed_interim"])
        assert all(a == "?" or a == b for a, b in zip(record["observed_interim"], remaining))
    assert sum(r["enumerated_witnesses"] for r in toy["cases"]) == toy["total_enumerated_witnesses"] == 9672
    assert toy["all_passed"]
    failures = [r for r in control_review if not r["plaintext_exact"]]
    assert all(r["candidate_minus_truth_score"] > 0 for r in failures)
    return {"schema": "adfgvx-interim-loss-independent-review-v1",
            "prepared_by": inputs["prepared_by"], "inputs_sha256": sha(HERE / "inputs.json"),
            "source_fixture_snapshots": fixtures, "radio_dataset_sha256": sha(dataset_path),
            "scope": reports, "completed_dp_jobs": 70, "pending_dp_jobs": 0,
            "total_states_expanded": sum(r["states_expanded"] for r in reports.values()),
            "total_transitions_evaluated": sum(r["transitions_evaluated"] for r in reports.values()),
            "contiguous_geometry_candidates": 4150, "contiguous_score_evaluations": 8300,
            "toy_exhaustive_cases": len(toy["cases"]), "toy_enumerated_witnesses": 9672,
            "fresh_control_runs": len(control_review), "fresh_control_bodies": 3,
            "fresh_control_exact_runs": sum(r["plaintext_exact"] for r in control_review),
            "fresh_control_failures": len(failures),
            "all_failed_controls_have_higher_scoring_wrong_candidate": True,
            "qualifying_five_loss_runs": qualifying, "control_review": control_review,
            "historical_accepted_plaintexts": 0,
            "limits": ["Fixed supplied ranks and square labels; partial squares remain partial and no unknown label assignments are optimized.",
                       "Scores across different amounts of unassigned square information are not comparable evidence for key identity; the entirely unknown example has a vacuous all-question-mark score of zero.",
                       "The 18 fresh run observations reuse three plaintexts and fixed keys across loss patterns and two related objectives.",
                       "The p126 A5 diagnostic is reused conditional evidence, not independently established historical truth.",
                       "Pointwise character agreement can be low when alternative losses shift a long otherwise matching passage; Levenshtein distance is also reported.",
                       "State and transition counters are actual completed DP operations, not counts of explicitly visited full loss-and-fill witnesses."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--book-model", type=Path)
    parser.add_argument("--radio-model", type=Path)
    args = parser.parse_args()
    inputs = json.loads((HERE / "inputs.json").read_text())
    models = load_models(args, inputs)
    result = rebuild(models)
    path = HERE / "review.json"
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, "dp_jobs": result["completed_dp_jobs"],
                      "contiguous_candidates": result["contiguous_geometry_candidates"],
                      "fresh_exact": result["fresh_control_exact_runs"],
                      "fresh_runs": result["fresh_control_runs"],
                      "independently_enumerated_toy_witnesses": result["toy_enumerated_witnesses"],
                      "score_models_recomputed": sorted(models)}, indent=2))


if __name__ == "__main__":
    main()
