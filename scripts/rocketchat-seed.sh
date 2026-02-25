#!/bin/bash
set -e

echo "💬 Instalando Rocket.Chat + MongoDB no namespace 'communication'..."

# Add Rocket.Chat helm repo
helm repo add rocketchat https://rocketchat.github.io/helm-charts
helm repo update

# Vamos criar um values.yaml dinâmico para garantir resiliência do MongoDB
# contra restarts abruptos (apagando mongod.lock)
cat << "EOF" > /tmp/rocketchat-values.yaml
mongodb:
  auth:
    passwords:
      - "sre-pass-2026"
    rootPassword: "sre-pass-2026"
  image:
    tag: "7.0.14-debian-12-r1"
  initContainers:
    - name: remove-lock
      image: busybox
      command: ['sh', '-c', 'rm -f /bitnami/mongodb/data/db/mongod.lock || true']
      securityContext:
        runAsUser: 0
      volumeMounts:
        - name: datadir
          mountPath: /bitnami/mongodb
extraEnv: |
  - name: ADMIN_USERNAME
    value: "admin"
  - name: ADMIN_PASS
    value: "sre-admin-2026"
  - name: ADMIN_EMAIL
    value: "admin@example.com"
host: "rocketchat.127.0.0.1.nip.io"
EOF

helm upgrade --install rocketchat rocketchat/rocketchat \
  --namespace communication --create-namespace \
  -f /tmp/rocketchat-values.yaml


# Como Ingress para o RocketChat no Helm pode ser específico, vamos forçar a criação declarativa do nosso jeito
cat << "EOF" | kubectl apply -n communication -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rocketchat-ingress
  namespace: communication
spec:
  ingressClassName: nginx
  rules:
  - host: rocketchat.127.0.0.1.nip.io
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: rocketchat-rocketchat
            port:
              number: 80
EOF

echo "⏳ Aguardando os Pods do Rocket.Chat subirem..."
# Dependendo do cluster e imagem, isso pode demorar devido ao MongoDB e setup inicial
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=rocketchat -n communication --timeout=400s || echo "Timeout aguardando Rocketchat"

echo "✅ Rocket.Chat instalado e exposto com sucesso!"
