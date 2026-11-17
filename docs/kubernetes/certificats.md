---
layout: default
title: Certificats
parent:  Kubernetes
nav_order: 12
---

### Certificat pour ton url
Gnerer un cert auto signé
~~~shell
openssl req -x509 -nodes -days 365   -newkey rsa:2048  \
        -keyout tls.key   -out tls.crt   -subj "/CN=app.rahali.com/O=Safar"
~~~

Encoder le cert/key en  b64 pour qu'ils puissent être ajouté sur une seule ligne
~~~shell
cat tls.crt | base64 | tr -d '\n' > tls.crt.b64
cat tls.key | base64 | tr -d '\n' > tls.key.b64
~~~

Creer un Secret nommé *my-app-tls-secret*
~~~yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-app-tls-secret
  namespace: demo-ns
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FU.... # en base64
  tls.key: LS0tLS1CRUdJTiBQUklWQVRFIEtFWS...
~~~

L'ajouter dans ton Ingress
~~~yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
...
spec:
  rules:
    - host: app.rahali.com
    ...
  tls:
    - hosts:
      - app.rahali.com
      secretName: my-app-tls-secret
~~~



### Cert Manager
Fournisseur de certificat au cluster. TODO