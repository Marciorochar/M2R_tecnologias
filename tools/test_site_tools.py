import http.client
import json
import re
import threading
import unittest
from http.server import ThreadingHTTPServer

from site_tools import Document, ORIGIN, Site, handler_for


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.site = Site()

    def test_all_links(self):
        self.site.check()

    def test_unknown_routes_fail(self):
        for reference in ("/rota-que-nao-existe", "/rota-que-nao-existe?q=1#x", ORIGIN + "/missing"):
            with self.subTest(reference=reference), self.assertRaises(ValueError):
                self.site.check_link(reference, ORIGIN + "/contato")

    def test_public_relative_links_queries_and_fragments(self):
        for reference in ("../assets/js/script.js?v=1", "/contato?q=1#name", "#name", "/pages/contato.html#name"):
            self.site.check_link(reference, ORIGIN + "/contato")
        with self.assertRaises(ValueError):
            self.site.check_link("#missing", ORIGIN + "/contato")
        with self.assertRaises(ValueError):
            self.site.check_link("/assets/missing.js?v=1", ORIGIN)

    def test_missing_rewrite_and_redirect_destinations(self):
        self.site.config["rewrites"].append({"source": "/broken", "destination": "/frontend/missing.html"})
        with self.assertRaises(ValueError):
            self.site.check()
        self.site = Site()
        self.site.config["redirects"].append({"source": "/broken", "destination": "/missing"})
        with self.assertRaises(ValueError):
            self.site.check()

    def test_redirect_cycle(self):
        self.site.config["redirects"].extend([
            {"source": "/a", "destination": "/b"},
            {"source": "/b", "destination": "/a"},
        ])
        with self.assertRaises(ValueError):
            self.site.check_link("/a", ORIGIN)

    def test_path_traversal(self):
        self.assertIsNone(self.site.file("/assets/%2e%2e/%2e%2e/backend/app.py"))

    def test_security_policy(self):
        self.site.security()

    def test_form_focus_keeps_a_visible_outline(self):
        css = (self.site.root / "frontend/assets/css/style.css").read_text(encoding="utf-8")
        rule = re.search(r"form input:focus-visible,\s*form textarea:focus-visible\s*\{([^}]*)\}", css)
        self.assertIsNotNone(rule)
        self.assertNotIn("outline: none", rule.group(1))

    def test_scroll_listener_is_passive_and_avoids_redundant_class_updates(self):
        script = (self.site.root / "frontend/assets/js/script.js").read_text(encoding="utf-8")
        self.assertIn("window.addEventListener('scroll', updateNavbarScrollState, { passive: true })", script)
        self.assertIn("if (shouldBeScrolled === navbarIsScrolled) return", script)

    def test_frontend_transport_and_static_cache_headers(self):
        config = json.loads((self.site.root / "vercel.json").read_text(encoding="utf-8"))
        asset_headers = {item["key"]: item["value"] for item in config["headers"][0]["headers"]}
        global_headers = {item["key"]: item["value"] for item in config["headers"][1]["headers"]}
        self.assertEqual(asset_headers["Cache-Control"], "public, max-age=604800, must-revalidate")
        self.assertEqual(global_headers["Strict-Transport-Security"], "max-age=2592000")

    def test_blog_titles_fit_search_result_target(self):
        for page in (self.site.root / "frontend/pages/blog").glob("*.html"):
            title = re.search(r"<title>(.*?)</title>", page.read_text(encoding="utf-8")).group(1)
            self.assertLessEqual(len(title), 60, f"Título longo em {page.name}: {title}")

    def test_new_window_links_announce_the_context_change(self):
        pages = list((self.site.root / "frontend").rglob("*.html")) + [self.site.root / "404.html"]
        for page in pages:
            html = page.read_text(encoding="utf-8")
            for link in re.findall(r"<a\b[^>]*target=[\"']_blank[\"'][^>]*>", html, re.IGNORECASE):
                self.assertRegex(link, r"aria-label=[\"'][^\"']*(?:nova aba|aplicativo)[^\"']*[\"']", page.name)

    def test_founder_image_has_responsive_webp_variants(self):
        image_dir = self.site.root / "frontend/assets/img"
        for width in (400, 640, 900):
            image = image_dir / f"Eu_fundador-{width}.webp"
            self.assertTrue(image.is_file(), image.name)
            self.assertLessEqual(image.stat().st_size, 250_000, image.name)
        for page_name in ("sobre.html", "fundador.html"):
            html = (self.site.root / "frontend/pages" / page_name).read_text(encoding="utf-8")
            self.assertIn("Eu_fundador-400.webp 400w", html)
            self.assertIn("Eu_fundador-640.webp 640w", html)
            self.assertIn("Eu_fundador-900.webp 900w", html)

    def test_vercel_deployment_uses_a_strict_allowlist(self):
        lines = [
            line.strip()
            for line in (self.site.root / ".vercelignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertEqual(lines, ["/*", "!frontend", "!404.html", "!vercel.json"])

    def test_vercel_blocks_internal_paths_with_http_404(self):
        routes = self.site.config["routes"]
        blocked = [route for route in routes if route.get("status") == 404]
        self.assertEqual(len(blocked), 2)
        self.assertIn("backend", blocked[0]["src"])
        self.assertIn("vercel", blocked[1]["src"])

    def test_html_entities_and_ids(self):
        document = Document('<a href="/contato?a=1&amp;b=2#nome">x</a><input id="nome">')
        self.assertEqual(document.links, ["/contato?a=1&b=2#nome"])
        self.assertIn("nome", document.ids)

    def test_http_routes(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(self.site))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for route, status in [("/", 200), ("/servicos", 200), ("/contato?ref=test", 200),
                                  ("/missing", 404), ("/missing/nested", 404),
                                  ("/pages/contato.html?ref=test", 308), ("/assets/js/script.js?v=1", 200)]:
                with self.subTest(route=route):
                    connection = http.client.HTTPConnection(*server.server_address)
                    connection.request("GET", route)
                    response = connection.getresponse()
                    self.assertEqual(response.status, status)
                    if status == 308:
                        self.assertEqual(response.getheader("Location"), "/contato?ref=test")
                    else:
                        self.assertTrue(response.getheader("Content-Security-Policy"))
                        self.assertTrue(response.read())
                    connection.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()
