#!/bin/bash
# push-gitops-foundation.sh: Semeando o repositório 'cluster-ops' via Gitea API

echo "🚀 Iniciando propagação da Infraestrutura Base para o Gitea (GitOps)..."

# Configurações do Repositório Local Temporário
TMP_DIR="/tmp/cluster-ops-seed"
GITEA_URL="http://gitea-http.gitops.svc.cluster.local:3000/marcelo/cluster-ops.git"

rm -rf $TMP_DIR
mkdir -p $TMP_DIR
cd $TMP_DIR

echo "🔗 Configurando Git local..."
git init -b main
git config user.name "Antigravity DevOps"
git config user.email "devops@antigravity.ai"

echo "📂 Copiando manifestos para o Worktree temporário..."
mkdir -p base/monitoring
cp /home/marcelo/lab-infra-repo/manifests/observability-gitops/alertmanager-config.yaml base/monitoring/

echo "➕ Realizando o Commit..."
git add .
git commit -m "feat(monitoring): Initial Alertmanager declarative configuration"

echo "🔗 Abrindo túnel e realizando Push para o Gitea Local..."
kubectl port-forward svc/gitea-http -n gitops 3000:3000 &
PF_PID=$!
sleep 3 # Aguarda o port-forward iniciar

# Sincronizar com o remote (Gitea cria README.md no auto-init)
git remote add origin http://marcelo:password123@localhost:3000/marcelo/cluster-ops.git
git pull origin main --rebase
git push -u origin main

echo "🧹 Limpando túnel..."
kill $PF_PID
rm -rf $TMP_DIR

echo "🎉 Push efetuado! O Argo CD deve sincronizar o alertmanager-config.yaml agora."
