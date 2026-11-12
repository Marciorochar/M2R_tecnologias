# 06 — Recomendações priorizadas

As recomendações abaixo não alteram configuração ou código; são propostas para uma execução futura.

## P1 — Garantir proveniência de cada análise Graphify

1. Registre versão do executável, comando e opções, commit, estado dirty/clean e escopo dos arquivos.
2. Gere para um diretório de saída dedicado escolhido para a execução, sem sobrescrever snapshots históricos.
3. Inclua hash/manifest das fontes e marque explicitamente arquivos ignorados, não classificados e sem extração semântica.
4. Ao documentar comparação, alinhe o modo de extração e compare identidade de nós/arestas, não totais brutos.

## P2 — Reduzir ruído e ampliar cobertura dos vínculos reais

1. Criar/revisar `.graphifyignore` para excluir `.git/`, ambientes Python, `node_modules/`, caches, relatórios e capturas de tela; preservar HTML, JavaScript, Python, JSON de rotas, workflows e manifests pertinentes.
2. Fazer uma passagem estrutural `--code-only` para arquitetura reproduzível sem inferência documental; manter uma passagem documental separada se as relações entre decisões e código forem necessárias.
3. Consultar nós por caminho/arquivo e tipo de relação; aumentar `--budget` ou reduzir a consulta quando houver truncamento. Não usar resultados por palavra-chave como caminho de execução validado.
4. Cruzar HTML (`script`, `link`, `href`), DOM IDs/classes e `vercel.json` com o grafo para capturar dependências não baseadas em import.
5. Investigar a auto-aresta do grafo recente pelo tipo, origem e destino antes de concluir que há ciclo; diferenciar self-loop de ciclo de importação.

## P2 — Tornar rastreável o limite frontend/backend

1. Manter documentado que o formulário público usa `mailto:`/WhatsApp e que Flask `/api/contato` valida um payload separado.
2. Se o backend estiver ativo, confirmar com o responsável sua origem pública, storage Redis, saltos de proxy e política CORS por ambiente; não inferir isso do código ou de deployment estático.
3. Se houver intenção de integrar o formulário com a API, tratar como mudança funcional futura com desenho, testes e revisão de privacidade separados.

## P3 — Controlar o crescimento de módulos compartilhados

- Acompanhar responsabilidades e contratos DOM em `script.js` e `site_tools.py`. Uma extração de módulo só se justifica se surgir mudança independente, acoplamento difícil de testar ou aumento claro de complexidade; os hubs Graphify atuais não bastam para decidir.

## Fluxo Codex sugerido

1. Ler o escopo e as exclusões do projeto.
2. Registrar `git rev-parse HEAD` e `git status --short` sem incluir valores de ambiente/segredos.
3. Executar extração Graphify em destino explicitamente escolhido, usando configuração de exclusões revista antes da execução.
4. Consultar hubs, rotas e fluxos por arquivo; guardar a evidência textual com o snapshot.
5. Confirmar manualmente arestas críticas nos arquivos de origem e marcar inferências/hipóteses.
6. Atualizar esta documentação somente após revisão de diff, preservando saída Graphify e arquivos de trabalho anteriores.

Nenhuma alteração de `.graphifyignore`, hook, CI, configuração Codex ou diretório de saída foi aplicada nesta análise.
