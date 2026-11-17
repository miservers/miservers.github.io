---
layout: default
title: TroubleShooting
parent:  Kubernetes
nav_order: 19
---

### Pod ne demarre pas correctement
- Etat du pod READY 1/2 : le pod contient 2 conteneurs. Un est OK, l'autre n'est pas OK(check le health) 

- Dans ce cas augmente les resources du conteneur: CPU et Memory Limits


### The Podis invalid: spec: Forbidden: pod updates may not change fields 
In Kubernetes, once a pod is created directly, most of its specification fields are immutable and cannot be updated directly. 

1. =>  Delete and recreate the pod
2. => Use a higher-level resource(**Deployment**, **ReplicaSet**, or **StatefulSet** to manage the pod.). For exemple to add a sidecar, don't modify the pod directely by adding new container. But use **Deployment** to use a sidecar(on Rancher).

### Status Error 504
Verifier Network policy : app.kubernetes.io/name: ingress-nginx  --> POD

### "https://10.24.1.247:6443/api?timeout=32s"  dial tcp 10.24.1.247:6443: connect: connection refused

Verfier que l'api server est demarré
~~~
crictl ps -a 
~~~

Logs
~~~
crictl logs CONTAINER_ID
~~~


