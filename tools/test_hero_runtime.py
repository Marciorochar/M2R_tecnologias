"""Browser regressions found during final review of the shared hero runtime."""

import threading
import time
from http.server import ThreadingHTTPServer

import pytest

from browser_check import boxes_overlap, chromium_launch_options
from site_tools import Site, handler_for


@pytest.fixture(scope="module")
def site_base():
    site = Site()

    class QuietHandler(handler_for(site)):
        def log_message(self, *_):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="module")
def browser():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        instance = playwright.chromium.launch(**chromium_launch_options(playwright))
        try:
            yield instance
        finally:
            instance.close()


def test_home_motion_control_does_not_cover_brand_at_320_by_600(browser, site_base):
    page = browser.new_page(viewport={"width": 320, "height": 600}, reduced_motion="no-preference")
    try:
        page.goto(site_base + "/")
        control = page.locator("#m2r-hero [data-hero-motion]")
        control.wait_for(state="visible")
        brand = page.locator("#m2r-hero .section-tag").bounding_box()
        button = control.bounding_box()
        assert not boxes_overlap(brand, button), {"brand": brand, "control": button}
        whatsapp = page.locator(".mobile-whatsapp-cta").bounding_box()
        assert not boxes_overlap(whatsapp, button), {"whatsapp": whatsapp, "control": button}
    finally:
        page.close()


def test_home_effects_initialize_if_home_script_loads_late(browser, site_base):
    context = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="no-preference")

    def delay_home_script(route):
        time.sleep(1.5)
        route.continue_()

    context.route("**/assets/js/hero-circuits.js*", delay_home_script)
    page = context.new_page()
    try:
        page.goto(site_base + "/")
        page.wait_for_function("() => document.querySelector('#m2r-hero')?.dataset.homeEffectsReady === 'true'", timeout=4000)
        assert page.locator("#m2r-hero .home-hero-motion-video").evaluate("video => !video.paused")
        assert page.locator("#m2r-circuit-activate").is_visible()
        assert page.locator("#m2r-hero .m2r-trace-core").count() == 14
    finally:
        context.close()


@pytest.mark.parametrize("invalid_svg", [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 610">',
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 610">' + '<path d="M0 0 H10"/>' * 13 + "</svg>",
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 610">' + '<path d="M"/>' * 14 + "</svg>",
])
def test_invalid_svg_payload_keeps_control_hidden_and_static_art(browser, site_base, invalid_svg):
    context = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="no-preference")

    def replace_fetch(route):
        if route.request.resource_type == "fetch":
            route.fulfill(status=200, content_type="image/svg+xml", body=invalid_svg)
        else:
            route.continue_()

    context.route("**/assets/img/hero-circuits.svg", replace_fetch)
    page = context.new_page()
    try:
        page.goto(site_base + "/servicos")
        control = page.locator("[data-hero-system] [data-hero-motion]")
        page.wait_for_function("() => document.querySelector('[data-hero-system] .hero-system__art')?.complete")
        page.wait_for_timeout(100)
        assert control.evaluate("el => el.hidden")
        assert page.locator("[data-hero-system] .hero-system__live").count() == 0
        assert page.locator("[data-hero-system] .hero-system__art").evaluate("el => el.naturalWidth === 1200")
    finally:
        context.close()
