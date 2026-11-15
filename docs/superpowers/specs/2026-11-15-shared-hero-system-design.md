# Sistema visual compartilhado dos Heroes M2R

## Intenção

Unificar a base visual, os circuitos e os controles de movimento da Home e dos Heroes das rotas internas. A identidade da Home é a referência aprovada; cada página mantém seu conteúdo, seus painéis e a composição que serve àquela rota.

O objetivo é que a pessoa reconheça um mesmo sistema M2R ao navegar pelo site, sem transformar artigos, páginas de serviço, projeto detalhado e erro 404 em cópias da Home.

## Estado atual

- A Home em `frontend/index.html` usa `home-hero--circuits`, vídeo decorativo, SVG embutido, animação conduzida por `hero-circuits.js`, efeito de ponteiro, ativação de circuito e controle de movimento.
- Os 11 destinos internos usam `page-hero--circuits`, `internal-hero.css` e `internal-hero.js`. O SVG `frontend/assets/img/hero-circuits.svg` fornece uma imagem estática e o script interno cria pulsos e halo de ponteiro sobre ela.
- Os dois sistemas compartilham os 14 traçados, mas mantêm regras próprias para gradiente, apresentação dos circuitos, animação e controle. Os gradientes atuais não são idênticos.
- Artigos, projeto detalhado e 404 têm arranjos específicos. A Home tem painel próprio de áreas de atuação. O 404 existe em `404.html` e `frontend/404.html`.
- O spec anterior proibia mudanças na Home para manter o trabalho interno isolado. A decisão do usuário nesta conversa substitui essa restrição: a unificação agora deve alcançar a Home também.

## Objetivos

- Definir uma única base de tokens e regras para cores, superfícies, traçados, pulsos, controles, foco e movimento dos Heroes.
- Usar a mesma fonte geométrica dos circuitos em todas as páginas.
- Dar aos controles de movimento aparência, rótulo, operação por teclado e resposta a `prefers-reduced-motion` coerentes.
- Manter variantes de layout e elementos específicos por rota sem duplicar o sistema visual.
- Preservar a aparência aprovada da Home como referência e trazer os Heroes internos para a mesma família visual.
- Manter fallback visual funcional quando JavaScript, busca do SVG ou aprimoramento de movimento falharem.

## Fora de escopo

- Trocar a direção visual aprovada ou redesenhar a Home.
- Copiar o vídeo da Home para as páginas internas.
- Tornar iguais a altura, o conteúdo, os metadados, os painéis ou a ordem dos elementos em todas as rotas.
- Alterar textos, destinos de links, conteúdo fora dos Heroes, breadcrumbs, navegação global ou configuração de produção.
- Introduzir framework, biblioteca ou dependência nova.
- Deploy ou merge do PR.

## O que faria o trabalho falhar

- A Home e uma página interna continuarem com cores, circuitos ou controles visivelmente incompatíveis.
- A unificação ser feita duplicando indefinidamente regras de Home e internas em folhas diferentes.
- O sistema comum remover conteúdo, ações ou hierarquia próprios de alguma página.
- As animações continuarem sem pausa acessível, ignorarem redução de movimento ou ficarem executando fora da tela.
- Uma falha de JavaScript remover texto, navegação, CTA ou a imagem estática dos circuitos.
- O WhatsApp fixo voltar a cobrir o CTA ou um controle nos viewports móveis já cobertos pelo CI.

## Alternativas consideradas

1. **Unificar somente os aspectos visuais.** Compartilhar tokens, gradiente, cores, tipografia, espaçamento, traços e estilo dos controles, mantendo a lógica de animação de cada sistema. Tem menor alcance, mas mantém duas implementações de movimento e permite que voltem a divergir.
2. **Criar uma base compartilhada com variantes.** Home e internos compartilham tokens, fonte dos circuitos, pulsos e controle de movimento. Camadas adicionais preservam as interações exclusivas da Home; variantes conservam composições e conteúdo por rota. **Escolhida pelo usuário.** Dá consistência sistêmica sem repetir vídeo ou impor a composição da Home a todas as páginas.
3. **Reproduzir a Home inteira em cada Hero.** Copiar vídeo, painel, composição e todas as interações para todas as rotas. Maximiza semelhança literal, mas repete elementos da Home, aumenta custo de carregamento e não respeita a diversidade dos conteúdos.

## Decisões confirmadas

- A opção escolhida é a base compartilhada com variantes.
- Todas as rotas usam a mesma base visual, os mesmos circuitos e o mesmo padrão de controle de movimento.
- Conteúdo, painéis e composição permanecem específicos por página.
- A Home pode manter vídeo, ativação por clique, efeito de ponteiro ou outras interações exclusivas, desde que se apoiem na base comum e não alterem a operação dos controles compartilhados.
- O vídeo continua restrito à Home.

## Direção para implementação

- Extrair uma única camada comum para tokens e estilos de superfície, circuitos, estados de movimento, controles e foco. Home e páginas internas carregam essa base; regras específicas ficam em variantes explícitas.
- Manter a geometria dos circuitos em uma fonte canônica compartilhada. A mesma arte estática permanece visível sem JavaScript; aprimoramentos animados são camadas opcionais sobre ela.
- Usar um controle comum de pausa/retomada para animações comuns. Ele inicia respeitando `prefers-reduced-motion`, permite teclado, expõe `aria-pressed` e não aparece funcionalmente quando o movimento está indisponível.
- Pausar movimento quando a página estiver oculta ou o Hero fora da tela, sem sobrescrever uma pausa manual.
- Tratar vídeo, ripples acionados por clique, destaque do ponteiro e painel da Home como complementos opcionais da variante Home. As variantes internas não carregam o vídeo.
- Preservar as variantes para Heroes simples, artigos, projeto detalhado e 404 sem forçar wrappers que quebrem grids ou metadados existentes.
- Manter `404.html` e `frontend/404.html` equivalentes.
- Respeitar a CSP atual: arquivos locais, sem script ou estilo inline novo.
- Ao mudar CSS ou JavaScript versionado, regenerar os hashes HTML com `tools/version-assets.js`.

## Critérios de aceitação

- As rotas Home e internas apresentam o mesmo tratamento base de cor, gradiente, circuito, movimento e controle, com variações locais claramente intencionais.
- As variantes preservam seus textos, links, breadcrumbs, metadados, painéis e ações.
- A fonte visual estática dos circuitos continua disponível sem JavaScript; falha de carregamento ou parsing não bloqueia o conteúdo.
- O controle compartilhado funciona com teclado e leitor de tela, respeita movimento reduzido e pausa fora de tela/aba oculta.
- Não há overflow ou colisão com WhatsApp/CTA em 320, 390, 768, 1024, 1440 e 1920 px, nem em títulos longos, projeto detalhado ou 404.
- `404.html` e `frontend/404.html` usam a mesma variante e os mesmos assets.
- A checagem de hashes, verificações estáticas e `tools/browser_check.py` passam; comparação visual confirma a base comum sem exigir layouts idênticos.

## Chamadas de implementação deixadas ao executor

- Escolher a divisão de arquivos e nomes de classes que melhor reduza sobreposição com as folhas atuais, mantendo uma fonte de verdade para cada token e estado.
- Migrar por incrementos verificáveis e retirar regras antigas somente quando todos os consumidores usarem a base comum.
- Manter os seletores de variante simples e explícitos, sem criar um sistema genérico de componentes além das necessidades atuais do site estático.
- Produzir capturas comparáveis de antes/depois nos seis viewports e páginas que cobrem cada variante.

## Referências

- Implementação atual: `frontend/index.html`, `frontend/assets/css/style.css`, `frontend/assets/js/hero-circuits.js`, `frontend/assets/css/internal-hero.css`, `frontend/assets/js/internal-hero.js` e `frontend/assets/img/hero-circuits.svg`.
- Inventário consultado: `C:\Users\marci\Documents\Inventario_IA_2026-11-13\apoio\skills_principais.tsv`. A skill `ecc:design-system` é o apoio principal para auditar e alinhar tokens/componentes; `frontend-design-direction` é um complemento se surgir uma decisão de direção, não necessária para copiar uma referência já definida. O inventário informa que a adequação é documental e não um ranking experimental.
- Skills de processo aplicadas: `superpowers:brainstorming`; a etapa seguinte, após aprovação deste documento, é `superpowers:writing-plans`.
