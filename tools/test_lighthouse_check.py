"""Tests for readable Lighthouse scores and incomplete report handling."""
import unittest
from pathlib import Path

import lighthouse_check
from lighthouse_check import summarize_lighthouse


class LighthouseCheckTests(unittest.TestCase):
    def test_all_four_scores_are_reported(self):
        report = {"categories": {
            "performance": {"score": 0.62},
            "accessibility": {"score": 0.95},
            "best-practices": {"score": 1},
            "seo": {"score": 0.9},
        }}
        summary = summarize_lighthouse(report)
        for expected in ("Desempenho: 62/100", "Acessibilidade: 95/100", "Boas praticas: 100/100", "SEO: 90/100"):
            self.assertIn(expected, summary)

    def test_missing_category_fails_explicitly(self):
        with self.assertRaises(ValueError):
            summarize_lighthouse({"categories": {"performance": {"score": 0.5}}})

    def test_invalid_score_fails_explicitly(self):
        with self.assertRaises(ValueError):
            summarize_lighthouse({"categories": {
                "performance": {"score": None},
                "accessibility": {"score": 0.5},
                "best-practices": {"score": 0.5},
                "seo": {"score": 0.5},
            }})

    def test_route_device_output_names_are_stable(self):
        name_builder = getattr(lighthouse_check, "lighthouse_output_path", lambda *_: None)
        self.assertEqual(name_builder(Path("reports"), "/", "mobile"), Path("reports/home-mobile.json"))
        self.assertEqual(name_builder(Path("reports"), "/servicos", "mobile"), Path("reports/servicos-mobile.json"))

    def test_lab_metrics_use_numeric_values_and_leave_missing_inp_unavailable(self):
        extractor = getattr(lighthouse_check, "extract_lab_metrics", lambda *_: None)
        report = {"audits": {
            "largest-contentful-paint": {"numericValue": 1234.5},
            "cumulative-layout-shift": {"numericValue": 0.04},
        }}
        self.assertEqual(extractor(report), {"lcp_ms": 1234.5, "cls": 0.04, "inp_ms": None})
        formatter = getattr(lighthouse_check, "format_lab_metrics", lambda *_: None)
        self.assertIn("INP: indisponível", formatter(extractor(report)))

    def test_missing_lab_audits_remain_unavailable(self):
        extractor = getattr(lighthouse_check, "extract_lab_metrics", lambda *_: None)
        self.assertEqual(extractor({"audits": {}}), {"lcp_ms": None, "cls": None, "inp_ms": None})

    def test_route_validation_rejects_unknown_paths(self):
        route_resolver = getattr(lighthouse_check, "validate_routes", lambda *_: None)
        self.assertEqual(route_resolver(["/", "/contato"]), ["/", "/contato"])
        with self.assertRaises(ValueError):
            route_resolver(["/unknown"])

    def test_lighthouse_binary_resolution_supports_windows_command_shim(self):
        resolver = getattr(lighthouse_check, "lighthouse_binary_path", lambda *_args, **_kwargs: None)
        root = Path("project")
        self.assertEqual(resolver(root, windows=True), Path("project/node_modules/.bin/lighthouse.cmd"))
        self.assertEqual(resolver(root, windows=False), Path("project/node_modules/.bin/lighthouse"))

    def test_legacy_no_argument_report_filename_is_preserved(self):
        name_builder = getattr(lighthouse_check, "lighthouse_output_path", lambda *_args, **_kwargs: None)
        self.assertEqual(
            name_builder(Path("test-results"), "/", "mobile", legacy_default=True),
            Path("test-results/lighthouse-home.json"),
        )


if __name__ == "__main__":
    unittest.main()
