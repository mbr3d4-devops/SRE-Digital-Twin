#!/bin/bash
# Sabotage Test v14.6
curl -s -X POST http://agent-orchestrator.ai-ops.svc:8080/ -d '{
  "status": "firing",
  "alerts": [
    {
      "labels": {
        "alertname": "AnalystSelfDiagnosticV16",
        "pod": "agent-analyst-c667ddff6-d9wv7",
        "namespace": "ai-ops"
      },
      "annotations": {
        "summary": "Verificação de Saúde do Agente Analista v16.1"
      }
    }
  ]
}'
echo -e "\nAlerta de sabotagem disparado."
