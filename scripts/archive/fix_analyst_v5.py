import yaml
import re

def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

# 1. Update skills
with open('/home/marcelo/lab-infra-repo/manifests/agent-skills.yaml', 'r') as f:
    skills_data = yaml.safe_load(f)

skills_data['data']['analyst.md'] = '''# PERFIL: SRE Forensic Investigator Senior
# IDIOMA: PT-BR. PROIBIDO INGLÊS.
# TAREFA: Escreva o laudo pericial preenchendo o formulário abaixo.
# REGRAS CRÍTICAS: NÃO ESCREVA PENSAMENTOS NESTE TEXTO. SAÍDA DEVE COMEÇAR COM "🔍 **Diagnóstico Detalhado**"

# DADOS COLETADOS PARA A ANÁLISE:
- Pod: {pod}
- Loki Logs: {loki_logs}
- Métricas e Eventos: {metrics_describe}
- Histórico: {contexto_historico}
- Configuração Atual: {yaml_atual}

# FORMATO OBRIGATÓRIO (Retorne APENAS o texto abaixo preenchido, sem qualquer introdução ou comentários adicionais):

🔍 **Diagnóstico Detalhado**
Resumo do Incidente:
[Escreva o resumo do incidente aqui em português]

Evidências Técnicas:

* Logs do Loki:
```text
{loki_logs}
```

* Métricas Prometheus e Eventos:
```text
{metrics_describe}
```

Análise de Causa Raiz: [Escreva a análise da causa raiz baseada nas evidências tecnológicas em português]

Contexto Histórico:
{contexto_historico}

Sugestão de Correção:

* Trecho Atual (YAML):
```yaml
{yaml_atual}
```

* Trecho Sugerido (YAML):
```yaml
{yaml_sugerido}
```

Além disso, é recomendável realizar uma análise mais profunda do aplicativo para identificar e corrigir as causas subjacentes que levaram à falha.
'''

with open('/home/marcelo/lab-infra-repo/manifests/agent-skills.yaml', 'w') as f:
    yaml.safe_dump(skills_data, f, default_flow_style=False, width=1000)

# 2. Update scripts
with open('/home/marcelo/lab-infra-repo/manifests/agent-scripts.yaml', 'r') as f:
    scripts_data = yaml.safe_load(f)

common = scripts_data['data']['common.py']

clean_ai_response_new = '''def clean_ai_response(text):
    """Padrão de Março: Deleta rascunhos e foca no Diagnóstico."""
    # 1. Remove tags de pensamento <think>
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    
    # Corte de monólogos indesejados muito comuns no Qwen
    if "* Interpretation" in text:
        text = text[:text.find("* Interpretation")]
    if "* Constraint Check" in text:
        text = text[:text.find("* Constraint Check")]
    
    # 2. Localiza a PRIMEIRA ocorrência de "\U0001F50D" e deleta TUDO antes dela
    marker = "\U0001F50D"
    if marker in text:
        text = text[text.find(marker):]
    else:
        marker2 = "Diagnóstico Detalhado"
        if marker2 in text:
            text = "\U0001F50D **Diagnóstico Detalhado**\\n" + text.split(marker2, 1)[1]

    # 3. Remove metadados em inglês que a IA insiste em colocar
    garbage = ["Analyze the Request", "Input Data:", "Evaluate", "Drafting", "Internal Monologue", "Interpretation:", "Constraint Check", "Evidence Analysis:", "As an AI"]
    for g in garbage:
        text = text.replace(g, "")
        
    return text.strip()'''

common = re.sub(r'def clean_ai_response\(text\):.*?return "\\\\n"\.join\(cleaned_lines\)\.strip\(\)', clean_ai_response_new, common, flags=re.DOTALL)

scripts_data['data']['common.py'] = common

with open('/home/marcelo/lab-infra-repo/manifests/agent-scripts.yaml', 'w') as f:
    yaml.safe_dump(scripts_data, f, default_flow_style=False, width=1000)

print("Updated configmaps")
