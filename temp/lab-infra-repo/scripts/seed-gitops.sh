#!/bin/bash
# seed-gitops.sh: Bootstrap do ecossistema GitOps (Gitea + Argo CD)

echo "🚀 Iniciando Fase 4: Semeando o Ecossistema GitOps no Kind..."

# 1. Instalar Gitea (Internal Git)
echo "📦 Instalando Gitea via Helm..."
helm repo add gitea-charts https://dl.gitea.com/charts/
helm repo update
helm upgrade --install gitea gitea-charts/gitea --namespace gitops -f /home/marcelo/lab-infra-repo/manifests/gitea-values.yaml

# 2. Aguardando Gitea subir
echo "⏳ Aguardando Pods do Gitea ficarem prontos (isso pode demorar uns minutos)..."
kubectl wait --namespace gitops --for=condition=ready pod -l app=gitea --timeout=300s

# 3. Criar os repositórios via API do Gitea (Port Forward)
echo "🔗 Abrindo túnel para a API do Gitea e criando repositórios fundacionais..."
kubectl port-forward svc/gitea-http -n gitops 3000:3000 &
PF_PID=$!
sleep 5 # Dá tempo do port-forward estabelecer

# Função para criar repo
create_repo() {
  curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:3000/api/v1/user/repos" \
    -H "accept: application/json" \
    -H "Content-Type: application/json" \
    -u "marcelo:password123" \
    -d "{ \"name\": \"$1\", \"private\": true, \"auto_init\": true }"
}

# Criar repositórios
create_repo "cluster-ops"
create_repo "target-app-infra"

echo "✅ Repositórios 'cluster-ops' e 'target-app-infra' criados no Gitea local."

# Fechar o túnel
kill $PF_PID

# 4. Instalando Argo CD
echo "🔄 Instalando Argo CD no namespace gitops..."
kubectl apply -n gitops -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "⏳ Aguardando Argo CD Controller..."
kubectl wait --namespace gitops --for=condition=ready pod -l app.kubernetes.io/name=argocd-server --timeout=300s

# 5. Aplicar as Root Applications do Argo CD
echo "🌱 Semeando os ApplicationSets/Root Apps..."
kubectl apply -n gitops -f /home/marcelo/lab-infra-repo/manifests/argo-root-apps.yaml

echo "🎉 Fase 4 completada com sucesso! O Motor GitOps está rodando."
