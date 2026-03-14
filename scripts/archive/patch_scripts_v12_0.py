import yaml
import os

file_path = '/home/marcelo/lab-infra-repo/manifests/agent-scripts.yaml'
with open(file_path, 'r') as f:
    data = yaml.safe_load(f)

common_py = """import json, os, urllib.request, base64, ssl, redis, pika, yaml, re, time
# Configurações de Snapshot v11.0 preservadas
def get_redis():
    return redis.Redis(host=os.environ.get("REDIS_HOST", "redis-state"), port=6379, decode_responses=True)

def mq_publish(ch, q, msg):
    # Correção v12: Indentação garantida pelo operador literal |
    ch.queue_declare(queue=q, durable=True)
    ch.basic_publish(exchange='', routing_key=q, body=json.dumps(msg))
"""

orchestrator_v12_py = """import json, hashlib, time, os, urllib.request, redis, pika, http.server, socketserver
from common import *

# Links Dinâmicos Snapshot v11.0
URL_RABBIT = "http://rabbitmq.127.0.0.1.nip.io/#/queues/%2F/sre_tasks"
URL_REDIS = "http://redis-commander.127.0.0.1.nip.io"

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health': self.send_response(200); self.end_headers(); self.wfile.write(b"OK")

    def do_POST(self):
        content_len = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_len))
        r = get_redis()
        for alert in data.get('alerts', []):
            l = alert.get('labels', {})
            ns, pod, an = l.get('namespace', 'app-production'), l.get('pod', 'unknown'), l.get('alertname', 'KubeAlert')
            sm = alert.get('annotations', {}).get('summary', 'CrashLoop detected')

            # 🛡️ ANTI-SPAM
            lock_key = f"lock:{ns}:{pod}:{an}"
            if r.get(lock_key): continue
            trace_id = hashlib.md5(f"{ns}{pod}{an}{time.time()}".encode()).hexdigest()[:8]
            r.set(lock_key, trace_id, ex=600)

            # 🎨 LAYOUT WIDE REAL (UNIFICADO)
            status_color = "#D32F2F" if alert['status'] == 'firing' else "#388E3C"
            rich_text = (
                f"🚨 **{an}**\\n"
                f"Pod **{pod}** | Namespace **{ns}** | Ocorrência **{sm}**\\n\\n"
                f"🆔 **Trace:** `{trace_id}` | "
                f"📬 **Fila:** [sre_tasks]({URL_RABBIT}) | "
                f"💾 **Estado:** [Redis Commander]({URL_REDIS})"
            )

            # Envio ao Rocket.Chat (Aproveitamento total da linha)
            payload = {"channel": "#ops-warroom", "alias": "Orchestrator", "attachments": [{"color": status_color, "title": "Novo Incidente Identificado", "text": rich_text, "ts": time.time()}]}
            req = urllib.request.Request(f"{os.environ['RC_URL']}/api/v1/chat.postMessage", data=json.dumps(payload).encode(), headers={"X-Auth-Token": os.environ['RC_TOKEN'], "X-User-Id": os.environ['RC_USER_ID'], "Content-Type": "application/json"})
            with urllib.request.urlopen(req) as res: msg_id = json.loads(res.read())["message"]["_id"]

            ctx = {"trace_id": trace_id, "pod": pod, "ns": ns, "alert_name": an, "thread_id": msg_id}
            r.set(f"incident:{trace_id}", json.dumps(ctx), ex=3600)
            
            # Despacho Threading
            conn = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_HOST']))
            ch = conn.channel(); mq_publish(ch, 'sre_tasks', ctx); conn.close()
        self.send_response(200); self.end_headers()

if __name__ == "__main__":
    # 🚀 MELHORIA SRE: Servidor Multi-thread para múltiplos alertas paralelos
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(("", 8080), WebhookHandler)
    print("Orchestrator v12.0 (AIOps Ready) Online"); httpd.serve_forever()
"""

# Store current scripts to keep them in the dictionary
new_scripts = {
    'common.py': common_py,
    'orchestrator_v12.py': orchestrator_v12_py
}

# Preserve other scripts if any
for k, v in data['data'].items():
    if k not in new_scripts and not k.startswith('orchestrator_v11'):
        new_scripts[k] = v

data['data'] = new_scripts

# Force representation for literal scalar style
def literal_presenter(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, literal_presenter)

with open(file_path, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

print("SUCCESS: agent-scripts.yaml patched with v12.0 merged logic.")
