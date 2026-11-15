# Exploração: padronização dos heros internos

## Escopo e estado
Leitura somente. Checkout C:/Users/marci/.codex/worktrees/m2r-hero-20261113, branch codex/hero-consistency-2026-11-13, inicialmente limpo e alinhado a origin/main (git status --short --branch). A home e assets não foram alterados. Inventário cobre as páginas HTML atualmente presentes no frontend, não valida visualmente o browser.

## Arquitetura e geometria reaproveitável
- A home é frontend/index.html:45-108,217: <section class= page-hero home-hero home-hero--circuits id=m2r-hero>, vídeo local, SVG de circuitos, copy/CTAs, painel de áreas, acionador e controle de movimento. Os caminhos base estão em markup para geometria determinística; vídeo é adorno.
- frontend/assets/css/style.css:280-301 define .page-hero como faixa escura com padding 150px 0 76px, títulos clampados, parágrafo até 700px. É a base simples reaproveitada pelas páginas internas.
- A composição home final está na camada tardia style.css:2387-2518: altura mínima 690px, centralização flex, padding responsivo, container de 1200px, layout grid 1.5fr/.68fr, tipografia com clamp, fundo radial marrom e mascaramento dos circuitos. As regras anteriores 2090-2385 incluem camada/efeitos, estados e breakpoints; há regras home repetidas e algumas sobrescritas entre os dois blocos.
- Vídeo e SVG da home usam camadas absolutas (style.css:2117-2144); conteúdo em z-index 4 (2197), controles em z-index 5/6 (2231, 2287). Não devem ser reutilizados como mecanismo interno: frontend/assets/js/hero-circuits.js:5-18 exige IDs e nós específicos e sai cedo se faltarem. Isso mantém o script inerte nas páginas internas.

## Variantes internas encontradas
- Páginas simples com .page-hero: serviços frontend/pages/servicos.html:44-55, projetos frontend/pages/projetos.html:38-40, blog frontend/pages/blog.html:33-34, contato frontend/pages/contato.html:33-34, sobre frontend/pages/sobre.html:33-34, fundador frontend/pages/fundador.html:34.
- Artigos: três documentos frontend/pages/blog/*.html:33-34 usam .page-hero.article-hero; cada qual tem tag, H1, descrição e .article-meta. Exemplo automacao-para-pequenos-negocios.html:34; style.css:478-486 só altera padding inferior/meta.
- Projeto detalhado frontend/pages/projetos/m2r-server.html:39-46 preserva breadcrumb e usa .page-hero.project-detail-hero, grid de texto e terminal; style.css:684-700 mantém layout 2 colunas e ações.
- Erro 404 duplicado: 404.html:46-57 e frontend/404.html:46-57, mesmo .page-hero.error-page, conteúdo em copy e painel decorativo. Site_tools checa especificamente raiz 404.html; Vercel serve o documento de erro padrão, portanto mudanças de visual devem manter os dois arquivos sincronizados ou esclarecer qual é fonte canônica.
- Breadcrumbs antecedem o hero, não estão dentro dele (exemplos em servicos.html:44-45, artigo :33-34, projeto :39-40). Aplicar fundo/circuitos no hero sem absorver/remover breadcrumb preserva hierarquia e navegação.

## Conflitos, riscos e dependências
1. CSS global tardio: style.css:2090-2518 tem seletor .home-hero.home-hero--circuits e breakpoints home-específicos, enquanto a base genérica é 280-301. Alterar a base diretamente pode mudar home por herança, inclusive alturas/contraste. Preferir classe aditiva interna como .page-hero--circuits e seletores ancorados nessa classe, sem editar regras home.
2. Exceções estruturais: artigo e detalhe de projeto precisam preservar suas classes e conteúdo internos; alterar markup interno para um único container genérico pode quebrar o grid do terminal ou espaçamento/meta. Envolver conteúdo em wrapper comum ou estilizar os containers existentes com seletor de variante.
3. 404 duplicado e tooling: tools/site_tools.py percorre HTML servido por rewrites e valida links/assets; para 404 valida 404.html na raiz. vercel.json:143+ roteia /404 para /frontend/404.html; fallback da plataforma usa raiz. Consistência exige ambos.
4. CSP em vercel.json:4-28 define script-src 'self' e style-src 'self'; efeito decorativo deveria ser CSS/SVG inline estático na página/CSS externo, sem script/estilo inline novo. JS da home existente deve ficar home-only.
5. Imagens de evidência existentes em docs/auditoria/evidencias/responsivo e checks axe (tools/test_hero_circuits.py) são evidência antiga/testes limitados: teste atual afirma conteúdo e controles home, não a paridade de heros internos. Não foi executado teste, conforme escopo.
6. Imports de CSS usam caminhos relativos em documentos internos; a nova classe deve residir no style.css já linkado. Confirmar em browser as camadas decorativas não bloqueiam texto, links, foco, breadcrumbs ou leitura em viewport mobile.

## Arquitetura mínima recomendada
Preservar literalmente frontend/index.html, frontend/assets/css/style.css nas regras home 1028+/2090+ e frontend/assets/js/hero-circuits.js. Adicionar uma classe interna explícita aos .page-hero das rotas não-home (inclusive artigos, detalhe de projeto e ambos 404), mantendo article-hero, project-detail-hero, error-page e todos os filhos atuais. Em CSS novo, colocar uma seção depois das regras atuais com escopo .page-hero--circuits para superfície marrom/gradientes e traçados dourados estáticos; não usar .home-hero, IDs m2r-*, vídeo ou lógica de interação da home. Regras responsivas devem reduzir densidade/contraste da decoração em telas estreitas e respeitar prefers-reduced-motion (recomendável não animar decoração interna). 404 duplo deve receber marcação equivalente.

## Perguntas abertas
- Todas as páginas internas inclui /404 explícito e o fallback 404 da hospedagem? A recomendação assume sim.
- Padrão precisa apenas da identidade marrom/dourada com circuitos estáticos, ou há requisito de parallax/ativação interativa também nas páginas internas? Arquitetura mínima assume decoração estática e acessível.
- Deve-se manter o layout atual de duas colunas do terminal M2R Server e a ordem atual dos breadcrumbs? Recomenda-se sim; não há decisão contrária no código.


