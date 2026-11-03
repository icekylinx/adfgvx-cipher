#!/usr/bin/env python3
"""Bind reviewed live Markdown quotations to their exact decoded labels.

This checks presentation, not source authenticity or historical uniqueness.
Only explicitly reviewed separator occurrences may be omitted from a display.
Prepared by icekylinx and GPT-6 Astra Pro. Apache-2.0.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / 'data/reviews/live_readable_mappings_20261103.json'


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def section(text, heading):
    matches = list(re.finditer(r'^## (.+)$', text, re.M))
    selected = [(i, m) for i, m in enumerate(matches) if m[1] == heading]
    assert len(selected) == 1, ('missing or repeated section', heading)
    i, match = selected[0]
    return text[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)]


def caption(text, start):
    return text[:start].rstrip().split('\n\n')[-1]


def displays(text):
    streams = [(m[1], caption(text, m.start()))
               for m in re.finditer(r'```text\n([A-Z0-9?]+)\n```', text)]
    quotes = [(' '.join(line[2:] for line in m[0].splitlines()), caption(text, m.start()))
              for m in re.finditer(r'(?:^>[^\n]*(?:\n|$))+', text, re.M)]
    return streams, quotes


def normalized(quote, allowed_brackets, question_punctuation=()):
    # Every removed editorial insertion is explicitly listed in the manifest.
    found = re.findall(r'\[[^\[\]]*\]', quote)
    assert found == allowed_brackets, ('unreviewed display insertions', found)
    for context in question_punctuation:
        assert context.endswith('?') and context.count('?') == 1
        assert quote.count(context) == 1, ('question-punctuation context changed', context)
        quote = quote.replace(context, context[:-1])
    # Inline code is often used to distinguish literal unresolved fields from
    # editorial punctuation. Remove only balanced single-backtick delimiters;
    # their contents remain subject to the same exact ordered-label equality.
    quote = re.sub(r'(?<!`)`([^`\n]+)`(?!`)', lambda match: match[1], quote)
    assert '`' not in quote, 'unreviewed or unbalanced code-span delimiters'
    value = re.sub(r'\[[^\[\]]*\]', '', quote).upper()
    for old, new in (('Ä', 'AE'), ('Ö', 'OE'), ('Ü', 'UE'), ('ẞ', 'SS')):
        value = value.replace(old, new)
    labels = []
    for char in value:
        if char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?':
            labels.append(char)
        else:
            assert char.isspace() or unicodedata.category(char).startswith('P'), ('unreviewed character', char)
    return ''.join(labels)


def verify(manifest):
    seen, total, unknowns, inserted = set(), 0, 0, 0
    for row in manifest['records']:
        assert row['id'] not in seen, row['id']
        seen.add(row['id'])
        text = section((ROOT / row['case_path']).read_text(), row['section'])
        streams, quotes = displays(text)
        stream, stream_caption = streams[row['stream_index']]
        quote, quote_caption = quotes[row['quote_index']]
        assert sha(stream) == row['stream_sha256'], (row['id'], 'decoded stream changed')
        assert stream_caption == row['stream_caption'], (row['id'], 'frame/layer qualifier changed')
        assert quote_caption == row['quote_caption'], (row['id'], 'readable qualification changed')
        assert '**Readable German' in quote_caption
        assert stream_caption.startswith('**' + row['layer'])
        labels = normalized(quote, row['display_only_insertions'], row.get('question_punctuation', ()))
        # Ordered equality protects every number, name, repeated label and '?'.
        separator = row.get('separator_label', 'X')
        retained = row.get('retained_separator_positions', [])
        assert len(set(retained)) == len(retained) and all(stream[i] == separator for i in retained)
        source_positions = [i for i, char in enumerate(stream) if char != separator or i in retained]
        for field in row.get('protected_fields', []):
            assert field in stream and field in quote, (row['id'], 'protected literal field changed')
        assert labels == ''.join(stream[i] for i in source_positions), (row['id'], 'readable labels differ')
        assert len(labels) == row['mapped_positions'] and labels.count('?') == row['unresolved_positions']
        total += len(labels)
        unknowns += labels.count('?')
        inserted += sum(char.isalpha() for s in row['display_only_insertions']
                        for char in s[1:-1])
    summary = {'records': len(seen), 'case_pages': len({r['case_path'] for r in manifest['records']}),
               'mapped_nonseparator_positions': total, 'unresolved_positions': unknowns,
               'display_only_inserted_letters': inserted}
    assert summary == manifest['summary'], summary
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=DEFAULT)
    args = parser.parse_args()
    result = verify(json.loads(args.manifest.read_text()))
    print('Live readable mappings: ' + json.dumps(result, sort_keys=True) + '; verified.')


if __name__ == '__main__':
    main()
