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

common = data['data']['common.py']

# New clean_ai_response using NL instead of \n to avoid YAML dump issues
clean_ai_response_v9 = """def clean_ai_response(text):
    \"\"\"Remove raciocínio da IA e mantém apenas o laudo final formatado.\"\"\"

    if not text:
        return ""

    # remove blocos de pensamento
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)

    # remove seções comuns de raciocínio
    garbage_sections = [
        r"\\\\* Interpretation.*",
        r"\\\\* Constraint Check.*",
        r"\\\\* Evidence Analysis.*",
        r"\\\\* Synthesis.*",
        r"Analyze the Request.*",
        r"Internal Monologue.*"
    ]

    for g in garbage_sections:
        text = re.sub(g, "", text, flags=re.DOTALL)

    # corta tudo antes do diagnóstico
    marker = "🔍"
    if marker in text:
        text = text[text.find(marker):]

    # remove placeholders não preenchidos
    text = text.replace("{resumo}", "")
    text = text.replace("{causa_raiz}", "")

    # remove linhas vazias excessivas - usando NL (chr(10)) para evitar quebra de sintaxe
    text = re.sub(NL + '{3,}', NL + NL, text)

    return text.strip()"""

# Replace the function
# Note: we need to match the previous version which might have been broken
common = re.sub(r'def clean_ai_response\(text\):.*?return text\.strip\(\)', clean_ai_response_v9, common, flags=re.DOTALL)

# Update send_to_rocket for WIDE layout
new_attachment_block = """    attachment = {
        "color": "#4A148C" if role == "analyst" else "#D32F2F",
        "collapsed": False,
        "text": text,
        "ts": time.time()
    }"""
common = re.sub(r'    attachment = \{.*?\}', new_attachment_block, common, flags=re.DOTALL)

data['data']['common.py'] = common

with open(file_path, 'w') as f:
    yaml.safe_dump(data, f, default_flow_style=False, width=1000000, allow_unicode=True)

print("Updated agent-scripts.yaml with NL-based regex to avoid SyntaxError")
