---
layout: default
title: K3S
parent:  Kubernetes
nav_order: 1.5
---

### Config files
1. */etc/rancher/k3s/k3s.yaml*: Default kubeconfig file for API access.
3. */etc/rancher/k3s/config.yaml*: Custom K3s server configuration (e.g., node settings).
4. */etc/rancher/k3s/agent.yaml*: Configuration for K3s agent nodes.
5. */var/lib/rancher/k3s/server/tls/*: Certificates for server and node communication.
6. */var/log/k3s/*: K3s server logs.

Voir la config du cluster

~~~
 kubectl config view
~~~

### ~/.kube/config not found
et Erreurs : ``Kubernetes cluster unreachable: Get "https://127.0.0.1:6443/version``

~~~
mkdir -p ~/.kube
cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
chown $(id -u):$(id -g) ~/.kube/config
~~~

### Install k3s server with nginx controller
- installer le sans le contrôleur traefik(par defaut)

~~~
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable traefik,servicelb" K3S_KUBECONFIG_MODE="644" sh -
~~~

- reboot the VM.

- Installer NGINX comme Controlleur Ingress

~~~
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/baremetal/deploy.yaml
~~~

This creates a **ingress-nginx** with the service **ingress-nginx-controller** and **ingress-nginx-controller** pod.


### Commandes kubectl

Edit un service config avec vi
~~~
kubectl edit svc ingress-nginx-controller -n ingress-nginx
~~~
 
Les Nodes du cluster
~~~
kubectl get nodes
~~~


### Ingress
curl http://app.rahali.com/  : bien saisir le context /.

~~~
---
apiVersion: networking.k8s.io/v1
apiVersion: networking.k8s.io/v1
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rahali-app-ingress
  namespace: default
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$1
spec:
  rules:
    - host: app.rahali.com
      http:
        paths:
          - path: /api(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
          - path: /?(.*)
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
~~~

### Service

~~~
 kubectl apply -f nginx-ingress-controller.yaml
~~~

nginx-ingress-controller.yaml
~~~
apiVersion: v1
kind: Service
metadata:
  name: ingress-nginx
  namespace: ingress-nginx
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: ingress-nginx
  ports:
    - name: http
      port: 80
      nodePort: 30080
      targetPort: http
    - name: https
      port: 443
      nodePort: 30443
      targetPort: https
~~~


