# Análise de arquitetura e resultados do Graphify

**Projeto:** M2R Tecnologias  
**Data da análise:** 12/11/2026  
**Escopo:** leitura estática do repositório atual, consulta ao grafo preexistente, extração estrutural isolada com Graphify 0.9.104 e conferência manual das relações relevantes nas fontes. A análise foi feita sobre uma árvore de trabalho com alterações locais não commitadas; o identificador de commit no JSON não representa sozinho uma revisão limpa do conteúdo analisado.

## Resumo executivo

O caminho de publicação configurado no repositório é um site multipágina estático em HTML, CSS e JavaScript, servido pela Vercel a partir de `frontend/`. O `vercel.json` define as rotas públicas, cabeçalhos, redirects e rewrites para os arquivos estáticos. O projeto também contém um aplicativo Flask separado em `backend/`; as regras de deploy atuais não publicam nem conectam esse aplicativo às rotas do site. A implantação ativa não foi verificada nesta análise.

O fluxo de contato do site usa `mailto:` e WhatsApp. O formulário prepara uma mensagem para o aplicativo de e-mail do visitante. Embora o Flask exponha `POST /api/contato`, esse endpoint só valida dados e não faz parte do fluxo do formulário nem envia mensagens.

O CI combina verificações de configuração, dependências, sintaxe, HTML/CSS, navegador, acessibilidade, Lighthouse e testes Python. A cobertura reflete melhor o site estático e suas regras de publicação do que uma integração entre frontend e API, pois tal integração não está configurada neste repositório.

## Arquitetura observada

```text
Visitante
  └─ Vercel: rotas, redirects, headers e arquivos estáticos
       └─ frontend/
            ├─ páginas HTML
            ├─ assets/css/style.css
            └─ assets/js/script.js + hero-circuits.js

Ferramentas de desenvolvimento e CI
  ├─ tools/: servidor local, validação, sitemap, browser e Lighthouse
  ├─ .github/workflows/validate-site.yml
  └─ package.json / requirements-dev.txt

Aplicação Flask separada
  └─ backend/app.py: status e validação de contato, com configuração própria
```

| Área | Responsabilidade observada | Fontes principais |
| --- | --- | --- |
| Site publicado | Páginas, navegação, conteúdo e assets estáticos | `frontend/`, `404.html`, `vercel.json` |
| JavaScript do site | Menu, revelação de conteúdo e formulário `mailto:` | `frontend/assets/js/script.js` |
| Animação da home | Circuitos SVG, interação, pausa, visibilidade e movimento reduzido | `frontend/index.html`, `frontend/assets/js/hero-circuits.js` |
| Roteamento local e auditoria estática | Leitura de `vercel.json`, resolução de rotas/arquivos, links e CSP | `tools/site_tools.py` |
| Qualidade de browser | Chromium/Playwright, axe-core e Lighthouse | `tools/browser_check.py`, `tools/lighthouse_check.py` |
| Sitemap e cache de assets | Geração de sitemap e query hashes de CSS/JS | `tools/generate-sitemap.js`, `tools/version-assets.js` |
| API Flask | Health/status e validação limitada de contato | `backend/app.py` |
| Automação | Validações em push e pull request para `main`; pins de Actions | `.github/workflows/validate-site.yml`, `.github/dependabot.yml` |

### Fluxos principais

**Navegação web:** requisição à rota limpa → regra de rewrite em `vercel.json` → arquivo HTML em `frontend/` → CSS e JavaScript estáticos sob `/assets/`. Redirects tratam aliases e URLs antigas; cabeçalhos globais e específicos de assets são declarados na mesma configuração.

**Contato do visitante:** `/contato` entrega o formulário inicialmente oculto/desabilitado → `script.js` habilita a interface → validação no navegador e composição do texto → navegação `mailto:` ou cópia para a área de transferência. O envio final e a entrega dependem do cliente de e-mail do visitante. Não há envio assíncrono ao Flask nesse caminho.

**API separada:** `backend/app.py` valida ambiente, origem CORS, armazenamento do rate limit, limites e campos; as rotas incluem `/healthz`, `/api/status` e `/api/contato`. O endpoint de contato retorna validação bem-sucedida, não entrega de mensagem. A presença dessas rotas na fonte não comprova que estejam publicadas em produção.

## Stack e dependências

| Camada | Evidência no repositório |
| --- | --- |
| Frontend | HTML5, CSS e JavaScript sem framework no manifesto Node |
| Node para CI | Node.js 22; dependências diretas de desenvolvimento `axe-core@4.14.0` e `lighthouse@13.6.0` |
| Backend | Flask 3.1.3, Flask-Cors 6.0.5, Flask-Limiter 4.1.1, Gunicorn 26.2.0, python-dotenv 1.2.4 e Redis 8.1.0; pins exatos em `backend/requirements.txt` |
| Ferramentas Python | pip-audit 2.10.1, Playwright 1.64.1 e pytest 9.2.0; pins exatos em `requirements-dev.txt` |
| Python para CI | Python 3.12 |
| Deploy | Regras de site estático da Vercel em `vercel.json`, com allowlist em `.vercelignore` |
| Atualização de dependências | Dependabot semanal para pip, npm e GitHub Actions |

`package.json` não define scripts de build, teste ou runtime. O `package-lock.json` inclui dependências transitivas das ferramentas de Lighthouse e axe; a tabela lista somente dependências diretas identificadas no manifesto.

## Validação existente no CI

O workflow `validate-site.yml` roda em push e pull request contra `main`, com permissões de conteúdo somente leitura. O fluxo instala as ferramentas, executa testes unitários auxiliares, `npm audit`, validação de sintaxe JS, Chromium/Playwright, Lighthouse, testes e compilação Python, `pip-audit` e verificações estruturais de Vercel, sitemap, HTML/CSS e versionamento de assets. Relatórios Lighthouse e capturas do site são publicados como artefatos da execução.

O teste de browser registra erros JavaScript e percorre as rotas configuradas em várias larguras, mas isso continua sendo evidência de automação local/CI. Esta análise não executou o workflow, testes, Lighthouse, browser, nem verificou a implantação publicada.

## Atualização isolada do Graphify

Para preservar `graphify-out/` e todas as alterações locais já existentes, a nova extração foi gravada em `docs/graphify-analysis-2026-11-12/graphify-out/`.

| Medida | Grafo preexistente | Extração estrutural isolada |
| --- | ---: | ---: |
| Nós | 346 | 267 |
| Arestas | 491 | 418 |
| Comunidades | 23 | 14 |
| Escopo | Grafo existente com código e conteúdo documental | 18 arquivos classificados como código; modo `--code-only` |
| Extração reportada | 94% extraídas, 6% inferidas | 97% extraídas, 3% inferidas (14 arestas) |

Os totais não são diretamente comparáveis como mudança de qualidade: a extração nova exclui 28 documentos e 10 imagens e não executa extração semântica. Também houve 7 arquivos sem classificação de extensão ou shebang e dois diretórios ignorados (`.venv-audit/` e `test-results/`). CSS e outros formatos sem suporte estrutural não devem ser considerados cobertos só porque pertencem ao projeto.

O diagnóstico estrutural do grafo isolado encontrou 267 nós verificados, 418 arestas candidatas válidas, nenhum endpoint ausente, nenhuma aresta duplicada exata e nenhum grupo de arestas colapsado por endpoints repetidos. Detectou uma auto-relação, examinada manualmente abaixo. Esses resultados validam a estrutura serializada do grafo, não a semântica de todas as relações.

### Achados sobre a qualidade do grafo

1. **A auto-relação é um falso sinal de ciclo arquitetural.** O diagnóstico aponta `walkHtml()` chamando `walkHtml()` em `tools/version-assets.js`. A função percorre subdiretórios recursivamente para enumerar HTML; a auto-aresta representa recursão local intencional, não um ciclo entre módulos.
2. **“God nodes” priorizam ferramentas e testes.** `SiteTests`, `Site`, `client()` e `Document` estão entre os símbolos de maior grau. Isso é útil para localizar a infraestrutura de validação, mas não equivale a centralidade de domínio no site. Nomes genéricos como `main()` e `with` também reduzem a utilidade de um ranking sem inspeção do arquivo de origem.
3. **Arestas inferidas precisam de revisão.** Na extração nova, 14 das 418 arestas foram marcadas `INFERRED`; elas não devem ser citadas como dependências confirmadas sem leitura do trecho de origem. Arestas de callback/argumentos e relações entre testes e implementação merecem atenção especial.
4. **Comunidades são agrupamentos, não limites de implantação.** O grafo estrutural deixa as comunidades como `Community N` porque o agrupamento foi executado com `--no-label`, sem nomenclatura automática. Os nomes funcionais da tabela de arquitetura acima foram atribuídos por comparação com os caminhos e fontes, não pelo Graphify.
5. **O grafo de código não modela as rotas de produto de ponta a ponta.** HTML e CSS foram excluídos no modo `--code-only`; por isso, não use esse grafo para provar qual script uma página carrega, qual rewrite serve uma rota ou se o backend atende ao frontend. Essas ligações foram verificadas diretamente em `frontend/index.html`, `frontend/pages/contato.html` e `vercel.json`.
6. **A extração semântica permanece pendente.** O relatório anterior reúne relações com documentos, mas suas arestas inferidas devem ser tratadas como pistas. Esta análise não reextraiu semanticamente os documentos nem validou todas as relações entre documentação e implementação.

## Documentos do Graphify

- [Relatório estrutural](graphify-analysis-2026-11-12/graphify-out/GRAPH_REPORT.md)
- [Grafo JSON](graphify-analysis-2026-11-12/graphify-out/graph.json)
- [Visualização interativa](graphify-analysis-2026-11-12/graphify-out/graph.html)
- [Call flow HTML](graphify-analysis-2026-11-12/graphify-out/callflow.html)
- [Índice da análise ampliada em seis partes](architecture/README.md)

## Limites e próximos passos sugeridos

- Para cruzar documentação e código com mais confiança, rodar extração semântica dos documentos em saída separada e revisar cada aresta inferida contra sua passagem e fonte de código.
- Se CSS, HTML, arquivos de configuração e assets forem importantes para as consultas, registrar quais extensões a instalação atual do Graphify não indexa e analisá-las por ferramenta apropriada, em vez de extrapolar o grafo de código.
- Manter a fronteira entre site estático e Flask explícita na documentação/deploy. Antes de afirmar disponibilidade pública da API, confirmar separadamente a configuração do serviço de backend.
- Tratar os relatórios de Lighthouse, acessibilidade e navegador como evidência de uma execução datada; seus resultados não são inferidos pela análise estática.

## Procedimento reproduzível

Os comandos abaixo foram usados para gerar e inspecionar os artefatos isolados; a exportação HTML foi feita após a extração e o agrupamento:

```powershell
graphify extract . --code-only --out docs/graphify-analysis-2026-11-12 --max-workers 4
graphify cluster-only docs/graphify-analysis-2026-11-12 --no-label --no-viz
graphify diagnose multigraph --graph docs/graphify-analysis-2026-11-12/graphify-out/graph.json --json
graphify god-nodes --top 15 --graph docs/graphify-analysis-2026-11-12/graphify-out/graph.json --json
graphify export html --graph docs/graphify-analysis-2026-11-12/graphify-out/graph.json --node-limit 1000
graphify export callflow-html docs/graphify-analysis-2026-11-12 --output docs/graphify-analysis-2026-11-12/graphify-out/callflow.html
```

As comunidades ficaram sem nomes automáticos. A exportação HTML alertou que o sidecar de análise descoberto na raiz correspondia ao grafo antigo (346 nós), não ao grafo isolado (267); por isso os achados de centralidade foram conferidos no relatório do grafo novo e na fonte. Os arquivos `graph.json`, `GRAPH_REPORT.md` e as visualizações isoladas são derivados de código e devem ser regenerados após mudanças nas fontes.
