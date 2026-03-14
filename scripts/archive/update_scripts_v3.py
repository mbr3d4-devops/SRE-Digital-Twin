import yaml
import re

def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

file_path = '/home/marcelo/lab-infra-repo/manifests/agent-scripts.yaml'

with open(file_path, 'r') as f:
    data = yaml.safe_load(f)

# Update analyst_consumer.py
analyst = data['data']['analyst_consumer.py']
analyst = re.sub(
    r'prompt = skill.format\(.*?\)',
    '''prompt = skill.format(
            pod=pod,
            loki_logs=logs[:1500],
            metrics_describe=f"{metrics}\\n\\nStatus: CrashLoopBackOff | Event: Back-off restarting failed container",
            yaml_atual=yaml_old[:1500],
            yaml_sugerido="Aguardando validação do Warden..."
        )''',
    analyst, flags=re.DOTALL
)
data['data']['analyst_consumer.py'] = analyst

# Update common.py
common = data['data']['common.py']

clean_ai_response_new = '''def clean_ai_response(text):
    """Padrão de Março: Deleta rascunhos e foca no Diagnóstico."""
    # 1. Remove tags de pensamento <think>
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # 2. Localiza a PRIMEIRA ocorrência de "🔍" e deleta TUDO antes dela
    marker = "🔍"
    if marker in text:
        text = text[text.find(marker):]
        
    # 3. Remove metadados em inglês que a IA insiste em colocar
    garbage = ["Analyze the Request", "Input Data:", "Evaluate", "Drafting", "Internal Monologue"]
    for g in garbage:
        text = text.replace(g, "")
        
    return text.strip()'''

common = re.sub(r'def clean_ai_response\(text\):.*?return "\\n"\.join\(cleaned_lines\)\.strip\(\)', clean_ai_response_new, common, flags=re.DOTALL)


send_to_rocket_new = '''def send_to_rocket(role, text, thread_id=None, channel="#ops-warroom"):
    """Postagem com Alias Real e Layout WIDE."""
    if not RC_TOKEN or not RC_USER: return None
    rid = ROOM_IDS.get(channel, ROOM_IDS.get("#ops-warroom"))
    alias_map = {
        "orchestrator": "Orchestrator",
        "analyst": "Analyst Forensic",
        "warden": "The Warden",
        "auditor": "Auditor SRE"
    }
    
    attachment = {
        "color": "#4A148C" if role == "analyst" else "#D32F2F",
        "text": text,
        "ts": time.time()
    }

    payload = {
        "rid": rid,
        "alias": alias_map.get(role, "Agente SRE"),
        "attachments": [attachment]
    }
    if thread_id: payload["tmid"] = thread_id
    
    try:
        req_data = json.dumps({"message": payload}, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(RC_URL + "/api/v1/chat.sendMessage", data=req_data, headers={"X-Auth-Token": RC_TOKEN, "X-User-Id": RC_USER, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            res_body = json.loads(r.read().decode('utf-8'))
            return res_body.get("message", {}).get("_id")
    except Exception as e:
        print(f"WARN RC: {e}", flush=True)
    return None'''

common = re.sub(r'def send_to_rocket\(role, text, thread_id=None, channel="#ops-warroom"\):.*?(?=def query_llm\()', send_to_rocket_new + '\n\n', common, flags=re.DOTALL)

data['data']['common.py'] = common

with open(file_path, 'w') as f:
    yaml.safe_dump(data, f, default_flow_style=False, width=1000)

print("Updated agent-scripts.yaml")
