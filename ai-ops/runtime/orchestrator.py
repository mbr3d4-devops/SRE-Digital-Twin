import json, os, uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from .messaging import get_mq_conn, send_to_rocket
from .thread_manager import ThreadManager

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"OK")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length).decode())
        tm = ThreadManager()
        
        for alert in data.get('alerts', []):
            tid = str(uuid.uuid4())[:8]
            labels = alert.get('labels', {})
            
            # Load Skill template
            with open("/etc/ai-ops/agents/orchestrator/skill.md", "r") as f: template = f.read()
            msg = template.format(
                alertname=labels.get('alertname', 'Alerta'),
                pod=labels.get('pod', 'N/A'),
                ns=labels.get('namespace', 'N/A'),
                summary=alert.get('annotations', {}).get('summary', 'Sem sumário'),
                trace_id=tid
            )
            
            msg_id = send_to_rocket("orchestrator", msg)
            if msg_id: tm.set_thread(tid, msg_id)
            tm.save_evidence(tid, json.dumps(alert))
            
            conn = get_mq_conn(); ch = conn.channel()
            ch.queue_declare(queue='sre_tasks', durable=True)
            ch.basic_publish(exchange='', routing_key='sre_tasks', body=json.dumps({"trace_id": tid, "thread_id": msg_id}))
            conn.close()
        
        self.send_response(200); self.end_headers()

def run():
    HTTPServer(('0.0.0.0', 8080), WebhookHandler).serve_forever()

if __name__ == "__main__":
    run()
