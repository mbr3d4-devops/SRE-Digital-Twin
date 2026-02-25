# 📋 Project Requirements

## R1. Infraestrutura (v1.0)
- Persistência real em NVMe com retenção pós-restart do Kind.
- Conectividade bidirecional Pod <-> Host (172.18.0.1).

## R2. Observabilidade (v1.3)
- Correlação de Logs, Métricas e Traces (TraceID unificado).
- Monitoramento de VRAM da GPU para evitar OOM no LM Studio.

## R3. Governança de IA (v1.8)
- Protocolo "Porta Aberta": Validação física de toda ação lógica.
- Kill Switch: Feature flags para desativar habilidades dos agentes.

## Definition of Done (DoD)
- Manifesto YAML no Git + Sync via ArgoCD + Auditoria do Watcher.
