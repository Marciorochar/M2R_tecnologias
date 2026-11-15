# Validação final

## Suítes existentes

- `pytest tools backend -q`: 147 testes aprovados e 54 subtestes aprovados.
- `python -m unittest discover -s tools -p "test_*.py"`: 59 testes aprovados.
- `python tools/site_tools.py check`: aprovado; 12 páginas verificadas.
- `python tools/site_tools.py security`: aprovado; 19 blocos JSON-LD verificados.
- `node tools/version-assets.js --check`: aprovado.
- `python tools/browser_check.py`: código de saída 0; log em `validation/browser-check.log`.
- `git diff --check`: aprovado nos commits da implementação.

## Matriz visual e funcional

- 12 rotas × 6 larguras (320, 390, 768, 1024, 1440 e 1920 px): 72 capturas antes e 72 depois, em `before/` e `after/`.
- Métricas MCP dos 72 casos: sem erro de página, sem rolagem horizontal, exatamente um H1 e arte decorativa com dimensões positivas.
- Validação Playwright do executor: 72 layouts, 11 conjuntos de interação, 33 casos de fallback e 24 execuções axe; sem erros de console nos casos reportados.
- Em 320 px, a correção do controle de movimento deixa 82,891 px entre seu limite direito (x=175,109) e o atalho WhatsApp (x=258). Revisão independente aprovou a correção em `fix-audit.md`.
- Comparação visual navegável: `comparisons.html`.

## Limitações registradas

- As comparações geométricas de colisão cobrem 20 de 22 casos móveis; em `/contato` a 320 e 390 px o helper retorna `null` após rolagem porque um dos elementos deixa de estar visível. Isso não é contado como comparação concluída.
- Os relatórios axe do Hero estão sem violações. Há achados `target-size` já existentes nos links de breadcrumbs fora do escopo, portanto esta implementação não declara conformidade WCAG integral.
- A execução Lighthouse iniciada durante a validação não produziu métricas finais; os arquivos de log correspondentes estão vazios e não são tratados como aprovação.
- A regra geral do verificador visual da skill de design reportou 27 diferenças estruturais já presentes na baseline do site (ritmo de seção e largura de colunas); esse gate não foi aprovado globalmente. O escopo e os limites estão em `checkers/`.

