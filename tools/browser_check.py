"""Reproducible Playwright smoke test for the local site.

Install: python -m pip install -r requirements-dev.txt && python -m playwright install chromium
Run from repository root: python tools/browser_check.py
"""
import os
import json
import shutil
import threading
from http.server import ThreadingHTTPServer
from site_tools import ROOT, Site, handler_for

AXE_SOURCE = ROOT / 'node_modules' / 'axe-core' / 'axe.min.js'
AXE_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']
EVIDENCE_ROUTES = ('/', '/servicos', '/contato')
RESPONSIVE_WIDTHS = (320, 390, 768, 1024, 1440)
ROUTE_SLUGS = {'/': 'home', '/servicos': 'servicos', '/contato': 'contato'}
PRIMARY_CTA_COLORS = ('rgb(135, 86, 47)', 'rgb(112, 67, 33)', 'rgb(146, 85, 45)')


def responsive_targets():
    """Return the canonical route/width pairs used by responsive evidence."""
    return [(route, width) for route in EVIDENCE_ROUTES for width in RESPONSIVE_WIDTHS]


def responsive_capture_name(route, width):
    """Create a stable, filesystem-safe name for a route viewport capture."""
    slug = ROUTE_SLUGS.get(route)
    return f'{slug}-{width}.png' if slug else None


def boxes_overlap(first, second):
    """Return whether two Playwright bounding boxes overlap by positive area."""
    if not first or not second:
        return False
    return (
        first['x'] < second['x'] + second['width']
        and first['x'] + first['width'] > second['x']
        and first['y'] < second['y'] + second['height']
        and first['y'] + first['height'] > second['y']
    )


def serious_axe_violations(report):
    """Only high-severity axe findings block this incremental quality gate."""
    return [item for item in report['violations'] if item.get('impact') in ('serious', 'critical')]


def check_accessibility(page, evidence_path=None, viewport_width=None):
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
    if evidence_path:
        report['audit'] = {
            'url': page.url,
            'viewportWidth': viewport_width,
            'axeVersion': page.evaluate('window.axe.version'),
            'runOnlyTags': AXE_TAGS,
            'scope': 'WCAG 2.0 and WCAG 2.1 A/AA tags supported by axe-core; not a WCAG 2.2 conformance claim',
        }
        evidence_path.parent.mkdir(parents=True, exist_ok=True)
        evidence_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def chromium_launch_options(playwright):
    """Use Playwright's browser in CI, or system Chromium on local machines."""
    explicit = os.environ.get('CHROME_PATH')
    if explicit:
        return {'executable_path': explicit}
    if not os.path.isfile(playwright.chromium.executable_path) and shutil.which('chromium'):
        return {'executable_path': shutil.which('chromium')}
    return {}


def check_layout(page):
    metrics = page.evaluate("""() => {
        const viewportWidth = window.innerWidth;
        const documentElement = document.documentElement;
        const offenders = [...document.querySelectorAll('body *')].filter(el => {
            if (el.closest('[aria-hidden="true"]')) return false;
            const rect = el.getBoundingClientRect();
            return rect.width > 0 && (rect.right > viewportWidth + 1 || rect.left < -1);
        }).map(el => {
            const rect = el.getBoundingClientRect();
            return {tag: el.tagName.toLowerCase(), id: el.id, className: typeof el.className === 'string' ? el.className : '',
                text: (el.textContent || '').trim().slice(0, 80), left: Math.round(rect.left), right: Math.round(rect.right),
                width: Math.round(rect.width)};
        }).slice(0, 30);
        return {viewportWidth, clientWidth: documentElement.clientWidth, documentScrollWidth: documentElement.scrollWidth,
            bodyScrollWidth: document.body.scrollWidth, offenders};
    }""")
    assert metrics['documentScrollWidth'] <= metrics['viewportWidth'], (page.url, metrics)
    assert page.locator('h1').count() == 1
    # Verifica a identidade visual e a legibilidade do CTA em todas as rotas e larguras.
    for button in page.locator('.btn-primary:visible').all():
        colors = button.evaluate('(el) => { const style = getComputedStyle(el); return [style.backgroundColor, style.color]; }')
        assert colors[0] in PRIMARY_CTA_COLORS and colors[1] == 'rgb(255, 255, 255)', (page.url, colors)
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
    for section_handle in page.locator('.fade-in-section:not([hidden])').element_handles():
        if not section_handle.evaluate('(el) => el.isConnected && !el.hidden'):
            continue
        section_handle.scroll_into_view_if_needed()
        page.wait_for_function('(el) => !el.isConnected || getComputedStyle(el).opacity === "1"', arg=section_handle)
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
    return metrics


def check_first_tab_is_skip_link(page, base):
    page.goto(base + '/')
    page.keyboard.press('Tab')
    assert page.locator('.skip-link').evaluate('(el) => el === document.activeElement'), 'first Tab should focus skip link'


def check_service_fragments(page, base):
    for service_id in ('servico-web', 'servico-automacao', 'servico-dados'):
        page.goto(base + '/')
        link = page.locator(f'.home-service-link[href="/servicos#{service_id}"]')
        link.scroll_into_view_if_needed()
        link.click()
        page.wait_for_function('(id) => location.pathname === "/servicos" && location.hash === `#${id}`', arg=service_id)
        target = page.locator(f'#{service_id}')
        page.wait_for_function('(el) => el === document.activeElement', arg=target.element_handle())
        box = target.bounding_box()
        nav_box = page.locator('.navbar').bounding_box()
        assert box and nav_box and box['y'] >= nav_box['y'] + nav_box['height'], (
            f'{service_id} should be visible below the sticky navigation: {box}, {nav_box}'
        )


def check_fixed_control_overlaps(page, base):
    page.set_viewport_size({'width': 320, 'height': 600})
    page.goto(base + '/')
    wa = page.locator('.mobile-whatsapp-cta')
    hero_cta = page.locator('.home-hero .btn-primary')
    assert not boxes_overlap(wa.bounding_box(), hero_cta.bounding_box()), 'WhatsApp CTA should not cover the home primary CTA'
    page.goto(base + '/servicos#servico-automacao')
    service_card = page.locator('#servico-automacao')
    page.wait_for_function('el => el === document.activeElement', arg=service_card.element_handle())
    page.wait_for_function('(el) => Math.abs(el.getBoundingClientRect().top - 112) <= 2', arg=service_card.element_handle())
    assert not boxes_overlap(wa.bounding_box(), service_card.bounding_box()), 'WhatsApp CTA should not cover the service anchor'
    page.goto(base + '/contato')
    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    contact_action = page.locator('#copy-message')
    assert not boxes_overlap(wa.bounding_box(), contact_action.bounding_box()), 'WhatsApp CTA should not cover contact actions'


def check_hero_motion(page, base):
    page.set_viewport_size({'width': 1440, 'height': 900})
    page.goto(base + '/')
    toggle = page.locator('#m2r-motion-toggle')
    page.wait_for_function("() => { const el = document.querySelector('#m2r-motion-toggle'); return el && !el.hidden; }")
    toggle_box = toggle.bounding_box()
    nav_box = page.locator('.navbar').bounding_box()
    status_box = page.locator('#m2r-circuit-status').bounding_box()
    tip_box = page.locator('#m2r-circuit-tip').bounding_box()
    assert toggle_box and nav_box and toggle_box['y'] >= nav_box['y'] + nav_box['height'], (
        f'motion toggle should remain clickable below the sticky navigation: {toggle_box}, {nav_box}'
    )
    assert status_box and tip_box and status_box['y'] + status_box['height'] <= tip_box['y'] + 1, (
        f'circuit status and helper text should have separate lines: {status_box}, {tip_box}'
    )
    toggle.click()
    page.wait_for_function("() => document.querySelector('#m2r-motion-toggle').getAttribute('aria-pressed') === 'true'")
    paused = page.evaluate("""() => {
        const hero = document.querySelector('#m2r-hero');
        const video = hero.querySelector('.home-hero-motion-video');
        const dot = hero.querySelector('.home-hero-status-dot');
        return {classPaused: hero.classList.contains('motion-paused'), videoPaused: video.paused,
            dotState: getComputedStyle(dot).animationPlayState, pulses: document.querySelector('#m2r-pulse-render').innerHTML};
    }""")
    assert paused['classPaused'] and paused['videoPaused'] and paused['dotState'] == 'paused', paused
    page.wait_for_timeout(200)
    assert page.locator('#m2r-pulse-render').inner_html() == paused['pulses'], 'SVG circuit pulses should remain still while paused'
    toggle.click()
    page.wait_for_function("() => document.querySelector('#m2r-motion-toggle').getAttribute('aria-pressed') === 'false'")
    resumed = page.evaluate("""() => ({
        classPaused: document.querySelector('#m2r-hero').classList.contains('motion-paused'),
        videoPaused: document.querySelector('.home-hero-motion-video').paused,
        dotState: getComputedStyle(document.querySelector('.home-hero-status-dot')).animationPlayState
    })""")
    assert not resumed['classPaused'] and not resumed['videoPaused'] and resumed['dotState'] == 'running', resumed
    page.wait_for_timeout(200)
    assert page.locator('#m2r-pulse-render').inner_html() != paused['pulses'], 'SVG circuit pulses should resume'

    # The Hero controller also pauses when its tab is hidden or it leaves the viewport.
    # Exercise both lifecycle transitions and verify every visible motion state agrees.
    page.evaluate("Object.defineProperty(document, 'visibilityState', { configurable: true, value: 'hidden' }); Object.defineProperty(document, 'hidden', { configurable: true, value: true }); document.dispatchEvent(new Event('visibilitychange'))")
    page.wait_for_function("() => document.querySelector('#m2r-hero').classList.contains('motion-paused')")
    hidden = page.evaluate("""() => ({
        videoPaused: document.querySelector('.home-hero-motion-video').paused,
        dotState: getComputedStyle(document.querySelector('.home-hero-status-dot')).animationPlayState,
        pulses: document.querySelector('#m2r-pulse-render').innerHTML
    })""")
    assert hidden['videoPaused'] and hidden['dotState'] == 'paused', hidden
    page.evaluate("Object.defineProperty(document, 'visibilityState', { configurable: true, value: 'visible' }); Object.defineProperty(document, 'hidden', { configurable: true, value: false }); document.dispatchEvent(new Event('visibilitychange'))")
    page.wait_for_function("() => !document.querySelector('#m2r-hero').classList.contains('motion-paused')")
    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    page.wait_for_function("() => document.querySelector('#m2r-hero').classList.contains('motion-paused')")
    offscreen = page.evaluate("""() => ({
        videoPaused: document.querySelector('.home-hero-motion-video').paused,
        dotState: getComputedStyle(document.querySelector('.home-hero-status-dot')).animationPlayState,
        pulses: document.querySelector('#m2r-pulse-render').innerHTML
    })""")
    assert offscreen['videoPaused'] and offscreen['dotState'] == 'paused', offscreen
    page.evaluate('window.scrollTo(0, 0)')
    page.wait_for_function("() => !document.querySelector('#m2r-hero').classList.contains('motion-paused')")
    returned = page.evaluate("""() => ({
        videoPaused: document.querySelector('.home-hero-motion-video').paused,
        dotState: getComputedStyle(document.querySelector('.home-hero-status-dot')).animationPlayState
    })""")
    assert not returned['videoPaused'] and returned['dotState'] == 'running', returned
    page.wait_for_timeout(200)
    assert page.locator('#m2r-pulse-render').inner_html() != offscreen['pulses'], 'SVG circuit pulses should resume after returning to the Hero'


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
    evidence_dir = ROOT / 'docs' / 'auditoria' / 'evidencias' / 'responsivo'
    evidence_dir.mkdir(parents=True, exist_ok=True)
    axe_dir = ROOT / 'docs' / 'auditoria' / 'evidencias' / 'axe'
    axe_dir.mkdir(parents=True, exist_ok=True)
    manifest = {'routes': list(EVIDENCE_ROUTES), 'widths': list(RESPONSIVE_WIDTHS), 'captures': []}
    for width in RESPONSIVE_WIDTHS:
        page.set_viewport_size({'width': width, 'height': 900})
        for route in routes:
            response = page.goto(base + route)
            assert response.status == 200
            check_menu(page, width <= 768)
            layout = check_layout(page)
            if width in (390, 1024):
                check_accessibility(page, axe_dir / f'{ROUTE_SLUGS.get(route, route.strip("/").replace("/", "-"))}-{width}.json', width)
            if route in EVIDENCE_ROUTES:
                page.evaluate('window.scrollTo({top: 0, behavior: "instant"})')
                name = responsive_capture_name(route, width)
                screenshot = evidence_dir / name
                page.screenshot(path=str(screenshot), full_page=False)
                manifest['captures'].append({**layout, 'route': route, 'width': width,
                    'screenshot': screenshot.relative_to(ROOT).as_posix()})
                (evidence_dir / 'manifest.json').write_text(
                    json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
                )
            if route in ('/sobre', '/fundador'):
                page.evaluate('document.activeElement.blur(); window.scrollTo({top: 0, behavior: "instant"})')
                page.screenshot(path=str(results / f'{route[1:]}-{width}.png'), full_page=True)
        print(f'PASS Chromium: {len(routes)} routes at {width}px', flush=True)
    page.set_viewport_size({'width': 390, 'height': 844})
    check_first_tab_is_skip_link(page, base)
    check_service_fragments(page, base)
    check_fixed_control_overlaps(page, base)
    check_hero_motion(page, base)
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
        assert fp.locator('.contact-email-disclosure').is_visible()
        assert fp.locator('.contact-direct a').count() == 3
        if disabled:
            fp.goto(base + '/')
            fallback_motion = fp.evaluate("""() => ({
                animation: getComputedStyle(document.querySelector('.home-hero-status-dot')).animationName,
                toggleHidden: document.querySelector('#m2r-motion-toggle').hidden
            })""")
            assert fallback_motion['animation'] == 'none' and fallback_motion['toggleHidden'], fallback_motion
        if not disabled:
            fp.goto(base + '/')
            motion_state = fp.evaluate("""() => ({
                status: document.querySelector('#m2r-circuit-status-text').textContent,
                toggleHidden: document.querySelector('#m2r-motion-toggle').hidden,
                animation: getComputedStyle(document.querySelector('.home-hero-status-dot')).animationName,
                videoPaused: document.querySelector('.home-hero-motion-video').paused
            })""")
            assert motion_state['status'] == 'Circuitos em repouso' and motion_state['toggleHidden']
            assert motion_state['animation'] == 'none' and motion_state['videoPaused'], motion_state
        fallback.close()
    no_preference = browser.new_context(java_script_enabled=False, reduced_motion='no-preference', viewport={'width': 390, 'height': 844})
    no_preference_page = no_preference.new_page()
    no_preference_page.goto(base + '/')
    no_js_motion = no_preference_page.evaluate("""() => ({
        animation: getComputedStyle(document.querySelector('.home-hero-status-dot')).animationName,
        toggleHidden: document.querySelector('#m2r-motion-toggle').hidden
    })""")
    assert no_js_motion['animation'] == 'none' and no_js_motion['toggleHidden'], no_js_motion
    no_preference.close()
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
    assert page.locator('#fundador').evaluate('el => getComputedStyle(el).backgroundColor') == 'rgb(59, 38, 27)'
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
