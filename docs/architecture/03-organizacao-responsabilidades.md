# 03 — Organização e responsabilidades

## Organização observada

O sistema tem uma divisão operacional clara entre publicação do frontend estático, backend Flask opcional e ferramentas de qualidade. O CSS e o JavaScript de comportamento geral são compartilhados pelas páginas. A exceção funcional identificada é a animação do hero, carregada apenas na home. O backend tem suas próprias dependências e testes; não participa da rota de publicação estática indicada pelo README.

| Unidade | Responsabilidade atual | Acoplamento observado |
| --- | --- | --- |
| Páginas HTML | Conteúdo, metadados, marcação e referências a recursos | Rotas, CSS/JS compartilhados e navegação entre páginas |
| `script.js` | Menu, scroll, navegação por seção, revelação, contato e movimento | DOM condicional por IDs/classes presentes em páginas diferentes |
| `hero-circuits.js` | Interação e animação do hero SVG | IDs/classes e geometria SVG de `frontend/index.html` |
| `site_tools.py` | Parser HTML, modelo `Site`, rotas/redirects/rewrites, links, segurança e servidor local | Configuração `vercel.json` e filesystem; também é usado em testes e ferramentas de browser |
| `backend/app.py` | API, validação de configuração/entrada, CORS, rate limit e cabeçalhos | Flask extensions, variáveis de ambiente, origem frontend e proxy configurado |
| `tools/` | Checks, geração de sitemap, versionamento e browser | HTML, JSON, configuração Vercel e ferramentas externas |
| CI | Executa verificações e publica artefatos | Node, Python, Chromium, GitHub Actions e Vercel config |

## Coesão e acoplamento

- Graphify classifica `Site` e `SiteTests` como hubs. A leitura do código confirma que `Site` é usado por verificações de links, servidor local e checks de navegador/Lighthouse; sua centralidade representa reutilização da abstração de rotas, não prova defeito de desenho.
- `script.js` agrega comportamentos globais e específicos. Os guardas por elemento tornam algumas rotinas opcionais por página, mas a mudança de um ID/contrato de formulário pode afetar o script central. Isso é um risco de manutenção, não falha confirmada.
- `site_tools.py` concentra parser, roteamento, validação de links e servidor. São responsabilidades relacionadas a um servidor local que espelha a configuração Vercel; separar módulos deve depender de crescimento e mudança independente, não apenas da centralidade do grafo.
- Backend e frontend estão desacoplados no fluxo público atual. A duplicidade entre API de validação e `mailto:` pode ser intencional: o README promete contato sem backend. Não se deve inferir integração ou envio server-side.

## Componentes sem referências aparentes

Graphify reporta nós isolados ou de baixa conectividade, incluindo categorias de conteúdo e componentes do projeto M2R Server; o relatório de 11/11 cita 21 nós com até uma conexão, mas inclui nós de arquivo, conceitos e racionales. Isso não demonstra código morto. Páginas acessadas por rotas, scripts por markup, handlers de framework e destinos dinâmicos podem não ter referências do tipo import que o extrator prioriza.

**Evidência principal:** `frontend/assets/js/script.js`; `frontend/assets/js/hero-circuits.js`; `tools/site_tools.py:17-173`; `tools/browser_check.py:127-206`; `tools/lighthouse_check.py`; `backend/app.py:22-233`; relatórios Graphify indicados em [05](05-graphify-validacao-cruzada.md).
