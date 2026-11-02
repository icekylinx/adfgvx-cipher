"""Check exact portable input recipes without launching a search."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from cipher import transpose, validate_square
from search_common import jobs, seed_for


def main():
    families = {name: list(jobs(name)) for name in ["fixed", "dictionary", "gap"]}
    assert {name: len(rows) for name, rows in families.items()} == {"fixed": 144, "dictionary": 1352, "gap": 136}
    for family, rows in families.items():
        assert len({row["label"] for row in rows}) == len(rows)
        for row in rows:
            assert 0 <= seed_for(family, row["label"]) < 2 ** 64
    odd = []
    for row in families["fixed"]:
        for part in row["parts"]:
            assert transpose(part["interim"], row["ranks"]) == part["ciphertext"]
            if part["abandoned_odd_interim_suffix"]:
                assert part["id"] == "p198"
                assert len(part["interim"]) == 165
                assert len(part["cells"]) == 82
                source_index = part["abandoned_odd_source_index"]
                assert part["ciphertext"][source_index] == part["abandoned_odd_interim_suffix"]
                odd.append({"label": row["label"], "unpaired_interim_suffix": part["abandoned_odd_interim_suffix"],
                            "abandoned_original_coordinate_index": source_index})
    assert len(odd) == 16
    for row in families["dictionary"]:
        assert transpose(row["interim"], row["ranks"]) == row["ciphertext"]
        assert len(row["ciphertext"]) in [178, 106]
    warm = 0
    for row in families["gap"]:
        assert len(row["ciphertext"]) == 170
        gap = row["gap_position"]
        assert row["ciphertext"][gap:gap + 5] == "?????"
        assert row["ciphertext"][:gap] + row["ciphertext"][gap + 5:] == row["received_ciphertext"]
        assert transpose(row["interim"], row["ranks"]) == row["ciphertext"]
        if row["initial_square"] is not None:
            validate_square(row["initial_square"])
            warm += 1
    assert warm == 102
    result = {"checks_passed": True, "case_counts": {name: len(rows) for name, rows in families.items()},
              "dictionary_target_counts": dict(Counter(r["id"] for r in families["dictionary"])),
              "p198_warm_starts": warm, "p198_cold_starts": 136 - warm,
              "abandoned_odd_suffixes_in_legacy_fixed_diagnostic": odd,
              "scope": "Input arithmetic and finite case enumeration only; no plaintext-recovery or search-coverage claim."}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
