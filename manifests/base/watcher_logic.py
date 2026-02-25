import os
import sys
import time
from kubernetes import client, config, watch
from openai import OpenAI

# Configuração de Identidade e Conectividade
try:
    config.load_incluster_config()  # Usa a watcher-sa
except Exception:
    config.load_kube_config()

client_ai = OpenAI(base_url=os.getenv("LM_STUDIO_URL"), api_key="lm-studio")
v1 = client.CoreV1Api()


def analyze_event(event_msg):
    """Envia o evento para o LLM e retorna a análise."""
    prompt = f"Como SRE Master, analise este evento de cluster e sugira se há risco: {event_msg}"
    try:
        response = client_ai.chat.completions.create(
            model=os.getenv("MODEL_NAME"),
            messages=[{"role": "user", "content": prompt}],
            timeout=30
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[LLM Offline ou Timeout: {e}]"


print("🔍 Watcher Ativo: Monitorando eventos em todos os namespaces...", flush=True)
print(f"   LM Studio: {os.getenv('LM_STUDIO_URL')}", flush=True)
print(f"   Modelo: {os.getenv('MODEL_NAME')}", flush=True)

w = watch.Watch()
for event in w.stream(v1.list_event_for_all_namespaces):
    obj = event['object']
    msg = getattr(obj, 'message', '') or ''
    reason = getattr(obj, 'reason', '') or ''
    ns = obj.metadata.namespace or 'unknown'
    name = obj.metadata.name or 'unknown'

    if "Error" in msg or "Failed" in msg or "BackOff" in reason or "ErrImage" in reason:
        timestamp = time.strftime("%H:%M:%S")
        print(f"⚠️  [{timestamp}] {reason} | {ns}/{name}: {msg}", flush=True)
        
        # Envia para o LLM analisar
        print(f"🧠 Consultando LLM...", flush=True)
        analysis = analyze_event(msg)
        print(f"📋 Análise IA:\n{analysis}\n{'='*60}", flush=True)
