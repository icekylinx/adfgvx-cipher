#!/usr/bin/env python3
"""Write or verify the frozen open-target package's artifact inventory.
ADFGVX Cipher. icekylinx and GPT-6 Astra Pro (2026). Apache-2.0.
Generated binaries, caches, and the manifest itself are excluded.
"""
from pathlib import Path
import argparse, hashlib, json

HERE = Path(__file__).resolve().parent
EXCLUDED = {'bin', 'work', '__pycache__', '.pytest_cache'}


def inventory():
    files = []
    for path in sorted(HERE.rglob('*')):
        relative = path.relative_to(HERE)
        if not path.is_file() or relative.parts[0] in EXCLUDED or any(part in EXCLUDED for part in relative.parts):
            continue
        if relative.as_posix() == 'MANIFEST.json' or path.suffix == '.pyc':
            continue
        data = path.read_bytes()
        files.append(dict(path=relative.as_posix(), bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
    return dict(project='ADFGVX Cipher', review_credit='icekylinx and GPT-6 Astra Pro',
                scope='All package source, documentation, and frozen result files; generated binaries and caches are excluded.',
                files=files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    result = inventory()
    path = HERE / 'MANIFEST.json'
    if args.verify:
        assert result == json.loads(path.read_text())
    else:
        path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(verified=args.verify, files=len(result['files']),
                          total_bytes=sum(r['bytes'] for r in result['files']))))


if __name__ == '__main__':
    main()
