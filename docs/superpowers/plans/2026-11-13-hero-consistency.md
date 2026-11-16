# Hero Consistency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Padronizar os Heroes de todas as páginas internas com a identidade aprovada da Home.

**Architecture:** Aprimoramento progressivo em HTML/CSS/JS estático, SVG compartilhado extraído da Home e estilos internos isolados. Home e seus arquivos permanecem byte a byte. Uma tarefa integrada evita interfaces temporárias entre markup, CSS e script.

**Tech Stack:** HTML, CSS, JavaScript sem dependências novas; Python/pytest e Playwright existentes.

**Spec:** `docs/superpowers/specs/2026-11-13-hero-consistency-design.md`

## Global Constraints
Preservar literalmente `frontend/index.html`, `frontend/assets/css/style.css`, `frontend/assets/js/hero-circuits.js` e o vídeo.
Preservar conteúdo fora dos Heroes, títulos, subtítulos, breadcrumbs, metadados e CTAs existentes.
Sem frameworks, alteração da configuração de produção, deploy ou merge.
Larguras: 320, 390, 768, 1024, 1440 e 1920px.
Workers não criam subagentes e têm propriedade exclusiva dos arquivos autorizados.

## Review Focus
JavaScript indisponível ou SVG falha: texto/CTAs e fundo estático continuam utilizáveis.
Redução de movimento inicial e alterada: pulsos param; controle oculto não bloqueia teclado.
Scroll e aba oculta: animação pausa sem alterar preferência manual.
Artigos com títulos longos, terminal e painel 404: sem sobreposição/overflow em 320px.
Home e conteúdo externo aos Heroes: sem regressão textual, funcional ou visual.

---

### Task 1: Shared internal Hero system and all page integrations

**Files:**
- Create: `frontend/assets/css/internal-hero.css`, `frontend/assets/js/internal-hero.js`, `frontend/assets/img/hero-circuits.svg`.
- Modify: `frontend/pages/**/*.html`, `frontend/404.html`, `404.html`, `tools/version-assets.js`.
- Create: `tools/test_internal_hero.py` (structural/copy preservation and routing regression), `tools/hero_check.py` (browser behavior, six-width screenshots/metrics/axe, reusable and readable, no brittle pixel assertions).
- Report: `.superpowers/sdd/hero-consistency/task-1-report.md`.

**Interfaces:**
- Consumes: original `.page-hero` content, existing `.container`, `.btn`, typography and palette tokens; home SVG path `d` attributes.
- Produces: `.page-hero--circuits` opt-in, `.internal-hero-art` decor, `[data-internal-hero-motion]` control, paused state on root. Only pages opting in load the new stylesheet and script. `hero_check.py` must use existing `Site`, `handler_for` and Playwright launch helpers; supports evidence output to docs/hero-standardization/evidence, inventories all routes dynamically, tests six widths, no change to production server/config.

- [ ] Step 1: Add regression tests that discover every internal HTML hero and assert the opt-in, shared assets, SVG decorative semantics, unique H1, original per-route heading/subtitle, breadcrumbs and original actions. Compare protected files and outside-Hero DOM with git base `7436829` (tests can use git show at that pinned base or fixture data for meaningful preservation).
- [ ] Step 2: Run `rtk proxy python -m pytest tools/test_internal_hero.py -q`; record expected initial failures.
- [ ] Step 3: Implement SVG, CSS and safe JS per spec; use static art fallback, scoped rules, CSS pulse animation, pause button, offscreen/hidden/reduced states and idempotent initialization. Enhance pointer interaction decoratively without extra inaccessible action. New CSS must load after style.css only on internal pages; don't use `.home-hero` on them.
- [ ] Step 4: Apply opt-in, one shared decorative image, motion control and contextual CTAs to every internal page; keep existing panels/classes and article metadata. Add target IDs only where needed. Update both 404 copies identically. Add new CSS/JS assets to version-assets list, regenerate hashes; protected Home must remain unchanged because original assets are unchanged.
- [ ] Step 5: Implement browser validation of Review Focus: all six widths/all routes, unique H1, no overflow/collisions, title and primary CTA contained, positive-size SVG traces, accessible motion control toggles pause, reduced-motion starts/stays static, offscreen/hidden pause, static fallback if JS/network unavailable. Capture after screenshots and JSON metrics. Axe WCAG 2.2 tags supported by installed axe; save reports without full redundant passes.
- [ ] Step 6: Run `rtk proxy python -m pytest tools -q`, `rtk proxy python tools/site_tools.py check`, `rtk proxy python tools/site_tools.py security`, `rtk proxy node tools/version-assets.js --check`, JS syntax checks. Report exact outcomes and limitations.
- [ ] Step 7: Self-review diff, commit only Task 1 owned files, return commit ID and concise report. Do not push. Root will review package, run MCP and existing browser checks, obtain independent audit, route fixes, and publish authorized PR.

## Coordinator validation and delivery
- [ ] Capture before images all routes/six widths with Playwright MCP (72 captures).
- [ ] Run existing browser_check and new hero_check, inspect screenshots, run MCP behavior checks and Chrome DevTools diagnostics.
- [ ] Independent auditor reviews task diff/report and evidence, executor fixes findings, auditor revalidates scoped corrections.
- [ ] Record final evidence and limitations, create screenshot comparison gallery, commit documentation/evidence.
- [ ] Push dedicated branch and create PR targeting main, no merge or deploy command.
