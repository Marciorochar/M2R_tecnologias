# Verificações de acessibilidade e desempenho — design

## Objetivo

Ampliar os controles de qualidade do site M2R Tecnologias sem mudar serviços externos nem a interface publicada. Publicar as alterações em um Pull Request separado para revisão.

## Escopo

- Automatizar uma auditoria axe-core nas páginas do site pelo Chromium já utilizado em `tools/browser_check.py`.
- Bloquear o CI apenas por violações axe de impacto `critical` ou `serious`, exibindo a rota e os elementos afetados. Os demais resultados são informativos.
- Executar Lighthouse contra o servidor estático local, registrar as notas das quatro categorias e disponibilizar o relatório JSON. Notas não são bloqueantes nesta etapa por sua variabilidade entre execuções.
- Atualizar as três capturas versionadas do README com imagens reais da paleta atual; continuar gerando capturas no CI como artefato temporário para revisão.
- Monitorar semanalmente as novas dependências npm no Dependabot e bloquear vulnerabilidades de severidade alta nas ferramentas de desenvolvimento.

## Não escopo

- Alterações no Render, GitHub Pages, ruleset da `main`, e-mail institucional, envio de formulário e projetos comerciais.
- Alterar a paleta, breadcrumbs, rotas ou comportamento visível do site fora de correções de acessibilidade demonstradas por teste.

## Abordagens consideradas

1. **Integração ao navegador existente (escolhida):** reutiliza o Playwright Python e o servidor estático, acrescentando o axe-core e um script Lighthouse específico. Menos infraestrutura nova e testes relevantes.
2. Nova suíte E2E JavaScript: facilita pacotes Node, porém duplica ferramentas de navegador e manutenção.
3. Apenas auditoria manual: não evita regressões futuras.

## Restrições e aprovação

O usuário autorizou explicitamente começar pelas melhorias de código em PR, mantendo os serviços publicados. Toda dependência de desenvolvimento deve ter versão fixa; a `main` não será alterada diretamente.
