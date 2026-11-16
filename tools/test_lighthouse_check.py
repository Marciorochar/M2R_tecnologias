"""Tests for readable Lighthouse scores and incomplete report handling."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lighthouse_check import extract_lab_metrics, lighthouse_output_name, summarize_lighthouse


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

    def test_lighthouse_output_name_encodes_route_and_device(self):
        self.assertEqual(lighthouse_output_name("/", "mobile"), "lighthouse-home-mobile.json")
        self.assertEqual(lighthouse_output_name("/servicos", "mobile"), "lighthouse-servicos-mobile.json")
        self.assertEqual(lighthouse_output_name("/contato", "desktop"), "lighthouse-contato-desktop.json")

    def test_extract_lab_metrics_reads_lcp_cls_and_marks_inp_unavailable_when_absent(self):
        report = {
            "audits": {
                "largest-contentful-paint": {"numericValue": 1840.4, "displayValue": "1.8 s"},
                "cumulative-layout-shift": {"numericValue": 0.012, "displayValue": "0.012"},
            }
        }
        metrics = extract_lab_metrics(report)
        self.assertEqual(metrics["lcp"], "1.8 s")
        self.assertEqual(metrics["cls"], "0.012")
        self.assertEqual(metrics["inp"], "indisponível (laboratório sem interação)")


if __name__ == "__main__":
    unittest.main()
