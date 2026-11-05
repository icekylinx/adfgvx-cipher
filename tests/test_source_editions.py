"""Archived source text retains exact bytes and stable public destinations."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from adfgvx import source_editions as sources


class SourceEditionTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix='adfgvx-source-editions-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'data').mkdir()
        self.key = 'cases/radio/shared.md'
        self.alias = 'cases/other/shared.md'
        self.original = '<a id="legacy"></a>\r\n# Rückkehr\r\n\r\n> Exact ? text.\r\n'
        self.data = {'schema': sources.SCHEMA, 'editions': {self.key: {
            'text': self.original,
            'sha256': hashlib.sha256(self.original.encode()).hexdigest()}},
            'aliases': {self.alias: self.key}}
        self.write_archive()
        self.catalogue = {'challenge': [], 'other': [
            {'id': 'p56_A', 'path': self.key + '#first', 'printed_page': 56},
            {'id': 'p75_B', 'path': self.key + '#second', 'printed_page': 75},
        ]}

    def write_archive(self):
        (self.root / sources.ARCHIVE).write_text(json.dumps(self.data))

    def test_exact_unicode_and_line_endings_without_physical_case(self):
        self.assertEqual(sources.load_editions(self.root), {self.key: self.original})
        self.assertEqual(sources.read_source_text(self.root / self.key, root=self.root),
                         self.original)
        self.assertTrue(sources.source_exists(self.root / self.key, root=self.root))
        self.assertFalse((self.root / self.key).exists())

    def test_alias_and_archive_precedence(self):
        path = self.root / self.key
        path.parent.mkdir(parents=True)
        path.write_text('Obsolete public view')
        for logical in (self.key, self.alias):
            self.assertEqual(sources.read_source_text(logical, root=self.root), self.original)
            self.assertTrue(sources.source_exists(logical, root=self.root))

    def test_real_file_fallback_preserves_encoding_and_missing_file_errors(self):
        path = self.root / 'ordinary.txt'
        path.write_bytes('Ä'.encode('latin-1'))
        self.assertEqual(sources.read_source_text(path, 'latin-1', root=self.root), 'Ä')
        self.assertTrue(sources.source_exists(path, root=self.root))
        self.assertFalse(sources.source_exists(self.root / 'missing.txt', root=self.root))
        with self.assertRaises(FileNotFoundError):
            sources.read_source_text(self.root / 'missing.txt', root=self.root)

    def test_corrupt_text_fails_closed(self):
        self.data['editions'][self.key]['text'] += 'changed'
        self.write_archive()
        with self.assertRaisesRegex(ValueError, 'integrity mismatch'):
            sources.load_editions(self.root)

    def test_invalid_alias_fails_closed(self):
        self.data['aliases'][self.alias] = 'cases/missing.md'
        self.write_archive()
        with self.assertRaisesRegex(ValueError, 'Invalid source-edition alias'):
            sources.load_editions(self.root)

    def test_matching_fragment_selects_its_physical_page(self):
        self.assertEqual(sources.page_target(self.key + '#second', self.catalogue, self.root),
                         'pages/075.md#edition-cases-radio-shared-second')
        self.assertEqual(sources.page_target(self.alias + '#second', self.catalogue, self.root),
                         'pages/075.md#edition-cases-radio-shared-second')

    def test_shared_context_uses_first_page_and_preserves_queries(self):
        self.assertEqual(sources.page_target(self.key + '?raw=1#legacy', self.catalogue, self.root),
                         'pages/056.md?raw=1#edition-cases-radio-shared-legacy')
        self.assertEqual(sources.page_target(self.key, self.catalogue, self.root),
                         'pages/056.md#edition-cases-radio-shared')
        self.assertEqual(sources.page_target('sources/image.png', self.catalogue, self.root),
                         'sources/image.png')

    def test_materialize_and_clean_keep_exact_bytes(self):
        public_page = self.root / 'pages/056.md'
        public_page.parent.mkdir()
        public_page.write_text('# Public page\n')
        self.assertEqual(sources.materialize_editions(self.root), [self.key])
        self.assertEqual((self.root / self.key).read_bytes(), self.original.encode('utf-8'))
        self.assertEqual(sources.materialize_editions(self.root), [])
        self.assertFalse((self.root / self.alias).exists())
        self.assertEqual(sources.clean_editions(self.root), ([self.key], []))
        self.assertFalse((self.root / self.key).exists())
        self.assertEqual(sources.load_editions(self.root)[self.key], self.original)
        self.assertEqual(public_page.read_text(), '# Public page\n')

    def test_edited_fixture_is_never_overwritten_or_deleted(self):
        sources.materialize_editions(self.root)
        path = self.root / self.key
        path.write_text('A new source correction.\n')
        with self.assertRaisesRegex(ValueError, 'Preserving existing files'):
            sources.materialize_editions(self.root)
        self.assertEqual(sources.clean_editions(self.root), ([], [self.key]))
        self.assertEqual(path.read_text(), 'A new source correction.\n')

    def test_retained_earlier_edition_uses_explicit_research_target(self):
        earlier = 'cases/radio/earlier.md'
        destination = 'experiments/earlier/README.md'
        self.data['editions'][earlier] = dict(self.data['editions'][self.key])
        self.data['public_targets'] = {earlier: destination}
        target = self.root / destination
        target.parent.mkdir(parents=True)
        target.write_text('# Earlier research\n\n## Evidence\n')
        self.write_archive()
        self.assertEqual(len(sources.load_editions(self.root)), 2)
        self.assertEqual(sources.page_target(earlier, self.catalogue, self.root), destination)
        self.assertEqual(sources.page_target(earlier + '#evidence', self.catalogue, self.root),
                         destination + '#evidence')
        self.assertEqual(sources.page_target(earlier + '#absent', self.catalogue, self.root),
                         destination)
        self.assertEqual(set(sources.materialize_editions(self.root)), {self.key, earlier})
        self.assertEqual((self.root / earlier).read_bytes(), self.original.encode())

    def test_old_guides_and_data_references_use_current_public_routes(self):
        expected = {
            **sources.GUIDE_TARGETS,
            **sources.DATA_TARGETS,
            'cases/README.md#the-original-22-challenges': 'topics/README.md#original-challenges',
            'cases/README.md#browse-by-topic': 'topics/README.md#subjects',
            'cases/README.md#how-to-read-a-case': 'docs/reading-conventions.md#source-editions',
            'cases/radio/README.md?raw=1#service': 'topics/radio.md?raw=1#service',
        }
        for legacy, destination in expected.items():
            with self.subTest(legacy=legacy):
                self.assertEqual(sources.page_target(legacy, root=self.root), destination)

    def test_embedded_old_page_and_document_links_use_relocated_targets(self):
        expected = {
            'cases/pages/056.md?raw=1#source-p56-a': 'pages/056.md?raw=1#source-p56-a',
            'cases/pages/050-074/README.md#p71': 'pages/056-074/README.md#p71',
            'cases/pages/225-249/README.md': 'pages/225-230/README.md',
            'experiments/corpus_attack/SOURCE_FAMILIES.md#source-fit':
                'experiments/corpus_attack/README.md#source-fit',
            'docs/historical-studies/what-retreat-cost.md#a-remittance-was-not-yet-a-payout':
                'docs/historical-studies/cash-procurement-liquidation.md#a-remittance-was-not-yet-a-payout',
        }
        for old, new in expected.items():
            self.assertEqual(sources.page_target(old, root=self.root), new)


if __name__ == '__main__':
    unittest.main()
