"""Present concise case meanings while preserving each complete source edition.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.
Run after editing the original edition or data/case_view_summaries.json.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import posixpath
import re

from .catalog import ROOT, load_catalog, source_locations

START = '<!-- CASE-EDITION:START -->'
END = '<!-- CASE-EDITION:END -->'
SUMMARY = 'Full source edition and evidence'
OPEN = START + '\n<details>\n<summary>' + SUMMARY + '</summary>\n\n'
CLOSE = '\n</details>\n' + END + '\n'
MANIFEST = 'data/case_view_summaries.json'
TITLE = re.compile(r'^# [^\r\n]+(?:\r?\n|$)', re.M)


def split_original(text):
    """Keep legacy anchors before the first H1, and every body byte after it."""
    match = TITLE.search(text)
    if match is None:
        raise ValueError('A case edition needs a Markdown H1 title')
    return text[:match.end()], text[match.end():]


def unwrap_original(text):
    """Reconstruct the original file exactly; plain editions pass through."""
    if START not in text and END not in text:
        return text
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('Expected exactly one complete case-edition wrapper')
    start = text.index(START)
    if not text.startswith(OPEN, start) or not text.endswith(CLOSE):
        raise ValueError('Malformed case-edition wrapper')
    prefix, _ = split_original(text)
    if len(prefix) > start:
        raise ValueError('Case title must precede the edition wrapper')
    body = text[start + len(OPEN):-len(CLOSE)]
    return prefix + body


def case_records(catalogue):
    """Only canonical catalogue paths; never topic indexes or alias pages."""
    grouped = defaultdict(list)
    for group in ('challenge', 'other'):
        for row in catalogue[group]:
            path = row['path'].split('#', 1)[0]
            if not path.startswith('cases/') or path.startswith('cases/pages/') or Path(path).name == 'README.md':
                raise ValueError('Not a canonical case path: ' + path)
            grouped[path].append(row)
    return dict(sorted(grouped.items()))


def case_source_pages(catalogue):
    locations = source_locations(catalogue)
    return {path: sorted({locations[row['id']][0] for row in rows})
            for path, rows in case_records(catalogue).items()}


def page_links(path, pages):
    """Links remain valid for both top-level challenges and topical cases."""
    parent = posixpath.dirname(path)
    return ' · '.join(f'[p. {page}]({posixpath.relpath(f"cases/pages/{page:03d}.md", parent)})'
                      for page in pages)


def load_summaries(root=ROOT):
    data = json.loads((root / MANIFEST).read_text())
    if data.get('schema') != 'adfgvx-case-view-summaries-v1':
        raise ValueError('Unknown case summary schema')
    result = data['cases']
    for path, item in result.items():
        paragraphs = item['summary']
        if not isinstance(paragraphs, list) or not paragraphs or not all(isinstance(p, str) and p.strip() for p in paragraphs):
            raise ValueError('Missing English meaning: ' + path)
        if any(START in p or END in p or '\n# ' in p or '<details' in p for p in paragraphs):
            raise ValueError('Summary contains source-edition structure: ' + path)
    return result


def render_case(path, text, summary, pages):
    original = unwrap_original(text)
    if START in original or END in original:
        raise ValueError('Original edition contains reserved case markers')
    prefix, body = split_original(original)
    if not prefix.endswith('\n'):
        raise ValueError('Case title must end with a newline')
    paragraphs = summary['summary']
    overview = '\n' + '\n\n'.join(paragraphs) + '\n\n'
    overview += '**Complete edition by printed page:** ' + page_links(path, pages) + '\n\n'
    rendered = prefix + overview + OPEN + body + CLOSE
    if unwrap_original(rendered) != original:
        raise AssertionError('The complete original edition changed: ' + path)
    return rendered


def build_views(catalogue, summaries, root=ROOT):
    grouped = case_records(catalogue)
    if set(summaries) != set(grouped):
        raise ValueError('Summary/case mismatch: missing=' + str(sorted(set(grouped)-set(summaries)))
                         + ', extra=' + str(sorted(set(summaries)-set(grouped))))
    pages = case_source_pages(catalogue)
    return {path: render_case(path, (root/path).read_bytes().decode("utf-8"), summaries[path], pages[path])
            for path in grouped}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true', help='Write concise views, preserving original editions')
    mode.add_argument('--check', action='store_true', help='Check that generated case views are current (default)')
    args = parser.parse_args()
    catalogue = load_catalog()
    summaries = load_summaries()
    rendered = build_views(catalogue, summaries)
    changed = []
    for path, expected in rendered.items():
        target = ROOT/path
        if target.read_bytes().decode("utf-8") != expected:
            changed.append(path)
            if args.write:
                target.write_bytes(expected.encode("utf-8"))
    if changed and not args.write:
        print('Case views need regeneration: ' + ', '.join(changed))
        raise SystemExit(1)
    print(('Wrote' if args.write else 'Verified') + f' {len(rendered)} concise case views; all complete editions preserved.')


if __name__ == '__main__':
    main()
