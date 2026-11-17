---
layout: default
title: Rancher
parent:  Kubernetes
nav_order: 1
---


### Install sur Docker
**Environnement**: Bien verifier la matrice de  compatibilité

- AlmaLinux  9.5
- Docker: 27.0.1
- Rancher: v2.10.3
- Desactive le firewall

Utilise un DNS a declarer dans les /etc/hosts: rancher.rahali.com

**Erreur** : https://127.0.0.1:6444: connect: connection refused

  https://github.com/ansible-collections/community.docker/issues/868

==> 

1. install iptables
2. make sure that missing iptables modules
~~~
sudo cat<<EOF >/etc/modules-load.d/modules.conf
iptable_nat
iptable_filter
EOF
~~~
3. Reboot the vm

**Install Rancher**
~~~
docker run -d --restart=unless-stopped \
  -p 80:80 -p 443:443 \
  --privileged --name rancher \
  rancher/rancher:v2.10.3
~~~

- Reboot the vm

waiiiit

**Tail des logs**
~~~
docker logs -f rancher
~~~

**Accéder à rancher**

https://rancher.rahali.com

**Reset admin password**
~~~
  docker exec -it rancher reset-password
~~~

### import du cluster dans rancher

utilise rancher pour generer le script d'import
si probleme de certif , telecharge le yaml puis:

kubectl apply -f ranch.yaml

Si le cluster  reste en pending, verifier les logs peut etre proble de certif.

Editer le yaml en utilisant 127.0.0.1

Logs du cluster :

 sudo journalctl -u k3s -f

logs d'un pod:

kubectl logs -n cattle-system cattle-node-agent-ndg8d


