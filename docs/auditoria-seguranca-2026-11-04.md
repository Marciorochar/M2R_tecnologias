# Auditoria de seguranca - M2R Tecnologias

Data: 04/11/2026  
Base local: branch `main`, commit `985864b6721597713bc703834bdd0662354f0ac7`  
Frontend publico: `https://m2rtecnologias.vercel.app`  
Backend publico encontrado: `https://m2r-backend.onrender.com`  
Metodo: revisao estatica, testes locais e verificacao passiva de producao

## Resumo executivo

O frontend publicado apresenta uma postura de seguranca adequada para um site
estatico: HTTPS e HSTS estao ativos, a CSP nao permite `unsafe-inline` nem
`unsafe-eval`, o framing esta bloqueado, nao foram observadas dependencias de
terceiros no carregamento inicial e o JavaScript nao usa sinks perigosos de HTML.

O principal risco esta fora do fluxo documentado do site. Um backend legado no
Render permanece ativo e nao corresponde ao backend atual de `main`. Ele expoe
rotas antigas de cadastro, login, verificacao de JWT e envio de e-mail, usa CORS
aberto em producao e pertence a uma familia de codigo que continha um segredo JWT
padrao publico, comparacao com senha em texto simples, ausencia de rate limiting
e retorno de detalhes internos em erros. A recomendacao prioritaria e desligar
esse servico, caso nao seja necessario, ou substitui-lo pelo backend minimo atual
depois de rotacionar todas as credenciais relacionadas.

| Severidade | Quantidade |
| --- | ---: |
| Critica | 0 |
| Alta | 1 |
| Media | 1 |
| Baixa | 3 |
| Informativa | 2 |

## Status da remediacao no repositorio

Em 04/11/2026, a branch `codex/security-remediation-2026-11-04` recebeu as
correcoes que podem ser controladas pelo codigo:

- allowlist `.vercelignore` e rotas Vercel com status 404 para impedir acesso a backend, docs, tools e workflows;
- CORS por rota e metodo, validacao fail-closed da origem e headers no Flask;
- Redis obrigatorio para rate limiting em producao;
- schema JSON estrito e limite para `/api/status`;
- actions fixadas por SHA e ferramentas Python com versoes exatas;
- testes de regressao para headers, CORS, configuracao e allowlist de deploy.

Validacao pos-correcao: 70 testes do backend e 11 testes das ferramentas
passaram; a auditoria das dependencias de producao nao encontrou vulnerabilidades
conhecidas, e as verificacoes de JavaScript, sitemap, links e CSP tambem passaram.
O Chromium validou as 12 rotas em 320, 390, 768, 1024 e 1440 pixels, alem dos
fallbacks sem JavaScript, movimento reduzido, observer fallbacks, redirecionamentos
e pagina 404. A configuracao de proxy agora e opt-in por quantidade explicita de
saltos confiaveis, e as respostas recebem um identificador aleatorio de requisicao.

AS-03, AS-04 e AS-05 ficam corrigidos no codigo e foram confirmados no dominio
publico apos o deploy. AS-06 foi endurecido: `memory://` continua disponivel
somente fora de producao e `ProxyFix` exige uma quantidade explicita de saltos
confiaveis. AS-01 e AS-02 permanecem abertos: o desligamento do
Render legado, a rotacao de segredos e a revisao de logs/banco/SMTP exigem acesso
ao provedor. O backend legado continua ativo e requer desativacao manual.

## Auditoria publica pos-deploy

Em 04/11/2026, apos a integracao na `main` pelos PRs #11, #14 e #15, foram
repetidas verificacoes passivas em `https://m2rtecnologias.vercel.app`:

- raiz, `/sobre`, `/fundador`, `/contato`, assets, robots e sitemap responderam corretamente;
- `/backend/app.py`, `/.github/workflows/validate-site.yml`, `/docs/`, `/tools/` e `/vercel.json` responderam HTTP 404;
- rota inexistente de teste respondeu HTTP 404;
- HTTPS, HSTS, CSP, `nosniff`, Permissions-Policy e framing bloqueado permaneceram ativos;
- Lighthouse na home marcou 100 em acessibilidade, boas praticas e SEO em mobile e desktop;
- a imagem do fundador passou a ser carregada com CSS versionado e proporcao efetiva 4:5 no navegador;
- `https://m2r-backend.onrender.com` continua respondendo e permanece como pendencia externa de alta prioridade.

## Escopo e limites

Foram examinados o frontend, o Flask atual, a configuracao da Vercel, o workflow
do GitHub Actions, as dependencias Python e 339 blobs de texto unicos do historico
Git. A producao recebeu somente requisicoes de leitura (`GET`) e observacao de
cabecalhos. Nenhum formulario foi enviado, nenhum login foi tentado e o rate
limit de producao nao foi exercitado.

Nao houve acesso aos paineis da Vercel ou Render, variaveis de ambiente,
PostgreSQL, conta SMTP, logs de producao ou configuracoes DNS. Portanto, nao foi
possivel confirmar se o segredo JWT padrao foi substituido no Render, se existem
usuarios indevidos, se houve abuso de e-mail ou se credenciais antigas continuam
validas.

## Achados confirmados

### AS-01 - Alta - Backend legado e desnecessario permanece ativo

**Evidencia de producao**

- `GET /healthz` retornou 200 e `{"status":"ok"}` pelo Gunicorn.
- A raiz retornou a mensagem antiga `Backend da M2R Tecnologias funcionando.`.
- `GET /verify` retornou 401, confirmando uma rota protegida por token.
- `GET /register`, `/login` e `/send-email` retornaram 405 com `Allow: OPTIONS, POST`, confirmando que as rotas POST estao publicadas.
- `GET /api/contato` retornou 404.
- O backend atual de `main` nao possui cadastro, login, JWT, banco ou SMTP; ele possui `/api/contato` e retorna outra mensagem na raiz (`backend/app.py:68-118`).

Esses resultados comprovam desvio entre o codigo versionado e o artefato em
producao. O servico ativo corresponde ao conjunto de rotas do antigo `app.py`,
removido no commit `813e5ce`.

**Cenario de abuso**

Um atacante pode concentrar tentativas em uma API que deveria estar fora de uso,
criando contas, testando credenciais ou consumindo o SMTP. Como esse servico
historico acessava PostgreSQL e credenciais de e-mail, ele amplia a superficie de
ataque e pode reter dados pessoais sem que o frontend atual dependa dele.

**Impacto**

- criacao nao autorizada de registros;
- tentativa automatizada de credenciais;
- consumo da cota ou bloqueio da conta SMTP;
- exposicao de erros, metadados ou dados antigos;
- manutencao de credenciais e banco que a aplicacao atual nao necessita.

**Correcao recomendada**

1. Desligar imediatamente `m2r-backend.onrender.com` se ele nao tiver uso legitimo.
2. Rotacionar `SECRET_KEY`, `DATABASE_URL`, credenciais SMTP e qualquer segredo configurado no servico, mesmo que ele seja desligado.
3. Revisar usuarios do banco, logs de login, envios SMTP e acessos ao Render desde a primeira publicacao.
4. Se a API ainda for necessaria, criar um novo servico a partir de `backend/app.py` atual, sem reutilizar as variaveis ou o banco legado antes da revisao.
5. Adicionar um inventario de ambientes publicados e um teste de paridade entre commit implantado e commit esperado.

OWASP: A05 Security Misconfiguration, A07 Identification and Authentication Failures.

### AS-02 - Media - Controles inseguros na familia de codigo implantada

**Evidencia confirmada em producao**

Uma requisicao a `/api/status` com `Origin: https://evil.example` recebeu
`Access-Control-Allow-Origin: https://evil.example`. Sem `Origin`, as respostas
receberam `Access-Control-Allow-Origin: *`. O CORS esta aberto para qualquer site.

**Evidencia no historico Git**

As versoes antigas que possuem exatamente as rotas observadas usam:

- `CORS(app)` global;
- fallback literal para `SECRET_KEY` com 24 caracteres, presente em seis blobs e fingerprint SHA-256 parcial `2984B4C54C98` (o valor nao e reproduzido neste relatorio);
- comparacao entre a senha armazenada e a senha informada quando a verificacao de hash falha;
- senha minima de apenas seis caracteres;
- ausencia de limite de corpo e rate limiting em `/register`, `/login` e `/send-email`;
- retorno de `str(exception)` em respostas 500;
- impressao da lista de e-mails cadastrados no log quando um login nao encontra usuario;
- execucao direta com `debug=True` (o Gunicorn observado nao executa esse bloco).

O commit `c9fb699` corrigiu CORS, segredo obrigatorio e comparacao de senha, mas a
producao continua exibindo o comportamento e as rotas anteriores a essa correcao.
Nao foi realizado POST em producao, portanto a utilizacao efetiva do fallback JWT
e os detalhes internos das rotas sao uma inferencia forte a partir da linhagem do
codigo, nao uma exploracao confirmatoria.

**Cenario de abuso e impacto**

O CORS aberto permite que qualquer pagina controle chamadas a API pelo navegador.
Sem limitacao, login e e-mail ficam sujeitos a automacao. Se o Render nao definir
um segredo JWT proprio, o fallback publicado permite fabricar tokens validos para
`/verify`. A aceitacao historica de senha em texto simples e o log de e-mails
podem expor dados de usuarios a operadores ou a qualquer pessoa com acesso aos
logs.

**Correcao recomendada**

- tratar o segredo historico como comprometido e nunca reutiliza-lo;
- invalidar tokens existentes ao rotacionar o segredo;
- eliminar compatibilidade com senha em texto simples e exigir redefinicao de senha para registros afetados;
- remover as rotas antigas ou exigir autenticacao e autorizacao apropriadas;
- restringir CORS ao frontend oficial e aos metodos necessarios;
- aplicar limites por IP/conta, tamanho de corpo, schema estrito e erros genericos;
- remover dados pessoais dos logs e definir retencao/monitoramento.

OWASP: A02 Cryptographic Failures, A05 Security Misconfiguration, A07 Identification and Authentication Failures, A09 Security Logging and Monitoring Failures.

### AS-03 - Baixa - Arquivos internos sao publicados no dominio do frontend

O deploy da Vercel serve arquivos fora de `frontend/`:

| Rota observada | Status |
| --- | ---: |
| `/backend/app.py` | 200 |
| `/backend/.env.example` | 200 |
| `/backend/requirements.txt` | 200 |
| `/backend/test_app.py` | 200 |
| `/tools/site_tools.py` | 200 |
| `/docs/auditoria-2026-10-17.md` | 200 |
| `/.github/workflows/validate-site.yml` | 200 |
| `/CHANGELOG.md` | 200 |
| `/backend/.env` | 404 |
| `/.git/config` | 404 |

O repositorio ja e publico, o `.env` nao foi exposto e esses arquivos nao
continham segredos atuais. Por isso o impacto imediato e baixo. Mesmo assim, o
dominio de producao entrega codigo, testes e relatorios que nao fazem parte do
produto e que facilitam fingerprinting da infraestrutura.

**Correcao recomendada**

Publicar um artefato contendo somente `frontend/` e os arquivos estritamente
necessarios ao roteamento. Validar na CI que rotas como `/backend/app.py`,
`/.github/` e `/docs/` retornem 404 antes de promover o deploy.

OWASP: A05 Security Misconfiguration.

### AS-04 - Baixa - Backend publico nao envia HSTS nem headers de endurecimento

O Render redireciona HTTP para HTTPS com 307, mas as respostas observadas do
backend nao incluem `Strict-Transport-Security`, `X-Content-Type-Options`,
`Referrer-Policy` ou CSP. Para uma API JSON, CSP tem utilidade limitada, mas HSTS
e `nosniff` continuam recomendados. O frontend da Vercel envia esses headers,
inclusive HSTS com `max-age=63072000; includeSubDomains; preload`.

**Correcao recomendada**

Configurar os headers no proxy/plataforma ou no Flask e testar as respostas de
sucesso e erro. Manter o redirecionamento HTTP para HTTPS.

OWASP: A05 Security Misconfiguration.

### AS-05 - Baixa - Dependencias de CI nao sao imutaveis

O workflow limita o token a `contents: read`, o que reduz o impacto, e o
Dependabot monitora Python e GitHub Actions semanalmente. Entretanto:

- `actions/checkout`, `actions/setup-node` e `actions/setup-python` usam tags `@v7`, nao SHAs imutaveis;
- Playwright, pytest e pip-audit sao instalados sem versao fixa durante a CI;
- as dependencias de runtime possuem versao exata, mas nao hashes de pacote.

Um comprometimento de tag ou uma publicacao maliciosa no indice pode alterar o
codigo executado pelo runner. Nao ha secrets de deploy no workflow auditado, mas
o risco de cadeia de fornecimento permanece.

**Correcao recomendada**

Fixar actions por SHA completo com comentario da versao, fixar ferramentas de
teste em um arquivo separado e considerar hashes para dependencias de producao.

OWASP: A08 Software and Data Integrity Failures.

## Endurecimentos e observacoes

### AS-06 - Informativa - Limitador atual usa memoria por processo

O backend limita `/api/contato` a duas requisicoes por hora. `memory://` continua
sendo o padrao local, mas a inicializacao em producao recusa esse armazenamento;
o ambiente produtivo precisa de Redis compartilhado. Em varios workers ou
instancias, cada processo mantem seu proprio contador quando o armazenamento local
e usado.

Se o backend atual for publicado, configurar armazenamento compartilhado e definir
`TRUSTED_PROXY_HOPS` somente apos validar a topologia do proxy. Com o valor padrao
zero, a implementacao ignora um `X-Forwarded-For` forjado e limita pelo endereco
remoto fornecido pelo servidor.

### AS-07 - Informativa - Dados de contato sao publicos por decisao editorial

E-mail, telefone, WhatsApp e foto do fundador aparecem em HTML/JSON-LD e podem ser
coletados automaticamente. Isso e coerente com um site institucional, mas deve
existir consentimento para essa publicacao e monitoramento de spam. Nao foram
classificados como segredo.

## Controles que passaram

- Nenhuma chave privada, token em formato conhecido ou `.env` real foi encontrado nos 339 blobs de texto examinados.
- Somente `backend/.env.example` apareceu como arquivo de ambiente versionado; `.env` e variantes locais estao no `.gitignore`.
- `pip-audit` nao encontrou vulnerabilidades conhecidas nas cinco dependencias Python fixadas.
- O backend atual limita o corpo a 16 KiB, valida tipos e comprimentos, rejeita JSON malformado e impede quebras de cabecalho em nome, e-mail e telefone.
- O backend atual restringe CORS ao frontend oficial em producao; origem nao permitida nao recebeu header CORS no teste local.
- O backend atual nao habilita debug em `production` ou `testing`.
- As consultas SQL do backend legado observado no historico eram parametrizadas; nao foi identificada concatenacao SQL.
- O frontend nao usa `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `eval`, `new Function`, `document.write`, `localStorage` ou `sessionStorage`.
- O formulario usa `textContent` para mensagens e `encodeURIComponent` para assunto e corpo do `mailto:`.
- Todos os links com `target="_blank"` encontrados possuem `rel="noopener"`.
- A CSP bloqueia scripts e estilos inline, objetos e framing; `base-uri` e `form-action` estao definidos.
- A pagina inicial carregou apenas cinco recursos do proprio dominio e nao apresentou erros JavaScript.
- Uma rota inexistente em producao retornou HTTP 404; HTTP redireciona para HTTPS.

## Matriz OWASP Top 10

| Categoria | Estado | Evidencia principal |
| --- | --- | --- |
| A01 Broken Access Control | Aplicavel | Backend legado expoe cadastro e e-mail sem necessidade atual; revisar autorizacao antes de reutilizar. |
| A02 Cryptographic Failures | Achado | Fallback JWT publico no historico e possivel uso na linhagem implantada. |
| A03 Injection | Sem achado confirmado | SQL historico parametrizado; frontend nao possui sinks HTML dinamicos. |
| A04 Insecure Design | Achado | Servico legado mantem banco, autenticacao e SMTP sem uso pelo site atual. |
| A05 Security Misconfiguration | Achado | Drift de deploy, CORS aberto, arquivos internos publicados e headers ausentes no backend. |
| A06 Vulnerable and Outdated Components | Sem achado conhecido | `pip-audit` limpo em 04/11/2026; manter verificacao continua. |
| A07 Identification and Authentication Failures | Achado | Login legado sem rate limiting, senha minima fraca e compatibilidade historica com texto simples. |
| A08 Software and Data Integrity Failures | Endurecimento | Actions e ferramentas de CI nao fixadas por SHA/versao. |
| A09 Security Logging and Monitoring Failures | Achado | Codigo legado registrava lista de e-mails e nao demonstra monitoramento de abuso. |
| A10 Server-Side Request Forgery | Nao aplicavel | Nao ha URL controlada pelo usuario nem fetch server-side generico no codigo atual. |

## Itens nao aplicaveis ao frontend atual

- autenticacao, sessoes e cookies;
- CSRF, pois o frontend nao possui operacao autenticada ou mutacao no servidor;
- banco de dados e SQL;
- upload de arquivos;
- pagamentos;
- blockchain e assinatura de carteira;
- armazenamento de dados do formulario: o navegador apenas prepara um `mailto:`.

Esses itens deixam de ser nao aplicaveis se o backend legado continuar como parte
do produto.

## Resultados reproduziveis

| Verificacao | Resultado |
| --- | --- |
| `python -m pytest backend` | PASS - 49 testes |
| `python -m unittest discover -s tools -p "test_*.py" -v` | PASS - 10 testes |
| `python tools/site_tools.py check` | PASS - 12 paginas |
| `python tools/site_tools.py security` | PASS - CSP e 11 JSON-LD |
| `node --check frontend/assets/js/script.js` | PASS |
| `node tools/generate-sitemap.js --check` | PASS; hash do sitemap permaneceu igual ao HEAD |
| `python -m pip_audit -r backend/requirements.txt` | PASS - nenhuma vulnerabilidade conhecida |
| `python tools/browser_check.py` | PASS - 12 rotas em 320, 390, 768, 1024 e 1440 px, fallbacks, redirects e 404 |
| Varredura historica redigida | 339 blobs; nenhum token conhecido/chave privada; um fallback JWT historico |
| Frontend Vercel | HTTPS/HSTS/CSP presentes; somente recursos same-origin; 404 correto |
| Backend Render | Ativo; rotas legadas presentes; CORS arbitrario; sem HSTS/headers de endurecimento |

O primeiro teste auxiliar falhou dentro do sandbox por bloqueio de sockets e do
diretorio temporario. A repeticao fora dessa restricao passou integralmente. O
primeiro teste Chromium local encontrou o pacote instalado sem o executavel; o
Chromium correspondente foi instalado no cache local do Playwright e a repeticao
passou. Nenhuma dessas ocorrencias foi falha do codigo auditado.

## Prioridade de resposta

### Imediata - 0 a 24 horas

1. Confirmar o proprietario do servico `m2r-backend.onrender.com` e desliga-lo se nao for necessario.
2. Rotacionar segredo JWT, banco e SMTP associados ao servico.
3. Revisar logs, usuarios cadastrados e atividade SMTP por sinais de abuso.

### Curto prazo

1. Restringir o artefato da Vercel a arquivos publicos do frontend.
2. Fixar dependencias da CI e actions por SHA.
3. Adicionar verificacao automatica das URLs publicadas e do commit implantado.

### Antes de republicar qualquer backend

1. Usar somente o Flask minimo atual ou realizar nova revisao do backend escolhido.
2. Configurar storage compartilhado para rate limiting, headers de seguranca e origem CORS explicita.
3. Executar testes de abuso em ambiente isolado, nunca diretamente em producao.

## Conclusao

Nao foi encontrada vulnerabilidade critica no frontend atual. O risco relevante
e operacional: um backend antigo, com controles de seguranca conhecidos como
insuficientes, continua acessivel publicamente embora o projeto atual declare que
o backend e opcional e nao utilizado pelo site. A remocao desse servico e a
rotacao de suas credenciais oferecem a maior reducao de risco imediata.
