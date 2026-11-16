"""Tests for UX/CRO home offer clarity, service anchors, and grouped catalogue."""

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_tools import Document, ORIGIN, Site


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "frontend/index.html"
SERVICOS = ROOT / "frontend/pages/servicos.html"


class UxHomeServicesTest(unittest.TestCase):
    def setUp(self):
        self.site = Site()
        self.home_html = HOME.read_text(encoding="utf-8")
        self.servicos_html = SERVICOS.read_text(encoding="utf-8")

    def test_home_hero_eyebrow_h1_subtitle_and_ctas(self):
        self.assertIn(
            '<span class="section-tag section-tag--dark">M2R Tecnologias</span>',
            self.home_html,
        )
        self.assertIn(
            "<h1>Sites, sistemas e automações para organizar processos</h1>",
            self.home_html,
        )
        self.assertIn(
            "Desenvolvemos soluções digitais sob medida para apresentar marcas, automatizar rotinas e organizar dados.",
            self.home_html,
        )
        self.assertRegex(
            self.home_html,
            r'<a class="btn btn-primary" href="/contato">Converse sobre seu projeto</a>',
        )
        self.assertRegex(
            self.home_html,
            r'<a class="btn btn-secondary" href="/servicos">Ver todos os serviços</a>',
        )

    def test_home_service_cards_link_to_specific_anchors_and_catalogue(self):
        expected_links = (
            ('/servicos#servico-web', 'Conhecer desenvolvimento web'),
            ('/servicos', 'Ver todos os serviços'),
            ('/servicos#servico-automacao', 'Ver soluções de automação'),
            ('/servicos#servico-dados', 'Conhecer dashboards e dados'),
        )
        for href, label in expected_links:
            with self.subTest(href=href):
                self.assertIn(
                    f'<a class="text-link home-service-link" href="{href}">{label}</a>',
                    self.home_html,
                )
                self.site.check_link(href, ORIGIN + "/")

    def test_servicos_page_groups_nine_cards_with_unique_anchor_ids(self):
        doc = Document(self.servicos_html)
        for anchor_id in ("servico-web", "servico-automacao", "servico-dados"):
            self.assertIn(anchor_id, doc.ids, f"ID ausente em servicos.html: {anchor_id}")
            self.assertEqual(
                len(re.findall(rf'\bid=["\']{anchor_id}["\']', self.servicos_html)),
                1,
            )

        for group_heading in (
            "Presença digital",
            "Operação e informação",
            "Soluções e orientação",
        ):
            self.assertIn(group_heading, self.servicos_html)

        expected_services = (
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
        for title in expected_services:
            with self.subTest(service=title):
                matches = re.findall(rf"<h3[^>]*>{re.escape(title)}</h3>|<h2[^>]*>{re.escape(title)}</h2>", self.servicos_html)
                self.assertEqual(len(matches), 1, f"Serviço deve aparecer exatamente 1 vez: {title}")


if __name__ == "__main__":
    unittest.main()
