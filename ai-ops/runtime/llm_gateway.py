import json, urllib.request, re, os

def clean_output(text):
    if not text: return '{"error": "EMPTY_LLM_RESPONSE"}'
    text = text.strip()
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    text = text.strip()
    
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end+1]
        try:
            json.loads(candidate)
            return candidate
        except: pass
    return '{"error": "AI_OUTPUT_CONTAMINATED"}'

def call_llm(agent_name, user_data, trace_id="global"):
    try:
        # Load Governance
        gov_path = "/etc/ai-ops/governance"
        gov = ""
        for f in os.listdir(gov_path):
            with open(os.path.join(gov_path, f), "r") as r: gov += r.read() + "\n"
        
        # Load Agent Skill
        skill_path = f"/etc/ai-ops/agents/{agent_name}/skill.md"
        with open(skill_path, "r") as f: skill = f.read()
        
        payload = {
            "model": "qwen2.5-7b-instruct",
            "messages": [
                {"role": "system", "content": f"{gov}\n{skill}\nCONTRATO: Responda APENAS JSON. Proibido introduções."},
                {"role": "user", "content": f"INPUT ({trace_id}):\n{user_data}\n\nResponda estritamente em JSON:"}
            ],
            "temperature": 0.0,
            "max_tokens": 1500
        }
        url = os.environ.get("LLM_URL", "http://172.18.0.1:1234/v1/chat/completions")
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as res:
            raw = json.loads(res.read())["choices"][0]["message"]["content"]
            return clean_output(raw)
    except Exception as e: return f"⚠️ Erro de IA ({agent_name}): {e}"
