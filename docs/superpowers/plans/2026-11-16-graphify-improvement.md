# Melhoria do Graphify M2R — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Higienizar o corpus, restaurar a camada semântica (HTML + documentos + hiperarestas), estabilizar os rótulos das comunidades em português e automatizar a verificação de integridade do grafo em `graphify-out/`.

**Architecture:** Configurar `.graphifyignore` e `.graphifyrc` na raiz para filtrar artefatos efêmeros de navegador/mídia, executar a extração híbrida (AST para Python/JS/YAML/JSON + semântica para HTML/Markdown) sobre árvore sem conflitos de merge, persistir rótulos curados em `.graphify_labels.json` e validar o grafo resultante com `graphify.diagnostics` e `unittest`.

**Tech Stack:** Python 3.12+, `graphifyy` 0.9.104 (`detect`, `extract`, `build`, `cluster`, `diagnostics`), `unittest`.

**Spec:** `docs/superpowers/specs/2026-11-16-graphify-improvement-design.md`

## Global Constraints

- Não executar extração semântica sobre arquivos HTML/CSS enquanto contiverem marcadores de conflito (`<<<<<<<`, `=======`, `>>>>>>>`).
- Não exigir chave de API externa (`GEMINI_API_KEY` é opcional; usar extração local ou subagentes quando ausente).
- Não versionar caches internos (`graphify-out/cache/`, backups datados `graphify-out/20*/` ou arquivos temporários `.graphify_chunk_*.json`).
- Manter 100% dos rótulos de comunidade em português e descritivos (sem nomes de identificadores crus como `with` ou `updates`).

## Review Focus

- `detect()` não deve incluir arquivos de `.playwright-mcp/`, `test-results/`, vídeos `.webm` nem binários temporários de auditoria.
- Todos os 12 arquivos HTML públicos (`frontend/index.html`, `frontend/404.html`, `frontend/pages/**/*.html`) devem possuir nós representados no `graph.json`.
- `diagnose_extraction` deve reportar zero `dangling_endpoint_edges`, `missing_endpoint_edges` e `self_loop_edges`.
- Nenhuma comunidade em `GRAPH_REPORT.md` deve exibir placeholder `Community N` ou nome de token sintático (`with`, `updates`).

---

### Task 1: Pré-requisito de árvore limpa e higiene do corpus (`.graphifyignore`, `.graphifyrc`, `.gitignore`)

**Files:**
- Create: `.graphifyignore`
- Create: `.graphifyrc`
- Modify: `.gitignore`

- [x] **Step 1: Verificar ausência de marcadores de conflito nos arquivos do corpus**

Run: `git diff --check`
Expected: nenhuma linha com conflict marker nos arquivos HTML, CSS, JS, Python ou Markdown antes da extração completa.

- [x] **Step 2: Criar `.graphifyignore` e `.graphifyrc` na raiz**

Incluir em `.graphifyignore`:
```gitignore
.playwright-mcp/
test-results/
playwright-report/
frontend/assets/video/
docs/auditoria/*.png
docs/auditoria/*.xlsx
404.html
*.pdf
```
*(Nota: `404.html` na raiz é cópia legada de `frontend/404.html`; ignorá-lo evita o nó duplicado `Página não encontrada` vs `Página 404 do frontend`).*

Incluir em `.graphifyrc`:
```ini
viz_node_limit=1000
query_budget=3000
query_depth=3
```

- [x] **Step 3: Atualizar `.gitignore` para ignorar artefatos voláteis do Graphify**

Adicionar regras para ignorar `graphify-out/cache/`, `graphify-out/20*/`, `graphify-out/.graphify_*` (preservando `!graphify-out/.graphify_labels.json` caso o time decida versionar os rótulos).

- [x] **Step 4: Validar a detecção limpa do corpus**

Run: `python -c "from pathlib import Path; from graphify.detect import detect; r = detect(Path('.')); print(r['total_files'], r['total_words'])"`
Expected: zero arquivos vindos de `.playwright-mcp/` ou `docs/auditoria/*.xlsx`.

---

### Task 2: Extração híbrida completa (AST + Semântica para HTML e Docs)

**Files:**
- Generate: `graphify-out/.graphify_detect.json`, `graphify-out/.graphify_ast.json`, `graphify-out/.graphify_semantic.json`, `graphify-out/.graphify_extract.json`

- [x] **Step 1: Executar extração AST para todos os arquivos de código**

Run: `graphify.extract.extract()` sobre a lista `detect['files']['code']`.
Expected: `.graphify_ast.json` gerado com todos os módulos Python (`backend/`, `tools/`), scripts JS (`frontend/assets/js/`, `tools/`) e configs (`vercel.json`, `package.json`, `.github/`).

- [x] **Step 2: Executar extração semântica sobre páginas HTML e documentação**

Processar `detect['files']['document']` (páginas em `frontend/`, `README.md`, `CHANGELOG.md`, auditorias e specs em `docs/`), gerando nós de conceitos/páginas, arestas `references`/`implements` ligando documentos aos símbolos de código (`Site`, `check_accessibility`, `refreshAnimation`, rotas de serviço) e hiperarestas das jornadas do site.
Expected: `.graphify_semantic.json` contendo nós para todas as páginas HTML e hiperarestas do ecossistema M2R.

- [x] **Step 3: Mesclar AST + Semântica e verificar integridade (`diagnose_extraction`)**

Run: script de merge (Step 3 Part C + Step 4.5 da skill `graphify`).
Expected: `Graph health: OK (no dangling/missing/collapsed edges).`

---

### Task 3: Clusterização, curadoria de rótulos e geração de relatórios

**Files:**
- Modify: `graphify-out/.graphify_labels.json`
- Generate: `graphify-out/graph.json`, `graphify-out/GRAPH_REPORT.md`, `graphify-out/graph.html`, `graphify-out/manifest.json`

- [x] **Step 1: Construir o grafo e executar clusterização**

Run: `build_from_json` + `cluster` + `score_all` + `god_nodes` + `surprising_connections`.

- [x] **Step 2: Nomear todas as comunidades em português e atualizar `.graphify_labels.json` + `.sig`**

Revisar os membros de cada comunidade em `.graphify_analysis.json`, atribuir nomes claros em português (ex.: `Auditoria de HTML (site_tools)`, `Backend Flask e Testes`, `Hero de Circuitos e UX/CRO`, `Jornada de Páginas e Serviços`), regenerar `GRAPH_REPORT.md` e `graph.html` via `graphify cluster-only .` e remover backups datados temporários (`graphify-out/2026-*/`).

---

### Task 4: Teste automatizado de saúde do grafo

**Files:**
- Create: `tools/test_graphify_health.py`

- [x] **Step 1: Escrever teste validando o grafo quando `graphify-out/graph.json` existir**

Verificar em `tools/test_graphify_health.py`:
1. `.graphifyignore` e `.graphifyrc` existem e são válidos.
2. `graphify-out/graph.json` não contém nós apontando para `.playwright-mcp/` ou arquivos com marcadores de conflito.
3. Todas as comunidades possuem `community_name` preenchido, sem placeholders `Community \d+` e sem tokens crus (`with`, `updates`).
4. Não há arestas com `source` ou `target` inexistente em `nodes`.

- [x] **Step 2: Executar o teste e confirmar aprovação**

Run: `python -m unittest tools/test_graphify_health.py`
Expected: `OK`.
