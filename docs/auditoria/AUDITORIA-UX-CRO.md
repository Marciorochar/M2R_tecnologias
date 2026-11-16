# Auditoria profissional de UX, UI e conversão — M2R Tecnologias

**Data:** 13/11/2026  
**Escopo:** diagnóstico da publicação `https://m2rtecnologias.vercel.app/` e confronto limitado com o código local.  
**Status:** somente diagnóstico; nenhum arquivo de produção foi alterado.

## 1. Resumo executivo

A publicação apresenta a M2R como provedora de desenvolvimento web, sites, landing pages, automação, dados e dashboards, sistemas, integrações e consultoria. A home mantém o conceito marrom escuro, branco e dourado com circuitos animados; lista quatro frentes de serviço e leva à página geral de serviços ou ao contato. Não há base de analytics ou experimento para quantificar conversão.

Os pontos de maior potencial de melhoria são: (1) o título principal destaca apenas o nome da empresa, deixando a oferta explícita no texto abaixo; (2) os quatro links dos cartões da home prometem assuntos específicos, mas levam todos ao catálogo geral; (3) o contato exige concluir a mensagem no aplicativo de e-mail, enquanto WhatsApp, telefone e e-mail direto são alternativas; (4) o controle de pausa não interrompe a animação do ponto de status; (5) nas páginas inspecionadas, não se observou prova social verificável que sustente a decisão comercial. O último ponto é limitado às páginas e áreas analisadas; não afirma que tal evidência inexista em outros canais. Os efeitos sobre conversão são hipóteses até serem medidos.

**Cinco prioridades recomendadas:** esclarecer a oferta no Hero; alinhar rótulo e destino dos serviços; reduzir a fricção do contato e apresentar claramente o canal preferencial; sincronizar pausa e animações; acrescentar evidência de trabalho real e pertinente, se disponível e autorizado.

## 2. Metodologia e ferramentas efetivamente utilizadas

- Inspeção ao vivo por Playwright MCP e Chrome DevTools MCP nas rotas `/`, `/servicos` e `/contato`.
- O resumo do testador relata verificações de `documentElement.scrollWidth` e `body.scrollWidth` nas três rotas e nos cinco viewports pedidos (320, 390, 768, 1024 e 1440 px). Essas medições, isoladamente, não provam ausência de overflow; não foi confirmado elemento ultrapassando o viewport. Não foram preservados logs brutos desses 15 pares rota/viewport; essa cobertura é reportada, mas não reproduzível pelos artefatos entregues.
- Interação com menu mobile, foco de teclado, formulário de contato e configuração de movimento reduzido. Console verificado após navegação: zero erros reportados.
- Inspeção das páginas e scripts locais como evidência auxiliar. O workspace local contém conflitos Git não resolvidos e marcadores de conflito em HTML/CSS; a publicação consultada serve outros assets e não apresenta esses marcadores. Portanto, problemas encontrados só na árvore local não foram classificados como defeitos publicados.
- Capturas full-page existentes em `docs/auditoria/`: `home-320.png`, `home-390.png`, `home-1440.png`, `servicos-320.png`, `servicos-390.png`, `servicos-1440.png`, `contato-320.png`, `contato-390.png`, `contato-1440.png` e `evidencia-home-320.png`. Não há capturas salvas de 768 ou 1024 px. As capturas de 320/390 mostram grandes áreas vazias entre algumas seções, compatíveis com conteúdo de revelação ainda não ativado durante a captura full-page; não permitem concluir que a página em uso tenha espaços vazios. Nenhuma captura registra por si só todos os estados interativos.
- Skills consultadas: `design-taste-frontend` e `ecc:accessibility`; usadas como referências de avaliação, sem aplicar suas prescrições estilísticas que conflitassem com a identidade solicitada.
- Playwright e Chrome DevTools estavam disponíveis. Lighthouse e métricas Core Web Vitals não foram executados. Agent-browser não foi usado. A primeira abertura Playwright falhou porque outra instância já ocupava o navegador; a auditoria prosseguiu pelo Chrome DevTools.

**Rubrica das notas:** quando o princípio se aplica ao percurso, cinco critérios observáveis recebem 0 (barreira observada), 1 (atendimento parcial ou evidência inconclusiva) ou 2 (atendido na inspeção); a nota é a soma de 0 a 10. Um ponto 1 usado por falta de medição representa incerteza, não problema confirmado nem evidência de atendimento. Por isso, notas com critérios não medidos são triagens provisórias e não devem ser comparadas como resultados quantitativos. Os critérios e pontos estão discriminados por princípio abaixo. A Lei de Zeigarnik é indicada como N/A quando o percurso não contém tarefa progressiva relevante. As notas não medem satisfação nem conversão. Confiança: alta para interação direta publicada; média para julgamento qualitativo/editorial; baixa quando depende de preferência ou dados não disponíveis.

### Mapa de cobertura e evidências arquivadas

O testador relata verificação das três rotas nos cinco tamanhos. Só existem capturas full-page nas três larguras abaixo; não foram arquivados logs de largura/overflow para os outros tamanhos. “Relatado” identifica evidência do resumo de execução, não artefato reproduzível.

| Rota | 320 px | 390 px | 768 px | 1024 px | 1440 px |
|---|---|---|---|---|---|
| Home `/` | Relatado; PNG full-page | Relatado; PNG full-page | Relatado; sem captura/log | Relatado; sem captura/log | Relatado; PNG full-page |
| Serviços `/servicos` | Relatado; PNG full-page | Relatado; PNG full-page | Relatado; sem captura/log | Relatado; sem captura/log | Relatado; PNG full-page |
| Contato `/contato` | Relatado; PNG full-page | Relatado; PNG full-page | Relatado; sem captura/log | Relatado; sem captura/log | Relatado; PNG full-page |

Menu foi aberto em mobile e primeiro Tab alcançou o link de salto. Não há registro da sequência completa de teclado em cada rota, nem logs de hover/foco/click por largura. Dimensões de alvos, razões de contraste e contato até a entrega final ao app externo não foram medidos. A pausa e movimento reduzido foram exercitados; console sem erros é reportado sem log bruto salvo. As imagens full-page em 320/390 têm grandes áreas vazias em algumas seções, compatíveis com conteúdo de revelação não ativado durante a captura; não são evidência de espaço vazio na experiência após rolagem natural.

## 3. Avaliação das 12 leis de UX

| Princípio | Nota / critérios (0–2 cada, subtotal) | Evidência e elemento/página | Problema / status | Correção recomendada | Prioridade / confiança |
|---|---|---|---|---|---|
| Jakob | 8/10: logo para início 2; rótulos familiares 2; padrão de navegação consistente 2; menu mobile previsível 2; destino corresponde ao rótulo 0. | Navegação global nas três rotas; menu mobile abriu e atualizou `aria-expanded`; quatro links de serviço na home levam a `/servicos`. | **Confirmado:** os quatro destinos são genéricos. **Hipótese:** a falta de correspondência aumenta busca/esforço. | Manter navegação; criar âncoras estáveis por serviço ou esclarecer que os links abrem o catálogo. | Média / alta |
| Hick | 7/10: duas ações no Hero 2; agrupamento visível 2; orientação de escolha 1; progressão até CTA 1; rótulos reconhecíveis 1. | Home oferece duas ações; Serviços enumera nove categorias em cartões e um CTA final. | **Confirmado:** nove categorias estão listadas. **Hipótese:** sem orientação, parte dos visitantes pode ter dificuldade de escolher. | Agrupar por objetivo e explicar brevemente a aplicação de cada grupo sem criar ofertas novas. | Média / média |
| Fitts | 7/10: tamanho dos alvos 1 (não medido); espaçamento 2 (inspeção visual); localização 2; ausência de obstrução 1 (clique automatizado inconclusivo); uso por teclado 1 (teste parcial: primeiro Tab chegou ao link de salto). | Menu/CTAs móveis e WhatsApp fixo. A tentativa de clique automatizado no controle foi interceptada ao rolar junto à navegação fixa; clique DOM funcionou. | **Inconclusivo:** a interceptação não confirma barreira para pessoas. Dimensão dos alvos e percurso completo por teclado não foram medidos. | Repetir teste manual de toque/teclado e medir alvos/obstruções antes de atribuir defeito. | Baixa / baixa |
| Miller | 7/10: grupos por seção 2; títulos de grupo 2; densidade 1; reconhecimento sem memorização 1; continuidade entre seções 1. | Home organiza sobre, serviços, projeto, CTA e rodapé; Serviços tem nove cartões. | **Confirmado:** existem nove cartões. **Hipótese:** a quantidade sem agrupamento por problema pode elevar carga de comparação. | Agrupar serviços relacionados e resumir as opções antes dos detalhes. | Média / média |
| Von Restorff | 6/10: contraste do CTA primário 2; destaque exclusivo 1; rótulo da ação 1; hierarquia consistente 1; decoração não compete 1. | “Conheça os serviços” é CTA primário e “Fale conosco” secundário; marca é o H1. | **Confirmado:** essa é a hierarquia visual/copy atual. **Hipótese:** priorizar contato pode melhorar foco comercial; sem dados de contato, não há efeito comprovado. | Testar hierarquia de conversa primária e catálogo secundário. | Alta / média |
| Estética-usabilidade | 8/10: paleta coerente 2; identidade tecnológica 2; consistência de componentes 2; credibilidade por conteúdo 1; estado visual/funcional coerente 1. | Cores marrom/branco/dourado, circuito SVG/vídeo; interação de pausa no Hero. | **Confirmado:** ao pausar, o ponto de status permaneceu animado. **Hipótese:** estado incompleto pode reduzir percepção de controle. | Sincronizar pausa com todas as animações que o controle anuncia controlar. | Média / alta |
| Proximidade | 8/10: heading e conteúdo 2; CTA e proposta 2; label e campo 2; separação dos grupos 1; relações preservadas no mobile 1. | Cartões e campos com labels; formulário é habilitado após JavaScript. | **Confirmado:** labels associados na fonte. **Hipótese:** explicar o passo do e-mail mais cedo pode melhorar expectativa. | Explicar conclusão externa junto à escolha do canal e preservar agrupamento visual. | Baixa / média |
| Posição serial | 7/10: oferta no início 1; próximo passo visível 2; evidência antes da decisão 1; CTA de encerramento 2; rodapé funcional 1. | Home começa com marca e oferta genérica, mostra projeto em desenvolvimento e termina com CTA. | **Confirmado:** essa sequência e o estado “Em desenvolvimento”. **Hipótese:** a mensagem inicial pouco específica e a pertinência do projeto podem reduzir clareza comercial. | Priorizar oferta; mostrar artefatos reais pertinentes, quando existentes e autorizados. | Média / média |
| Pico-final | 8/10: início do contato claro 2; etapa externa explicada 2; retorno ao preparar/copiar a mensagem 1; alternativa disponível 2; estado de conclusão sem falsa confirmação 1. | Página declara que o formulário prepara e-mail; há alternativas tel/e-mail/WhatsApp/cópia. | **Confirmado:** o fluxo prepara a mensagem e deixa a entrega para o app externo. **Hipótese:** a troca de contexto pode reduzir conclusão; não foi medida. A ausência de envio pelo site não é tratada como falha, pois esse fluxo é informado. | Manter explícito o passo externo; priorizar canal; em etapa futura autorizada, avaliar envio próprio e confirmação verdadeira. | Média / média |
| Doherty | 8/10: resposta de controles 2; navegação observada 2; feedback de estado 2; estabilidade visual 1 (não medida); desempenho sob carga 1 (não medido em Lighthouse/trace). | Os controles acionados e a navegação responderam na sessão; vídeo readyState 2; console sem erros reportados. | **Observação qualitativa:** controles e navegação responderam na sessão; tempos não foram medidos. **Não medido:** LCP, INP e CLS; a nota não representa velocidade quantificada. | Medir laboratório e campo; só então priorizar peso de vídeo/circuitos e latência. | Baixa / baixa |
| Tesler | 6/10: ajuda para escolher 1; contexto preservado 0; dados pedidos pertinentes 2; quantidade de passos 2; dependência externa/alternativas 1. | Nove serviços; cartões da home chegam ao catálogo; contato pede nome, e-mail, telefone opcional e mensagem. | **Confirmado:** destino genérico e etapa externa por e-mail. **Hipótese:** esforço adicional para mapear intenção e concluir contato. | Preservar serviço de origem com âncora/contexto; manter dados mínimos; medir conclusão por canal. | Alta / média |
| Zeigarnik | **N/A neste percurso** | O contato é uma tarefa curta, sem etapas progressivas nem estado que precise ser retomado. A mensagem preparada é entregue pelo aplicativo externo. | A lei tem baixa aplicabilidade aqui; não se atribui nota nem se trata a ausência de progresso como problema. | Manter explícito o passo restante no app externo; não criar progresso artificial. | — / média |

**Como interpretar:** achados confirmados descrevem elementos/estados verificados. Impactos comportamentais e recomendações são hipóteses até teste com usuários ou dados. Um ponto 1 em item não medido indica somente evidência inconclusiva; não deve ser lido como falha observada. As notas de Fitts e Doherty são triagens qualitativas; não substituem medição de alvo, latência ou Core Web Vitals. Zeigarnik não foi pontuada por não haver tarefa progressiva relevante no percurso observado.

## 4. Auditoria visual e responsiva

### Achados confirmados

- A identidade visual existente está refletida no Hero: fundo escuro, texto claro, destaques dourados e circuito interativo. O vídeo foi carregado na sessão observada.
- Hierarquia da home: H1 “M2R Tecnologias”; descrição “Soluções digitais, desenvolvimento web e projetos tecnológicos sob medida”; suporte cita apresentação de marcas, organização de processos, tecnologia, automação e inovação. A mensagem é coerente com os serviços, porém genérica como proposta inicial.
- Em 320 e 390 px, a navegação é recolhida em botão; o botão abriu o menu e alterou `aria-expanded` para `true`. A versão desktop usa links horizontais.
- Nos cinco tamanhos testados não se confirmou conteúdo transbordando horizontalmente; o delta de 15 px nas medidas da página é compatível com a barra de rolagem do navegador. Revalidar em aparelhos reais e zoom de 200–400%.
- A captura de 320 px mostra os CTAs empilhados e as categorias de serviço resumidas em linhas no Hero; o CTA WhatsApp fica fixo e visível. Há risco de competição espacial com o conteúdo em telas curtas, a validar por inspeção física e acessibilidade de zoom.

### Hipóteses de melhoria

- Avaliar ritmo vertical e ocupação de tela no mobile em estados após as animações/revelações; capturas automáticas de página inteira podem não reproduzir fielmente a rolagem natural.
- Revisar contraste calculado de texto dourado/cinza sobre marrom e estados hover/foco com ferramenta WCAG; nesta rodada não foram obtidas razões numéricas de contraste.
- Preservar o circuito como acento tecnológico, verificando que o brilho não compete com texto ou ações em cada largura.

## 5. Auditoria de conversão

**Público-alvo:** o site não nomeia segmentos, setores ou perfis de compradores de forma explícita nas páginas inspecionadas. As referências a marcas, processos, equipes internas e operações sugerem organizações e pessoas que precisam de presença digital ou ferramentas digitais, mas isso é inferência a partir do texto publicado. Não se deve inventar segmento mais específico.

**Percurso observado:** entrada na home → compreensão geral da oferta → CTA “Conheça os serviços” ou “Fale conosco” → catálogo de nove serviços ou página de contato → WhatsApp, telefone, e-mail direto ou formulário que prepara mensagem para o aplicativo de e-mail e oferece cópia como alternativa. O handoff foi verificado apenas até o controle/link disponibilizado; não foi enviado contato comercial nem confirmado recebimento.

O site não define o que torna um contato “qualificado” (por exemplo, critérios de escopo, orçamento, prazo ou perfil). Sem critério fornecido pela empresa, a auditoria pode avaliar fricção e clareza do caminho, mas não classificar ou otimizar qualificação comercial.

| Critério | Observação confirmada | Implicação / hipótese |
|---|---|---|
| Proposta de valor | Home cita soluções digitais, desenvolvimento web e projetos sob medida; suporte cita marcas, processos, automação e inovação. | A abrangência pode dificultar identificação imediata do caso de uso; testar formulação orientada ao problema. |
| CTA | Dois CTAs no Hero; serviços como ação primária e contato secundário. CTA final leva ao contato. | A hierarquia atual favorece exploração antes da conversa; pode ser adequada a visitantes frios, mas não há dados para decidir. |
| Compreensão dos serviços | Quatro grupos na home; nove serviços detalhados na página Serviços, incluindo automação, dashboards, sistemas, integrações e consultoria. | Amplitude confirmada; falta caminho direto para cada serviço a partir dos quatro cartões da home. |
| Confiança | Projeto próprio M2R Server é descrito como “Em desenvolvimento”; não foram observados depoimentos/resultados verificáveis nas áreas inspecionadas. | Projeto é transparência legítima, mas a adequação como prova comercial para outras ofertas é hipótese. Não inventar cases, números ou clientes. |
| Facilidade de contato | Telefone, e-mail, WhatsApp e formulário que prepara e-mail/copia mensagem. | Dependência de aplicativo externo e escolha entre canais acrescentam esforço. Perda de conversão é hipótese, não medida. |
| Consistência | Contato usa linguagem de conversa e oferece múltiplos canais; cópia explica o funcionamento. | Tornar o canal recomendado explícito pode reduzir indecisão; validar com testes de usuário. |

## 6. Performance e acessibilidade

### Performance

- **Métricas de campo (CrUX/RUM):** não disponíveis. Não há LCP, INP ou CLS de usuários reais.
- **Laboratório:** Lighthouse e trace de performance não foram executados. Portanto, nenhum valor numérico de Core Web Vitals é reportado.
- **Observações:** erro JavaScript no console: nenhum na sessão observada. Vídeo do Hero estava carregado e em reprodução; isso não determina seu custo total de rede ou impacto de desempenho. Verificar byte weight, carregamento sob rede móvel, poster/fallback e estabilidade de layout em medição futura.

### Acessibilidade (triagem WCAG 2.2; não declaração de conformidade)

- Primeiro Tab focou “Pular para conteúdo”, como esperado; controles nativos e links foram usados no percurso. Menu atualizou o estado acessível. Os campos ativados tinham rótulos associados na inspeção de fonte.
- `prefers-reduced-motion: reduce` foi reconhecido; o filme reduziu sua duração computada para aproximadamente `0.00001s`. O controle de movimento pausou o vídeo e atualizou o texto/estado para “Animações pausadas”, mas a animação do ponto de status permaneceu `running` — inconsistência confirmada.
- A tentativa de clique por coordenadas no controle de movimento encontrou a navegação fixa no caminho ao rolar; como o clique DOM confirmou a ação, a interceptação pode decorrer da automação/rolagem, sem confirmação de bloqueio para usuário real.
- Não foram calculados contrastes numéricos, não houve leitor de tela e não foi executada auditoria automatizada Axe/Lighthouse. Revisar contrastes, foco visível em todos os fundos, alvos de toque, zoom/reflow e sobreposição do CTA fixo com conteúdo/controles.

## 7. Matriz de problemas

A matriz completa está em [Matriz de problemas UX-CRO corrigida.xlsx](Matriz-de-problemas-UX-CRO-corrigida.xlsx). As prioridades combinam impacto esperado, confiança da evidência e esforço estimado. “Impacto esperado” é avaliação qualitativa, não previsão de aumento percentual.

## 8. Cinco melhorias prioritárias

1. **Reescrever a hierarquia do Hero:** tornar a categoria de trabalho e o benefício já sustentado pelo site legíveis antes do nome da empresa; medir compreensão em teste moderado.
2. **Correspondência dos links de serviço:** apontar cada cartão da home para sua seção correspondente na página Serviços, ou renomear o link para indicar “ver todos os serviços”.
3. **Contato com menos incerteza:** explicar junto ao formulário que a conclusão ocorre no cliente de e-mail; destacar um canal principal com alternativas claras. Se houver autorização futura, avaliar envio próprio com confirmação verdadeira.
4. **Pausa coerente:** fazer o estado de pausa interromper também o indicador animado que permanece em movimento; confirmar com preferência de movimento reduzido e botão manual.
5. **Evidência de credibilidade pertinente:** exibir artefatos/capturas e escopo real de trabalho, relacionando capacidades transferíveis sem atribuir resultados não documentados; só usar cases/depoimentos autorizados.

## 9. Propostas de textos e interface

As sugestões abaixo usam apenas serviços e objetivos declarados pela M2R; são hipóteses de clareza para validação, não alegações de resultado.

| Elemento | Original publicado | Proposta | Justificativa |
|---|---|---|---|
| Título (H1) | “M2R Tecnologias” | “Sites, automação e sistemas para organizar seu negócio” | Nomeia serviços já apresentados e liga automação/sistemas ao objetivo de organização declarado. Manter “M2R Tecnologias” como marca/eyebrow. |
| Subtítulo | “Soluções digitais, desenvolvimento web e projetos tecnológicos sob medida.” | “Desenvolvemos sites, automações, dashboards e sistemas personalizados para apresentar sua marca e organizar processos.” | Concretiza a oferta e reutiliza descrições já existentes nas páginas. |
| CTA principal | “Conheça os serviços” | “Converse sobre seu projeto” | Direciona ao contato como ação comercial; comparar com CTA atual em teste. |
| CTA secundário | “Fale conosco” | “Ver serviços” | Dá uma ação de exploração secundária com verbo e destino explícitos. |
| Hero | H1 de marca, dois parágrafos explicativos, dois CTAs e três destaques | Eyebrow “M2R Tecnologias”; H1 orientado à oferta; um parágrafo curto; CTA principal de conversa; secundário de serviços; manter três destaques como resumo | Reduz repetição da marca e melhora leitura inicial sem remover circuito, cor ou personalidade visual. |
| Serviços | Nove cartões em grade; quatro links da home convergem para `/servicos` | Agrupar por presença digital, operação/automação e sistemas/dados; ancorar cada cartão da home; CTA contextual no fim de cada grupo | Facilita varredura e conserva catálogo existente; não implica criar páginas novas. |
| Contato | Formulário prepara e-mail, oferece cópia e lista tel/e-mail/WhatsApp | Título “Escolha como prefere conversar”; canais em ordem clara; nota curta antes do formulário: “O formulário prepara uma mensagem para seu aplicativo de e-mail; você conclui o envio por lá.” | Define expectativa antes do esforço e reduz falsa impressão de envio pelo site. |

## 10. Critérios para validar após implementação

1. **Compreensão:** em teste moderado com público-alvo definido pelo negócio, pedir que participantes expliquem em palavras próprias o que a M2R oferece e para quem; registrar acerto e dúvidas sem indução.
2. **Navegação de serviço:** verificar se cada link da home chega ao serviço nomeado e preserva o contexto; validar teclado, leitor de tela e link direto.
3. **Contato:** registrar eventos consentidos de clique por canal, início/conclusão do fluxo próprio (se vier a existir) e erros; distinguir abrir `mailto:` de mensagem realmente enviada. Não contar abertura como lead recebido.
4. **Experimento comercial:** comparar CTA/hero com hipótese, população, duração e métrica primária previamente definidos; reportar tamanho de amostra e incerteza. Não inferir ganho sem evidência.
5. **Responsividade:** repetir 320, 390, 768, 1024 e 1440 px, além de zoom 200–400%, em navegadores/aparelhos reais; verificar overflow geométrico por elemento, menu, CTA fixo, formulário e orientação.
6. **Acessibilidade:** executar auditoria WCAG 2.2 AA com ferramenta automatizada e revisão manual (teclado, leitor de tela, contraste calculado, movimento reduzido, foco, alvos e zoom); registrar critérios e achados, sem tratar score automático como conformidade.
7. **Movimento:** testar alternância de pausa, `prefers-reduced-motion`, aba em segundo plano e retorno; confirmar que texto, estado acessível, vídeo, pontos e demais animações concordam.
8. **Performance:** rodar Lighthouse/trace em mobile e desktop com rede/CPU registrados; obter métricas de laboratório separadas de CrUX/RUM. Avaliar LCP/INP/CLS somente quando medidos; usar p75 de campo para decisões de Core Web Vitals.

## Plano técnico de correções (para etapa futura autorizada)

1. Definir mensagem e CTA por hipótese comercial, preservando tokens de cor, circuito e estrutura estática existente.
2. Adicionar IDs/âncoras e ajustar destinos dos cartões sem introduzir arquitetura nova; atualizar testes de links.
3. Revisar o mecanismo de contato e estados de feedback conforme canal e capacidade aprovados pelo negócio.
4. Alinhar estado de pausa no JS/CSS e testar preferência de movimento.
5. Preparar inventário de artefatos reais e autorização de publicação; não fabricar prova social.
6. Corrigir e reconciliar, antes de implementar, os conflitos Git no workspace local. Eles não foram considerados defeitos da publicação auditada.
7. Validar nos cinco breakpoints, auditoria manual/automatizada de acessibilidade, performance medida e experimento/analytics; registrar evidência por mudança.

---

**Limites:** revisão de interface e conteúdo, não pesquisa com usuários nem análise de analytics; teste de interação restrito às sessões e dispositivos emulados; nenhum resultado comercial foi inferido como fato. A publicação pode mudar após a data da auditoria.
