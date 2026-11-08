"""Tests for readable Lighthouse scores and incomplete report handling."""
import unittest

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


if __name__ == "__main__":
    unittest.main()
