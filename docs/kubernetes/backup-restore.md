---
layout: default
title: Backup & Restore
parent:  Kubernetes
nav_order: 8.2
---

### Notes
**Activer la completion sur etcdutl**
~~~sh
etcdutl completion bash > completion_etcd.sh
chmod +x completion_etcd.sh
echo "source completion_etcd.sh" >> .bashrc
source .bashrc
~~~


### Install etcdutl et etcdctl: Sur un noeud
https://github.com/etcd-io/etcd/releases/


### Backup ETCD
**Create a Snapshot**
~~~sh
ETCDCTL_API=3 etcdctl  snapshot save /tmp/snapshot-etcd.db --endpoints=https://kmaster:2379   \
          --cert=/etc/kubernetes/pki/etcd/server.crt   \
          --key=/etc/kubernetes/pki/etcd/server.key   \
          --cacert=/etc/kubernetes/pki/etcd/ca.crt   
          
~~~

Inspect the snapshot
~~~sh
etcdutl --write-out=table snapshot status /tmp/snapshot-etcd.db

+----------+----------+------------+------------+
|   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+----------+----------+------------+------------+
| ac6d925f |   228453 |       3809 |      50 MB |
+----------+----------+------------+------------+
~~~

### Restoring an etcd 
1. Arreter l'Api Server: pour ce faire deplacer le manifest *kube-apiserver.yaml* et le kubelet le detecte et arrête l'api server.

Sur le Master:
~~~sh
mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/kube-apiserver.yaml
~~~

Check si l'api server est arrêté:
~~~sh
ps -ef | grep api-server
~~~


3. Stop the etcd, move the manifest, then kubelet will stop it: `mv /etc/kubernetes/manifests/etcd.yaml /tmp/`

4. Supprime le repertoire data de etcd: `rm -fr /var/lib/etcd`

5. restorer la base etcd 

~~~sh
etcdutl --data-dir /var/lib/etcd snapshot restore /tmp/snapshot-etcd.db
~~~

5. Restart etcd : `mv /tmp/etcd.yaml /etc/kubernetes/manifests/` then kubelet will start it

6. Redemarer l'api server: juste remet le manifest de l'api server. `mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/`



### List des member du cluster etcd
~~~
ETCDCTL_API=3 etcdctl --endpoints kmaster:2379   --cert=/etc/kubernetes/pki/etcd/server.crt \
               --key=/etc/kubernetes/pki/etcd/server.key   \
               --cacert=/etc/kubernetes/pki/etcd/ca.crt   member list
~~~


### Favoris
- https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/
- https://github.com/walidshaari/Kubernetes-Certified-Administrator
- https://github.com/OneideLuizSchneider/CKA/blob/main/03%20-%20backup-restore.md

