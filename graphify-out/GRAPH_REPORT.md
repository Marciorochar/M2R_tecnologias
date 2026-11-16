# Graph Report - Meu Site - M2R  (2026-11-16)

## Corpus Check
- Corpus is ~32,345 words - fits in a single context window. You may not need a graph.

## Summary
- 334 nodes · 576 edges · 12 communities (11 shown, 1 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 20 edges (avg confidence: 0.89)
- Token cost: 18,500 input · 6,200 output

## Community Hubs (Navigation)
- Navegador, Lighthouse e Infra de Testes
- Auditoria de HTML e Plano UX/CRO
- Rotas, Segurança Flask e Auditorias
- Validação e Testes do Backend Flask
- Sitemap, Versionamento de Assets e Rotas Vercel
- Páginas do Site, Blog e Identidade Visual
- Quality Gates e Melhoria do Graphify
- Hero de Circuitos e Design UX/CRO
- Verificação de Acessibilidade (axe-core)
- Pipeline de CI (GitHub Actions)
- Automação de Dependências (Dependabot)
- Testes de Sitemap e Robots

## God Nodes (most connected - your core abstractions)
1. `SiteTests` - 35 edges
2. `Site` - 21 edges
3. `client()` - 18 edges
4. `Página Inicial M2R Tecnologias (index.html)` - 14 edges
5. `Document` - 13 edges
6. `check_accessibility()` - 11 edges
7. `handler_for()` - 10 edges
8. `Pipeline de Verificações de Qualidade, Acessibilidade (axe-core) e Lighthouse` - 9 edges
9. `with` - 8 edges
10. `validate_rate_limit_storage()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Tarefa Quality Gates: Auditoria axe-core bloqueante para violações graves` --implements--> `check_accessibility()`  [INFERRED]
  docs/superpowers/plans/2026-11-08-quality-gates.md → tools/browser_check.py
- `Tarefa PR #21: Fusão da main, override CSS .home-hero e hashes` --conceptually_related_to--> `Document`  [INFERRED]
  docs/superpowers/plans/2026-11-08-pr21-remediation.md → tools/site_tools.py
- `Tarefa Quality Gates: Auditoria axe-core bloqueante para violações graves` --conceptually_related_to--> `AccessibilityCheckTests`  [INFERRED]
  docs/superpowers/plans/2026-11-08-quality-gates.md → tools/test_accessibility_check.py
- `Releases 1.0.5 e 1.0.6: Endurecimento de Segurança, Proxies Confiáveis e Allowlist Vercel` --references--> `validate_rate_limit_storage()`  [EXTRACTED]
  CHANGELOG.md → backend/app.py
- `Achados AS-03 a AS-06: Remediação de Exposição na Vercel, Headers HSTS/CSP, Pins de CI e Rate Limit com Redis` --references--> `validate_rate_limit_storage()`  [EXTRACTED]
  docs/auditoria-seguranca-2026-11-04.md → backend/app.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Governança de Segurança, Endurecimento do Backend/Deploy e Validação Automatizada no CI** — docs_auditoria_seguranca_2026_11_04_relatorio, docs_auditoria_seguranca_2026_11_04_controles_remediados, readme_pipeline_validacao_qualidade, readme_backend_flask_opcional_contrato, backend_requirements_dependencias_runtime, requirements_dev_ferramentas_teste_auditoria, changelog_release_1_0_5_1_0_6_endurecimento_seguranca, backend_app, vercel, github_workflows_validate_site [EXTRACTED 1.00]
- **Qualidade de Experiência do Usuário (UX/CRO), Responsividade e Acessibilidade do Frontend** — docs_auditoria_2026_10_17_relatorio_corretivo, docs_auditoria_2026_10_17_correcoes_p0_p1_p2, docs_auditoria_auditoria_ux_cro_diagnostico, docs_auditoria_auditoria_ux_cro_cinco_prioridades, readme_fluxo_contato_mailto_whatsapp, frontend_assets_js_script, frontend_assets_js_hero_circuits, tools_browser_check [EXTRACTED 1.00]
- **Ciclo de Especificações e Planos Superpowers M2R (PR #21 → Quality Gates → UX/CRO → Graphify)** — spec_pr21_remediation_design, plan_pr21_remediation_plano, spec_quality_gates_design, plan_quality_gates_plano, spec_ux_cro_integrado_design, plan_ux_cro_integrado_plano, spec_graphify_improvement_design, plan_graphify_improvement_plano [EXTRACTED 1.00]
- **Malha de Verificação Automatizada Governada pelas Specs (Site, Playwright, Axe, Lighthouse, Hashes)** — plan_pr21_remediation_testes_regressao, plan_quality_gates_auditoria_axe_ci, plan_quality_gates_relatorio_lighthouse, plan_ux_cro_integrado_evidencias_auditoria, tools_site_tools_site, tools_browser_check, tools_lighthouse_check, tools_version_assets [EXTRACTED 1.00]
- **Jornada de Conteúdo, Serviços e Conversão da M2R Tecnologias** — frontend_index_m2r_tecnologias, frontend_pages_servicos_catalogo_servicos, frontend_pages_projetos_portfolio, frontend_pages_projetos_m2r_server_estudo_caso, frontend_pages_blog_blog_insights, frontend_pages_blog_automacao_pequenos_negocios, frontend_pages_blog_organizacao_processos_digitais, frontend_pages_blog_site_profissional_marca, frontend_pages_sobre_institucional, frontend_pages_contato_fluxo_contato [EXTRACTED 1.00]
- **Ecossistema de Publicação, Scripts e Ativos Visuais do Frontend M2R** — frontend_index_m2r_tecnologias, frontend_index_hero_circuitos_svg, frontend_robots_txt, frontend_assets_img_logo_png, frontend_assets_img_m2r_png, frontend_assets_img_og_image_png, frontend_assets_js_script, frontend_assets_js_hero_circuits, tools_generate_sitemap, tools_version_assets, tools_site_tools_site, vercel [EXTRACTED 1.00]

## Communities (12 total, 1 thin omitted)

### Community 0 - "Navegador, Lighthouse e Infra de Testes"
Cohesion: 0.07
Nodes (16): Tarefa PR #21: Testes de regressão de Hero responsivo, breadcrumbs e CSP, Pipeline de Verificações de Qualidade, Acessibilidade (axe-core) e Lighthouse, Dependências Python de Desenvolvimento e Auditoria (pip-audit, Playwright, pytest), check_layout(), check_menu(), check_site(), chromium_launch_options(), main() (+8 more)

### Community 1 - "Auditoria de HTML e Plano UX/CRO"
Cohesion: 0.06
Nodes (7): Tarefa UX/CRO: Arquivamento de evidências responsivas, axe e Lighthouse, Tarefa UX/CRO: Hierarquia de contato com WhatsApp e aviso de app de e-mail, Tarefa UX/CRO: Clareza da oferta na Home e âncoras de serviços, Plano: Implementação de UX/CRO Integrado (2026-11-13), Document, Site, SiteTests

### Community 2 - "Rotas, Segurança Flask e Auditorias"
Cohesion: 0.07
Nodes (14): add_security_headers(), assign_request_id(), has_header_break(), healthz(), home(), ratelimit_handler(), request_too_large_handler(), status() (+6 more)

### Community 3 - "Validação e Testes do Backend Flask"
Cohesion: 0.12
Nodes (32): clean_field(), validate_app_environment(), validate_frontend_origin(), validate_proxy_hops(), validate_rate_limit_storage(), client(), test_api_status_returns_service_status(), test_app_environment_rejects_unknown_values() (+24 more)

### Community 4 - "Sitemap, Versionamento de Assets e Rotas Vercel"
Cohesion: 0.08
Nodes (20): Diretivas de Indexação e Sitemap (robots.txt), Tarefa PR #21: Fusão da main, override CSS .home-hero e hashes, Plano: Remediação do PR #21 (2026-11-08), Spec: Remediação do PR #21 (2026-11-08), buildSitemap(), CHECK_MODE, dates, destinationToFile() (+12 more)

### Community 5 - "Páginas do Site, Blog e Identidade Visual"
Cohesion: 0.17
Nodes (23): Foto do Fundador 400w (Eu_fundador-400.webp), Foto do Fundador 640w (Eu_fundador-640.webp), Foto do Fundador 900w (Eu_fundador-900.webp), Foto Social do Fundador Open Graph (Eu_fundador-social.jpg), Ícone e Emblema M2R (logo.png), Logotipo Horizontal M2R Tecnologias (m2r.png), Banner de Compartilhamento Social (og-image.png), initApp() (+15 more)

### Community 6 - "Quality Gates e Melhoria do Graphify"
Cohesion: 0.09
Nodes (21): name, on, pull_request, push, permissions, contents, branches, branches (+13 more)

### Community 7 - "Hero de Circuitos e Design UX/CRO"
Cohesion: 0.13
Nodes (16): Avaliação das 12 Leis de UX (Jakob, Hick, Fitts, Miller, Von Restorff, Tesler, Estética-Usabilidade), Auditoria Profissional de UX, UI e Conversão (CRO) de 13/11/2026, defaultTip(), draw(), energize(), frame(), nearestOnPath(), onPointerLeave() (+8 more)

### Community 8 - "Verificação de Acessibilidade (axe-core)"
Cohesion: 0.15
Nodes (4): check_accessibility(), serious_axe_violations(), AccessibilityCheckTests, FakePage

### Community 9 - "Pipeline de CI (GitHub Actions)"
Cohesion: 0.12
Nodes (17): jobs, validate, if, name, run, uses, with, name (+9 more)

### Community 10 - "Automação de Dependências (Dependabot)"
Cohesion: 0.14
Nodes (13): prefix, day, interval, time, timezone, updates, commit-message, directory (+5 more)

## Knowledge Gaps
- **7 isolated node(s):** `Avaliação das 12 Leis de UX (Jakob, Hick, Fitts, Miller, Von Restorff, Tesler, Estética-Usabilidade)`, `Tarefa Graphify: Higiene do corpus (.graphifyignore e .graphifyrc)`, `Diretivas de Indexação e Sitemap (robots.txt)`, `Foto Social do Fundador Open Graph (Eu_fundador-social.jpg)`, `Ícone e Emblema M2R (logo.png)` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 125 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Site` connect `Auditoria de HTML e Plano UX/CRO` to `Navegador, Lighthouse e Infra de Testes`, `Páginas do Site, Blog e Identidade Visual`, `Quality Gates e Melhoria do Graphify`?**
  _High betweenness centrality (0.170) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `SiteTests` (e.g. with `Document` and `Site`) actually correct?**
  _`SiteTests` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Avaliação das 12 Leis de UX (Jakob, Hick, Fitts, Miller, Von Restorff, Tesler, Estética-Usabilidade)`, `Tarefa Graphify: Higiene do corpus (.graphifyignore e .graphifyrc)`, `Diretivas de Indexação e Sitemap (robots.txt)` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Navegador, Lighthouse e Infra de Testes` be split into smaller, more focused modules?**
  _Cohesion score 0.0746606334841629 - nodes in this community are weakly interconnected._
- **Why does `Pipeline de Verificações de Qualidade, Acessibilidade (axe-core) e Lighthouse` connect `Navegador, Lighthouse e Infra de Testes` to `Rotas, Segurança Flask e Auditorias`, `Sitemap, Versionamento de Assets e Rotas Vercel`, `Quality Gates e Melhoria do Graphify`, `Verificação de Acessibilidade (axe-core)`, `Automação de Dependências (Dependabot)`?**
  _High betweenness centrality (0.166) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Document` (e.g. with `Tarefa PR #21: Fusão da main, override CSS .home-hero e hashes` and `SiteTests`) actually correct?**
  _`Document` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `Auditoria de HTML e Plano UX/CRO` be split into smaller, more focused modules?**
  _Cohesion score 0.05952380952380952 - nodes in this community are weakly interconnected._