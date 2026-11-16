# Padronização do halo do ponteiro nos Heroes

## Intenção

Reduzir o círculo de luz que acompanha o mouse e dar ao efeito o mesmo tamanho na Home e nas páginas internas. O efeito deve continuar perceptível, sem dominar o conteúdo ou parecer maior na Home.

## Objetivos e limites

- Usar raio `72` nos dois círculos criados pelo sistema de Hero.
- Preservar o gradiente e a intensidade mais expressiva da Home.
- Preservar movimento, pulsos, parallax, clique e estados de pausa existentes.
- Não alterar o tamanho dos pulsos nos circuitos nem os anéis criados por clique.
- Manter o efeito desativado para toque e movimento reduzido conforme o comportamento atual.

## Abordagens consideradas

1. **Um único tamanho compartilhado — escolhida.** Home e internos usam raio `72`; a diferenciação da Home continua em cor, gradiente e opacidade. Produz consistência e impede divergência futura.
2. **Dois tamanhos proporcionais.** Manteria a Home um pouco maior, mas conservaria dois números e reduziria a padronização desejada.
3. **Um único halo por página.** Evitaria sobreposição na Home, porém criaria uma estrutura diferente entre as variantes e mudaria mais comportamento do que o necessário.

## Implementação proposta

Definir uma constante compartilhada no runtime comum, exposta ao complemento da Home pelo evento `m2rhero:ready`. O runtime usa essa constante ao criar `.hero-system__halo`; a Home usa o mesmo valor ao criar `.m2r-cursor-halo`. Isso centraliza o tamanho sem transformar uma medida SVG em variável CSS que não controla diretamente o atributo `r`.

Os testes devem verificar que os dois círculos usam raio `72`, que não restam os valores `110` e `119` nesses pontos e que o ciclo de movimento e os fallbacks continuam passando no navegador.

## Resultado esperado

Ao mover o mouse sobre os circuitos, o círculo iluminado terá aproximadamente 60% do raio atual da Home. Home e páginas internas ocuparão a mesma área ao redor do ponteiro, enquanto a Home continuará visualmente mais luminosa.
