"""Regression checks for the interactive M2R homepage hero."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "frontend/index.html"
HERO_JS = ROOT / "frontend/assets/js/hero-circuits.js"
VIDEO = ROOT / "frontend/assets/video/m2r-circuitos.webm"
STYLE = ROOT / "frontend/assets/css/style.css"
SHARED_STYLE = ROOT / "frontend/assets/css/hero-system.css"


class HeroCircuitsTest(unittest.TestCase):
    def test_original_home_content_and_links_remain(self):
        html = HOME.read_text(encoding="utf-8")
        for text in (
            "M2R Tecnologias",
            "Sites, sistemas e automações para organizar processos",
            "Converse sobre seu projeto",
            "Ver serviços",
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
        self.assertIn('class="hero-system__art"', html)
        self.assertIn('src="/assets/img/hero-circuits.svg"', html)
        self.assertNotRegex(html, r'<path\b[^>]*id="m2r-path-\d+"')
        self.assertTrue(VIDEO.is_file() and VIDEO.stat().st_size > 10_000)

    def test_interactivity_is_external_and_keyboard_accessible(self):
        html = HOME.read_text(encoding="utf-8")
        self.assertIn('src="assets/js/hero-circuits.js', html)
        self.assertIn('id="m2r-circuit-activate"', html)
        self.assertIn('aria-labelledby="m2r-circuit-status-text m2r-circuit-tip"', html)
        self.assertIn('type="button"', html)
        self.assertTrue(HERO_JS.is_file())
        script = HERO_JS.read_text(encoding="utf-8")
        for feature in ("pointermove", "pointerleave", "click", "requestAnimationFrame", "prefers-reduced-motion"):
            self.assertIn(feature, script)

    def test_paused_state_synchronizes_status_dot_with_hero_animation(self):
        script = HERO_JS.read_text(encoding="utf-8")
        style = SHARED_STYLE.read_text(encoding="utf-8")
        self.assertRegex(
            script,
            r"hero\.classList\.contains\(['\"]hero-system--paused['\"]\)",
        )
        self.assertRegex(
            style,
            r"\.hero-system--paused\s+\.home-hero-status-dot\s*\{[^}]*animation-play-state:\s*paused",
        )

    def test_home_effects_subscribe_to_the_shared_hero_event(self):
        script = HERO_JS.read_text(encoding="utf-8")
        self.assertIn("m2rhero:ready", script)
        self.assertIn("event.detail.svg", script)
        self.assertIn("event.detail.paths", script)
        self.assertIn("hero-system--paused", script)

    def test_home_activation_control_stays_hidden_until_shared_art_is_ready(self):
        html = HOME.read_text(encoding="utf-8")
        style = STYLE.read_text(encoding="utf-8")
        self.assertRegex(html, r'id="m2r-circuit-activate"[^>]*\bhidden(?:[ >])')
        self.assertRegex(style, r'\.home-hero-circuit-trigger\[hidden\]\s*\{[^}]*display:\s*none')


if __name__ == "__main__":
    unittest.main()
