import unittest

from adfgvx.case_views import (
    START, END, OPEN, CLOSE, case_records, page_links, render_case,
    split_original, unwrap_original,
)


class CaseViewTests(unittest.TestCase):
    def setUp(self):
        self.summary = {'summary': ['The sender asks for ships to carry troops home.']}

    def test_original_roundtrip_and_idempotence(self):
        original = ('# A shipping inquiry\n\n[Reading conventions](../docs/reading-conventions.md)\n\n'
                    '## First part\n\n**Readable German:**\n\n> Schiffe erbeten.\n\n'
                    '<details>\n<summary>Source</summary>\n\n```text\nADFGVX\n```\n\n</details>\n')
        rendered = render_case('cases/p89.md', original, self.summary, [89, 98])
        self.assertEqual(unwrap_original(rendered), original)
        self.assertEqual(render_case('cases/p89.md', rendered, self.summary, [89, 98]), rendered)
        self.assertEqual(rendered.count('\n# '), 0)
        self.assertEqual(rendered.count('## First part'), 1)
        self.assertIn('[p. 89](pages/089.md)', rendered)
        self.assertIn('[p. 98](pages/098.md)', rendered)

    def test_preamble_and_unicode_and_missing_final_newline(self):
        original = '<a id="legacy-title"></a>\n\n# Rückkehr\n\nExact original body: ü, —, ?'
        rendered = render_case('cases/naval/example.md', original, self.summary, [56, 100])
        self.assertTrue(rendered.startswith('<a id="legacy-title"></a>\n\n# Rückkehr\n'))
        self.assertEqual(unwrap_original(rendered), original)
        self.assertIn('[p. 56](../pages/056.md)', rendered)
        self.assertIn('[p. 100](../pages/100.md)', rendered)

    def test_source_edit_in_wrapper_is_retained(self):
        original = '# Title\n\nOld source reading.\n'
        rendered = render_case('cases/p56.md', original, self.summary, [56])
        edited = rendered.replace('Old source reading.', 'Corrected source reading.')
        rerendered = render_case('cases/p56.md', edited, self.summary, [56])
        self.assertEqual(unwrap_original(rerendered), original.replace('Old', 'Corrected'))

    def test_no_loss_of_nested_drawers_or_marker_like_prose(self):
        original = '# Title\n\n<details>\n<summary>One</summary>\n\n<details>\n<summary>Two</summary>\n\nText\n\n</details>\n</details>\n'
        rendered = render_case('cases/p56.md', original, self.summary, [56])
        self.assertEqual(rendered.count('<details>'), 3)
        self.assertEqual(unwrap_original(rendered), original)

    def test_malformed_wrapper_fails_without_discarding_content(self):
        with self.assertRaises(ValueError):
            unwrap_original('# Title\n\n' + START + '\nSome source text')
        with self.assertRaises(ValueError):
            unwrap_original('# Title\n\n' + OPEN + 'Source' + CLOSE + 'unexpected tail')

    def test_only_catalogued_cases_and_fragments_group_once(self):
        data = {'challenge': [{'id': 'p56', 'path': 'cases/p56.md'}],
                'other': [{'id': 'p57_A', 'path': 'cases/radio/shared.md#p57-a'},
                          {'id': 'p58_B', 'path': 'cases/radio/shared.md#p58-b'}]}
        rows = case_records(data)
        self.assertEqual(set(rows), {'cases/p56.md', 'cases/radio/shared.md'})
        self.assertEqual(len(rows['cases/radio/shared.md']), 2)
        self.assertEqual(page_links('cases/radio/shared.md', [57, 58]),
                         '[p. 57](../pages/057.md) · [p. 58](../pages/058.md)')


if __name__ == '__main__':
    unittest.main()
