---
layout: default
title: Security
parent:  Kubernetes
nav_order: 9
---

### PSS : Pods Security Standards
- PSS s'applique à un namespace

- Il y a **trois** niveaux:
    
    1. **privileged** : permissif
    2. **baseline** : moyen. Interdit les  :
        - containers privilégiés (`privileged: true`), 
        - hostPath volumes, 
        - hostNetwork
    3. **restricted**: plus strict. Les conteneurs doivent se répondre au exigences: 
        - Pas d’utilisateur root
        - runAsNonRoot: true
        - seccompProfile.type: RuntimeDefault ou Localhost
        - readOnlyRootFilesystem: true
        - Pas de capabilities supplémentaires 

- Pour l'activer le niveau **restricted** il faut ajouter ces deux labels
~~~
kubectl label namespace demo-ns pod-security.kubernetes.io/enforce=restricted --overwrite
kubectl label namespace demo-ns pod-security.kubernetes.io/enforce-version=latest --overwrite
~~~

- Pour verfier si le PSS est activé
~~~
kubectl get ns demo-ns --show-labels
~~~

- Au niveau de l'image Docker, il faut utiliser un user applicatif **non root**. Ajouter dans le `Dockefile`
~~~
RUN adduser --system --uid 1001 --home /home/diaguser --shell /bin/bash diaguser
USER 1001:1001
~~~


