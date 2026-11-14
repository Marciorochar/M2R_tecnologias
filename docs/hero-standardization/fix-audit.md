# Revalidação independente — correção da Task 1

Data: 2026-11-14. Commit revisado: `0cf4b129172af8a4a97e8fa25e87e1b2d4def74b`, comparado ao seu pai `0f5876e`. Escopo: achado A1 de `docs/hero-standardization/task-audit.md` e regressões pertinentes ao diff da primeira correção.

**Veredito: A1 corrigido nas evidências examinadas; correção aprovada nesta revisão focada. Nenhum novo achado acionável P0, P1, P2 ou P3 identificado.** A revisão não autoriza deploy nem certifica acessibilidade integral.

## Vínculo entre achado, correção e evidência

**A1 — P2 original — controle de movimento sob o WhatsApp em `/404`, 320×900: resolvido.**

- Correção em `frontend/assets/css/internal-hero.css:151`: o bloco móvel até 768px alinha `.internal-hero-controls` à esquerda e reserva 72px à direita. O CTA global e seu CSS permanecem fora do diff.
- Evidência lida diretamente em `test-results/internal-hero-fix1/metrics.json`, entrada `captures` com `route: /404`, `width: 320`, `artifactState: manually-paused`: controle x20–175,109/y816,125–860,125, com altura de 44px; WhatsApp x258–306/y842–886. Embora os intervalos verticais se cruzem, os horizontais estão separados por 82,891px; as caixas não colidem.
- O mesmo arquivo registra `/404` após a ação de rolagem, em 320px: controle x20–163,516/y816,125–860,125 e o mesmo WhatsApp. A diferença de largura corresponde ao rótulo de movimento ativo antes do clique. Também não há colisão.
- `tools/hero_check.py:83` acrescenta comparação explícita entre o botão novo e o CTA global, antes ausente. `tools/hero_check.py:175` verifica os casos móveis após `scrollIntoView`, clica no controle e exige `aria-pressed=true`. A geometria registrada, o novo alinhamento e a leitura do teste sustentam a resolução do defeito original.

## Pontos sem achados adicionais

- **Escopo:** o inventário do commit contém 15 arquivos: CSS/JS internos novos, helper de navegador e 12 documentos HTML com atualização dos hashes dos dois assets. O diff não inclui Home, CSS global, JS de circuitos da Home, vídeo, SVG, dependências ou configuração. O pacote `.superpowers/sdd/hero-consistency/fix-1.diff` e o diff do commit apresentam as mesmas alterações funcionais examinadas. Não identifiquei mudança de conteúdo, links, metadados ou estrutura dos breadcrumbs.
- **Autorização das alterações adicionais:** a especificação atual em `docs/superpowers/specs/2026-11-13-hero-consistency-design.md:32` permite expressamente apresentação dos breadcrumbs no CSS interno, alvos de pelo menos 44px, prevenção de colisão com WhatsApp e remoção do destaque do ponteiro ao pausar. Assim, os ajustes de breadcrumbs e halo estão contemplados no escopo atualizado, embora fossem externos ao contrato inicial da Task 1.
- **Halo:** `frontend/assets/js/internal-hero.js:22` remove a classe de ponteiro quando `paused` é verdadeiro. A expressão existente inclui pausa manual, preferência de movimento reduzido, documento oculto e Hero fora da tela. O helper acrescenta ativação real do ponteiro e assertiva de remoção após pausa por teclado. Não identifiquei regressão introduzida por essa alteração.
- **Breadcrumbs:** CSS restrito à folha interna posiciona os itens abaixo da navbar, mantém largura comum ao conteúdo, permite quebra, aumenta alvos e define foco visível; há ajuste específico para navbar móvel sem JS. O helper verifica itens reais, alinhamento, dimensões, hit testing central e foco, inclusive nos fallbacks. Não identifiquei defeito novo nesses caminhos na leitura do diff e métricas.
- **Evidência de regressão:** o JSON contém 12 rotas, 72 entradas responsivas, 11 conjuntos de comportamento, 22 entradas móveis adicionais e `pageErrors: []`. A leitura dos 24 arquivos `test-results/internal-hero-fix1/axe-*.json` confirmou `violations: []` em todos. Isso corresponde ao relatório da primeira correção; não substitui inspeção visual ou execução independente.

## Limitações e precisão da cobertura

- **20/22 medições móveis:** existem 22 entradas em `mobileOverlays`, mas somente 20 têm duas caixas medidas. `/contato` em 320 e 390px tem `afterScroll: null`. O helper retorna `None` se o controle ou WhatsApp estiver invisível, sem registrar qual dos dois ocasionou a omissão. Portanto, não se pode descrever o resultado como 22 comparações geométricas com os dois elementos visíveis. O código ainda executa o clique e a assertiva do estado do controle nessas rotas; o relato de conclusão do helper sustenta essa execução, sem provar presença simultânea do WhatsApp nesses dois casos. Esta é uma limitação da evidência, não demonstração de regressão do produto, e não impede a resolução específica de A1 em `/404`.
- A rodada `internal-hero-fix1` foi executada com `--no-screenshots`. Não usei a antiga imagem `internal-hero-executor-captures/404-320.png` como prova da correção, nem realizei nova inspeção visual completa. A revalidação de A1 nesta revisão usa medidas DOM registradas e leitura independente do código/diff. Capturas canônicas atualizadas e revisão visual final pertencem ao coordenador.
- Não executei testes, browser, check/security, versionamento de assets, build ou diagnósticos MCP/DevTools. Os 18 testes de preservação e demais comandos verdes são resultados reportados pelo executor em `.superpowers/sdd/hero-consistency/task-1-report.md`, seção “Fix round 1”; não execuções deste auditor. Nenhuma alegação de cobertura de todas as alturas, níveis de zoom, navegadores ou transição nativa de abas é feita.
- A única escrita desta revisão é este relatório; nenhum arquivo de produto, índice, branch ou configuração foi alterado pelo auditor.
