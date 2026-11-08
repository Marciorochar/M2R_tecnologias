"""Reproducible Playwright smoke test for the local site.

Install: python -m pip install -r requirements-dev.txt && python -m playwright install chromium
Run from repository root: python tools/browser_check.py
"""
import os
import shutil
import threading
from http.server import ThreadingHTTPServer
from site_tools import ROOT, Site, handler_for

AXE_SOURCE = ROOT / 'node_modules' / 'axe-core' / 'axe.min.js'
AXE_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']


def serious_axe_violations(report):
    """Only high-severity axe findings block this incremental quality gate."""
    return [item for item in report['violations'] if item.get('impact') in ('serious', 'critical')]


def check_accessibility(page):
    """Audit the rendered DOM without changing the site's production CSP."""
    report = page.evaluate("""async tags => {
        if (!window.axe) throw new Error('axe-core nao foi carregado');
        return await window.axe.run(document, {
            runOnly: {type: 'tag', values: tags},
            resultTypes: ['violations'],
        });
    }""", AXE_TAGS)
    def describe(finding):
        return f"{finding['impact']} / {finding['id']}: " + ', '.join(
            ' '.join(node.get('target', [])) for node in finding.get('nodes', [])[:5]
        )

    serious = serious_axe_violations(report)
    informative = [item for item in report['violations'] if item.get('impact') in ('moderate', 'minor')]
    if informative:
        print(
            f'INFO axe em {page.url}: {len(informative)} achado(s) nao bloqueante(s): '
            + '; '.join(describe(item) for item in informative),
            flush=True,
        )
    if serious:
        raise AssertionError(f'Falha axe em {page.url}: ' + '; '.join(describe(item) for item in serious))


def chromium_launch_options(playwright):
    """Use Playwright's browser in CI, or system Chromium on local machines."""
    explicit = os.environ.get('CHROME_PATH')
    if explicit:
        return {'executable_path': explicit}
    if not os.path.isfile(playwright.chromium.executable_path) and shutil.which('chromium'):
        return {'executable_path': shutil.which('chromium')}
    return {}


def check_layout(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (page.url, page.evaluate("() => [...document.querySelectorAll('body *')].filter(el => el.getBoundingClientRect().right > innerWidth + 1).map(el => ({tag: el.tagName, class: el.className, text: el.textContent.slice(0, 80), width: el.getBoundingClientRect().width}))"))
    assert page.locator('h1').count() == 1
    assert page.locator('.breadcrumbs').count() == 0, f'Trilha de navegação ainda visível: {page.url}'
    # Verifica a identidade visual e a legibilidade do CTA em todas as rotas e larguras.
    for button in page.locator('.btn-primary:visible').all():
        colors = button.evaluate('(el) => { const style = getComputedStyle(el); return [style.backgroundColor, style.color]; }')
        assert colors[0] in ('rgb(199, 122, 59)', 'rgb(225, 162, 111)') and colors[1] == 'rgb(30, 23, 17)', (page.url, colors)
    if page.viewport_size['width'] <= 900 and page.locator('body.home-page').count():
        hero = page.locator('.home-hero .hero-layout').bounding_box()
        copy = page.locator('.home-hero-copy').bounding_box()
        assert hero and copy and copy['width'] >= hero['width'] * 0.7, (
            f'Hero comprimido em {page.viewport_size["width"]} px: '
            f'texto={copy["width"] if copy else "invisível"}, '
            f'grade={hero["width"] if hero else "invisível"}'
        )
    for image in page.locator('img').all():
        image.scroll_into_view_if_needed()
        page.wait_for_function('(el) => el.complete && el.naturalWidth > 0', arg=image.element_handle())
        assert image.get_attribute('width') and image.get_attribute('height')
    for section in page.locator('.fade-in-section:not([hidden])').all():
        section.scroll_into_view_if_needed()
        page.wait_for_function('(el) => getComputedStyle(el).opacity === "1"', arg=section.element_handle())
    form = page.locator('#contact-form')
    if form.count():
        assert form.get_attribute('aria-describedby') == 'form-intro'
        assert page.locator('#form-status').get_attribute('role') == 'status'
        for label in form.locator('label').all():
            assert label.get_attribute('for')
            assert form.locator(f'#{label.get_attribute("for")}').count() == 1
    founder_picture = page.locator('#fundador .founder-photo picture')
    if founder_picture.count():
        box = founder_picture.bounding_box()
        assert box and box['height'] > box['width']


def check_menu(page, mobile):
    button, links = page.locator('.mobile-menu-btn'), page.locator('#menu-principal')
    assert button.count() == 1 and links.count() == 1, page.url
    assert button.get_attribute('aria-controls') == 'menu-principal'
    assert button.get_attribute('aria-expanded') == 'false'
    if not mobile:
        assert not button.is_visible() and links.is_visible()
        return
    assert button.is_visible() and not links.is_visible()
    button.focus()
    page.keyboard.press('Enter')
    assert links.is_visible() and button.get_attribute('aria-expanded') == 'true'
    assert button.get_attribute('aria-label') == 'Fechar menu'
    assert button.text_content() == '✕'
    page.keyboard.press('Tab')
    assert links.locator('a').first.evaluate('(el) => el === document.activeElement')
    page.keyboard.press('Escape')
    assert button.evaluate('(el) => el === document.activeElement')
    assert not links.is_visible() and button.get_attribute('aria-expanded') == 'false'
    assert button.get_attribute('aria-label') == 'Abrir menu'
    assert button.text_content() == '☰'
    button.click()
    links.locator('a').first.evaluate("el => el.addEventListener('click', e => e.preventDefault(), {once: true})")
    links.locator('a').first.click()
    assert button.get_attribute('aria-expanded') == 'false' and not links.is_visible()
    button.click()
    width = page.viewport_size['width']
    page.set_viewport_size({'width': 1024, 'height': 900})
    page.wait_for_function("() => document.querySelector('.mobile-menu-btn').getAttribute('aria-expanded') === 'false'")
    assert links.is_visible() and button.get_attribute('aria-expanded') == 'false'
    page.set_viewport_size({'width': width, 'height': 900})
    page.wait_for_function("() => getComputedStyle(document.querySelector('#menu-principal')).display === 'none'")
    assert not links.is_visible()


def check_site(browser, base):
    if not AXE_SOURCE.is_file():
        raise RuntimeError('axe-core ausente. Execute npm ci --ignore-scripts antes dos testes.')
    site = Site()
    routes = [r['source'] for r in site.config['rewrites'] if r['destination'].endswith('.html')]
    context = browser.new_context()
    context.add_init_script(path=str(AXE_SOURCE))
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    results = ROOT / 'test-results'
    results.mkdir(exist_ok=True)
    # Produz evidencias mesmo quando um teste posterior falhar.
    preview = results / 'site-previews'
    preview.mkdir(exist_ok=True)
    page.set_viewport_size({'width': 1365, 'height': 768})
    for name, route in (('home', '/'), ('projetos', '/projetos'), ('blog', '/blog')):
        page.goto(base + route)
        page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        page.screenshot(path=str(preview / f'{name}.png'), full_page=False)
    for width in (320, 390, 640, 768, 1024, 1440):
        page.set_viewport_size({'width': width, 'height': 900})
        for route in routes:
            response = page.goto(base + route)
            assert response.status == 200
            check_menu(page, width <= 768)
            check_layout(page)
            if width in (390, 1024):
                check_accessibility(page)
            if route in ('/sobre', '/fundador'):
                page.evaluate('document.activeElement.blur(); window.scrollTo({top: 0, behavior: "instant"})')
                page.screenshot(path=str(results / f'{route[1:]}-{width}.png'), full_page=True)
        print(f'PASS Chromium: {len(routes)} routes at {width}px', flush=True)
    for disabled in (True, False):
        fallback = browser.new_context(java_script_enabled=not disabled, reduced_motion='reduce', viewport={'width': 390, 'height': 844})
        fp = fallback.new_page()
        for route in routes:
            fp.goto(base + route)
            check_layout(fp)
            if disabled:
                assert fp.locator('#menu-principal').is_visible()
                assert not fp.locator('.mobile-menu-btn').is_visible()
                assert fp.evaluate("document.querySelector('main').getBoundingClientRect().top >= document.querySelector('.navbar').getBoundingClientRect().bottom")
        fp.goto(base + '/contato')
        assert fp.locator('#contact-form').is_visible() == (not disabled)
        fallback.close()
    for setup in (
        'delete window.IntersectionObserver',
        "window.IntersectionObserver = class { constructor() { throw Error('test'); } }",
        'window.IntersectionObserver = class { observe() {} disconnect() {} }',
    ):
        fallback = browser.new_context()
        fallback.add_init_script(setup)
        fp = fallback.new_page()
        fp.goto(base + '/sobre')
        fp.wait_for_function("() => !document.documentElement.classList.contains('reveal-animations-enabled')", timeout=8000)
        check_layout(fp)
        fallback.close()
    page.goto(base + '/sobre')
    page.emulate_media(reduced_motion='reduce')
    check_layout(page)
    assert page.locator('#fundador').evaluate('el => getComputedStyle(el).backgroundColor') == 'rgb(18, 60, 73)'
    for redirect in site.config.get('redirects', []):
        response = context.request.get(base + redirect['source'], max_redirects=0)
        assert response.status in (307, 308)
        assert response.headers['location'] == redirect['destination']
    assert page.goto(base + '/missing/nested/path').status == 404
    assert page.locator('h1').is_visible()
    assert not errors, errors
    context.close()
    print('PASS Chromium: no JS, reduced motion, observer fallbacks, redirects and 404', flush=True)

def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("Playwright ausente. Instale requirements-dev.txt e execute: python -m playwright install chromium")
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(Site()))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(**chromium_launch_options(p))
            check_site(browser, base)
            page = browser.new_page()
            page.goto(base + "/contato"); assert page.locator("#contact-form").is_visible()
            page.locator("#name").fill("Teste"); page.locator("#email").fill("invalido"); page.locator("#message").fill("Mensagem")
            assert not page.locator("#email").evaluate("e => e.checkValidity()")
            page.locator("#email").fill("teste@example.com")
            # Keep the mailto navigation inside the test browser; no email is sent.
            page.route('mailto:**', lambda route: route.abort())
            page.locator("#prepare-email").click()
            assert page.locator("#name").input_value() == "Teste"
            page.set_viewport_size({"width": 390, "height": 844}); page.goto(base + "/")
            menu = page.locator(".mobile-menu-btn")
            assert menu.count() == 1
            menu.click(); assert menu.get_attribute("aria-expanded") == "true"; page.keyboard.press("Escape"); assert menu.get_attribute("aria-expanded") == "false"
            browser.close()
        with sync_playwright() as p:
            browser = p.chromium.launch(**chromium_launch_options(p)); page = browser.new_page(java_script_enabled=False); page.goto(base + "/contato"); assert not page.locator("#contact-form").is_visible(); browser.close()
    finally:
        server.shutdown(); server.server_close(); thread.join()
if __name__ == "__main__": main()
