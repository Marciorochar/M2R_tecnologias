"""Regression checks for the integrated home-to-services path."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / "frontend/index.html").read_text(encoding="utf-8")
SERVICES = (ROOT / "frontend/pages/servicos.html").read_text(encoding="utf-8")
STYLE = (ROOT / "frontend/assets/css/style.css").read_text(encoding="utf-8")


class HomeServicesPathTest(unittest.TestCase):
    def test_hero_copy_and_ctas_match_the_approved_offer(self):
        self.assertRegex(HOME, r"<span class=\"section-tag section-tag--dark\">M2R Tecnologias")
        self.assertRegex(HOME, r"<h1>Sites, sistemas e automações para organizar processos</h1>")
        self.assertIn(
            "Desenvolvemos soluções digitais sob medida para apresentar marcas, "
            "automatizar rotinas e organizar dados.",
            HOME,
        )
        self.assertRegex(
            HOME,
            r'<a class="btn btn-primary" href="/contato">Converse sobre seu projeto</a>',
        )
        self.assertRegex(HOME, r'<a class="btn btn-secondary" href="/servicos">Ver serviços</a>')

    def test_home_service_cards_open_the_named_service_or_catalogue(self):
        expected = {
            "Desenvolvimento Web": "/servicos#servico-web",
            "Automação de Processos": "/servicos#servico-automacao",
            "Dashboards e Dados": "/servicos#servico-dados",
        }
        for title, href in expected.items():
            with self.subTest(title=title):
                self.assertIsNotNone(
                    re.search(
                        rf"<h3>{re.escape(title)}</h3>.*?<a[^>]+href=\"{re.escape(href)}\"",
                        HOME,
                        flags=re.S,
                    ),
                    f"home link for {title} should target {href}",
                )
        self.assertRegex(
            HOME,
            r'<a class="text-link home-service-link" href="/servicos">Ver todos os serviços</a>',
        )

    def test_services_are_grouped_without_changing_the_nine_catalogue_items(self):
        headings = {
            "servicos-presenca-heading": "Presença digital",
            "servicos-operacao-heading": "Operação e informação",
            "servicos-solucoes-heading": "Soluções e orientação",
        }
        for heading_id, heading in headings.items():
            with self.subTest(heading=heading):
                self.assertIn(f'<h2 id="{heading_id}">{heading}</h2>', SERVICES)

        titles = (
            "Desenvolvimento web",
            "Sites institucionais",
            "Landing pages",
            "Automação de processos",
            "Dados e dashboards",
            "Sistemas personalizados",
            "Integrações backend",
            "Soluções digitais",
            "Consultoria tecnológica",
        )
        for title in titles:
            with self.subTest(title=title):
                self.assertEqual(len(re.findall(rf"<h[23]>{re.escape(title)}</h[23]>", SERVICES)), 1)

    def test_service_fragments_are_unique_and_clear_the_sticky_header(self):
        for service_id in ("servico-web", "servico-automacao", "servico-dados"):
            with self.subTest(service_id=service_id):
                self.assertEqual(SERVICES.count(f'id="{service_id}"'), 1)
                self.assertRegex(
                    SERVICES,
                    rf'<article[^>]+id="{service_id}"[^>]+tabindex="-1"',
                )
        self.assertIn("scroll-margin-top:", STYLE)


if __name__ == "__main__":
    unittest.main()
