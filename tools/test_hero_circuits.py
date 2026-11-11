"""Regression checks for the interactive M2R homepage hero."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "frontend/index.html"
HERO_JS = ROOT / "frontend/assets/js/hero-circuits.js"
VIDEO = ROOT / "frontend/assets/video/m2r-circuitos.webm"


class HeroCircuitsTest(unittest.TestCase):
    def test_original_home_content_and_links_remain(self):
        html = HOME.read_text(encoding="utf-8")
        for text in (
            "M2R Tecnologias",
            "Conheça os serviços",
            "Fale conosco",
            'href="/servicos"',
            'href="/contato"',
            'class="section-block home-about"',
            'class="section-block section-block--muted home-services"',
        ):
            self.assertIn(text, html)

    def test_hero_uses_own_video_and_dense_golden_circuits(self):
        html = HOME.read_text(encoding="utf-8")
        self.assertIn('class="home-hero-motion-video"', html)
        self.assertIn('src="assets/video/m2r-circuitos.webm"', html)
        self.assertIn('id="m2r-circuit-paths"', html)
        self.assertGreaterEqual(len(re.findall(r'id="m2r-path-\d+"', html)), 14)
        self.assertTrue(VIDEO.is_file() and VIDEO.stat().st_size > 10_000)

    def test_interactivity_is_external_and_keyboard_accessible(self):
        html = HOME.read_text(encoding="utf-8")
        self.assertIn('src="assets/js/hero-circuits.js', html)
        self.assertIn('id="m2r-circuit-activate"', html)
        self.assertIn('type="button"', html)
        self.assertTrue(HERO_JS.is_file())
        script = HERO_JS.read_text(encoding="utf-8")
        for feature in ("pointermove", "pointerleave", "click", "requestAnimationFrame", "prefers-reduced-motion"):
            self.assertIn(feature, script)


if __name__ == "__main__":
    unittest.main()
