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

# Update analyst_consumer.py
analyst = data['data']['analyst_consumer.py']
analyst = re.sub(
    r'prompt = skill.format\(.*?\)',
    '''prompt = skill.format(
            pod=pod,
            loki_logs=logs[:1500],
            metrics_describe=f"CPU/RAM:\\n{metrics}\\n\\nStatus: CrashLoopBackOff | Event: Back-off restarting failed container",
            contexto_historico=history,
            yaml_atual=yaml_old[:1500],
            yaml_sugerido="Aguardando validação do Warden..."
        )''',
    analyst, flags=re.DOTALL
)
data['data']['analyst_consumer.py'] = analyst

with open(file_path, 'w') as f:
    yaml.safe_dump(data, f, default_flow_style=False, width=1000)

print("Updated agent-scripts.yaml template arguments to include contexto historico again.")
