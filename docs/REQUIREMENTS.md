# Requisitos Arquiteturais do Laboratório AI-Ops

## 1. Limites de Recursos (Resource Quotas)
- NENHUM container no namespace `app-production` pode ter `limits.memory` inferior a `64Mi`.
- NENHUM Banco de Dados pode rodar sem PersistentVolume.

## 2. Padrões de Imagem
- É PROIBIDO o uso da tag `:latest` em namespaces de produção.
- Imagens do Docker Hub devem ser homologadas ou verificadas.
