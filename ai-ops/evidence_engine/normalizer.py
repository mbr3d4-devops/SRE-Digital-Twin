import time, json
from .collectors import *

def package_evidence(pod, ns):
    if not pod or pod == "N/A": 
        return "Nenhuma evidência capturada (Pod N/A)."
    
    describe, logs, events = collect_k8s_assets(pod, ns)
    live_yaml = collect_live_yaml(ns, describe)
    metrics = get_metrics_mock(pod)
    
    package = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "describe": describe,
        "logs": logs,
        "events": events,
        "live_yaml": live_yaml,
        "metrics": metrics,
        "gitops_drift": "ArgoCD Status: OutOfSync (Simulado v0.9)"
    }
    return json.dumps(package, indent=2)
