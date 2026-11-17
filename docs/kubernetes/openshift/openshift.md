
### Operateurs

**Opérateurs installés**: `oc get operators`

**Opérateurs via OLM**:  `oc get subscription -A`

**État des opérateurs cluster**: `oc get clusteroperators`

### LM — Operator Lifecycle Manager
C'est le gestionnaire d'opérateurs d'OpenShift. Il automatise l'installation, la mise à jour et la gestion des opérateurs.

**Catalogues disponibles**: `oc get catalogsource -n openshift-marketplace`
```
NAME                  DISPLAY               TYPE   PUBLISHER   AGE
certified-operators   Certified Operators   grpc   Red Hat     8d
community-operators   Community Operators   grpc   Red Hat     8d
redhat-marketplace    Red Hat Marketplace   grpc   Red Hat     8d
redhat-operators      Red Hat Operators     grpc   Red Hat     8d
```

**Opérateurs disponibles**: `oc get packagemanifest -n openshift-marketplace`

**Opérateurs installés**: `oc get csv -A`

**Subscriptions actives**: `oc get subscription -A`

### Routes, Ingress
**Ingress** : `oc create ingress nginx-ingress --rule="nginx.safarit.local/=nginx-svc:8080" --class=openshift-default`

**HTTPRoute** : Il faut un GatewayClass(ex: OVN Kubernetes). Le mieux c'est d'utiliser les Routes natif d'Openshift
