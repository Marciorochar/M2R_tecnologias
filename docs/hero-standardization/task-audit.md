# Auditoria independente — Task 1

Data: 2026-11-13. Revisão do pacote `eccb540..0f5876e`, com referência de preservação `7436829`.

**Veredito: correção necessária antes da aprovação da Task 1.** Um achado P2 no novo controle de movimento; nenhum P0/P1 identificado. Não houve implementação, alteração de arquivos de produto, índice, branch, configuração, merge ou deploy nesta auditoria. Este relatório é a única escrita autorizada ao auditor.

## Achado acionável

### A1 — P2 — Controle de movimento parcialmente encoberto pelo WhatsApp em 320px

- **Localização:** `frontend/assets/css/internal-hero.css:64` (alinhamento do contêiner do controle), `frontend/assets/css/internal-hero.css:70` (botão); integração observada em `frontend/404.html:66` e sua cópia raiz. Lacuna de cobertura em `tools/hero_check.py:64` e `tools/hero_check.py:76`.
- **Evidência:** `test-results/internal-hero-executor-captures/404-320.png`, captura de `/404` em 320×900, no topo, com movimento pausado. O botão “Retomar movimento” ocupa aproximadamente x145–300/y816–861 e o WhatsApp ocupa x258–306/y842–886. O canto inferior direito do novo botão fica sob o atalho fixo. Os valores são estimados da imagem, não uma medição de DOM.
- **Justificativa:** o atalho existente tem `position: fixed`, `right: 14px`, `bottom: 14px` e `z-index: 1100` (`frontend/assets/css/style.css:1849`); o novo controle alinha-se à direita sem reservar espaço para ele. Parte do alvo do controle pode acionar WhatsApp em vez de retomar/pausar o movimento. Isso contraria a exigência de controles utilizáveis e sem sobreposição em 320px e é uma interação introduzida pelo novo Hero, mesmo que o atalho já existisse.
- **Por que os checks não detectam:** `layout_metrics` compara somente `a.btn` e botões descendentes do Hero; o atalho global fica fora desse conjunto. O axe é executado com redução de movimento, quando o novo botão está oculto, portanto seus relatórios sem violações no Hero não afastam essa colisão.
- **Correção solicitada ao executor:** ajustar somente os estilos/posicionamento novos para que o controle permaneça livre do atalho fixo nas larguras móveis, preservando o CSS global e o próprio CTA existente. Incluir verificação de colisão/oclusão com o atalho visível e capturar novamente `/404` em 320×900, no topo e com o controle visível; verificar também o estado após rolagem nas demais rotas móveis. O auditor deve revalidar A1 e a regressão pertinente após a correção.

## Conformidade da especificação: pontos sem achados adicionais

- **Escopo e preservação:** o inventário do diff contém os 18 arquivos autorizados de produto/testes. A listagem de mudanças entre `7436829` e `0f5876e` não inclui `frontend/index.html`, `frontend/assets/css/style.css`, `frontend/assets/js/hero-circuits.js`, vídeo ou configuração de produção. Os testes de preservação comparam os arquivos protegidos e o DOM externo ao Hero; títulos, parágrafos e ações originais são verificados separadamente. Não identifiquei mudança indevida de conteúdo, metadados ou breadcrumbs nas evidências examinadas. Os três IDs de destino externos ao Hero são previstos no contrato.
- **Sistema visual e integrações:** CSS com escopo `.page-hero--circuits`, carregamento exclusivo nas internas, SVG decorativo compartilhado, 14 geometrias e pontos estáticos, CTAs contextuais e conservação dos painéis de projeto/404 correspondem ao desenho aprovado. A amostra visual de artigo320, projeto320, 404320 e blog1440 não mostrou outro problema material de texto/painel. A amostra não equivale à inspeção visual de todas as 105 capturas.
- **Qualidade e aprimoramento progressivo:** o JavaScript mantém imagem estática, verifica origem, constrói apenas elementos SVG conhecidos a partir de geometria validada e não injeta markup recebido. Há proteção contra inicialização duplicada, pausa manual separada de visibilidade/interseção/redução de movimento e fallback de rolagem. Não há loop permanente de RAF. Não identifiquei defeito adicional nesses caminhos na leitura de `internal-hero.js` e `internal-hero.css`.
- **Rotas e verificações:** os artefatos `test-results/internal-hero-executor-captures/metrics.json` registram 12 rotas, seis larguras (320, 390, 768, 1024, 1440, 1920), 72 casos, 11 conjuntos de comportamento, três modos de fallback por interna e `pageErrors: []`. O diretório contém 105 PNGs e 24 relatórios axe. Os campos de comportamento e contraste correspondem ao relato do executor. Não identifiquei outra ausência material além da interação A1.

## Avaliação independente dos achados axe externos

Os 24 JSONs examinados contêm `heroViolations: []`. Oito relatórios mantêm `target-size` com impacto axe `serious`: três artigos e `/projetos/m2r-server`, em 390 e 1440. Os seletores apontam para links dos breadcrumbs, fora do Hero. O axe informa 21px de altura, com espaço seguro de 18,4px nos artigos e 21px no projeto. A descrição do relatório do executor simplifica esse segundo valor, sem mudar a conclusão.

Esses elementos e as regras globais responsáveis estão preservados e são explicitamente externos ao escopo autorizado; não são achados novos que justifiquem alterar breadcrumbs nesta Task 1. Devem continuar declarados como limitação de acessibilidade do site, sem alegação de conformidade integral. A1 permanece distinto: envolve um botão novo do Hero sobreposto por um elemento global existente.

## Evidência e limitações da revisão

Entradas comparadas: `.superpowers/sdd/hero-consistency/task-1-brief.md`, `task-1-report.md`, `task-review.diff` e `docs/superpowers/specs/2026-11-13-hero-consistency-design.md`. Inspeção adicional dirigida: script/CSS/SVG novos, lógica do checker, inventário de mudanças desde a base, métricas/24 relatórios axe e quatro capturas citadas. A consulta externa ao diff ficou restrita às regras existentes do WhatsApp, necessárias para explicar A1.

Não repeti pytest, check/security, version-assets ou os passes de navegador já registrados, conforme o contrato de auditoria. Os resultados de 77 testes/54 subtestes e demais comandos são evidência reportada pelo executor; não são execuções independentes do auditor. A validação `browser_check` e os diagnósticos MCP/DevTools pertencem ao coordenador. O teste de aba oculta usa override de propriedade/evento e não comprova a transição nativa entre abas; o caso de interseção da 404 usa transformação temporária, ambos declarados pelo executor. Nenhuma certificação WCAG ou aprovação de deploy é inferida.

Revalidação de A1: pendente da correção do executor.
