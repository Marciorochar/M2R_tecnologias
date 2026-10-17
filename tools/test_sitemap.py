import os
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from site_tools import ROOT


class RobotsParser(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.noindex = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta' and attrs.get('name', '').lower() == 'robots':
            self.noindex |= 'noindex' in attrs.get('content', '').lower().replace(',', ' ').split()


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
            config = json.loads((root / 'vercel.json').read_text(encoding='utf-8'))
            expected = set()
            for rule in config['rewrites']:
                if rule['source'] == '/404' or not rule['destination'].endswith('.html'):
                    continue
                html = (root / rule['destination'].lstrip('/')).read_text(encoding='utf-8')
                if not RobotsParser(html).noindex:
                    expected.add('https://m2rtecnologias.vercel.app' + rule['source'])
            actual = {item.text for item in ET.fromstring(before).findall('{*}url/{*}loc')}
            self.assertEqual(actual, expected)
            self.assertNotIn(b"/404</loc>", before)
            founder = root / 'frontend/pages/fundador.html'
            html = founder.read_text(encoding='utf-8')
            founder.write_text(html.replace('noindex, follow', 'index, follow'), encoding='utf-8')
            run('node', 'tools/generate-sitemap.js')
            with_founder = (root / 'frontend/sitemap.xml').read_text(encoding='utf-8')
            self.assertIn('https://m2rtecnologias.vercel.app/fundador</loc>', with_founder)
            founder.write_text(html, encoding='utf-8')
            run('node', 'tools/generate-sitemap.js')
            self.assertEqual(before, (root / 'frontend/sitemap.xml').read_bytes())
