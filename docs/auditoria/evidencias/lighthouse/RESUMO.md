# Evidências Lighthouse — execução local

**Data:** 13/11/2026  
**Ferramenta:** Lighthouse 13.6.0, servido localmente em Chromium.  
**Tipo:** medições de laboratório, uma execução por rota/perfil.

| Rota | Perfil | Desempenho | Acessibilidade | Boas práticas | SEO | LCP (lab) | CLS (lab) | INP |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `/` | mobile | 63 | 100 | 100 | 100 | 1.072 ms | 0 | indisponível |
| `/servicos` | mobile | 73 | 100 | 100 | 100 | 1.053 ms | 0,503 | indisponível |
| `/contato` | mobile | 96 | 100 | 100 | 100 | 1.057 ms | 0 | indisponível |
| `/` | desktop | 66 | 100 | 100 | 100 | 421 ms | 0 | indisponível |

Os valores de LCP e CLS acima vêm dos relatórios JSON ao lado e descrevem apenas esta execução de laboratório. INP não foi fornecido pelos relatórios. Não há dados de campo CrUX/RUM nesta entrega; os valores não representam a experiência p75 dos visitantes.

O relatório de `/servicos` em mobile registra um deslocamento de layout de `0,503`. A auditoria `layout-shifts` aponta o `body` como elemento deslocado e associa o logo da navegação como causa (“Media element lacking an explicit size”). Tratar como achado laboratorial a investigar e revalidar; não é uma medição de usuários reais.

Os arquivos `home-mobile.json`, `servicos-mobile.json`, `contato-mobile.json` e `home-desktop.json` contêm os relatórios detalhados. As capturas responsivas estão em `../responsivo/` e o manifesto relaciona cada screenshot à rota e largura testadas.
