---
layout: default
title: Storage NFS
parent:  Kubernetes
nav_order: 10
---


Tuto: https://blog.stephane-robert.info/docs/conteneurs/orchestrateurs/kubernetes/storageclass/

### Install NFS Server
```
sudo apt install nfs-server

vi /etc/exports
/data *(rw,sync,no_subtree_check,no_root_squash)

sudo systemctl restart nfs-kernel-server

sudo chown nobody:nogroup /data                  
sudo chmod 777 /data                             
sudo exportfs -ra  # reload

sudo exportfs # verifie 
```

### Install CSI nfs driver
```
helm repo add csi-driver-nfs https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/charts
helm install csi-driver-nfs csi-driver-nfs/csi-driver-nfs --namespace kube-system --version 4.12.0
```

### Verifier le pod du controleur:
```
k get pod -n kube-system -l app.kubernetes.io/name=csi-driver-nfs --watch -owide

NAME                                  READY   STATUS    RESTARTS      AGE     IP              NODE       
csi-nfs-controller-7f69b88754-xsfjd   5/5     Running   8 (19m ago)   4h45m   172.31.33.171   kworker2
csi-nfs-node-lkkh4                    3/3     Running   3 (19m ago)   4h45m   172.31.33.73    kmaster    
csi-nfs-node-pth6b                    3/3     Running   3 (19m ago)   4h45m   172.31.33.171   kworker2  
```

```
k get csidrivers.storage.k8s.io

NAME             ATTACHREQUIRED   PODINFOONMOUNT   STORAGECAPACITY   TOKENREQUESTS    MODES       
nfs.csi.k8s.io   false            false            false             <unset>          Persistent   
```

### Storage class 
```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-sc
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: nfs.csi.k8s.io
parameters:
  server: 172.31.21.15 # Remplacer par l'adresse IP du serveur NFS
  share: /data
reclaimPolicy: Delete #Retain
volumeBindingMode: WaitForFirstConsumer  #Immediate
allowVolumeExpansion: true
mountOptions:
  - nfsvers=4.1
  ```
  
### PVC
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nfs-claim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: nfs-sc
  resources:
    requests:
      storage: 1Gi
```

### Pod de test
```
apiVersion: v1
kind: Pod
metadata:
  name: app-using-nfs
spec:
  containers:
    - name: app
      image: busybox
      command: [ "sleep", "3600" ]
      volumeMounts:
        - mountPath: "/backup"
          name: nfs-volume

  volumes:
    - name: nfs-volume
      persistentVolumeClaim:
        claimName: nfs-claim
```

### Le PV est automatiquement créé 
```
$ k get pv              
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM               STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
pvc-80531f92-9774-4ede-9d36-a8c0ff4bb9d0   1Gi        RWO            Delete           Bound    default/nfs-claim   nfs-sc         <unset>                          8s
```
### Ce qui coté serveur nfs
```
ubuntu@nfs-srv1:/data$ ls                                                                                    pvc-5a4fc3f9-081a-41da-aa6f-434e5ccb6bf5                                      
  pvc-31b607c1-564d-4e1a-9d9a-df35070561be  
  pvc-80531f92-9774-4ede-9d36-a8c0ff4bb9d0
```