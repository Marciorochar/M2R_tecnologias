# 04 — Problemas confirmados e riscos potenciais

Esta revisão não encontrou prova de defeito funcional no código-fonte examinado. Os itens abaixo separam inconsistências comprovadas na documentação/análise de riscos de manutenção que precisam de decisão futura.

## Achados confirmados

### A-01 — Snapshot Graphify de 11/11 está desatualizado para o estado da revisão

- **Descrição:** o relatório antigo foi produzido em 11/11 e antecede o estado de trabalho atual; não deve ser tratado como inventário vigente.
- **Arquivo/localização:** `graphify-out/GRAPH_REPORT.md`, cabeçalho do relatório; `git status --short` mostrou alterações e arquivos novos no working tree.
- **Evidência:** o snapshot tem 346 nós e 491 arestas; há arquivos atualmente modificados. O relatório por si só não registra hash dos arquivos modificados. A animação `hero-circuits.js` já aparece no snapshot antigo, portanto não é citada como item omitido.
- **Impacto:** usar o grafo antigo como mapa atual pode omitir/remapear alterações locais.
- **Prioridade:** P1 para qualquer análise baseada no snapshot antigo; P3 para o projeto se o artefato for mantido apenas como histórico.
- **Recomendação:** gerar análise incremental/full em destino revisado e registrar commit, estado dirty, escopo, versão Graphify e hashes/manifests junto do relatório.

### A-02 — Há dois snapshots Graphify com bases de comparação diferentes

- **Descrição:** o snapshot histórico e o snapshot em `docs/graphify-analysis-2026-11-12/graphify-out/` diferem em contagem e metadados; o segundo mostra comunidades genéricas em cluster-only.
- **Arquivo/localização:** os dois `GRAPH_REPORT.md` e `manifest.json` citados.
- **Evidência:** 346/491 nós/arestas e 23 comunidades no histórico; 267/418 e 14 comunidades no relatório de 12/11. Um relatório anuncia nomes de comunidades e relações inferidas; o outro não nomeia comunidades. O grafo de 12/11 declara base `904ac508`, igual ao HEAD consultado.
- **Impacto:** comparar deltas como mudança de arquitetura seria inválido sem igualar escopo e modo de extração.
- **Prioridade:** P2 para análises comparativas.
- **Recomendação:** padronizar execução e registrar configurações; comparar nós/arestas por identidade e proveniência, não só totais.

## Riscos potenciais (não são defeitos comprovados)

### R-01 — Script compartilhado concentra rotinas de navegação, efeitos e contato

- **Descrição:** `script.js` é entrada global para todas as páginas e contém lógica de menu/scroll/observadores e preparação de contato.
- **Arquivo/localização:** `frontend/assets/js/script.js:1-309`; referências HTML nas páginas e `frontend/pages/contato.html:50`.
- **Evidência:** inicialização global e handlers condicionados a elementos encontrados no DOM.
- **Impacto:** crescimento pode aumentar acoplamento com markup e tornar regressões transversais mais difíceis de localizar.
- **Prioridade:** P3, risco de manutenção.
- **Recomendação:** manter contratos DOM explícitos e considerar módulos separados quando surgirem mudanças independentes ou testes unitários específicos.

### R-02 — Comportamento operacional do backend não foi verificado

- **Descrição:** o repositório exige HTTPS e storage Redis compartilhado em `production`, mas não se verificou o ambiente implantado, trusted proxy nem se o backend continua ativo externamente.
- **Arquivo/localização:** `backend/app.py:22-113`; instruções de backend no `README.md`.
- **Evidência:** validação de `APP_ENV`, `FRONTEND_URL`, `RATELIMIT_STORAGE_URI` e `TRUSTED_PROXY_HOPS`; o README declara que o backend não integra o deploy estático Vercel.
- **Impacto:** uma configuração externa divergente pode afetar CORS, limite de requisições ou interpretação de IP do cliente.
- **Prioridade:** P2 se a API estiver em uso; P3 caso contrário.
- **Recomendação:** confirmar ambiente e topologia do serviço no repositório/operador responsável antes de mudanças na API. Não assumir que a API recebe o formulário público.

### R-03 — Associações dinâmicas e markup podem não aparecer como dependências no grafo

- **Descrição:** referências por `<script>`, DOM, `vercel.json`, criação de SVG e listeners são mecanismos que não dependem de imports entre módulos.
- **Arquivo/localização:** HTML em `frontend/`, `frontend/assets/js/hero-circuits.js:35-...`, `vercel.json`, `tools/site_tools.py`.
- **Evidência:** análise direta confirmou carregamento de dois scripts só na página inicial, construção dinâmica de SVG e mapeamento de rotas por JSON.
- **Impacto:** um relatório centrado em arestas de código pode classificar indevidamente como isolados elementos acionados pelo browser/configuração.
- **Prioridade:** P2 para completude da análise; não é defeito do produto.
- **Recomendação:** cruzar Graphify com busca de referências em HTML/configuração e checks de links, rotas e DOM.

## Não confirmado nesta revisão

Não se confirma código morto, vulnerabilidade explorável, falha de acessibilidade, ciclo de importação, duplicação problemática ou erro de deploy. Os arquivos contêm testes e controles de segurança, mas eles não foram executados nesta análise.
