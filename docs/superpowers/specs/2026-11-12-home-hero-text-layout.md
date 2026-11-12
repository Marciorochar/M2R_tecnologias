# Ajuste da composição textual do hero

## Diagnóstico e intenção
O H1 atual possui quebra fixa depois de “Ideias conectadas.” e a segunda frase longa ocupa uma coluna estreita. O painel de três itens, com números decorativos, compete com a mensagem principal. Em 320 px, `overflow-wrap: anywhere` pode quebrar palavras arbitrariamente. Ajustar posições e ritmo para que texto e circuitos tenham funções distintas.

## Abordagens
- Centralizar tudo sobre o fundo: simples, mas reduz a área útil para circuitos e CTAs.
- Manter duas colunas com texto dominante à esquerda e painel secundário mais compacto à direita: escolhida por preservar o conceito e ordenar a leitura.
- Deixar apenas texto à esquerda e retirar o painel: menor densidade, mas perde a síntese das áreas.

## Direção visual
Paleta existente: fundo #211610, marrom #362218, bronze #92552d, dourado #efbd7d, branco #ffffff. Mesma fonte do site. Alinhar H1, texto e CTAs pelo mesmo eixo à esquerda; ampliar a coluna de texto; retirar quebra de linha obrigatória e coloração isolada de frase; manter uma medida de leitura controlada. Aproximar descrição do título e separar o apoio dos CTAs por ritmo claro. À direita, reduzir o peso do painel, substituir números sequenciais decorativos por marcadores ou divisores discretos, e abrir espaço para a malha luminosa. Em telas até 900 px, empilhar; em telas pequenas, H1 deve quebrar apenas entre palavras e controles não devem sobrepor o painel.

## Restrições e aceite
Preservar conteúdo essencial, paleta marrom/branco/bronze, circuitos interativos, links e controles. Sem dependências. Não descartar alterações locais anteriores. Verificar ausência de rolagem horizontal e legibilidade em 320, 390, 768 e 1440 px; não afirmar inspeção visual se o navegador local estiver bloqueado.
