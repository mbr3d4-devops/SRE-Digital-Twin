import os, time, json

def run_command(cmd):
    try: return os.popen(cmd).read()[:3000]
    except Exception as e: return f"Erro coleta: {e}"

def collect_k8s_assets(pod, ns):
    clean_pod = pod.split('/')[-1]
    describe = run_command(f'kubectl describe pod {clean_pod} -n {ns}')
    logs = run_command(f'kubectl logs {clean_pod} -n {ns} --tail=100')
    events = run_command(f'kubectl get events -n {ns} --sort-by=.lastTimestamp | tail -n 15')
    return describe, logs, events

def collect_live_yaml(ns, describe):
    live_yaml = "EVIDÊNCIA INSUFICIENTE (YAML)"
    owner_type = "deployment"
    if "Owner-Ref" in describe or "Controlled By" in describe:
        live_yaml = run_command(f'kubectl get {owner_type} -n {ns} -o yaml | grep -A 20 "spec:"')
    return live_yaml

def get_metrics_mock(pod):
    return [
        f"container_memory_usage_bytes{{pod='{pod}'}} 850Mi",
        f"kube_pod_container_status_restarts_total{{pod='{pod}'}} 4",
        "kube_node_status_condition{condition='Ready'} 1"
    ]
