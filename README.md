# M2R Tecnologias

Site institucional da M2R Tecnologias para apresentar servicos, projetos, conteudos, informacoes sobre a empresa e canais de contato.

O projeto nao possui login, cadastro, area restrita, usuario ou senha de e-mail.

## Estrutura do projeto

```text
M2R/
  frontend/
    index.html
    robots.txt
    sitemap.xml
    assets/
      css/style.css
      js/script.js
      img/
        logo.png
        m2r.png
    pages/
      servicos.html
      projetos.html
      blog.html
      sobre.html
      contato.html
  backend/
    app.py
    requirements.txt
    .env.example
  .gitignore
  README.md
  render.yaml
  vercel.json
```

## Frontend

O frontend e estatico, feito com HTML, CSS e JavaScript.

Para testar localmente, abra `frontend/index.html` com o Live Server do VS Code ou rode um servidor local dentro da pasta `frontend`.
Nesse modo local, acesse tambem os arquivos `.html` listados abaixo. As URLs limpas ficam ativas no deploy pela configuracao do `vercel.json`.

Paginas disponiveis:

- Inicio: `frontend/index.html`
- Servicos: `frontend/pages/servicos.html`
- Projetos: `frontend/pages/projetos.html`
- Blog: `frontend/pages/blog.html`
- Sobre: `frontend/pages/sobre.html`
- Contato: `frontend/pages/contato.html`

Na Vercel, o arquivo `vercel.json` tambem libera URLs limpas:

- `/`
- `/servicos`
- `/projetos`
- `/blog`
- `/sobre`
- `/contato`

## Contato

O formulario da pagina de contato usa `mailto:` para abrir o aplicativo de e-mail do visitante com a mensagem preenchida.

Nao e necessario configurar:

- usuario de e-mail;
- senha de e-mail;
- SMTP;
- Gmail;
- banco de dados.

## Backend

O backend Flask esta mantido para status, health check e validacao simples de dados de contato.

Rotas disponiveis:

- `GET /`
- `GET /healthz`
- `GET /api/status`
- `POST /api/contato`

Para rodar localmente:

```powershell
cd backend
python -m pip install -r requirements.txt
python app.py
```

Variavel opcional:

```text
FRONTEND_URL=https://m2r-tecnologias.vercel.app
```

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

O `vercel.json` encaminha os arquivos da pasta `frontend/` corretamente.

## Deploy no Render

O backend pode ser publicado pelo `render.yaml` na raiz do projeto ou configurado manualmente:

```text
Root Directory:
backend

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app --bind 0.0.0.0:$PORT

Health Check Path:
/healthz
```

Nao configure usuario ou senha de e-mail no Render.

## Checklist antes de postar

```powershell
git status
python -m py_compile backend/app.py
node --check frontend/assets/js/script.js
git add .
git commit -m "Prepara projeto M2R para deploy"
git push origin main
```

Depois do push, confira:

- site aberto na Vercel;
- paginas com URLs limpas;
- menu mobile;
- formulario abrindo o aplicativo de e-mail;
- backend do Render respondendo em `/healthz`, se decidir manter o backend publicado.
