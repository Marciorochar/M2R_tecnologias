# Verificações de qualidade — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Incluir auditoria automatizada de acessibilidade e relatório Lighthouse no CI da M2R Tecnologias, com documentação e capturas atualizadas.

**Architecture:** Reutilizar o Playwright Python e o servidor estático existente. Pacotes Node ficam em `devDependencies` com lockfile; verificações de axe são bloqueantes apenas para violações graves, e Lighthouse publica resultados informativos.

**Tech Stack:** Python 3.12, Playwright, Node.js 22, axe-core 4.14.0, Lighthouse 13.6.0 e GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-11-08-quality-gates-design.md`

## Global Constraints

- Nenhuma mudança de infraestrutura ou fluxo de contato.
- Não alterar o deploy da Vercel além de arquivos necessários ao desenvolvimento.
- Usar dependências fixadas e `npm ci` no CI.
- Não bloquear merges por pontuações instáveis do Lighthouse.

## Review Focus

- A página com CSP restritiva deve permitir inspeção axe pelo navegador de teste sem afrouxar a CSP publicada.
- Cada violação grave deve identificar a rota e o elemento associado.
- Lighthouse deve funcionar com o Chromium disponível no ambiente e encerrar seu servidor local.
- Relatório Lighthouse incompleto deve produzir falha explícita, não sucesso silencioso.
- Capturas atualizadas devem representar a paleta marrom/cobre, não o tema anterior.

---

### Task 1: Dependências de desenvolvimento e axe-core

**Files:** `package.json`, `package-lock.json`, `tools/browser_check.py`, `tools/test_site_tools.py`, `.github/workflows/validate-site.yml`.

- [ ] Criar teste que detecte ausência do arquivo axe e que exija verificação efetiva de violações graves.
- [ ] Executar o teste e observar falha pela função ausente.
- [ ] Instalar versões fixadas de `axe-core` e `lighthouse`, integrar `axe.run` ao Chromium e `npm ci` ao workflow.
- [ ] Executar testes de axe e corrigir apenas problemas reais identificados, se houver.

### Task 2: Relatório Lighthouse

**Files:** `tools/lighthouse_check.py`, `tools/test_lighthouse_check.py`, `.github/workflows/validate-site.yml`.

- [ ] Criar testes de parsing/relato para resultados completos, incompletos e scores baixos não bloqueantes.
- [ ] Confirmar falha antes da implementação.
- [ ] Implementar geração local do JSON, relatório legível e upload do artefato no GitHub Actions.
- [ ] Executar Lighthouse localmente e conferir as quatro categorias.

### Task 3: Documentação e evidências visuais

**Files:** `README.md`, `tools/browser_check.py`, `.github/workflows/validate-site.yml`.

- [ ] Gerar capturas atuais de três páginas com Chromium em 1365×768 e anexar artefato no CI.
- [ ] Conferir as imagens geradas no CI e atualizar a documentação dos testes.
- [ ] Executar a suíte completa, conferir `git diff --check`, revisar o escopo e criar PR sem merge.
