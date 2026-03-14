import urllib.request
import json
import base64

GRAFANA_URL = "http://kube-prometheus-stack-grafana.monitoring.svc.cluster.local/api/dashboards/db"
CREDS = base64.b64encode(b"admin:prom-operator").decode()

dashboard = {
    "dashboard": {
        "id": None,
        "title": "AI-Ops Agent Control Plane",
        "tags": ["ai-ops", "agents", "trace"],
        "timezone": "browser",
        "panels": [
            {
                "title": "Incident Timeline (Trace IDs)",
                "type": "logs",
                "gridPos": {"h": 10, "w": 24, "x": 0, "y": 0},
                "targets": [
                    {
                        "expr": "{namespace=\"ai-ops\", container=\"orchestrator\"} | json | line_format \"{{.timestamp}} [{{.agent_role}}] {{.operation}} - {{.message}} (Trace: {{.trace_id}})\"",
                        "refId": "A"
                    }
                ],
                "options": {
                    "showLabels": False,
                    "showCommonLabels": False,
                    "showTime": True,
                    "wrapLogMessage": True,
                    "sortOrder": "Descending"
                }
            },
            {
                "title": "Agent Latency (ms)",
                "type": "timeseries",
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 10},
                "targets": [
                    {
                        "expr": "avg_over_time({namespace=\"ai-ops\", container=\"orchestrator\"} | json | unwrap latency_ms [5m]) by (agent_role, operation)",
                        "refId": "A",
                        "legendFormat": "{{agent_role}} - {{operation}}"
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "custom": {"drawStyle": "line", "lineInterpolation": "smooth"},
                        "unit": "ms"
                    }
                }
            },
            {
                "title": "Operation Success Distribution",
                "type": "bargauge",
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 10},
                "targets": [
                    {
                        "expr": "sum by (operation) (count_over_time({namespace=\"ai-ops\", container=\"orchestrator\"} | json [5m]))",
                        "refId": "A"
                    }
                ]
            }
        ],
        "schemaVersion": 36,
        "refresh": "5s"
    },
    "overwrite": True
}

req = urllib.request.Request(
    GRAFANA_URL,
    data=json.dumps(dashboard).encode(),
    headers={
        "Authorization": f"Basic {CREDS}",
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except Exception as e:
    print(f"Error: {e}")
