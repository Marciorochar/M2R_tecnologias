# Auditoria corretiva - 17/10/2026

## Base e preservacao

A copia auditada pelo solicitante estava em `378790f`. A verificacao remota
encontrou `origin/main` em `0bc3842`, com as PRs #8 e #9 ja mescladas.
A #8 reverteu ajustes do fundador; a #9 atualizou python-dotenv para 1.2.4.
Essas PRs nao foram integradas novamente. A working tree original estava limpa,
inclusive ao ignorar diferencas CRLF/LF. As correcoes foram feitas em checkout
isolado, na branch `codex/auditoria-corretiva-2026-10-17`, baseada em origin/main.

O CSS exclusivo de `codex/ajusta-foto-fundador` foi portado seletivamente:
faixa azul #10233a, painel #17304d, imagem clara a esquerda, texto branco,
duas colunas e empilhamento abaixo de 900 px. A main nao tinha esses overrides.
Foram acrescentados contraste do selo, foco no painel escuro e suporte a picture.
O PNG original e a atualizacao de dependencia da main foram preservados.

## Causas e severidade

| Prioridade | Causa comprovada | Correcao |
| --- | --- | --- |
| P0 | JS criava segundo botao e nao ativava o CSS progressivo | Reuso do HTML, inicializacao unica, ARIA sincronizado, Escape, links e resize |
| P0 | JS nao ativava reveal; CI dependia de strings literais | Observer preparado antes da classe; testes comportamentais no Chromium |
| P0 | Elementos poderiam permanecer ocultos apos falha do observer | Fallback sem JS, sem observer, erro de inicializacao, reduced motion e limite de 5 segundos |
| P1 | Teste de sitemap fixava 10 URLs sem considerar as rotas | Comparacao dinamica com rewrites e exclusao de noindex/404 |
| P1 | Perfil do fundador prometia biografia nao fornecida | Noindex temporario, texto baseado no repositorio e CTA para projetos |
| P1 | Foto sem dimensoes e PNG pesado | 1254x1254 declarados, WebP sem perdas e PNG de fallback |
| P1 | Navegacao fixa cobria conteudo sem JS no celular | Navbar no fluxo normal sem inicializacao JS |
| P1 | Selo do fundador com texto claro sobre fundo claro | Fundo transparente no painel escuro |
| P1 | Titulo longo e tamanho minimo das colunas geravam overflow no Chromium Linux | Quebra de palavras quando necessaria e tracks minmax(0, 1fr) |
| P1 | Botao secundario branco sobre fundo claro em /fundador | Botao outline do proprio site |
| P2 | README continha tres blocos de conflito | Reconciliacao mantendo backend opcional e contrato mailto |
| P2 | Execucao direta do Flask habilitava debug em producao | Debug apenas com APP_ENV de desenvolvimento/local; teste de regressao |

## Arquivos

| Arquivo | Alteracao e motivo |
| --- | --- |
| frontend/assets/js/script.js | Estado unico do menu; Escape/foco/resize; reveal com fallbacks |
| frontend/assets/css/style.css | Porte do design do fundador; contraste/foco; alvos de toque e menu sem JS |
| frontend/pages/sobre.html | Ordem institucional clara, texto direto, picture e CTA para projetos |
| frontend/pages/fundador.html | Menu padrao, noindex, metadados coerentes e conteudo sem biografia inventada |
| frontend/assets/img/Eu_fundador.webp | Conversao sem perdas; PNG original mantido |
| tools/generate-sitemap.js | Respeita meta robots noindex |
| tools/test_sitemap.py | Rotas dinamicas, alternancia de indexacao e datas estaveis apos commit nao editorial |
| tools/sitemap-dates.json | Data editorial apenas de /sobre e /fundador atualizada |
| frontend/sitemap.xml | Regenerado; /fundador nao publicavel por noindex |
| tools/browser_check.py | Chromium em 320/390/768/1024/1440 px; menu, teclado, ARIA, imagens, overflow e fallbacks |
| .github/workflows/validate-site.yml | Substitui dois checks textuais por execucao real do navegador; demais checks mantidos |
| backend/app.py | Impede debug na execucao direta em producao |
| backend/test_app.py | Testa debug em production, development e testing |
| .gitignore | Ignora caches pytest e resultados de navegador; ambientes e .env ja cobertos |
| README.md | Remove marcadores, documenta backend opcional, rotas, comandos e decisao editorial |

## Imagem

PNG original: 1.810.409 bytes; WebP lossless: 1.283.586 bytes (29,1% menor).
Mesmas dimensoes, sem recorte ou perda de pixels. Ambos os HTMLs usam picture,
fallback PNG, dimensoes explicitas e lazy loading pois a foto esta abaixo da dobra.

## Validacao

Ambiente isolado `.venv-audit`, Python 3.14.7 local, com dependencias do backend
fixadas pelo repositorio. A CI usa Python 3.12 e Node 22.
Nenhum ambiente virtual ou arquivo pessoal foi removido.

| Comando | Estado |
| --- | --- |
| node --check frontend/assets/js/script.js | PASS |
| node tools/generate-sitemap.js --check | PASS |
| python tools/site_tools.py check | PASS - 12 paginas e recursos |
| python tools/site_tools.py security | PASS - 11 blocos JSON-LD e CSP |
| python -m unittest discover -s tools -p 'test_*.py' -v | PASS - 10 testes |
| python -m py_compile backend/app.py | PASS |
| python -m pytest backend | PASS - 49 testes |
| python -m pip_audit -r backend/requirements.txt | PASS - nenhuma vulnerabilidade conhecida |
| python tools/browser_check.py | Resultados locais e execucao Linux nos checks da PR #10 |
| Workflow Validar site | [Resultado atualizado nos checks da PR #10](https://github.com/Marciorochar/M2R_tecnologias/pull/10/checks) |

O primeiro check de links executou antes da conversao WebP terminar e falhou
por arquivo ainda ausente. A repeticao apos a conversao passou. O primeiro
teste Chromium expunha uma espera ausente no proprio teste de resize; foi
substituida por espera do estado observado apos o evento de media query.
Expressoes de espera foram convertidas em funcoes para respeitar a CSP sem
unsafe-eval. A CI identificou overflow em /projetos a 320 px no Linux, corrigido
sem esconder conteudo. O fallback do teste foi ajustado para criar o viewport
no BrowserContext e respeitar o atributo hidden do formulario sem JavaScript;
a verificacao especifica continua exigindo que esse formulario esteja oculto.

PR corretiva: https://github.com/Marciorochar/M2R_tecnologias/pull/10.
Os checks vinculados a PR identificam o commit testado e mantem o resultado
atualizado sem fixar o estado de uma execucao anterior neste documento.

O servidor local testa as regras estaticas, nao emula toda a plataforma Vercel.
`/404` e uma rota explicitamente reescrita e responde 200 no adaptador local;
rotas desconhecidas respondem 404, inclusive caminhos aninhados. O status de
producao nao foi verificado por deploy nesta auditoria.
O formulario usa mailto e exige envio no aplicativo do visitante. A API opcional
somente valida dados. Os testes nao enviam mensagens.

## Pendencias editoriais

- Nome publico e apresentacao profissional do fundador aprovados pela empresa.
- Formacao, experiencias e competencias verificaveis para eventual biografia.
- Autorizacao para retirar noindex e reativar o CTA biografico quando o perfil estiver completo.
- Casos, clientes e resultados apenas quando houver evidencias e autorizacao de publicacao.

Nao houve merge, push direto para main ou deploy solicitado pela ferramenta.
