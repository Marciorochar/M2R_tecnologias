"""Internal hero contract, including preservation against the approved baseline."""
import re
import subprocess
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

import pytest

from site_tools import ROOT, Site

BASE = '7436829'
PAGES = sorted((ROOT / 'frontend/pages').rglob('*.html')) + [ROOT / 'frontend/404.html', ROOT / '404.html']
HERO = re.compile(r'<section class="page-hero\b[^>]*>.*?</section>', re.S)
CTAS = {
    'sobre.html': ('/servicos', 'Ver serviços'),
    'servicos.html': ('/contato', 'Converse sobre seu projeto'),
    'contato.html': ('#contato-mensagem', 'Preencher mensagem'),
    'fundador.html': ('/sobre', 'Conhecer a M2R'),
    'projetos.html': ('/projetos/m2r-server', 'Conhecer o M2R Server'),
    'blog.html': ('#artigos', 'Ler os artigos'),
}


def baseline(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path.relative_to(ROOT).as_posix()}'], cwd=ROOT).decode('utf-8')


class Tokens(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tokens = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = [(k, v) for k, v in attrs if not (k == 'id' and v in ('artigos', 'artigo', 'contato-mensagem'))]
        self.tokens.append((tag, sorted(attrs)))

    def handle_endtag(self, tag):
        self.tokens.append(('/' + tag,))

    def handle_data(self, text):
        if text.strip():
            self.tokens.append(('text', text.strip()))


def outside(source):
    source = HERO.sub('', source)
    source = re.sub(r'\s*<link[^>]+internal-hero\.css[^>]*>', '', source)
    source = re.sub(r'\s*<script[^>]+internal-hero\.js[^>]*></script>', '', source)
    return Tokens(source).tokens


@pytest.mark.parametrize('path', PAGES, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_internal_hero_contract_and_copy(path):
    current, original = path.read_text(encoding='utf-8'), baseline(path)
    hero, old_hero = HERO.search(current).group(), HERO.search(original).group()
    assert 'page-hero--circuits' in hero
    assert 'home-hero' not in hero
    assert current.count('internal-hero.css') == current.count('internal-hero.js') == 1
    assert current.index('style.css') < current.index('internal-hero.css')
    assert len(re.findall(r'<h1\b', current)) == 1
    for tag in ('h1', 'p'):
        old_copy = re.findall(fr'<{tag}\b[^>]*>.*?</{tag}>', old_hero, re.S)
        assert all(copy in hero for copy in old_copy)
    for action in re.findall(r'<a\b[^>]*>.*?</a>', old_hero, re.S):
        assert action in hero
    assert re.search(r'<img[^>]+class="internal-hero-art"[^>]+alt=""[^>]+aria-hidden="true"[^>]+width="1200"[^>]+height="610"', hero)
    assert 'data-internal-hero-motion' in hero and 'aria-pressed="false"' in hero and ' hidden' in hero
    assert outside(current) == outside(original), 'DOM outside hero changed beyond permitted assets and anchor IDs'
    if 'hero-actions' not in old_hero:
        href, label = CTAS.get(path.name, ('#artigo', 'Ler o artigo'))
        assert f'href="{href}">{label}</a>' in hero
        if href.startswith('#'):
            assert f'id="{href[1:]}"' in current


@pytest.mark.parametrize('relative', ['frontend/index.html', 'frontend/assets/css/style.css', 'frontend/assets/js/hero-circuits.js', 'frontend/assets/video/m2r-circuitos.webm'])
def test_protected_home_files(relative):
    expected = subprocess.check_output(['git', 'show', f'{BASE}:{relative}'], cwd=ROOT)
    actual = (ROOT / relative).read_bytes()
    if not relative.endswith('.webm'):
        actual = actual.replace(b'\r\n', b'\n')
    assert actual == expected


def test_shared_svg_exact_home_paths_and_decorative_content():
    root = ET.parse(ROOT / 'frontend/assets/img/hero-circuits.svg').getroot()
    paths = root.findall('.//{http://www.w3.org/2000/svg}path')
    home = baseline(ROOT / 'frontend/index.html')
    expected = re.findall(r'<path id="m2r-path-\d+" d="([^"]+)"', home)
    assert len(paths) == len(expected) == 14
    assert [p.attrib['d'] for p in paths] == expected
    assert root.findall('.//{http://www.w3.org/2000/svg}circle')
    assert not root.findall('.//{http://www.w3.org/2000/svg}script')


def test_all_internal_routes_and_404_are_integrated():
    site = Site()
    routes = {site.file(rule['source']) for rule in site.config['rewrites'] if '(.*)' not in rule['source']}
    assert set(PAGES[:-1]) - {ROOT / 'frontend/404.html'} <= routes
    assert (ROOT / '404.html').read_bytes() == (ROOT / 'frontend/404.html').read_bytes()
    site.check()
