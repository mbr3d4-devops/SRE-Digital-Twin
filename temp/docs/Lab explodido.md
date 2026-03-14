Esta é a visão explodida e minuciosa de todo o ecossistema. Aqui, detalhamos a "fiação" técnica que permite a fluidez entre o seu **Fedora** e o cluster **Kind**, garantindo que cada agente saiba exatamente onde atuar e como se comunicar.

---

## 1. Arquitetura do Ecossistema Híbrido: Conectividade e Portas

A arquitetura é dividida entre o **Host** (sua máquina) e o **Control Plane** do Kubernetes.

### Localização e Acesso

- **LM Studio (Host Fedora):**
    
    - **Porta:** `1234`.
        
    - **Acesso:** O servidor deve estar em modo `bind 0.0.0.0` para aceitar conexões da rede do Docker/Kind.
        
    - **DNS Interno:** O Agente acessa via `http://172.18.0.1:1234` (Gateway do Kind).
        
- **Acesso Externo (Fora do Cluster):**
    
    - Utilizaremos o **Ingress Nginx** mapeando portas do Host para o Cluster:
        
        - **Gitea:** `http://localhost:3000`
            
        - **Grafana:** `http://localhost:3001`
            
        - **Rocket.Chat:** `http://localhost:3002`
            
        - **Argo CD:** `http://localhost:3003`
            

---

## 2. A Equipe de Agentes: Visão Explodida

Todos os agentes rodam como **Pods Python** dentro do namespace `ai-ops`. Eles se comunicam via **gRPC** ou **FastAPI HTTP** interno.

### A. Orchestrator Agent (O Maestro)

- **Onde roda:** Pod `orchestrator-agent` (Deployment).
    
- **Escuta:** Webhook na porta `8080`.
    
- **Função:** Recebe o alerta do Alertmanager, cria o ID do incidente e despacha tarefas para os Sub-Agents.
    
- **Comunicação:** Envia prompts formatados para o LM Studio e notificações para o Rocket.Chat.
    

### B. Analyst Agent (O Investigador - MCP Specialist)

- **Onde roda:** Pod `analyst-agent`.
    
- **Plugins & MCPs:** Implementa o **Model Context Protocol** para conectar em:
    
    - **Prometheus API (Porta 9090):** Query de métricas.
        
    - **Grafana API (Porta 3000):** Extração do **Query Inspector**.
        
    - **Loki API (Porta 3100):** Busca de logs brutos.
        
- **Output:** Gera um relatório técnico resumido para o Orchestrator.
    

### C. DevOps Agent (O Executor - Git Worktree Specialist)

- **Onde roda:** Pod `devops-agent` com volume `HostPath` montado.
    
- **Skills (Habilidades):**
    
    - **Manipulação de Git:** Clonagem do Gitea interno.
        
    - **Git Worktree:** Cria um ambiente em `/tmp/fix-<id>` para evitar sujar a branch principal.
        
- **Fluxo:** Edita o arquivo -> Faz o Push para o Gitea -> Notifica o Orchestrator.
    

### D. Auditor Agent (O Post-Mortem & Validator)

- **Novo Agente:** Responsável pela validação final e documentação.
    
- **Função:** * **Validação:** Monitora o Grafana 5 minutos após o deploy para confirmar a queda nos erros.
    
    - **Post-Mortem:** Consolida o alerta original, o log de diagnóstico do Analyst e a ação do DevOps em um relatório Markdown.
        
- **Output:** Envia o **Post-Mortem** para o Rocket.Chat e salva no Gitea em uma pasta `/docs/incidents/`.
    

---

## 3. Fluxo de Remediação: Ciclo Fechado (Passo a Passo)

1. **Alerta (Prometheus):** Detecta falha -> Envia JSON para `orchestrator:8080`.
    
2. **Investigação (Analyst):** O Orchestrator pede análise. O Analyst usa **MCP** para ler o Grafana Inspector.
    
3. **Decisão (LM Studio):** O Orchestrator envia os dados ao LM Studio (`172.18.0.1:1234`).
    
4. **Ação (DevOps):** Após o "OK" no Rocket.Chat, o DevOps abre a **Git Worktree**, altera o YAML e dá push no Gitea.
    
5. **Sync (Argo CD):** O Argo CD puxa a alteração do Gitea e aplica no cluster.
    
6. **Encerramento (Auditor):** O Auditor valida a saúde do Pod e gera o relatório Post-Mortem.
    

---

## 4. Segurança e Conectividade (StackGuard)

- **Preflight Check:** Antes de iniciar, o script valida se o `kind0` consegue "pingar" a porta `1234` do seu Fedora.
    
- **Isolamento:** Nenhuma Skill tem permissão de `DELETE`. A única forma de alterar o cluster é via Push no Gitea (GitOps).
    
- **Secrets:** Se o Analyst detectar `Unauthorized`, o DevOps não edita código; ele solicita ao Vault a rotação da credencial.
    

---

## 🗺️ Diagrama Mermaid: Visão Explodida dos Componentes

Snippet de código

```
graph TB
    subgraph Host_Fedora ["💻 HOST: FEDORA 42 (Antigravity Managed)"]
        LM[("🧠 LM Studio <br/>(Port 1234/0.0.0.0)")]
        LocalRepo[("📂 Local Git Worktree Space <br/>(/home/marcelo/lab-infra)")]
    end

    subgraph Cluster_Kind ["☸️ CLUSTER KIND (Network 172.18.0.x)"]
        
        subgraph Logic_Layer ["🤖 AGENT TEAM (Namespace: ai-ops)"]
            Orch["<b>Orchestrator Pod</b><br/>(Listener :8080)"]
            Anly["<b>Analyst Pod</b><br/>(MCP Client)"]
            DevOps["<b>DevOps Pod</b><br/>(Git/Worktree Skill)"]
            Audt["<b>Auditor Pod</b><br/>(Post-Mortem & Validation)"]
        end

        subgraph Infra_Layer ["📦 GITOPS & GIT (Namespace: gitops)"]
            Gitea[("🏗️ Gitea <br/>(:3000)")]
            Argo["🔄 Argo CD <br/>(:8080)"]
        end

        subgraph Obs_Layer ["📊 OBSERVABILITY (Namespace: monitoring)"]
            Prom["Prometheus <br/>(:9090)"]
            Graf["Grafana <br/>(:3000 / Query Inspector)"]
            Loki["Loki <br/>(:3100)"]
        end

        RC["💬 Rocket.Chat <br/>(:3000)"]
    end

    %% Fluxos de Comunicação
    Prom -->|1. Webhook JSON| Orch
    Orch -->|2. Get Context| Anly
    Anly -->|3. MCP Query| Graf
    Anly -->|4. MCP Logs| Loki
    
    Orch -->|5. Inference Request| LM
    LM -->|6. Diagnosis & Patch| Orch
    
    Orch -->|7. User Approval| RC
    RC -->|8. Trigger Fix| DevOps
    
    DevOps -->|9. Git Worktree Skill| LocalRepo
    DevOps -->|10. Push Code| Gitea
    Gitea -->|11. Webhook/Sync| Argo
    
    Argo -->|12. Deploy| Target["Target App Pod"]
    
    Target -.->|13. Telemetry| Obs_Layer
    Audt -->|14. Revalidation| Graf
    Audt -->|15. Generate Post-Mortem| RC
    Audt -->|16. Archive Doc| Gitea

    %% Estilos
    style Host_Fedora fill:#f9f,stroke:#333
    style Logic_Layer fill:#e1f5fe,stroke:#01579b
    style LM fill:#fff9c4,stroke:#fbc02d
    style Audt fill:#c8e6c9,stroke:#2e7d32
```

### O que mudou com o Auditor Agent?

Agora o seu laboratório não apenas "conserta" as coisas; ele se torna um sistema de aprendizado. O relatório **Post-Mortem** incluirá:

1. **Causa Raiz:** Identificada pelo Analyst.
    
2. **Tempo de Resolução:** Do alerta ao deploy.
    
3. **Evidência do Grafana:** Print dos dados do Query Inspector (em formato texto) provando que o fix funcionou.
    

**Podemos agora gerar o primeiro arquivo `post-mortem-template.md` que o Auditor Agent irá preencher automaticamente?**