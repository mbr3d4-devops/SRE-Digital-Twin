#!/bin/bash
set -e

echo "🔒 Inicializando as políticas e chaves no Vault..."

# Usar token de root definido no helm
export VAULT_TOKEN="root-token-lab"

# Aguardar API do Vault responder no pod
kubectl exec -n security vault-0 -- vault status > /dev/null || echo "Aguardando vault..."

# Habilitar Secret Engine KV (versão 2) em secret/
kubectl exec -n security vault-0 -- vault secrets enable -path=secret kv-v2 || echo "KV já habilitado"

# Habilitar o auth method Kubernetes
kubectl exec -n security vault-0 -- vault auth enable kubernetes || echo "Auth Kubernetes já habilitado"

# Configurar conectividade da API do K8s com o Vault
kubectl exec -n security vault-0 -- sh -c 'vault write auth/kubernetes/config \
    token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
    kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
    kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'

# Criar política para os Agentes (apenas leitura no KV)
kubectl exec -n security vault-0 -- sh -c 'cat << "EOF" > /tmp/agent-policy.hcl
path "secret/data/ai-ops/*" {
  capabilities = ["read", "list"]
}
path "secret/data/monitoring/*" {
  capabilities = ["read", "list"]
}
EOF
vault policy write agent-ro-policy /tmp/agent-policy.hcl'

# Configurar Role do Kubernetes para o ServiceAccount da equipe AI (default no ai-ops por enquanto, depois pode ser ajustado)
kubectl exec -n security vault-0 -- vault write auth/kubernetes/role/ai-ops-role \
    bound_service_account_names=default \
    bound_service_account_namespaces=ai-ops \
    policies=agent-ro-policy \
    ttl=24h

# Injetar os segredos iniciais (Seed "First-Push")
echo "🔑 Injetando credenciais Iniciais..."
kubectl exec -n security vault-0 -- vault kv put secret/ai-ops/gitea pat=gitea-devops-token-1234
kubectl exec -n security vault-0 -- vault kv put secret/ai-ops/grafana token=grafana-analyst-token-5678

echo "✅ Vault inicializado com sucesso e credenciais injetadas."
