"""Read preserved source editions and resolve their former public locations.

Legacy case paths are stable evidence identifiers. Their complete Markdown
texts live in one checked archive; printed-page editions are the public view.
icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import posixpath
import re
from urllib.parse import unquote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = 'data/source_editions.json'
SCHEMA = 'adfgvx-source-editions-v1'
GUIDE_TARGETS = {
    'cases/README.md': 'topics/README.md',
    'cases/other/README.md': 'topics/README.md',
    **{f'cases/{topic}/README.md': f'topics/{topic}.md'
       for topic in ('caucasus', 'naval', 'military', 'radio', 'finance', 'people', 'open')},
}
DATA_TARGETS = {
    'data/topic_reading_paths.json': 'data/topic_exploration.json',
    'data/case_view_summaries.json': 'data/topic_exploration.json',
    'data/case_path_aliases.json': 'data/source_editions.json',
}


@lru_cache(maxsize=8)
def _load_archive(filename, modified, size):
    data = json.loads(Path(filename).read_text(encoding='utf-8'))
    if data.get('schema') != SCHEMA:
        raise ValueError('Unknown source-edition archive schema')
    editions = {}
    for path, record in data['editions'].items():
        if (not path.startswith('cases/') or not path.endswith('.md')
                or posixpath.normpath(path) != path or path.startswith('cases/pages/')):
            raise ValueError('Invalid source-edition identifier: ' + path)
        text = record['text']
        if not isinstance(text, str):
            raise ValueError('Source edition must be text: ' + path)
        digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
        if digest != record['sha256']:
            raise ValueError('Source-edition integrity mismatch: ' + path)
        editions[path] = text
    aliases = data.get('aliases', {})
    for alias, canonical in aliases.items():
        if alias in editions or canonical not in editions:
            raise ValueError('Invalid source-edition alias: ' + alias)
    public_targets = data.get('public_targets', {})
    for legacy, destination in public_targets.items():
        if (legacy not in editions or not isinstance(destination, str)
                or posixpath.normpath(destination) != destination
                or destination.startswith(('/', '../'))
                or urlsplit(destination).scheme or '#' in destination or '?' in destination):
            raise ValueError('Invalid explicit public target: ' + legacy)
    return editions, aliases, public_targets


def _archive(root):
    path = Path(root).resolve() / ARCHIVE
    if not path.is_file():
        return {}, {}, {}
    stat = path.stat()
    return _load_archive(str(path), stat.st_mtime_ns, stat.st_size)


def load_editions(root=ROOT):
    """Return canonical legacy identifiers mapped to exact original Markdown."""
    return dict(_archive(root)[0])


def _identifier(path, root):
    path, root = Path(path), Path(root).resolve()
    absolute = path.resolve() if path.is_absolute() else (root / path).resolve()
    try:
        return absolute.relative_to(root).as_posix()
    except ValueError:
        return None


def read_source_text(path, encoding=None, errors=None, *, root=ROOT):
    """Read an archived edition by logical path, or an ordinary physical file."""
    editions, aliases, _ = _archive(root)
    key = _identifier(path, root)
    key = aliases.get(key, key)
    if key in editions:
        return editions[key]
    return Path(path).read_text(encoding=encoding, errors=errors)


def source_exists(path, *, root=ROOT):
    """Whether a logical source edition or physical file is available."""
    editions, aliases, _ = _archive(root)
    key = _identifier(path, root)
    return key in editions or key in aliases or Path(path).is_file()


def page_target(legacyref, catalogue=None, root=ROOT):
    """Map a former case/alias link to a full page and its stable section anchor.

    A catalogue row with the requested fragment selects its own printed page.
    Other fragments use the first page containing that shared complete edition.
    An explicitly retained earlier edition may instead point to its research
    package. Such a target keeps only fragments present in that package.
    Unknown references pass through unchanged.
    """
    value = str(legacyref)
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return value
    editions, aliases, public_targets = _archive(root)
    key = posixpath.normpath(unquote(parsed.path))
    fragment = unquote(parsed.fragment)
    if key in GUIDE_TARGETS or key in DATA_TARGETS:
        destination = (GUIDE_TARGETS if key in GUIDE_TARGETS else DATA_TARGETS)[key]
        if key == 'cases/README.md':
            fragment = {'the-original-22-challenges': 'original-challenges',
                        'browse-by-topic': 'subjects'}.get(fragment, fragment)
            if fragment == 'how-to-read-a-case':
                destination, fragment = 'docs/reading-conventions.md', 'source-editions'
        return urlunsplit(('', '', destination, parsed.query, fragment))
    key = aliases.get(key, key)
    if key not in editions:
        return value
    root = Path(root)
    if key in public_targets:
        destination = public_targets[key]
        target = root / destination
        if not target.is_file():
            raise ValueError('Missing explicit public target: ' + destination)
        if fragment:
            from .navigation import anchors
            if fragment not in anchors(target.read_text(encoding='utf-8')):
                fragment = ''
        return urlunsplit(('', '', destination, parsed.query, fragment))
    if catalogue is None:
        catalogue = json.loads((root / 'data/reading_catalog.json').read_text())
    rows = [row for group in ('challenge', 'other') for row in catalogue[group]
            if row['path'].split('#', 1)[0] == key]
    if not rows:
        raise ValueError('No printed source page for edition: ' + key)
    exact = [row for row in rows if row['path'].partition('#')[2] == fragment]
    selected = exact or rows
    messages = None
    pages = []
    for row in selected:
        if 'printed_page' in row:
            pages.append(row['printed_page'])
        else:
            if messages is None:
                messages = {m['id']: m for m in json.loads(
                    (root / 'data/messages.json').read_text())['messages']}
            pages.append(messages[row['id']]['source']['printed_page'])
    anchor = 'edition-' + re.sub(r'[^a-z0-9-]', '-', key[:-3].lower()).strip('-')
    if fragment:
        anchor += '-' + fragment
    return urlunsplit(('', '', f'cases/pages/{min(pages):03d}.md', parsed.query, anchor))


def materialize_editions(root=ROOT):
    """Prepare exact legacy-path fixtures for the unchanged research verifiers.

    Existing files must already match the archive. Check all conflicts before
    writing anything, so an edited fixture is never overwritten.
    """
    root = Path(root)
    payloads = {root / path: text.encode('utf-8')
                for path, text in load_editions(root).items()}
    conflicts = [str(path.relative_to(root)) for path, body in payloads.items()
                 if path.exists() and (not path.is_file() or path.read_bytes() != body)]
    if conflicts:
        raise ValueError('Preserving existing files that differ from the archive: '
                         + ', '.join(conflicts))
    written = []
    for path, body in payloads.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            written.append(path.relative_to(root).as_posix())
    return written


def clean_editions(root=ROOT):
    """Remove only fixtures whose bytes still exactly match the archive."""
    root = Path(root)
    removed, preserved = [], []
    for name, text in load_editions(root).items():
        path = root / name
        if not path.exists():
            continue
        if path.is_file() and path.read_bytes() == text.encode('utf-8'):
            path.unlink()
            removed.append(name)
        else:
            preserved.append(name)
    return removed, preserved


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--check', action='store_true', help='Verify archive integrity (default)')
    modes.add_argument('--materialize', action='store_true',
                       help='Prepare exact legacy-path files for unchanged research verifiers')
    modes.add_argument('--clean', action='store_true',
                       help='Remove matching verification fixtures; preserve edited files')
    args = parser.parse_args()
    editions = load_editions()
    if not editions:
        parser.error('The source-edition archive is missing or empty')
    if args.materialize:
        try:
            written = materialize_editions()
        except ValueError as error:
            parser.exit(1, str(error) + '\n')
        print(f'Prepared {len(editions)} exact verification fixtures; wrote {len(written)} files.')
    elif args.clean:
        removed, preserved = clean_editions()
        print(f'Removed {len(removed)} unchanged verification fixtures.')
        if preserved:
            parser.exit(1, 'Preserved edited files: ' + ', '.join(preserved) + '\n')
    else:
        print(f'Verified {len(editions)} complete source editions and their SHA-256 digests.')


if __name__ == '__main__':
    main()
