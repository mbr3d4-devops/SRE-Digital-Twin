# Roadmap de Implementação Organizacional (SRE AI-Ops Lab)

Este documento define a ordem cronológica e lógica exata para levantar a infraestrutura do laboratório, garantindo que as dependências (como redes, diretórios e integrações) estejam prontas antes que os serviços que dependam delas tentem iniciar.

## Fase 1: Preparação do Host (Fedora) e Hardware
> O alicerce. Sem isso, o cluster Kind não sobe corretamente ou não usará todo o potencial de I/O e GPU.

- [x] **1.1 Criar a estrutura de diretórios no Host:**
    - Criar o diretório raiz `/home/marcelo/lab-infra-repo`.
    - Criar subdiretórios `scripts`, `manifests`, `manifests/observability-gitops`.
- [x] **1.2 Otimização e Permissões do Host (Tuning script):**
    - Criar e revisar o script `scripts/prepare-fedora-hw.sh`.
    - O script deve conter liberação do Firewall (`172.18.0.0/16`), ajuste de inotify (para Argo/Gitea), swappiness (para NVMe) e chcon do SELinux.
    - **Ação:** O usuário precisa rodar `sudo ./scripts/prepare-fedora-hw.sh`.
- [x] **1.3 Validação do LM Studio:**
    - Garantir que o LM Studio está rodando no Fedora, porta 1234, escutando em `0.0.0.0`, com a RTX 4070 (GPU Offload Max) ativa.

## Fase 2: Provisionamento do Cluster (Kind)
> O ambiente Kubernetes otimizado.

- [x] **2.1 Criar o manifesto do Kind (`kind-config.yaml`):**
    - Definir o `extraMounts` mapeando a pasta `/home/marcelo/lab-infra-repo`.
    - Definir `extraPortMappings` para as portas de Ingress/Git.
- [x] **2.2 Iniciar o Cluster:**
    - Executar o comando `kind create cluster --config manifests/kind-config.yaml`.

## Fase 3: Infraestrutura Base (Kubernetes Core)
> Namespaces, rotas e mapeamento do LM Studio para dentro do cluster.

- [x] **3.1 Criar e aplicar os Namespaces:**
    - Gerar e aplicar `manifests/namespaces.yaml` (`ai-ops`, `gitops`, `monitoring`, `communication`, `app-production`).
- [x] **3.2 Criar e aplicar Endpoint do LM Studio:**
    - Gerar e aplicar `manifests/connectivity.yaml` (Service `lmstudio-service` sem seletor, com Endpoint apontando para `172.18.0.1:1234`).
- [x] **3.3 Criar Banco de Dados do Post-Mortem:**
    - Gerar e aplicar `manifests/post-mortem-db.yaml` no namespace `ai-ops`.

## Fase 4: O Motor GitOps (Gitea e Argo CD)
> O coração do declarativo. O cluster passará a ser gerido por este núcleo.

- [x] **4.1 Criar o script de Seed do GitOps (`scripts/seed-gitops.sh`):**
    - Criar diretório e preparar os *values* locais para o Helm do Gitea.
    - Script deve instalar o Gitea via Helm no namespace `gitops`.
    - Script deve aguardar o Gitea ficar online e, via API (curl), criar o primeiro usuário (`marcelo`), gerar um Token (PAT) e criar dois repos de fundação: `cluster-ops` e `target-app-infra`.
- [x] **4.2 Instalar o Argo CD:**
    - Script instala o Argo CD no namespace `gitops`.
- [x] **4.3 Aplicar Root Applications (Argo CD):**
    - Criar e aplicar `infra-foundation-stack` e `ai-driven-apps` (`Application` resources) para que o Argo comece a ler do Gitea.

## Fase 4.5: Security Foundation (Vault)
> Protegendo as identidades antes de iniciar a IA.

- [x] **4.5.1 Instalando o Vault:**
    - Fazer deploy do HashiCorp Vault no `security` (Helm).
- [x] **4.5.2 "First-Push" Credentials:**
    - Inicializar as credenciais iniciais na API do Vault (Token do Gitea/Grafana).

## Fase 4.6: The Full Observability Stack
> Garantindo que Analyst e Auditor tenham olhos (Métricas + Logs) antes do deploy.

- [x] **4.6.1 Kube-Prometheus-Stack:**
    - Instalar Prometheus e Grafana no `monitoring`.
- [x] **4.6.2 Loki & Promtail:**
    - Instalar o framework de log no `monitoring` (JSON-ready).
- [x] **4.6.3 Thanos Integration:**
    - Adicionar Thanos Sidecar para longa persistência.

## Fase 4.7: Communication Stack (Rocket.Chat)
> O Command Center humano interagindo com o Orchestrator Agent.

- [x] **4.7.1 Banco de Dados MongoDB:**
    - Deploy da persistência de mensagens.
- [x] **4.7.2 Rocket.Chat e Canais:**
    - Deploy do server e configuração dos webhooks para `ai-ops`.

## Fase 5: Alertas e Automação via GitOps
> O monitoramento declarativo e a "fiação" para enviar os alertas para os agentes.

- [x] **5.1 Configurar o Alertmanager Declarativo:**
    - Criar `manifests/observability-gitops/alertmanager-config.yaml`.
    - Fazer push via script do passo 4.1 deste arquivo para o repositório `cluster-ops` recém criado no Gitea, para que o Argo CD aplique a configuração do Alertmanager (direcionando alertas para o webhook do Orchestrator Agent).

## Fase 6: Deploy da Equipe de Agentes
> A inteligência entra no jogo (Apenas quando Host, Kind, Banco, Gitea e LM Studio estiverem prontos).

- [x] **6.1 Criar o manifesto dos Agentes (`manifests/agent-deployments.yaml`):**
    - Incorporar o `preflight-check` como `InitContainer`.
    - Definir Orchestrator, Analyst, DevOps, Auditor e Archivist com suas respectivas variáveis (Gitea PAT, Grafana Token, Webhooks).
- [x] **6.2 Aplicar manifesto dos Agentes:**
    - Fazer o deploy da equipe no namespace `ai-ops`.
    - Acompanhar os logs do `InitContainer` para se certificar de que ele passou na prova de conectividade.
- [x] **6.3 Habilitar ServiceMonitor (Prometheus):**
    - Criar `agent-monitor.yaml` e aplicar para permitir que o Grafa colete métricas customizadas via Prometheus.

## Fase 7: Testes e Validação Fechada
> Ver se o ecossistema reage adequadamente a uma falha real.

- [x] **7.1 Injetar Pod com Falha:**
    - Fazer deploy de um Nginx com imagem errada no namespace `app-production`.
- [x] **7.3 Corrigir Formatação Rocket.Chat:**
    - Atualizar os webhooks do Rocket.Chat com um script JavaScript para transformar o JSON do Alertmanager em mensagens legíveis.
    - Validar as notificações nos canais `#ops-critical` e `#ops-remediation`.

## Fase 8: Backup e Ponto de Restauração (Snapshot)
> Garantindo a posteridade e a facilidade de recuperação total.

- [x] **8.1 Auditoria do Estado do Sistema:**
    - Mapear todas as URLs, credenciais, segredos do Vault e DB.
- [x] **8.2 Geração do Ponto de Restauração Master:**
    - Criar o artefato `SYSTEM_SNAPSHOT_RESTORE.md` com o blueprint de restauração faseado.
    - Consolidar a lógica v7.1 do Orchestrator e os novos padrões de UI Widescreen.
