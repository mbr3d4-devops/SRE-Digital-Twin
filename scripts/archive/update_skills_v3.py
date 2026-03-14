import codecs
import re

src_file = '/home/marcelo/lab-infra-repo/manifests/agent-skills.yaml'
with codecs.open(src_file, 'r', 'utf-8') as f:
    text = f.read()

new_text = re.sub(r'  analyst\.md:(?:.|\n)*?(?=  warden\.md:)', '''  analyst.md: |
    # PERFIL: SRE Forensic Investigator Senior
    # IDIOMA: PT-BR. PROIBIDO INGLÊS.
    # TAREFA: Preencha o formulário técnico abaixo SEM introduções.

    🔍 **Diagnóstico Técnico: {pod}**

    ### 📝 1. Resumo do Incidente
    {{resumo}}

    ### 📊 2. Evidências Técnicas
    - **Logs do Loki**:
    ```text
    {loki_logs}
    ```
    - **Prometheus/Describe**:
    ```text
    {metrics_describe}
    ```

    ### 🛠️ 3. Análise de Causa Raiz
    {{causa_raiz}}

    ### 💾 4. Sugestão de Correção
    **YAML Atual:**
    ```yaml
    {yaml_atual}
    ```
    **YAML Sugerido:**
    ```yaml
    {yaml_sugerido}
    ```
''', text)

with codecs.open(src_file, 'w', 'utf-8') as f:
    f.write(new_text)

print("Updated agent-skills.yaml")
