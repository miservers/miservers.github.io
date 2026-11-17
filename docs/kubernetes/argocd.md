---
layout: default
title: ArgoCD
parent:  Kubernetes
nav_order: 7
---

### Install 
~~~
kubectl create ns argocd
wget https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml -O install.yaml
kubectl apply -n argocd -f install.yaml
~~~


Check if Argocd is running
~~~
kubectl get all -n argocd
~~~


### Create an Ingress For ArgoCD

argocd-ingress.yaml 
~~~
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-ingress
  namespace: argocd
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: argocd.rahali.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: argocd-server
            port:
              number: 443
~~~

Apply it:
~~~
k apply -n argocd -f argocd-ingress.yaml
~~~

**URL**: 
 - https://argocd.rahali.com:<node-port>/
 - User: admin
 - Password: CHANGE_ME Rancher UI : Argocd namespace -> Storage -> Secrets -> argocd-initial-admin-secret

**Ajouter un Repo Git sur Argocd UI**
  - Url Git: https://gitlab.com/miservers/demo-helm.git  (Bien Ajouter .git)
  - User: oauth
  - password: CHANGE_ME Tocken: <TOKEN_GITLAB>
 
**Creer une application**: demo-spring-chart. et entrer les infos:
  - Repo Git
  - Repertoire
  - Cluser
  - Namespace

Puis Synchroniser via argocd. https://app.rahali.com:<nod-port>/
