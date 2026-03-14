import urllib.request, json, base64

creds = base64.b64encode(b'marcelo:password123').decode()

def push_to_gitea(filepath, content_str, message):
    url = f'http://gitea-http.gitops.svc.cluster.local:3000/api/v1/repos/marcelo/target-app-infra/contents/{filepath}'
    
    # Get current SHA
    sha = None
    try:
        req_get = urllib.request.Request(url, headers={'Authorization': 'Basic ' + creds})
        with urllib.request.urlopen(req_get) as r:
            file_data = json.loads(r.read().decode())
            sha = file_data['sha']
    except: pass

    body = {
        'content': base64.b64encode(content_str.encode()).decode(),
        'message': message,
        'branch': 'main'
    }
    if sha: body['sha'] = sha
    
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method='PUT' if sha else 'POST', headers={
        'Authorization': 'Basic ' + creds,
        'Content-Type': 'application/json'
    })
    try:
        with urllib.request.urlopen(req) as r:
            print(f'SUCCESS: {filepath}')
    except Exception as e:
        print(f'ERROR: {filepath}', e)
        if hasattr(e, 'read'): print(e.read().decode())

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
      expr: sum by (pod, namespace) (rate(container_cpu_usage_seconds_total{pod=~"cpu-stress-test.*", container!="POD"}[1m])) > 0.1
      for: 1m
      labels:
        severity: critical
        group: custom
      annotations:
        summary: "High CPU on stress test"
        description: "CPU is higher than 0.1 cores for 1m on cpu-stress-test pod."
"""

push_to_gitea('cpu-stress-rule.yaml', rule_yaml, 'Fix High CPU PrometheusRule syntax to preserve pod and namespace labels')
