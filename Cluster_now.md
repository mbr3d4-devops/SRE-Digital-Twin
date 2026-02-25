# SRE Digital Twin - Snapshot do Cluster e Host
## 🚀 Dump do Cluster Kubernetes
```text
NAMESPACE            NAME                                                            READY   STATUS                  RESTARTS          AGE
ai-ops               pod/agent-team-6855f67446-dlv24                                 0/5     Init:CrashLoopBackOff   12 (97s ago)      37m
ai-ops               pod/postgres-db-0                                               1/1     Running                 2 (45m ago)       4d4h
app-production       pod/cpu-stress-test-6b47d946d6-8srs7                            1/1     Running                 2 (45m ago)       3d22h
app-production       pod/nginx-poison-deployment-7bbb6bc5bb-j48qw                    1/1     Running                 2 (45m ago)       3d23h
app-production       pod/oom-stress-test-58494dd588-hhhcm                            0/1     CrashLoopBackOff        198 (3m25s ago)   3d2h
communication        pod/rocketchat-account-7884cb94d6-lfrnw                         1/1     Running                 2 (45m ago)       3d5h
communication        pod/rocketchat-authorization-77fb4cc544-6jlxz                   1/1     Running                 2 (45m ago)       3d5h
communication        pod/rocketchat-ddp-streamer-bcd56dcf6-52twj                     1/1     Running                 3 (44m ago)       3d5h
communication        pod/rocketchat-mongodb-0                                        2/2     Running                 2 (45m ago)       3d5h
communication        pod/rocketchat-nats-0                                           3/3     Running                 3 (45m ago)       3d5h
communication        pod/rocketchat-nats-1                                           3/3     Running                 3 (45m ago)       3d5h
communication        pod/rocketchat-nats-box-6765d46868-md9j8                        1/1     Running                 1 (45m ago)       3d6h
communication        pod/rocketchat-presence-bbbbcff4b-g8tlh                         1/1     Running                 2 (45m ago)       3d5h
communication        pod/rocketchat-rocketchat-768f9c44b4-fb6kl                      1/1     Running                 1 (45m ago)       3d5h
gitops               pod/argocd-application-controller-0                             1/1     Running                 2 (45m ago)       4d4h
gitops               pod/argocd-applicationset-controller-5b7845d676-4qbdd           1/1     Running                 1 (45m ago)       3d4h
gitops               pod/argocd-dex-server-75769fdf9-tfr5n                           1/1     Running                 2 (45m ago)       4d4h
gitops               pod/argocd-notifications-controller-7d4fc69775-p9vl6            1/1     Running                 2 (45m ago)       4d4h
gitops               pod/argocd-redis-58c554d54-rmpkh                                1/1     Running                 2 (45m ago)       4d4h
gitops               pod/argocd-repo-server-6db86f5c9d-5hlc9                         1/1     Running                 0                 37m
gitops               pod/argocd-server-647fbc7fdb-qlfsm                              1/1     Running                 1 (45m ago)       3d4h
gitops               pod/gitea-d9b88486f-s4vw4                                       1/1     Running                 2 (45m ago)       4d4h
gitops               pod/gitea-postgresql-0                                          1/1     Running                 2 (45m ago)       4d4h
gitops               pod/gitea-valkey-cluster-0                                      1/1     Running                 6 (45m ago)       4d4h
gitops               pod/gitea-valkey-cluster-1                                      1/1     Running                 4 (45m ago)       4d4h
gitops               pod/gitea-valkey-cluster-2                                      1/1     Running                 3 (45m ago)       4d4h
ingress-nginx        pod/ingress-nginx-controller-864978f47d-fm4rb                   1/1     Running                 0                 37m
kube-system          pod/coredns-6f6b679f8f-qbvmq                                    1/1     Running                 2 (45m ago)       4d4h
kube-system          pod/coredns-6f6b679f8f-vk2nw                                    1/1     Running                 2 (45m ago)       4d4h
kube-system          pod/etcd-kind-control-plane                                     1/1     Running                 2 (45m ago)       4d4h
kube-system          pod/kindnet-sc2xb                                               1/1     Running                 2 (45m ago)       4d4h
kube-system          pod/kube-apiserver-kind-control-plane                           1/1     Running                 2 (45m ago)       4d4h
kube-system          pod/kube-controller-manager-kind-control-plane                  1/1     Running                 2 (45m ago)       4d4h
kube-system          pod/kube-proxy-s7g7x                                            1/1     Running                 2 (45m ago)       4d4h
kube-system          pod/kube-scheduler-kind-control-plane                           1/1     Running                 2 (45m ago)       4d4h
local-path-storage   pod/local-path-provisioner-57c5987fd4-mdn75                     1/1     Running                 3 (45m ago)       4d4h
monitoring           pod/alertmanager-kube-prometheus-stack-alertmanager-0           2/2     Running                 4 (45m ago)       4d1h
monitoring           pod/kube-prometheus-stack-grafana-668b9bb785-lfp48              3/3     Running                 6 (45m ago)       4d3h
monitoring           pod/kube-prometheus-stack-kube-state-metrics-7685cd7d69-9k5p9   1/1     Running                 3 (45m ago)       4d3h
monitoring           pod/kube-prometheus-stack-operator-8498bb9cfb-vqht5             1/1     Running                 3 (45m ago)       4d3h
monitoring           pod/kube-prometheus-stack-prometheus-node-exporter-v5r2s        1/1     Running                 2 (45m ago)       4d3h
monitoring           pod/loki-stack-0                                                1/1     Running                 2 (45m ago)       4d3h
monitoring           pod/loki-stack-promtail-psr79                                   1/1     Running                 2 (45m ago)       4d3h
monitoring           pod/prometheus-kube-prometheus-stack-prometheus-0               3/3     Running                 6 (45m ago)       3d22h
security             pod/vault-0                                                     1/1     Running                 2 (45m ago)       4d3h
security             pod/vault-agent-injector-678f868cb9-tppgg                       1/1     Running                 2 (45m ago)       4d3h

NAMESPACE       NAME                                                     TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                                                 AGE
ai-ops          service/agent-team                                       ClusterIP      10.96.138.83    <none>        8080/TCP                                                4d1h
ai-ops          service/lmstudio-service                                 ClusterIP      10.96.77.37     <none>        1234/TCP                                                4d4h
ai-ops          service/orchestrator                                     ClusterIP      10.96.108.153   <none>        8080/TCP                                                4d2h
ai-ops          service/postgres-db                                      ClusterIP      10.96.56.154    <none>        5432/TCP                                                4d4h
communication   service/rocketchat-account                               ClusterIP      10.96.4.110     <none>        9458/TCP                                                4d3h
communication   service/rocketchat-authorization                         ClusterIP      10.96.180.179   <none>        9458/TCP                                                4d3h
communication   service/rocketchat-ddp-streamer                          ClusterIP      10.96.79.110    <none>        3000/TCP,9458/TCP                                       4d3h
communication   service/rocketchat-mongodb-headless                      ClusterIP      None            <none>        27017/TCP                                               4d3h
communication   service/rocketchat-mongodb-metrics                       ClusterIP      10.96.175.57    <none>        9216/TCP                                                4d3h
communication   service/rocketchat-nats                                  ClusterIP      None            <none>        4222/TCP,6222/TCP,8222/TCP,7777/TCP,7422/TCP,7522/TCP   4d3h
communication   service/rocketchat-presence                              ClusterIP      10.96.163.252   <none>        9458/TCP                                                4d3h
communication   service/rocketchat-rocketchat                            ClusterIP      10.96.39.73     <none>        80/TCP,9100/TCP                                         4d3h
communication   service/rocketchat-rocketchat-monolith-ms-metrics        ClusterIP      10.96.136.77    <none>        9458/TCP                                                4d3h
default         service/kubernetes                                       ClusterIP      10.96.0.1       <none>        443/TCP                                                 4d4h
gitops          service/argocd-applicationset-controller                 ClusterIP      10.96.54.86     <none>        7000/TCP,8080/TCP                                       4d4h
gitops          service/argocd-dex-server                                ClusterIP      10.96.39.36     <none>        5556/TCP,5557/TCP,5558/TCP                              4d4h
gitops          service/argocd-metrics                                   ClusterIP      10.96.144.50    <none>        8082/TCP                                                4d4h
gitops          service/argocd-notifications-controller-metrics          ClusterIP      10.96.246.140   <none>        9001/TCP                                                4d4h
gitops          service/argocd-redis                                     ClusterIP      10.96.206.173   <none>        6379/TCP                                                4d4h
gitops          service/argocd-repo-server                               ClusterIP      10.96.77.203    <none>        8081/TCP,8084/TCP                                       4d4h
gitops          service/argocd-server                                    ClusterIP      10.96.7.157     <none>        80/TCP,443/TCP                                          4d4h
gitops          service/argocd-server-metrics                            ClusterIP      10.96.72.171    <none>        8083/TCP                                                4d4h
gitops          service/gitea-http                                       ClusterIP      None            <none>        3000/TCP                                                4d4h
gitops          service/gitea-postgresql                                 ClusterIP      10.96.56.208    <none>        5432/TCP                                                4d4h
gitops          service/gitea-postgresql-hl                              ClusterIP      None            <none>        5432/TCP                                                4d4h
gitops          service/gitea-ssh                                        ClusterIP      None            <none>        22/TCP                                                  4d4h
gitops          service/gitea-valkey-cluster                             ClusterIP      10.96.139.2     <none>        6379/TCP                                                4d4h
gitops          service/gitea-valkey-cluster-headless                    ClusterIP      None            <none>        6379/TCP,16379/TCP                                      4d4h
ingress-nginx   service/ingress-nginx-controller                         LoadBalancer   10.96.216.247   <pending>     80:30752/TCP,443:31308/TCP                              4d4h
ingress-nginx   service/ingress-nginx-controller-admission               ClusterIP      10.96.65.86     <none>        443/TCP                                                 4d4h
kube-system     service/kube-dns                                         ClusterIP      10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP                                  4d4h
kube-system     service/kube-prometheus-stack-coredns                    ClusterIP      None            <none>        9153/TCP                                                4d3h
kube-system     service/kube-prometheus-stack-kube-controller-manager    ClusterIP      None            <none>        10257/TCP                                               4d3h
kube-system     service/kube-prometheus-stack-kube-etcd                  ClusterIP      None            <none>        2381/TCP                                                4d3h
kube-system     service/kube-prometheus-stack-kube-proxy                 ClusterIP      None            <none>        10249/TCP                                               4d3h
kube-system     service/kube-prometheus-stack-kube-scheduler             ClusterIP      None            <none>        10259/TCP                                               4d3h
kube-system     service/kube-prometheus-stack-kubelet                    ClusterIP      None            <none>        10250/TCP,4194/TCP,10255/TCP                            4d3h
monitoring      service/alertmanager-operated                            ClusterIP      None            <none>        9093/TCP,9094/TCP,9094/UDP                              4d3h
monitoring      service/kube-prometheus-stack-alertmanager               ClusterIP      10.96.229.187   <none>        9093/TCP,8080/TCP                                       4d3h
monitoring      service/kube-prometheus-stack-grafana                    ClusterIP      10.96.140.178   <none>        80/TCP                                                  4d3h
monitoring      service/kube-prometheus-stack-kube-state-metrics         ClusterIP      10.96.188.179   <none>        8080/TCP                                                4d3h
monitoring      service/kube-prometheus-stack-operator                   ClusterIP      10.96.187.86    <none>        443/TCP                                                 4d3h
monitoring      service/kube-prometheus-stack-prometheus                 ClusterIP      10.96.175.85    <none>        9090/TCP,8080/TCP                                       4d3h
monitoring      service/kube-prometheus-stack-prometheus-node-exporter   ClusterIP      10.96.12.158    <none>        9100/TCP                                                4d3h
monitoring      service/loki-stack                                       ClusterIP      10.96.70.163    <none>        3100/TCP                                                4d3h
monitoring      service/loki-stack-headless                              ClusterIP      None            <none>        3100/TCP                                                4d3h
monitoring      service/loki-stack-memberlist                            ClusterIP      None            <none>        7946/TCP                                                4d3h
monitoring      service/prometheus-operated                              ClusterIP      None            <none>        9090/TCP,10901/TCP                                      4d3h
security        service/vault                                            ClusterIP      10.96.244.59    <none>        8200/TCP,8201/TCP                                       4d3h
security        service/vault-agent-injector-svc                         ClusterIP      10.96.205.83    <none>        443/TCP                                                 4d3h
security        service/vault-internal                                   ClusterIP      None            <none>        8200/TCP,8201/TCP                                       4d3h

NAMESPACE     NAME                                                            DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
kube-system   daemonset.apps/kindnet                                          1         1         1       1            1           kubernetes.io/os=linux   4d4h
kube-system   daemonset.apps/kube-proxy                                       1         1         1       1            1           kubernetes.io/os=linux   4d4h
monitoring    daemonset.apps/kube-prometheus-stack-prometheus-node-exporter   1         1         1       1            1           kubernetes.io/os=linux   4d3h
monitoring    daemonset.apps/loki-stack-promtail                              1         1         1       1            1           <none>                   4d3h

NAMESPACE            NAME                                                       READY   UP-TO-DATE   AVAILABLE   AGE
ai-ops               deployment.apps/agent-team                                 0/1     1            0           4d4h
app-production       deployment.apps/cpu-stress-test                            1/1     1            1           3d22h
app-production       deployment.apps/nginx-poison-deployment                    1/1     1            1           3d23h
app-production       deployment.apps/oom-stress-test                            0/1     1            0           3d2h
communication        deployment.apps/rocketchat-account                         1/1     1            1           4d3h
communication        deployment.apps/rocketchat-authorization                   1/1     1            1           4d3h
communication        deployment.apps/rocketchat-ddp-streamer                    1/1     1            1           4d3h
communication        deployment.apps/rocketchat-nats-box                        1/1     1            1           4d3h
communication        deployment.apps/rocketchat-presence                        1/1     1            1           4d3h
communication        deployment.apps/rocketchat-rocketchat                      1/1     1            1           4d3h
gitops               deployment.apps/argocd-applicationset-controller           1/1     1            1           4d4h
gitops               deployment.apps/argocd-dex-server                          1/1     1            1           4d4h
gitops               deployment.apps/argocd-notifications-controller            1/1     1            1           4d4h
gitops               deployment.apps/argocd-redis                               1/1     1            1           4d4h
gitops               deployment.apps/argocd-repo-server                         1/1     1            1           4d4h
gitops               deployment.apps/argocd-server                              1/1     1            1           4d4h
gitops               deployment.apps/gitea                                      1/1     1            1           4d4h
ingress-nginx        deployment.apps/ingress-nginx-controller                   1/1     1            1           4d4h
kube-system          deployment.apps/coredns                                    2/2     2            2           4d4h
local-path-storage   deployment.apps/local-path-provisioner                     1/1     1            1           4d4h
monitoring           deployment.apps/kube-prometheus-stack-grafana              1/1     1            1           4d3h
monitoring           deployment.apps/kube-prometheus-stack-kube-state-metrics   1/1     1            1           4d3h
monitoring           deployment.apps/kube-prometheus-stack-operator             1/1     1            1           4d3h
security             deployment.apps/vault-agent-injector                       1/1     1            1           4d3h

NAMESPACE            NAME                                                                  DESIRED   CURRENT   READY   AGE
ai-ops               replicaset.apps/agent-team-58946ddc96                                 0         0         0       3d3h
ai-ops               replicaset.apps/agent-team-5b8f7874d                                  0         0         0       3d3h
ai-ops               replicaset.apps/agent-team-6496444fd7                                 0         0         0       3d2h
ai-ops               replicaset.apps/agent-team-6779ffd555                                 0         0         0       3d2h
ai-ops               replicaset.apps/agent-team-6855f67446                                 1         1         0       3d1h
ai-ops               replicaset.apps/agent-team-6c8b484666                                 0         0         0       3d2h
ai-ops               replicaset.apps/agent-team-74d9b64d55                                 0         0         0       3d2h
ai-ops               replicaset.apps/agent-team-77f86d56d7                                 0         0         0       3d3h
ai-ops               replicaset.apps/agent-team-7b96579786                                 0         0         0       3d2h
ai-ops               replicaset.apps/agent-team-869997ddc9                                 0         0         0       3d3h
ai-ops               replicaset.apps/agent-team-c74bd445f                                  0         0         0       3d2h
app-production       replicaset.apps/cpu-stress-test-6b47d946d6                            1         1         1       3d22h
app-production       replicaset.apps/nginx-poison-deployment-576846bc6c                    0         0         0       3d4h
app-production       replicaset.apps/nginx-poison-deployment-6f56b8678c                    0         0         0       3d23h
app-production       replicaset.apps/nginx-poison-deployment-7bbb6bc5bb                    1         1         1       3d23h
app-production       replicaset.apps/nginx-poison-deployment-c8bcb99bf                     0         0         0       3d21h
app-production       replicaset.apps/oom-stress-test-58494dd588                            1         1         0       3d2h
communication        replicaset.apps/rocketchat-account-7884cb94d6                         1         1         1       4d3h
communication        replicaset.apps/rocketchat-authorization-77fb4cc544                   1         1         1       4d3h
communication        replicaset.apps/rocketchat-ddp-streamer-bcd56dcf6                     1         1         1       4d3h
communication        replicaset.apps/rocketchat-nats-box-6765d46868                        1         1         1       4d3h
communication        replicaset.apps/rocketchat-presence-bbbbcff4b                         1         1         1       4d3h
communication        replicaset.apps/rocketchat-rocketchat-59b98f86fb                      0         0         0       4d3h
communication        replicaset.apps/rocketchat-rocketchat-768f9c44b4                      1         1         1       3d5h
gitops               replicaset.apps/argocd-applicationset-controller-5b7845d676           1         1         1       3d4h
gitops               replicaset.apps/argocd-applicationset-controller-5dbfd5b658           0         0         0       3d4h
gitops               replicaset.apps/argocd-applicationset-controller-67dd8bddd8           0         0         0       4d4h
gitops               replicaset.apps/argocd-dex-server-75769fdf9                           1         1         1       4d4h
gitops               replicaset.apps/argocd-notifications-controller-7d4fc69775            1         1         1       4d4h
gitops               replicaset.apps/argocd-redis-58c554d54                                1         1         1       4d4h
gitops               replicaset.apps/argocd-repo-server-6db86f5c9d                         1         1         1       4d4h
gitops               replicaset.apps/argocd-server-647fbc7fdb                              1         1         1       3d4h
gitops               replicaset.apps/argocd-server-764d8968b8                              0         0         0       4d4h
gitops               replicaset.apps/gitea-d9b88486f                                       1         1         1       4d4h
ingress-nginx        replicaset.apps/ingress-nginx-controller-69cfc98579                   0         0         0       4d4h
ingress-nginx        replicaset.apps/ingress-nginx-controller-864978f47d                   1         1         1       37m
kube-system          replicaset.apps/coredns-6f6b679f8f                                    2         2         2       4d4h
local-path-storage   replicaset.apps/local-path-provisioner-57c5987fd4                     1         1         1       4d4h
monitoring           replicaset.apps/kube-prometheus-stack-grafana-668b9bb785              1         1         1       4d3h
monitoring           replicaset.apps/kube-prometheus-stack-kube-state-metrics-7685cd7d69   1         1         1       4d3h
monitoring           replicaset.apps/kube-prometheus-stack-operator-8498bb9cfb             1         1         1       4d3h
security             replicaset.apps/vault-agent-injector-678f868cb9                       1         1         1       4d3h

NAMESPACE       NAME                                                               READY   AGE
ai-ops          statefulset.apps/postgres-db                                       1/1     4d4h
communication   statefulset.apps/rocketchat-mongodb                                1/1     4d3h
communication   statefulset.apps/rocketchat-nats                                   2/2     4d3h
gitops          statefulset.apps/argocd-application-controller                     1/1     4d4h
gitops          statefulset.apps/gitea-postgresql                                  1/1     4d4h
gitops          statefulset.apps/gitea-valkey-cluster                              3/3     4d4h
monitoring      statefulset.apps/alertmanager-kube-prometheus-stack-alertmanager   1/1     4d3h
monitoring      statefulset.apps/loki-stack                                        1/1     4d3h
monitoring      statefulset.apps/prometheus-kube-prometheus-stack-prometheus       1/1     4d3h
security        statefulset.apps/vault                                             1/1     4d3h
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                        STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
pvc-123ab02b-9594-432d-8d94-76e0cc621fab   8Gi        RWO            Delete           Bound    gitops/valkey-data-gitea-valkey-cluster-1    standard       <unset>                          4d4h
pvc-22f32212-bc99-4ea6-997d-a603fa48d98f   8Gi        RWO            Delete           Bound    communication/datadir-rocketchat-mongodb-0   standard       <unset>                          3d6h
pvc-4f70bfe0-24c8-4fa0-a84a-c32e80068090   8Gi        RWO            Delete           Bound    gitops/valkey-data-gitea-valkey-cluster-2    standard       <unset>                          4d4h
pvc-5ec655d6-21de-479c-aaec-72218720bca5   8Gi        RWO            Delete           Bound    gitops/valkey-data-gitea-valkey-cluster-0    standard       <unset>                          4d4h
pvc-96cb160a-4efd-40fd-b3a9-27416a82ceb3   10Gi       RWO            Delete           Bound    gitops/data-gitea-postgresql-0               standard       <unset>                          4d4h
pvc-9c657f01-e08b-4d24-a689-ea1c45d802b5   5Gi        RWO            Delete           Bound    ai-ops/postgres-data-postgres-db-0           standard       <unset>                          4d4h
pvc-be913df3-6789-450b-aa20-add9af46fa68   10Gi       RWO            Delete           Bound    gitops/gitea-shared-storage                  standard       <unset>                          4d4h
NAMESPACE       NAME                                 STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
ai-ops          postgres-data-postgres-db-0          Bound     pvc-9c657f01-e08b-4d24-a689-ea1c45d802b5   5Gi        RWO            standard       <unset>                 4d4h
ai-ops          postgres-pvc                         Pending                                                                        standard       <unset>                 4d4h
communication   datadir-rocketchat-mongodb-0         Bound     pvc-22f32212-bc99-4ea6-997d-a603fa48d98f   8Gi        RWO            standard       <unset>                 3d6h
gitops          data-gitea-postgresql-0              Bound     pvc-96cb160a-4efd-40fd-b3a9-27416a82ceb3   10Gi       RWO            standard       <unset>                 4d4h
gitops          gitea-shared-storage                 Bound     pvc-be913df3-6789-450b-aa20-add9af46fa68   10Gi       RWO            standard       <unset>                 4d4h
gitops          valkey-data-gitea-valkey-cluster-0   Bound     pvc-5ec655d6-21de-479c-aaec-72218720bca5   8Gi        RWO            standard       <unset>                 4d4h
gitops          valkey-data-gitea-valkey-cluster-1   Bound     pvc-123ab02b-9594-432d-8d94-76e0cc621fab   8Gi        RWO            standard       <unset>                 4d4h
gitops          valkey-data-gitea-valkey-cluster-2   Bound     pvc-4f70bfe0-24c8-4fa0-a84a-c32e80068090   8Gi        RWO            standard       <unset>                 4d4h
```
## 🖥️ Configurações do Host
### Redes (Netstat)
```text
Conexões Internet Ativas (sem os servidores)
Proto Recv-Q Send-Q Endereço Local          Endereço Remoto         Estado      PID/Program name    
tcp        0      0 0.0.0.0:80              0.0.0.0:*               OUÇA       -                   
tcp        0      0 0.0.0.0:443             0.0.0.0:*               OUÇA       -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               OUÇA       -                   
tcp        0      0 0.0.0.0:2222            0.0.0.0:*               OUÇA       -                   
tcp        0      0 127.0.0.1:46697         0.0.0.0:*               OUÇA       16621/exe           
tcp        0      0 0.0.0.0:3000            0.0.0.0:*               OUÇA       -                   
tcp        0      0 127.0.0.1:45527         0.0.0.0:*               OUÇA       16915/language_serv 
tcp        0      0 127.0.0.54:53           0.0.0.0:*               OUÇA       -                   
tcp        0      0 127.0.0.1:44033         0.0.0.0:*               OUÇA       -                   
tcp        0      0 127.0.0.1:11434         0.0.0.0:*               OUÇA       -                   
tcp        0      0 127.0.0.1:44835         0.0.0.0:*               OUÇA       16915/language_serv 
tcp        0      0 0.0.0.0:5355            0.0.0.0:*               OUÇA       -                   
tcp        0      0 0.0.0.0:27500           0.0.0.0:*               OUÇA       -                   
tcp        0      0 127.0.0.1:37081         0.0.0.0:*               OUÇA       16621/exe           
tcp        0      0 127.0.0.1:35257         0.0.0.0:*               OUÇA       16915/language_serv 
tcp        0      0 127.0.0.1:631           0.0.0.0:*               OUÇA       -                   
tcp6       0      0 :::33977                :::*                    OUÇA       16398/antigravity   
tcp6       0      0 :::5355                 :::*                    OUÇA       -                   
tcp6       0      0 ::1:631                 :::*                    OUÇA       -                   
udp        0      0 0.0.0.0:60363           0.0.0.0:*                           116926/python3      
udp        0      0 0.0.0.0:47074           0.0.0.0:*                           116926/python3      
udp        0      0 127.0.0.54:53           0.0.0.0:*                           -                   
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -                   
udp        0      0 127.0.0.1:323           0.0.0.0:*                           -                   
udp        0      0 192.168.49.1:3702       0.0.0.0:*                           116926/python3      
udp        0      0 239.255.255.250:3702    0.0.0.0:*                           116926/python3      
udp        0      0 192.168.67.1:3702       0.0.0.0:*                           116926/python3      
udp        0      0 239.255.255.250:3702    0.0.0.0:*                           116926/python3      
udp        0      0 172.18.0.1:3702         0.0.0.0:*                           116926/python3      
udp        0      0 239.255.255.250:3702    0.0.0.0:*                           116926/python3      
udp        0      0 172.17.0.1:3702         0.0.0.0:*                           116926/python3      
udp        0      0 239.255.255.250:3702    0.0.0.0:*                           116926/python3      
udp        0      0 192.168.0.25:3702       0.0.0.0:*                           116926/python3      
udp        0      0 239.255.255.250:3702    0.0.0.0:*                           116926/python3      
udp        0      0 0.0.0.0:36877           0.0.0.0:*                           116926/python3      
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           -                   
udp        0      0 0.0.0.0:5355            0.0.0.0:*                           -                   
udp        0      0 0.0.0.0:38861           0.0.0.0:*                           116926/python3      
udp        0      0 0.0.0.0:59132           0.0.0.0:*                           116926/python3      
udp6       0      0 ::1:323                 :::*                                -                   
udp6       0      0 :::52717                :::*                                116926/python3      
udp6       0      0 fe80::9c3d:bfff:fe:3702 :::*                                116926/python3      
udp6       0      0 ff02::c:3702            :::*                                116926/python3      
udp6       0      0 fe80::70c7:a8ff:fe:3702 :::*                                116926/python3      
udp6       0      0 ff02::c:3702            :::*                                116926/python3      
udp6       0      0 fe80::12ff:e0ff:fe:3702 :::*                                116926/python3      
udp6       0      0 ff02::c:3702            :::*                                116926/python3      
udp6       0      0 :::53504                :::*                                116926/python3      
udp6       0      0 :::37974                :::*                                116926/python3      
udp6       0      0 :::5353                 :::*                                -                   
udp6       0      0 :::5355                 :::*                                -                   
```
### GPU (nvidia-smi)
```text
Wed Feb 25 17:59:15 2026       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.119.02             Driver Version: 580.119.02     CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 4070 ...    Off |   00000000:01:00.0  On |                  N/A |
|  0%   50C    P8              7W /  220W |     594MiB /  12282MiB |     52%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A            2199      G   /usr/libexec/Xorg                       330MiB |
|    0   N/A  N/A            5057      G   cinnamon                                 57MiB |
|    0   N/A  N/A           16433      G   ...share/antigravity/antigravity         75MiB |
|    0   N/A  N/A           17767      G   ...rack-uuid=3190708988185955192         82MiB |
+-----------------------------------------------------------------------------------------+
```
### SELinux & Permissões
```text
total 0
drwxr-xr-x. 1 marcelo marcelo unconfined_u:object_r:user_home_t:s0       64 fev 25 17:45 .
drwx------. 1 marcelo marcelo unconfined_u:object_r:user_home_dir_t:s0 1490 fev 25 17:22 ..
drwxr-xr-x. 1 marcelo marcelo unconfined_u:object_r:user_home_t:s0       80 fev 25 17:45 docs
drwxr-xr-x. 1 marcelo marcelo unconfined_u:object_r:user_home_t:s0      128 fev 25 17:46 .git
drwxr-xr-x. 1 marcelo marcelo unconfined_u:object_r:user_home_t:s0      630 fev 25 17:43 manifests
drwxr-xr-x. 1 marcelo marcelo unconfined_u:object_r:user_home_t:s0        0 fev 25 17:43 research
drwxr-xr-x. 1 marcelo marcelo unconfined_u:object_r:user_home_t:s0      266 fev 22 12:01 scripts
Data dir not found
```
## 🛠️ Configuração do Kind
```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  # Mapear as portas do Host (Fedora) para o Ingress Controller e Gitea
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
  - containerPort: 3000
    hostPort: 3000
    protocol: TCP # Porta para o Gitea UI/HTTP
  - containerPort: 2222
    hostPort: 2222
    protocol: TCP # Porta para o Gitea SSH

  # Mapear o diretório de infraestrutura do Fedora para dentro do Node do Kind
  extraMounts:
  - hostPath: /home/marcelo/lab-infra-repo
    containerPath: /home/marcelo/lab-infra-repo
```
