"""Tests for contact channel hierarchy and pre-form external email-app disclosure."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTATO = ROOT / "frontend/pages/contato.html"


class UxContactTest(unittest.TestCase):
    def setUp(self):
        self.html = CONTATO.read_text(encoding="utf-8")

    def test_whatsapp_is_first_in_direct_contact_list_and_alternatives_remain(self):
        direct_block = re.search(
            r'<div class="contact-direct">(.*?)</div>',
            self.html,
            re.DOTALL,
        )
        self.assertIsNotNone(direct_block)
        links = re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>', direct_block.group(1))
        self.assertGreaterEqual(len(links), 3)
        self.assertTrue(
            links[0].startswith("https://wa.me/5522998270026"),
            f"WhatsApp deve ser o primeiro canal direto, encontrado: {links}",
        )
        self.assertIn("tel:+5522998270026", links)
        self.assertIn("mailto:marciinhofla@gmail.com", links)

    def test_external_email_app_disclosure_appears_before_form_fields(self):
        disclosure_pos = self.html.find("O formulário prepara um e-mail para conclusão no aplicativo")
        self.assertNotEqual(
            disclosure_pos,
            -1,
            "Aviso claro de que o formulário prepara um e-mail para conclusão no aplicativo deve existir",
        )
        form_pos = self.html.find('<form id="contact-form"')
        name_input_pos = self.html.find('<input id="name"')
        self.assertNotEqual(form_pos, -1)
        self.assertNotEqual(name_input_pos, -1)
        self.assertLess(
            disclosure_pos,
            name_input_pos,
            "O aviso deve aparecer antes dos campos de preenchimento",
        )

    def test_form_remains_hidden_until_js_and_keeps_copy_fallback(self):
        self.assertRegex(self.html, r'<form id="contact-form"[^>]*\bhidden\b')
        for field_id in ("name", "email", "phone", "message", "prepare-email", "copy-message"):
            self.assertRegex(
                self.html,
                rf'id="{field_id}"[^>]*\bdisabled\b',
                f"Controle {field_id} deve iniciar desabilitado no HTML estático",
            )


if __name__ == "__main__":
    unittest.main()
