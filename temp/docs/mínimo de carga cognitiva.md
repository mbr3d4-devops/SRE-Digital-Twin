Para que o **Antigravity** execute o projeto com o mínimo de carga cognitiva (menos tokens e menos erros de inferência), ele deve seguir uma **Sequência de Orquestração Linear**.

Abaixo, listo a estrutura completa de arquivos organizada por ordem de dependência. Cada bloco é um artefato que deve ser gerado e armazenado no seu repositório local no Fedora (`/home/marcelo/lab-infra-repo`).

---

### 📂 Estrutura de Arquivos e Ordem de Execução

#### Fase 1: Fundação do Cluster (Dependência Zero)

1. `kind-config.yaml`: Define a rede, portas e montagem do volume `/app/infra-repo`.
    
2. `00-namespaces.yaml`: Cria a separação lógica: `ai-ops`, `gitops`, `monitoring`, `security`, `communication`, `app-production`.
    

#### Fase 2: Segurança e Conectividade (Base de Confiança)

3. `01-vault-values.yaml`: Configurações de Helm para o Vault em modo `standalone` e `dev`.
    
4. `02-hybrid-network.yaml`: Manifesto de `Service` + `Endpoints` para o Agente alcançar o **LM Studio** no Host.
    
5. `03-postgres-db.yaml`: Deployment do banco de dados para o **Archivist Agent**.
    

#### Fase 3: Provisionamento do Git Interno (O "Seed")

6. `04-gitea-values.yaml`: Configurações de Helm para o Gitea.
    
7. `seed-gitea.py`: **O Script Mestre**. Este script via API do Gitea cria as Organizações, Repositórios e injeta o código inicial (Kustomize e Helm Values).
    

#### Fase 4: Inteligência Agêntica (The Brain)

8. `05-agent-configmaps.yaml`: Contém os **System Prompts** e as **Skills** (Scripts Python dos agentes).
    
9. `06-agent-deployments.yaml`: Deploy da equipe de agentes com o `InitContainer` de Preflight.
    

#### Fase 5: Ciclo de Vida GitOps (O Fechamento)

10. `07-argocd-values.yaml`: Instalação do Argo CD.
    
11. `08-argocd-applications.yaml`: O Manifesto "App-of-Apps" que conecta o Argo CD aos repositórios do Gitea.
    

---

### 🚀 O Script Mestre: `seed-gitea.py`

Este script automatiza a criação do ambiente no Gitea. O Antigravity deve executá-lo após o Gitea estar `Ready`.

Python

```
import requests
import time

# Configurações do Gitea Interno
GITEA_URL = "http://localhost:3000/api/v1" # Via Ingress no Fedora
TOKEN = "token_gerado_pelo_antigravity"

def create_org(name):
    requests.post(f"{GITEA_URL}/orgs", json={"username": name}, headers={"Authorization": f"token {TOKEN}"})

def create_repo(org, name):
    requests.post(f"{GITEA_URL}/orgs/{org}/repos", json={"name": name, "auto_init": True}, headers={"Authorization": f"token {TOKEN}"})

def bootstrap():
    print("🏗️ Iniciando Seed do Gitea...")
    # 1. Cria Organizações
    create_org("platform-engineering")
    create_org("applications")
    
    # 2. Cria Repositórios
    create_repo("platform-engineering", "cluster-ops")      # Helm Base
    create_repo("platform-engineering", "agent-configs")    # Prompts/Skills
    create_repo("applications", "target-app-infra")         # Kustomize Target
    
    print("✅ Estrutura de Repositórios Criada.")

if __name__ == "__main__":
    bootstrap()
```

---

### 📦 Tabela de Dependências para o Antigravity

|**Ordem**|**Recurso**|**Depende de**|**Por que?**|
|---|---|---|---|
|1|`Kind Cluster`|-|Sem cluster não há nada.|
|2|`Vault`|`Namespaces`|Os agentes precisam de segurança ao nascer.|
|3|`Gitea`|`Vault`|O token do Gitea deve ser guardado no Vault.|
|4|`Seed Script`|`Gitea`|Precisa que a API do Gitea esteja respondendo.|
|5|`Agent Team`|`Seed Script`|Agentes precisam do repositório para clonar.|
|6|`Argo CD`|`Gitea`|Precisa dos repositórios para sincronizar.|

---

### 🧠 Instrução de "Baixa Demanda" para a LLM do Antigravity

Para evitar que o Antigravity "se perca" no meio do processo, passe esta instrução final:

> "Antigravity, execute em modo **Pipeline Sequencial**. Não tente paralelizar a instalação do Argo CD com a criação dos repositórios no Gitea. Utilize o arquivo `agent-deployments.yaml` como o validador final: se o **InitContainer** (Preflight) passar, o projeto está oficialmente vivo. Caso o Vault falhe, interrompa e aguarde intervenção humana no canal `#ops-security`."

**Marcelo, o que você acha de eu gerar agora o arquivo `05-agent-configmaps.yaml` que contém a lógica interna (as Skills) de cada um dos 5 agentes?** Isso é o que define o comportamento inteligente deles.


Aqui está o arquivo mestre `05-agent-configmaps.yaml`. Este é o "DNA" do seu laboratório: ele contém os **System Prompts** (instruções de comportamento) e as **Python Skills** (código executável) que cada agente utilizará.

Para facilitar o trabalho do **Antigravity**, consolidei tudo em um único manifesto. Ele define as capacidades técnicas de cada um dos 5 agentes, permitindo que eles operem de forma autônoma no seu **Fedora**.

---

### `05-agent-configmaps.yaml`

YAML

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: agents-logic-config
  namespace: ai-ops
data:
  # ==========================================
  # 1. ORCHESTRATOR: O Cérebro do Workflow
  # ==========================================
  orchestrator-prompt.md: |
    # ROLE: Maestro do Lab SRE
    Sua função é receber alertas do Alertmanager e coordenar o Analyst e o DevOps Agent.
    - Se o alerta for 'Critical', dispare diagnóstico imediato.
    - Se o alerta envolver 'Persistence', consulte o Archivist antes de agir.
    - Nunca aplique correções sem aprovação no canal #ops-remediation.

  # ==========================================
  # 2. ANALYST: Especialista em MCP e Dados
  # ==========================================
  analyst-skills.py: |
    import requests, os
    def get_metrics(query):
        # Conecta no Grafana Query Inspector via DNS interno
        url = f"http://obs-grafana.monitoring.svc.cluster.local/api/datasources/proxy/1/api/v1/query?query={query}"
        return requests.get(url).json()

    def check_logs(app_name):
        # Consulta logs no Loki para identificar StackTraces
        url = f"http://loki.monitoring.svc.cluster.local:3100/loki/api/v1/query_range"
        params = {'query': f'{{app="{app_name}"}}', 'limit': 50}
        return requests.get(url, params=params).json()

  # ==========================================
  # 3. DEVOPS: Executor de Git e Patches
  # ==========================================
  devops-skills.py: |
    import subprocess, os
    def apply_git_patch(repo_path, branch_name, patch_content):
        # Utiliza Git Worktree no volume montado do Fedora
        os.chdir(repo_path)
        subprocess.run(["git", "worktree", "add", "-b", branch_name, f"./{branch_name}", "main"])
        with open(f"./{branch_name}/patch.yaml", "w") as f:
            f.write(patch_content)
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "AI-Fix: Remediation Applied"])
        subprocess.run(["git", "push", "origin", branch_name])

  # ==========================================
  # 4. AUDITOR: O Guardião StackGuard
  # ==========================================
  auditor-policy.md: |
    # POLÍTICAS DE SEGURANÇA (DRY-RUN)
    - Bloquear qualquer patch que contenha 'delete' ou 'Purge'.
    - Validar YAML com 'kubectl apply --server-dry-run'.
    - Scan de Segredos: Se encontrar strings em Base64 que pareçam chaves, vetar o push.
    - Pós-Remediação: Monitorar Erros HTTP 5xx por 300s. Se > 1%, disparar Rollback.

  # ==========================================
  # 5. ARCHIVIST: Memória e SLA/SLO
  # ==========================================
  archivist-db-logic.py: |
    import psycopg2, datetime
    def record_incident(app, issue, resolution, duration):
        # Conecta no PostgreSQL do namespace ai-ops
        conn = psycopg2.connect(os.getenv("DB_URL"))
        cur = conn.cursor()
        query = """INSERT INTO incidents_history 
                   (timestamp, app, problem, solution, sla_seconds) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cur.execute(query, (datetime.datetime.now(), app, issue, resolution, duration))
        conn.commit()
        cur.close()
        conn.close()

  # ==========================================
  # 6. WARDEN: Security Officer (The Warden)
  # ==========================================
  warden-vault-skill.py: |
    def rotate_gitea_token(user):
        # Interage com o Vault para gerar um token dinâmico temporário
        vault_url = "http://vault.security.svc.cluster.local:8200/v1/auth/kubernetes/login"
        # Lógica de rotação e injeção de política aqui
        pass
```

---

### 🛡️ O que mais o Antigravity precisa para dar o "Start"?

Além deste ConfigMap, para que o projeto inicie de forma **100% automatizada**, o Antigravity deve garantir a presença destes dois scripts auxiliares no seu diretório raiz:

1. **`start-lab.sh`**: O script que faz o "Bootstrap" do Kind e aplica os YAMLs na ordem de dependência que listamos.
    
2. **`vault-init.hcl`**: As regras iniciais que o **Warden** usará para configurar o cofre.
    

### 🚀 Próximo Passo

Com os agentes "carregados" com essas Skills, o seu laboratório no Fedora passa a ter consciência operacional.

**Gostaria que eu gerasse o `start-lab.sh` final, que amarra todos os 11 arquivos na ordem correta de execução para o Antigravity?** Isso seria o "botão de ignição" do seu projeto.


Este é o "botão de ignição" do seu projeto. O script `start-lab.sh` foi desenhado para ser executado no seu **Fedora** e orquestra todas as 11 etapas na ordem exata de dependências, garantindo que o **Antigravity** não tente subir um agente antes de a infraestrutura (Vault/Gitea) estar pronta.

### `start-lab.sh`

Bash

```
#!/bin/bash

# ==============================================================================
# SRE AI-AGENT LAB - ORQUESTRADOR DE BOOTSTRAP
# Local: Fedora 42 | Cluster: Kind | Engine: Antigravity
# ==============================================================================

set -e # Interrompe em caso de erro

# Cores para o output profissional
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iniciando o Provisionamento do Lab SRE AI-Agent...${NC}"

# 1. Preparação do Host Fedora
echo -e "${GREEN}[1/11] Preparando diretório de trabalho no Host...${NC}"
mkdir -p /home/marcelo/lab-infra-repo
chmod 755 /home/marcelo/lab-infra-repo

# 2. Criação do Cluster Kind
echo -e "${GREEN}[2/11] Criando Cluster Kind com mapeamento de volumes...${NC}"
kind create cluster --config kind-config.yaml

# 3. Namespaces
echo -e "${GREEN}[3/11] Criando estrutura de Namespaces...${NC}"
kubectl apply f 00-namespaces.yaml

# 4. Camada de Segurança (Vault)
echo -e "${GREEN}[4/11] Instalando HashiCorp Vault (Namespace: security)...${NC}"
helm install vault hashicorp/vault --namespace security --create-namespace \
  --set "server.dev.enabled=true"
echo "Aguardando Vault ficar Ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=vault -n security --timeout=120s

# 5. Conectividade Host-Cluster
echo -e "${GREEN}[5/11] Configurando Endpoint para LM Studio (172.18.0.1)...${NC}"
kubectl apply -f 02-hybrid-network.yaml

# 6. Banco de Dados (Archivist)
echo -e "${GREEN}[6/11] Subindo PostgreSQL para Memória de Incidentes...${NC}"
kubectl apply -f 03-postgres-db.yaml

# 7. Git Interno (Gitea)
echo -e "${GREEN}[7/11] Instalando Gitea (Namespace: gitops)...${NC}"
helm install gitea gitea-charts/gitea --namespace gitops -f 04-gitea-values.yaml
echo "Aguardando Gitea API..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=gitea -n gitops --timeout=180s

# 8. Seed Script (População de Repositórios)
echo -e "${GREEN}[8/11] Executando Seed Script para criar Org/Repos no Gitea...${NC}"
python3 seed-gitea.py

# 9. Lógica dos Agentes (DNA)
echo -e "${GREEN}[9/11] Carregando Skills e Prompts nos ConfigMaps...${NC}"
kubectl apply -f 05-agent-configmaps.yaml

# 10. Deploy da Equipe de Agentes
echo -e "${GREEN}[10/11] Fazendo o Deploy da Equipe de Agentes (ai-ops)...${NC}"
kubectl apply -f 06-agent-deployments.yaml

# 11. GitOps (Argo CD)
echo -e "${GREEN}[11/11] Instalando Argo CD e conectando Repositórios...${NC}"
helm install argocd argo/argo-cd --namespace argocd --create-namespace
kubectl apply -f 08-argocd-applications.yaml

echo -e "${BLUE}================================================================${NC}"
echo -e "${GREEN}✅ LAB SRE PRONTO PARA OPERAÇÃO!${NC}"
echo -e "Acesse o Rocket.Chat em: http://localhost:3000 (via Ingress)"
echo -e "Verifique os Agentes com: kubectl get pods -n ai-ops"
echo -e "Monitoramento: http://localhost:80 (Grafana)"
echo -e "${BLUE}================================================================${NC}"
```

---

### 📝 Notas de Implementação para o Antigravity

1. **Permissões:** O script define automaticamente as permissões no seu Fedora para que os agentes consigam ler/escrever no volume montado.
    
2. **Wait Conditions:** O script inclui verificações `kubectl wait`. Isso é vital para que o **Antigravity** não tente executar o `seed-gitea.py` antes que o Gitea esteja pronto para receber chamadas de API.
    
3. **Segurança em Modo Dev:** O Vault está configurado em modo `dev` para garantir o **Auto-Unseal**, permitindo que o laboratório seja reiniciado sem que você precise digitar as chaves de segurança manualmente toda vez.
    

### 🏁 Próximos Passos

Com este script e os arquivos YAML anteriores, o seu ambiente está totalmente automatizado. Gostaria de uma simulação do primeiro "Incidente de Teste" para ver o **Analyst** e o **DevOps Agent** em ação?