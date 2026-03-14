import json, os, urllib.request, re, time, redis, pika, base64, sys

def clean_output(text):
    \"\"\"Padrao Março: Deleta pensamentos e corta instruções repetidas.\"\"\"
    # 1. Remove tags <think>
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # 2. INVERSE DECAPITATION: Busca a ÚLTIMA ocorrência do marcador (evita repetir prompt)
    marker = "🔍 **Diagnóstico Técnico"
    if marker in text:
        text = text[text.rfind(marker):]
    
    # 3. Remove lixo residual em inglês
    noise = ["Analyze", "Input Data", "Task", "Evaluate", "Rules:", "PROIBIDO"]
    lines = [l for l in text.split('\n') if not any(n in l for n in noise)]
    return "\n".join(lines).strip()

def send_to_rocket(role, content, tmid=None):
    \"\"\"Layout WIDE e Alias Real - v12.3 Definitive.\"\"\"
    alias_map = {"orchestrator": "Orchestrator", "analyst": "Analyst Forensic"}
    
    attachment = {
        "color": "#4A148C" if role == "analyst" else "#D32F2F",
        "text": clean_output(content),
        "ts": time.time()
    }
    
    payload = {
        "alias": alias_map.get(role, "Agente SRE"),
        "attachments": [attachment]
    }
    
    # roomId Fix (Crucial for Lab Env)
    if tmid and str(tmid).strip().lower() != "unknown" and len(str(tmid)) > 10:
        payload["tmid"] = str(tmid)
        payload["roomId"] = "#ops-warroom"
    else:
        payload["channel"] = "#ops-warroom"
    
    req = urllib.request.Request(f"{os.environ['RC_URL']}/api/v1/chat.postMessage",
        data=json.dumps(payload).encode(),
        headers={
            "X-Auth-Token": os.environ['RC_TOKEN'],
            "X-User-Id": os.environ['RC_USER_ID'],
            "Content-Type": "application/json"
        })
    try:
        with urllib.request.urlopen(req) as res: 
            return json.loads(res.read())
    except Exception as e:
        print(f"[RC_FATAL_ERR] {e}", flush=True)
        return None
