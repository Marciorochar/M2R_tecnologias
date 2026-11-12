# Graph Report - Meu Site - M2R  (2026-11-08)

## Corpus Check
- Corpus is ~19,878 words - fits in a single context window. You may not need a graph.

## Summary
- 262 nodes · 361 edges · 17 communities (11 shown, 6 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.89)
- Token cost: 25,800 input · 10,200 output

## Community Hubs (Navigation)
- Validação do Backend
- Auditoria de HTML
- Sitemap e Robots
- Rotas e Segurança Flask
- Geração do Sitemap
- Conteúdo Institucional
- CI do GitHub
- Testes do Site
- Arquitetura e Deploy
- Dependabot
- Páginas e Serviços
- Configuração Vercel
- Identidade Social
- Página 404
- Retratos Responsivos
- Retratos Sociais

## God Nodes (most connected - your core abstractions)
1. `SiteTests` - 27 edges
2. `client()` - 18 edges
3. `Site` - 16 edges
4. `Document` - 12 edges
5. `handler_for()` - 8 edges
6. `updates` - 7 edges
7. `schedule` - 5 edges
8. `steps` - 5 edges
9. `validate_rate_limit_storage()` - 5 edges
10. `validate_contact()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Página não encontrada` --semantically_similar_to--> `Página 404 do frontend`  [INFERRED] [semantically similar]
  404.html → frontend/404.html
- `Frontend estático endurecido` --conceptually_related_to--> `Frontend estático publicado na Vercel`  [INFERRED]
  docs/auditoria-seguranca-2026-11-04.md → README.md
- `Descoberta do sitemap por robôs` --conceptually_related_to--> `Frontend estático publicado na Vercel`  [INFERRED]
  frontend/robots.txt → README.md
- `Contato por mailto e WhatsApp` --implements--> `Preparação de e-mail no dispositivo do visitante`  [INFERRED]
  README.md → frontend/pages/contato.html
- `Acessibilidade progressiva e fallbacks` --conceptually_related_to--> `M2R Tecnologias`  [INFERRED]
  docs/auditoria-2026-10-17.md → frontend/index.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Ecossistema de publicação do site M2R** — readme_frontend_estatico_vercel, frontend_index_m2r_tecnologias, frontend_robots_descoberta_sitemap, frontend_404_pagina_nao_encontrada [INFERRED 0.85]
- **Jornada de conteúdo, serviços e contato** — frontend_pages_blog_blog_insights, frontend_pages_servicos_catalogo_servicos, frontend_pages_contato_fluxo_contato [INFERRED 0.75]
- **Governança de segurança e validação** — docs_auditoria_seguranca_2026_11_04_auditoria_seguranca, readme_validacao_continua, requirements_dev_playwright_pip_audit_pytest, backend_requirements_flask_stack [INFERRED 0.85]
- **Identidade Visual M2R** — docs_screenshots_blog_blog_page, docs_screenshots_home_home_page, docs_screenshots_projetos_projects_page [INFERRED 0.95]

## Communities (17 total, 6 thin omitted)

### Community 0 - "Validação do Backend"
Cohesion: 0.11
Nodes (32): clean_field(), validate_app_environment(), validate_frontend_origin(), validate_proxy_hops(), validate_rate_limit_storage(), client(), test_api_status_returns_service_status(), test_app_environment_rejects_unknown_values() (+24 more)

### Community 3 - "Rotas e Segurança Flask"
Cohesion: 0.10
Nodes (9): add_security_headers(), assign_request_id(), has_header_break(), healthz(), home(), ratelimit_handler(), request_too_large_handler(), status() (+1 more)

### Community 4 - "Geração do Sitemap"
Cohesion: 0.10
Nodes (17): buildSitemap(), CHECK_MODE, dates, destinationToFile(), formatPath(), fs, generated, path (+9 more)

### Community 5 - "Conteúdo Institucional"
Cohesion: 0.10
Nodes (14): Auditoria corretiva de 17 de outubro de 2026, M2R Tecnologias, Soluções digitais sob medida, Tecnologia e automação para pequenos negócios, Blog e insights da M2R, Projetos digitais e organização de processos, Como um site profissional fortalece uma marca, Perfil auxiliar do fundador (+6 more)

### Community 6 - "CI do GitHub"
Cohesion: 0.10
Nodes (20): jobs, validate, name, on, pull_request, push, permissions, contents (+12 more)

### Community 7 - "Testes do Site"
Cohesion: 0.18
Nodes (9): check_layout(), check_menu(), check_site(), main(), handler_for(), do_GET(), do_HEAD(), respond() (+1 more)

### Community 8 - "Arquitetura e Deploy"
Cohesion: 0.11
Nodes (15): Dependências de runtime do backend, Stack Flask com CORS, rate limiting e Redis, Pendência do backend legado no Render, Evolução do site M2R Tecnologias, Auditoria de segurança de 4 de novembro de 2026, Backend legado ativo no Render, Frontend estático endurecido, Fluxo de contato da M2R (+7 more)

### Community 9 - "Dependabot"
Cohesion: 0.14
Nodes (13): prefix, day, interval, time, timezone, updates, commit-message, directory (+5 more)

### Community 10 - "Páginas e Serviços"
Cohesion: 0.33
Nodes (7): Categorias de Conteúdo do Blog, Página do Blog M2R, Serviços Digitais da M2R, Página Inicial M2R Tecnologias, Ambientes Conectados, M2R Server, Página de Projetos M2R

### Community 11 - "Configuração Vercel"
Cohesion: 0.40
Nodes (4): headers, redirects, rewrites, routes

### Community 12 - "Identidade Social"
Cohesion: 0.67
Nodes (4): Símbolo da M2R Tecnologias, Logotipo horizontal da M2R Tecnologias, Cartão social da M2R Tecnologias, Soluções digitais e desenvolvimento web sob medida

## Knowledge Gaps
- **16 isolated node(s):** `Página não encontrada`, `Evolução do site M2R Tecnologias`, `Dependências de runtime do backend`, `Página 404 do frontend`, `Fluxo de contato da M2R` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 108 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SiteTests` connect `Auditoria de HTML` to `Sitemap e Robots`, `Testes do Site`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `SiteTests` (e.g. with `Document` and `Site`) actually correct?**
  _`SiteTests` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Página não encontrada`, `Evolução do site M2R Tecnologias`, `Dependências de runtime do backend` to the rest of the system?**
  _16 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Validação do Backend` be split into smaller, more focused modules?**
  _Cohesion score 0.11095305832147938 - nodes in this community are weakly interconnected._
- **Why does `Site` connect `Testes do Site` to `Auditoria de HTML`, `Sitemap e Robots`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Should `Auditoria de HTML` be split into smaller, more focused modules?**
  _Cohesion score 0.07862903225806452 - nodes in this community are weakly interconnected._
- **Why does `Document` connect `Auditoria de HTML` to `Sitemap e Robots`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._