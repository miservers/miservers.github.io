---
layout: default
title: Storage
parent:  Kubernetes
nav_order: 10
---

### Pourquoi une StorageClass ?
Sans StorageClass, le processus de stockage est statique : un administrateur doit d’abord créer un PersistentVolume (PV), puis un PersistentVolumeClaim (PVC) doit le réclamer. 

Avec une StorageClass, Kubernetes peut créer des volumes à la demande, en fonction des besoins de l’application. L’administrateur définit une fois les règles et Kubernetes gère le reste !


### AWS EBS CSI Driver sur un cluster on-prime (kubeadm ec2)
[Référence](https://medium.com/@govind_sharma/aws-ebs-csi-driver-deployment-on-on-prem-kubernetes-cluster-kubeadm-ec2-f2dd70b00a03)

voir [notes aws](../aws) pour installer/configurer aws cli sur termux

Installed CSI drivers : `k get csidrivers.storage.k8s.io  -n kube-system`


### PV - Persistant Volum
Le PV est crée par l'administrateur Kube et System. Tandit que le PVC est crée/géré par les Deployment et Pods.

pv-petclinic-logs.yaml
~~~
apiVersion: v1
kind: PersistentVolume
metadata:
  name: petclinic-logs-pv
  namespace: demo-backend-ns
spec:
  capacity:
    storage: 100Mi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: /var/log/petclinic
~~~

Puis:
~~~
k apply -f pv-petclinic-logs.yaml

sudo mkdir -p /var/log/petclinic
sudo chown -R 1000:1000 /var/log/petclinic

~~~

### Partage de Volume entre Container et initContainer
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: emptydir-pod
spec:
  containers:
  - image: nginx:latest
    name: test-container
    volumeMounts:
    - mountPath: /data/bbc
      name: data-volume
  initContainers:
  - image: busybox:latest
    name: bbclog
    command:
    - sh
    - -c 
    - | 
      echo "HELLO" >> /data/bbc/test.log
    volumeMounts:
    - mountPath: /data/bbc
      name: data-volume
  volumes:
  - name: data-volume
    emptyDir:
      sizeLimit: 50Mi
```

### Rancher Local Path Provisioner
Installation: `kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.36/deploy/local-path-storage.yaml`

Creer un storage class


### Favoris
- https://www.ionos.fr/digitalguide/serveur/configuration/kubernetes-persistent-volume/
