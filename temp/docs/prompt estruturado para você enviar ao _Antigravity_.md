O **Antigravity** orquestra a montagem completa deste laboratório no seu Fedora, utilizando uma estratégia **Hardware-Aware** e **GitOps-First**. Este prompt consolidado é o "Manual de Voo" para o provisionamento.

---

### 🚀 Prompt para Antigravity: "Digital Twin | SRE AI-Ops Lab Provisioning"

"Atue como um **Principal Platform Engineer** e utilize o **Antigravity** para provisionar o laboratório **Digital Twin** no meu Fedora 42. Este é um ambiente de Auto-Remediação Agêntica de alta maturidade.

**Cenário de Hardware (CRÍTICO):**
O host possui um **Intel i7** e uma **NVIDIA RTX 4070 (12GB VRAM)**. Toda a estratégia de execução de IA deve ser **Hardware-Aware**, utilizando o recurso `ai.sre/low-resource-mode` se o consumo de VRAM exceder 80%.

**Siga rigorosamente estas diretrizes de montagem:**

#### 1. Infraestrutura Base (Kind & Network)
- Crie o cluster `ai-sre-lab` (1 Control-Plane, 2 Workers) com suporte a Ingress.
- Monte `/home/marcelo/lab-infra-repo` como o volume persistente de código padrão.
- **[CRÍTICO - HYBRID DNS]:** Configure o service `lm-studio` (ExternalName) apontando para a interface host do kind (`172.18.0.1:1234`) para conectar as IAs locais.
- **[CRÍTICO - PERSISTENCE]:** Defina um PersistentVolume (PV) mapeado para um diretório real do NVMe e atrele um PVC ao banco de dados do **Archivist Agent** para retenção de histórico de incidentes.

#### 2. Stack de Observabilidade & Routing de Alertas
- Instale `kube-prometheus-stack` e `Loki/Promtail` no namespace `monitoring`.
- Aplique a **Taxonomia de Labels** (ver `docs/Taxonomia de Labels.md`) em todos os recursos para garantir logs estruturados e correlação de eventos.
- **[CRÍTICO - ALERT ROUTING]:** Configure o `AlertmanagerConfig` estabelecendo o endpoint do `Orchestrator Agent` (porta 8080) como receiver para todos os alertas críticos.

#### 3. Core Agêntico & Feature Flags (AIOps Ready)
- Realize o deploy da equipe no namespace `ai-ops`: **Orchestrator, Analyst, DevOps, Auditor, The Archivist**.
- **Feature Flags:** Garanta que os agentes consultem as flags de segurança (ex: `ai.sre/auto-remediation`) antes de realizar alterações no cluster. O comportamento padrão deve ser `dry-run: ON` até validação manual.
- Integre o **Rocket.Chat** para notificações de comando e controle.

#### 4. GitOps Workflow & Vault Bootstrap
- Provisione o **Gitea** (gitops) e o **Argo CD** (argocd).
- Configure o pipeline para que o Agente DevOps interaja com o repositório local e o Argo CD sincronize as mudanças.
- **[CRÍTICO - VAULT SEEDING]:** Execute o script de inicialização do Vault (`vault-bootstrap.sh`) injetando as credenciais essenciais para habilitar o *first-push* do DevOps Agent.

#### 5. Segurança & Governança (The Warden)
- Aplique as restrições do **Security Officer** para garantir que os agentes de IA não tenham acesso a segredos fora de seu escopo.

**Ao concluir, apresente o 'Dashboard de Conectividade' com os endpoints locais e o status de saúde da GPU.**"

---

### 🧠 O que muda com este prompt?

1.  **Conectividade e Persistência Sanadas:** Agora o LM Studio roda transparente para os agentes e o Archivist nunca perde dados se o pod morrer.
2.  **Alertas Ativos:** O Prometheus sabe exatamente para onde mandar a "dor" (para a IA), e não para o vazio.
3.  **Segurança por Design:** A inclusão das Feature Flags impede ações destrutivas sem aprovação (Ops Flags), e o Vault garante que senhas não fiquem plantadas no texto puro.
4.  **Rastreabilidade:** A taxonomia garante que todos os logs gerados pelos agentes sejam fáceis de filtrar no Grafana/Loki.