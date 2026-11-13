"""Tests for stable responsive evidence targets and filenames."""
import unittest

import browser_check


class BrowserEvidenceTargetTests(unittest.TestCase):
    def test_targets_are_three_canonical_routes_at_five_requested_widths(self):
        expected = [
            (route, width)
            for route in ("/", "/servicos", "/contato")
            for width in (320, 390, 768, 1024, 1440)
        ]
        target_builder = getattr(browser_check, "responsive_targets", lambda: None)
        self.assertEqual(target_builder(), expected)

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
