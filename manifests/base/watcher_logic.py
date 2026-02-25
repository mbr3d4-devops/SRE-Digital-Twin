import os
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
    prompt = f"Como SRE Master, analise este evento de cluster e sugira se há risco: {event_msg}"
    response = client_ai.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


print("🔍 Watcher Ativo: Monitorando eventos no namespace ai-ops...")
w = watch.Watch()
for event in w.stream(v1.list_event_for_all_namespaces):
    if "Error" in event['object'].message or "Failed" in event['object'].message:
        print(f"⚠️ Detectado: {event['object'].message}")
        # Aqui o Watcher envia para a IA analisar
        # analysis = analyze_event(event['object'].message)
        # print(f"🧠 IA Analysis: {analysis}")
