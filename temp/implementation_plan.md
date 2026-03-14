# Orchestrator Avançado - Plano de Implementação (Ajustes Finos)

## Objetivo
Elevar o nível dos agentes no fluxo GitOps, adicionando consultas reais de observabilidade (Loki/Prometheus), persistência de post-mortems em repositório Git, e verificações de recorrência de incidentes históricos.

## Melhorias por Agente

### 1. The Orchestrator (O Maestro)
**Nova Feature: Verificação de Recorrência**
- Antes de disparar o Analyst/DevOps, o Orchestrator vai consultar o banco de dados PostgreSQL (`incident_logs`).
- Vai checar se aquele `alertname` e `namespace` já ocorreram no passado.
- Se sim, busca a solução que foi dada (`fix_description`) e posta um alerta no `#ops-critical` avisando: *"⚠️ Incidente Reincidente. Solução anterior: X"*.

### 2. The Analyst (O Investigador)
**Nova Feature: Observabilidade Rica (Loki/Prometheus + LLM)**
- Vai fazer requisições reais HTTP para o Loki (`http://loki.observability.svc.cluster.local:3100/loki/api/v1/query`) buscando logs do Pod nas últimas horas.
- Vai fazer requisições para o Prometheus (`http://prometheus-operated.monitoring.svc.cluster.local:9090/api/v1/query`) buscando métricas básicas (CPU/RAM).
- Vai enviar esses logs/métricas brutos como **contexto para o LLM (LM Studio)**.
- A resposta no Rocket.Chat terá detalhes ricos, evidências extraídas dos logs, e links dinâmicos para o Grafana Dashboard e Explore do Loki.

### 3. The Warden (O Fiscal)
**Nova Feature: Rastreador de Contexto (Audit Trail)**
- Vai reportar no `#ops-security` não apenas a aprovação do `dry-run`, mas **o que exatamente foi lido e manipulado**.
- Exemplo: *"Warden interceptou JSON do Analyst. Nenhuma Secret exposta nas variáveis do deployment `nginx-poison-deployment`. Validação Kustomize concluída."*
- Terá acesso ao LLM para gerar uma explicação clara e humana do risco e de por que a correção é segura, sem expor chaves.

### 4. The Archivist (O Historiador)
**Nova Feature: Post-Mortem Automático no Gitea**
- Adiciado ao fluxo pós-"Aprovação Humana" / "Status Resolved".
- Consulta o LLM passando toda a timeline do incidente (alerta, análise, fix_description) e pede a **geração de um Post-Mortem completo em Markdown**.
- Grava os dados no PostgreSQL (como já faz).
- **GitOps Commit**: O Archivist usará a Gitea API para criar um arquivo `postmortems/YYYY-MM-DD-alertname.md` no repositório `target-app-infra` (ou `cluster-ops`).
- Postará no `#ops-history` um resumo com um **botão linkando direto para o Markdown** no Gitea.

---

## Modificações no Código (`orchestrator.py`)

1. **Novos Helpers de Observabilidade**:
   - `query_loki(pod_name, namespace)`
   - `query_prometheus(query)`
2. **Helper de Banco de Dados Expandido**:
   - `check_recurring(alertname, namespace)`
3. **Novos Prompts de LLM**:
   - Prompt do Analyst (Contexto: Logs Reais)
   - Prompt do Archivist (Contexto: Timeline do Incidente gerando Markdown)
   - Prompt do Warden (Contexto: Mudanças no JSON)
4. **Novo Fluxo de Commit do Archivist**:
   - Função HTTP PUT para o Gitea (`/postmortems/...md`).

## Verification Plan
1. Quebrar o nginx novamente.
2. Confirmar que o Orchestrator avisa ser reincidente.
3. Confirmar que o Analyst posta logs reais do Loki.
4. Aprovar o erro, e confirmar que o Archivist comita um `.md` de Post-mortem no Gitea.
