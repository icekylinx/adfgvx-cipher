"""Full page editions retain source content and working, unambiguous links."""
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest

from adfgvx import catalog
from adfgvx import page_editions as editions
from adfgvx.case_views import render_case


class PageEditionTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix='adfgvx-page-editions-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ('cases/pages', 'cases/radio', 'experiments/example', 'sources', 'docs',
                          'docs/historical-studies'):
            (self.root / directory).mkdir(parents=True)
        for path in ('cases/README.md', 'cases/pages/README.md', 'docs/reading-conventions.md',
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
        (self.root / self.first).write_text(self.original)
        (self.root / self.second).write_text(
            '# Second message\n\n## Evidence\n\nIndependent explanation.\n'
        )
        self.catalogue = {'challenge': [], 'other': [
            {'id': 'p56_A', 'label': 'p56 A', 'state': 'READING', 'subject': 'First subject',
             'path': self.first + '#p56-a'},
            {'id': 'p56_B', 'label': 'p56 B', 'state': 'PARTIAL', 'subject': 'Second subject',
             'path': self.second},
            {'id': 'p57_A', 'label': 'p57 A', 'state': 'CONDITIONAL', 'subject': 'Companion',
             'path': self.first + '#p57-a'},
        ]}
        self.locations = {'p56_A': (56, 'A'), 'p56_B': (56, 'B'), 'p57_A': (57, 'A')}

    def build(self):
        return editions.generate(self.catalogue, self.root, self.locations)

    def test_complete_contents_are_embedded_once_per_case_per_page(self):
        generated = self.build()
        text = generated[self.root / 'cases/pages/056.md']
        self.assertEqual(text.count('English interpretation retained in full.'), 1)
        self.assertIn('> German reading.', text)
        self.assertIn('AD?FGX\n# Not a heading\n[Not a link](missing-file.md)', text)
        self.assertIn('Companion source and explanation.', text)
        self.assertIn('**Shared edition.**', text)
        self.assertIn('[p57 A](057.md#source-p57-a)', text)
        self.assertIn('<summary>Machine evidence</summary>', text)
        self.assertEqual(sum(line.startswith('# ') for line in text.splitlines()), 2)
        # The second '# ' occurs inside the unchanged ciphertext example.

    def test_source_and_duplicate_heading_links_are_namespaced(self):
        generated = self.build()
        text = generated[self.root / 'cases/pages/056.md']
        first, second = editions.case_anchor(self.first), editions.case_anchor(self.second)
        self.assertIn(f'[Reading](#{first}-p56-a)', text)
        self.assertIn('[Case](../radio/first.md)', text)
        self.assertNotIn('[Case](../radio/first.md#', text)
        self.assertIn(f'[Self](#{first}-evidence)', text)
        self.assertIn(f'[Other](#{second}-evidence)', text)
        self.assertIn(f'[Repeated heading](#{first}-evidence-1)', text)
        self.assertIn(f'<a id="{first}-legacy-title"></a>', text)
        self.assertIn('[External](https://example.org/x#keep)', text)
        self.assertIn('![Cipher](../../sources/cipher.png)', text)
        summary = editions.validate(generated, self.catalogue, self.root, self.locations)
        self.assertEqual((summary['pages'], summary['sources']), (2, 3))

    def test_nonembedded_case_link_keeps_its_original_destination(self):
        text = self.build()[self.root / 'cases/pages/057.md']
        self.assertIn('[Other](../radio/second.md#evidence)', text)

    def test_case_brief_wrapper_does_not_change_full_page_editions(self):
        expected = self.build()
        wrapped = render_case(self.first, self.original,
                              {'summary': ['A new concise English meaning.']}, [56, 57])
        (self.root / self.first).write_text(wrapped)
        actual = self.build()
        self.assertEqual(actual, expected)
        self.assertNotIn('A new concise English meaning.', actual[self.root / 'cases/pages/056.md'])

    def test_only_generic_leading_navigation_is_omitted(self):
        text = self.build()[self.root / 'cases/pages/056.md']
        self.assertNotIn('[All cases](../README.md)', text)
        self.assertEqual(text.count('[Reading conventions]'), 1)
        mixed = '[Case guide](../README.md) · [Source image](../../sources/cipher.png)\n'
        self.assertEqual(editions.omit_top_navigation(mixed), mixed)
        prose = 'Keep this introduction.\n\n[Case index](../README.md)\n'
        self.assertEqual(editions.omit_top_navigation(prose), prose)

    def test_repeated_or_wrong_page_source_anchor_is_rejected(self):
        generated = self.build()
        path = self.root / 'cases/pages/057.md'
        generated[path] += '\n<a id="source-p56-b"></a>\n'
        with self.assertRaisesRegex(AssertionError, 'Wrong printed page'):
            editions.validate(generated, self.catalogue, self.root, self.locations)

    def test_missing_image_and_broken_section_are_rejected(self):
        generated = self.build()
        path = self.root / 'cases/pages/056.md'
        generated[path] += '\n[Broken](#missing-heading)\n'
        with self.assertRaisesRegex(AssertionError, 'Missing anchor'):
            editions.validate(generated, self.catalogue, self.root, self.locations)
        generated = self.build()
        (self.root / 'sources/cipher.png').unlink()
        with self.assertRaisesRegex(AssertionError, 'Missing file'):
            editions.validate(generated, self.catalogue, self.root, self.locations)

    def test_rebase_keeps_queries_and_angle_brackets(self):
        target = editions.rebase_target('<../../experiments/example/README.md?raw=1#check>',
                                        self.first, 'cases/pages/056.md', {})
        self.assertEqual(target, '<../../experiments/example/README.md?raw=1#check>')

    def test_home_page_numbers_open_dedicated_editions_directly(self):
        pages = {page: {'challenge': [], 'other': []} for page in (56, 75, 230)}
        text = catalog.render(self.catalogue, catalog.ROOT / 'README.md', pages=pages)
        number_links = re.findall(r'\[(\d+)\]\(([^)]+)\)', text)
        self.assertEqual(number_links, [
            ('56', 'cases/pages/056.md'),
            ('75', 'cases/pages/075.md'),
            ('230', 'cases/pages/230.md'),
        ])


if __name__ == '__main__':
    unittest.main()
