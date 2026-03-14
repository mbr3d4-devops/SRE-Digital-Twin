---
description: Teste de Agnosticismo para validar processamento dinâmico da LLM
---
// turbo-all
Este workflow valida se os agentes estão processando dados reais através da LLM ou se estão usando templates estáticos.

1. Gere um valor único para o teste:
```bash
UNIQUE_VAL="VAL-$(date +%s)"
echo "Test ID: $UNIQUE_VAL"
```

2. Dispare um alerta sintético via pod temporário no cluster:
```bash
kubectl run tmp-curl-test --image=curlimages/curl --restart=Never -- -s -X POST http://agent-orchestrator.ai-ops.svc:8080/ -d '{"status": "firing", "alerts": [{"labels": {"alertname": "AgnosticTest", "pod": "test-pod-'"$UNIQUE_VAL"'"}, "annotations": {"summary": "Validacao de Inteligencia v13.4"}}]}'
```

3. Aguarde o processamento pela malha de agentes (20 segundos):
```bash
sleep 20
```

4. Verifique se o valor único foi processado e armazenado no Redis pelo Analista:
```bash
RESPONSE=$(kubectl exec -n ai-ops deployment/redis-state -c redis -- redis-cli KEYS "*" | xargs -I {} kubectl exec -n ai-ops deployment/redis-state -c redis -- redis-cli GET {})
if [[ "$RESPONSE" == *"$UNIQUE_VAL"* ]]; then
  echo "✅ SUCESSO: A LLM processou a variável dinâmica."
else
  echo "❌ FALHA: A LLM não processou a variável."
fi
```

5. Limpe o pod de teste:
```bash
kubectl delete pod tmp-curl-test
```
