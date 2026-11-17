---
layout: default
title: Workloads & Scheduling
parent:  Kubernetes
nav_order: 8.1
---
### Comprendre
- **rolling update**: permet de mettre à jour un Deployment sans interruption de service en remplaçant progressivement les anciens Pods par les nouveaux. 

- **Stratégie de mise à jour (spec.strategy)**: est de type *RollingUpdate* par défaut . Ses deux paramètres clés :

    - *maxSurge* : nb max de pods créé au dela du nb de pods désiré pendant l'update.
    - *maxUnavailable* : nombre maximal de Pods qui peuvent être indisponibles pendant l’update.

Example:
~~~yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mon-app
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
~~~

### Rolling out: déploiement progressif
**kubectl rollout** : faire un déploiement progressif, conformément à la stratégie defini (ex. RollingUpdate).

~~~sh
kubectl rollout status deployment nginx-deployment
~~~

- Liste les revisions disponibles
~~~sh
kubectl rollout history deployment nginx-deployment
~~~

- Rollback a un revision
~~~sh
kubectl rollout undo deployment  nginx-deployment --to-revision=1
~~~

- Autres commandes
~~~sh
kubectl rollout restart|paus|resume deployment nginx-deployment
~~~


### DaemonSet

- Yamls : https://kubernetes.io/docs/tasks/manage-daemon/
- Concepts: https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/

But : s’assurer qu’un Pod spécifique tourne sur chaque nœud.

Exemple d'utilisation:

    - Agents de monitoring (Prometheus Node Exporter, Datadog Agent…)
    - Collecteurs de logs (Fluentd, Logstash…)
    - Services réseau ou de stockage local

DaemonSet est different du Deployment dans le sens où le Deployment permet de créer des replicas librement sur les noeud. Mais Le DaemonSet assure qu'un Pod tourne sur chaque noeud. 

### Pod Affinity AntiAffinity
Pod Affinity : choisit les colocataires(sur le meme host) d'un pod. Par exemple tu veux que les  pods app et redis soient sur le meme noeud pour reduire la latence.

Pod Anti Affinity : eviter que deux pods soint colocataires sur le meme host, par exemple du veux que les pods soit repartit par region ou zone.

La repartition est faite via topologyKey: ex. topologyKey: "kubernetes.io/hostname" par hostname

### Node Affinity
Node affinity is a property of Pods that attracts them to a set of nodes (either as a preference or a hard requirement). Taints are the opposite -- they allow a node to repel a set of pods.

### taints
Un **taint** est une propriété appliquée à un noeud pour repousser les pods qui n'ont pas la **tolérance** adéquate de tourner sur ce noeud. Le noeud est ainsi réservé à certains pods.  

Tolerations are applied to pods. Tolerations allow the scheduler to schedule pods with matching taints.

Structure du taint : `clé=valeur:Effet`
- Effet: NoSchedule, PreferNoSchedule, NoExecute(les pods seront éjectés du noeud)

**Ajouter un Taint**
~~~sh
kubectl taint node kworker2 dedicated=frontend:NoSchedule
~~~

**Vérifier les taints d'un noeud**
~~~sh
kubectl describe nodes kworker2 |grep -i taint
~~~

**Supprimer un taint** : ajouter `-` à la fin
~~~sh
kubectl taint node kworker2 dedicated=frontend:NoSchedule-
~~~

**Configurer un Pod avec la tolérance**
~~~yaml
spec:
  tolerations:
  - key: "dedicated"
    operator: "Equal"
    value: "frontend"
    effect: "NoSchedule"
~~~

