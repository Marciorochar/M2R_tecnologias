"""Shared hero contract and route-content preservation checks."""
import html
import re
import subprocess
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

import pytest

from site_tools import ROOT, Site

BASE = '4c41e22'
PAGES = sorted((ROOT / 'frontend/pages').rglob('*.html')) + [ROOT / 'frontend/404.html', ROOT / '404.html']
HERO_PAGES = [ROOT / 'frontend/index.html', *PAGES]
HERO_OPEN = re.compile(r'<section\b(?=[^>]*\bclass="[^"]*(?:page-hero|home-hero))[^>]*>', re.S)


def baseline(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT).decode('utf-8')


class Tokens(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tokens = []
        self.hero_depth = 0
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ('href', 'src'):
            if attrs.get(name):
                attrs[name] = re.sub(r'\?v=[A-Za-z0-9._-]+$', '?v=<content-hash>', attrs[name])
        if self.hero_depth:
            if tag == 'section':
                self.hero_depth += 1
            return
        if tag == 'section' and {'page-hero', 'home-hero'} & set((attrs.get('class') or '').split()):
            self.hero_depth = 1
            return
        attrs = [(k, v) for k, v in attrs.items() if not (k == 'id' and v in ('artigos', 'artigo', 'contato-mensagem'))]
        self.tokens.append((tag, sorted(attrs)))

    def handle_endtag(self, tag):
        if self.hero_depth:
            if tag == 'section':
                self.hero_depth -= 1
            return
        self.tokens.append(('/' + tag,))

    def handle_data(self, text):
        if not self.hero_depth and text.strip():
            self.tokens.append(('text', text.strip()))


def outside(source):
    source = re.sub(r'\s*<nav\b[^>]*class="breadcrumbs"[^>]*>.*?</nav>', '', source, flags=re.S)
    source = re.sub(r'\s*<link\b(?=[^>]*(?:hero-system|internal-hero)\.css)[^>]*>', '', source)
    source = re.sub(r'\s*<script\b(?=[^>]*src="[^"]*(?:hero-system|internal-hero|hero-circuits)\.js)[^>]*>.*?</script>', '', source, flags=re.S)
    return Tokens(source).tokens


def hero_content(source):
    opening = HERO_OPEN.search(source)
    assert opening, 'Hero section missing'
    end = source.find('</section>', opening.end())
    section = source[opening.start():end + len('</section>')]
    values = {}
    for tag in ('h1', 'p'):
        values[tag] = [html.unescape(re.sub(r'<[^>]+>', '', item)).strip()
                       for item in re.findall(fr'<{tag}\b[^>]*>(.*?)</{tag}>', section, re.S)]
    values['links'] = [
        (href, html.unescape(re.sub(r'<[^>]+>', '', label)).strip())
        for href, label in re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', section, re.S)
    ]
    return values


def test_all_hero_routes_use_shared_system_contract():
    for path in HERO_PAGES:
        source = path.read_text(encoding='utf-8')
        opening = HERO_OPEN.search(source)
        assert opening, path
        section = source[opening.start():source.find('</section>', opening.end()) + len('</section>')]
        assert 'hero-system' in opening.group(), path
        assert 'data-hero-system' in opening.group(), path
        assert 'hero-system.css' in source and source.count('hero-system.css') == 1, path
        assert 'hero-system.js' in source and source.count('hero-system.js') == 1, path
        assert re.search(r'<img\b(?=[^>]*class="[^"]*hero-system__art")(?=[^>]*src="/assets/img/hero-circuits\.svg")', source), path
        assert re.search(r'<button\b(?=[^>]*data-hero-motion)(?=[^>]*aria-pressed="false")(?=[^>]*\bhidden(?:[ >]))', source), path
        assert 'internal-hero.js' not in source, path
        is_home = path == ROOT / 'frontend/index.html'
        assert ('hero-circuits.js' in source) is is_home, path


@pytest.mark.parametrize('path', PAGES, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_internal_variants_keep_their_original_content(path):
    current, original = path.read_text(encoding='utf-8'), baseline(path)
    assert outside(current) == outside(original), f'DOM outside Hero changed: {path}'
    current_hero, old_hero = hero_content(current), hero_content(original)
    for tag in ('h1', 'p', 'links'):
        for item in old_hero[tag]:
            assert item in current_hero[tag], (path, tag, item)
    if path == ROOT / '404.html':
        assert (ROOT / '404.html').read_bytes() == (ROOT / 'frontend/404.html').read_bytes()


def test_home_video_is_preserved():
    relative = 'frontend/assets/video/m2r-circuitos.webm'
    assert (ROOT / relative).read_bytes() == subprocess.check_output(['git', 'show', f'{BASE}:{relative}'], cwd=ROOT)


def test_shared_svg_is_the_single_circuit_source_and_fallback():
    root = ET.parse(ROOT / 'frontend/assets/img/hero-circuits.svg').getroot()
    paths = root.findall('.//{http://www.w3.org/2000/svg}path')
    assert len(paths) == 14
    assert root.findall('.//{http://www.w3.org/2000/svg}circle')
    assert not root.findall('.//{http://www.w3.org/2000/svg}script')
    for path in HERO_PAGES:
        source = path.read_text(encoding='utf-8')
        assert '/assets/img/hero-circuits.svg' in source, path
    home = (ROOT / 'frontend/index.html').read_text(encoding='utf-8')
    assert not re.search(r'<path\b[^>]*\bid="m2r-path-\d+"', home)


def test_all_internal_routes_and_404_are_integrated():
    site = Site()
    routes = {site.file(rule['source']) for rule in site.config['rewrites'] if '(.*)' not in rule['source']}
    assert set(PAGES[:-1]) - {ROOT / 'frontend/404.html'} <= routes
    assert (ROOT / '404.html').read_bytes() == (ROOT / 'frontend/404.html').read_bytes()
    site.check()
