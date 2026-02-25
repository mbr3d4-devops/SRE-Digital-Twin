#!/bin/bash
set -e

echo "📊 Instalando a Observability Stack no namespace 'monitoring'..."

# Repositórios
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# 1. Kube-Prometheus-Stack (Grafana + Prometheus + Alertmanager)
# Desabilitamos persistent volumes temporariamente para ser rápido, mas no mundo real usaríamos StorageClasses.
# A senha do grafana admin vai ser 'prom-operator' (conforme docs/Handover.md)
echo "📈 Instalando Prometheus e Grafana..."
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  --set grafana.adminPassword=prom-operator \
  --set grafana.service.type=ClusterIP \
  --set prometheus.prometheusSpec.retention=15d \
  --set prometheus.prometheusSpec.thanos.version="v0.32.5" \
  --set prometheus.prometheusSpec.thanos.image="quay.io/thanos/thanos:v0.32.5"

# 2. Loki Stack (Loki + Promtail)
# Configuramos o Promtail para coletar tudo do cluster e enviar pro Loki
echo "📝 Instalando Loki e Promtail..."
helm upgrade --install loki-stack grafana/loki-stack \
  --namespace monitoring \
  --set loki.persistence.enabled=false \
  --set promtail.enabled=true \
  --set "grafana.enabled=false" # Usamos o grafana do kube-prometheus-stack

# 3. Mapeando grafana ingress nip.io
cat << "EOF" | kubectl apply -n monitoring -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: grafana-ingress
  namespace: monitoring
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: grafana.127.0.0.1.nip.io
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: kube-prometheus-stack-grafana
            port:
              number: 80
EOF

echo "⏳ Aguardando os Pods de Monitoramento subirem (Isso pode levar alguns minutos)..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=grafana -n monitoring --timeout=300s || echo "Timeout aguardando grafana"
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=300s || echo "Timeout aguardando prometheus"

echo "✅ Observability Stack instalada!"
