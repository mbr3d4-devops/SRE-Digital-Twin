import os, json, time, pika, urllib.request

def get_mq_conn():
    creds = pika.PlainCredentials(os.environ.get('RABBITMQ_USER', 'sre'), os.environ.get('RABBITMQ_PASS', 'sre2026'))
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=os.environ.get('RABBITMQ_HOST', 'rabbitmq'), 
        virtual_host='sre-ops', 
        credentials=creds))

def send_to_rocket(role, text, tmid=None):
    alias_map = {"orchestrator": "Orchestrator", "analyst": "Analyst Forensic", "warden": "The Warden", "auditor": "Auditor SLA"}
    colors = {"orchestrator": "#D32F2F", "analyst": "#4A148C", "warden": "#1B1E21", "auditor": "#2E7D32"}
    
    safe_text = text.encode('utf-8', 'ignore').decode('utf-8')
    if len(safe_text) > 4000: safe_text = safe_text[:4000] + "..."
    
    payload = {
        "roomId": "699b26601cf126f19882ef8d",
        "text": safe_text,
        "alias": alias_map.get(role, "Agente SRE"),
        "attachments": [{"color": colors.get(role, "#555555"), "ts": time.time()}]
    }
    if tmid: payload["tmid"] = tmid
    
    try:
        url = f"{os.environ['RC_URL']}/api/v1/chat.postMessage"
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
            headers={"X-Auth-Token": os.environ['RC_TOKEN'], "X-User-Id": os.environ['RC_USER_ID'], "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as res:
            body = json.loads(res.read())
            return body["message"]["_id"] if body.get("success") else None
    except Exception as e:
        print(f"[RC ERROR] {e}")
        return None
