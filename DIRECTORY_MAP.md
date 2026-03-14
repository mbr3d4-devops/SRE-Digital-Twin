# Projeto Digital Twin - Mapa do Diretório

Este arquivo serve como guia para a organização do projeto, descrevendo as funções de cada pasta e arquivo principal.

## Estrutura de Pastas

| Pasta | Função |
| :--- | :--- |
| `docs/` | Documentação técnica, requisitos, roadmap e status atual do cluster. |
| `logs/` | Logs de simulações do SRE Warden e arquivos de métricas extraídas. |
| `manifests/` | Configurações Kubernetes (ArgoCD, GitOps, Apps, Agents, Monitoring). |
| `postmortems/` | Relatórios de análise de causa raiz (RCA) após incidentes simulados. |
| `research/` | Pesquisas técnicas, dumps de dados e testes experimentais. |
| `scripts/` | Ferramentas de automação, scripts de setup e utilitários ativos. |
| `scripts/archive/` | Arquivo histórico de scripts de versões anteriores ou de depuração pontual. |
| `temp/` | Área temporária para rascunhos, planos de implementação e backups de trabalho. |
| `todos/` | Listas de pendências técnicas e tarefas futuras (`backlog`). |

---

## Arquivos Chave na Raiz

- `DIRECTORY_MAP.md`: Este guia de organização (mapa do projeto).
- `.agent/`: Configurações e competências do agente de IA.
- `.gitignore`: Definições de arquivos ignorados pelo controle de versão.

## Detalhes por Componente (Resumo)

### Manifestos Kubernetes (`manifests/`)
- `agent-skills.yaml`: Definições de prompts e lógica para os agentes IA.
- `argo-root-apps.yaml`: App-of-Apps para sincronização via ArgoCD.
- `kind-config.yaml`: Configuração do cluster local.

### Scripts Utilitários (`scripts/`)
- `seed-gitops.sh`: Inicializa a estrutura GitOps no cluster.
- `vault-init.sh`: Prepara o HashiCorp Vault para gerenciamento de segredos.
- `apply_final_formatting.py`: Padroniza o layout de relatórios forenses.

### Logs e Simulações (`logs/`)
- `simulation_log_vX.md`: Histórico detalhado das execuções do ciclo de governança.
- `métricas.txt`: Dados consolidados extraídos do Prometheus durante testes.

---
> [!NOTE]
> **Manutenção**: Sempre que criar uma nova subpasta importante ou um script que mude a lógica do projeto, atualize este mapa para manter a clareza para ambos (humano e IA).
