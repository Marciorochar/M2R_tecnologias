"""Tests for stable responsive evidence targets and filenames."""
import unittest
import re
from pathlib import Path

import browser_check


class BrowserEvidenceTargetTests(unittest.TestCase):
    def test_targets_are_three_canonical_routes_at_six_requested_widths(self):
        expected = [
            (route, width)
            for route in ("/", "/servicos", "/contato")
            for width in (320, 390, 768, 1024, 1440, 1920)
        ]
        target_builder = getattr(browser_check, "responsive_targets", lambda: None)
        self.assertEqual(target_builder(), expected)

    def test_shared_motion_control_uses_common_contract(self):
        root = Path(browser_check.ROOT)
        variants = (
            root / 'frontend/index.html',
            root / 'frontend/pages/servicos.html',
            root / 'frontend/pages/blog/automacao-para-pequenos-negocios.html',
            root / 'frontend/pages/projetos/m2r-server.html',
            root / 'frontend/404.html',
        )
        for path in variants:
            source = path.read_text(encoding='utf-8')
            button = re.search(r'<button\b(?=[^>]*data-hero-motion)[^>]*>(.*?)</button>', source, re.S)
            self.assertIsNotNone(button, path)
            self.assertRegex(button.group(0), r'aria-pressed="false"')
            self.assertRegex(button.group(0), r'\bhidden(?:[ >])')
            self.assertRegex(button.group(0), r'aria-label="Pausar movimento do destaque"')
            self.assertEqual(re.sub(r'\s+', ' ', button.group(1)).strip(), 'Pausar movimento', path)
            self.assertEqual(source.count('data-hero-motion'), 1, path)

    def test_capture_names_are_stable_and_route_safe(self):
        name_builder = getattr(browser_check, "responsive_capture_name", lambda *_: None)
        self.assertEqual(name_builder("/", 320), "home-320.png")
        self.assertEqual(name_builder("/servicos", 768), "servicos-768.png")
        self.assertEqual(name_builder("/contato", 1440), "contato-1440.png")
        self.assertIsNone(name_builder("/outro", 390))

    def test_primary_cta_palette_includes_the_existing_circuit_hero_variant(self):
        self.assertIn("rgb(146, 85, 45)", getattr(browser_check, "PRIMARY_CTA_COLORS", ()))

    def test_fixed_control_rectangle_overlap_is_detected(self):
        overlap = getattr(browser_check, "boxes_overlap", lambda *_: None)
        self.assertTrue(overlap({"x": 0, "y": 0, "width": 20, "height": 20},
                                {"x": 10, "y": 10, "width": 20, "height": 20}))
        self.assertFalse(overlap({"x": 0, "y": 0, "width": 10, "height": 10},
                                 {"x": 10, "y": 10, "width": 10, "height": 10}))


if __name__ == "__main__":
    unittest.main()
