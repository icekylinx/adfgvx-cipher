"""Consistent reader typography without altering quoted or machine evidence.

The source archive remains literal. This formatter operates on its public
Markdown view, after source selection, link rebasing and anchor assignment.
"""
from __future__ import annotations

from collections import defaultdict
import html
import re

MONTHS = ('January February March April May June July August September October '
          'November December').split()
MONTH_FIRST = re.compile(
    r'\b(' + '|'.join(MONTHS) + r') ([1-9]|[12][0-9]|3[01])'
    r'(?:[ \t]*[–-][ \t]*([1-9]|[12][0-9]|3[01]))?'
    r'(?:,? ((?:18|19|20)\d{2}))?(?![\w-])')
CROSS_MONTH = re.compile(
    r'\b(' + '|'.join(MONTHS) + r') ([1-9]|[12][0-9]|3[01])'
    r'\s*[–-]\s*(' + '|'.join(MONTHS) + r') ([1-9]|[12][0-9]|3[01])'
    r'(?:,? ((?:18|19|20)\d{2}))?(?!\w)')
PAGE = re.compile(
    r'(?<![\w/])(?P<kind>pp|p)\.?[ \t]*(?P<first>\d+)'
    r'(?P<range>[ \t]*[–-][ \t]*(?:p\.?[ \t]*)?(?P<last>\d+))?'
    r'(?![\d_])')
FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})')
HEADING = re.compile(r'^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$')
INLINE_CODE = re.compile(r'(`+)(?!`)(.*?)(?<!`)\1(?!`)', re.S)
LINK_TARGET = re.compile(r'\]\((?:<[^>]*>|[^\s)]+)(?:\s+["\'][^"\']*["\'])?\)')
REFERENCE_TARGET = re.compile(r'^ {0,3}\[(?!\^)[^\]]+\]:\s*\S+(?:\s+.*)?$')
QUOTED = re.compile(r'"(?:\\.|[^"\\])*"|“[^”]*”|‘[^’]*’')
HTML_TAG = re.compile(r'<[^>]*>')
HTML_LITERAL = re.compile(r'<(pre|code)(?:\s[^>]*)?>.*?</\1\s*>', re.I | re.S)
URL = re.compile(r'https?://[^\s<>]+')


def _prose(text):
    def page(match):
        if match['range']:
            if int(match['last']) < int(match['first']):
                return match[0]
            return 'pp' + match['first'] + '–' + match['last']
        return match['kind'] + match['first']

    def date(match):
        month, first, last, year = match.groups()
        return first + ('–' + last if last else '') + ' ' + month + (' ' + year if year else '')

    text = re.sub(r'\bPDF pp?\.?[ \t]*(\d+)(?:[ \t]*[–-][ \t]*(\d+))?',
                  lambda m: 'PDF ' + ('pages ' + m[1] + '–' + m[2]
                                      if m[2] else 'page ' + m[1]), text)
    text = PAGE.sub(page, text)
    text = re.sub(r'(\[p\d+)_([A-Z]\d*)(?=\]|$)', r'\1 \2', text)
    text = CROSS_MONTH.sub(lambda m: m[2] + ' ' + m[1] + '–' + m[4] + ' ' + m[3]
                           + (' ' + m[5] if m[5] else ''), text)
    text = MONTH_FIRST.sub(date, text)
    text = text.replace('| What remains separate |', '| Evidence distinctions |')
    text = text.replace('| What it establishes |', '| Evidence provided |')
    text = text.replace('**Editorial limits.**', '**Editorial limits:**')
    text = text.replace('**Unresolved details and editorial limits.**',
                        '**Unresolved details and editorial limits:**')
    text = text.replace('**Later copy evidence.**', '**Later copy evidence:**')
    text = text.replace('**Readable German — based on the edited candidate above; the local qualifications remain in force:**',
                        '**Readable German — edited candidate:**')
    text = text.replace('**Readable German** — based on the explicitly repaired output below.',
                        '**Readable German — repaired output:**')
    text = text.replace('**Meaning.**', '**Meaning:**')
    text = text.replace('**Readable German** — ', '**Readable German:** ')
    return re.sub(r'\broundtrip\b', 'round-trip', text)


def inline(text, protected=()):
    """Format editorial prose, leaving destinations, literals and tags exact."""
    spans = list(protected)
    for pattern in (INLINE_CODE, LINK_TARGET, REFERENCE_TARGET, QUOTED, HTML_LITERAL, HTML_TAG, URL):
        spans.extend(match.span() for match in pattern.finditer(text))
    merged = []
    for start, end in sorted(spans):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    output, previous = [], 0
    for start, end in merged:
        output.extend((_prose(text[previous:start]), text[start:end]))
        previous = end
    output.append(_prose(text[previous:]))
    return ''.join(output)


def _slug(title):
    title = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', title)
    title = re.sub(r'<[^>]*>', '', title).replace('`', '').replace('*', '').strip()
    return re.sub(r'[^\w\- ]', '', html.unescape(title).lower()).replace(' ', '-')


def markdown(text):
    """Normalize public prose and retain old heading URLs when labels change.

    Fenced blocks, blockquotes, indented code, inline literals, reference
    destinations and HTML attributes are preserved byte for byte. Page and
    source IDs inside those evidence layers retain their original spelling.
    """
    result, headings, old_counts = [], [], defaultdict(int)
    existing_ids = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', text))
    fence, quote = None, False
    literal_spans = sorted(match.span() for pattern in (INLINE_CODE, QUOTED, HTML_LITERAL)
                           for match in pattern.finditer(text))
    position = 0
    for line in text.splitlines(keepends=True):
        start, end = position, position + len(line)
        position = end
        if fence is None:
            if re.match(r'^ {0,3}>', line):
                quote = True
                result.append(line)
                continue
            if quote:
                if not line.strip() or re.match(r'^ {0,3}(?:#{1,6}\s|`{3,}|~{3,}|<|[-+*]\s|1[.)]\s)', line):
                    quote = False
                else:
                    result.append(line)
                    continue
        marker = FENCE.match(line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not line[marker.end():].strip():
                fence = None
            result.append(line)
            continue
        if fence is not None or re.match(r'^(?: {0,3}>| {4}|\t)', line):
            result.append(line)
            continue
        protected = [(max(0, a - start), min(len(line), b - start))
                     for a, b in literal_spans if a < end and b > start]
        formatted = inline(line, protected)
        if re.fullmatch(r'\|(?:\s*:?-{3,}:?\s*\|)+\s*', formatted):
            cells = [cell.strip() for cell in formatted.strip().strip('|').split('|')]
            formatted = '| ' + ' | '.join(cells) + ' |' + ('\n' if line.endswith('\n') else '')
        old, new = HEADING.match(line.rstrip('\n')), HEADING.match(formatted.rstrip('\n'))
        if old and new:
            before = _slug(old[1])
            old_count = old_counts[before]
            old_counts[before] += 1
            old_anchor = before + (f'-{old_count}' if old_count else '')
            headings.append((len(result), old_anchor, line))
        result.append(formatted)
    # A new automatic heading slug must not take an older section's URL.
    owners = {anchor: index for index, anchor, _ in headings}
    while True:
        counts, new_ids, conflicts = defaultdict(int), set(), []
        for index, old_anchor, original in headings:
            base = _slug(HEADING.match(result[index].rstrip('\n'))[1])
            count = counts[base]
            counts[base] += 1
            anchor = base + (f'-{count}' if count else '')
            new_ids.add(anchor)
            if result[index] != original and (owners.get(anchor, index) != index
                                              or anchor in existing_ids and anchor != old_anchor):
                conflicts.append((index, original))
        if not conflicts:
            break
        for index, original in conflicts:
            result[index] = original
    for index, anchor, _ in reversed(headings):
        if anchor not in existing_ids and anchor not in new_ids:
            result[index] = result[index].rstrip('\n') + f'\n\n<a id="{anchor}"></a>\n'
            existing_ids.add(anchor)
    return ''.join(result)
