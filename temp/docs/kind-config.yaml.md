Para que o **Antigravity** consiga orquestrar o ambiente conforme o planejamento, o arquivo `kind-config.yaml` precisa ser configurado com mapeamentos de porta específicos (para o Ingress) e montagens de volume (para as **Git Worktrees** e manipulação de arquivos no seu Fedora).

Aqui está o arquivo configurado para o seu setup de **SRE AI-Agent Lab**:

---

### `kind-config.yaml`

YAML

```
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: ai-sre-lab
nodes:
- role: control-plane
  # Configuração do Ingress para expor Gitea, Grafana, ArgoCD e Rocket.Chat
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
  
  # Montagem de Volumes para persistência e manipulação do Agente DevOps (Skills)
  extraMounts:
  - hostPath: /home/marcelo/lab-infra-repo
    containerPath: /app/infra-repo
    # Permite que o DevOps Agent crie Git Worktrees diretamente no seu sistema de arquivos Fedora
    propagation: Bidirectional 

- role: worker
- role: worker

# Configuração para garantir que o Kind use a rede correta para falar com o Host (LM Studio)
networking:
  apiServerAddress: "127.0.0.1"
  apiServerPort: 6443
  podSubnet: "10.244.0.0/16"
  serviceSubnet: "10.96.0.0/12"
```

---

### 📝 Notas de Implementação para o Antigravity

- **Mapeamento de Porta:** O Ingress Controller será instalado pelo Antigravity para rotear o tráfego de `localhost` (portas 80/443) para os serviços internos como **Gitea** e **Grafana**.
    
- **Persistent Storage (HostPath):** O caminho `/home/marcelo/lab-infra-repo` deve existir no seu Fedora antes do deploy. O Agente DevOps utilizará esse local para executar suas **Skills** de Git.
    
- **Propagação Bidirecional:** Essencial para que as mudanças feitas pelo **DevOps Agent** (como a criação de uma pasta de worktree) sejam visíveis instantaneamente tanto para o container quanto para o seu sistema operacional.
    

### Próximo Passo

Com este arquivo, o **Antigravity** pode iniciar o provisionamento. Gostaria que eu preparasse o manifesto do **Auditor Agent** com o script para gerar o relatório **Post-Mortem** em Markdown automaticamente?