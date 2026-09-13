"""Reproducible Playwright smoke test for the local site.

Install: python -m pip install playwright && python -m playwright install chromium
Run from repository root: python tools/browser_check.py
"""
import threading
from http.server import ThreadingHTTPServer
from urllib.request import urlopen
from site_tools import Site, handler_for

def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("Playwright ausente. Instale com: python -m pip install playwright; python -m playwright install chromium")
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(Site()))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(); page = browser.new_page()
            page.goto(base + "/contato"); assert page.locator("#contact-form").is_visible()
            page.locator("#name").fill("Teste"); page.locator("#email").fill("invalido"); page.locator("#message").fill("Mensagem")
            assert not page.locator("#email").evaluate("e => e.checkValidity()")
            page.locator("#email").fill("teste@example.com"); page.locator("#prepare-email").click()
            assert page.locator("#name").input_value() == "Teste"
            page.set_viewport_size({"width": 390, "height": 844}); page.goto(base + "/")
            menu = page.locator(".mobile-menu-btn")
            if menu.count():
                menu.click(); assert menu.get_attribute("aria-expanded") == "true"; page.keyboard.press("Escape"); assert menu.get_attribute("aria-expanded") == "false"
            browser.close()
        with sync_playwright() as p:
            browser = p.chromium.launch(); page = browser.new_page(java_script_enabled=False); page.goto(base + "/contato"); assert not page.locator("#contact-form").is_visible(); browser.close()
    finally:
        server.shutdown(); server.server_close(); thread.join()
if __name__ == "__main__": main()
