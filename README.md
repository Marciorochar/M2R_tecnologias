# M2R Tecnologias

Site institucional da M2R Tecnologias para apresentar solucoes em engenharia, automacao, desenvolvimento web, dados e BI. O projeto nao possui fluxo de login, cadastro ou area restrita.

## Estrutura

```text
frontend/
  index.html
  assets/
    css/style.css
    js/script.js
    img/
  pages/
    index_servicos.html
    index_projetos.html
    index_blog.html
    index_sobre.html
    index_contatos.html
backend/
  app.py
  requirements.txt
  .env.example
vercel.json
```

## Frontend

Abra `frontend/index.html` com o Live Server do VS Code. Os estilos, scripts e imagens usam caminhos relativos dentro de `frontend/`.

## Backend local

```powershell
cd backend
python -m pip install -r requirements.txt
python app.py
```

Rotas disponiveis:

- `GET /`
- `GET /healthz`
- `GET /api/status`
- `POST /api/contato`

Crie `backend/.env` a partir de `backend/.env.example` e informe `EMAIL_USER`, `EMAIL_PASS` e `FRONTEND_URL`.

## Deploy

### Vercel

O `vercel.json` na raiz encaminha as requisicoes para `frontend/`. Como alternativa, configure `frontend` como **Root Directory** no projeto da Vercel e remova as rewrites de raiz.

### Render

- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
- **Health Check Path:** `/healthz`

## Git

```powershell
git status
git add .
git commit -m "Organiza estrutura do projeto e remove login"
git push origin main
```