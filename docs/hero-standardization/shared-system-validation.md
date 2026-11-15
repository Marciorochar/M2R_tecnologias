# Validação do sistema compartilhado de Hero

**Data:** 15/11/2026  
**Escopo:** Home e 11 rotas internas, incluindo páginas de artigo, detalhe de projeto e 404.

## Resultado

A Home e as páginas internas carregam a mesma base de superfície, arte de circuitos e controle de movimento. As páginas internas mantêm seus painéis e conteúdo próprios; a Home mantém vídeo e interações adicionais. O SVG continua como arte estática quando JavaScript está indisponível ou a requisição `fetch` falha.

A regressão do CI em `/` a 320×600 foi incorporada à checagem de colisão entre o CTA principal e o botão fixo do WhatsApp. A asserção passou após o ajuste de posicionamento do controle.

## Verificações executadas

| Verificação | Resultado |
|---|---|
| `python -m pytest tools/test_internal_hero.py tools/test_hero_circuits.py tools/test_browser_check.py tools/test_site_tools.py -q` | 56 testes e 33 subtestes passaram |
| `python tools/site_tools.py check` | Links, assets, fragmentos e destinos corretos nas 12 páginas |
| `python tools/browser_check.py` | 12 rotas passaram em 320, 390, 768, 1024, 1440 e 1920 px; sem erro de navegador |
| `python tools/hero_check.py --output-dir test-results/hero-system/after` | 72 casos responsivos, 11 verificações de comportamento, 33 verificações de fallback e 24 relatórios Axe; 105 PNGs gerados |
| `node tools/version-assets.js --check` | Hashes de assets atualizados |
| `node --check` para os dois scripts de Hero | Sintaxe JavaScript válida |
| `git diff --check` | Sem erros de whitespace |

Os cenários de comportamento cobrem pausa e retomada pelo teclado, preferência de movimento reduzido alterada em runtime, aba oculta, Hero fora da viewport e idempotência do runtime. Os fallbacks cobrem JavaScript desabilitado, falha de `fetch` do SVG e preferência inicial por movimento reduzido. Axe foi executado a 390 e 1440 px em todas as rotas; não foram encontrados problemas graves dentro do Hero ou da navegação de breadcrumb.

## Comparação visual

As 72 capturas de `before` foram pareadas com as 72 capturas de `after`; todas mantiveram as mesmas dimensões. A diferença média absoluta por canal foi 1,505/255 e, em média, 9,96% dos pixels diferiram acima do limiar de 5. As diferenças são esperadas porque fundo, arte, circuitos e controles passaram a compartilhar a mesma base visual.

Também foi feita inspeção visual da Home, Serviços, um artigo, detalhe do M2R Server e 404 nos seis tamanhos. A composição e o conteúdo próprios de cada variante permanecem visíveis; em telas pequenas o conteúdo não ultrapassa a largura disponível. A folha comparativa e os dados numéricos ficam em `test-results/hero-system/comparison-sheet.jpg` e `test-results/hero-system/visual-comparison.json`.

## Limites

As evidências foram coletadas em Chromium local e em ambiente CI com viewport simulado. Axe cobre as rotas e tamanhos indicados, mas estes resultados não equivalem a uma declaração de conformidade WCAG integral nem substituem testes com leitores de tela, dispositivos reais ou dados de campo.
