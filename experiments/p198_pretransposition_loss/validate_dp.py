#!/usr/bin/env python3
"""Compare the C++ DP with an independent tiny exhaustive enumerator.

Prepared by icekylinx and GPT-6 Astra Pro. A deterministic synthetic objective
avoids dependence on external language models. Tests cover one/two inserted
coordinates, a received erasure, complete and partial squares, and all four
within-pair consumption modes. This checks arithmetic, not language quality.
"""
from array import array
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
CO = "ADFGVX"
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?"


def label_score(text, model):
    values = [ABC.index(char) for char in text]
    return sum(model[((a * 37 + b) * 37 + c) * 37 + d]
               for a, b, c, d in zip(values, values[1:], values[2:], values[3:]))


def enumerate_witnesses(observed, losses, square, model):
    total = len(observed) + losses
    count, best = 0, float("-inf")
    best_example = None
    for mask in itertools.combinations(range(total), losses):
        missing = set(mask)
        skeleton, consumed = [], 0
        for index in range(total):
            if index in missing:
                skeleton.append("?")
            else:
                skeleton.append(observed[consumed])
                consumed += 1
        unknown = [index for index, char in enumerate(skeleton) if char == "?"]
        for values in itertools.product(CO, repeat=len(unknown)):
            full = list(skeleton)
            for index, char in zip(unknown, values):
                full[index] = char
            text = "".join(square[6 * CO.index(a) + CO.index(b)]
                           for a, b in zip(full[::2], full[1::2]))
            score = label_score(text, model)
            count += 1
            if score > best:
                best = score
                best_example = {"plaintext": text, "full_interim": "".join(full),
                                "missing_interim_indices": list(mask)}
    return count, best, best_example


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=HERE / "results/toy_validation.json")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    full = "D5613Q9KBNO0HY8EISJUTZFCW7VPML2ARG4X"
    partial = "H??BMUF15PX0DJLR????S6VONKZ?AWITEGC?"
    fixtures = [
        ("one_full", "ADFGVXA", 1, full),
        ("two_full", "GXADFVVX", 2, full),
        ("one_with_erasure", "AX?GDVF", 1, full),
        ("two_with_erasure", "V?AFGX", 2, full),
        ("one_partial", "GXXAVDF", 1, partial),
        ("two_partial", "FADGVXAX", 2, partial),
    ]
    model = array("f", (-((index * 104729 + 17) % 9973) / 1000
                        for index in range(37 ** 4)))
    records = []
    with tempfile.TemporaryDirectory(prefix="adfgvx-interim-dp-check-") as temporary:
        path = Path(temporary) / "synthetic37.bin"
        path.write_bytes(model.tobytes())
        for label, observed, losses, square in fixtures:
            result = json.loads(subprocess.run(
                [str(args.engine), str(path), square, str(losses), observed],
                check=True, capture_output=True, text=True).stdout)
            count, best, example = enumerate_witnesses(observed, losses, square, model)
            assert abs(result["score_sum"] - best) < 1e-12
            assert abs(label_score(result["plaintext"], model) - best) < 1e-12
            shortened = "".join(char for i, char in enumerate(result["full_interim"])
                                if i not in result["missing_interim_indices"])
            assert len(shortened) == len(observed)
            assert all(a == "?" or a == b for a, b in zip(observed, shortened))
            records.append({"id": label, "observed_interim": observed, "loss_count": losses,
                            "square": square, "enumerated_witnesses": count,
                            "independent_optimum_score": best,
                            "independent_best_example": example,
                            "dp_result": {key: result[key] for key in [
                                "plaintext", "full_interim", "missing_interim_indices", "score_sum"]},
                            "passed": True})
    result = {"schema": "adfgvx-interim-dp-small-exhaustive-validation-v1",
              "prepared_by": ["icekylinx", "GPT-6 Astra Pro"],
              "engine_source_sha256": hashlib.sha256((HERE / "interim_dp.cpp").read_bytes()).hexdigest(),
              "synthetic_model_rule": "float32(-((index * 104729 + 17) % 9973) / 1000), base37 ABC...Z0123456789? quadruple order",
              "synthetic_model_sha256": hashlib.sha256(model.tobytes()).hexdigest(),
              "total_enumerated_witnesses": sum(r["enumerated_witnesses"] for r in records),
              "cases": records, "all_passed": True}
    if args.verify:
        assert result == json.loads(args.output.read_text())
    else:
        assert not args.output.exists(), "Refusing to overwrite original validation"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"verified": args.verify, "cases": len(records),
                      "enumerated_witnesses": result["total_enumerated_witnesses"],
                      "all_passed": True}, indent=2))


if __name__ == "__main__":
    main()
