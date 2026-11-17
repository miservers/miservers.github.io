---
layout: default
title: Secret / Vault
parent:  Kubernetes
nav_order: 9
---

### Secret 
**Creer un secret**
~~~sh
kubectl -n demo-ns create secret generic my-db-creds  \
        --from-literal=username=admin   \
        --from-literal=password=CHANGE_ME
~~~

**Editer un secret**: Les valeurs sont  encodés en base64
~~~
kubectl -n demo-ns  edit secrets my-db-creds
~~~

- Pour Encoder un secret: ``echo -n "my_secret" | base64`` 
- Pour Decoder : ``echo -n "bXlwYXNzd2Q="| base64 -d``

**Utiliser un Secret au sein d'un pod**
~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: db-client
spec:
  containers:
  - name: app2
    image: bitnami/nginx
    env:
    - name: DB_USER
      valueFrom:
        secretKeyRef:
          name: my-db-creds
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: my-db-creds
          key: password
    securityContext:
      runAsNonRoot: true
      readOnlyRootFilesystem: false
      capabilities:
        drop:
          - ALL
      privileged: false
      allowPrivilegeEscalation: false
      seccompProfile:
        type: RuntimeDefault
~~~

### Vault Hashicorp
Application pour stocker les secrets

- Instaler sure kube via helm: https://github.com/hashicorp/vault-helm

- Url:
  https://vault.rahali.com:30330/ui

### External Secrets Operator

This is a solution for Kubernetes that will pull secrets from outside sources and populate secret objects in K8s on a schedule.

### Link external-secrets and vault
todo
https://yodamad.hashnode.dev/manage-your-secrets-in-kubernetes-with-external-secrets-hashicorp-vault

### Favoris
- [Setup  Vault in self managed](https://developer.hashicorp.com/vault/tutorials/get-started/setup)
- https://blog.cockpitio.com/kubernetes/vault-agent-kubernetes/
- https://www.nixknight.com/2022/07/deploy-ha-vault-cluster-with-integrated-storage-raft/
