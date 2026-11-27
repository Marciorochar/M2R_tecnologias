# Graph Report - Meu Site - M2R  (2026-11-26)

## Corpus Check
- 72 files · ~44,271 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 473 nodes · 837 edges · 23 communities (14 shown, 9 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 29 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Backend Flask, deploy e documentação
- Verificação em navegador e acessibilidade
- Testes do backend Flask
- Validação dos Heroes no navegador
- Medição com Lighthouse
- Páginas do site e sistema de Heroes
- Interações dos circuitos da Home
- Pipeline de CI e quality gates
- Testes estruturais do site
- Sitemap e versionamento de assets
- Auditoria de HTML e UX/CRO
- Testes dos Heroes internos
- Configuração do Dependabot
- Dependências Node e melhoria do Graphify
- Testes de evidências no navegador
- Testes de sitemap e robots
- Parser de HTML dos testes
- Saúde do grafo
- Testes de serviços da Home
- Servidor HTTP de teste
- Testes do fluxo de contato

## God Nodes (most connected - your core abstractions)
1. `SiteTests` - 33 edges
2. `client()` - 18 edges
3. `check_site()` - 18 edges
4. `Página Inicial M2R Tecnologias (index.html)` - 17 edges
5. `run()` - 15 edges
6. `Arte canônica dos circuitos do Hero (14 traçados, 1200x610)` - 14 edges
7. `Site` - 12 edges
8. `check_accessibility()` - 12 edges
9. `main()` - 12 edges
10. `Document` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Tarefa PR #21: Fusão da main, override CSS .home-hero e hashes` --conceptually_related_to--> `Document`  [INFERRED]
  docs/superpowers/plans/2026-11-08-pr21-remediation.md → tools/site_tools.py
- `Tarefa Quality Gates: Auditoria axe-core bloqueante para violações graves` --conceptually_related_to--> `AccessibilityCheckTests`  [INFERRED]
  docs/superpowers/plans/2026-11-08-quality-gates.md → tools/test_accessibility_check.py
- `Tarefa Quality Gates: Auditoria axe-core bloqueante para violações graves` --implements--> `check_accessibility()`  [INFERRED]
  docs/superpowers/plans/2026-11-08-quality-gates.md → tools/browser_check.py
- `Tarefa UX/CRO: Hierarquia de contato com WhatsApp e aviso de app de e-mail` --references--> `SiteTests`  [EXTRACTED]
  docs/superpowers/plans/2026-11-13-ux-cro-integrado.md → tools/test_site_tools.py
- `Tarefa Graphify: Extração híbrida, curadoria de comunidades e teste de saúde` --references--> `Site`  [EXTRACTED]
  docs/superpowers/plans/2026-11-16-graphify-improvement.md → tools/site_tools.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Ecossistema de Publicação, Scripts e Ativos Visuais do Frontend M2R** — frontend_index_m2r_tecnologias, frontend_index_hero_circuitos_svg, frontend_robots_txt, frontend_assets_img_logo_png, frontend_assets_img_m2r_png, frontend_assets_img_og_image_png, frontend_assets_js_script, frontend_assets_js_hero_circuits, tools_generate_sitemap, tools_version_assets, tools_site_tools_site, vercel [EXTRACTED 1.00]
- **Ciclo de Especificações e Planos Superpowers M2R (PR #21 → Quality Gates → UX/CRO → Graphify)** — spec_pr21_remediation_design, plan_pr21_remediation_plano, spec_quality_gates_design, plan_quality_gates_plano, spec_ux_cro_integrado_design, plan_ux_cro_integrado_plano, spec_graphify_improvement_design, plan_graphify_improvement_plano [EXTRACTED 1.00]
- **Governança de Segurança, Endurecimento do Backend/Deploy e Validação Automatizada no CI** — docs_auditoria_seguranca_2026_11_04_relatorio, docs_auditoria_seguranca_2026_11_04_controles_remediados, readme_pipeline_validacao_qualidade, readme_backend_flask_opcional_contrato, backend_requirements_dependencias_runtime, requirements_dev_ferramentas_teste_auditoria, changelog_release_1_0_5_1_0_6_endurecimento_seguranca, backend_app, vercel, github_workflows_validate_site [EXTRACTED 1.00]
- **Jornada de Conteúdo, Serviços e Conversão da M2R Tecnologias** — frontend_index_m2r_tecnologias, frontend_pages_servicos_catalogo_servicos, frontend_pages_projetos_portfolio, frontend_pages_projetos_m2r_server_estudo_caso, frontend_pages_blog_blog_insights, frontend_pages_blog_automacao_pequenos_negocios, frontend_pages_blog_organizacao_processos_digitais, frontend_pages_blog_site_profissional_marca, frontend_pages_sobre_institucional, frontend_pages_contato_fluxo_contato [EXTRACTED 1.00]
- **Malha de Verificação Automatizada Governada pelas Specs (Site, Playwright, Axe, Lighthouse, Hashes)** — plan_pr21_remediation_testes_regressao, plan_quality_gates_auditoria_axe_ci, plan_quality_gates_relatorio_lighthouse, plan_ux_cro_integrado_evidencias_auditoria, tools_site_tools_site, tools_browser_check, tools_lighthouse_check, tools_version_assets [EXTRACTED 1.00]
- **Qualidade de Experiência do Usuário (UX/CRO), Responsividade e Acessibilidade do Frontend** — docs_auditoria_2026_10_17_relatorio_corretivo, docs_auditoria_2026_10_17_correcoes_p0_p1_p2, docs_auditoria_auditoria_ux_cro_diagnostico, docs_auditoria_auditoria_ux_cro_cinco_prioridades, readme_fluxo_contato_mailto_whatsapp, frontend_assets_js_script, frontend_assets_js_hero_circuits, tools_browser_check [EXTRACTED 1.00]
- **Sistema compartilhado dos Heroes: arte, runtime, páginas e verificações** — frontend_assets_img_hero_circuits_svg, frontend_assets_js_hero_system, frontend_assets_js_hero_circuits, spec_shared_hero_system_design, plan_shared_hero_system_plano, tools_hero_check, tools_browser_check, frontend_404_pagina_erro [EXTRACTED 1.00]

## Communities (23 total, 9 thin omitted)

### Community 0 - "Backend Flask, deploy e documentação"
Cohesion: 0.06
Nodes (18): add_security_headers(), assign_request_id(), has_header_break(), healthz(), home(), ratelimit_handler(), request_too_large_handler(), status() (+10 more)

### Community 1 - "Verificação em navegador e acessibilidade"
Cohesion: 0.08
Nodes (21): Tarefa PR #21: Testes de regressão de Hero responsivo, breadcrumbs e CSP, Pipeline de Verificações de Qualidade, Acessibilidade (axe-core) e Lighthouse, Dependências Python de Desenvolvimento e Auditoria (pip-audit, Playwright, pytest), check_accessibility(), check_first_tab_is_skip_link(), check_fixed_control_overlaps(), check_hero_motion(), check_home_motion_brand_clearance() (+13 more)

### Community 2 - "Testes do backend Flask"
Cohesion: 0.12
Nodes (32): clean_field(), validate_app_environment(), validate_frontend_origin(), validate_proxy_hops(), validate_rate_limit_storage(), client(), test_api_status_returns_service_status(), test_app_environment_rejects_unknown_values() (+24 more)

### Community 3 - "Validação dos Heroes no navegador"
Cohesion: 0.09
Nodes (18): boxes_overlap(), chromium_launch_options(), assert_static_usable(), behavior_checks(), breadcrumb_checks(), contrast_ratio(), fixed_overlay_check(), html_routes() (+10 more)

### Community 4 - "Medição com Lighthouse"
Cohesion: 0.09
Nodes (10): build_parser(), extract_lab_metrics(), find_chrome(), format_lab_metrics(), lighthouse_binary_path(), lighthouse_output_path(), main(), summarize_lighthouse() (+2 more)

### Community 5 - "Páginas do site e sistema de Heroes"
Cohesion: 0.16
Nodes (29): Captura antiga (Blog), anterior aos Heroes com circuitos, Captura antiga (Home), anterior aos Heroes com circuitos, Captura antiga (Projetos), anterior aos Heroes com circuitos, Página de erro 404 (frontend/404.html), Foto do Fundador 400w (Eu_fundador-400.webp), Foto do Fundador 640w (Eu_fundador-640.webp), Foto do Fundador 900w (Eu_fundador-900.webp), Foto Social do Fundador Open Graph (Eu_fundador-social.jpg) (+21 more)

### Community 6 - "Interações dos circuitos da Home"
Cohesion: 0.11
Nodes (22): Avaliação das 12 Leis de UX (Jakob, Hick, Fitts, Miller, Von Restorff, Tesler, Estética-Usabilidade), Auditoria Profissional de UX, UI e Conversão (CRO) de 13/11/2026, buildHomeEffects(), createLayers(), defaultTip(), draw(), energize(), frame() (+14 more)

### Community 7 - "Pipeline de CI e quality gates"
Cohesion: 0.07
Nodes (29): jobs, validate, name, on, pull_request, push, permissions, contents (+21 more)

### Community 9 - "Sitemap e versionamento de assets"
Cohesion: 0.08
Nodes (20): Diretivas de Indexação e Sitemap (robots.txt), Tarefa PR #21: Fusão da main, override CSS .home-hero e hashes, Plano: Remediação do PR #21 (2026-11-08), Spec: Remediação do PR #21 (2026-11-08), buildSitemap(), CHECK_MODE, dates, destinationToFile() (+12 more)

### Community 10 - "Auditoria de HTML e UX/CRO"
Cohesion: 0.16
Nodes (6): Tarefa UX/CRO: Arquivamento de evidências responsivas, axe e Lighthouse, Tarefa UX/CRO: Hierarquia de contato com WhatsApp e aviso de app de e-mail, Tarefa UX/CRO: Clareza da oferta na Home e âncoras de serviços, Plano: Implementação de UX/CRO Integrado (2026-11-13), Document, Site

### Community 12 - "Testes dos Heroes internos"
Cohesion: 0.24
Nodes (7): baseline(), hero_content(), outside(), test_all_hero_routes_use_shared_system_contract(), test_home_video_is_preserved(), test_internal_variants_keep_their_original_content(), test_shared_svg_is_the_single_circuit_source_and_fallback()

### Community 13 - "Configuração do Dependabot"
Cohesion: 0.14
Nodes (13): prefix, day, interval, time, timezone, updates, commit-message, directory (+5 more)

### Community 14 - "Dependências Node e melhoria do Graphify"
Cohesion: 0.22
Nodes (9): devDependencies, axe-core@4.14.0, lighthouse@13.6.0, Tarefa Graphify: Higiene do corpus (.graphifyignore e .graphifyrc), Plano: Melhoria do Graphify M2R (2026-11-16), Tarefa Graphify: Extração híbrida, curadoria de comunidades e teste de saúde, axe-core, lighthouse (+1 more)

### Community 21 - "Servidor HTTP de teste"
Cohesion: 0.83
Nodes (4): handler_for(), do_GET(), do_HEAD(), respond()

## Knowledge Gaps
- **11 isolated node(s):** `Avaliação das 12 Leis de UX (Jakob, Hick, Fitts, Miller, Von Restorff, Tesler, Estética-Usabilidade)`, `Diretivas de Indexação e Sitemap (robots.txt)`, `Foto Social do Fundador Open Graph (Eu_fundador-social.jpg)`, `Banner de Compartilhamento Social (og-image.png)`, `Logotipo Horizontal M2R Tecnologias (m2r.png)` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 194 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Pipeline de Verificações de Qualidade, Acessibilidade (axe-core) e Lighthouse` connect `Verificação em navegador e acessibilidade` to `Backend Flask, deploy e documentação`, `Medição com Lighthouse`, `Pipeline de CI e quality gates`, `Sitemap e versionamento de assets`, `Ferramentas e imports compartilhados`, `Configuração do Dependabot`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **What connects `Avaliação das 12 Leis de UX (Jakob, Hick, Fitts, Miller, Von Restorff, Tesler, Estética-Usabilidade)`, `Diretivas de Indexação e Sitemap (robots.txt)`, `Foto Social do Fundador Open Graph (Eu_fundador-social.jpg)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Backend Flask, deploy e documentação` be split into smaller, more focused modules?**
  _Cohesion score 0.06312292358803986 - nodes in this community are weakly interconnected._
- **Why does `SiteTests` connect `Testes estruturais do site` to `Verificação em navegador e acessibilidade`, `Auditoria de HTML e UX/CRO`, `Ferramentas e imports compartilhados`, `Páginas do site e sistema de Heroes`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Should `Verificação em navegador e acessibilidade` be split into smaller, more focused modules?**
  _Cohesion score 0.07641196013289037 - nodes in this community are weakly interconnected._
- **Why does `Página Inicial M2R Tecnologias (index.html)` connect `Páginas do site e sistema de Heroes` to `Testes estruturais do site`, `Sitemap e versionamento de assets`, `Auditoria de HTML e UX/CRO`, `Interações dos circuitos da Home`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Should `Testes do backend Flask` be split into smaller, more focused modules?**
  _Cohesion score 0.11561561561561562 - nodes in this community are weakly interconnected._