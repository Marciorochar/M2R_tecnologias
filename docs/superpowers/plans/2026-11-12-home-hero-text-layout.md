# Home Hero Text Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Melhorar a hierarquia e posição do texto no hero preservando circuitos e identidade M2R.

**Architecture:** Refinar marcação do H1 e painel em `frontend/index.html` e regras finais de `frontend/assets/css/style.css`; não alterar o script dos circuitos. Atualizar hashes via ferramenta existente após CSS.

**Tech Stack:** HTML, CSS e Node.js para version-assets.

**Spec:** `docs/superpowers/specs/2026-11-12-home-hero-text-layout.md`

## Global Constraints

- Preservar conteúdo essencial, paleta marrom/branco/bronze, circuitos interativos, links e controles.
- Sem dependências. Não descartar alterações locais anteriores.
- Não afirmar inspeção visual se o navegador local estiver bloqueado.

## Review Focus

- 320 px: H1 quebra entre palavras e não cria overflow.
- 390 px: CTAs permanecem legíveis e acionáveis.
- 768 px: painel empilhado sem competir com texto.
- 1440 px: painel secundário e circuitos visíveis.
- Foco por teclado e redução de movimento preservados.

---

### Task 1: Texto e composição do hero

**Files:** Modify `frontend/index.html`, `frontend/assets/css/style.css`; refresh hash references with `node tools/version-assets.js`.

**Interfaces:** Consumes existing `.home-hero--circuits`, `.home-hero-panel`, circuit SVG IDs and button IDs. Produces fluid headline and balanced text-panel layout.

- [x] Remove fixed heading break and decorative item numbering while preserving semantic service descriptions.
- [x] Update scoped hero CSS for text width, vertical rhythm, panel weight, 900/640 px stacking and word wrapping.
- [x] Run `node tools/version-assets.js` and `node tools/version-assets.js --check`.
- [x] Run `python -m pytest tools/test_site_tools.py -q -k 'not http_routes'` and `git diff --check`.
- [x] Browser availability checked: localhost socket was blocked (WinError 10013) and file protocol was blocked. Visual rendering at 320, 390, 768 and 1440 px remains unverified.
