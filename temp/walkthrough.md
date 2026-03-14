# Orchestrator v7 - Advanced AI SRE Squad

Após a análise do export JSON do Rocket.Chat, confirmamos que a infraestrutura estava sub-utilizada e o formato de parsing precisava de ajustes para clients rigorosos. Implementei a v7 que eleva o nível técnico dos agentes para um patamar de SREs Sênior reais!

## O Que Foi Implementado (v7):

### 🔍 1. The Analyst (Logs e Métricas Reais)
- O Analyst agora faz queries via HTTP **dentro do cluster** no Loki (`LogQL`) buscando logs do Pod com erro.
- Faz queries na API do Prometheus buscando as taxas de CPU recentes.
- Esses dados são interpolados em um "Contexto Suplementar" injetado no LM Studio!
- Isso dota o LLM de *visão* sobre o estado real da aplicação no exato minuto do alerta.
- O JSON enviado ao `#ops-critical` usa campos de Markdown robustos.

### 🔄 2. The Orchestrator (Prevenção de Recorrência)
- O Maestro agora consulta a base PostgreSQL *antes* mesmo de abrir chamados com os outros agentes.
- Através da tabela `incident_logs`, ele varre por incidentes prévios na combinação `(alertname, namespace)`.
- Se um histórico existe, ele avisa imediatamente: *"ALERTA REINCIDENTE. Solução Prévias: ..."*.

### 📚 3. The Archivist (Post-Mortems Automáticos no Gitea)
- Após a **Aprovação Humana** (via endpoint `/approve`), o The DevOps faz o patch normal da infra.
- Simultaneamente, uma thread em *background* é iniciada. O Archivist processa TODO o fluxo do incidente e gera relatórios formais.
- Ele usa novamente o LLM passando toda essa *timeline* e escrevendo o documento em `<Markdown>`.
- O documento é comitado usando o Gitea API via HTTP PUT/POST diretamente no diretório `/postmortems` dentro do repositório respectivo do serviço (ex: `target-app-infra`).
- No fim, envia um log final ao `#ops-history` com um **botão linkando diretamente para o arquivo `.md` no Gitea**.

### 🛡️ 4. The Warden (Auditoria e Veto de Segurança)
- A lógica de simulação `dry-run` do Kustomize continua existindo, mas agora o pacote que chega ao `#ops-security` não é vazio nem genérico.
- O texto contém logs completos da modificação que ocorreu nas chaves, garantindo que as `Secrets` mantiveram paridade cega no patch GitOps.

## Status Atual
- **Infraestrutura**: As conexões de LLM local, Gitea API (com base64 creds), e persistência no PG (`psycopg2`) estão testadas e saudáveis.
- **Workflow Ativo**: Envie um novo break test ao repositório ou dispare manualmente um curl de alerta simulado, e veja a mágica dos 4 Agentes rodando orquestrados.
