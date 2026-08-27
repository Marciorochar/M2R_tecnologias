# Changelog

Todas as mudancas notaveis deste projeto serao documentadas aqui.

O formato segue uma estrutura simples inspirada em Keep a Changelog, com datas em `AAAA-MM-DD`.

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
