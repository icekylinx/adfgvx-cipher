"""Fail-closed source-evidence mode tests using an isolated generated fixture."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest

import fitz

from adfgvx.source_evidence import SourceEvidenceError, verify_source_evidence


class SourceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.pdf = self.base / 'source.pdf'
        with fitz.open() as doc:
            page = doc.new_page(width=160, height=120)
            page.draw_rect(fitz.Rect(10, 10, 110, 70), color=(0, 0, 0), fill=(0.7, 0.8, 0.9))
            page.insert_text((15, 40), 'ADFGVX')
            doc.save(self.pdf)
        self.source = {'pdf_bytes': self.pdf.stat().st_size,
                       'pdf_sha256': hashlib.sha256(self.pdf.read_bytes()).hexdigest()}
        with fitz.open(self.pdf) as doc:
            pix = doc[0].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(5, 5, 120, 85),
                                  colorspace=fitz.csRGB, alpha=False)
            pix.save(self.base / 'crop.png')
            self.crop = {'path': 'crop.png', 'pdf_page_1based': 1,
                         'crop_pdf_points': [5, 5, 120, 85], 'render_scale': 2,
                         'width': pix.width, 'height': pix.height, 'channels': 3,
                         'sha256': hashlib.sha256((self.base / 'crop.png').read_bytes()).hexdigest(),
                         'rgb_sha256': hashlib.sha256(pix.samples).hexdigest()}

    def check(self, pdf=None, crop=None, source=None):
        return verify_source_evidence(pdf, source or self.source, [crop or self.crop], self.base)

    def test_default_embedded_png_and_actual_pdf_pixels(self):
        report = self.check(self.pdf)
        self.assertTrue(report['source_pdf']['sha256_verified'])
        self.assertTrue(report['crops'][0]['embedded_png_accessed'])
        self.assertTrue(report['crops'][0]['pdf_pixels_checked'])

    def test_embedded_without_pdf_does_not_claim_source_pixel_check(self):
        report = self.check()
        self.assertTrue(report['crops'][0]['embedded_rgb_checked'])
        self.assertFalse(report['crops'][0]['pdf_pixels_checked'])
        self.assertIsNone(report['source_pdf']['actual_sha256'])
        self.assertIsNone(report['crops'][0]['pdf_render_rgb_sha256'])

    def test_external_without_pdf_never_reads_png_or_fakes_pixel_hash(self):
        crop = dict(self.crop, storage='external_pdf_reference', path='does-not-exist.png')
        report = self.check(crop=crop)
        row = report['crops'][0]
        self.assertEqual(row['verification_mode'], 'external_reference_only_pixels_unchecked')
        self.assertFalse(row['embedded_png_accessed'])
        self.assertFalse(row['pdf_pixels_checked'])
        self.assertIsNone(row['actual_png_sha256'])
        self.assertIsNone(row['embedded_rgb_sha256'])
        self.assertIsNone(row['pdf_render_rgb_sha256'])
        self.assertFalse(report['summary']['all_declared_crops_checked_against_pdf_pixels'])

    def test_external_with_pdf_does_not_require_png(self):
        crop = dict(self.crop, storage='external_pdf_reference', path='absent.png', sha256='f' * 64)
        report = self.check(self.pdf, crop)
        self.assertFalse(report['crops'][0]['embedded_png_accessed'])
        self.assertTrue(report['crops'][0]['pdf_pixels_checked'])
        self.assertIsNone(report['crops'][0]['actual_png_sha256'])

    def test_external_without_path_uses_only_pdf_recipe(self):
        crop = dict(self.crop, storage='external_pdf_reference', fresh_render_cache=True)
        del crop['path']
        del crop['sha256']
        report = self.check(self.pdf, crop)
        row = report['crops'][0]
        self.assertIsNone(row['recorded_png_path'])
        self.assertTrue(row['path_reference'].startswith('pdf:1:crop:'))
        self.assertTrue(row['pdf_pixels_checked'])
        self.assertTrue(row['pdf_render_cache_cleared'])
        self.assertFalse(row['embedded_png_accessed'])

    def test_wrong_pdf_same_length_fails_closed(self):
        wrong = self.base / 'wrong.pdf'
        content = bytearray(self.pdf.read_bytes())
        content[-1] ^= 1
        wrong.write_bytes(content)
        with self.assertRaisesRegex(SourceEvidenceError, 'PDF SHA-256'):
            self.check(wrong, dict(self.crop, storage='external_pdf_reference'))

    def test_bad_rgb_digest_fails_both_modes(self):
        for storage, pdf in [('embedded_png', None), ('external_pdf_reference', self.pdf)]:
            with self.subTest(storage=storage):
                with self.assertRaisesRegex(SourceEvidenceError, 'RGB SHA-256'):
                    self.check(pdf, dict(self.crop, storage=storage, rgb_sha256='0' * 64))

    def test_missing_embedded_png_is_not_downgraded_even_with_pdf(self):
        with self.assertRaisesRegex(SourceEvidenceError, 'Cannot read evidence file'):
            self.check(self.pdf, dict(self.crop, path='missing.png'))

    def test_bad_png_digest_fails(self):
        with self.assertRaisesRegex(SourceEvidenceError, 'PNG SHA-256'):
            self.check(crop=dict(self.crop, sha256='0' * 64))

    def test_existing_aliases_and_conflicting_aliases(self):
        for rect_name in ['clip_points', 'crop_rectangle_pdf_points', 'clip_pdf_points']:
            crop = copy.deepcopy(self.crop)
            crop[rect_name] = crop.pop('crop_pdf_points')
            crop['scale'] = crop.pop('render_scale')
            crop['png_sha256'] = crop.pop('sha256')
            crop['rgb_pixel_sha256'] = crop.pop('rgb_sha256')
            self.assertTrue(self.check(self.pdf, crop)['crops'][0]['pdf_pixels_checked'])
        crop = dict(self.crop, clip_points=[0, 0, 1, 1])
        with self.assertRaisesRegex(SourceEvidenceError, 'Conflicting evidence aliases'):
            self.check(crop=crop)

    def test_unknown_storage_and_missing_rgb_metadata_fail(self):
        with self.assertRaisesRegex(SourceEvidenceError, 'Unsupported crop storage'):
            self.check(crop=dict(self.crop, storage='external'))
        crop = dict(self.crop)
        del crop['rgb_sha256']
        with self.assertRaisesRegex(SourceEvidenceError, 'Missing evidence field'):
            self.check(crop=crop)


if __name__ == '__main__':
    unittest.main()
