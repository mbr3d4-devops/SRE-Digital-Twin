#!/bin/bash
# Otimização de Performance para i7-13700K + 32GB RAM e Preparação para o SRE AI-Ops Lab

echo "🚀 Iniciando preparação do Host (Fedora 42) para o Digital Twin Lab..."

# 1. Garantir que a pasta do host exista e tenha as permissões corretas
echo "📁 Configurando diretórios base em /home/marcelo/lab-infra-repo"
mkdir -p /home/marcelo/lab-infra-repo/{scripts,manifests/observability-gitops}

# 2. SELinux: Permitir que o Kind (Docker) acesse o diretório mapeado
echo "🛡️ Ajustando contexto SELinux para o diretório de infraestrutura"
sudo chcon -Rt svirt_sandbox_file_t /home/marcelo/lab-infra-repo

# 3. Firewall: Abrir caminho para o LM Studio e Ingress do Kind (Sub-rede 172.18.0.0/16)
echo "🔥 Configurando Firewalld para aceitar tráfego do cluster Kind..."
sudo firewall-cmd --permanent --zone=trusted --add-source=172.18.0.0/16
sudo firewall-cmd --reload

# 4. Inotify Limits: Essencial para ArgoCD e Gitea monitorarem pastas grandes sem CrashLoopBackOff
echo "👀 Aumentando limites do inotify para o Gitea e Argo CD..."
if ! grep -q "fs.inotify.max_user_watches" /etc/sysctl.conf; then
    echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
fi
if ! grep -q "fs.inotify.max_user_instances" /etc/sysctl.conf; then
    echo "fs.inotify.max_user_instances=512" | sudo tee -a /etc/sysctl.conf
fi

# 5. Swap: Preservar o NVMe Gen4 limitando o uso agressivo de Swap pelo Fedora
echo "⚡ Otimizando uso de Swap (vm.swappiness=10) para o NVMe"
if ! grep -q "vm.swappiness" /etc/sysctl.conf; then
    echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
else
    # Update se já existir
    sudo sed -i 's/vm.swappiness=.*/vm.swappiness=10/' /etc/sysctl.conf
fi

# Aplicar mudanças do sysctl
sudo sysctl -p

echo "✅ Tuning do Host finalizado com sucesso! Seu i7-13700K e NVMe estão prontos para o cluster."
echo "⚠️ Lembre-se de iniciar o LM Studio na porta 1234, escutando em 0.0.0.0, com GPU Offload no Max (RTX 4070)."
