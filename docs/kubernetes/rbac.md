---
layout: default
title: RBAC
parent:  Kubernetes
nav_order: 9
---

### ServiceAcount

**SA = ServiceAcount**: compte de service utilisé par les processus/pods pour s'authentifié auprés de l'API Server. Chaque pod a un SA associé (par defaut: `default`) pour pouvoir communiquer avec l'API Server(lire la conf, lister les ressources, etc)

Les permissions du SA sont définiées via le **RBAC** ( Role-Based Access Control). Le 'mot de passe' du SA est le **token**


List des serviceAccount : `k get serviceaccounts [-n namespace]`

Creer un token pour le SA default: `oc create token default -n dev-monitoring --duration 1h`

### Create a ServiceAcount pour lire les metrics 
!! Il faut creer un Cluster Role et pas un Role puisque NODE n'est pas namespacé

1. Creer un SA : `oc create serviceaccount mysa`
2. Créer un cluster role : `oc create clusterrole my-clusterrole --verb=get,list,watch --resource=nodes/metrics,nodes/stats`
3. Créer ClusterBinding : `oc create clusterrolebinding my-clusterrolebinding --serviceaccount=dev-monitoring:mysa --clusterrole=my-clusterrole`
4. Créer un Token : `oc create token mysa --duration=1h`
5. Test : `curl -k -H "Authorization: Bearer $TOKEN" https://<NODE-IP>:10250/metrics/cadvisor`
6. Test: `oc auth can-i get nodes/metrics --as=system:serviceaccount:dev-monitoring:mysa -A`
 