---
layout: default
title: Etcd
parent:  Kubernetes
nav_order: 9
---

### Etcd
ETCD est embarqué dans des pods : */etc/kubernetes/manifests/etcd.yaml**
```yaml
kind: Pod
  name: etcd
  namespace: kube-system
spec:
  containers:
  - command:
    - etcd
    - --advertise-client-urls=https://10.24.1.20:2379
    - --cert-file=/etc/kubernetes/pki/etcd/server.crt
    - --client-cert-auth=true
    - --data-dir=/var/lib/etcd
```

**Installer le client**: installe etcd il embarque le etcdctl et etcdutl
image: registry.k8s.io/etcd:3.6.6-0

**Take a snapshot: backup**
```
ETCDCTL_API=3  etcdctl --endpoints=https://10.24.1.20:2379  --cert=/etc/kubernetes/pki/etcd/server.crt \
                       --key=/etc/kubernetes/pki/etcd/server.key   --cacert=/etc/kubernetes/pki/etcd/ca.crt \
                       snapshot save snapshot.db
```

/!\: N'oublie pas les certs,sinon il reste bloqué

**Verifier le snaphot**
```
etcdutl --write-out=table snapshot status snapshot.db
+----------+----------+------------+------------+
|   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+----------+----------+------------+------------+
| 357c8bd6 |    79548 |       1997 |     9.0 MB |
+----------+----------+------------+------------+
```

**Restore a backup**

Restaurer : `etcdutl --data-dir /var/lib/etcd-backup snapshot restore snapshot.db`

Default : data-dir-location is /var/lib/etcd use an other

A ce point etcd ne poitent pas sur la restore, pour le faire il faut modifier `etcd.yaml`. Modifier le manifest ETCD pour pointer sur /var/lib/etcd-backup 

```
spec:
  containers:
  - command:
    - etcd
    - --data-dir=/var/lib/etcd-from-backup   # 👈 ICI
    volumeMounts:
      - mountPath: /var/lib/etcd-from-backup
  volumes:
  - hostPath:
      path: /var/lib/etcd-from-backup        # 👈 ET ICI
      type: DirectoryOrCreate
    name: etcd-data
``

Le kubelet va automatiquement relancer le pod etcd: `watch crictl ps`

/!\: Ne jamais relancer manuellement un pod static avec `crictl stop`, c'est kubelet qui le fait.


**Verifier le backup** : `ETCDCTL_API=3 etcdctl snapshot status /opt/etcd-backup.db --write-out=table`


### Etcd Browser



### Etcd Tools
- https://etcd.io/docs/v3.4/integrations/
- [Etcd Browser](https://github.com/henszey/etcd-browser)
