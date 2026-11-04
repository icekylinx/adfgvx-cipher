"""Editorial formatting must not rewrite source evidence or public targets."""
import unittest

from adfgvx.editorial_style import inline, markdown
from adfgvx.navigation import anchors, targets


class EditorialStyleTests(unittest.TestCase):
    def test_printed_pages_and_dates_in_reader_prose(self):
        self.assertEqual(inline('Childs p. 153; pp. 152-153; pp 226–227; November 7–8, 1918.'),
                         'Childs p153; pp152–153; pp226–227; 7–8 November 1918.')
        self.assertEqual(inline('p153a and p153b; p153 A3; Nov10–12; PDF p. 5.'),
                         'p153a and p153b; p153 A3; Nov10–12; PDF page 5.')

    def test_literals_quotes_destinations_and_attributes_are_exact(self):
        source = ('[p. 153](../p.153.md#November-7 "p. 153") `p. 153` '
                  '``November 7 ` raw`` "November 7" “p. 153” '
                  '<a id="p. 153"></a> https://example.org/p.153')
        self.assertEqual(inline(source), source.replace('[p. 153]', '[p153]', 1))

    def test_evidence_blocks_are_byte_identical(self):
        evidence = ('> p. 153; November 7; roundtrip\n\n'
                    '```text\np. 153 November 7\n```\n\n'
                    '    p. 153 November 7\n\n'
                    '[source]: https://example.org/p.153 "November 7"\n')
        self.assertEqual(markdown(evidence), evidence)

    def test_multiline_literal_and_quotation_remain_exact(self):
        text = ('Header `p. 153\nNovember 7` compared with p. 154.\n\n'
                'The source says “p. 153\nNovember 7”, on p. 155.\n')
        self.assertEqual(markdown(text), text.replace('with p. 154', 'with p154')
                         .replace('on p. 155', 'on p155'))

    def test_legacy_heading_links_survive(self):
        source = '# November 7: Childs p. 153\n\n[Reading](#november-7-childs-p-153)\n'
        formatted = markdown(source)
        self.assertTrue(formatted.startswith('# 7 November: Childs p153\n'))
        self.assertIn('november-7-childs-p-153', anchors(formatted))
        self.assertEqual(list(targets(source)), list(targets(formatted)))
        self.assertEqual(markdown(formatted), formatted)

    def test_duplicate_heading_aliases_remain_distinct(self):
        formatted = markdown('# November 7\n\n## November 7\n')
        self.assertIn('november-7', anchors(formatted))
        self.assertIn('november-7-1', anchors(formatted))

    def test_tables_and_repeated_passes(self):
        source = '| Page | Date |\n|---|---:|\n| p. 153 | November 7 |\n'
        formatted = markdown(source)
        self.assertIn('| --- | ---: |', formatted)
        self.assertIn('| p153 | 7 November |', formatted)
        self.assertEqual(markdown(formatted), formatted)

    def test_machine_ids_and_key_names_are_not_editorial_ranges(self):
        value = 'p132_radio_service; p153_A3; Nov10–12; 1918-11-07; 500-12519-274.'
        self.assertEqual(inline(value), value)

    def test_caption_punctuation_does_not_change_its_literal_qualifier(self):
        value = '**Meaning.** The raw field is `p. 153`.\n**Readable German** — retain `X`.'
        self.assertEqual(markdown(value), '**Meaning:** The raw field is `p. 153`.\n'
                         '**Readable German:** retain `X`.')

    def test_lazy_blockquote_continuation_is_literal(self):
        source = '> Verbatim report:\np. 153 November 7\n\nBody p. 154.\n'
        self.assertEqual(markdown(source), source.replace('Body p. 154', 'Body p154'))

    def test_straight_multiline_quotation_is_literal(self):
        source = 'The report says "p. 153\nNovember 7", on p. 154.\n'
        self.assertEqual(markdown(source), source.replace('on p. 154', 'on p154'))

    def test_heading_collision_does_not_retarget_existing_section(self):
        source = ('# November 7\n\nFirst section.\n\n'
                  '# 7 November\n\nSecond section.\n\n'
                  '[First](#november-7) [Second](#7-november)\n')
        # Both old slugs name distinct sections. Normalizing the first heading
        # into the second slug would silently send the second link to the first.
        self.assertEqual(markdown(source), source)

    def test_cross_month_date_range_formats_both_endpoints(self):
        self.assertEqual(inline('October 31-November 2; November 30–December 1.'),
                         '31 October–2 November; 30 November–1 December.')

    def test_ambiguous_abbreviated_page_ranges_are_not_expanded(self):
        source = 'pp. 152–3; p153-2; 1917–18; Nov10–12.'
        self.assertEqual(inline(source), source)

    def test_html_code_elements_preserve_literal_contents(self):
        for source in ('<pre>\np. 153 November 7\n</pre>\n',
                       '<code>p. 153 November 7</code>\n'):
            with self.subTest(source=source):
                self.assertEqual(markdown(source), source)

    def test_fence_with_trailing_text_is_not_a_closing_fence(self):
        source = '~~~text\n~~~ still literal\np. 153 November 7\n~~~\n'
        self.assertEqual(markdown(source), source)

    def test_escaped_quotes_do_not_end_literal_span(self):
        source = r'The source says "p. 153 \"and p. 154\" November 7".'
        self.assertEqual(markdown(source), source)


if __name__ == '__main__':
    unittest.main()
