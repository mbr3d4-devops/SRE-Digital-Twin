def section(title, content):
    if not content: return ""
    return f"\n{title}\n{content}\n"

def code_block(lang, content):
    if not content: return ""
    return f"```{lang}\n{content}\n```"

def list_to_block(lang, items):
    if not items: return ""
    if isinstance(items, str): return code_block(lang, items)
    return code_block(lang, "\n".join(items))

def metrics_block(metrics):
    if not metrics: return ""
    if isinstance(metrics, dict):
        lines = [f"{k} {v}" for k, v in metrics.items()]
    elif isinstance(metrics, list):
        lines = metrics
    else:
        return code_block("metrics", str(metrics))
    return list_to_block("metrics", lines)

def render(data):
    """Renderer Layer v0.8.3: Codeblock Evidence Style (SRE-grade)."""
    if not isinstance(data, dict): return data
    
    out = "INCIDENT FORENSIC REPORT\n"
    out += "────────────────────────\n"
    
    out += section("Incident", data.get("incidente"))
    out += section("Executive Summary", data.get("resumo_forense"))
    
    ev = data.get("evidencias", {})
    
    out += section("Metrics (Prometheus)", metrics_block(ev.get("metricas")))
    out += section("Logs (Loki)", list_to_block("log", ev.get("logs")))
    out += section("Kubernetes Events", list_to_block("event", ev.get("eventos")))
    out += section("Describe (kubectl)", code_block("describe", ev.get("describe")))
    out += section("GitOps Context", code_block("gitops", ev.get("gitops")))
    out += section("Incident History", code_block("history", ev.get("historico")))
    
    out += section("Technical Correlation", data.get("correlacao_tecnica"))
    out += section("Root Cause", data.get("causa_raiz"))
    out += section("Operational Impact", data.get("impacto"))
    
    if data.get("yaml_atual"):
        out += section("Current Controller YAML", code_block("yaml", data.get("yaml_atual")))
    
    if data.get("yaml_sugerido"):
        out += section("Proposed Change", code_block("yaml", data.get("yaml_sugerido")))
        
    out += section("Action Risk", data.get("risco_da_acao"))
    out += section("Analysis Confidence", data.get("confianca"))
    
    return out.strip()
