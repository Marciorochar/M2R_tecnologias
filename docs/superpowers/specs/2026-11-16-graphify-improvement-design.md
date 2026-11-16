# Melhoria do Grafo de Conhecimento (Graphify) — design

## Objetivo

Tornar o grafo de conhecimento (`graphify`) do repositório M2R Tecnologias limpo, completo, versionável e auditável: eliminar ruídos de artefatos locais, restaurar a camada semântica sobre as páginas HTML e documentos institucionais, garantir rótulos estáveis em português para as comunidades e validar a saúde estrutural do grafo.

## Diagnóstico atual (16/11/2026)

1. **Poluição do corpus por artefatos temporários:** diretórios não rastreados como `.playwright-mcp/`, capturas de auditoria (`docs/auditoria/*.png`, `.xlsx`) e backups datados dentro de `graphify-out/YYYY-MM-DD/` entram no manifesto ou inflam o diretório de saída sem acrescentar valor arquitetural ao grafo do código e das páginas.
2. **Perda da camada semântica (HTML e hiperarestas):** a execução de `graphify update` (modo CLI puramente AST/estrutural) reconstrói o grafo apenas a partir de código e cabeçalhos Markdown (417 nós, 562 arestas, 0 hiperarestas), descartando os nós semânticos das 12 páginas HTML do `frontend/` e as 5 hiperarestas de jornada do usuário que existiam na extração completa.
3. **Deriva de rótulos de comunidades:** quando o algoritmo Leiden/Louvain re-clusteriza após adição de arquivos, as assinaturas em `.graphify_labels.json.sig` invalidam parte dos nomes curados e o fallback de hub renomeia comunidades com identificadores crus (`with`, `updates`, `Review Focus`, `site_tools.py`).
4. **Arquivos não classificados e desconexão doc ↔ código:** `frontend/assets/css/style.css` e `sitemap.xml` aparecem como não classificados; planos em `docs/superpowers/` e auditorias em `docs/` formam componentes conexos isolados quando não referenciam explicitamente os símbolos ou caminhos de arquivo que modificam.
5. **Política de versionamento indefinida:** `graphify-out/` está inteiramente não rastreado (`??`), misturando caches voláteis (`cache/`, `.graphify_analysis.json`, backups datados) com artefatos úteis de documentação e consulta (`GRAPH_REPORT.md`, `graph.json`, `.graphify_labels.json`).

## Escopo

- Criar `.graphifyignore` na raiz para excluir artefatos de execução e mídia binária pesada (`.playwright-mcp/`, `test-results/`, `playwright-report/`, `docs/auditoria/*.png`, `docs/auditoria/*.xlsx`, `frontend/assets/video/`), mantendo código, páginas HTML, especificações e documentação arquitetural.
- Criar `.graphifyrc` com padrões de projeto (`query_budget=3000`, `query_depth=3`, `viz_node_limit=1000`).
- Definir no `.gitignore` a separação entre artefatos efêmeros do Graphify (`graphify-out/cache/`, `graphify-out/20*/`, `graphify-out/.graphify_*`, exceto `.graphify_labels.json`) e artefatos opcionais de leitura/curadoria.
- Executar o pipeline completo (AST + extração semântica sobre páginas HTML e documentos) somente sobre uma árvore Git limpa (sem marcadores de conflito `<<<<<<<`).
- Curar `.graphify_labels.json` em português claro e validar integridade com `graphify.diagnostics` (zero arestas pendentes, órfãs ou auto-loops) e um teste leve em `tools/test_graphify_health.py`.

## Não escopo

- Alterar o código de produção do `frontend/`, `backend/` ou regras de deploy na Vercel/Render.
- Exigir chaves de API pagas no GitHub Actions ou bloquear o CI por execução de LLM.
- Modificar o worktree original enquanto houver arquivos `UU` não resolvidos (seguir a regra de isolamento ou aguardar resolução do merge).

## Abordagens consideradas

1. **Apenas `graphify update` via CLI / git hook (descartada como solução única):** rápida e gratuita, mas apaga ou ignora relações semânticas das páginas HTML estáticas, que são o núcleo do site M2R.
2. **Híbrida curada — escolhida:** `.graphifyignore` + `.graphifyrc` para higiene do corpus, extração híbrida (AST + semântica via subagentes/agente local sobre HTML e docs), `.graphify_labels.json` versionado em português e verificação determinística de saúde do `graph.json`.
3. **Graphify no CI a cada push com LLM:** custo de tokens desnecessário para um corpus de ~25–35 mil palavras que cabe em janela de contexto.
