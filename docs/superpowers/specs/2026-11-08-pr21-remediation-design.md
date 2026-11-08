# PR #21 — Remediação da auditoria

## Objetivo

Corrigir a quebra do layout inicial em dispositivos móveis, resolver os conflitos do PR #21 com `main`, preservar as trilhas de navegação visíveis e os controles de segurança, padronizar os hashes no Windows e consolidar URLs públicas canônicas.

## Limites

- Atualizar somente a branch `fix/hash-normalization`, sem mesclar o PR.
- Não desativar o Render, GitHub Pages ou alterar as regras de proteção do repositório; exigem decisões administrativas independentes.
- Manter a stack atual (HTML, CSS, JavaScript, Python, Vercel) e a forma de contato existente.

## Abordagem

Reaproveitar os redirecionamentos e a normalização de hashes já introduzidos no PR, integrar `main` escolhendo os HTMLs atuais para preservar breadcrumbs, corrigir pontualmente a regra CSS com maior especificidade e adicionar asserções de responsividade e navegação ao navegador automatizado. Restaurar a política CSP existente na `main`.

Alternativas descartadas: refazer todo o frontend (risco desnecessário) ou substituir o PR por outro (o proprietário autorizou especificamente o #21).
