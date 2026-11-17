---
layout: default
title: Helm
parent:  Kubernetes
nav_order: 3
---

### Best Practice
#### Values par environnement
Pour reduire les erreurs de depoilement des values de DEV en Prod:

- values-dev.yaml
- values-pprd.yaml
- values-prod.yaml

#### Debug
utilise `helm lint ./chart` et `helm template ./chart -f values-dev.yaml --debug`

#### Utilise les labels
nottament les label communs **app.kubernetes.io**: voir la doc

#### Chart templates and namespaces
Avoid defining the namespace property in the metadata section. Use the flag `--namespace`.

#### Naming Conventions
Good
```
replicas: 1
soapTop: "valstr"
```

#### Templates
Template directives should have whitespace after the opening braces and before the closing braces:

Correct: `{{- print "bar" }}`

Incorrect: `{{print "bar"}}`


### Aide Memoire
- **.Release.Namespace** : est une variable interne dans les templates Helm. Elle représente le namespace dans lequel ton chart Helm est déployé. Cela evite les collesions de noms entre (prod, recette, dev)/
- **Ordre de priorité des values**
~~~
1. --set (ligne de commande)        priorité max
2. -f values.yaml (fichier externe)
3. values.yaml du chart
4. values.yaml des dépendances
~~~

**nameOverride**:	override name of the chart component default : .Release.Name

### Nommer dynamiquement les objets Kubernetes créés
Les vars sont définis dans **templates/_helpers.tpl**:
~~~
{{- define "demo-spring-chart.fullname" -}}
{{ printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
~~~

L'utiliser dans **templates/deployment.yaml**
~~~
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "demo-spring-chart.fullname" . }}-deployment
  labels:
    app: {{ include "demo-spring-chart.fullname" . }}
~~~



### Tutorial
- Repo du chart: [demo helm Chart ](ttps://gitlab.com/miservers/demo-helm)
- Image Spring sur docker hub:  **ddock789/spring-petclinic**. c'est moi qui la généré se basant sur [spring-petclinic](https://gitlab.com/miservers/spring-petclinic)

**Create a namespace**

``kubectl create namespace demo-backend-ns``


**Install a Chart**
~~~
helm install  demo-spring-chart ./demo-spring-chart --namespace demo-backend-ns
~~~

**List of installed Charts**
~~~
helm list --namespace demo-backend-ns
~~~

**URL**: 

- http://app.rahali.com:NodePort/. 

 Ou trouver ``NodePort``:  voir le YAML du service ``ingress-nginx-controller`` sous le namespace ``ingress-nginx``

- http://app.rahali.com:31837/actuator/health
   

**Mettre a jour une Chart**

~~~
helm upgrade  demo-spring-chart ./demo-spring-chart -n demo-backend-ns
~~~

**Uninstall a Chart**
~~~
helm delete demo-spring-chart   --namespace demo-backend-ns
~~~


### Chart utiles
- https://github.com/mlkmhd/kubernetes-network-policy-helm-chart/
- https://medium.com/@mgaurang123/building-scalable-application-pipelines-with-helm-and-kubernetes-a-practical-perspective-473a6ffa6deb