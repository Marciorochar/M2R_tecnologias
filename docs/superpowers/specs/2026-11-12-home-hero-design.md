# Redesenho do hero da página inicial

## Intenção
Tornar a primeira dobra da M2R mais reconhecível e clara para visitantes interessados em sites, automação e dados, preservando circuitos dourados, paleta marrom e branco e os dois caminhos de conversão.

## Diagnóstico
O nome da empresa como título principal comunica pouco valor; a descrição e o apoio repetem conceitos; a malha de circuitos e o vídeo não têm um ponto focal e ficam parcialmente escondidos pelas camadas escuras. Os itens de serviços parecem etiquetas genéricas.

## Abordagens consideradas
1. Refinar apenas cores e tamanhos: baixo esforço, impacto limitado na mensagem.
2. Composição editorial com mensagem concreta à esquerda e painel técnico à direita: melhora hierarquia e preserva o conceito de circuitos. **Escolhida pelo usuário ao delegar decisões de design.**
3. Substituir por vídeo em tela cheia: dá protagonismo à animação, mas compromete leitura e diferenciação.

## Design
Manter a marca em etiqueta, trocar o H1 por promessa curta ligada a tecnologia aplicada a negócios e usar texto de apoio conciso sobre sites, automação e dados. Preservar os links de serviços e contato. À direita, criar um painel translúcido com três capacidades apresentadas com tipografia e separadores, sem métricas inventadas ou promessas não comprovadas. Reservar área desobstruída para os caminhos SVG e o acionador do pulso. Usar contraste alto, foco visível, sem animação obrigatória e empilhamento fluido em telas estreitas.

## Restrições
Não remover o trabalho local em andamento. Reutilizar HTML/CSS atuais, sem dependências novas. O arquivo de vídeo referenciado não existe no repositório: retirar a referência quebrada e sustentar o visual com SVG/CSS. Preservar funcionamento de hero-circuits.js, botões de movimento, `prefers-reduced-motion` e navegação. Atualizar hashes de assets nas páginas com o gerador existente.

## Critérios de aceite
Hero legível a 320, 390, 768 e 1440 px; sem rolagem horizontal; CTAs e controles acessíveis; circuito perceptível sem cobrir texto; testes existentes continuam passando.
