"""Generate topic guides and verify stable reading links.

ADFGVX Cipher -- icekylinx and GPT-6 Astra Pro. Apache-2.0.
The reading catalogue remains authoritative for status, credit and evidence.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import html
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from .catalog import ROOT, load_catalog, relative_link, table

START = '<!-- TOPIC-NAVIGATION:START -->'
END = '<!-- TOPIC-NAVIGATION:END -->'
LINK = re.compile(r'\]\((<[^>]+>|[^\s)]+)(?:\s+["\'][^"\']*["\'])?\)')
REFERENCE = re.compile(r'^\s{0,3}\[(?!\^)[^\]]+\]:\s*(<[^>]+>|\S+)')


def prose_lines(text):
    """Exclude fenced examples from link and heading checks."""
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield line


def plain_heading(text):
    text = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<[^>]*>', '', text)
    return html.unescape(text.replace('`', '').replace('*', '').strip())


def anchors(text):
    """GitHub-style heading slugs plus explicit HTML anchors."""
    result, occurrences = {}, defaultdict(int)
    for line in prose_lines(text):
        for match in re.finditer(r'<a\s+(?:id|name)=["\']([^"\']+)["\']', line, re.I):
            result[html.unescape(match.group(1))] = html.unescape(match.group(1))
        heading = re.match(r'^\s{0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$', line)
        if not heading:
            continue
        label = plain_heading(heading.group(1))
        slug = re.sub(r'[^\w\- ]', '', label.lower()).replace(' ', '-')
        occurrence = occurrences[slug]
        occurrences[slug] += 1
        if occurrence:
            slug += '-' + str(occurrence)
        result.setdefault(slug, label)
    return result


def targets(text):
    for line in prose_lines(text):
        for match in LINK.finditer(line):
            yield match.group(1).strip('<>')
        definition = REFERENCE.match(line)
        if definition:
            yield definition.group(1).strip('<>')


def page_title(path):
    for line in prose_lines(path.read_text()):
        if line.startswith('# '):
            return plain_heading(line[2:])
    raise AssertionError(f'Missing case title: {path.relative_to(ROOT)}')


def load_groups(catalogue):
    settings = json.loads((ROOT / 'data/reading_groups.json').read_text())
    groups = settings['groups']
    assert len({g['id'] for g in groups}) == len(groups)
    rows = {g['id']: [] for g in groups}
    challenge_ids = {r['id'] for r in catalogue['challenge']}
    for group in groups:
        assert group['directory'] == 'cases/' + group['id']
        assert set(group.get('related_challenge_ids', [])) <= challenge_ids
        for path in group.get('additional_case_paths', []):
            assert (ROOT / path).is_file(), path
    for row in catalogue['other']:
        path = row['path'].split('#')[0]
        matches = [g['id'] for g in groups
                   if path.startswith(g['directory'] + '/')
                   or path in g.get('additional_case_paths', [])]
        assert len(matches) == 1, f"Assign exactly one reading topic: {row['id']} ({path})"
        rows[matches[0]].append(row)
    for value in rows.values():
        value.sort(key=lambda r: (r['printed_page'], r['source_section'], r['id']))
    assert sum(map(len, rows.values())) == len(catalogue['other'])
    return groups, rows


def load_aliases():
    data = json.loads((ROOT / 'data/case_path_aliases.json').read_text())
    aliases = data['aliases']
    old_paths = {a['old_path'] for a in aliases}
    assert len(old_paths) == len(aliases)
    assert len({a['canonical_path'] for a in aliases}) == len(aliases)
    for alias in aliases:
        assert alias['old_path'].startswith('cases/other/')
        assert alias['canonical_path'] not in old_paths
        assert (ROOT / alias['canonical_path']).is_file()
        assert len({a['id'] for a in alias['anchors']}) == len(alias['anchors'])
        current = anchors((ROOT / alias['canonical_path']).read_text())
        assert all(a['id'] in current for a in alias['anchors']), alias['canonical_path']
    return aliases


def render_alias(alias):
    destination = ROOT / alias['old_path']
    canonical = alias['canonical_path']
    link = relative_link(canonical, destination)
    topic = relative_link(str(Path(canonical).parent / 'README.md'), destination)
    lines = [
        '# Reading location', '', f"**{alias['title']}**", '',
        f'[Open the complete source edition]({link}) · [Browse this topic]({topic})', '',
        'This earlier URL remains available for published links and preserved',
        'research records. The complete reading, source evidence and credits are',
        'maintained at the new location.', '', '## Preserved section links', '',
    ]
    for anchor in alias['anchors']:
        lines.extend([f'<a id="{html.escape(anchor["id"], quote=True)}"></a>', '',
                      f'[{anchor["label"]}]({link}#{anchor["id"]})', ''])
    lines.extend(['Navigation maintained by **icekylinx and GPT-6 Astra Pro**.', ''])
    return '\n'.join(lines)


def render_alias_index(aliases):
    destination = ROOT / 'cases/other/README.md'
    lines = [
        '# Earlier case paths', '',
        'Complete source editions are now organized in the six '
        '[reading topics](../README.md#browse-by-topic). This directory keeps',
        'earlier URLs and their section anchors available for citations and',
        'preserved research records.', '',
        '| Earlier URL | Current source edition |', '|---|---|',
    ]
    for alias in aliases:
        old = relative_link(alias['old_path'], destination)
        new = relative_link(alias['canonical_path'], destination)
        title = alias['title'].replace('|', '\\|')
        lines.append(f'| [{Path(alias["old_path"]).name}]({old}) | [{title}]({new}) |')
    lines.extend(['', 'Navigation maintained by **icekylinx and GPT-6 Astra Pro**.', ''])
    return '\n'.join(lines)


def render_topic(group, rows, catalogue):
    destination = ROOT / group['directory'] / 'README.md'
    families = {}
    for row in rows:
        families.setdefault(row['path'].split('#')[0], []).append(row)
    lines = [
        '# ' + group['title'], '',
        '[All readings](../README.md) · [Repository map](../../docs/repository-map.md) · '
        '[Evidence and methods](../../docs/methods.md)', '',
        group['summary'], '',
        f'**{len(rows)} reviewed physical records across {len(families)} case pages.** '
        'Multipart segments and repeated transmissions retain their separate source identifiers.', '',
        '## Case pages', '', '| Case | Source records |', '|---|---|',
    ]
    for path, family in families.items():
        title = page_title(ROOT / path).replace('|', '\\|')
        labels = ', '.join(row['label'] for row in family)
        lines.append(f'| [{title}]({relative_link(path, destination)}) | {labels} |')
    lines.extend(['', '## Reviewed source records', '', table(rows, destination), ''])
    related_ids = group.get('related_challenge_ids', [])
    if related_ids:
        related = [r for r in catalogue['challenge'] if r['id'] in related_ids]
        lines.extend(['## Related challenge entries', '',
                      'These retain their original challenge identifiers and statuses; '
                      'they are separate from the record count above.', '',
                      table(related, destination), ''])
    lines.extend([
        'Topics are reading aids. Each family page preserves its own keys, source',
        'relationships, earlier credits and limits. The live reading catalogue',
        'supplies every record status and credit shown here.', '',
        'Research and editorial work: **icekylinx and GPT-6 Astra Pro**.', '',
    ])
    return '\n'.join(lines)


def render_overview(groups, rows):
    lines = [START, '## Browse by topic', '',
             '| Topic | Reviewed source records | Case pages |', '|---|---:|---:|']
    for group in groups:
        records = rows[group['id']]
        families = len({r['path'].split('#')[0] for r in records})
        lines.append(f"| [{group['title']}]({group['id']}/README.md) | {len(records)} | {families} |")
    lines.extend(['', 'These topic guides cover every record in the second table below. '
                  'The challenge table retains all 22 original entries.', END])
    return '\n'.join(lines)


def check_links(paths):
    known_anchors, checked, failures = {}, 0, []
    for source in sorted(paths):
        for target in targets(source.read_text()):
            if urlsplit(target).scheme or target.startswith('//'):
                continue
            file, _, fragment = target.partition('#')
            file = unquote(file.partition('?')[0])
            destination = (source.parent / file).resolve() if file else source
            try:
                destination.relative_to(ROOT)
            except ValueError:
                failures.append(f'{source.relative_to(ROOT)} -> {target}: outside repository')
                continue
            if not destination.exists():
                failures.append(f'{source.relative_to(ROOT)} -> {target}: missing file')
                continue
            checked += 1
            if destination.is_dir() and (destination / 'README.md').is_file():
                destination /= 'README.md'
            if fragment and destination.suffix.lower() == '.md':
                if destination not in known_anchors:
                    known_anchors[destination] = anchors(destination.read_text())
                if unquote(fragment) not in known_anchors[destination]:
                    failures.append(f'{source.relative_to(ROOT)} -> {target}: missing section')
    assert not failures, '\n'.join(failures)
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify generated guides, aliases and local links without writing')
    args = parser.parse_args()
    catalogue = load_catalog()
    groups, rows = load_groups(catalogue)
    aliases = load_aliases()
    generated = {ROOT / a['old_path']: render_alias(a) for a in aliases}
    generated[ROOT / 'cases/other/README.md'] = render_alias_index(aliases)
    generated.update({ROOT / g['directory'] / 'README.md': render_topic(g, rows[g['id']], catalogue)
                      for g in groups})
    guide = ROOT / 'cases/README.md'
    current = guide.read_text()
    assert current.count(START) == current.count(END) == 1
    before, rest = current.split(START)
    _, after = rest.split(END)
    generated[guide] = before + render_overview(groups, rows) + after
    for path, expected in generated.items():
        if args.check:
            assert path.read_text() == expected, f'Regenerate navigation: {path.relative_to(ROOT)}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected)
    paths = set(generated) | {ROOT / 'README.md', ROOT / 'docs/repository-map.md'}
    paths |= {ROOT / r['path'].split('#')[0] for group in ['challenge', 'other']
              for r in catalogue[group]}
    checked = check_links(paths)
    family_count = len({r['path'].split('#')[0] for r in catalogue['other']})
    print(f'Navigation: {len(groups)} topics, {len(catalogue["other"])} reviewed records, '
          f'{family_count} case pages, {len(aliases)} legacy aliases; '
          f'{checked} local links and their Markdown sections checked.')


if __name__ == '__main__':
    main()
