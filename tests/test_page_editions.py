"""Full page editions retain source content and working, unambiguous links."""
from pathlib import Path
from collections import Counter
import hashlib
import json
from tempfile import TemporaryDirectory
import unittest

from adfgvx import catalog
from adfgvx import page_editions as editions
from adfgvx import source_editions


class PageEditionTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix='adfgvx-page-editions-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ('data', 'pages', 'experiments/example', 'sources', 'docs',
                          'docs/historical-studies', 'topics'):
            (self.root / directory).mkdir(parents=True)
        for path in ('pages/README.md', 'topics/README.md', 'docs/reading-conventions.md',
                     'docs/historical-studies/README.md'):
            (self.root / path).write_text('# Index\n')
        (self.root / 'sources/cipher.png').write_bytes(b'fixture-image')
        (self.root / 'experiments/example/README.md').write_text('# Evidence\n\n## Check\n')
        self.first = 'cases/radio/first.md'
        self.second = 'cases/radio/second.md'
        self.original = (
            '<a id="legacy-title"></a>\n\n# First message\n\n'
            '[All cases](../README.md) · [Reading conventions](../../docs/reading-conventions.md)\n\n'
            'English interpretation retained in full.\n\n'
            '## p56 A\n\n> German reading.\n\n'
            '[Self](#evidence) · [Other](second.md#evidence) · '
            '[External](https://example.org/x#keep)\n\n'
            '![Cipher](../../sources/cipher.png)\n\n'
            '<details>\n<summary>Machine evidence</summary>\n\n'
            '**Raw output:**\n\n```text\nAD?FGX\n# Not a heading\n'
            '[Not a link](missing-file.md)\n```\n\n</details>\n\n'
            '## p57 A\n\nCompanion source and explanation.\n\n'
            '## Evidence\n\n[Certificate](../../experiments/example/README.md#check)\n\n'
            '## Evidence\n\n[Repeated heading](#evidence-1)\n'
        )
        self.editions = {self.first: self.original,
                         self.second: '# Second message\n\n## Evidence\n\nIndependent explanation.\n'}
        self.catalogue = {'challenge': [], 'other': [
            {'id': 'p56_A', 'label': 'p56 A', 'state': 'READING', 'subject': 'First subject',
             'path': self.first + '#p56-a', 'printed_page': 56, 'source_section': 'A'},
            {'id': 'p56_B', 'label': 'p56 B', 'state': 'PARTIAL', 'subject': 'Second subject',
             'path': self.second, 'printed_page': 56, 'source_section': 'B'},
            {'id': 'p57_A', 'label': 'p57 A', 'state': 'CONDITIONAL', 'subject': 'Companion',
             'path': self.first + '#p57-a', 'printed_page': 57, 'source_section': 'A'},
        ]}
        self.locations = {'p56_A': (56, 'A'), 'p56_B': (56, 'B'), 'p57_A': (57, 'A')}

    def build(self):
        archive = {'schema': source_editions.SCHEMA, 'editions': {
            path: {'text': text, 'sha256': hashlib.sha256(text.encode()).hexdigest()}
            for path, text in self.editions.items()}, 'aliases': {}}
        (self.root / source_editions.ARCHIVE).write_text(json.dumps(archive))
        return editions.generate(self.catalogue, self.root, self.locations)

    def test_complete_contents_are_embedded_once_per_case_per_page(self):
        text = self.build()[self.root / 'pages/056.md']
        self.assertEqual(text.count('English interpretation retained in full.'), 1)
        self.assertIn('> German reading.', text)
        self.assertIn('AD?FGX\n# Not a heading\n[Not a link](missing-file.md)', text)
        self.assertIn('Companion source and explanation.', text)
        self.assertIn('**Related source pages:**', text)
        self.assertIn('[p57 A](057.md#source-p57-a)', text)
        self.assertIn('<summary>Comparative source sections from other printed pages</summary>', text)
        self.assertIn('<summary>Machine evidence</summary>', text)
        self.assertEqual(sum(line.startswith('# ') for line in text.splitlines()), 2)
        # The second '# ' occurs inside the unchanged ciphertext example.

    def test_source_and_duplicate_heading_links_are_namespaced(self):
        generated = self.build()
        text = generated[self.root / 'pages/056.md']
        first, second = editions.case_anchor(self.first), editions.case_anchor(self.second)
        self.assertIn('[p56 A](#source-p56-a)', text)
        self.assertNotIn('[Case]', text)
        self.assertNotIn('Concise case study', text)
        self.assertIn(f'<a id="source-p56-a"></a>\n<a id="{first}-p56-a"></a>', text)
        self.assertGreater(text.index('<a id="source-p56-a">'), text.index('## p56 A'))
        self.assertIn(f'[Self](#{first}-evidence)', text)
        self.assertIn(f'[Other](#{second}-evidence)', text)
        self.assertIn(f'[Repeated heading](#{first}-evidence-1)', text)
        self.assertIn(f'<a id="{first}-legacy-title"></a>', text)
        self.assertIn('[External](https://example.org/x#keep)', text)
        self.assertIn('![Cipher](../sources/cipher.png)', text)
        self.assertIn('[Page ranges](README.md)', text)
        self.assertIn('[By subject](../topics/README.md)', text)
        summary = editions.validate(generated, self.catalogue, self.root, self.locations)
        self.assertEqual((summary['pages'], summary['sources']), (2, 3))

    def test_nonembedded_case_link_opens_its_page_edition(self):
        text = self.build()[self.root / 'pages/057.md']
        self.assertIn('[Other](056.md#edition-cases-radio-second-evidence)', text)
        self.assertNotIn('../radio/second.md', text)

    def test_archive_is_sufficient_without_case_files(self):
        generated = self.build()
        self.assertFalse((self.root / self.first).exists())
        self.assertFalse((self.root / self.second).exists())
        self.assertEqual(editions.validate(generated, self.catalogue, self.root,
                                          self.locations)['sources'], 3)

    def test_only_generic_leading_navigation_is_omitted(self):
        text = self.build()[self.root / 'pages/056.md']
        self.assertNotIn('[All cases](../README.md)', text)
        self.assertEqual(text.count('[Reading conventions]'), 1)
        mixed = '[Case guide](../README.md) · [Source image](../../sources/cipher.png)\n'
        self.assertEqual(editions.omit_top_navigation(mixed), '[Source image](../../sources/cipher.png)\n')
        prose = 'Keep this introduction.\n\n[Case index](../README.md)\n'
        self.assertEqual(editions.omit_top_navigation(prose), prose)

    def test_repeated_or_wrong_page_source_anchor_is_rejected(self):
        generated = self.build()
        path = self.root / 'pages/057.md'
        generated[path] += '\n<a id="source-p56-b"></a>\n'
        with self.assertRaisesRegex(AssertionError, 'Wrong printed page'):
            editions.validate(generated, self.catalogue, self.root, self.locations)

    def test_missing_image_and_broken_section_are_rejected(self):
        generated = self.build()
        path = self.root / 'pages/056.md'
        generated[path] += '\n[Broken](#missing-heading)\n'
        with self.assertRaisesRegex(AssertionError, 'Missing anchor'):
            editions.validate(generated, self.catalogue, self.root, self.locations)
        generated = self.build()
        (self.root / 'sources/cipher.png').unlink()
        with self.assertRaisesRegex(AssertionError, 'Missing file'):
            editions.validate(generated, self.catalogue, self.root, self.locations)

    def test_rebase_keeps_queries_and_angle_brackets(self):
        target = editions.rebase_target('<../../experiments/example/README.md?raw=1#check>',
                                        self.first, 'pages/056.md', {})
        self.assertEqual(target, '<../experiments/example/README.md?raw=1#check>')

    def test_home_page_opens_ranges_and_range_opens_full_pages(self):
        pages = {page: {'challenge': [], 'other': []} for page in (56, 57, 75, 230)}
        text = catalog.render(self.catalogue, catalog.ROOT / 'README.md', pages=pages)
        self.assertIn('pages/056-057/README.md', text)
        self.assertIn('pages/075-075/README.md', text)
        self.assertIn('pages/230-230/README.md', text)
        self.assertNotIn('pages/056.md', text)
        band = catalog.render_band(self.catalogue, pages, 50)
        self.assertIn('[56](../056.md)', band)
        self.assertIn('[57](../057.md)', band)
        self.assertNotIn('[p56](#p56)', band)

    def test_current_sections_precede_comparisons_and_keep_every_block(self):
        text = self.build()[self.root / 'pages/057.md']
        self.assertLess(text.index('### p57 A'), text.index('### p56 A'))
        self.assertLess(text.index('Companion source and explanation.'),
                        text.index('<summary>Comparative source sections'))
        for phrase in ('English interpretation retained in full.', 'Companion source and explanation.',
                       '> German reading.', 'AD?FGX\n# Not a heading\n[Not a link](missing-file.md)'):
            self.assertEqual(text.count(phrase), 1)
        self.assertIn('[Repeated heading](#edition-cases-radio-first-evidence-1)', text)
        prefix = editions.case_anchor(self.first)
        _, before = editions.embed_case(self.original, self.first, 'pages/057.md',
                                         {self.first: prefix}, self.catalogue, self.root)
        after = editions.focus_page_sections(before, 57, self.first,
                                              self.catalogue['other'], self.locations)
        content = lambda value: Counter(line for line in value.splitlines() if line.strip())
        self.assertFalse(content(before) - content(after))

    def test_nested_reading_keeps_its_gap_context_and_shared_argument(self):
        self.editions[self.first] = (
            '# First message\n\nIntroduction mentions p57 A without classifying it.\n\n'
            '## p57 A\n\nOther source body.\n\n'
            '## p56 A source and gap model\n\nRetain the complete gap explanation.\n\n'
            '## Conditional result\n\nShared argument before the reading.\n\n'
            '### Readiness\n\n> Recovered readiness clause.\n\n'
            '<details>\n<summary>Raw evidence</summary>\n\n'
            '```text\n### p57 A\nADF?GX\n```\n\n</details>\n')
        self.catalogue['other'][0]['path'] = self.first + '#readiness'
        text = self.build()[self.root / 'pages/056.md']
        comparative = text.index('<summary>Comparative source sections')
        for phrase in ('Retain the complete gap explanation.', 'Shared argument before the reading.',
                       '> Recovered readiness clause.', '```text\n### p57 A\nADF?GX\n```'):
            self.assertEqual(text.count(phrase), 1)
            self.assertLess(text.index(phrase), comparative)
        self.assertGreater(text.index('Other source body.'), comparative)
        self.assertIn('<a id="source-p56-a"></a>\n<a id="edition-cases-radio-first-readiness">', text)

    def test_sections_inside_existing_drawers_are_not_cut(self):
        body = ('Introduction.\n\n<details>\n<summary>Joint evidence</summary>\n\n'
                '<a id="edition-cases-radio-first-p57-a"></a>\n\n'
                '### p57 A\n\nOther-page wording required for this argument.\n\n</details>\n')
        result = editions.focus_page_sections(body, 56, self.first,
                                             self.catalogue['other'], self.locations)
        self.assertEqual(result, body)

    def test_section_naming_both_pages_stays_visible(self):
        body = 'Introduction.\n\n### p57 A / p56 A comparison\n\nA single shared argument.\n'
        result = editions.focus_page_sections(body, 56, self.first,
                                             self.catalogue['other'], self.locations)
        self.assertIn('A single shared argument.', result)
        self.assertNotIn('<details>', result)

    def test_reviewed_procedure_scope_keeps_mixed_source_section_whole(self):
        case = 'cases/radio/late_november_cipher_instructions.md'
        prefix = editions.case_anchor(case)
        headings = [
            ('november-key-reused-because-december-tables-are-missing', 'Earlier key notice.'),
            ('numerical-code-fragment-and-army-routing', 'p226 B2 words.\n\np227 B words.'),
            ('a-cleartext-request-to-avoid-an-unreadable-cipher', 'Cleartext service annotation.'),
        ]
        body = 'Joint introduction.\n\n' + ''.join(
            f'<a id="{prefix}-{slug}"></a>\n\n### {slug.replace("-", " ")}\n\n{text}\n\n'
            for slug, text in headings)
        locations = {'p225_A': (225, 'A'), 'p226_B2': (226, 'B2'), 'p227_B': (227, 'B'),
                     'p228_C1': (228, 'C1'), 'p228_C2': (228, 'C2')}
        rows = [{'id': ident, 'label': ident.replace('_', ' '), 'path': case}
                for ident in locations]
        result = editions.focus_page_sections(body, 226, case, rows, locations)
        boundary = result.index('<summary>Comparative source sections')
        for phrase in ('p226 B2 words.', 'p227 B words.'):
            self.assertEqual(result.count(phrase), 1)
            self.assertLess(result.index(phrase), boundary)
        for phrase in ('Earlier key notice.', 'Cleartext service annotation.'):
            self.assertEqual(result.count(phrase), 1)
            self.assertGreater(result.index(phrase), boundary)


if __name__ == '__main__':
    unittest.main()
