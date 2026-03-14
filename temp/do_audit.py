import subprocess, json

def run(cmd):
    try: return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
    except Exception as e: return getattr(e, 'output', b'').decode()

pod = run("kubectl get pods -n ai-ops -l app=agent-team -o jsonpath='{.items[0].metadata.name}'").strip()

print("--- DEEP SCAN REPORT ---")

# 1. Loki Health & PVC
loki_ready = run(f"kubectl exec -n ai-ops {pod} -c analyst -- curl -s -m 5 http://loki-stack.monitoring.svc.cluster.local:3100/ready")
loki_q = run(f"kubectl exec -n ai-ops {pod} -c analyst -- curl -s -m 10 -G --data-urlencode 'query={{job=\"fluent-bit\"}}' http://loki-stack.monitoring.svc.cluster.local:3100/loki/api/v1/query")

# 2. Prometheus targets & CPU
prom_targets = run("kubectl exec -n monitoring prometheus-kube-prometheus-stack-prometheus-0 -c prometheus -- wget -qO- http://localhost:9090/api/v1/targets")
prom_down = [t['labels']['job'] for t in json.loads(prom_targets).get('data', {}).get('activeTargets', []) if t['health'] != 'up']
prom_cpu = run("kubectl exec -n monitoring prometheus-kube-prometheus-stack-prometheus-0 -c prometheus -- wget -qO- 'http://localhost:9090/api/v1/query?query=sum(rate(node_cpu_seconds_total[5m]))'")

# 3. DNS 
dns_loki = run(f"kubectl exec -n ai-ops {pod} -c analyst -- python3 -c \"import socket; print(socket.gethostbyname('loki-stack.monitoring.svc.cluster.local'))\"")

# Logs
loki_logs = run("kubectl logs -n monitoring loki-stack-0 --tail 5")
etcd_logs = run("kubectl logs -n kube-system etcd-kind-control-plane --tail 5")

# PVCs
pvcs = run("kubectl get pvc -n monitoring")

print(f"Loki Ready: {loki_ready.strip()}")
print(f"Loki Query Output: {loki_q[0:100]}...")
print(f"Prometheus Down Targets: {prom_down}")
print(f"DNS Loki Analyst: {dns_loki.strip()}")
print(f"PVCs:\n{pvcs}")

# Formatting Payload for Chat
report = ""
if "kube-etcd" in prom_down:
    report += f"**Componente**: etcd\n**Status de Conexão**: Prometheus Target Down (kube-etcd)\n**Último Log do Pod**:\n```\n{etcd_logs.strip()}\n```\n**Evidência de Disco**: N/A (Kind node)\n\n"

if 'ready' not in loki_ready or '[]' in loki_q:
    report += f"**Componente**: Loki\n**Status de Conexão**: Sucesso, mas LogQL Vazio\n**Último Log do Pod**:\n```\n{loki_logs.strip()}\n```\n**Evidência de Disco**:\n```\n{pvcs.strip()}\n```\n"

if report:
    print("\n--- REPORT TO POST ---")
    print(report)
    
    # Send to RocketChat (via Orchestrator logic or direct curl)
    rc_url = "http://rocket-chat.observability.svc.cluster.local:3000/hooks/dummy"
    # Will use a placeholder or let Antigravity do the webhook since I don't know the exact RC webhook URL here.
