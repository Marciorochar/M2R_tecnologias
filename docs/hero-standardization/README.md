# Padronização dos Heroes internos

Implementação para revisão da identidade visual da Home nos Heroes de todas as rotas internas. A implementação preserva os arquivos da página inicial e dá a cada página título, contexto, CTA e conteúdo próprios.

## Páginas incluídas

Inclui Sobre, Serviços, Contato, Fundador, Projetos, Blog, os três artigos, detalhe M2R Server e os documentos 404 da raiz e de `frontend/`.

## Componentes compartilhados

- `frontend/assets/css/internal-hero.css`: tokens/estrutura do Hero interno, composição responsiva, breadcrumb, botão de movimento e tratamento de movimento reduzido.
- `frontend/assets/js/internal-hero.js`: inicialização segura, movimento pausável, visibilidade/interseção e compatibilidade com fallback.
- `frontend/assets/img/hero-circuits.svg`: arte decorativa compartilhada, derivada da geometria existente da Home.
- `tools/version-assets.js`: manutenção dos hashes dos assets com validação.
- `tools/test_internal_hero.py` e `tools/hero_check.py`: regressão de estrutura, conteúdo e layout.

Não foi introduzida uma framework. As páginas internas não carregam o vídeo da Home. Os arquivos `frontend/index.html`, `frontend/assets/css/style.css`, `frontend/assets/js/hero-circuits.js` e `frontend/assets/video/m2r-circuitos.webm` permanecem intactos na branch.

## Diferenças intencionais

A hierarquia visual, superfície marrom escura, circuitos dourados e proporções são compartilhadas. Copy, subtítulo, chamadas e conteúdo do Hero seguem a finalidade de cada página. Artigos conservam metadados; M2R Server preserva seu painel/terminal; páginas 404 conservam sua ação de retorno. Breadcrumbs e navegação existentes são mantidos.

## Comparação visual

Abra [`comparisons.html`](comparisons.html) em um navegador para navegar pelas capturas pré e pós-implementação. Há 72 capturas antes e depois, cobrindo 12 rotas em 320, 390, 768, 1024, 1440 e 1920 px. Os resultados e limitações estão em [`existing-tests.md`](existing-tests.md); a auditoria da correção está em [`fix-audit.md`](fix-audit.md).

## Arquivos

As mudanças de implementação estão nos componentes compartilhados, páginas internas e testes relacionados. Artefatos desta pasta guardam a exploração, a auditoria, as capturas, os dados e os relatórios de validação. A página inicial foi preservada.

## Limitações

Não há aprovação de conformidade WCAG integral: os achados axe de `target-size` em breadcrumbs existentes permanecem fora do Hero. Duas comparações geométricas móveis não foram medidas porque o helper não obteve geometria após rolagem. Lighthouse não gerou resultado final. O verificador de design genérico também aponta diferenças estruturais preexistentes na baseline, fora do escopo. A branch foi preparada para PR sem merge e sem deploy.
