# 05 — Graphify e validação cruzada

## Disponibilidade e execução observada

Graphify 0.9.104 está instalado em `C:\Users\marci\.local\bin\graphify.exe`. A extração atualizada foi executada em modo `--code-only` para `docs/graphify-analysis-2026-11-12/graphify-out/`, sem sobrescrever o grafo preexistente. Em seguida foram gerados relatório, diagnóstico estrutural, visualização HTML e call flow HTML. O `cluster-only` foi usado com `--no-label --no-viz`; por isso as comunidades ficaram sem rótulos semânticos automáticos.

## Resultados preservados

| Snapshot | Resultado | Observações |
| --- | --- | --- |
| `graphify-out/` | 346 nós, 491 arestas, 23 comunidades; 94% extraídas e 31 inferidas; report de 11/11 | Comunidades nomeadas e conteúdo documental inferido. Relatório raiz de saída em cluster-only em um arquivo alternativo. Histórico antigo; não atesta alterações locais de hoje. |
| `docs/graphify-analysis-2026-11-12/graphify-out/` | 267 nós, 418 arestas, 14 comunidades; 97% extraídas e 14 inferidas; report de 12/11 | Comunidades aparecem como `Community N`; report diz cluster-only e registra commit `904ac508`, igual ao HEAD observado. |

O diagnóstico read-only do grafo recente registrou uma auto-aresta, nenhum endpoint ausente, nenhuma aresta duplicada/colapsada, zero grupos de mesmo par e nenhuma falha ao materializar grafo não direcionado. O report declara “Import Cycles: None detected”. Auto-aresta não equivale automaticamente a ciclo de import; a relação concreta precisa ser interpretada pelo tipo e origem da aresta.

Graphify apontou `SiteTests` (32 arestas), `Site` (18), `client()` (18), `Document` (12) e `handler_for()` (10) entre os hubs. O código confirma reutilização de `Site` por checks, server local e verificações de browser/Lighthouse. Centralidade representa conexões no modelo, não complexidade cognitiva nem problema por si só.

## Divergências e correções de interpretação

| Saída Graphify | Validação direta | Interpretação corrigida |
| --- | --- | --- |
| Consultas por fluxo da home também retornaram `home()` e ferramentas Flask | `home()` é handler de `backend/app.py`; home do site é `frontend/index.html` | Colisão lexical de “home”; separar nó pelo arquivo e papel. |
| Consulta de Flask/contact trouxe `Site`, `Document`, browser checks e imports genéricos (`os`, `json`) | Os nós pertencem a ferramentas diferentes e imports comuns não são dependências semânticas do endpoint | BFS por palavras-chave serve para navegação; resultado truncado/ambíguo exige inspeção de origem. |
| `SiteTests` aparece como hub e o grafo infere uso de `Document`/`Site` | `tools/test_site_tools.py` instancia/usa `Site` e sua leitura de arquivos; a evidência de fonte é válida, embora a relação inferida não substitua a referência exata | Confirmar aresta no código; manter marcação INFERRED quando a ferramenta assim o classifica. |
| Relatório antigo sugere nodes isolados e comunidades de baixa coesão | HTML, rotas JSON, seletores DOM, eventos e criação dinâmica de SVG criam ligações não necessariamente modeladas como import/call | Não declarar componentes mortos nem recomendar split por score isolado. |
| As contagens dos snapshots divergem | Relatórios têm modos, datas, nomes de comunidade e metadados distintos | Não atribuir delta a mudanças de arquitetura sem execução equivalente e comparação por identidade de nó/aresta. |

## Comparação das capacidades

- **Graphify:** mapa de símbolos/arquivos, relações extraídas/inferidas, hubs, comunidades e navegação BFS; útil para orientar a leitura.
- **Busca/inspeção de fonte:** confirmou imports, handlers, chamadas, seletores e dependências estabelecidas por HTML/configuração, esclarecendo falsos positivos lexicais e inferências.
- **ECC security-and-hardening:** enquadrou fronteiras de entrada, CORS, tamanho/validação de campos, rate limit, proxy e segredos; a revisão ficou estática e não prova estado remoto ou segurança completa.
- **Reverse-engineer-anything / REA:** skill instalada, porém o próprio escopo exclui arquitetura de repositório-fonte completo; nenhum binário ou comportamento opaco exigiu REA.
- **ECC repo-scan:** o arquivo disponível é um ponteiro de instalação de scanner externo, não o scanner; não foi instalado nem executado.

## Limitações

- A extração foi feita com a árvore de trabalho suja. O campo `built_at_commit` registra `HEAD` (`904ac508`) como base, mas não registra hashes de conteúdo dos arquivos alterados; logo, o commit isolado não identifica de forma completa a revisão analisada.
- O modo `--code-only` omite documentos e imagens, e a instalação não classificou todos os formatos do projeto. O grafo atualizado não modela integralmente relações HTML/CSS/configuração sem inspeção adicional.
- A exportação HTML detectou sidecar de análise da raiz com 346 nós ao exportar o grafo de 267 nós. A visualização foi gerada no diretório isolado; centralidade e comunidades devem ser interpretadas a partir dos dados/report desse diretório, não do sidecar da raiz.
- Consultas BFS exibiram truncamento com orçamento limitado e misturaram símbolos de domínios distintos.
- Não foram rodados testes, análise dinâmica, scanners de segurança, auditoria de dependências ou checagens no deploy.
