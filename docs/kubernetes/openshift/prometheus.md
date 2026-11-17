

### Install Prometheus Operator
1. Creer un namespace dedié : `dev-monitoring`
2.  Cherche le sur le marketplace: `oc get packagemanifests -n openshift-marketplace |grep prometheus`  
3. Infos sur l'operateur: `oc describe packagemanifests prometheus -n openshift-marketplace`
