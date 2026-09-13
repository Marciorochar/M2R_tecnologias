# M2R Tecnologias

[![Deploy](https://img.shields.io/badge/deploy-Vercel-000000?style=for-the-badge&logo=vercel)](https://m2rtecnologias.vercel.app/)
[![Validar site](https://github.com/Marciorochar/M2R_tecnologias/actions/workflows/validate-site.yml/badge.svg)](https://github.com/Marciorochar/M2R_tecnologias/actions/workflows/validate-site.yml)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=000)](https://developer.mozilla.org/docs/Web/JavaScript)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)

Site institucional da M2R Tecnologias, criado para apresentar servicos, projetos, conteudos, informacoes sobre a empresa e canais de contato.

O projeto esta organizado para publicacao simples no GitHub e deploy estatico pela Vercel. O contato funciona sem backend, sem usuario, sem senha e sem SMTP, usando `mailto:` e WhatsApp.

## Visao geral

- Site multipaginas em HTML, CSS e JavaScript.
- Frontend estatico dentro da pasta `frontend/`.
- Rotas limpas configuradas no `vercel.json`.
- Pagina `404.html` personalizada com fallback nativo de erro 404 na Vercel.
- `robots.txt` e `sitemap.xml` preparados para publicacao.
- Sitemap gerado a partir das rotas do `vercel.json`, com datas editoriais explicitas em `tools/sitemap-dates.json`.
- Formulario de contato sem login, sem usuario de e-mail, sem senha e sem SMTP.
- Fonte de sistema para evitar dependencia externa de carregamento.
- Imagens da marca otimizadas e com dimensoes declaradas no HTML.
- Melhorias de acessibilidade com foco visivel, link para pular ao conteudo e menu ativo com `aria-current`.
- Headers de seguranca e cache configurados no `vercel.json`.
- GitHub Actions para validar JS, Vercel, sitemap, links internos, fontes e dimensoes de imagens.
- Dependabot configurado para revisar dependencias Python e GitHub Actions semanalmente.

## Links

- Site publicado: [https://m2rtecnologias.vercel.app/](https://m2rtecnologias.vercel.app/)
- Repositorio GitHub: [https://github.com/Marciorochar/M2R_tecnologias](https://github.com/Marciorochar/M2R_tecnologias)
- Sitemap: [https://m2rtecnologias.vercel.app/sitemap.xml](https://m2rtecnologias.vercel.app/sitemap.xml)
- Robots: [https://m2rtecnologias.vercel.app/robots.txt](https://m2rtecnologias.vercel.app/robots.txt)

## Prints do site

### Pagina inicial

![Pagina inicial da M2R Tecnologias](docs/screenshots/home.png)

### Projetos

![Pagina de projetos da M2R Tecnologias](docs/screenshots/projetos.png)

### Blog

![Pagina de blog da M2R Tecnologias](docs/screenshots/blog.png)

## Paginas do site

| Pagina | Arquivo | Rota no deploy |
| --- | --- | --- |
| Inicio | `frontend/index.html` | `/` |
| Servicos | `frontend/pages/servicos.html` | `/servicos` |
| Projetos | `frontend/pages/projetos.html` | `/projetos` |
| M2R Server | `frontend/pages/projetos/m2r-server.html` | `/projetos/m2r-server` |
| Blog | `frontend/pages/blog.html` | `/blog` |
| Artigo: Automacao para pequenos negocios | `frontend/pages/blog/automacao-para-pequenos-negocios.html` | `/blog/automacao-para-pequenos-negocios` |
| Artigo: Site profissional fortalece marca | `frontend/pages/blog/site-profissional-fortalece-marca.html` | `/blog/site-profissional-fortalece-marca` |
| Artigo: Organizacao de processos digitais | `frontend/pages/blog/organizacao-de-processos-digitais.html` | `/blog/organizacao-de-processos-digitais` |
| Sobre | `frontend/pages/sobre.html` | `/sobre` |
| Contato | `frontend/pages/contato.html` | `/contato` |
| Erro 404 | `404.html` e `frontend/404.html` | `/404` e rotas inexistentes |

## Tecnologias

### Frontend

- HTML5
- CSS3
- JavaScript puro
- Layout responsivo
- Menu mobile
- Animacoes leves com `IntersectionObserver`

## Estrutura do projeto

```text
M2R/
  404.html
  frontend/
    index.html
    404.html
    robots.txt
    sitemap.xml
    assets/
      css/
        style.css
      js/
        script.js
      img/
        logo.png
        m2r.png
        og-image.png
    pages/
      servicos.html
      projetos.html
      projetos/
        m2r-server.html
      blog.html
      blog/
        automacao-para-pequenos-negocios.html
        site-profissional-fortalece-marca.html
        organizacao-de-processos-digitais.html
      sobre.html
      contato.html
  docs/
    screenshots/
      home.png
      projetos.png
      blog.png
  .gitignore
  .github/
    dependabot.yml
    workflows/
      validate-site.yml
  tools/
    generate-sitemap.js
  CHANGELOG.md
  LICENSE
  README.md
  vercel.json
```

## Como rodar o frontend localmente

Pre-requisitos: Python 3.10 ou superior e Node.js 22 ou superior (para o sitemap). Na raiz do repositorio, inicie o servidor local, sem dependencias extras:

```powershell
python tools/site_tools.py serve --port 5500
```

Depois acesse:

```text
http://127.0.0.1:5500/
```

O servidor reutiliza rewrites, redirects e headers do `vercel.json`, incluindo `/servicos`, `/contato`, assets e resposta 404 para rotas inexistentes. Use outra porta com `--port 5501` se necessario. Ele atende apenas em loopback e implementa as regras estaticas atuais; nao e um emulador completo da Vercel nem comprova comportamento em producao.

<<<<<<< HEAD
## Como rodar o backend localmente

```powershell
cd backend
python -m pip install -r requirements.txt
python app.py
```

Rotas disponiveis:

| Metodo | Rota | Uso |
| --- | --- | --- |
| GET | `/` | Mensagem de status |
| GET | `/healthz` | Health check |
| GET | `/api/status` | Status da API |
| POST | `/api/contato` | Validacao simples dos dados de contato |

Variavel opcional:

```text
FRONTEND_URL=https://m2rtecnologias.vercel.app
APP_ENV=production
RATELIMIT_STORAGE_URI=memory://
```

Em producao, o CORS aceita apenas `FRONTEND_URL`. Em desenvolvimento local, use `APP_ENV=development` para permitir os servidores locais documentados no codigo.

O limitador usa memoria por processo por padrao: reinicios apagam contadores e workers nao os compartilham. Para usar a API em producao com varios workers, configure `RATELIMIT_STORAGE_URI` com armazenamento compartilhado e instale o driver correspondente (por exemplo, Redis). Nenhum servico externo e criado automaticamente. O endereco remoto continua sendo o fornecido pelo servidor; confirme a topologia do proxy antes de adicionar `ProxyFix` ou confiar em `X-Forwarded-For`.

### Contrato de contato

`POST /api/contato` apenas valida dados. Use `Content-Type: application/json` e um objeto com `name`, `email` e `message` obrigatorios; `phone` pode ser omitido. Todos os campos presentes devem ser strings. Limites antes de remover espacos nas extremidades: nome 120, e-mail 254, telefone 30 e mensagem 2000 caracteres. Conteudo excedente e rejeitado; quebras internas da mensagem sao preservadas. Nome, e-mail e telefone nao aceitam quebras internas de linha.

Respostas JSON: 200 para validacao bem-sucedida, 400 para JSON vazio/malformado, corpo que nao seja objeto ou campos invalidos, 415 para tipo de conteudo incompativel, 413 para corpo acima de 16 KiB e 429 apos duas tentativas por hora por endereco. Erros usam `error`; sucesso usa `message` e nao confirma envio. JSON `null`, listas, numeros, booleanos e strings no nivel raiz sao invalidos.

=======
>>>>>>> ba892d0 (Remove backend opcional)
## Contato

O formulario da pagina de contato usa `mailto:` para solicitar a abertura do aplicativo de e-mail do visitante com a mensagem preenchida.
O botao Preparar e-mail solicita a abertura; o visitante precisa revisar e enviar no proprio aplicativo. Nao ha confirmacao de abertura ou entrega. Os campos permanecem preenchidos para copia manual. Sem JavaScript, os campos ficam desabilitados, o formulario fica oculto e os canais diretos continuam disponiveis; os campos nao possuem atributos `name`, evitando dados pessoais em uma submissao nativa.
O site tambem possui link direto para WhatsApp com mensagem pre-preenchida e CTA fixo discreto no mobile.

Nao e necessario configurar:

- usuario de e-mail;
- senha de e-mail;
- SMTP;
- Gmail;
- banco de dados.

## Deploy na Vercel

Configuracao recomendada:

```text
Root Directory:
raiz do repositorio

Framework Preset:
Other

Build Command:
deixar vazio

Output Directory:
deixar vazio
```

O arquivo `vercel.json` faz o roteamento da raiz do projeto para os arquivos dentro de `frontend/`.
A pagina `404.html` na raiz e usada pela Vercel como fallback nativo para rotas inexistentes, preservando o status HTTP 404.
O mesmo arquivo tambem define headers de seguranca para todas as rotas e cache curto com revalidacao para arquivos em `/assets/*`, pois CSS, JavaScript e imagens ainda usam nomes fixos.

Rotas configuradas:

- `/`
- `/servicos`
- `/projetos`
- `/projetos/m2r-server`
- `/blog`
- `/blog/automacao-para-pequenos-negocios`
- `/blog/site-profissional-fortalece-marca`
- `/blog/organizacao-de-processos-digitais`
- `/sobre`
- `/contato`
- `/404`
- `/robots.txt`
- `/sitemap.xml`

Tambem ha redirecionamentos para URLs antigas, como `/index.html` e `/pages/contato.html`.
Rotas inexistentes nao usam rewrite generico; elas caem no 404 nativo da Vercel.

## Validacao antes de publicar

Use estes comandos para uma validacao local rapida antes de fazer commit:

```powershell
<<<<<<< HEAD
node tools/generate-sitemap.js --check
python tools/site_tools.py check
python tools/site_tools.py security
python -m unittest discover -s tools -p "test_*.py" -v
python -m pip install -r backend/requirements.txt pytest pip-audit
python -m pytest backend
python -m pip_audit -r backend/requirements.txt
python -m py_compile backend/app.py
=======
>>>>>>> ba892d0 (Remove backend opcional)
node --check frontend/assets/js/script.js
git status
```

Quando uma pagina nova for criada ou uma rota mudar, registre a data real da mudanca editorial apenas nas rotas afetadas em `tools/sitemap-dates.json` e gere o sitemap. Datas existentes vieram do sitemap anterior; alteracoes em ferramentas, commits, checkout e builds nao atualizam datas de paginas. Esse registro explicito produz o mesmo resultado antes e depois do commit, inclusive sem historico Git. O teste cria um commit sem relacao com as paginas em outra data para verificar a estabilidade.

```powershell
node tools/generate-sitemap.js
```

A CSP permite scripts locais, sem `unsafe-inline`. Os blocos JSON-LD sao validados como dados estruturados, nao executam JavaScript, e o check confirma que permanecem JSON valido e que a politica final nao reintroduz permissoes inline.

Testes opcionais de navegador: instale `playwright`, execute `python -m playwright install chromium` e depois `python tools/browser_check.py`. O teste usa servidor local temporario e intercepta o mailto, sem enviar mensagens.

O workflow do GitHub Actions tambem roda em cada push e pull request para validar:

- JavaScript;
- HTML e CSS;
- `vercel.json`;
- sitemap;
- sitemap atualizado a partir do `vercel.json`;
- links internos;
- ausencia de Google Fonts;
- dimensoes declaradas em imagens;
- dependencias do backend com versoes fixadas no `backend/requirements.txt`;
- sintaxe Python;
- testes Python do backend Flask;
- auditoria de vulnerabilidades com `pip-audit`.

O Dependabot verifica semanalmente:

- pacotes Python do `backend/requirements.txt`;
- versoes usadas pelos workflows do GitHub Actions.

As versoes das dependencias Python ficam somente em `backend/requirements.txt`. O workflow valida o formato com pin exato (`==`) e usa instalacao, testes e `pip-audit` para verificar compatibilidade e seguranca.

Depois, envie para o GitHub:

```powershell
git add .
git commit -m "Atualiza projeto M2R"
git push origin main
```

## Checklist de publicacao

- Conferir se a pagina inicial abre corretamente.
- Conferir se as rotas limpas funcionam.
- Testar menu mobile.
- Testar o formulario abrindo o aplicativo de e-mail.
- Conferir `/404` e uma rota inexistente com status HTTP 404 no deploy.
- Conferir `/robots.txt`.
- Conferir `/sitemap.xml`.
<<<<<<< HEAD
- Atualizar os prints em `docs/screenshots/` quando houver mudanca visual relevante.
- Se o backend for publicado, testar `/healthz`.
=======
>>>>>>> ba892d0 (Remove backend opcional)

## Status atual

Projeto estatico preparado para publicacao na Vercel e versionamento pelo GitHub.
