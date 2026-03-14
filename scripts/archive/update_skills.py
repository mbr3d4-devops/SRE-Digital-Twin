import codecs
import re

src_file = '/home/marcelo/lab-infra-repo/manifests/agent-skills.yaml'
with codecs.open(src_file, 'r', 'utf-8') as f:
    text = f.read()

new_text = re.sub(r'  analyst\.md:(?:.|\n)*?(?=  warden\.md:)', '''  analyst.md: |
    # PERFIL: SRE Forensic Investigator Senior
    # TAREFA: Preencher o laudo abaixo com dados técnicos reais.
    # REGRAS: Responda APENAS o laudo. Idioma PT-BR. Proibido introduções.

    🔍 **Diagnóstico Técnico: {pod}**

    ### 📝 1. Resumo do Incidente
    {{resumo}}

    ### 📊 2. Evidências Técnicas
    - **Logs do Loki (Últimas 10 linhas)**:
    ```text
    {loki_logs}
    ```
    - **Métricas do Prometheus**:
    ```text
    {prometheus_metrics}
    ```
    - **Kubectl Describe (Eventos)**:
    ```text
    {kubectl_describe}
    ```

    ### 🛠️ 3. Análise de Causa Raiz
    {{causa_raiz}}

    ### 📜 4. Contexto Histórico
    {contexto_historico}

    ### 💾 5. Sugestões de Correção
    **YAML Atual:**
    ```yaml
    {yaml_atual}
    ```
    **Sugestão de Ajuste:**
    ```yaml
    {yaml_sugerido}
    ```

    ### 🚀 Recomendações SRE
    {{recomendacoes}}
''', text)

with codecs.open(src_file, 'w', 'utf-8') as f:
    f.write(new_text)

print("Updated agent-skills.yaml")
