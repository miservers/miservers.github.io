---
layout: default
title: CKA
parent:  Kubernetes
nav_order: 1
---

DNS My
http://safarit.duckdns.org/

### CKA Program & Examplee
- [CKA Program](https://training.linuxfoundation.org/certified-kubernetes-administrator-cka-program-changes/)

variables importantes à créer
```
dr='--dry-run=client -oyaml'
now='--grace-prriod=0 --force'
```

### Astuces Jour 
- Alias importants

  ```
  alias kn='kubectl config set-context --current --namespace'

  export dr="--dry-run=client -o yaml"

  # Cherche "kubectl alias ou kubectl quick reference"
  alias k=kubectl
  source <(kubectl completion bash)
  complete -F __start_kubectl k

  export KUBE_EDITOR=vim
  ```
- Aucun papier sur le bureau, avoir la piece d'identite et passport
- se rappeler de l'url de la doc : https://kubernetes.io/docs
- copier/coler : Ctl+Shift+C/V
- ALWAYS do this first: k config use-context <context-name>
- se connecter en root
- Deux passes approche : 80min=premiere passe, pas de plus de 8min par question. 2e passe=40 dernieres minutes
- Prefixer les noms des YAMLs par le numero des questions, par exemple 6-pvc.yaml pour la question n°6, pour pouvoir revenir corriger/reviser 
- Changer de context
  ~~~sh
  kubectl config get-contexts
  kubectl config use-context kubernetes-admin@kubernetes
  ~~~

Afficher les nom des pod ou tout autre resource: `k get po -o name`  
- To debug

  ```
  kubectl describe pod mypod # pod events
  kubectl get events 
  kubectl logs mypod --previous
  kubectl describe node worker-1
  journalctl -u kubelet -n 50
  ``` 

- Backup manifests for static pod before modifications: `/etc/kubernetes/manifests`

- Variable d'env à créer: `dr='--dry-run=client -o yaml'` et l'utiliser `k run/create .... $dr` pour generer rapidement un yaml

- Utiliser `--now` pour supprimer immediatement un objet avec `k delete ... --now`

  ~~~sh
  k run nginx --image=nginx --dry-run=client -o yaml
  k create deployment nginx-deploy --image=nginx --replicas=2 --dry-run=client -o yaml
  k run debug --image=busybox --dry-run=client -oyaml -- sleep 3600
  ~~~

le `--` separe les options passées à kubectl des arguments passés au conteneur. dans l'exemple ci-dessus `sleep 3600` est un  argument passé au conteneur.

### Questions types
- [Doc](https://github.com/theplatformlab/CKA-Certified-Kubernetes-Administrator#exam-day-strategy--time-allocation)

| Question Type                            | Note                                         |
|------------------------------------------|----------------------------------------------|
| Creation de Pod/deploiment/svc           | kubectl,  var dr=--dry-run=client -oyaml     |
| RBAC                                     | connaitre les commandes kubectl              |
| etcd: backup/restore                     | les info du connection dans kube-apiserver.yaml. Pour la resto, modifier le etcd.yaml dans deux endroits : --data-dir et hostPath|
| PV: perte PVC | Chercher "Bind PV": creer un pvc, modifier le deployment.yaml pour pointer sur ce pvc|
|Les resources(cpu/mem/disque) dispo pour les pods sur un noeud  | `k describe node <node> | grep Allocatable` |
|HPA                                       | `k autoscale ...`, il y a aussi HPA Walkthrough, un tuto à parcourir| 
| Gateway Api                              | Si la gateway a plusieurs listeners, utilise `sectionName: web-http` au niveau de httproute pour cibler le bon|
| Network Policy                           | Toujours utiliser `k describe networkpolicies` pour voir comment le netpol est interpreté|


### Commandes Indispensables
- Lister les resources deployé sur le cluster: `k api-resources`
- Run pod on a specific node:

  ```
  kubectl run debug --image=busybox --rm -it --restart=Never \
    --overrides='{"spec":{"nodeName":"kworker2"}}' \
    -- sh
  ```

- Lister les Pods en triant par date de creation/AGE: `k get po --sort-by=.metadata.creationTimestamp`
- Si le champs n'est pas présent, utiliser le custom-column: `k get po -ocustom-columns=NAME:.metadata.name,UID:.metadata.uid --sort-by=.metadata.uid`
- Liste des events ordonné: `k get events --sort-by {.metadata.creationTimestamp}`
- Affiche la Doc sur un champ(CRDs): `k explain <type>.<fieldName>[.<fieldName>] #ex: k explain certificate.spec.subject`


### RBAC Must know
Use kubectl wich is faster than yaml:
```
kubectl create serviceaccount my-sa -n default
kubectl create role pod-reader --verb=get,list,watch --resource=pods -n default
kubectl create rolebinding rb1 --role=pod-reader --serviceaccount=default:my-sa -n default

# Always verify
kubectl auth can-i list pods --as system:serviceaccount:default:my-sa
```

### Startup, Readiness and Liveness Probes

| Probe  | But | Succès  | Échec  | Quand  |
|--------|-----|---------|--------|--------|
| `livenessProbe` | Détecter un blocage ou panne| Rien | Redémarrage du Pod | Toute la vie du Pod |
| `readinessProbe` | App prête à recevoir du trafic? | Ajout aux endpoints | Retiré des endpoints | Toute la vie du Pod |
| `startupProbe` | Gérer un démarrage lent | Active les autres probes | Redémarrage du Pod | Au démarrage uniquement |

Exemple:
```
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  periodSeconds: 10
  failureThreshold: 3   # restart si 30s(3*10s) sans réponse

readinessProbe:
  httpGet:
    path: /health/db     # check connexion DB
    port: 8080
  periodSeconds: 5
  failureThreshold: 2   # retire du trafic si DB down pendant 10s
```

### Kustomize
- Voir le resultat avant appliquer: `kubectl apply -k <kustomization_dir>/`
- Overlays

### HPA - HorizontalPodAutoScaler
- Autoscale de 1 à  8 à partir de 50% de cpu: `kubectl autoscale deployment myapp --cpu=50% --min=1 --max=8`
  Dans cet exemple: les replicas vont être créé si l'utilisation de la CPU du POD depasse 50%
- Voir : `k get hpa -w`
- Un exemple contret : https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/
- Pour que les replicas retourne à la valeur initial avec un seuil, utilise `scaleDown`


### Metrics Server
- Installer  Metrics Server sur ton cluster

Pour afficher les stats CPU/MEM:
- Par Noeud: `ubectl top node `
- Par Pod et leurs conteneurs: `kubectl top pod --containers=true -A`
- Metrics d'un noeud: `kubectl get --raw "/api/v1/nodes/<node-name>/proxy/stats/summary" | jq '.'`
- Metrics CAdvisor sur un noeud: `kubectl get --raw "/api/v1/nodes/<node-name>/proxy/metrics/cadvisor" | jq '.'`

### Node Resources
- Pour Savoir les capacity (cpu/mem/disque) d'un noeud ansi que les resources **Allocatable** disponibles pour les pods, execulte `k describe node <node-name`
  
  ```
  Capacity:
  cpu:                2
  ephemeral-storage:  64704108Ki
  memory:             2910232Ki

  Allocatable:
    cpu:                2
    ephemeral-storage:  59631305835
    memory:             2807832Ki
    pods:               110
  ```

### Pod Priority
-  **preempt=evict**, un pod prioaitaire peut preempter un autre d'une prioritaire faible.

### CNI
- Quel CNI installé: /etc/cni/net.d
  
Installer un CNI, par exemple Flannel
1. Apply le manifest 
2. Verifier les Pods, ils vont tomber a cause du CIDR, donc faire
   ```
   k  logs kube-flannel-ds-rjbwv -n kube-flannel  # Pour voir l'erreur
   k edit cm kube-flannel-cfg -n kube-flannel     # Corrige le CIDR
   ```
3. Relance tous les pods de Flannel


### Metrics Server
- Installer  Metrics Server sur ton cluster

Pour afficher les stats CPU/MEM:
- Par Noeud: `ubectl top node `
- Par Pod et leurs conteneurs: `kubectl top pod --containers=true -A`
- Metrics d'un noeud: `kubectl get --raw "/api/v1/nodes/<node-name>/proxy/stats/summary" | jq '.'`
- Metrics CAdvisor sur un noeud: `kubectl get --raw "/api/v1/nodes/<node-name>/proxy/metrics/cadvisor" | jq '.'`


### Static Pods
Defini par defaut dans /etc/kubernetes/manifests (il y a api-server, scheduler, etcd et controller-manager), pour arrêter un de  ces pods il suffit de "supprimer/mover" son yaml. Kubelet scan periodiquement ce repertoire pour creer/supprimer les pods statics. utilise `crictl ps`. Les noms du pods statics ont un prefix le nom du host.

### Certificats & CSR
CSR permets de gerer les certs par kube sans passer par openssl.

- Verifier les dates d'expiration des certs des composants(api-server, etcd,etc): `kubeadm certs check-expiration`

- Generer un csr: `kubeadm certs generate-csr --kubeconfig-dir /tmp/etc-k8s --cert-dir /tmp/etc-k8s/pki`

- renouveler un cert d'un ou de touts les composant du controler manager: `kubeadm certs renew all | apiserver|etcd-server`


### CoreDNS
Deux elements pour configurer le coreDNS

  1. Configmap `coredns` 
  2. Service `kube-dns` 

### CRDs : CustomResourceDefinitions
- Affiche la Doc sur un champ(CRDs): `k explain <type>.<fieldName>[.<fieldName>]`
- Extract the doc for subject spec de Certificate(cert-manager): `k explain certificate.spec.subject`

### Network Policies
- Utilise `describe` Pour voir comment ton network policy a été interprété: `k describe networkpolicies -n frontend`
- Une subtilité : utilise `describe`
```yaml
egress:   # vers les pod backend sur port 80 + vers tous les pods des namespaces backend sur port 80
  - to:
    - podSelector:
        matchLabels:
          app: backend
    - namespaceSelector:
        matchLabels:
          role: backend
    ports:
    - port: 80
      protocol: TCP
```
Est different de : vers les pod backends des namespaces backend sur le port 80 
```yaml
egress:
  - to:
    - podSelector:
        matchLabels:
          app: backend
      namespaceSelector:
        matchLabels:
          role: backend
    ports:
    - port: 80
      protocol: TCP
```

### Etcd Backup/Restore
- Les infos de connection à etcd (cert, key, endpoint ) sont dans /etc/kubernetes/manifest, nottament dans kube-apiserver.yaml
- Prendre un snapshot: 
  ```
  ETCDCTL_API=3 etcdctl --cacert /etc/kubernetes/pki/etcd/ca.crt \
                        --cert /etc/kubernetes/pki/apiserver-etcd-client.crt \
                        --key /etc/kubernetes/pki/apiserver-etcd-client.key \
                        --endpoints https://127.0.0.1:2379 snapshot save  snapshot.db
  ```
- Inspecter le snapshot: `etcdutl --write-out=table snapshot status snapshot.db`
- Restaurer un snapshot
  1. `etcdutl --data-dir <data-dir-location> snapshot restore snapshot.db`
  2. Pointer le pod static etcd sur la nouvelle location. Deux endroits dans etcd.yaml  : --data-dir et hostPath


### Gateway Api
- Si la gateway a plusieurs listeners, utilise `sectionName: web-http` au niveau de la httproute pour cibler le bon

### Categories
- [Cluster Installation & Configuration](../cluster-admin)
- [Workloads & Scheduling](../Workloads-Scheduling)
- [Backup et Restore](../backup-restore)

### Examples CKA
- https://github.com/alijahnas/CKA-practice-exercises
- https://github.com/markdjones82/CKA-PREP-2025-v2/
- https://github.com/CameronMetcalfe22/CKA-PREP
- https://github.com/theplatformlab/CKA-Certified-Kubernetes-Administrator
  
### Favoris
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts)
- https://github.com/walidshaari/Kubernetes-Certified-Administrator
- [Certified Kubernetes Administrator (CKA) Course](https://github.com/kodekloudhub/certified-kubernetes-administrator-course)

### Resources
- Chaine youtube **Jaydemy** : CKA exam examples
- YouTube IT Kiddie et Dumb IT Guy,

### CKA  Questions
- **Lister les pods, en affichant Nom et IP et Statut du pod**
~~~
k get po debug -ojson
k get po debug -oyaml
k get po -A --sort-by='{.status.podIP}' -ocustom-columns=NAME:.metadata.name,IP:.status.podIP,STATUS:.status.phase
~~~

Options:
  - `-ojson` ou `-oyaml` pour voir tous les champs, 
  - le help `-o -h` pour les options du output
  - https://kubernetes.io/docs/reference/kubectl/#custom-columns

- **créer un cluster**
~~~
kubeadm init --pod-network-cidr 10.24.0.0/16  --apiserver-advertise-address 172.24.1.156   --ignore-preflight-errors all
~~~
apiserver-advertise-address est l'ip de la vm

~~~
 cp /etc/kubernetes/admin.conf ./kube/Configuration
~~~

- Mark a Node unschedulable
~~~
kubectl cordon node1
~~~


- **Sidecar** : est un initContainer avec restartPolicy: Always
        