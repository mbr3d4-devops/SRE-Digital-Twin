import urllib.request, json, base64

creds = base64.b64encode(b'marcelo:password123').decode()

def push_to_gitea(filepath, content_str, message):
    url = f'http://gitea-http.gitops.svc.cluster.local:3000/api/v1/repos/marcelo/target-app-infra/contents/{filepath}'
    body = {
        'content': base64.b64encode(content_str.encode()).decode(),
        'message': message,
        'branch': 'main'
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method='POST', headers={
        'Authorization': 'Basic ' + creds,
        'Content-Type': 'application/json'
    })
    try:
        with urllib.request.urlopen(req) as r:
            print(f'SUCCESS: {filepath}')
    except Exception as e:
        print(f'ERROR: {filepath}', e)
        if hasattr(e, 'read'): print(e.read().decode())

deployment_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cpu-stress-test
  namespace: app-production
  labels:
    app: stress
spec:
  replicas: 1
  selector:
    matchLabels:
      app: stress
  template:
    metadata:
      labels:
        app: stress
    spec:
      containers:
      - name: stress
        image: busybox:latest
        command: ["/bin/sh", "-c", "while true; do yes > /dev/null; done"]
        resources:
          limits:
            cpu: "200m"
            memory: "100Mi"
          requests:
            cpu: "100m"
"""

rule_yaml = """
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: cpu-stress-alert
  namespace: app-production
  labels:
    release: kube-prometheus-stack
spec:
  groups:
  - name: stress.rules
    rules:
    - alert: HighCPUUsageTest
      expr: sum(rate(container_cpu_usage_seconds_total{pod=~"cpu-stress-test.*", container!="POD"}[1m])) > 0.1
      for: 1m
      labels:
        severity: critical
        group: custom
      annotations:
        summary: "High CPU on stress test"
        description: "CPU is higher than 0.1 cores for 1m on cpu-stress-test pod."
"""

push_to_gitea('cpu-stress-deployment.yaml', deployment_yaml, 'Add CPU stress deployment for E2E')
push_to_gitea('cpu-stress-rule.yaml', rule_yaml, 'Add High CPU PrometheusRule for E2E')
