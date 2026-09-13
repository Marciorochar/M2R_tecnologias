# Changelog

Todas as mudancas notaveis deste projeto serao documentadas aqui.

O formato segue uma estrutura simples inspirada em Keep a Changelog, com datas em `AAAA-MM-DD`.

## [1.0.4] - 2026-09-06

### Adicionado

- Gerador de sitemap baseado nas rotas do `vercel.json`, com `lastmod` calculado pelo historico do Git.
- Validacao no GitHub Actions para detectar `frontend/sitemap.xml` desatualizado.
- Testes automatizados para rotas principais do backend Flask e validacao de contato.
- Limite de tamanho para requisicoes do backend.
- Validacao no CI para manter `404.html` e `frontend/404.html` sincronizados.
- Checkout completo no GitHub Actions para permitir `lastmod` confiavel no sitemap automatico.

### Alterado

- README atualizado com orientacao para gerar e validar o sitemap antes da publicacao.
- Workflow ajustado para nao duplicar versoes de dependencias Python fora do `backend/requirements.txt`.
- Cache de `/assets/*` alterado para `max-age=3600, must-revalidate`, evitando `immutable` em arquivos com nomes fixos.
- CORS do backend separado por ambiente, mantendo localhost apenas em desenvolvimento.
- Validacao de links internos do CI passa a derivar rotas do `vercel.json`.
- Gerador de sitemap passa a falhar em modo `--check` quando o historico Git necessario nao estiver disponivel.

## [1.0.3] - 2026-09-06

### Adicionado

- Content Security Policy nos headers da Vercel, incluindo `frame-ancestors 'none'` e compatibilidade com JSON-LD inline.
- Validacao no GitHub Actions para impedir remocao acidental das diretivas CSP principais.
- Validacoes de CI para instalacao do backend, `pip-audit`, testes Python quando existirem, HTML e CSS.
- `python-dotenv` atualizado para `1.2.2` apos auditoria automatizada de dependencias.
- Dependabot configurado para atualizar semanalmente dependencias Python e GitHub Actions.

## [1.0.2] - 2026-09-06

### Corrigido

- Atualizacao das dependencias do backend para remover `Flask-Cors` da faixa afetada por vulnerabilidades conhecidas.
- Animacao `fade-in-section` ajustada para manter o conteudo visivel quando JavaScript falhar, for bloqueado ou estiver indisponivel.
- Dominio de exemplo do backend alinhado ao dominio oficial `https://m2rtecnologias.vercel.app`.
- Menu mobile ajustado para continuar acessivel quando JavaScript falhar, com botao presente no HTML e estados ARIA sincronizados.

### Alterado

- `Flask` atualizado para `3.1.3`.
- `Flask-Cors` atualizado para `6.0.5`.
- `Flask-Limiter` atualizado para `4.1.1`.
- `gunicorn` atualizado para `26.2.0`.

## [1.0.1] - 2026-08-27

### Corrigido

- Ajuste do fallback 404 para permitir status HTTP 404 real em rotas inexistentes na Vercel.
- Inclusao de `404.html` na raiz do projeto para erro personalizado nativo da Vercel.

### Adicionado

- Headers de seguranca `X-Content-Type-Options`, `Referrer-Policy` e `Permissions-Policy`.
- Cache longo para arquivos estaticos em `/assets/*`.
- Workflow do GitHub Actions para validar site estatico em push e pull request.

## [1.0.0] - 2026-08-22

### Adicionado

- Site institucional multipaginas da M2R Tecnologias.
- Rotas limpas para publicacao na Vercel.
- Pagina 404 personalizada.
- Open Graph e Twitter Cards para compartilhamento.
- SEO com canonical, sitemap, robots e dados estruturados.
- Pagina detalhada do projeto M2R Server.
- Blog com 3 artigos iniciais e paginas proprias.
- Contato sem usuario, senha ou SMTP, usando `mailto:` e WhatsApp.
- CTA fixo discreto de WhatsApp no mobile.
- Melhorias de acessibilidade com foco visivel, link para pular conteudo e `aria-current`.
- Otimizacoes de performance com fonte de sistema, imagens dimensionadas e PNGs comprimidos.
- Documentacao com README, LICENSE, CHANGELOG e prints do site.

### Alterado

- Dominio oficial definido como `https://m2rtecnologias.vercel.app/`.
- README reorganizado para uso no GitHub e publicacao.
- Contraste visual dos cards, tags e textos secundarios.

### Removido

- Dependencia de fonte externa do Google Fonts.
