# 01 — Estrutura, tecnologias e componentes

## Visão do repositório

| Área | Conteúdo observado | Papel |
| --- | --- | --- |
| `frontend/` | HTML multipágina, CSS compartilhado, JavaScript e imagens | Site estático servido sob rotas limpas |
| `backend/` | `app.py`, testes Flask e requirements próprios | API opcional para status, saúde e validação de contato |
| `tools/` | Ferramentas Python/Node e testes | Servidor local compatível com regras estáticas, análise de links/HTML, browser, Lighthouse, sitemap e versionamento de assets |
| `.github/workflows/` | `validate-site.yml` | Pipeline de validação automatizada e artefatos |
| `vercel.json` | Headers, rewrites e rotas | Configuração da publicação estática |
| `docs/` | Auditorias, screenshots, planos e especificações | Documentação e evidência de projeto |
| `package.json` / lockfile | `axe-core` e `lighthouse` como dependências de desenvolvimento | Ferramentas de qualidade no navegador |
| `requirements-dev.txt`, `backend/requirements.txt` | Dependências Python separadas por ambiente | Testes/ferramentas e backend |

O README do projeto descreve HTML5, CSS3 e JavaScript sem framework no frontend, deploy estático na Vercel e Flask opcional. A árvore publicada e a rota 404 são organizadas em torno dos arquivos HTML em `frontend/` e de `vercel.json`.

## Entradas e componentes principais

- `frontend/index.html`: página inicial; carrega `script.js` e, apenas nela, `hero-circuits.js`.
- `frontend/pages/*.html` e subpastas: páginas de serviços, projetos, blog, sobre, fundador e contato. Carregam CSS comum e o script global.
- `frontend/assets/css/style.css`: camada visual comum e regras por página.
- `frontend/assets/js/script.js`: inicialização no `DOMContentLoaded`, navegação, observação de seções, preferências de movimento e comportamento de contato.
- `frontend/assets/js/hero-circuits.js`: animação SVG interativa da página inicial, com pausa, preferência por movimento reduzido, visibilidade e interseção.
- `backend/app.py`: aplicação Flask e rotas `/`, `/healthz`, `/api/status` e `/api/contato`.
- `tools/site_tools.py`: classes `Document` e `Site`, resolução de URLs/arquivos segundo regras Vercel, verificações e servidor local.
- `tools/browser_check.py` e `tools/lighthouse_check.py`: verificações com navegador/Chromium e relatório Lighthouse.
- `tools/generate-sitemap.js` e `tools/version-assets.js`: geração de sitemap a partir das rotas e versionamento por conteúdo de assets.
- `backend/test_app.py`, `tools/test_*.py`: testes de backend, ferramentas, sitemap, acessibilidade e Lighthouse.

## Dependências externas declaradas

- Frontend publicado: sem framework de execução declarado.
- Node: `axe-core` 4.14.0 e `lighthouse` 13.6.0, em `package.json`.
- Python: dependências do backend Flask em `backend/requirements.txt`; ferramentas/testes em `requirements-dev.txt`.
- GitHub Actions e Vercel são integrações externas declaradas na configuração. O estado/versão efetiva de serviços remotos não foi verificado.

## Entradas de execução

1. Navegador → `frontend/index.html` ou página resolvida por `vercel.json`.
2. CI → steps do workflow `.github/workflows/validate-site.yml`.
3. Backend, quando iniciado separadamente → `backend/app.py`; o arquivo chama `app.run` apenas quando executado diretamente.
4. Ferramentas locais → scripts Python/Node em `tools/`.

**Evidência principal:** `README.md`; `package.json`; `vercel.json`; `backend/app.py:174-233`; `tools/site_tools.py:17-173`; `tools/browser_check.py:16-206`; `tools/lighthouse_check.py:24-...`; `tools/generate-sitemap.js`; `.github/workflows/validate-site.yml`.
