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
common = common.replace('text = "🔍 **Diagnóstico Detalhado**\n" + text.split(marker2, 1)[1]', 'text = "🔍 **Diagnóstico Detalhado**\\\\n" + text.split(marker2, 1)[1]')

data['data']['common.py'] = common

with open(file_path, 'w') as f:
    yaml.safe_dump(data, f, default_flow_style=False, width=1000)

print("Fixed syntax error related to newline in common.py")
