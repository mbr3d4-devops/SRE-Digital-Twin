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

# Fix analyst_consumer.py syntax error created by string literal with actual newlines inside
analyst = data['data']['analyst_consumer.py']
analyst = analyst.replace('metrics_describe=f"CPU/RAM:\n{metrics}\n\nStatus: CrashLoopBackOff | Event: Back-off restarting failed container",', 'metrics_describe=f"CPU/RAM:\\\\n{metrics}\\\\n\\\\nStatus: CrashLoopBackOff | Event: Back-off restarting failed container",')

data['data']['analyst_consumer.py'] = analyst

with open(file_path, 'w') as f:
    yaml.safe_dump(data, f, default_flow_style=False, width=1000)

print("Fixed syntax error in agent-scripts.yaml")
