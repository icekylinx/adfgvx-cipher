"""Inventory distributable source/evidence files, excluding generated assets."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    paths = set()
    for pattern in ["README.md", "Makefile", "src/*.py", "src/*.c", "src/*.h",
                    "tools/*.py", "data/**/*.json", "data/dictionary_profiles/*.txt",
                    "data/WORDLIST_COPYING", "repro/*.json", "repro/archived_*.py"]:
        paths.update(p for p in ROOT.glob(pattern) if p.is_file())
    files = [{"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
              "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
             for path in sorted(paths)]
    result = {"format_version": 1, "file_count": len(files),
              "total_bytes": sum(row["bytes"] for row in files),
              "excludes": ["executables", "binary models", "books", "normalized wordlists", "Python caches", "generated work outputs"],
              "files": files}
    (ROOT / "MANIFEST.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"files": len(files), "bytes": result["total_bytes"]}))


if __name__ == "__main__":
    main()
