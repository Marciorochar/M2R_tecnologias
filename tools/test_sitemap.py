import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from site_tools import ROOT


class SitemapTests(unittest.TestCase):
    def test_unrelated_commit_does_not_change_dates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "frontend", root / "frontend")
            (root / "tools").mkdir()
            for name in ("generate-sitemap.js", "sitemap-dates.json"):
                shutil.copy(ROOT / "tools" / name, root / "tools" / name)
            shutil.copy(ROOT / "vercel.json", root / "vercel.json")
            env = {**os.environ, "GIT_AUTHOR_NAME": "Test", "GIT_COMMITTER_NAME": "Test",
                   "GIT_AUTHOR_EMAIL": "test@example.com", "GIT_COMMITTER_EMAIL": "test@example.com",
                   "GIT_AUTHOR_DATE": "2026-09-06T12:00:00Z", "GIT_COMMITTER_DATE": "2026-09-06T12:00:00Z"}
            def run(*args):
                subprocess.run(args, cwd=root, env=env, check=True, capture_output=True)
            run("git", "init")
            run("git", "add", ".")
            run("git", "-c", "commit.gpgsign=false", "commit", "-m", "Initial fixture")
            run("node", "tools/generate-sitemap.js")
            before = (root / "frontend/sitemap.xml").read_bytes()
            (root / "unrelated.txt").write_text("Unrelated change", encoding="utf-8")
            env.update(GIT_AUTHOR_DATE="2026-10-01T12:00:00Z", GIT_COMMITTER_DATE="2026-10-01T12:00:00Z")
            run("git", "add", "unrelated.txt")
            run("git", "-c", "commit.gpgsign=false", "commit", "-m", "Unrelated fixture")
            run("node", "tools/generate-sitemap.js", "--check")
            run("node", "tools/generate-sitemap.js")
            self.assertEqual(before, (root / "frontend/sitemap.xml").read_bytes())
            self.assertEqual(before.count(b"<loc>"), 10)
            self.assertNotIn(b"/404</loc>", before)
