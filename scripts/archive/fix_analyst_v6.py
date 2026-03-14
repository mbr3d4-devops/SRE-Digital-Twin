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

clean_ai_response_new = '''def clean_ai_response(text):
    """Padrão de Março: Extrai APENAS o laudo a partir do ícone da lupa."""
    # Encontra onde o laudo realmente começa
    marker = "\U0001F50D"
    if marker in text:
        # Pega do ícone para frente, jogando fora todo o monólogo inicial
        text = text[text.find(marker):]
    else:
        marker_alt = "Diagnóstico Detalhado"
        if marker_alt in text:
            text = "\U0001F50D **Diagnóstico Detalhado**\\\\n" + text.split(marker_alt, 1)[1]
            
    # Limpa possíveis palavras do vocabulário da IA que possam ter "vazado" pro laudo final
    garbage = ["Analyze the Request", "Input Data:", "Evaluate", "Drafting", "Internal Monologue", "Interpretation:", "Constraint Check", "Evidence Analysis:", "As an AI"]
    for g in garbage:
        text = text.replace(g, "")
        
    return text.strip()'''

common = re.sub(r'def clean_ai_response\(text\):.*?return text\.strip\(\)', clean_ai_response_new, common, flags=re.DOTALL)

data['data']['common.py'] = common

with open(file_path, 'w') as f:
    yaml.safe_dump(data, f, default_flow_style=False, width=1000)

print("Updated configmaps")
