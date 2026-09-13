import http.client
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
