"""Check the current research packages' declared files after editorial updates."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]


def verify():
    manifests = sorted((ROOT / 'experiments').rglob('MANIFEST.json'))
    checked = 0
    for manifest in manifests:
        data = json.loads(manifest.read_text())
        records = data['files']
        if isinstance(records, dict):
            records = [dict(path=path, sha256=digest) for path, digest in records.items()]
        assert len({row['path'] for row in records}) == len(records), manifest
        total = 0
        for row in records:
            relative = row['path']
            path = (ROOT if relative.startswith('experiments/') else manifest.parent) / relative
            body = path.read_bytes()
            assert hashlib.sha256(body).hexdigest() == row['sha256'], (manifest, relative)
            if 'bytes' in row:
                assert len(body) == row['bytes'], (manifest, relative, 'length')
            total += len(body)
            checked += 1
        for field in ('bytes', 'total_bytes'):
            if field in data:
                assert total == data[field], (manifest, field)
        if 'file_count' in data:
            assert len(records) == data['file_count'], manifest
    return dict(inventories=len(manifests), files=checked)


if __name__ == '__main__':
    print(json.dumps(verify()))
