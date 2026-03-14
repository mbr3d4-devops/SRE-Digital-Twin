#!/bin/bash
set -e

echo "🔒 Instalando HashiCorp Vault (Modo Dev) no namespace 'security'..."

# Add HashiCorp Helm repo
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update

# Install Vault with Dev mode enabled
helm upgrade --install vault hashicorp/vault \
  --namespace security --create-namespace \
  --set "server.dev.enabled=true" \
  --set "server.dev.devRootToken=root-token-lab" \
  --set "injector.enabled=true"

echo "⏳ Aguardando Vault ficar Ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=vault -n security --timeout=120s

echo "✅ Vault implantado com sucesso!"
