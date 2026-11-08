"""Tests for the axe results that gate Chromium smoke checks."""
import unittest

from browser_check import serious_axe_violations


class AccessibilityCheckTests(unittest.TestCase):
    def test_only_serious_and_critical_violations_block(self):
        report = {"violations": [
            {"id": "minor", "impact": "minor", "nodes": [{"target": [".minor"]}]},
            {"id": "moderate", "impact": "moderate", "nodes": [{"target": [".moderate"]}]},
            {"id": "serious", "impact": "serious", "nodes": [{"target": ["#bad"]}]},
            {"id": "critical", "impact": "critical", "nodes": [{"target": ["#critical"]}]},
        ]}
        self.assertEqual(
            [violation["id"] for violation in serious_axe_violations(report)],
            ["serious", "critical"],
        )

    def test_empty_report_passes(self):
        self.assertEqual(serious_axe_violations({"violations": []}), [])


if __name__ == "__main__":
    unittest.main()
