---
layout: default
title: Cluster Admin
parent:  Kubernetes
nav_order: 8.1
---

### Init a Cluster
~~~
kubeadm init --pod-network-cidr=10.2.0.0/16 --apiserver-advertise-address=172.31.46.82
~~~
l'addresse de l'api-server doit etre celle de la VM

### Ajouter un noeud au Cluster
1. Create a Token, avec l'option de générer la commande join
~~~sh
kubeadm token create --print-join-command
~~~

2. La commande ci-dessus va créer un token sur le serveur, et vous donne la commande `kubeadm join` à executer sur le noeud à joindre au cluster
~~~sh
kubeadm join 172.31.46.82:6443 --token pmofnp.xxxxxx --discovery-token-ca-cert-hash sha256:xxxx
~~~

3. Verifier que le status du noeud: attendre 2 min pour qu'il soit **Ready**
~~~sh
k get nodes
~~~

### Upgrade the cluster
Follow the good official Doc [Under Documentation Tasks](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade)
1. Upgrade control-plane
  1.1 update `kubeadm`
  1.1 Verify the version : `kubeadm version`
  1.2 Upgrade cluster : `kubeadm upgrade  plan | apply`
2. Upgrade worker nodes
  2.1 Drain node
  2.2 Upgrade kubelet  
  2.3 Uncodon the node