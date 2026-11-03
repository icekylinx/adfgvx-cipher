#!/usr/bin/env python3
"""Replay bounded, unaccepted odd-fragment diagnostics.

Default: standard-library source/hash, retained geometry/plaintext and count
checks. --quad additionally re-enumerates every scored configuration using
NumPy. --pdf checks the two freshly bound crop images against the primary PDF.
Prepared by icekylinx and GPT-6 Astra Pro.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import itertools
import json
import math

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CO = "ADFGVX"
AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?"
KINDS = ("insert_transmitted", "delete_transmitted", "insert_fractionated", "delete_fractionated")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def inverse_indices(n, ranks):
    """Independent column placement; preserves odd intermediate streams."""
    columns = [[] for _ in ranks]
    offset = 0
    for column in sorted(range(len(ranks)), key=lambda i: ranks[i]):
        length = len(range(column, n, len(ranks)))
        columns[column] = list(range(offset, offset + length))
        offset += length
    assert offset == n
    return [columns[i % len(ranks)][i // len(ranks)] for i in range(n)]


def inverse(text, ranks):
    return "".join(text[i] for i in inverse_indices(len(text), ranks))


def decode_middle(text, square):
    assert len(text) % 2 == 0
    unused = set(AL[:-1]) - set(square)
    domains = []
    for i in range(0, len(text), 2):
        values = set()
        for a in CO if text[i] == "?" else text[i]:
            for b in CO if text[i + 1] == "?" else text[i + 1]:
                value = square[CO.index(a) * 6 + CO.index(b)]
                values.update(unused if value == "?" else value)
        domains.append("".join(sorted(values)))
    raw = "".join(d if len(d) == 1 else "?" for d in domains)
    return raw, [{"position": i, "domain": d} for i, d in enumerate(domains) if len(d) != 1]


def known_windows(raw):
    return sum("?" not in raw[i:i + 4] for i in range(len(raw) - 3))


def location(candidate):
    if "insert_source_boundary" in candidate:
        return candidate["insert_source_boundary"], candidate["insert_value"]
    return candidate.get("index", candidate.get("boundary_or_index")), candidate["fill"]


def replay(source, key, kind, index, fill):
    text = source if kind.endswith("transmitted") else inverse(source, key["column_rank_order"])
    if kind.startswith("insert"):
        assert 0 <= index <= len(text) and fill in CO
        text = text[:index] + fill + text[index:]
    else:
        assert 0 <= index < len(text) and fill is None
        text = text[:index] + text[index + 1:]
    if kind.endswith("transmitted"):
        text = inverse(text, key["column_rank_order"])
    return decode_middle(text, key["square"])[0]


def threshold(record, plain_length):
    rule = record["minimum_known_quad_rule"]
    if rule["kind"] == "absolute":
        return rule["minimum"]
    return (plain_length - 3) * rule["numerator"] // rule["denominator"]


def all_scores(source, key, kind, minimum, quad, np):
    """Optional full finite enumeration, with the historical exclusion rule."""
    text = source if kind.endswith("transmitted") else inverse(source, key["column_rank_order"])
    base = np.array([CO.index(c) for c in text], dtype=np.int16)
    if kind.startswith("insert"):
        frames = np.stack([np.insert(base, i, c) for i in range(len(base) + 1) for c in range(6)])
    else:
        frames = np.stack([np.delete(base, i) for i in range(len(base))])
    if kind.endswith("transmitted"):
        frames = frames[:, inverse_indices(frames.shape[1], key["column_rank_order"])]
    square = np.array([AL.index(c) for c in key["square"]], dtype=np.int32)
    plain = square[frames[:, ::2] * 6 + frames[:, 1::2]]
    valid = (plain[:, :-3] < 36) & (plain[:, 1:-2] < 36) & (plain[:, 2:-1] < 36) & (plain[:, 3:] < 36)
    coverage = valid.sum(axis=1)
    indices = ((plain[:, :-3] * 37 + plain[:, 1:-2]) * 37 + plain[:, 2:-1]) * 37 + plain[:, 3:]
    sums = np.where(valid, quad[indices], 0).sum(axis=1, dtype=np.float64)
    scores = np.divide(sums, coverage, out=np.full(len(frames), -100.), where=coverage > 0)
    scores = np.where(coverage >= minimum, scores, -100.)
    return scores, coverage


def verify(quad_path=None, pdf_path=None):
    inputs = read(HERE / "inputs.json")
    certificate = read(HERE / "certificate.json")
    assert sha(HERE / "inputs.json") == certificate["inputs_sha256"]
    for row in inputs["original_files"] + inputs["images"]:
        assert sha(HERE / row["path"]) == row["sha256"], row["path"]
    for row in inputs["dependencies"] + [inputs["key_file"]]:
        assert sha(ROOT / row["path"]) == row["sha256"], row["path"]
    keys = read(ROOT / inputs["key_file"]["path"])["keys"]
    assert len(keys) == 25
    key_map = {key["id"]: key for key in keys}
    records = {r["id"]: r for r in inputs["records"]}
    sources = {ident: "".join("".join(row["source_rows"]).split()) for ident, row in records.items()}
    for ident, source in sources.items():
        assert len(source) == records[ident]["literal_source_slots"]
        assert set(source) <= set(CO)
    source_tree = ast.parse((HERE / "original/p159_transcription_origin.py").read_text())
    original_p159 = [ast.literal_eval(n.value) for n in source_tree.body
                     if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Subscript)
                     and ast.literal_eval(n.targets[0].slice) == "p159_A"]
    assert len(original_p159) == 1 and "".join(original_p159[0].split()) == sources["p159_A"]
    source_tree = ast.parse((HERE / "original/p162_rows.py").read_text())
    original_p162 = ast.literal_eval(source_tree.body[0].value)["p162_C1"]
    assert "".join(original_p162.split()) == sources["p162_C1"]
    upstream = read(ROOT / inputs["dependencies"][0]["path"])
    prior = next(r for r in upstream["records"] if r["id"] == "p163_A_unlabelled")
    assert sources["p163_unlabelled"] == "".join("".join(prior["source_rows"]).split())
    quad = np = None
    if quad_path:
        import numpy as np
        assert sha(quad_path) == inputs["model_sha256"]
        quad = np.fromfile(quad_path, dtype="<f4")
        assert len(quad) == 37 ** 4 and np.isfinite(quad).all()
    reports = [
        ("p159_A", "p159_one_insert_all_keys.json", "insert_transmitted", 30),
        ("p159_A", "p159_phase_screen.json", None, 30),
        ("p162_C1", "p162_C1_four_models.json", None, 40),
        ("p163_unlabelled", "p163_unlabelled_four_models.json", None, 40),
    ]
    count_by_record = dict.fromkeys(records, 0)
    configurations = retained = runs_checked = cutoff_ties = 0
    for ident, filename, forced_kind, top_limit in reports:
        result = read(HERE / "original" / filename)
        assert result["literal_source"] == sources[ident]
        assert result["model_sha256"] == inputs["model_sha256"]
        expected_kinds = [forced_kind] if forced_kind else (["insert_fractionated", "delete_fractionated", "delete_transmitted"] if ident == "p159_A" else list(KINDS))
        expected_order = [(k["id"], kind) for k in keys for kind in expected_kinds]
        assert [(r["key_id"], forced_kind or r["kind"]) for r in result["runs"]] == expected_order
        eligible = []
        total = 0
        for run in result["runs"]:
            key = key_map[run["key_id"]]
            kind = forced_kind or run["kind"]
            size = (len(sources[ident]) + 1) * 6 if kind.startswith("insert") else len(sources[ident])
            assert run["evaluations"] == size and len(run["top"]) == 5
            minimum = threshold(records[ident], (len(sources[ident]) + (1 if kind.startswith("insert") else -1)) // 2)
            if "min_known_windows" in run:
                assert run["min_known_windows"] == minimum
            scores = coverage = None
            if quad is not None:
                scores, coverage = all_scores(sources[ident], key, kind, minimum, quad, np)
                assert len(scores) == size
                cutoff = float(np.sort(scores)[-5])
            for candidate in run["top"]:
                assert candidate["key_id"] == key["id"]
                assert candidate.get("kind", kind) == kind
                index, fill = location(candidate)
                raw = replay(sources[ident], key, kind, index, fill)
                assert raw == candidate["plaintext"]
                known = known_windows(raw)
                assert known == candidate.get("known_quad_windows", candidate.get("known_windows"))
                is_eligible = candidate.get("eligible_for_ranking", candidate.get("eligible"))
                assert is_eligible == (known >= minimum)
                assert math.isfinite(candidate["score"])
                if not is_eligible:
                    assert candidate["score"] == -100.
                if quad is not None:
                    flat = index * 6 + CO.index(fill) if fill is not None else index
                    assert int(coverage[flat]) == known
                    assert math.isclose(float(scores[flat]), candidate["score"], rel_tol=0., abs_tol=1e-12)
                    assert float(scores[flat]) >= cutoff - 1e-12
                    cutoff_ties += int(float(scores[flat]) == cutoff)
                retained += 1
                if is_eligible:
                    eligible.append(candidate)
            assert len({location(c) for c in run["top"]}) == 5
            assert all(a["score"] >= b["score"] for a, b in zip(run["top"], run["top"][1:]))
            runs_checked += 1
            total += size
        assert total == result["total_evaluations"]
        assert sorted(eligible, key=lambda r: -r["score"])[:top_limit] == result["top"]
        count_by_record[ident] += total
        configurations += total
    assert count_by_record == {k: v["single_change_evaluations"] for k, v in records.items()}
    prefix_count = 0
    for ident, filename in [("p162_C1", "p162_C1_prefix_suffix.json"), ("p163_unlabelled", "p163_prefix_suffix.json")]:
        rows = read(HERE / "original" / filename)
        assert len(rows) == 102
        assert {(r["gap"], r["end"]) for r in rows} == {(gap, end) for gap in range(1, 102, 2) for end in ("prefix", "suffix")}
        key = key_map["Nov7-9"]
        for row in rows:
            frame = "?" * row["gap"] + sources[ident] if row["end"] == "prefix" else sources[ident] + "?" * row["gap"]
            raw, domains = decode_middle(inverse(frame, key["column_rank_order"]), key["square"])
            assert (raw, domains) == (row["plaintext"], row["domains"])
            known = known_windows(raw)
            assert known == row["known_windows"]
            if known < 12:
                assert row["score"] == -100.
            if quad is not None:
                indices = []
                for i in range(len(raw) - 3):
                    gram = raw[i:i + 4]
                    if "?" not in gram:
                        value = 0
                        for ch in gram:
                            value = value * 37 + AL.index(ch)
                        indices.append(value)
                score = float(quad[indices].mean(dtype=np.float64)) if known >= 12 else -100.
                assert math.isclose(score, row["score"], rel_tol=0., abs_tol=1e-12)
            prefix_count += 1
        assert all(a["score"] >= b["score"] for a, b in zip(rows, rows[1:]))
    near = read(HERE / "original/p159_near_key_screen.json")
    assert near["source"] == sources["p159_A"]
    assert near["published_key_id"] == "Nov7-9" and near["model_sha256"] == inputs["model_sha256"]
    pairs = [None] + [list(pair) for pair in itertools.combinations(range(20), 2)]
    assert near["key_variants"] == 191 and len(near["runs"]) == 191
    assert [r["swapped_column_positions"] for r in near["runs"]] == pairs
    near_candidates = []
    near_evaluations = 0
    for run in near["runs"]:
        key = dict(key_map["Nov7-9"])
        ranks = list(key["column_rank_order"])
        pair = run["swapped_column_positions"]
        if pair is not None:
            ranks[pair[0]], ranks[pair[1]] = ranks[pair[1]], ranks[pair[0]]
        assert run["ranks"] == ranks
        key["column_rank_order"] = ranks
        assert run["evaluations"] == 1632 and len(run["top"]) == 3
        if quad is not None:
            scores, coverage = all_scores(sources["p159_A"], key, "insert_transmitted", 100, quad, np)
            cutoff = float(np.sort(scores)[-3])
        for candidate in run["top"]:
            assert candidate["swapped_column_positions"] == pair
            index, fill = location(candidate)
            raw = replay(sources["p159_A"], key, "insert_transmitted", index, fill)
            assert raw == candidate["plaintext"]
            known = known_windows(raw)
            assert known == candidate["known_quad_windows"]
            assert math.isfinite(candidate["score"])
            if known < 100:
                assert candidate["score"] == -100.
            if quad is not None:
                flat = index * 6 + CO.index(fill)
                assert int(coverage[flat]) == known
                assert math.isclose(float(scores[flat]), candidate["score"], rel_tol=0., abs_tol=1e-12)
                assert float(scores[flat]) >= cutoff - 1e-12
            near_candidates.append(candidate)
        assert len({location(c) for c in run["top"]}) == 3
        assert all(a["score"] >= b["score"] for a, b in zip(run["top"], run["top"][1:]))
        near_evaluations += run["evaluations"]
    assert near_evaluations == near["total_evaluations"] == 311712
    assert sorted(near_candidates, key=lambda r: -r["score"])[:20] == near["top"]
    pixels = 0
    if pdf_path:
        import fitz
        assert sha(pdf_path) == inputs["primary_pdf"]["sha256"]
        document = fitz.open(pdf_path)
        for row in inputs["images"]:
            fitz.TOOLS.store_shrink(100)
            pix = document[row["pdf_page_1based"] - 1].get_pixmap(matrix=fitz.Matrix(row["scale"], row["scale"]), clip=fitz.Rect(*row["clip_points"]))
            assert (pix.width, pix.height) == (row["width"], row["height"])
            assert hashlib.sha256(pix.samples).hexdigest() == row["pixel_sha256"]
            saved = fitz.Pixmap(str(HERE / row["path"]))
            assert saved.samples == pix.samples
            pixels += 1
    result = {"schema": "adfgvx-odd-fragment-verification-v1", "prepared_by": inputs["prepared_by"], "accepted_complete_readings": 0,
              "single_change_configurations_declared_and_counted": configurations,
              "configurations_by_source": count_by_record, "retained_candidates_replayed": retained,
              "retained_run_lists_checked": runs_checked, "prefix_suffix_frames_replayed": prefix_count,
              "exploratory_rank_variants": 191, "rank_variant_parameter_evaluations": near_evaluations,
              "rank_variant_retained_candidates_replayed": len(near_candidates),
              "known_cross_campaign_overlap_evaluations": 1632,
              "total_parameter_evaluations_including_prefix_suffix": configurations + near_evaluations + prefix_count,
              "count_limit": "Parameter evaluations, not distinct ciphertexts, plaintexts or independent witnesses. The unswapped 1,632-frame Nov7-9 branch repeats the earlier single-insertion branch; other geometry duplicates are not deduplicated.",
              "source_images_pixel_verified": pixels, "all_model_scores_and_retained_rank_cutoffs_recomputed": quad is not None,
              "full_parameter_evaluations_scored_in_this_check": configurations + near_evaluations + prefix_count if quad is not None else 0,
              "rank_tie_limit": "Equal-score cutoff alternatives are accepted; unstable NumPy tie ordering is not treated as evidence.",
              "default_limit": "Without --quad, no language scores or exhaustive rank cutoffs are recomputed. Stored score ordering alone is checked, not certified as a model ranking.",
              "source_limit": "The p163 crop and input are hash-bound prior dependencies; --pdf newly rerenders only p159 and p162 crops.",
              "passed": True}
    assert {k: result[k] for k in certificate["expected_counts"]} == certificate["expected_counts"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Explicit synonym for the default read-only verification")
    parser.add_argument("--quad", type=Path, help="Optional complete 37-symbol model; requires NumPy")
    parser.add_argument("--pdf", type=Path, help="Optional original SHA-pinned PDF; requires PyMuPDF")
    parser.add_argument("--output", type=Path, help="Optional verification report destination")
    args = parser.parse_args()
    result = verify(args.quad, args.pdf)
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
