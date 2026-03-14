"""
Digital Twin Orchestrator v7 - Advanced AI SRE
==============================================
- Analyst: Real Prometheus & Loki queries -> LLM Context
- Orchestrator: Postgres Recurrence checks
- Warden: Detailed Security Audit Trails
- Archivist: LLM-generated Post-Mortems committed to Gitea
"""
import http.server
import socketserver
import json
import urllib.request
import urllib.parse
import time
import hashlib
import base64
import psycopg2
import ssl
import datetime
import logging
import re
import uuid
import sys

# Formatador JSON para o Loki
class AntigravityJSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "agent_role": getattr(record, 'role', 'unidentified'),
            "operation": getattr(record, 'operation', 'idle'),
            "trace_id": getattr(record, 'trace_id', 'no-trace'),
            "thread_id": getattr(record, 'thread_id', 'no-thread'),
            "message": record.getMessage(),
            "latency_ms": getattr(record, 'latency_ms', 0)
        }
        if hasattr(record, 'metadata'):
            log_record["metadata"] = record.metadata
        return json.dumps(log_record)

# Configuração Global
logger = logging.getLogger("Antigravity")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(AntigravityJSONFormatter())
logger.addHandler(handler)

WEBHOOK_CONFIG_PATH = "/etc/config/rocketchat_hooks.json"
RC_TOKEN = ""
RC_USER_ID = ""
RC_URL = "http://rocketchat-rocketchat.communication.svc.cluster.local:80"

def load_credentials():
    global RC_TOKEN, RC_USER_ID
    try:
        import os
        if os.path.exists(WEBHOOK_CONFIG_PATH):
            with open(WEBHOOK_CONFIG_PATH, "r") as f:
                creds = json.load(f)
                RC_TOKEN = creds.get("RC_TOKEN", "")
                RC_USER_ID = creds.get("RC_USER_ID", "")
                print(f"DEBUG: Loaded RC Credentials from {WEBHOOK_CONFIG_PATH}", flush=True)
    except Exception as e:
        print(f"DEBUG Error loading credentials: {e}", flush=True)

# Initial load
load_credentials()

LM_STUDIO = "http://172.18.0.1:1234/v1/chat/completions"
LM_MODEL = "meta-llama-3.1-8b-instruct"
GRAFANA_URL = "http://grafana.127.0.0.1.nip.io"
ORCH_URL = "http://orchestrator.127.0.0.1.nip.io"
GITEA_API = "http://gitea-http.gitops.svc.cluster.local:3000/api/v1/repos/marcelo/target-app-infra/contents/"
GITEA_CREDS = base64.b64encode(b"marcelo:password123").decode()

# Observability APIs
LOKI_URL = "http://loki-proxy.observability.svc.cluster.local:3100/loki/api/v1/query_range"
PROM_URL = "http://kube-prometheus-stack-prometheus.monitoring.svc.cluster.local:9090/api/v1/query"

K8S_URL = "https://kubernetes.default.svc"
try:
    with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as f: K8S_TOKEN = f.read().strip()
    CTX = ssl.create_default_context(cafile='/var/run/secrets/kubernetes.io/serviceaccount/ca.crt')
except:
    K8S_TOKEN, CTX = "", ssl._create_unverified_context()

COLORS = {
    "ops-critical": "#FF0000", "ops-remediation": "#FFA500", "ops-security": "#7000FF",
    "ops-history": "#4A4A4A", "ops-debug": "#FFFF00", "analyst": "#9C27B0",
    "devops": "#2196F3", "approved": "#4CAF50", "rejected": "#F44336",
}
SECURITY_ALERTS = ["VaultSealed", "VaultTokenExpiring", "SecretExposed", "RBACViolation", "CertExpiringSoon", "AuthFailure"]
pending_actions = {}


# ============================================================
# UTILS & OBSERVABILITY
# ============================================================
def send_to_rocket(agent_role, text, aliases=None, attachments=None, thread_id=None, channel_override=None):
    channels = {
        "orchestrator": "ops-warroom",
        "analyst": "ops-warroom",
        "devops": "ops-warroom",
        "warden": "ops-security",
        "archivist": "ops-history"
    }
    
    payload = {
        "text": text,
        "alias": aliases or agent_role.capitalize()
    }
    target_channel = channel_override if channel_override else f"#{channels.get(agent_role, 'ops-warroom')}"
    
    if attachments: payload["attachments"] = attachments
    if thread_id:
        payload["roomId"] = target_channel
        payload["tmid"] = thread_id
    else:
        payload["channel"] = target_channel
        
    req = urllib.request.Request(f"{RC_URL}/api/v1/chat.postMessage", data=json.dumps(payload).encode(), headers={
        "Content-Type": "application/json", "X-Auth-Token": RC_TOKEN, "X-User-Id": RC_USER_ID
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            res = json.loads(r.read().decode())
            return res.get("message", {}).get("_id")
    except Exception as e:
        print(f"Error sending to RC: {e}", flush=True)
        return None

def get_system_prompt(role, default_text):
    import os
    skill_path = f"/etc/agent/skills/{role}.md"
    if os.path.exists(skill_path):
        try:
            with open(skill_path, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {skill_path}: {e}")
    return default_text

def query_llm(sys_p, usr_p, max_tok=600):
    req = urllib.request.Request(LM_STUDIO, data=json.dumps({"model": LM_MODEL, "messages": [{"role": "system", "content": sys_p}, {"role": "user", "content": usr_p}], "temperature": 0.2, "max_tokens": max_tok}).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())["choices"][0]["message"]["content"], LM_MODEL
    except Exception as e:
        return "Erro LLM: " + str(e), "offline"

def k8s_request(method, path, body=None):
    url = K8S_URL + path
    headers = {"Authorization": "Bearer " + K8S_TOKEN, "Content-Type": "application/json", "Accept": "application/json"}
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=10) as r: return r.getcode(), json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode() if e.fp else ""
        try:
            return e.code, json.loads(err_body) if err_body else {"message": str(e)}
        except:
            return e.code, {"message": err_body or str(e)}
    except Exception as e: return 500, {"message": str(e)}

def query_loki(pod_name):
    query = f'{{pod=~".*{pod_name}.*"}}'
    q_url = f"{LOKI_URL}?query={urllib.parse.quote(query)}&limit=15"
    try:
        with urllib.request.urlopen(urllib.request.Request(q_url)) as r:
            res = json.loads(r.read().decode())
            if not res["data"]["result"]: return "Nenhum log encontrado para o pod."
            logs = []
            for stream in res["data"]["result"]:
                for val in stream["values"]: logs.append(val[1].strip())
            return "\n".join(logs[-10:])
    except Exception as e:
        return f"[Loki indisponivel ou timeout: {e}]"

def query_prometheus(pod_name):
    q = f'sum(rate(container_cpu_usage_seconds_total{{pod=~".*{pod_name}.*"}}[5m]))'
    q_url = f"{PROM_URL}?query={urllib.parse.quote(q)}"
    try:
        with urllib.request.urlopen(urllib.request.Request(q_url)) as r:
            res = json.loads(r.read().decode())
            val = res["data"]["result"][0]["value"][1] if res["data"]["result"] else "0"
    try:
        conn = get_db_connection()
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO incident_logs (action_id, alertname, namespace, pod, severity, diagnosis, fix_description, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (action_id) DO UPDATE SET status = EXCLUDED.status, resolved_at = NOW();
        """, (action_id, alertname, ns, pod, severity, diag, fix_desc, status))
        cur.close(); conn.close()
    except Exception as e:
        print(f"DEBUG DB ERROR: {e}", flush=True)

def get_recurring_incident(alertname, ns):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT created_at, fix_description, action_id FROM incident_logs WHERE alertname=%s AND namespace=%s AND status='executed' ORDER BY created_at DESC LIMIT 1;", (alertname, ns))
        row = cur.fetchone()
        cur.close(); conn.close()
        return row
    except: return None


# ============================================================
# WORKFLOW CRITICAL (Orchestrator -> Analyst -> DevOps/Warden)
# ============================================================
def workflow_critical(alert):
    trace_id = str(uuid.uuid4())
    start_orch = time.time()

    l = alert.get("labels", {})
    a = alert.get("annotations", {})
    ns, pod, alertname = l.get("namespace", "N/A"), l.get("pod", "N/A"), l.get("alertname", "Unknown")
    desc = a.get("description", "Incidente severo.")
    
    logger.info("Alerta recebido do Alertmanager", 
                extra={"role": "orchestrator", "operation": "alert_received", "trace_id": trace_id, "metadata": {"alertname": alertname, "namespace": ns}})

    is_system_event = ("Watchdog" in alertname or "InfoInhibitor" in alertname)

    # 1. Orchestrator Card
    if is_system_event:
        thread_id = send_to_rocket("orchestrator", 
            f"🤖 **SYSTEM EVENT:** {alertname}\n\n**Namespace:** `{ns}` | **Pod:** `{pod}`\n\n{desc}",
            "The Orchestrator", thread_id=None, channel_override="#ops-debug")
    else:
        thread_id = send_to_rocket("orchestrator", 
            f"🚨 **CRITICAL INCIDENT:** {alertname}\n\n**Namespace:** `{ns}` | **Pod:** `{pod}`\n\n{desc}",
            "The Orchestrator", 
            attachments=[{
                "color": COLORS["ops-critical"], "title": "Ações Rápidas",
                "actions": [{"type": "button", "text": "Ver no Grafana", "url": GRAFANA_URL}]
            }])

    # 1.5. Orchestrator Recurrence Check
    recur = get_recurring_incident(alertname, ns)
    if recur:
        prev_date, prev_fix, prev_trace = recur[0], recur[1], recur[2]
        date_formatted = prev_date.strftime("%Y-%m-%d %H:%M:%S")
        date_url = prev_date.strftime("%Y-%m-%d-%H-%M")
        
        pm_link = f"https://gitea.local/sre/post-mortems/blob/main/postmortems/{date_url}-{alertname}.md"
        loki_link = f"{GRAFANA_URL}/explore?left=%5B%22now-1h%22,%22now%22,%22Loki%22,%7B%22expr%22:%22%7Bpod%3D~%5C%22{pod.rsplit('-', 2)[0]}.*%5C%22%7D%22%7D%5D"

        recur_text = (f"⚠️ **INCIDENTE REINCIDENTE**\n"
                      f"Este problema foi visto em: `{date_formatted}`\n"
                      f"Rastro Anterior: `{prev_trace}`\n\n"
                      f"📖 [Ler Post-Mortem da Época (Gitea)]({pm_link}) | 📊 [Ver Métricas do Incidente Passado (Grafana)]({loki_link})\n\n"
                      f"**A solução aplicada na última vez foi:** {prev_fix}")

        send_to_rocket("orchestrator", recur_text, "The Orchestrator", thread_id=thread_id)

    # 2. Analyst (LogQL + Prometheus + LLM + YAML + Hist)
    app_pod_name = pod.rsplit("-", 2)[0] if "-" in pod else pod
    loki_logs = query_loki(app_pod_name)
    prom_metrics = query_prometheus(app_pod_name)
    
    deploy_name = l.get("deployment", app_pod_name)
    code, manifest = k8s_request("GET", "/apis/apps/v1/namespaces/" + ns + "/deployments/" + deploy_name)
    manifest_str = "Manifesto inacessível."
    if code == 200:
        for k in ["creationTimestamp", "generation", "resourceVersion", "uid", "managedFields", "annotations"]:
            manifest.get("metadata", {}).pop(k, None)
        manifest.pop("status", None)
        manifest_str = json.dumps(manifest, indent=2)

    logger.info(f"Metricas coletadas para {app_pod_name}", 
                extra={"role": "analyst", "operation": "telemetry_query", "trace_id": trace_id, "thread_id": thread_id})
    
    sys_p = get_system_prompt("analyst", "Você é o 'The Analyst', SRE focado em observabilidade... Seja conciso.")
    starts_at = alert.get("startsAt", "Data e Hora Desconhecidas")
    hist_text = prev_fix if recur else "Nenhum incidente histórico similar."
    
    usr_p = f"TIMESTAMP DO ALERTA: {starts_at}\nALERTA: {alertname}\nDESC: {desc}\nLOGS: {loki_logs}\nMÉTRICAS: {prom_metrics}\nMANIFESTO K8S:\n{manifest_str}\nHISTÓRICO:\n{hist_text}"
    
    start_llm = time.time()
    llm_text, model = query_llm(sys_p, usr_p, 800)
    latency_llm = (time.time() - start_llm) * 1000
    logger.info("Processamento LLM concluído", 
                extra={"role": "analyst", "operation": "llm_inference", "trace_id": trace_id, "thread_id": thread_id, "latency_ms": latency_llm, "metadata": {"model": model}})

    
    # Grafana URLs
    grafana_loki_url = f"{GRAFANA_URL}/explore?left=%5B%22now-1h%22,%22now%22,%22Loki%22,%7B%22expr%22:%22%7Bpod%3D~%5C%22{app_pod_name}.*%5C%22%7D%22%7D%5D"
    grafana_prom_url = f"{GRAFANA_URL}/explore?left=%5B%22now-1h%22,%22now%22,%22Prometheus%22,%7B%22expr%22:%22sum(rate(container_cpu_usage_seconds_total%7Bpod%3D~%5C%22{app_pod_name}.*%5C%22%7D%5B5m%5D))%22%7D%5D"

    main_text = f"🔍 **Investigação Concluída ({model})**\n\n{llm_text}"

    channel_override = "#ops-debug" if ("Watchdog" in alertname or "InfoInhibitor" in alertname) else None

    send_to_rocket("analyst", main_text, "The Analyst", 
        attachments=[{
            "color": COLORS["analyst"],
            "title": "Ações Dinâmicas",
            "text": "Explore a telemetria ao invés de ler apenas:",
            "actions": [
                {"type": "button", "text": "📈 Ver Métricas (Grafana)", "url": grafana_prom_url},
                {"type": "button", "text": "📝 Ver Logs (Loki)", "url": grafana_loki_url}
            ]
        }], thread_id=thread_id, channel_override=channel_override)

    # 3. Build & Validate via DevOps + Warden
    if not is_system_event:
        build_and_validate_fix(alert, llm_text, trace_id, thread_id)


# Correção do link para o Gitea do Marcelo
def get_gitea_url(path):
    # Removendo prefixos desnecessários se existirem
    clean_path = path.replace("namespace/", "").replace("namespaces/", "")
    # Garante que o caminho do arquivo comece sem barra para não quebrar a URL
    clean_path = clean_path.lstrip('/')
    return f"http://gitea.127.0.0.1.nip.io/marcelo/digital-twin/src/branch/main/{clean_path}"

def build_and_validate_fix(alert, diagnosis, trace_id, thread_id):
    l = alert.get("labels", {})
    ns, pod, alertname = l.get("namespace", "default"), l.get("pod", ""), l.get("alertname", "Unknown")
    deploy = l.get("deployment", pod.rsplit("-", 2)[0] if pod else "unknown")
    
    action_id = hashlib.md5((alertname + ns + pod + str(time.time())).encode()).hexdigest()[:12]
    
    print(f"DEBUG: Fetching deployment {deploy} in {ns}")
    code, manifest = k8s_request("GET", "/apis/apps/v1/namespaces/" + ns + "/deployments/" + deploy)
    print(f"DEBUG: GET deploy code {code}")
    if code != 200:
        print(f"DEBUG: Failed to fetch deploy. Aborting fix generation. Msg: {manifest}")
        return
        
    for k in ["creationTimestamp", "generation", "resourceVersion", "uid", "managedFields", "annotations"]:
        manifest["metadata"].pop(k, None)
    manifest.pop("status", None)
    
    fix_desc = "Investigacao manual necessaria ou restart solicitado."
    
    # 1. Tentar Parsear o FIX_SUGGESTION do Analyst:
    # Regex robusto para pegar FIX_SUGGESTION mesmo com negrito (**) e espaços.
    match = re.search(r"FIX_SUGGESTION\s*[:*]+\s*(.*)", diagnosis, re.IGNORECASE)
    if match:
        fix_desc = match.group(1).strip().split('\n')[0].strip()
    else:
        # Fallback Defaults
        if "ImagePull" in alertname:
            manifest["spec"]["template"]["spec"]["containers"][0]["image"] = "nginx:latest"
            fix_desc = "Correção da tag da imagem para `nginx:latest`"
        elif "CrashLoop" in alertname or "HighCPU" in alertname:
            manifest.setdefault("spec", {}).setdefault("template", {}).setdefault("metadata", {}).setdefault("annotations", {})["restartedAt"] = str(time.time())
            fix_desc = "Efetuando Rollout Restart no Deployment para restabelecer os pods"

    # WARDEN Validation
    code_orig, orig_obj = k8s_request("GET", "/apis/apps/v1/namespaces/" + ns + "/deployments/" + deploy)
    original_manifest = orig_obj if code_orig == 200 else {}
    
    # K8s DryRun First
    code2, res2 = k8s_request("PUT", "/apis/apps/v1/namespaces/" + ns + "/deployments/" + deploy + "?dryRun=All", manifest)
    warden_ok = (code2 in [200, 201])
    
    if warden_ok:
        # Governance Eval (As 3 Leis)
        warden_result = evaluate_warden_pod(deploy, ns, original_manifest, manifest, trace_id)
        if "DECISION: APPROVED" in warden_result:
            w_audit = f"✅ **DryRun K8s Aprovado**\n✅ **Governança Aprovada**\n\nNenhuma violação de `STATE.md` ou `REQUIREMENTS.md`.\n\n🛡️ Nenhuma Secret foi exposta no spec."
            send_to_rocket("warden", f"🔒 **Patch Aprovado**\n\n{w_audit}", "The Warden", attachments=[{"color": COLORS["ops-security"], "title": "Status da Auditoria", "text": "Seguro para aplicar"}])
            
            logger.info(f"DryRun Aprovado para deployment {deploy}", 
                        extra={"role": "warden", "operation": "security_dryrun", "trace_id": trace_id, "thread_id": thread_id, "metadata": {"status": "success"}})
        else:
            warden_ok = False
            reason = warden_result.split("REASON:")[1].strip() if "REASON:" in warden_result else warden_result
            w_audit = f"✅ **DryRun K8s Aprovado**\n🚨 **Governança REJEITADA**\n\n**Motivo (Warden):** {reason}\n\nO patch não será enviado ao Git."
            send_to_rocket("warden", f"🔒 **VETO DE GOVERNANÇA**\n\n{w_audit}", "The Warden", attachments=[{"color": COLORS["rejected"], "title": "Status da Auditoria", "text": "Violou as Leis do Warden"}])
            logger.warning(f"Governanca Rejeitada para deployment {deploy}", 
                           extra={"role": "warden", "operation": "security_governance", "trace_id": trace_id, "thread_id": thread_id, "metadata": {"status": "failed", "reason": reason}})
        
        file_path = f"namespaces/{ns}/{deploy}/deployment.yaml"
        gitea_link = get_gitea_url(file_path)

        send_to_rocket("devops", 
            f"🛠️ **GitOps Patch Criado**\n\n**Ação:** `{action_id}`\n\n**Arquivo Mapeado:** `{file_path}`\n\n**Solução Proposta:** {fix_desc}\n\n⏳ *Aguardando autorização humana para injetar o commit no Gitea.*", 
            "The DevOps", 
            attachments=[{"color": COLORS["ops-remediation"], "title": "Ações de Remediação", "actions": [
                {"type": "button", "text": "✅ Aprovar (Aplicar)", "url": ORCH_URL + "/approve?id=" + action_id}, 
                {"type": "button", "text": "🔍 Inspecionar Repositório (Gitea)", "url": gitea_link, "is_webview": False},
                {"type": "button", "text": "❌ Rejeitar", "url": ORCH_URL + "/reject?id=" + action_id}
            ]}], thread_id=thread_id)

    else:
        logger.warning(f"DryRun Rejeitado para deployment {deploy}", 
                       extra={"role": "warden", "operation": "security_dryrun", "trace_id": trace_id, "thread_id": thread_id, "metadata": {"status": "failed", "reason": str(res2.get('message', res2))}})
        send_to_rocket("warden", f"🚨 **VETO DE SEGURANÇA NA PROPOSTA**\n\nDryRun Bloqueado pelo Controller K8s.\n\n**Motivo Reportado:**\n`{str(res2.get('message', res2))}`", "The Warden", attachments=[{"color": COLORS["rejected"], "title": "Status da Auditoria", "text": "Inseguro ou Inválido"}])


# ============================================================
# HEALTH CHECK (Argo CD / K8s Status)
# ============================================================
def wait_for_resource_health(deploy, ns, timeout=120):
    """Polls K8s Deployment status until healthy or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        code, obj = k8s_request("GET", f"/apis/apps/v1/namespaces/{ns}/deployments/{deploy}")
        if code == 200:
            status = obj.get("status", {})
            replicas = obj.get("spec", {}).get("replicas", 1)
            available = status.get("availableReplicas", 0)
            ready = status.get("readyReplicas", 0)
            conditions = {c["type"]: c["status"] for c in status.get("conditions", [])}
            if available >= replicas and ready >= replicas and conditions.get("Available") == "True":
                return True, f"Healthy: {available}/{replicas} replicas available"
        time.sleep(10)
    return False, f"Timeout: recurso {deploy} em {ns} nao atingiu estado saudavel em {timeout}s"


# ============================================================
# ARCHIVIST (Post-Mortem Generator — Health Gatekeeper)
# ============================================================
def archivist_postmortem(action, action_id, trace_id, thread_id):
    a = action["alert"]
    l = a.get("labels", {})
    alertname, ns, desc = l.get("alertname", ""), action["ns"], action["desc"]
    deploy = action["deploy"]
    starts_at = a.get("startsAt", "")
    
    # === HEALTH GATE: Wait for resource to become healthy ===
    send_to_rocket("archivist", f"⏳ **Aguardando estabilização do recurso** `{deploy}` em `{ns}`...\nMonitorando por até 120s.", "The Archivist", thread_id=thread_id)
    
    healthy, health_msg = wait_for_resource_health(deploy, ns, timeout=120)
    
    if not healthy:
        # === REJECTION: Resource still degraded ===
        logger.warning(f"Remediation failed for {deploy}", 
                       extra={"role": "archivist", "operation": "health_gate_failed", "trace_id": trace_id, "thread_id": thread_id, "metadata": {"reason": health_msg}})
        log_to_db(action_id, alertname, ns, "", "critical", action["diag"], desc, "remediation_failed")
        send_to_rocket("archivist", 
            f"🚨 **Erro na Remediação**\n\nO DevOps reportou sucesso, mas o recurso `{deploy}` em `{ns}` **continua degradado**.\n\n**Status:** {health_msg}\n\n⚠️ Reabrindo investigação. Post-Mortem **NÃO** gerado.", 
            "The Archivist", 
            attachments=[{"color": COLORS["rejected"], "title": "Remediação Falhou", "text": "O Archivist bloqueou o encerramento do incidente."}],
            thread_id=thread_id, channel_override="#ops-warroom")
        return
    
    # === HEALTHY: Generate Post-Mortem ===
    logger.info(f"Resource {deploy} healthy. Generating Post-Mortem.", 
                extra={"role": "archivist", "operation": "health_gate_passed", "trace_id": trace_id, "thread_id": thread_id})
    
    # Calculate MTTR
    mttr_str = "N/A"
    try:
        if starts_at:
            start_time = datetime.datetime.fromisoformat(starts_at.replace("Z", "+00:00"))
            end_time = datetime.datetime.now(datetime.timezone.utc)
            mttr_delta = end_time - start_time
            mttr_minutes = mttr_delta.total_seconds() / 60
            mttr_str = f"{mttr_minutes:.1f} minutos"
    except Exception as e:
        mttr_str = f"Erro no calculo: {e}"
    
    sys_p = get_system_prompt("archivist", "Você é SRE. Crie um Post-Mortem rico. Use Markdown.")
    usr_p = (f"Incidente: {alertname} | Namespace: {ns} | Deploy: {deploy}\n"
             f"Causa Investigada: {action['diag']}\n"
             f"Acao Tomada: {desc}\n"
             f"MTTR: {mttr_str}\n"
             f"Status Final: Recurso saudavel ({health_msg})")
    
    start_llm = time.time()
    md, model = query_llm(sys_p, usr_p, 800)
    latency_pm = (time.time() - start_llm) * 1000
    logger.info("Post-Mortem gerado", 
                extra={"role": "archivist", "operation": "post_mortem_generation", "trace_id": trace_id, "thread_id": thread_id, "latency_ms": latency_pm})
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    filename = f"postmortems/{date_str}-{alertname}.md"
    url = GITEA_API + filename
    body = {"content": base64.b64encode(md.encode()).decode(), "message": f"Doc: Post-Mortem {alertname} [MTTR: {mttr_str}]", "branch": "main"}

    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST", headers={"Authorization": "Basic " + GITEA_CREDS, "Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
        gitea_web_url = f"http://gitea.127.0.0.1.nip.io/marcelo/target-app-infra/src/branch/main/{filename}"
        log_to_db(action_id, alertname, ns, "", "critical", action["diag"], desc, "resolved")
        
        send_to_rocket("archivist", 
            f"📜 **Post-Mortem Oficial Arquivado:** `{filename}`\n\n**MTTR:** {mttr_str}\n**Health:** ✅ {health_msg}", 
            "The Archivist", attachments=[{
                "color": COLORS["approved"],
                "text": f"O relatório final do incidente foi documentado e salvo via GitOps. Recurso verificado como saudável.",
                "actions": [{"type": "button", "text": "📖 Ver Post-Mortem (Gitea)", "url": gitea_web_url}]
            }], thread_id=thread_id)
        logger.info("Post-mortem salvo no Gitea", 
                    extra={"role": "archivist", "operation": "git_commit", "trace_id": trace_id, "thread_id": thread_id, "metadata": {"file": filename, "mttr": mttr_str}})
    except Exception as e:
        print("[Archivist Erro Gitea]", e)


# ============================================================
# ENDPOINTS GITOPS (Approve Action — DevOps Real Executor)
# ============================================================
def handle_approve(action_id):
    if action_id not in pending_actions: return "<h1>Invalido</h1>"
    action = pending_actions[action_id]
    if action["status"] != "pending": return "<h1>Processado</h1>"
    action["status"] = "approved"
    trace_id = action.get("trace_id", "no-trace")
    thread_id = action.get("thread_id", None)
    deploy = action["deploy"]
    ns = action["ns"]
    alertname = action["alert"].get("labels",{}).get("alertname","")
    
    # --- STEP 1: GET current file from Gitea (with SHA) ---
    filepath = f"{ns}-{deploy}.json"
    url = GITEA_API + filepath
    sha = None
    try:
        req_check = urllib.request.Request(url, headers={"Authorization": "Basic " + GITEA_CREDS})
        with urllib.request.urlopen(req_check) as r:
            resp = json.loads(r.read().decode())
            sha = resp["sha"]
            print(f"DEBUG: DevOps GET file {filepath} OK. SHA={sha[:8]}", flush=True)
    except Exception as e:
        print(f"DEBUG: DevOps GET file {filepath} failed: {e}. Will create new.", flush=True)
    
    # --- STEP 2: Commit the fixed manifest to Gitea ---
    commit_msg = f"Fix: {action['desc']} [action_id:{action_id}] [trace:{trace_id[:8]}]"
    body = {
        "content": base64.b64encode(action["manifest_str"].encode()).decode(),
        "message": commit_msg,
        "branch": "main"
    }
    if sha:
        body["sha"] = sha
    
    method = "PUT" if sha else "POST"
    req_commit = urllib.request.Request(url, data=json.dumps(body).encode(), method=method, headers={"Authorization": "Basic " + GITEA_CREDS, "Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req_commit) as r:
            commit_resp = json.loads(r.read().decode())
            commit_sha = commit_resp.get("content", {}).get("sha", "unknown")[:12]
    except Exception as e:
        logger.error(f"DevOps push FAILED: {e}", 
                     extra={"role": "devops", "operation": "git_push_failed", "trace_id": trace_id, "thread_id": thread_id})
        send_to_rocket("devops", f"🔴 **Push Falhou**\n\nErro ao enviar commit para Gitea: `{e}`", "The DevOps", 
                       attachments=[{"color": COLORS["rejected"], "title": "Erro GitOps", "text": "O commit NÃO foi realizado. Nenhuma alteração no repositório."}],
                       thread_id=thread_id)
        return f"<html><body style='background:#10141b;color:red;text-align:center;font-family:sans-serif;'><h1>ERRO GITEA {str(e)}</h1></body></html>"
    
    # --- STEP 3: Confirm push to Rocket.Chat ---
    log_to_db(action_id, alertname, ns, "", "critical", action["diag"], action["desc"], "executed")
    gitea_file_url = f"http://gitea.127.0.0.1.nip.io/marcelo/target-app-infra/src/branch/main/{filepath}"
    
    logger.info(f"DevOps push confirmed. SHA={commit_sha}", 
                extra={"role": "devops", "operation": "git_push_confirmed", "trace_id": trace_id, "thread_id": thread_id, "metadata": {"file": filepath, "commit_sha": commit_sha}})
    
    send_to_rocket("devops", 
        f"🟢 **Commit GitOps Confirmado**\n\n"
        f"**Arquivo:** `{filepath}`\n"
        f"**Commit SHA:** `{commit_sha}`\n"
        f"**Ação:** {action['desc']}\n"
        f"**Trace:** `{trace_id[:8]}`\n\n"
        f"⏳ Aguardando Argo CD sincronizar e o Archivist validar a saúde do recurso.", 
        "The DevOps", 
        attachments=[{
            "color": COLORS["approved"], 
            "title": f"Push Confirmado [{action_id}]", 
            "text": f"O patch foi comitado no Gitea. O Archivist agora validará a saúde do recurso.",
            "actions": [{"type": "button", "text": "🔍 Ver Arquivo (Gitea)", "url": gitea_file_url}]
        }], thread_id=thread_id)
    
    # --- STEP 4: Trigger Archivist Health Gatekeeper (async) ---
    import threading
    threading.Thread(target=archivist_postmortem, args=(action, action_id, trace_id, thread_id)).start()
    
    return "<html><body style='background:#10141b;color:#4CAF50;text-align:center;font-family:sans-serif;'><h1>SUCESSO</h1><h2>GitOps Commit Confirmado</h2><p>SHA: " + commit_sha + "</p><p>O Archivist esta validando a saude do recurso antes de encerrar o incidente.</p></body></html>"

def handle_reject(action_id):
    if action_id in pending_actions:
        pending_actions[action_id]["status"] = "rejected"
        log_to_db(action_id, "", "", "", "", "", "", "rejected")
        send_to_rocket("devops", "🔴 **Patch Rejeitado**", "The DevOps", attachments=[{"color": COLORS["rejected"], "title": "Operacao Abortada [" + action_id + "]", "text": "O patch GitOps foi recusado pelo humano in the loop."}])
    return "<html><body style='background:#10141b;color:#F44336;text-align:center;font-family:sans-serif;'><h1>REJEITADO</h1><p>Fluxo GitOps finalizado sem sucesso.</p></body></html>"


# ============================================================
# SERVER
# ============================================================
def route_alert(alert):
    l = alert.get("labels", {})
    a = alert.get("annotations", {})
    status, severity, alertname, ns = alert.get("status"), l.get("severity", "unknown"), l.get("alertname", "UnknownAlert"), l.get("namespace", "N/A")
    desc = a.get("description", a.get("summary", "No description"))
    base_text = f"**{alertname}** em `{ns}`\n\n_{desc}_"

    if status == "resolved":
        if severity == "critical":
            send_to_rocket("orchestrator", f"✅ **CRITICAL INCIDENT Resolved:** {alertname}", "The Orchestrator", attachments=[{"color": COLORS["approved"], "title": f"Sistema Estável em {ns}", "text": "O Alertmanager confirmou que as métricas/logs voltaram à normalidade."}])
        return
    if severity == "critical" or "Watchdog" in alertname or "InfoInhibitor" in alertname: 
        workflow_critical(alert)
    elif alertname in SECURITY_ALERTS or l.get("group") == "security": 
        send_to_rocket("warden", f"🛡️ **Politica Violada** {alertname}", "The Warden", attachments=[{"color": COLORS["ops-security"], "title": "[SECURITY] " + alertname, "text": base_text}])
    else: 
        send_to_rocket("analyst", f"⚠️ **Monitoramento** ({severity})", "The Analyst", attachments=[{"color": COLORS["ops-debug"], "title": "[WATCH] " + alertname, "text": base_text}])

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            d = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode())
            print(f"DEBUG: Received {len(d.get('alerts', []))} alerts", flush=True)
            for a in d.get("alerts", []): route_alert(a)
            self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
        except Exception as e:
            import traceback
            print("ERROR in do_POST:", str(e), flush=True)
            traceback.print_exc()
            self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())
    def do_GET(self):
        p = urllib.parse.urlparse(self.path); qs = urllib.parse.parse_qs(p.query); a_id = qs.get("id", [""])[0]
        html = "Digital Twin Advanced Agent Team v7"
        if p.path == "/approve": html = handle_approve(a_id)
        elif p.path == "/reject": html = handle_reject(a_id)
        self.send_response(200); self.send_header("Content-Type", "text/html"); self.end_headers(); self.wfile.write(html.encode())
    def log_message(self, f, *a): pass

print("Agent Team v7 Online"); socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", 9091), Handler); httpd.serve_forever()
import urllib.request
import json
import base64

def evaluate_warden_pod(deploy_name, namespace, original_manifest, proposed_manifest, trace_id):
    import subprocess
    diff_cmd = "diff -u <(echo '{}') <(echo '{}')".format(
        json.dumps(original_manifest, indent=2), json.dumps(proposed_manifest, indent=2))
    
    try:
        # A quick hack to get diff without writing to disk
        import difflib
        orig_lines = json.dumps(original_manifest, indent=2).splitlines(keepends=True)
        new_lines = json.dumps(proposed_manifest, indent=2).splitlines(keepends=True)
        diff = "".join(difflib.unified_diff(orig_lines, new_lines))
        
        if not diff:
            return "DECISION: APPROVED\nREASON: Nenhuma alteração real no arquivo."
            
        pod_cmd = "kubectl get pods -n ai-ops -l app=warden -o jsonpath='{.items[0].metadata.name}'"
        warden_pod = subprocess.check_output(pod_cmd, shell=True, text=True)
        
        # We write a tiny python script to execute inside the warden pod
        script = f'''
import sys; sys.path.append('/app')
from warden_logic import evaluate_patch
diff = """{diff}"""
res = evaluate_patch(diff, trace_id="{trace_id}")
print("---WARDEN_RESULT_START---")
print(res)
print("---WARDEN_RESULT_END---")
'''
        # We pass this script to the warden pod via stdin to avoid escaping issues
        cmd = f"kubectl exec -i -n ai-ops {warden_pod} -- python3"
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = proc.communicate(input=script)
        
        if "---WARDEN_RESULT_START---" in out:
            return out.split("---WARDEN_RESULT_START---")[1].split("---WARDEN_RESULT_END---")[0].strip()
        else:
            return f"DECISION: REJECTED\nREASON: Erro de comunicacao com Warden Pod: {err}"
    except Exception as e:
        return f"DECISION: REJECTED\nREASON: Falha interna na comunicacao ({e})"
import urllib.request
import json
import base64

def evaluate_warden_pod(deploy_name, namespace, original_manifest, proposed_manifest, trace_id):
    import urllib.request
    import json
    import difflib
    
    try:
        orig_lines = json.dumps(original_manifest, indent=2).splitlines(keepends=True)
        new_lines = json.dumps(proposed_manifest, indent=2).splitlines(keepends=True)
        diff = "".join(difflib.unified_diff(orig_lines, new_lines))
        
        if not diff:
            return "DECISION: APPROVED\nREASON: Nenhuma alteracao real no arquivo."
            
        url = "http://warden-service.ai-ops.svc.cluster.local:8080/evaluate"
        payload = json.dumps({
            "patch": diff,
            "trace_id": trace_id
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=15) as r:
            res_data = json.loads(r.read().decode())
            return res_data.get("result", "DECISION: REJECTED\nREASON: Resposta vazia do Warden")
    except Exception as e:
        return f"DECISION: REJECTED\nREASON: Falha na comunicacao com Warden Service: {e}"
import urllib.request
import json
import base64

def evaluate_warden_pod(deploy_name, namespace, original_manifest, proposed_manifest, trace_id):
    import urllib.request
    import json
    import difflib
    
    try:
        orig_lines = json.dumps(original_manifest, indent=2).splitlines(keepends=True)
        new_lines = json.dumps(proposed_manifest, indent=2).splitlines(keepends=True)
        diff = "".join(difflib.unified_diff(orig_lines, new_lines))
        
        if not diff:
            return "DECISION: APPROVED\nREASON: Nenhuma alteracao real no arquivo."
            
        url = "http://warden-service.ai-ops.svc.cluster.local:8080/evaluate"
        payload = json.dumps({
            "patch": diff,
            "trace_id": trace_id
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=15) as r:
            res_data = json.loads(r.read().decode())
            return res_data.get("result", "DECISION: REJECTED\nREASON: Resposta vazia do Warden")
    except Exception as e:
        return f"DECISION: REJECTED\nREASON: Falha na comunicacao com Warden Service: {e}"
import urllib.request
import json
import base64

def evaluate_warden_pod(deploy_name, namespace, original_manifest, proposed_manifest, trace_id):
    import urllib.request
    import json
    import difflib
    
    try:
        orig_lines = json.dumps(original_manifest, indent=2).splitlines(keepends=True)
        new_lines = json.dumps(proposed_manifest, indent=2).splitlines(keepends=True)
        diff = "".join(difflib.unified_diff(orig_lines, new_lines))
        
        if not diff:
            return "DECISION: APPROVED\nREASON: Nenhuma alteracao real no arquivo."
            
        url = "http://warden-service.ai-ops.svc.cluster.local:8080/evaluate"
        payload = json.dumps({
            "patch": diff,
            "trace_id": trace_id
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=15) as r:
            res_data = json.loads(r.read().decode())
            return res_data.get("result", "DECISION: REJECTED\nREASON: Resposta vazia do Warden")
    except Exception as e:
        return f"DECISION: REJECTED\nREASON: Falha na comunicacao com Warden Service: {e}"
