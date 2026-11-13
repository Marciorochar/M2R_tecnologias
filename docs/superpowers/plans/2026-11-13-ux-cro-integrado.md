# UX/CRO integrado — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Work inline; use fresh multi-agent audit at the end.

**Goal:** Clarify the M2R offer and service paths, reduce uncertainty in contact, synchronize hero motion controls, and archive repeatable responsive/accessibility/performance evidence.

**Architecture:** Keep the static HTML/CSS/JavaScript site and its existing Vercel routing. Reuse the current Playwright, axe-core and Lighthouse setup; add no backend, analytics service, or new runtime dependency. Build in an isolated worktree from the preserved stash snapshot, importing only the staged circuit asset/test files required by the approved design.

**Tech Stack:** HTML, CSS, vanilla JavaScript, Python `unittest`, Playwright, axe-core 4.14.0, Lighthouse 13.6.0, Vercel static routes.

**Spec:** `docs/superpowers/specs/2026-11-13-ux-cro-integrado-design.md`

## Global Constraints

- “Sites, sistemas e automações para organizar processos” is the approved H1 proposal; retain “M2R Tecnologias” as brand eyebrow.
- Preserve all nine current service names and descriptions; do not add commercial scopes.
- The site does not name buyer segments explicitly; do not invent audience, outcomes, metrics, reviews, clients, or case studies.
- “O formulário prepara um e-mail para conclusão no aplicativo” must be clear before fields are filled; do not implement server-side submission or send real contact messages.
- Keep WhatsApp visually first while retaining phone, direct email, and the copy fallback; do not claim it is the company’s declared preferred channel.
- Preserve the dark-brown, white, and gold circuit identity and the existing reduced-motion behavior.
- Do not publish/deploy, create a pull request, modify the original conflicted worktree, apply/drop the stash, or import unrelated Graphify artifacts.
- Do not claim field Core Web Vitals from Lighthouse lab results; report INP as unavailable if the run does not provide it.
- Use the existing pinned dependencies and no new production or development dependency.

## Review Focus

- At 320 px and short viewport height, fixed WhatsApp and sticky navigation must not cover service anchors, contact controls, or the primary action. Test in `tools/browser_check.py` at 320 px.
- A service anchor opened directly or by clicking must land on the named card below the sticky navigation, with a visible focus target. Test each mapped fragment in `tools/test_ux_home_services.py` and browser checks.
- Pause, resume, `prefers-reduced-motion`, tab hiding, and leaving/re-entering the hero must keep the visible dot, video, SVG animation, and accessible status in agreement. Exercise transitions in the browser check.
- Without JavaScript, contact routes and direct channels remain usable and no unfinished email is presented as sent. Test static fallback in `tools/test_ux_contact.py` and the no-JavaScript browser context.
- When one of the three routes or a hero media asset is missing, test/evidence generation must fail clearly and preserve the source worktree. Test route/asset validation and verify the original worktree remains unchanged in Task 1.

---

### Task 1: Establish the isolated implementation baseline

**Files:**
- Create worktree/branch: `C:\Users\marci\Desktop\M2R-UX-CRO` / `codex/ux-cro-integrado-2026-11-13`.
- Copy from the original index into the new worktree: `frontend/assets/js/hero-circuits.js`, `frontend/assets/video/m2r-circuitos.webm`, `tools/test_hero_circuits.py`.
- Copy: `docs/superpowers/specs/2026-11-13-ux-cro-integrado-design.md`.
- Recompute hashes in the isolated worktree with `tools/version-assets.js`.

**Interfaces:**
- Consumes: stash snapshot `0edd05481b3b0aabaf465a0b0cc6f857ddf39581`; original index stage-0 files listed above.
- Produces: clean isolated feature branch with the circuit-enabled source, existing test/toolchain, and approved design doc. Original worktree and `refs/stash` remain byte-for-byte unchanged.

- [ ] **Step 1: Record and verify the source snapshot and original state**

Run: `rtk git rev-parse refs/stash` and `rtk git status --short --branch` in the original repository.
Expected: stash resolves to `0edd05481b3b0aabaf465a0b0cc6f857ddf39581`; the existing unmerged files and dirty state are recorded and left untouched.

- [ ] **Step 2: Create an isolated worktree from the tracked stash snapshot**

Run: `rtk git worktree add -b codex/ux-cro-integrado-2026-11-13 C:\Users\marci\Desktop\M2R-UX-CRO 0edd05481b3b0aabaf465a0b0cc6f857ddf39581`.
Expected: new branch points at the snapshot commit and target worktree has no unresolved index entries.

- [ ] **Step 3: Copy only the staged circuit files and approved design into the isolated worktree**

Copy the three listed source files from the original working directory and the approved spec. Do not copy the stash’s third parent or other untracked folders.

Expected: the copied files’ `git hash-object` values match the source files; `frontend/index.html`, `frontend/pages/servicos.html`, `frontend/pages/contato.html`, and `frontend/assets/css/style.css` contain no conflict markers; original `refs/stash` and worktree remain unchanged.

- [ ] **Step 4: Generate and check asset hashes**

Run: `rtk node tools/version-assets.js` then `rtk node tools/version-assets.js --check` in the isolated worktree.
Expected: the second command prints `versoes dos assets atualizadas`; every loaded CSS/JS URL refers to the content hash of the restored files.

- [ ] **Step 5: Run baseline static tests before product changes**

Run: `rtk .venv-audit\Scripts\python.exe tools\test_site_tools.py` and `rtk .venv-audit\Scripts\python.exe tools\test_hero_circuits.py`.
Expected: both baseline suites pass before the new UX behavior is added.

- [ ] **Step 6: Commit the isolated baseline**

Commit only the three copied circuit files, the design doc, and generated hash updates in the isolated branch.
Expected: baseline commit exists on `codex/ux-cro-integrado-2026-11-13`; original worktree has no new changes.

### Task 2: Clarify the home offer and make service destinations specific

**Files:**
- Modify: `frontend/index.html`.
- Modify: `frontend/pages/servicos.html`.
- Modify: `frontend/assets/css/style.css` (anchor offset/visible focus only if required by the sticky header).
- Create: `tools/test_ux_home_services.py`.
- Update generated asset URLs with `tools/version-assets.js`.

**Interfaces:**
- Consumes: the approved text and service mapping from the design doc.
- Produces: Hero H1/eyebrow/subtitle/CTAs; stable IDs `servico-web`, `servico-automacao`, and `servico-dados`; “Ver todos os serviços” for the broad home card; three service groups retaining the same nine article titles/descriptions.

- [ ] **Step 1: Write failing tests for copy, CTA, anchors, and the nine-card catalogue**

Add tests asserting the exact H1, eyebrow, subtitle, CTA labels and hrefs; the three home-card fragments resolve to unique IDs; the broad card says “Ver todos os serviços” and points to `/servicos`; group headings are the three names in the design; all nine existing service titles remain exactly once.

- [ ] **Step 2: Run the new tests and confirm the expected failure**

Run: `rtk .venv-audit\Scripts\python.exe tools\test_ux_home_services.py`.
Expected: FAIL on the old H1/CTA, missing fragment IDs/group headings, and unchanged generic link label.

- [ ] **Step 3: Implement the approved Hero copy and service structure**

Set eyebrow `M2R Tecnologias`, H1 `Sites, sistemas e automações para organizar processos`, subtitle `Desenvolvemos soluções digitais sob medida para apresentar marcas, automatizar rotinas e organizar dados.`, primary CTA `Converse sobre seu projeto` → `/contato`, secondary CTA `Ver serviços` → `/servicos`. Add IDs and card links per the design; group existing nine service cards as presence digital, operation/information, and solutions/guidance. Preserve descriptions and project status.

- [ ] **Step 4: Run focused and route validation tests**

Run: `rtk .venv-audit\Scripts\python.exe tools\test_ux_home_services.py`, `rtk .venv-audit\Scripts\python.exe tools\test_site_tools.py`, and `rtk node tools/version-assets.js --check`.
Expected: all tests pass; `Site.check()` accepts every fragment; hash check passes.

- [ ] **Step 5: Commit the home/service pathway**

Commit the home, service, minimal anchor CSS, tests, and hash updates.
Expected: commit is limited to the approved home/service path.

### Task 3: Make the contact handoff clear before form entry

**Files:**
- Modify: `frontend/pages/contato.html`.
- Create: `tools/test_ux_contact.py`.
- Update generated asset URLs with `tools/version-assets.js` only if a linked asset changes.

**Interfaces:**
- Consumes: existing mailto/copy behavior in `frontend/assets/js/script.js` and approved contact copy.
- Produces: WhatsApp visually first; phone/email alternatives remain; external email-app step appears before fields; form activation, validation and copy behavior remain unchanged.

- [ ] **Step 1: Write failing tests for channel order, external handoff disclosure and no-send behavior**

Assert the visible external-email instruction precedes the form fields, WhatsApp link is first in the direct contact list, phone and email remain, form is initially hidden/disabled in markup, and the page does not claim receipt.

- [ ] **Step 2: Run the new tests and confirm they fail**

Run: `rtk .venv-audit\Scripts\python.exe tools\test_ux_contact.py`.
Expected: FAIL because the external step is currently inside the hidden form and WhatsApp follows phone/email.

- [ ] **Step 3: Implement the approved contact hierarchy without adding transmission**

Move/add a concise email-app disclosure beside the contact choices before the form. Place the existing WhatsApp link first and visually primary; retain telephone, direct email, hidden-until-JS form, `mailto:`, copy fallback, field validation and privacy note. Do not send a message in tests.

- [ ] **Step 4: Run contact and static route checks**

Run: `rtk .venv-audit\Scripts\python.exe tools\test_ux_contact.py` and `rtk .venv-audit\Scripts\python.exe tools\test_site_tools.py`.
Expected: both pass; no new backend or network submission path exists.

- [ ] **Step 5: Commit the contact handoff**

Commit only the contact markup and its regression tests.
Expected: external handoff remains explicit and all listed channels remain usable.

### Task 4: Synchronize the hero pause state

**Files:**
- Modify: `frontend/assets/js/hero-circuits.js`.
- Modify: `frontend/assets/css/style.css`.
- Modify: `tools/test_hero_circuits.py`.
- Update generated asset URLs with `tools/version-assets.js`.

**Interfaces:**
- Consumes: `refreshAnimation()`, `userPaused`, `reducedMotion`, `.home-hero--circuits.motion-paused`, and existing video/rAF lifecycle.
- Produces: one synchronized pause class/state for status-dot animation and the current video/SVG animation controls.

- [ ] **Step 1: Write a failing regression test for paused-state synchronization**

Assert the common animation refresh updates the Hero paused class and the CSS state pauses `.home-hero-status-dot`; verify the pause state is removed on resume.

- [ ] **Step 2: Run the regression test and confirm failure**

Run: `rtk .venv-audit\Scripts\python.exe tools\test_hero_circuits.py`.
Expected: FAIL because JavaScript does not currently synchronize `.motion-paused`.

- [ ] **Step 3: Implement the minimal common-state update**

Update the Hero class within `refreshAnimation()` for manual pause and ensure resume removes it. Keep reduced-motion handling, hidden-tab and intersection behavior intact; do not change circuit appearance or add another animation loop.

- [ ] **Step 4: Run unit and browser motion transition checks**

Run: `rtk .venv-audit\Scripts\python.exe tools\test_hero_circuits.py`.
Expected: pass; browser-level pause/resume and reduced-motion assertions are added and run in Task 5.

- [ ] **Step 5: Regenerate hashes and commit the motion fix**

Run: `rtk node tools/version-assets.js --check`; if stale, regenerate then rerun. Commit JS/CSS/test/hash changes.
Expected: all hero assets are hash-versioned and the working branch passes the hash gate.

### Task 5: Archive responsive, accessibility and performance evidence

**Files:**
- Modify: `tools/browser_check.py`.
- Modify: `tools/lighthouse_check.py`.
- Modify: `tools/test_lighthouse_check.py`.
- Create: `tools/test_browser_check.py`.
- Create generated artifacts: `docs/auditoria/evidencias/responsivo/`, `docs/auditoria/evidencias/lighthouse/`.

**Interfaces:**
- Consumes: the local `Site` server, Playwright and axe already used by current checks; the three named canonical routes.
- Produces: responsive evidence manifest and viewport captures for `/`, `/servicos`, `/contato` at 320, 390, 768, 1024 and 1440 px; mobile Lighthouse JSON for all three routes and desktop Lighthouse JSON for `/`; pause/resume runtime checks; lab metric extraction with unavailable metrics labelled unavailable.

- [ ] **Step 1: Write failing tests for evidence target generation and Lighthouse output/metric extraction**

Test that responsive targets are exactly the three routes × five requested widths; capture names are stable and route-safe; Lighthouse output names encode route/device; LCP/CLS are read only when present; INP stays unavailable if Lighthouse does not provide it; malformed/missing Lighthouse categories still fail explicitly.

- [ ] **Step 2: Run the new tool tests and confirm failure**

Run: `rtk .venv-audit\Scripts\python.exe tools\test_browser_check.py` and `rtk .venv-audit\Scripts\python.exe tools\test_lighthouse_check.py`.
Expected: new helper/target and multi-route output behavior are missing; existing Lighthouse summary tests remain green.

- [ ] **Step 3: Extend the browser check to save reproducible responsive evidence**

For each route and requested width, run layout checks, record viewport/client/document widths and offending elements, scroll each reveal section into view and wait for it to appear, return to top and capture a viewport screenshot. Add browser checks for first Tab/skip link, service fragment landing below the sticky header, WhatsApp/contact visibility, and hero pause/resume/video/status-dot state. Run axe at existing mobile/desktop audit widths and reduced-motion/no-JavaScript fallbacks.

- [ ] **Step 4: Extend the Lighthouse runner for selected routes and device profile**

Add CLI options `--routes` (validated against the known home/services/contact routes), `--device mobile|desktop`, and `--output-dir`; keep existing no-argument CI behavior (home only, `test-results/lighthouse-home.json`). Save JSON by route/device and summarize performance/accessibility/best-practices/SEO plus LCP/CLS if present. Print INP as unavailable when absent. Keep scores informational and lab-only.

- [ ] **Step 5: Run unit tests and browser/axe checks**

Run: `rtk .venv-audit\Scripts\python.exe tools\test_browser_check.py`; `rtk .venv-audit\Scripts\python.exe tools\test_lighthouse_check.py`; `rtk .venv-audit\Scripts\python.exe tools\browser_check.py`.
Expected: all unit/browser checks pass; screenshots and JSON manifest exist for the 15 route/width combinations; axe has no serious/critical findings.

- [ ] **Step 6: Run and archive Lighthouse laboratory audits**

Run: `rtk .venv-audit\Scripts\python.exe tools\lighthouse_check.py --routes / /servicos /contato --device mobile --output-dir docs\auditoria\evidencias\lighthouse` and the same command with `--routes / --device desktop`.
Expected: four valid JSON reports and category summaries; LCP/CLS values are recorded when available, INP is explicitly unavailable unless returned. Do not report field CWV.

- [ ] **Step 7: Review evidence sizes and commit test/evidence changes**

Run: `rtk git diff --check` and list the generated evidence files. Commit the tool changes and requested evidence artifacts; exclude `node_modules`, temporary logs and unrelated files.
Expected: evidence is readable, linked to its route/device/width, no secret/contact data is present, and diff check passes.

## Final execution review

After all task commits, calculate the range from the stash-snapshot base to branch head and dispatch one fresh auditor to review the whole branch against the approved spec, with special focus on merge preservation, static route/anchor integrity, no real contact transmission, accessibility motion states, metrics provenance, and generated evidence completeness. Fix any important finding before handing back. Do not merge, push, open a PR, or deploy.
