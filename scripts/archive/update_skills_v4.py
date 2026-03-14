import codecs
import re

src_file = '/home/marcelo/lab-infra-repo/manifests/agent-skills.yaml'
with codecs.open(src_file, 'r', 'utf-8') as f:
    text = f.read()

new_text = re.sub(r'  analyst\.md:(?:.|\n)*?(?=  warden\.md:)', '''  analyst.md: |
    # PERFIL: SRE Forensic Investigator Senior
    # IDIOMA: PT-BR. PROIBIDO INGLÊS.
    # TAREFA: Preencha o formulário técnico abaixo SEM introduções adicionais.
    # APENAS transcreva a estrutura abaixo preenchendo as chaves {{}}.

    🔍 **Diagnóstico Detalhado**
    Resumo do Incidente:
    {{resumo}}

    Evidências Técnicas:

    * Logs do Loki:
    ```text
    {loki_logs}
    ```

    * Métricas Prometheus e Eventos:
    ```text
    {metrics_describe}
    ```

    Análise de Causa Raiz: {{causa_raiz}}

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
''', text)

with codecs.open(src_file, 'w', 'utf-8') as f:
    f.write(new_text)

print("Updated agent-skills.yaml format to match plain screenshot layout")
