# Graph Report - Meu Site - M2R  (2026-11-11)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 346 nodes · 491 edges · 23 communities (16 shown, 7 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 31 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Auditoria de HTML (site_tools)
- Backend Flask e Testes
- Verificação no Navegador e Lighthouse
- Sitemap e Versionamento de Assets
- Rotas e Segurança Flask
- Arquitetura, Segurança e Deploy
- Conteúdo Institucional
- CI do GitHub
- Dependabot
- Testes do Sitemap
- Páginas e Serviços
- Identidade Visual
- Página 404
- Retratos Responsivos
- Retratos Sociais
- Remediação PR #21 (Task 3)
- Remediação PR #21 (Nota)
- Verificação de Acessibilidade (axe)
- Animação de Circuitos do Hero
- Plano de Quality Gates
- Design de Quality Gates
- Dependências Node (axe/Lighthouse)

## God Nodes (most connected - your core abstractions)
1. `SiteTests` - 32 edges
2. `Site` - 18 edges
3. `client()` - 18 edges
4. `Document` - 12 edges
5. `handler_for()` - 10 edges
6. `check_accessibility()` - 8 edges
7. `main()` - 8 edges
8. `with` - 8 edges
9. `check_site()` - 7 edges
10. `summarize_lighthouse()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Página não encontrada` --semantically_similar_to--> `Página 404 do frontend`  [INFERRED] [semantically similar]
  404.html → frontend/404.html
- `Frontend estático endurecido` --conceptually_related_to--> `Frontend estático publicado na Vercel`  [INFERRED]
  docs/auditoria-seguranca-2026-11-04.md → README.md
- `Plano de Remediação do PR #21` --conceptually_related_to--> `Frontend estático publicado na Vercel`  [INFERRED]
  docs/superpowers/plans/2026-11-08-pr21-remediation.md → README.md
- `Descoberta do sitemap por robôs` --conceptually_related_to--> `Frontend estático publicado na Vercel`  [INFERRED]
  frontend/robots.txt → README.md
- `Contato por mailto e WhatsApp` --implements--> `Preparação de e-mail no dispositivo do visitante`  [INFERRED]
  README.md → frontend/pages/contato.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fluxo Completo de Remediação do PR #21** — docs_superpowers_plans_2026_11_08_pr21_remediation_task_1_regression_tests, docs_superpowers_plans_2026_11_08_pr21_remediation_task_2_integrate_main_css, docs_superpowers_plans_2026_11_08_pr21_remediation_task_3_verification_pr [EXTRACTED 1.00]
- **Jornada de conteúdo, serviços e contato** — frontend_pages_blog_blog_insights, frontend_pages_servicos_catalogo_servicos, frontend_pages_contato_fluxo_contato [INFERRED 0.75]
- **Ecossistema de publicação do site M2R** — readme_frontend_estatico_vercel, frontend_index_m2r_tecnologias, frontend_robots_descoberta_sitemap, frontend_404_pagina_nao_encontrada [INFERRED 0.85]
- **Governança de segurança e validação** — docs_auditoria_seguranca_2026_11_04_auditoria_seguranca, readme_validacao_continua, requirements_dev_playwright_pip_audit_pytest, backend_requirements_flask_stack [INFERRED 0.85]
- **Identidade Visual M2R** — docs_screenshots_blog_blog_page, docs_screenshots_home_home_page, docs_screenshots_projetos_projects_page [INFERRED 0.95]

## Communities (23 total, 7 thin omitted)

### Community 0 - "Auditoria de HTML (site_tools)"
Cohesion: 0.06
Nodes (3): Document, Site, SiteTests

### Community 1 - "Backend Flask e Testes"
Cohesion: 0.12
Nodes (32): clean_field(), validate_app_environment(), validate_frontend_origin(), validate_proxy_hops(), validate_rate_limit_storage(), client(), test_api_status_returns_service_status(), test_app_environment_rejects_unknown_values() (+24 more)

### Community 2 - "Verificação no Navegador e Lighthouse"
Cohesion: 0.08
Nodes (15): Task 1: Testes de Regressão, Responsividade do Home Hero (<=900px), check_layout(), check_menu(), check_site(), chromium_launch_options(), main(), find_chrome() (+7 more)

### Community 3 - "Sitemap e Versionamento de Assets"
Cohesion: 0.08
Nodes (23): Task 2: Integrar Main e Corrigir CSS, Preservação de Breadcrumbs e CSP, buildSitemap(), CHECK_MODE, dates, destinationToFile(), formatPath(), fs (+15 more)

### Community 4 - "Rotas e Segurança Flask"
Cohesion: 0.10
Nodes (9): add_security_headers(), assign_request_id(), has_header_break(), healthz(), home(), ratelimit_handler(), request_too_large_handler(), status() (+1 more)

### Community 5 - "Arquitetura, Segurança e Deploy"
Cohesion: 0.10
Nodes (18): Dependências de runtime do backend, Stack Flask com CORS, rate limiting e Redis, Pendência do backend legado no Render, Evolução do site M2R Tecnologias, Auditoria de segurança de 4 de novembro de 2026, Backend legado ativo no Render, Frontend estático endurecido, Plano de Remediação do PR #21 (+10 more)

### Community 6 - "Conteúdo Institucional"
Cohesion: 0.10
Nodes (14): Auditoria corretiva de 17 de outubro de 2026, M2R Tecnologias, Soluções digitais sob medida, Tecnologia e automação para pequenos negócios, Blog e insights da M2R, Projetos digitais e organização de processos, Como um site profissional fortalece uma marca, Perfil auxiliar do fundador (+6 more)

### Community 7 - "CI do GitHub"
Cohesion: 0.08
Nodes (25): jobs, validate, name, on, pull_request, push, permissions, contents (+17 more)

### Community 8 - "Dependabot"
Cohesion: 0.14
Nodes (13): prefix, day, interval, time, timezone, updates, commit-message, directory (+5 more)

### Community 10 - "Páginas e Serviços"
Cohesion: 0.33
Nodes (7): Categorias de Conteúdo do Blog, Página do Blog M2R, Serviços Digitais da M2R, Página Inicial M2R Tecnologias, Ambientes Conectados, M2R Server, Página de Projetos M2R

### Community 11 - "Identidade Visual"
Cohesion: 0.67
Nodes (4): Símbolo da M2R Tecnologias, Logotipo horizontal da M2R Tecnologias, Cartão social da M2R Tecnologias, Soluções digitais e desenvolvimento web sob medida

### Community 18 - "Verificação de Acessibilidade (axe)"
Cohesion: 0.14
Nodes (4): check_accessibility(), serious_axe_violations(), AccessibilityCheckTests, FakePage

### Community 19 - "Animação de Circuitos do Hero"
Cohesion: 0.30
Nodes (9): defaultTip(), draw(), energize(), frame(), nearestOnPath(), onPointerLeave(), refreshAnimation(), svgPoint() (+1 more)

### Community 20 - "Plano de Quality Gates"
Cohesion: 0.29
Nodes (6): Global Constraints, Review Focus, Task 1: Dependências de desenvolvimento e axe-core, Task 2: Relatório Lighthouse, Task 3: Documentação e evidências visuais, Verificações de qualidade — Implementation Plan

### Community 21 - "Design de Quality Gates"
Cohesion: 0.29
Nodes (6): Abordagens consideradas, Escopo, Não escopo, Objetivo, Restrições e aprovação, Verificações de acessibilidade e desempenho — design

### Community 22 - "Dependências Node (axe/Lighthouse)"
Cohesion: 0.47
Nodes (5): devDependencies, axe-core@4.14.0, lighthouse@13.6.0, axe-core, lighthouse

## Knowledge Gaps
- **21 isolated node(s):** `Categorias de Conteúdo do Blog`, `M2R Server`, `Símbolo da M2R Tecnologias`, `Página não encontrada`, `Página 404 do frontend` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 145 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SiteTests` connect `Auditoria de HTML (site_tools)` to `Verificação no Navegador e Lighthouse`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `SiteTests` (e.g. with `Document` and `Site`) actually correct?**
  _`SiteTests` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Categorias de Conteúdo do Blog`, `M2R Server`, `Símbolo da M2R Tecnologias` to the rest of the system?**
  _21 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Auditoria de HTML (site_tools)` be split into smaller, more focused modules?**
  _Cohesion score 0.06464646464646465 - nodes in this community are weakly interconnected._
- **Why does `Site` connect `Auditoria de HTML (site_tools)` to `Verificação no Navegador e Lighthouse`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Should `Backend Flask e Testes` be split into smaller, more focused modules?**
  _Cohesion score 0.11561561561561562 - nodes in this community are weakly interconnected._
- **Why does `Document` connect `Auditoria de HTML (site_tools)` to `Verificação no Navegador e Lighthouse`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._