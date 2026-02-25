<plan>
  <task id="04-fix-selinux-storage">
    <objective>Garantir que o Pod tenha permissão de escrita no NVMe.</objective>
    <steps>
      <step>Executar: sudo chcon -Rt svirt_sandbox_file_t /home/marcelo/lab-infra-repo/data</step>
      <step>Validar com: ls -laZ</step>
    </steps>
    <verification>Criação de um arquivo teste de dentro de um Pod temporário.</verification>
  </task>
  <task id="09-watcher-deployment">
    <objective>Subir o primeiro agente funcional (The Watcher).</objective>
    <steps>
      <step>Criar a branch 'feature/v1.2-watcher-deploy'.</step>
      <step>Implementar manifests/base/configmaps.yaml (Prompts e URLs).</step>
      <step>Implementar manifests/base/watcher-deployment.yaml.</step>
    </steps>
    <verification>Log do pod mostrando: 'Conectado ao LM Studio e Cluster Auditoria Ativa'.</verification>
  </task>
</plan>
