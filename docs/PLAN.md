<plan>
  <task id="01-infra-audit">
    <objective>Validar a integridade física e lógica da fundação v1.0.</objective>
    <steps>
      <step>Executar snapshot do cluster (kubectl dump).</step>
      <step>Verificar permissões de escrita no volume NVMe.</step>
      <step>Analisar logs do Antigravity vs Estado Real.</step>
    </steps>
    <verification>Status 'Bound' nos PVCs e conectividade com LM Studio confirmada.</verification>
  </task>
</plan>
