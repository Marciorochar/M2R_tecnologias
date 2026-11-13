# Padronização dos Heroes M2R

Tipo: serviço de desenvolvimento web, sistemas e automação, com identidade tecnológica existente.

## Intenção e limites
Aplicar a linguagem visual oficial da Home em todas as 11 rotas internas, incluindo três artigos, projeto detalhado e 404 (ambas as cópias). Preservar literalmente `frontend/index.html`, `frontend/assets/css/style.css`, `frontend/assets/js/hero-circuits.js` e o vídeo. Preservar conteúdo fora dos Heroes, títulos, subtítulos, breadcrumbs, metadados e CTAs existentes. Sem frameworks, alteração da configuração de produção, deploy ou merge.

## Diagnóstico
Base: origin/main `7436829`. Checkout original tem merge pendente e 15 arquivos em conflito; foi preservado. Trabalho em `codex/hero-consistency-2026-11-13`, worktree separado. Home publicada inspecionada com Playwright MCP. Detalhes em `docs/hero-standardization/exploration.md`. Testes de base: 59 testes, 54 subtestes passaram.

## Alternativas e decisão técnica
1. Generalizar o script e CSS da Home: menos código inicial, porém risco de regressão na referência explicitamente protegida.
2. SVG compartilhado extraído dos caminhos existentes, CSS interno e aprimoramento progressivo: escolhido pelo coordenador, permite manter a Home byte a byte e circuitos estáticos sem JavaScript. Movimento usa CSS e pausa fora da tela, sem vídeo adicional.
3. Copiar SVG, vídeo e lógica por documento: descartado por duplicação e custo.

A execução contínua foi explicitamente autorizada pelo usuário; não houve escolha de nova direção visual nem solicitação de confirmação intermediária.

## Sistema visual preservado
Fundo radial da Home: `#644026`, `#362218`, `#211610`, `#1b130f`; texto `#ffffff`; ouro `#f1c994`; ações usam tokens bronze já existentes. Fonte system-ui existente. Títulos balanceados, alinhados à esquerda; largura de conteúdo até 1200px e margens iguais. Nos Heroes simples, texto ocupa aproximadamente 62% da largura, circuitos à direita. Projeto e 404 mantêm grade e painel. Em <=900px, conteúdo ocupa toda a largura, decoração atenuada. Botões empilhados e de largura total em <=640px. Altura interna menor que Home de propósito, sem cortes nem min-height fixo que impeça crescimento.

```text
desktop: | título + descrição + CTA | circuitos / painel existente |
mobile:  | título + descrição + CTA em coluna, circuitos atenuados |
```

## Reutilização e comportamento
Novo `internal-hero.css`, somente carregado nas páginas internas, com escopo `.page-hero--circuits`. Novo SVG `hero-circuits.svg` com os 14 caminhos da Home e pontos estáticos; imagem decorativa com alt vazio, aria-hidden e dimensões. Novo `internal-hero.js` faz fetch same-origin do SVG para adicionar pulsos e destaque ao ponteiro, somente dentro de Heroes marcados. Sem HTML remoto ou dependências. Deve ser idempotente, tolerar falha de rede e manter a imagem estática. Pulsos em CSS, pausados por controle visível com nome acessível e aria-pressed, `IntersectionObserver`, visibilidade da aba e preferência de redução de movimento (inclusive mudanças em tempo de execução). Sem loop requestAnimationFrame permanente. Não animar entrada escondendo conteúdo.

CTAs novos somente onde ausentes: Sobre -> Ver serviços (/servicos); Serviços -> Converse sobre seu projeto (/contato); Contato -> Preencher mensagem (#contact-form); Fundador -> Conhecer a M2R (/sobre); Projetos -> Conhecer o M2R Server (/projetos/m2r-server); Blog -> Ler os artigos (#artigos); artigos -> Ler o artigo (#artigo). Adicionar IDs em blocos existentes apenas para esses destinos. Não fazer #contact-form depender de JS: apontar para wrapper da seção de contato com ID contato-mensagem, preservando o formulário oculto quando JS indisponível.

## Validação
Playwright MCP: antes/depois de todas as 12 rotas incluindo Home nas larguras 320, 390, 768, 1024, 1440 e 1920px. Capturas com 900px de altura. Confirmar sem overflow, H1 único, circuitos visíveis, controles e links acessíveis, pausa/redução de movimento, no-JS/falha do SVG e conteúdo intacto. Ferramentas existentes: pytest tools, site_tools check/security, version-assets --check, browser_check (axe-core). Complementar axe com tags WCAG 2.2 onde suportadas, sem afirmar certificação. Chrome DevTools MCP para console e diagnóstico. Auditor independente revisa diff e evidências; correções retornam ao implementador.

## Exceções às skills
O briefing prevalece sobre geração aleatória de novo design, reescrita de contatos/copy e mudanças em seções fora do Hero. Scripts de qualidade da taste skill são informativos para o site existente, e seus resultados serão relatados honestamente. Ferramentas de navegador foram explicitamente solicitadas. Não há autorização para alterar o kit nem descartar o merge local. PR em branch nova é autorizado.
