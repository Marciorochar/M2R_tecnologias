# UX/CRO integrado — desenho

## Intenção

Tornar mais claro o que a M2R oferece, ligar os cartões da home ao tópico correto, orientar o visitante no contato, agrupar o catálogo existente e alinhar o controle de pausa dos circuitos. O objetivo é reduzir ambiguidades observáveis sem prometer aumento de conversão sem experimento.

## Abordagens consideradas

1. **Ajustes pontuais:** H1, rótulos genéricos para os quatro links, instrução de contato e sincronização da pausa. Menor esforço, mas mantém a busca manual no catálogo.
2. **Percurso integrado — escolhido pelo usuário:** H1 orientado à oferta, âncoras de serviço, catálogo agrupado por objetivo, explicação e hierarquia de contato, pausa coerente e medições com evidência arquivada. Esforço médio; melhora etapas consecutivas sem novo backend.
3. **Formulário com envio próprio / prova social nova:** exigiria backend, tratamento de dados e material comercial autorizado. Fica fora deste escopo; a tabela já restringe envio próprio a decisão futura.

## Resultado desejado

- A home explica a oferta antes de usar o nome da marca como mensagem principal.
- Links de serviços prometem o destino que realmente abrem.
- O catálogo mantém os nove serviços e os agrupa por necessidades já descritas no site.
- O visitante sabe antes de preencher que a mensagem será entregue pelo aplicativo de e-mail; WhatsApp aparece primeiro como canal de contato sugerido, mantendo telefone, e-mail e formulário disponíveis.
- Ao pausar as animações do Hero, vídeo, circuitos e ponto de status ficam em repouso; a preferência `prefers-reduced-motion` continua respeitada.
- Resultados de browser/axe e Lighthouse são registrados por rota/largura e distinguidos de métricas de campo.

## Proposta de conteúdo e navegação

- Marca como eyebrow: **M2R Tecnologias**.
- H1 proposto: **“Sites, sistemas e automações para organizar processos”**. A oferta e o benefício vêm do conteúdo atual da M2R. O restante das soluções continua explicado no subtítulo e na lista de destaques.
- Subtítulo proposto: **“Desenvolvemos soluções digitais sob medida para apresentar marcas, automatizar rotinas e organizar dados.”**
- CTA principal: **“Converse sobre seu projeto”** para `/contato`; CTA secundário: **“Ver serviços”** para `/servicos`.
- Cartões da home: “Desenvolvimento Web” → âncora do serviço correspondente; “Soluções Digitais” → renomear para **“Ver todos os serviços”** e manter `/servicos`, pois o serviço é abrangente; “Automação de Processos” → âncora de automação; “Dashboards e Dados” → âncora de dados/dashboards.
- Página Serviços: manter os nove nomes e descrições. Agrupar cartões sob três títulos editoriais: presença digital (web, sites institucionais, landing pages), operação e informação (automação, dashboards, sistemas personalizados, integrações backend) e soluções e orientação (soluções digitais, consultoria tecnológica). Não criar novos escopos comerciais.
- Página Contato: priorizar visualmente o link de WhatsApp já apresentado como CTA fixo no mobile, sem afirmar que é o canal preferido da empresa. Manter telefone e e-mail direto como alternativas. Colocar a instrução de que o formulário prepara um e-mail para conclusão no aplicativo antes dos campos; manter cópia como fallback.
- Não adicionar depoimentos, métricas, clientes, estudos de caso ou artefatos sem material real e autorização.

## Movimento do Hero

O estado comum em `refreshAnimation()` governa vídeo e `requestAnimationFrame`; o CSS do ponto exige `.motion-paused`, que o JavaScript atual não sincroniza. Atualizar esse estado comum para sincronizar classe/estilo do Hero com pausa manual e movimento reduzido. A pausa, retomada, aba oculta, saída/retorno do viewport e `prefers-reduced-motion` devem permanecer coerentes; não remover o controle nem a identidade de circuitos dourados.

## Escopo técnico

- Páginas estáticas: `frontend/index.html`, `frontend/pages/servicos.html`, `frontend/pages/contato.html`.
- Comportamento e estilo: `frontend/assets/js/hero-circuits.js`, `frontend/assets/js/script.js`, `frontend/assets/css/style.css`.
- Testes e ferramentas existentes: `tools/test_site_tools.py`, `tools/test_hero_circuits.py`, `tools/browser_check.py`, `tools/lighthouse_check.py` e testes correspondentes.
- Evidências de execução: `docs/auditoria/evidencias/`, com screenshots após rolagem/revelação, resultados Axe, tabela responsiva e relatório JSON Lighthouse. Laboratório não será apresentado como CrUX/RUM.
- Reusar Playwright/axe-core/Lighthouse já presentes. Não adicionar dependências nem mudar infraestrutura de produção.

## Não objetivos e restrições

- Não implementar envio de formulário no servidor, CRM, analytics novo, teste A/B ou integração externa.
- Não escolher público-alvo/qualificação comercial sem dados da empresa; descrever apenas serviços e benefícios já declarados.
- Não publicar prova social sem evidência e autorização.
- Não alegar ganho de conversão nem conformidade WCAG com base apenas em score automatizado.
- Preservar a identidade visual marrom, branca e dourada e os circuitos tecnológicos existentes.
- Não publicar/deployar, criar PR ou enviar contato real durante o trabalho.

## Estado do repositório e regra de reconciliação

No início do desenho, a branch local `codex/redesign-visual-m2r` tem vários arquivos unmerged (`UU`), incluindo páginas e stylesheet; os lados 2 e 3 contêm alterações distintas do Hero/circuitos. A comparação read-only encontrou no `frontend/index.html` o Hero antigo no estágio 2 e a implementação de circuitos no estágio 3, com o mesmo conteúdo principal/CTAs; `servicos.html` e `contato.html` diferem apenas na URL versionada do CSS. O CSS do estágio 3 acrescenta a implementação dos circuitos e tokens de movimento. Regra escolhida para preservar a intenção expressa no pedido: manter a estrutura/copy compartilhada e os circuitos dourados do estágio 3, integrar as regras CSS aditivas ao stylesheet base e recalcular as URLs com `tools/version-assets.js`; não restaurar arquivo inteiro de uma ponta nem usar `reset`/`checkout` para descartar alterações.

Uma exploração posterior encontrou um snapshot rastreado desse estado em `refs/stash` (`0edd05481b3b0aabaf465a0b0cc6f857ddf39581`), cujo pai é o commit local `904ac5085a96b5afe93802b8e8eb2b95e4db5091`. Esse snapshot contém HTML/CSS dos circuitos sem marcadores; o JavaScript, vídeo e teste do Hero precisam ser copiados seletivamente do índice atual, pois não estão na árvore rastreada do snapshot. A implementação deve criar um worktree/branch isolado a partir desse snapshot, copiar só esses três arquivos e este documento/plano; não aplicar nem remover o stash, não alterar o worktree original, não importar artefatos Graphify de sua terceira árvore. Conferir hashes dos arquivos copiados e pesquisar marcadores nos arquivos do escopo. Se o conteúdo real divergir do inventário, parar e perguntar ao usuário antes de escolher. A publicação pode não corresponder ao estado local.

## Verificação de aceitação

- Testes direcionados provam os textos aprovados, destinos/IDs, agrupamentos e estado de pausa.
- Browser check percorre as rotas em 320, 390, 768, 1024 e 1440 px, verifica overflow por elemento, menu, foco/reduced motion, formulário e erros JavaScript; evidências de viewport são salvas após revelar o conteúdo.
- Axe verifica as páginas renderizadas. Lighthouse/trace registra dados de laboratório, com rede e viewport declarados; resultados de campo ficam “não disponíveis” se não houver CrUX/RUM.
- Revisão manual confirma a ordem dos canais, legibilidade, identidade visual e que o estado de pausa não deixa movimento visível.

## Aprovação

- O usuário aprovou o percurso integrado em 13/11/2026, incluindo o texto proposto do Hero, o destaque visual do WhatsApp e o agrupamento das nove categorias. O método de execução escolhido é `superpowers:executing-plans`.
