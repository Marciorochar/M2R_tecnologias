"""Tests for the axe results that gate Chromium smoke checks."""
import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import browser_check
from browser_check import check_accessibility, serious_axe_violations


class FakePage:
    url = 'http://127.0.0.1:5500/exemplo'

    def __init__(self, report):
        self.report = report

    def evaluate(self, script, tags):
        assert 'window.axe.run' in script
        assert tags == browser_check.AXE_TAGS
        return self.report


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

    def test_nonblocking_findings_are_reported_with_route_and_selector(self):
        report = {"violations": [
            {"id": "minor-issue", "impact": "minor", "nodes": [{"target": [".caption"]}]},
            {"id": "moderate-issue", "impact": "moderate", "nodes": [{"target": ["#navigation"]}]},
        ]}
        stream = io.StringIO()
        with redirect_stdout(stream):
            check_accessibility(FakePage(report))
        self.assertIn('/exemplo', stream.getvalue())
        self.assertIn('moderate-issue', stream.getvalue())
        self.assertIn('#navigation', stream.getvalue())
        self.assertIn('minor-issue', stream.getvalue())

    def test_serious_finding_fails_with_page_and_selector(self):
        report = {"violations": [
            {"id": "bad-role", "impact": "serious", "nodes": [{"target": ["#mockup"]}]},
        ]}
        with self.assertRaisesRegex(AssertionError, r'exemplo.*bad-role.*#mockup'):
            check_accessibility(FakePage(report))

    def test_missing_axe_dependency_is_an_explicit_error(self):
        with patch.object(browser_check, 'AXE_SOURCE', Path('/missing-axe-core.js')):
            with self.assertRaisesRegex(RuntimeError, 'npm ci'):
                browser_check.check_site(None, '')


if __name__ == "__main__":
    unittest.main()
