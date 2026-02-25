import os
import json
import time
from urllib.request import Request, urlopen
from openai import OpenAI

# ======= CONFIGURATION =======
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://172.18.0.1:1234/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama-3.1-8b-instruct")
STATE_FILE = os.getenv("STATE_FILE_PATH", "/repo/docs/STATE.md")
REQ_FILE = os.getenv("REQ_FILE_PATH", "/repo/docs/REQUIREMENTS.md")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://127.0.0.1:9091/warden_eval") # Local mock URL for now

client_ai = OpenAI(base_url=LM_STUDIO_URL, api_key="lm-studio")


def read_context(filepath):
    """Lê o conteúdo de um arquivo de contexto (STATE ou REQUIREMENTS)"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"⚠️ Erro ao ler {filepath}: {e}")
        return "Not available"


def evaluate_patch(patch_diff, trace_id="N/A"):
    """
    As 3 Leis do Warden (Implementação via LLM Prompting)
    """
    print(f"\n🛡️ Iniciando Avaliação de Governança (Trace: {trace_id})", flush=True)
    
    current_state = read_context(STATE_FILE)
    current_reqs = read_context(REQ_FILE)
    
    prompt = f"""
Você é o Agente Warden (Self-Healing Governance / Admission Controller).
Sua responsabilidade vital é aprovar ou rejeitar alterações no cluster com base EXCLUSIVAMENTE nas documentações de contexto.

=== CONTEXTO 1: STATE.md ===
{current_state[:1000]}

=== CONTEXTO 2: REQUIREMENTS.md ===
{current_reqs[:1000]}

=== PROPOSTA DE PATCH (Recebida do DevOps Agente) ===
TraceID do Incidente: {trace_id}
Patch:
{patch_diff}

=== AS 3 LEIS DO WARDEN ===
Lei 1 - Consistência de Estado: Se o STATE indicar um bloqueio Crítico (ex: Freeze), REJEITE.
Lei 2 - Verificação de Requisitos: Se o patch tenta reduzir limites (CPU/Memory) definidos no REQUIREMENTS abaixo do mínimo, REJEITE.
Lei 3 - Rastreabilidade: Se a proposta parece ser prejudicial ou introduzir bugs de infraestrutura claros, REJEITE.

Analise o patch proposto acima em conjunto com os contextos. 
Responda EXATAMENTE neste formato de 2 linhas:
DECISION: [APPROVED ou REJECTED]
REASON: [Explicação curta e direta de 1 frase do motivo baseado nas leis]
"""
    
    print(f"🧠 Consultando {MODEL_NAME}...", flush=True)
    try:
        start_time = time.time()
        response = client_ai.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=200
        )
        latency = time.time() - start_time
        result = response.choices[0].message.content.strip()
        print(f"⏱️ Latência LLM: {latency:.2f}s", flush=True)
        print(f"📋 Veredito Final:\n{result}\n", flush=True)
        return result
    except Exception as e:
        print(f"❌ Falha crítica na LLM: {e}", flush=True)
        return "DECISION: REJECTED\nREASON: LLM Endpoint Offline (Fail-Safe Ativado)."


import http.server
import socketserver

class WardenHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/evaluate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                diff = data.get('patch', '')
                trace_id = data.get('trace_id', 'unknown')
                
                result = evaluate_patch(diff, trace_id)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"result": result}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


def main():
    print(f"🛡️ Warden Governance Agent v1.8 Iniciado", flush=True)
    print(f"📁 Lendo contextos de: {STATE_FILE} e {REQ_FILE}", flush=True)
    
    port = 8080
    print(f"\nAguardando avaliação via HTTP na porta {port}...", flush=True)
    
    Handler = WardenHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    main()
