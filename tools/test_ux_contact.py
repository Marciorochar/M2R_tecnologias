"""Regression checks for truthful, low-friction contact handoff."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTACT = (ROOT / "frontend/pages/contato.html").read_text(encoding="utf-8")
SCRIPT = (ROOT / "frontend/assets/js/script.js").read_text(encoding="utf-8")


class ContactHandoffTest(unittest.TestCase):
    def test_external_email_step_is_visible_before_form_fields(self):
        note_match = re.search(r'<p[^>]+class="contact-email-disclosure"[^>]*>(.*?)</p>', CONTACT, re.S)
        self.assertIsNotNone(note_match, "visible email handoff instruction should be present")
        self.assertLess(note_match.start(), CONTACT.index('<form id="contact-form"'))
        note = note_match.group(1)
        for phrase in ("prepara", "aplicativo de e-mail", "conclui o envio"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, note)

    def test_direct_contact_order_leads_with_whatsapp_and_keeps_phone_and_email(self):
        direct = re.search(r'<div class="contact-direct">(.*?)</div>', CONTACT, re.S)
        self.assertIsNotNone(direct)
        links = re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', direct.group(1), re.S)
        hrefs = [href for href, _ in links]
        self.assertTrue(hrefs[0].startswith("https://wa.me/"), "WhatsApp should lead the direct channels")
        self.assertIn("tel:+5522998270026", hrefs)
        self.assertIn("mailto:marciinhofla@gmail.com", hrefs)

    def test_contact_form_is_not_presented_as_sent_or_transmitted_by_site(self):
        form = re.search(r'<form\b([^>]*)>(.*?)</form>', CONTACT, re.S)
        self.assertIsNotNone(form)
        self.assertIn("hidden", form.group(1))
        self.assertRegex(form.group(2), r'<input[^>]+disabled')
        self.assertRegex(form.group(2), r'<textarea[^>]+disabled')
        self.assertNotRegex(form.group(1), r'\bmethod\s*=\s*["\']?post')
        self.assertNotRegex(CONTACT + SCRIPT, r"recebemos sua mensagem|mensagem enviada com sucesso")
        self.assertIn("window.location.href = `mailto:${contactRecipient}", SCRIPT)
        self.assertIn("navigator.clipboard.writeText", SCRIPT)


if __name__ == "__main__":
    unittest.main()
