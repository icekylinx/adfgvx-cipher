"""Verify source-crop evidence with explicit local and external-reference modes.

ADFGVX Cipher — icekylinx and GPT-6 Astra Pro. Apache-2.0.

``embedded_png`` (the default) always checks the local PNG bytes and decoded
RGB pixels. ``external_pdf_reference`` never opens the recorded PNG path. Both
modes can verify actual source pixels when the caller supplies the original
PDF; an absent PDF is always reported as an unchecked source-pixel comparison.
This helper reads evidence only. It never creates, downloads, or uploads it.
"""
from __future__ import annotations

import hashlib
import math
from pathlib import Path
import re
from collections.abc import Mapping, Sequence


class SourceEvidenceError(ValueError):
    """Declared source evidence is missing, inconsistent, or does not match."""


def _require(condition, message):
    if not condition:
        raise SourceEvidenceError(message)


def _alias(data, names, *, required=True):
    present = [(name, data[name]) for name in names if name in data]
    if not present:
        if required:
            raise SourceEvidenceError('Missing evidence field: ' + ' / '.join(names))
        return None
    value = present[0][1]
    _require(all(other == value for _, other in present),
             'Conflicting evidence aliases: ' + ', '.join(name for name, _ in present))
    return value


def _digest_value(value, description):
    _require(isinstance(value, str) and re.fullmatch(r'[0-9a-fA-F]{64}', value) is not None,
             description + ' must be an explicit SHA-256 hexadecimal digest')
    return value.lower()


def _positive_int(value, description):
    _require(isinstance(value, int) and not isinstance(value, bool) and value > 0,
             description + ' must be a positive integer')
    return value


def _file_digest(path):
    try:
        with path.open('rb') as stream:
            digest = hashlib.sha256()
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(block)
            return digest.hexdigest()
    except OSError as exc:
        raise SourceEvidenceError(f'Cannot read evidence file {path}: {exc}') from exc


def _crop_metadata(crop):
    _require(isinstance(crop, Mapping), 'Each crop must be a metadata mapping')
    storage = crop.get('storage', 'embedded_png')
    _require(storage in {'embedded_png', 'external_pdf_reference'},
             f'Unsupported crop storage mode: {storage!r}')
    page = _positive_int(_alias(crop, ['pdf_page_1based']), 'PDF page number')
    rect = _alias(crop, ['crop_pdf_points', 'clip_points',
                         'crop_rectangle_pdf_points', 'clip_pdf_points'])
    _require(isinstance(rect, (list, tuple)) and len(rect) == 4,
             'Crop rectangle must contain four PDF-point coordinates')
    _require(all(isinstance(x, (int, float)) and not isinstance(x, bool)
                 and math.isfinite(x) for x in rect), 'Crop rectangle coordinates must be finite numbers')
    _require(rect[0] < rect[2] and rect[1] < rect[3], 'Crop rectangle must have positive area')
    recorded_path = crop.get('path')
    if storage == 'embedded_png':
        _require(isinstance(recorded_path, str) and bool(recorded_path),
                 'An embedded crop requires a nonempty local PNG path')
    elif recorded_path is not None:
        _require(isinstance(recorded_path, str) and bool(recorded_path),
                 'An optional external path must be a nonempty provenance reference')
    reference = recorded_path if recorded_path is not None else crop.get('reference', crop.get('id'))
    if reference is None:
        reference = f'pdf:{page}:crop:' + ','.join(str(x) for x in rect)
    _require(isinstance(reference, str) and bool(reference), 'Crop reference must be a nonempty string')
    scale = _alias(crop, ['render_scale', 'scale'])
    _require(isinstance(scale, (int, float)) and not isinstance(scale, bool)
             and math.isfinite(scale) and scale > 0, 'Render scale must be finite and positive')
    width = _positive_int(_alias(crop, ['width']), 'Crop pixel width')
    height = _positive_int(_alias(crop, ['height']), 'Crop pixel height')
    _require(crop.get('channels', 3) == 3, 'The declared pixel digest must describe three-channel RGB')
    rgb = _digest_value(_alias(crop, ['rgb_sha256', 'rgb_pixel_sha256']), 'RGB pixel digest')
    png = _alias(crop, ['sha256', 'png_sha256'], required=storage == 'embedded_png')
    if png is not None:
        png = _digest_value(png, 'PNG file digest')
    fresh = crop.get('fresh_render_cache', False)
    _require(isinstance(fresh, bool), 'fresh_render_cache must be a boolean')
    return {'storage': storage, 'path': reference, 'recorded_path': recorded_path,
            'fresh_render_cache': fresh, 'page': page, 'rect': list(rect),
            'scale': scale, 'width': width, 'height': height,
            'rgb_sha256': rgb, 'png_sha256': png}


def verify_source_evidence(pdf, source, crops, base):
    """Check declared source evidence and return a truthful, runtime mode report.

    Args:
        pdf: Original PDF path, or ``None`` for a check without the PDF.
        source: Mapping with ``pdf_bytes`` / ``bytes`` and
            ``pdf_sha256`` / ``sha256``. Conflicting aliases are rejected.
        crops: Sequence of crop mappings. Accepted crop aliases are
            ``crop_pdf_points`` / ``clip_points`` /
            ``crop_rectangle_pdf_points`` / ``clip_pdf_points``;
            ``render_scale`` / ``scale``; ``sha256`` / ``png_sha256``;
            ``rgb_sha256`` / ``rgb_pixel_sha256``. Every crop needs
            ``pdf_page_1based``, ``width`` and ``height``. Embedded mode
            additionally requires ``path``. External mode may keep ``path``
            as provenance or use ``reference`` / ``id``; if none is present,
            a page-and-rectangle reference label is generated without file I/O.
            ``channels`` defaults to three and must describe RGB.
            ``fresh_render_cache=True`` clears the MuPDF rendering cache
            immediately before rendering, matching the recorded crop recipe.
        base: Directory against which embedded PNG paths are resolved.

    The return value is a report of checks actually performed. It intentionally
    differs between calls with and without the PDF. For an external reference,
    ``path`` and any PNG digest remain provenance metadata: that path is never
    opened. A supplied PDF must match both its declared byte count and SHA-256
    before any rendering occurs. Each rendered crop must match its declared
    dimensions and RGB digest, and an embedded crop must also match pixel bytes.

    Raises:
        SourceEvidenceError: Missing metadata/files, conflicting aliases,
            unsupported storage, or any evidence mismatch. Required checks
            never silently downgrade to a weaker mode.
    """
    _require(isinstance(source, Mapping), 'Source must be a metadata mapping')
    _require(isinstance(crops, Sequence) and not isinstance(crops, (str, bytes)),
             'Crops must be a sequence of metadata mappings')
    expected_bytes = _positive_int(_alias(source, ['pdf_bytes', 'bytes']), 'PDF byte count')
    expected_sha = _digest_value(_alias(source, ['pdf_sha256', 'sha256']), 'PDF digest')
    specifications = [_crop_metadata(crop) for crop in crops]
    base = Path(base)
    pdf_report = {'provided': pdf is not None, 'byte_count_verified': False,
                  'sha256_verified': False, 'expected_bytes': expected_bytes,
                  'expected_sha256': expected_sha, 'actual_bytes': None,
                  'actual_sha256': None}
    document = None
    fitz = None
    if pdf is not None:
        pdf_path = Path(pdf)
        try:
            size = pdf_path.stat().st_size
        except OSError as exc:
            raise SourceEvidenceError(f'Cannot read source PDF {pdf_path}: {exc}') from exc
        _require(size == expected_bytes, 'Source PDF byte count does not match')
        actual_sha = _file_digest(pdf_path)
        _require(actual_sha == expected_sha, 'Source PDF SHA-256 does not match')
        try:
            import fitz
            document = fitz.open(pdf_path)
            if not document.is_pdf:
                document.close()
                document = None
                raise SourceEvidenceError('Supplied source is not a PDF document')
        except SourceEvidenceError:
            raise
        except Exception as exc:
            raise SourceEvidenceError(f'Cannot open verified PDF bytes: {exc}') from exc
        pdf_report.update(byte_count_verified=True, sha256_verified=True,
                          actual_bytes=size, actual_sha256=actual_sha)
    checked = []
    try:
        for spec in specifications:
            embedded = spec['storage'] == 'embedded_png'
            row = {'path_reference': spec['path'], 'storage': spec['storage'],
                   'recorded_png_path': spec['recorded_path'],
                   'pdf_page_1based': spec['page'],
                   'embedded_png_accessed': False, 'embedded_png_sha256_checked': False,
                   'embedded_rgb_checked': False, 'pdf_pixels_checked': False,
                   'pdf_render_cache_cleared': False,
                   'expected_png_sha256': spec['png_sha256'], 'actual_png_sha256': None,
                   'expected_rgb_sha256': spec['rgb_sha256'],
                   'embedded_rgb_sha256': None, 'pdf_render_rgb_sha256': None}
            embedded_rgb = None
            if embedded:
                image_path = base / spec['path']
                actual_png = _file_digest(image_path)
                _require(actual_png == spec['png_sha256'], f'PNG SHA-256 mismatch: {spec["path"]}')
                try:
                    from PIL import Image
                    with Image.open(image_path) as image:
                        _require(image.format == 'PNG', f'Embedded evidence is not PNG: {spec["path"]}')
                        rgb = image.convert('RGB')
                        _require(rgb.size == (spec['width'], spec['height']),
                                 f'Embedded RGB dimensions mismatch: {spec["path"]}')
                        embedded_rgb = rgb.tobytes()
                except SourceEvidenceError:
                    raise
                except Exception as exc:
                    raise SourceEvidenceError(f'Cannot decode embedded PNG {spec["path"]}: {exc}') from exc
                pixel_digest = hashlib.sha256(embedded_rgb).hexdigest()
                _require(pixel_digest == spec['rgb_sha256'], f'Embedded RGB SHA-256 mismatch: {spec["path"]}')
                row.update(embedded_png_accessed=True, embedded_png_sha256_checked=True,
                           embedded_rgb_checked=True, actual_png_sha256=actual_png,
                           embedded_rgb_sha256=pixel_digest)
            if document is not None:
                _require(spec['page'] <= len(document), f'PDF crop page is outside the document: {spec["page"]}')
                try:
                    if spec['fresh_render_cache']:
                        fitz.TOOLS.store_shrink(100)
                        row['pdf_render_cache_cleared'] = True
                    pix = document[spec['page'] - 1].get_pixmap(
                        matrix=fitz.Matrix(spec['scale'], spec['scale']),
                        clip=fitz.Rect(*spec['rect']), colorspace=fitz.csRGB, alpha=False)
                except Exception as exc:
                    raise SourceEvidenceError(f'Cannot render source crop {spec["path"]}: {exc}') from exc
                _require((pix.width, pix.height, pix.n) == (spec['width'], spec['height'], 3),
                         f'PDF-render dimensions/channels mismatch: {spec["path"]}')
                pixels = pix.samples
                actual_rgb = hashlib.sha256(pixels).hexdigest()
                _require(actual_rgb == spec['rgb_sha256'], f'PDF-render RGB SHA-256 mismatch: {spec["path"]}')
                if embedded:
                    _require(pixels == embedded_rgb, f'Embedded PNG pixels differ from PDF render: {spec["path"]}')
                row.update(pdf_pixels_checked=True, pdf_render_rgb_sha256=actual_rgb)
            row['verification_mode'] = (
                ('embedded_png_and_pdf_pixels' if embedded else 'external_reference_and_pdf_pixels')
                if document is not None else
                ('embedded_png_only_pdf_pixels_unchecked' if embedded else 'external_reference_only_pixels_unchecked'))
            checked.append(row)
    finally:
        if document is not None:
            document.close()
    return {
        'schema': 'adfgvx-source-evidence-check-report-v1',
        'source_pdf': pdf_report, 'crops': checked,
        'summary': {
            'declared_crops': len(checked),
            'embedded_pngs_checked': sum(row['embedded_png_accessed'] for row in checked),
            'external_pdf_references': sum(row['storage'] == 'external_pdf_reference' for row in checked),
            'crops_checked_against_pdf_pixels': sum(row['pdf_pixels_checked'] for row in checked),
            'crops_without_pdf_pixel_check': sum(not row['pdf_pixels_checked'] for row in checked),
            'all_declared_crops_checked_against_pdf_pixels': bool(checked) and all(row['pdf_pixels_checked'] for row in checked),
        },
        'scope': 'The report records performed file and pixel checks only. An external reference without the PDF verifies no source pixels; an embedded PNG without the PDF verifies its frozen bytes and RGB digest, not its derivation from the source PDF.',
    }
