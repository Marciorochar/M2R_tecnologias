"""Responsive hero evidence and progressive-enhancement behavior checks.

Run: python tools/hero_check.py --output-dir docs/hero-standardization/evidence
Optional: --axe-source /existing/node_modules/axe-core/axe.min.js (or AXE_SOURCE).
Inventories production HTML rewrites, includes Home, and serves the same Site router.
"""
import argparse
import json
import os
import re
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

from browser_check import chromium_launch_options, boxes_overlap, serious_axe_violations
from site_tools import ROOT, Site, handler_for

WIDTHS = (320, 390, 768, 1024, 1440, 1920)


def html_routes(site):
    return sorted({rule['source'] for rule in site.config['rewrites']
                   if '(.*)' not in rule['source'] and site.file(rule['source'])
                   and site.file(rule['source']).suffix == '.html'})


def slug(route):
    return route.strip('/').replace('/', '--') or 'home'


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def contrast_ratio(first, second):
    def luminance(color):
        components = [int(value) / 255 for value in re.findall(r'\d+', color)[:3]]
        linear = [value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4 for value in components]
        return sum(value * weight for value, weight in zip(linear, (.2126, .7152, .0722)))
    bright, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (bright + .05) / (dark + .05)


def assert_static_usable(page, route, image_expected=True):
    hero = page.locator('.page-hero--circuits')
    assert hero.locator('h1').is_visible(), route
    assert hero.locator('.hero-actions .btn-primary').is_visible(), route
    assert hero.evaluate("el => getComputedStyle(el).backgroundImage.includes('radial-gradient')"), route
    assert not hero.locator('[data-internal-hero-motion]').is_visible(), route
    if image_expected:
        assert hero.locator('img.internal-hero-art').evaluate('el => el.complete && el.naturalWidth > 0'), route


def layout_metrics(page, route):
    metrics = page.evaluate("""() => {
        const box = el => {const r=el.getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom};};
        const hero=document.querySelector('.page-hero');
        return {viewport:innerWidth,clientWidth:document.documentElement.clientWidth,
            scrollWidth:document.documentElement.scrollWidth,h1Count:document.querySelectorAll('h1').length,
            hero:box(hero),title:box(hero.querySelector('h1')),navbar:box(document.querySelector('.navbar')),
            cta:box(hero.querySelector('.btn-primary')),art:hero.querySelector('.internal-hero-art') ? box(hero.querySelector('.internal-hero-art')) : null,
            traceCount:hero.querySelectorAll('.internal-hero-live path').length,
            positiveTraces:[...hero.querySelectorAll('.internal-hero-live path')].filter(p=>p.getTotalLength()>0 && p.getBoundingClientRect().width>0).length,
            controls:[...hero.querySelectorAll('a.btn,button:not([hidden])')].map(box),
            panel:hero.querySelector('.project-detail-terminal,.error-page-panel') ? box(hero.querySelector('.project-detail-terminal,.error-page-panel')) : null};
    }""")
    assert metrics['h1Count'] == 1 and metrics['scrollWidth'] <= metrics['viewport'], (route, metrics)
    for name in ('title', 'cta'):
        item, hero = metrics[name], metrics['hero']
        assert item['width'] > 0 and item['height'] > 0, (route, name, metrics)
        assert item['x'] >= hero['x'] - 1 and item['right'] <= hero['right'] + 1, (route, name, metrics)
        assert item['y'] >= metrics['navbar']['bottom'] - 1 and item['bottom'] <= hero['bottom'] + 1, (route, name, metrics)
    if metrics['art']:
        assert metrics['art']['width'] > 0 and metrics['art']['height'] > 0, (route, metrics)
        assert metrics['traceCount'] == metrics['positiveTraces'] == 14, (route, metrics)
        for i, first in enumerate(metrics['controls']):
            for second in metrics['controls'][i + 1:]:
                assert not boxes_overlap(first, second), (route, 'controls collide', metrics)
        if metrics['panel']:
            assert not boxes_overlap(metrics['title'], metrics['panel']), (route, 'panel/title collision', metrics)
            assert not boxes_overlap(metrics['cta'], metrics['panel']), (route, 'panel/CTA collision', metrics)
    return metrics


def behavior_checks(page, base, route):
    page.goto(base + route)
    hero = page.locator('.page-hero--circuits')
    control = hero.locator('[data-internal-hero-motion]')
    control.wait_for(state='visible')
    assert control.get_attribute('aria-label') and control.get_attribute('aria-pressed') == 'false'
    assert not hero.evaluate("el => el.classList.contains('internal-hero-paused')")
    control.focus()
    page.keyboard.press('Enter')
    assert control.get_attribute('aria-pressed') == 'true'
    states = hero.locator('.internal-hero-pulse').evaluate_all("els => els.map(el => getComputedStyle(el).animationPlayState)")
    assert states == ['paused'] * 14
    control.click()
    assert control.get_attribute('aria-pressed') == 'false'
    assert hero.locator('.internal-hero-pulse').first.evaluate("el => getComputedStyle(el).animationPlayState") == 'running'
    page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true}); document.dispatchEvent(new Event('visibilitychange'))")
    assert hero.evaluate("el => el.classList.contains('internal-hero-paused')")
    assert control.get_attribute('aria-pressed') == 'false'
    page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:false}); document.dispatchEvent(new Event('visibilitychange'))")
    assert not hero.evaluate("el => el.classList.contains('internal-hero-paused')")
    can_scroll = page.evaluate("document.documentElement.scrollHeight - innerHeight > document.querySelector('.page-hero--circuits').getBoundingClientRect().bottom")
    if can_scroll:
        page.evaluate("window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
    else:
        # Short 404 pages cannot scroll their whole hero out of view.
        hero.evaluate("el => {el.style.transform='translateY(-300vh)'}")
    page.wait_for_function("() => document.querySelector('.page-hero--circuits').classList.contains('internal-hero-paused')")
    assert control.get_attribute('aria-pressed') == 'false'
    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    hero.evaluate("el => {el.style.transform=''}")
    page.wait_for_function("() => !document.querySelector('.page-hero--circuits').classList.contains('internal-hero-paused')")
    control.click()
    page.emulate_media(reduced_motion='reduce')
    assert_static_usable(page, route)
    page.keyboard.press('Tab')
    assert not control.evaluate('el => el === document.activeElement'), route
    page.emulate_media(reduced_motion='no-preference')
    assert control.get_attribute('aria-pressed') == 'true', 'manual choice survives reduced-motion changes'
    control.click()
    # Repeated execution is safe and does not duplicate controllers or SVGs.
    page.add_script_tag(url=base + '/assets/js/internal-hero.js')
    assert hero.locator('.internal-hero-live').count() == 1
    return {'route': route, 'toggleKeyboard': True, 'hiddenTab': True, 'intersection': True,
            'reducedMotionChange': True, 'manualPreferencePreserved': True, 'idempotent': True}


def run(output, axe_source, screenshots=True):
    from playwright.sync_api import sync_playwright
    output.mkdir(parents=True, exist_ok=True)
    site = Site()
    routes = html_routes(site)
    class EvidenceHandler(handler_for(site)):
        def log_message(self, *_):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), EvidenceHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}'
    results, behavior, errors = [], [], []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(**chromium_launch_options(playwright))
            context = browser.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='no-preference')
            # Test-only initialization, preserving the production CSP unchanged.
            context.add_init_script(path=str(axe_source))
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            for route in routes:
                for width in WIDTHS:
                    page.set_viewport_size({'width': width, 'height': 900})
                    page.goto(base + route)
                    page.evaluate('document.fonts.ready')
                    if route == '/':
                        page.emulate_media(reduced_motion='reduce')
                    else:
                        control = page.locator('[data-internal-hero-motion]')
                        control.wait_for(state='visible')
                        control.click()
                    # Long mobile heroes place the motion control below the
                    # fold; clicking it scrolls. Capture the original top view.
                    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
                    metrics = layout_metrics(page, route)
                    name = f'{slug(route)}-{width}'
                    metrics.update(route=route, width=width, artifactState='reduced-motion' if route == '/' else 'manually-paused')
                    results.append(metrics)
                    if screenshots:
                        page.screenshot(path=str(output / f'{name}.png'), animations='disabled')
                    page.emulate_media(reduced_motion='no-preference')
                # Axe once per route at mobile and desktop, preserving full findings.
                for width in (390, 1440):
                    page.set_viewport_size({'width': width, 'height': 900})
                    # Audit a settled state so existing reveal transitions do not
                    # produce transient opacity/contrast failures outside the hero.
                    page.emulate_media(reduced_motion='reduce')
                    page.goto(base + route)
                    audit = page.evaluate("""async () => {
                        const supported = new Set(axe.getRules().flatMap(rule => rule.tags));
                        const tags=['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22a','wcag22aa'].filter(tag=>supported.has(tag));
                        const result=await axe.run(document,{runOnly:{type:'tag',values:tags},resultTypes:['violations']});
                        const inHero = node => node.target.some(selector => typeof selector === 'string' && document.querySelector(selector)?.closest('.page-hero'));
                        const scoped = inside => result.violations.map(finding => ({...finding,nodes:finding.nodes.filter(node=>Boolean(inHero(node))===inside)})).filter(finding=>finding.nodes.length);
                        return {violations:result.violations,heroViolations:scoped(true),outsideHeroViolations:scoped(false),
                            axeVersion:axe.version,tags,scope:'Full document A/AA report; changed hero nodes gate this task. Outside-hero findings are retained, not certified or silently waived.'};
                    }""")
                    save(output / f'axe-{slug(route)}-{width}.json', audit)
                    assert not serious_axe_violations({'violations': audit['heroViolations']}), (route, width, audit['heroViolations'])
                    if audit['outsideHeroViolations']:
                        print(f"INFO axe outside hero {route} at {width}: " + ', '.join(item['id'] for item in audit['outsideHeroViolations']), flush=True)
                page.emulate_media(reduced_motion='no-preference')
                if route != '/':
                    result = behavior_checks(page, base, route)
                    primary = page.locator('.page-hero--circuits .btn-primary')
                    primary.hover()
                    page.wait_for_function("el => getComputedStyle(el).backgroundColor === 'rgb(112, 67, 33)'", arg=primary.element_handle())
                    colors = primary.evaluate('el => [getComputedStyle(el).backgroundColor,getComputedStyle(el).color]')
                    result['primaryHoverContrast'] = contrast_ratio(*colors)
                    assert result['primaryHoverContrast'] >= 4.5, (route, colors, result)
                    page.mouse.move(0, 0)
                    behavior.append(result)
            internal = [route for route in routes if route != '/']
            for mode in ('no-js', 'svg-failure', 'reduced-initial'):
                fallback = browser.new_context(viewport={'width': 320, 'height': 900}, java_script_enabled=mode != 'no-js', reduced_motion='reduce' if mode == 'reduced-initial' else 'no-preference')
                if mode == 'svg-failure':
                    fallback.route('**/hero-circuits.svg', lambda request: request.abort())
                sample = fallback.new_page()
                for route in internal:
                    sample.goto(base + route)
                    assert_static_usable(sample, route, image_expected=mode != 'svg-failure')
                    assert sample.locator('h1').count() == 1
                    assert sample.evaluate('document.documentElement.scrollWidth <= innerWidth')
                    if route == '/contato':
                        assert sample.locator('#contato-mensagem').count() == 1
                    if screenshots:
                        sample.screenshot(path=str(output / f'{slug(route)}-320-{mode}.png'), animations='disabled')
                fallback.close()
            assert not errors, errors
            browser.close()
        save(output / 'metrics.json', {'routes': routes, 'widths': WIDTHS, 'captures': results, 'behavior': behavior,
                                     'fallbacks': ['no-js', 'svg-failure', 'reduced-initial'], 'pageErrors': errors})
        pngs = len(results) + len(internal) * 3 if screenshots else 0
        print(f'Hero checks OK: {len(routes)} routes, {len(results)} responsive cases, {len(behavior)} behavior checks, {len(internal)*3} fallback checks, {len(routes)*2} axe reports, {pngs} PNGs written')
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'docs/hero-standardization/evidence')
    parser.add_argument('--axe-source', type=Path, default=Path(os.environ.get('AXE_SOURCE', ROOT / 'node_modules/axe-core/axe.min.js')))
    parser.add_argument('--no-screenshots', action='store_true', help='Keep JSON evidence without writing PNG captures')
    args = parser.parse_args()
    if not args.axe_source.is_file():
        parser.error('axe-core missing: use --axe-source or AXE_SOURCE for an existing axe.min.js')
    run(args.output_dir.resolve(), args.axe_source.resolve(), screenshots=not args.no_screenshots)
