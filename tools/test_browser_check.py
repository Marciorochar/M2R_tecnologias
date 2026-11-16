"""Tests for responsive evidence target generation and safe capture filenames."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from browser_check import EVIDENCE_ROUTES, EVIDENCE_WIDTHS, evidence_capture_name, responsive_evidence_targets


class BrowserCheckEvidenceTests(unittest.TestCase):
    def test_responsive_targets_cover_three_routes_across_five_widths(self):
        self.assertEqual(EVIDENCE_ROUTES, ("/", "/servicos", "/contato"))
        self.assertEqual(EVIDENCE_WIDTHS, (320, 390, 768, 1024, 1440))
        targets = responsive_evidence_targets()
        self.assertEqual(len(targets), 15)
        self.assertEqual(
            targets[0],
            {"route": "/", "width": 320, "filename": "home-320.png"},
        )
        self.assertEqual(
            targets[-1],
            {"route": "/contato", "width": 1440, "filename": "contato-1440.png"},
        )

    def test_evidence_capture_name_is_route_safe(self):
        self.assertEqual(evidence_capture_name("/", 390), "home-390.png")
        self.assertEqual(evidence_capture_name("/servicos", 768), "servicos-768.png")
        self.assertEqual(evidence_capture_name("/contato", 1440), "contato-1440.png")


if __name__ == "__main__":
    unittest.main()
