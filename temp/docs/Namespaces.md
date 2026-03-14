Para garantir a organização, isolamento de recursos e segurança (RBAC) do seu laboratório no **Fedora**, a estrutura de namespaces deve ser segmentada por responsabilidade técnica.

Aqui está a visão explodida da topologia de recursos por namespace, detalhando o que roda em cada um, as portas e as comunicações:

---

### 1. Namespace: `ai-ops` (O Coração Agêntico)

Onde residem os agentes e a base de dados de inteligência.

- **Orchestrator Agent**: Listener HTTP (Porta `8080`). Ponto de entrada para alertas.
    
- **Analyst Agent**: Worker de diagnóstico. Utiliza **MCP** para ler métricas e logs.
    
- **DevOps Agent**: Executor de patches. Possui volume montado para **Git Worktree**.
    
- **Auditor Agent**: Validador e gerador de Post-mortem.
    
- **Archivist Agent**: Gerente da base de dados histórica.
    
- **PostgreSQL**: Base de dados persistente (Porta `5432`) para histórico de SLA/SLO.
    
- **Preflight-Job**: Script de validação de conectividade com o **LM Studio** (Host).
    

---

### 2. Namespace: `gitops` (A Fonte da Verdade)

Responsável pela infraestrutura como código (IaC) e sincronização.

- **Gitea**: Servidor Git local (Portas `3000` HTTP, `22` SSH). Armazena os repositórios de infra.
    
- **Argo CD**: Controlador de GitOps (Portas `8080` API, `443` UI). Sincroniza o Gitea com o cluster.
    
- **Redis**: Cache para o Argo CD acelerar a detecção de mudanças.
    

---

### 3. Namespace: `monitoring` (Os Sentidos)

Camada de observabilidade que alimenta os agentes com dados brutos.

- **Prometheus**: Coleta métricas do cluster e exporters (Porta `9090`).
    
- **Alertmanager**: Roteia alertas para o `Orchestrator Agent` via webhook.
    
- **Grafana**: Visualização e **Query Inspector** (Porta `3000`).
    
- **Loki**: Agregador de logs (Porta `3100`).
    
- **Thanos**: Sidecars e Querier para métricas históricas de longa duração.
    

---

### 4. Namespace: `communication` (Interface Humana)

Onde o SRE interage com a IA.

- **Rocket.Chat**: Servidor de mensagens (Porta `3000`). Recebe diagnósticos e botões de ação.
    
- **MongoDB**: Base de dados persistente para as mensagens do Rocket.Chat.
    

---

### 5. Namespace: `app-production` (O Alvo)

Onde as aplicações de teste e falhas propositais ocorrem.

- **Target App**: Pod configurado pelo **Antigravity** com erros propositais (ex: Dockerfile corrompido).
    
- **Prometheus Exporters**: Exportam métricas específicas da aplicação para gerar alertas.
    

---

### 📊 Tabela de Comunicação entre Namespaces

|**Origem (Namespace)**|**Destino (Namespace)**|**Protocolo/Porta**|**Objetivo**|
|---|---|---|---|
|`monitoring`|`ai-ops`|HTTP/8080|Alertmanager envia evento para Orchestrator.|
|`ai-ops`|`monitoring`|HTTP/3000-9090|Analyst usa **MCP** para ler métricas/logs.|
|`ai-ops`|**Host (Fedora)**|HTTP/1234|Agentes consultam o **LM Studio**.|
|`ai-ops`|`gitops`|HTTP/3000|DevOps faz push do patch para o Gitea.|
|`gitops`|`app-production`|K8s API|Argo CD aplica o fix no cluster.|
|`ai-ops`|`communication`|Webhook/API|Agentes notificam e recebem aprovação humana.|

---

### 🗺️ Diagrama de Estrutura de Recursos (Mermaid)

Snippet de código

```
graph TD
    subgraph Cluster_Kind ["Cluster Kind (Local)"]
        
        subgraph NS_AiOps ["Namespace: ai-ops"]
            AgTeam["Agent Team <br/>(Orch, Anly, Dev, Aud, Arch)"]
            DB[("PostgreSQL <br/>(Incident History)")]
        end

        subgraph NS_GitOps ["Namespace: gitops"]
            GT[("Gitea <br/>(Local Repo)")]
            Argo["Argo CD <br/>(GitOps Controller)"]
        end

        subgraph NS_Monitoring ["Namespace: monitoring"]
            Prom["Prometheus"]
            Graf["Grafana <br/>(Query Inspector)"]
            Lok["Loki"]
        end

        subgraph NS_Comm ["Namespace: communication"]
            RC["Rocket.Chat"]
        end

        subgraph NS_App ["Namespace: app-production"]
            Target["Target App <br/>(Faulty Pod)"]
        end
    end

    subgraph Host_Fedora ["Host: Fedora 42"]
        LM[("🧠 LM Studio")]
        Worktree["📂 HostPath Volume <br/>(Git Worktree)"]
    end

    %% Conexões Estratégicas
    AgTeam -->|Inference| LM
    AgTeam -->|MCP Query| NS_Monitoring
    AgTeam -->|Write Fix| GT
    AgTeam -->|Read/Write| DB
    AgTeam -->|Notify| RC
    GT -->|Sync| Argo
    Argo -->|Deploy| Target
    RC -->|Action Approval| AgTeam
    AgTeam -.->|Git Operations| Worktree
```

Esta estrutura garante que, se você precisar reiniciar o sistema de monitoramento, os agentes e a base de dados histórica (`ai-ops`) permanecerão intactos, mantendo a integridade do seu SLA.

**Qual o próximo passo: quer que eu gere o script SQL para a tabela de incidentes no PostgreSQL do namespace `ai-ops`?**