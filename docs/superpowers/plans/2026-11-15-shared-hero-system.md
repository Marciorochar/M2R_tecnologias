# Sistema visual compartilhado dos Heroes M2R — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Unificar a base visual, os circuitos e os controles de movimento da Home e dos 11 destinos internos, preservando variantes de conteúdo e composição.

**Architecture:** `hero-system.css` será a fonte comum de tokens, superfície, circuito e controle. `hero-system.js` aprimorará progressivamente todos os elementos `data-hero-system` a partir do SVG canônico, manterá um único estado de pausa e notificará a camada opcional de interações da Home; `hero-circuits.js` continuará carregado somente na Home. `internal-hero.css` permanecerá como folha de composição das variantes internas.

**Tech Stack:** HTML estático, CSS, JavaScript sem framework, SVG local, pytest, Playwright/Chromium e utilitário Node existente para hashes de assets.

**Spec:** `docs/superpowers/specs/2026-11-15-shared-hero-system-design.md`

## Global Constraints

- Manter a Home como referência visual; usar sua superfície ativa `#4d3021`, `#302016`, `#23160f`, `#1c120d`, texto branco e acento dourado `#f1c994`.
- Todas as páginas usam a mesma base visual, a mesma fonte dos circuitos e o mesmo padrão de pausa/retomada.
- Conteúdo, painéis, metadados, breadcrumbs, ações e composição continuam específicos por página.
- O vídeo e interações extras de clique/ponteiro continuam opcionais da Home; páginas internas não carregam o vídeo.
- O SVG estático permanece como fallback sem JavaScript e contém exatamente os 14 caminhos existentes no `viewBox="0 0 1200 610"`.
- Respeitar a CSP atual; não instalar dependências nem introduzir framework, script inline ou estilo inline.
- Manter `404.html` e `frontend/404.html` equivalentes.
- Evitar colisões com CTA/WhatsApp em 320, 390, 768, 1024, 1440 e 1920 px.
- Gerar hashes HTML com `tools/version-assets.js`; validar com `rtk node tools/version-assets.js --check`.
- Não alterar conteúdo fora dos Heroes nem configuração/deploy/merge.

## Review Focus

- **Sem JavaScript ou fetch/SVG inválido:** arte estática, título e ação permanecem; o controle de movimento não fica visível como se estivesse funcional. Testar ausência de JS e resposta de fetch não OK na Task 3.
- **Redução de movimento inicial ou alterada em runtime:** pulsos, vídeo e efeitos extras param; o controle fica coerente com a preferência. Testar a preferência ligada/desligada e sua mudança na Task 3.
- **Pausa manual combinada com aba oculta ou Hero fora da tela:** a pausa manual não se perde e os efeitos não continuam em segundo plano. Testar as transições na Task 3.
- **Títulos e rótulos longos em telas estreitas:** conteúdo quebra sem overflow e os controles não cobrem CTA/WhatsApp. Cobrir artigos, projeto detalhado e 404 na Task 4.
- **Variantes com estrutura própria:** painel da Home, metadados de artigos, grid/terminal do projeto e painel 404 permanecem. Comparar DOM fora do Hero com a base da Task 1 e percorrer todas as rotas na Task 4.

---

### Task 1: Fixar o contrato compartilhado em testes

**Files:**
- Modify: `tools/test_internal_hero.py`
- Modify: `tools/test_hero_circuits.py`
- Modify: `tools/test_browser_check.py`

**Interfaces:**
- Consumes: base de comparação `4c41e22708291fa4156893c7e1abe66f1345bd94`, `Site` de `tools/site_tools.py` e helpers existentes de Playwright.
- Produces: contrato de marcação compartilhada `.hero-system`, `data-hero-system`, `data-hero-motion`, imagem `.hero-system__art`, overlay `.hero-system__live`, classe `.hero-system--paused` e evento `m2rhero:ready` com `detail.svg` e `detail.paths`.

- [ ] **Step 0: Capturar baseline antes da implementação com `rtk proxy python tools/hero_check.py --output-dir test-results/hero-system/before`; confirmar 12 rotas e seis larguras `(320, 390, 768, 1024, 1440, 1920)`.**
- [ ] **Step 1: Adicionar `test_all_hero_routes_use_shared_system_contract` em `tools/test_internal_hero.py`.** Parametrizar Home, todos os HTML internos, `frontend/404.html` e `404.html`; exigir a base CSS/JS compartilhada, `data-hero-system`, `<img class="hero-system__art">` apontando para `/assets/img/hero-circuits.svg`, botão `data-hero-motion` iniciado oculto e estado `aria-pressed="false"`. Exigir `hero-circuits.js` somente em `frontend/index.html`.
- [ ] **Step 2: Adicionar `test_internal_variants_keep_their_original_content` em `tools/test_internal_hero.py`.** Comparar cada documento com o commit-base removendo apenas o nó Hero e as referências novas dos assets; confirmar igualdade do restante do DOM, CTAs, metadados e breadcrumbs. Manter também a igualdade byte a byte entre as duas cópias do 404.
- [ ] **Step 3: Substituir `test_protected_home_files` por `test_home_video_is_preserved` e atualizar `test_shared_svg_exact_home_paths_and_decorative_content`.** Continuar protegendo o arquivo de vídeo; validar que o SVG canônico tem 14 caminhos e é referenciado como fallback pela Home e pelas rotas internas, sem uma segunda lista divergente de `d` no HTML da Home.
- [ ] **Step 4: Atualizar `test_browser_check.py::BrowserCheckTests.test_targets_are_three_canonical_routes_at_five_requested_widths` para exigir as seis larguras `(320, 390, 768, 1024, 1440, 1920)`.** Adicionar `test_shared_motion_control_uses_common_contract` para nomes, `aria-pressed` e estados esperados nas variantes Home, simples, artigo, projeto e 404.
- [ ] **Step 5: Executar `rtk proxy python -m pytest tools/test_internal_hero.py tools/test_hero_circuits.py tools/test_browser_check.py -q`.** Esperado antes da implementação: falhas nos novos seletores compartilhados, na proteção antiga da Home e na largura 1920; nenhuma falha de importação.
- [ ] **Step 6: Commit dos testes de contrato.** `rtk git add tools/test_internal_hero.py tools/test_hero_circuits.py tools/test_browser_check.py && rtk git commit -m "test: define shared hero system contract"`.

### Task 2: Unificar base visual e integrar as variantes HTML

**Files:**
- Create: `frontend/assets/css/hero-system.css`
- Modify: `frontend/assets/css/style.css`
- Modify: `frontend/assets/css/internal-hero.css`
- Modify: `frontend/index.html`
- Modify: `frontend/pages/**/*.html`
- Modify: `frontend/404.html`
- Modify: `404.html`

**Interfaces:**
- Consumes: contrato HTML da Task 1 e SVG estático `frontend/assets/img/hero-circuits.svg`.
- Produces: markup `.hero-system` compartilhado; `.hero-system__art` para fallback; `.hero-system__live` como camada aprimorada; `[data-hero-motion]` para controle comum; classes atuais específicas de cada variante mantidas.

- [ ] **Step 1: Rodar `rtk proxy python -m pytest tools/test_internal_hero.py -q` e confirmar que `test_all_hero_routes_use_shared_system_contract` falha pelos novos elementos ausentes.**
- [ ] **Step 2: Criar `hero-system.css` com tokens compartilhados da Home, superfície e camadas comuns, apresentação do SVG, estilo/foco do botão de movimento e estados `.hero-system--paused`.** O gradiente comum deve usar os valores ativos definidos nas Global Constraints; reduzir a intensidade da arte em telas estreitas sem ocultar texto.
- [ ] **Step 3: Refatorar `style.css` e `internal-hero.css` para remover gradientes, cores, animação-base e estilo de controle duplicados.** Deixar em `style.css` apenas composição/interações específicas da Home e em `internal-hero.css` somente ajustes estruturais das variantes internas.
- [ ] **Step 4: Migrar Home, páginas internas e os dois 404 para o contrato comum.** Usar a mesma imagem estática SVG com dimensões 1200×610; manter classes de conteúdo e variante (`home-hero`, `article-hero`, `project-detail-hero`, `error-page`) e preservar painéis, metadados, ações, breadcrumbs e ordem do DOM.
- [ ] **Step 5: Adicionar `hero-system.css` à Home e a todos os documentos internos depois de `style.css`; remover a dependência das páginas sobre a antiga apresentação base de `internal-hero.css`, mantendo essa folha somente onde a variante precisar de composição.**
- [ ] **Step 6: Executar `rtk proxy python -m pytest tools/test_internal_hero.py -q`.** Esperado: contrato de marcação, preservação fora dos Heroes, igualdade dos 404 e SVG canônico passam.
- [ ] **Step 7: Commit da migração visual.** `rtk git add frontend tools/test_internal_hero.py && rtk git commit -m "feat: share hero visual system"`.

### Task 3: Compartilhar circuitos e estado de movimento

**Files:**
- Create: `frontend/assets/js/hero-system.js`
- Delete: `frontend/assets/js/internal-hero.js`
- Modify: `frontend/assets/js/hero-circuits.js`
- Modify: `frontend/index.html`
- Modify: `frontend/pages/**/*.html`
- Modify: `frontend/404.html`
- Modify: `404.html`
- Modify: `tools/version-assets.js`
- Modify: `tools/test_internal_hero.py`
- Modify: `tools/test_hero_circuits.py`
- Modify: `tools/test_browser_check.py`

**Interfaces:**
- Consumes: markup e classes da Task 2.
- Produces: `hero-system.js` varre `[data-hero-system]`, valida resposta same-origin do SVG com 14 caminhos, popula `.hero-system__live` e dispara `m2rhero:ready` com `{svg, paths}`; o controle `[data-hero-motion]` atualiza `aria-pressed` e `.hero-system--paused`.
- The Home-only `hero-circuits.js` subscribes to `m2rhero:ready`, adds only its pointer/click/video effects to the provided SVG, and checks `.hero-system--paused` before advancing custom motion.

- [ ] **Step 1: Ampliar `test_shared_motion_control_uses_common_contract` em `tools/test_browser_check.py`.** Verificar que a Home e as variantes internas expõem os mesmos rótulos de pausar/retomar, semântica de `aria-pressed` e classe de pausa; confirmar que o script exclusivo da Home acrescenta interações ao evento `m2rhero:ready`.
- [ ] **Step 2: Executar `rtk proxy python -m pytest tools/test_internal_hero.py tools/test_hero_circuits.py tools/test_browser_check.py -q` e confirmar falhas por script/evento compartilhado ausente e contrato de controle divergente.**
- [ ] **Step 3: Implementar `hero-system.js` como aprimoramento progressivo idempotente.** Para cada raiz `[data-hero-system]`, validar que a imagem fallback é same-origin; buscar e analisar o SVG; exigir exatamente 14 caminhos; copiar somente a geometria para um SVG construído localmente com `viewBox="0 0 1200 610"`; inserir como `.hero-system__live`; revelar e conectar o controle somente após a inicialização bem-sucedida. Em falha, manter a imagem estática e deixar o controle oculto.
- [ ] **Step 4: Implementar estado único de movimento em `hero-system.js`.** Ativar `.hero-system--paused` quando houver pausa manual, movimento reduzido, documento oculto ou Hero fora da viewport. O botão alterna somente a pausa manual; `aria-pressed` acompanha esse estado; mudanças em runtime de `prefers-reduced-motion` sincronizam o estado. Incluir fallback de visibilidade e `IntersectionObserver` conforme o script interno atual.
- [ ] **Step 5: Refatorar `hero-circuits.js` para ouvir `m2rhero:ready` e consumir `detail.svg`/`detail.paths`.** Manter vídeo, foco de ponteiro, ripples por clique, status e dica da Home; remover o estado duplicado de pausa e interromper o loop de animação sempre que `.hero-system--paused` estiver ativo.
- [ ] **Step 6: Carregar `hero-system.js` em todas as páginas Hero antes do script exclusivo da Home `hero-circuits.js`; remover referências a `internal-hero.js` e excluir sua entrada de assets.** Incluir `hero-system.css` e `hero-system.js` em `tools/version-assets.js`, retirar o JS removido da lista e regenerar hashes HTML.
- [ ] **Step 7: Executar `rtk proxy python -m pytest tools/test_internal_hero.py tools/test_hero_circuits.py tools/test_browser_check.py -q`.** Esperado: contrato compartilhado e testes das interações exclusivas da Home passam.
- [ ] **Step 8: Commit do runtime compartilhado.** `rtk git add frontend tools && rtk git commit -m "feat: share hero circuit motion"`.

### Task 4: Verify responsive variants and finalize

**Files:**
- Modify: `tools/browser_check.py`
- Modify: `tools/test_browser_check.py`
- Modify: HTML asset hashes if regenerated
- Evidence output: `test-results/hero-system/` (ignored local verification artifacts)

**Interfaces:**
- Consumes: shared CSS/JS, canonical SVG and all route variants from Tasks 2–3.
- Produces: passing responsive/motion regression coverage, six-width captures for 12 routes, current content hashes, and a concise validation record.

- [ ] **Step 1: Extend `RESPONSIVE_WIDTHS` in `tools/browser_check.py` to `(320, 390, 768, 1024, 1440, 1920)` and direct screenshots/manifests to `test-results/hero-system/` rather than overwriting tracked audit snapshots.**
- [ ] **Step 2: Add Playwright assertions for all-route shared styles, single visible shared motion control after enhancement, static art when JavaScript is disabled, fallback on SVG fetch failure, keyboard pause/resume, runtime reduced-motion changes, and paused state when the Hero is offscreen or the tab is hidden.**
- [ ] **Step 3: Add responsive comparison checks for 320/390 px CTA and fixed WhatsApp overlap; cover long article title, project detail grid/terminal, and 404 panel.** Keep the successful 2026-11-15 CI case at `/` 320×600 as a regression target.
- [ ] **Step 4: Executar verificações estáticas e browser.** Comandos: `rtk proxy python -m pytest tools/test_internal_hero.py tools/test_hero_circuits.py tools/test_browser_check.py tools/test_site_tools.py -q`, `rtk node tools/version-assets.js --check`, `rtk proxy python tools/site_tools.py check`, `rtk proxy python tools/browser_check.py` e `rtk proxy python tools/hero_check.py --output-dir test-results/hero-system/after`. Esperado: testes passam, 12 rotas passam nas seis larguras e não há erro de browser nem colisão com CTA/WhatsApp.
- [ ] **Step 5: Revisar capturas nas seis larguras para `/`, `/servicos`, um artigo, `/projetos/m2r-server` e `/404`; comparar as 72 capturas de `after` com `test-results/hero-system/before`.** Confirmar que a base visual está unificada e que as variantes mantêm seu conteúdo; registrar rotas, larguras e limitações em `docs/hero-standardization/shared-system-validation.md`.
- [ ] **Step 6: Executar `rtk node tools/version-assets.js --check` e `rtk git diff --check`; restaurar qualquer evidência auditável rastreada que o browser tenha sobrescrito.** Esperado: hashes atuais, nenhum erro de whitespace e apenas arquivos de fonte/teste/relatório pretendidos alterados.
- [ ] **Step 7: Commit das verificações finais e do registro.** `rtk git add tools docs/hero-standardization/shared-system-validation.md && rtk git commit -m "test: verify shared hero variants"`.

## Self-review

- **Spec coverage:** common tokens/surface/circuits/control in Tasks 2–3; variants and Home extras in Tasks 2–3; no-JS/fetch failure, motion lifecycle and accessibility in Task 3; responsive collisions and 404 copies in Tasks 2 and 4; hashes/CSP/static checks in Tasks 3–4; before/after evidence in Task 4.
- **Step scan:** every implementation step names files, selectors, expected behavior and a command where appropriate; no task assumes a UI framework or external package.
- **Type/interface consistency:** `hero-system.js` emits `m2rhero:ready` with `{svg, paths}`; the Home listener consumes the same keys and reads `.hero-system--paused`; all route markup uses the named selectors.
- **Review focus:** all five risk classes are paired to tests in Tasks 1, 3 or 4.
- **Proportion:** four tasks keep the coupled CSS/markup/runtime migration together while allowing each task a focused verification and commit.
