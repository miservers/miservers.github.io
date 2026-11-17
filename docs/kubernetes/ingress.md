---
layout: default
title: Ingress
parent:  Kubernetes
nav_order: 5
---

### Must Know
Si tu utilise istio comme ingress controller, tu dois utiliser  son IP ou son EXTERNAL-IP si metallb est configuré. Avec istio-ingressgateway, une seule IP externe (172.31.64.100) suffit pour exposer tous vos services, le routage interne se faisant via le hostname ou le chemin de l'URL.

```
k get svc -n istio-system
NAME                          TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                                      AGE
istio-ingressgateway          LoadBalancer   10.111.57.127    172.31.64.100   15021:32288/TCP,80:32407/TCP,443:31339/TCP   20h

curl -H"Host: app2.safarit.local" http://172.31.64.100

```


Pour creer rapidement un yaml pour ingress:
`k create ingress ingress2 --class=istio-ingress-controller --rule="foo.com/*=svc:8080,tls=secret1" --dry-run -oyaml`

Les Ingress Class peut être de scope cluster ou namespacé



### Commands
**Liste des Ingress**
~~~sh
$ kubectl  -n monitoring get ingress
~~~
~~~
NAME                    CLASS   HOSTS                   ADDRESS     PORTS     AGE
ingress-monitoring      nginx   grafana.rahali.com      10.0.2.15   80, 443   22h
monitoring-prometheus   nginx   prometheus.rahali.com   10.0.2.15   80        23h
~~~

**Lists des Services**
~~~sh
$ kubectl  -n <ns> get svc
~~~
~~~
NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
prometheus-k8s          ClusterIP   10.43.192.199   <none>        9090/TCP,8080/TCP            24h
grafana                 ClusterIP   10.43.172.157   <none>        3000/TCP                     24h
~~~

**Faire un curl vers un service local**
~~~sh
curl http://<service>.<namespace>.svc.cluster.local:<port>/health
~~~




### Rewrite
- Si Aucune annotation de rewrite : pas de redirection, le chemin original est conservé.
- Exemple(Helm Values) de reecriture de /admin/xyz en /actuator/xyz et les uri autres restent inchangés

~~~
ingress:
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
    nginx.ingress.kubernetes.io/use-regex: "true"
    nginx.ingress.kubernetes.io/rewrite-target: /actuator/$2
  hosts:
  - host: app.rahali.com
    paths:
      - path: /admin(/|$)(.*)    # redirige /admin/health -> /actuator/health
        pathType: ImplementationSpecific
      - path: /
        pathType: Prefix
~~~

### URL 

- http://app.rahali.com:NodePort/. 

 Ou trouver ``NodePort``:  voir le YAML du service ``ingress-nginx-controller`` sous le namespace ``ingress-nginx``

### Ingress-NGINX Controller
Quand on crée une resource ingress, cela inserre automatiquement un vhost dans le fichier **nginx.conf** du Nginx. Pour voir son contenu, il faut entrer en shell dans le POD **ingress-nginx-controller**.



### Controlleurs Ingress
- Traefic: par defaut sur k3s. a remplacer par nginx, facile
- ingress-nginx: officiel k8s, opensource
- nginx-ingress: commercial (par F5/NGINX Inc)

### Troubleshooting Nginx - Ingress Controller
- [Article Interessant](https://github.com/giantswarm/ingress-nginx-upstream/blob/main/docs/troubleshooting.md)

- Verifier l'etat des pods
~~~
kubectl get pods -n ingress-nginx
~~~

- Inspecter les Logs
~~~
kubectl logs -n ingress-nginx  ingress-nginx-controller-6fb7885497-w8g89 -f
~~~

**Activer le debug**
  - Recuperer le deplyment
  ~~~
  kubectl get deploy -n ingress-nginx 
  ~~~

  - Editer Le, et y ajouter **-
  ~~~
  kubectl edit deploy ingress-nginx-controller -n ingress-nginx
  ~~~
  
  Et ajouter à **args** avec **--v=XX**

  - **--v=2** : shows diff about the changes in the config in nginx
  - **--v=3** : shows the service, Ingress rule,..
  - **--v=5**:  debug mode


  args:    
- /nginx-ingress-controller                
- --v=3



#### Erreur 404: Page not found
- Verifier si le Ingress contient un ingressClass Valid.

 => Logs du Pod du Controller Ingress-Nginx : ``"Ignoring ingress because of error while validating ingress class" ingress="vault/ingress-vault" error="ingress does not contain a valid IngressClass"``

 => Correction Ajouter cette annotation dans ton Ingress Manifest
 ~~~
      apiVersion: v1
      kind: Ingress
      metadata:
        ...
      spec:
        ingressClassName: nginx
 ~~~

- Activer le Debug dans ton Ingres
~~~
      apiVersion: v1
      kind: Ingress
      metadata:
        annotations:
          nginx.ingress.kubernetes.io/log-level: "debug"  
          nginx.ingress.kubernetes.io/enable-debug: "true" # Optionnel 
 ~~~

Les access logs sont ecrits dans les logs du POD du controlleur Ingress-Nginx

#### Service without Active Endpoints
-- **Service does not have any active Endpoint.**: no pods available to serve traffic
  
  cas 1: Verifier que les labels corespondent entre pod  service et deployment

   ~~~
   kubectl get pods --show-labels -n demo-backend-ns
   ~~~

   ~~~
   kubectl get svc demo-spring-api-svc -n demo-backend-ns -o yaml
   ~~~

   et compare **spec.selector** avec les labels des pods.


  cas 2: Verifier targetPort declaré dans le service existe bien dans le pod  

  ~~~
  kubectl describe svc demo-spring-api-svc -n demo-backend-ns 
  ~~~

  ~~~
  kubectl describe deployment demo-spring -n demo-backend-ns
  ~~~
  
  verrifier que ``tagetPort`` correspond celui qui est exposé par le conteneur ``ports.containerPort``

### This site can’t be reached
- Changer le type: LoadBalancer → type: NodePort
~~~
kubectl edit svc ingress-nginx-controller -n ingress-nginx
~~~

Puis utilise le NodePort: http://app.rahali.com:31837/


### Favoris
- [TroubleShooting Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/#troubleshooting)


