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

# 1. Update analyst_consumer.py
analyst = data['data']['analyst_consumer.py']
analyst = analyst.replace(
    'prompt = skill.format(\n            pod=pod, ns=ns, alert_name=alert_name,\n            loki_logs=logs[:1500],\n            prometheus_metrics=metrics,\n            kubectl_describe="Status: CrashLoopBackOff | Event: Back-off restarting failed container",\n            historical_context=history,\n            current_yaml=yaml_old[:1500],\n            suggested_yaml="Aguardando validação do Warden..."\n        )',
    'prompt = skill.format(\n            pod=pod, ns=ns, alert_name=alert_name,\n            loki_logs=logs[:1500],\n            prometheus_metrics=metrics,\n            kubectl_describe="Status: CrashLoopBackOff | Event: Back-off restarting failed container",\n            contexto_historico=history,\n            yaml_atual=yaml_old[:1500],\n            yaml_sugerido="Aguardando validação do Warden..."\n        )'
)
analyst = analyst.replace(
    'final_report = clean_ai_output(raw_ai)\n\n        # Postagem Rica na Thread Original (usando o common.py send_rc_wide)\n        send_rc_wide(\n            attachment={\n                "color": "#4A148C",\n                "title": f"🔍 Relatório Forense - Trace {trace_id[:8]}",\n                "text": final_report,\n                "ts": time.time()\n            },\n            channel=ctx.get("channel", "#ops-warroom"),\n            thread_id=ctx.get("thread_id"),\n            alias="Analyst"\n        )',
    'final_report = clean_ai_response(raw_ai)\n\n        # Postagem Rica na Thread Original (usando o common.py send_to_rocket)\n        send_to_rocket("analyst", final_report, thread_id=ctx.get("thread_id"), channel=ctx.get("channel", "#ops-warroom"))'
)
data['data']['analyst_consumer.py'] = analyst

# 2. Update common.py
common = data['data']['common.py']

clean_funcs = '''def clean_ai_response(text):
    """Garante o padrão de Março: Remove 'thinking' e lixo de introdução."""
    # 1. Remove tags <think> se houver
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # 2. Localiza a PRIMEIRA ocorrência de "🔍" e deleta tudo o que vem antes
    marker = "🔍"
    if marker in text:
        text = text[text.find(marker):]

    # 3. Limpeza de metadados em inglês que a IA insiste em postar
    noise = [
        "Analyze the Request", "Input Data", "Task:", "Evaluate", 
        "Drafting", "Internal Monologue", "Forbidden", "Rules:"
    ]
    lines = text.split('\\n')
    cleaned_lines = [l for l in lines if not any(n in l for n in noise)]
    
    return "\\n".join(cleaned_lines).strip()

def clean_ai_output(text):
    return clean_ai_response(text)'''

common = re.sub(r'def clean_ai_output\(raw_text\):.*?return \'\\n\'\.join\(cleaned_lines\)\.strip\(\)', clean_funcs, common, flags=re.DOTALL)

send_to_rocket_new = '''def send_to_rocket(role, text, thread_id=None, channel="#ops-warroom"):
    """Postagem com Alias Correto e Layout Wide."""
    if not RC_TOKEN or not RC_USER: return None
    rid = ROOM_IDS.get(channel, ROOM_IDS.get("#ops-warroom"))
    
    alias_map = {
        "orchestrator": "Orchestrator",
        "analyst": "Analyst Forensic",
        "warden": "The Warden",
        "auditor": "Auditor SRE"
    }
    
    attachment = {
        "color": "#4A148C" if role == "analyst" else "#000000",
        "title": f"Relatório do Agente: {alias_map.get(role, role.capitalize())}",
        "text": text,
        "ts": time.time()
    }

    payload = {
        "rid": rid,
        "alias": alias_map.get(role, "Agente SRE"),
        "attachments": [attachment]
    }
    if thread_id:
        payload["tmid"] = thread_id

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

print("Updated agent-scripts.yaml successfully")
