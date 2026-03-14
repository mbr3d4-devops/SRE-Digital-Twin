Este documento é o **Standard Operating Procedure (SOP)** de Metadados para o seu ecossistema. Ao alimentar o **Antigravity** com estas definições, você garante que a IA não apenas "veja" recursos, mas entenda o **contexto operacional** de cada um.

---

# 📑 Especificação Técnica: Taxonomia de Labels (SRE AI-Lab)

## 1. Objetivo

Padronizar a classificação de recursos no cluster **ai-sre-lab** para permitir:

- **Roteamento Dinâmico:** Alertas direcionados aos agentes corretos.
    
- **Observabilidade Granular:** Dashboards no Grafana filtrados por função.
    
- **Governança:** Bloqueio de ações não autorizadas pelo Auditor Agent.
    

---

## 2. Categorias de Labels (Dicionário de Dados)

### A. Metadados de Identidade (Standard K8s)

Estas labels devem estar presentes em **todos** os objetos para compatibilidade com Argo CD e Helm.

|**Chave**|**Exemplo**|**Descrição**|
|---|---|---|
|`app.kubernetes.io/name`|`analyst`|Nome do componente específico.|
|`app.kubernetes.io/part-of`|`sre-ai-lab`|Nome do projeto global.|
|`app.kubernetes.io/managed-by`|`argocd`|Ferramenta que gerencia o ciclo de vida.|

### B. Labels Operacionais (Agente-Specific)

Utilizadas pela equipe de agentes para comunicação e estado.

|**Chave**|**Valores Possíveis**|**Função**|
|---|---|---|
|`sre.ai/agent-role`|`orchestrator`, `analyst`, `devops`, `auditor`, `archivist`|Identifica a "profissão" do Pod.|
|`sre.ai/state`|`healthy`, `investigating`, `remediating`, `degraded`|Estado atual do recurso visto pela IA.|
|`sre.ai/incident-id`|`INC-2026-001`|Vincula um recurso a um incidente ativo no Archivist.|

### C. Labels de Governança (StackGuard)

Lidas pelo Auditor Agent para permitir ou negar operações de escrita/patch.

|**Chave**|**Valores Possíveis**|**Função**|
|---|---|---|
|`sre.ai/policy`|`strict`, `relaxed`, `manual-only`|Nível de autonomia da IA sobre o recurso.|
|`sre.ai/criticality`|`tier-0`, `tier-1`, `tier-2`|Define prioridade de remediação e impacto.|
|`sre.ai/auto-healing`|`true`, `false`|Se `false`, o DevOps Agent é bloqueado de agir.|

---

## 3. Implementação Prática (YAML snippets)

### Exemplo: Deployment do Analyst Agent

O Antigravity deve garantir que o template de pod contenha:

YAML

```
metadata:
  labels:
    app.kubernetes.io/name: analyst
    sre.ai/agent-role: analyst
    sre.ai/policy: strict
    sre.ai/state: healthy
    hardware/affinity: gpu-preferred # Para o seu i7/RTX4070
```

### Exemplo: Aplicação Alvo (Target-App)

Para que o sistema monitore erros reais, a aplicação deve ser marcada:

YAML

```
metadata:
  labels:
    sre.ai/monitored: "true"
    sre.ai/owner-team: "platform-ops"
    sre.ai/slo-tier: "99.9"
```

---

## 4. Roteamento de Alertas via Labels

Instrução para o **Alertmanager** no arquivo `alertmanager-config.yaml`:

YAML

```
route:
  group_by: ['sre.ai/agent-role'] # Alertas agrupados por agente responsável
  routes:
    - match:
        severity: critical
      receiver: orchestrator-webhook
```

---

## 5. Script de Aplicação em Lote: `apply-standard-labels.sh`

O Antigravity deve executar este script para "sanear" o cluster após o deploy inicial:

Bash

```
#!/bin/bash
echo "🏷️ Aplicando taxonomia de labels no cluster..."

# Marcar o namespace de IA
kubectl label namespace ai-ops sre.ai/stack=ai-core --overwrite

# Marcar o Persistent Volume do Archivist
kubectl label pv $(kubectl get pv -o jsonpath='{.items[0].metadata.name}') \
    sre.ai/data-criticality=high --overwrite

# Marcar Pods de agentes com política de proteção
kubectl label pods -n ai-ops -l app.kubernetes.io/part-of=sre-ai-lab \
    sre.ai/auto-healing=false --overwrite

echo "✅ Taxonomia aplicada com sucesso."
```

---

## 6. Por que isso é vital para o Antigravity?

Com estas labels, se você perguntar ao Antigravity: _"Quais aplicações estão sob investigação da IA agora?"_, ele simplesmente executará:

`kubectl get pods -A -l sre.ai/state=investigating`

A resposta será precisa e baseada na verdade do cluster, não em suposições.

**Marcelo, este documento encerra a padronização de metadados. Gostaria que eu preparasse um "Manual de Troubleshooting de Labels" para os agentes saberem o que fazer quando encontrarem um recurso sem etiqueta?**


## O Gemini disse

Este é um manual estratégico para os seus agentes (e para o Antigravity). No mundo SRE, uma label errada ou ausente é como um fio cortado em um painel elétrico: a energia (os dados/alertas) está lá, mas não chega ao destino.

---

# 🛠️ Manual de Troubleshooting de Labels (SRE AI-Lab)

Este guia deve ser injetado na **Skill do Analyst Agent** para que ele saiba como agir quando a observabilidade falhar.

### 1. O Sintoma: "Silêncio Operacional"

Se um alerta disparou no Prometheus mas o **Orchestrator** não reagiu, o problema 90% das vezes é uma label de roteamento.

**Ação do Agente:**

- **Comando:** `kubectl get pods -A --show-labels`
    
- **Checklist:**
    
    1. O Pod alvo tem a label `sre.ai/monitored: "true"`?
        
    2. A severidade no alerta casa com a label `sre.ai/agent-role` esperada?
        
    3. Existe o seletor `app.kubernetes.io/name` para o Argo CD identificar o recurso?
        

### 2. O Protocolo de "Auto-Saneamento"

Se o **Analyst** encontrar um recurso sem etiquetas, ele não deve ignorá-lo. Ele deve:

1. **Identificar:** Usar a imagem do container e o namespace para deduzir o papel do recurso.
    
2. **Notificar:** Enviar mensagem ao Rocket.Chat: _"⚠️ Detectado recurso [NOME] sem taxonomia. Aplicando labels padrão de segurança."_
    
3. **Corrigir:** Executar `kubectl label [RESOURCE] [NAME] sre.ai/state=unknown sre.ai/policy=strict`.
    

### 3. Matriz de Erros Comuns

|Erro|Consequência|Como Corrigir|
|---|---|---|
|**Typo na Label**|Alertas ignorados ou dashboards vazios.|Usar `kubectl label --overwrite` com a grafia correta.|
|**Label vs Selector**|O Service não encontra os Pods (503 Service Unavailable).|Validar se o `spec.selector` do Service bate com o `spec.template.metadata.labels` do Deployment.|
|**Falta de Label de Vault**|O Pod sobe sem as senhas do Gitea/DB.|Injetar `vault.hashicorp.com/agent-inject: "true"`.|