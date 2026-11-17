---
layout: default
title: Kubectl
parent:  Kubernetes
nav_order: 2
---

### Aide mémoire Kubectl
[Lien](https://kubernetes.io/fr/docs/reference/kubectl/cheatsheet/
)

**SSH on a pod**
~~~
kubectl -n <namespace> exec -it <pod-name> -- /bin/bash

k exec -n <namespace> exec -it <pod-name> -- ls /tmp/
~~~

**Config**
  
  - Afficher la config: `kubectl config view --minify`
  - Changer le namespace par defaut pour kubectl: `k config set-context --current --namespace sample`
  

**Tester les Flux**

  Tester les flux vers mysql depuis un autre pod sur le meme cluster:
  ~~~
  telnet mysql-service.nom-du-namespace.svc.cluster.local 3306
  ~~~
  

**Creer un pod de test: Busybox**
  ~~~
  kubectl run -i --tty debug --image=busybox --restart=Always -n argocd -- sh
  ~~~

**Tranferer un fichier externe sur un pod avec kubectl**
~~~
kubectl cp my.txt <nom-du-pod>:/tmp/my.txt
~~~

**Port Forward**
~~~sh
k port-forward pods/nginx --address=0.0.0.0 8000:80
~~~
Le port sera ouvert sur la machine qui a lancé le forward


**Supprimer tous les pods d'un deployment**
~~~sh
kubectl delete pod -n kube-system -l app=antrea
~~~

**Kubectl Raccourcis**
~~~sh
k api-resources 

NAME                                SHORTNAMES                   

configmaps                          cm                                  
endpoints                           ep                                
....
~~~

**Tester avec curl sans modifier le /etc/hosts**
~~~sh
curl -H "Host: app.rahali.com" http://192.168.56.10
~~~

**NSlookup**
~~~
nslookup <mysql-demo-service>.<mysql-namespace>.svc.cluster.local
~~~

**Gateway API**
```
k get gtw
k get httproute   
k get gatewayclasses
```
