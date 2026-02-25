<plan>
  <task id="04-fix-selinux-storage">
    <objective>Garantir que o Pod tenha permissão de escrita no NVMe.</objective>
    <steps>
      <step>Executar: sudo chcon -Rt svirt_sandbox_file_t /home/marcelo/lab-infra-repo/data</step>
      <step>Validar com: ls -laZ</step>
    </steps>
    <verification>Criação de um arquivo teste de dentro de um Pod temporário.</verification>
  </task>
</plan>
