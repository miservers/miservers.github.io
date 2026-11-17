---
layout: default
title: Network Policy
parent:  Kubernetes
nav_order: 12
---

### Important Notes
- **Deny by default**: une fois une network policy s'applique à un pod, tout flux non autorisé sera interdit et ce pour tous les pods du namespace.
- Le network policy est **scopé** par namespace. 
- Le network policy utilise les **labels** pour selectionner les objets(pods, namespaces).
- Sans NetworkPolicy, tout le trafic est autorisé par défaut.

### Attention à la factorisation 
on veux ouvrir sur le pod backend vers les pods:
- db1-* port 1111
- db2-* port 2222

**Mauvais:** ça ouvre vers db1/2222 et db2/1111 aussi. ce qui n'est pas voulu!
~~~
egress:
  - to:
    - podSelector:
        matchLabels:
          app: db1
    - podSelector:
        matchLabels:
          app: db2
    ports:
    - protocol: TCP
      port: 1111
    - protocol: TCP
      port: 2222
~~~

**Bon**
~~~
egress:
  - to:
    - podSelector:
        matchLabels:
          app: db1
    ports:
    - protocol: TCP
      port: 1111
  - to:
    - podSelector:
        matchLabels:
          app: db2
    ports:
    - protocol: TCP
      port: 2222
~~~

### Pod Netdiag
~~~sh
kubectl run netdiag --image=ddock789/netdiag:0.7 
k exec -it pods/netdiag -- bash
~~~

### Commands
**Show Network Policies**    
~~~
kubectl get networkpolicy -A | [-n demo-ns]
~~~

~~~
k describe networkpolicy  demo-helm-egress-mysql -n demo-ns
~~~

**Show Pod Labels**
~~~sh
k get pod nginx --show-labels
~~~

**Trouver les pods ciblés par une policy**
~~~sh
kubectl get pods -n <namespace> -l "app=backend"
~~~


**Test Acces**
~~~
kubectl exec -it demo-spring-deployment-6c474ff598-xkw25 -c nettools-sidecar -n demo-ns -- /bin/sh
~~~

**NSlookup**
~~~
nslookup <mysql-service>.<mysql-namespace>.svc.cluster.local
~~~

### Permettre au Pod de faire des requetes DNS
Mettre a jour le Egress Network Policy avec:
~~~yaml
egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - port: 53
      protocol: UDP
    - port: 53
      protocol: TCP
~~~

### Debug les Flux avec Cilium

~~~sh
kubectl -n kube-system exec -it cilium-xxxx -- bash

cilium monitor | grep 53
~~~

