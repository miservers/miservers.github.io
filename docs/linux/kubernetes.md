---
layout: default
title: Kubernetes
parent: Linux
nav_order: 9
---
## Kubernetes
--------------------------------
### Architecture
![art](/docs/images/kubernetes-cluster-architecture.svg)

### kubectl
kubectl is the primary tool for managing kubernetes clusters throughout the command line.

**List pods running on your cluster**
~~~sh 
$ kubectl get pods -A  
~~~

~~~log
	NAMESPACE              NAME                                         READY   STATUS 
	default                web-57f46db77f-dgh2w                         1/1     Running     2 (4h21m 
	kube-system            etcd-minikube                                1/1     Running     3 (4h21m 
	kube-system            kube-apiserver-minikube                      1/1     Running     3 (4h21m 
	kube-system            kube-scheduler-minikube                      1/1     Running     3 (4h21m 
	kube-system            storage-provisioner                          1/1     Running     6 (4h21m 
	kubernetes-dashboard   kubernetes-dashboard-8694d4445c-px9t2        1/1     Running     4 (4h21m 
~~~


### Ingress
Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster. An Ingress may be configured to give Services externally-reachable URLs, load balance traffic, terminate SSL/TLS, and offer name-based virtual hosting.
![ingress](/docs/images/kubernetes-ingress.svg)



## Minikube
--------------------------------

### Start/Stop the Cluster
~~~sh
$ minikube start | stop
~~~
Once started, you can interact with your cluster using ``kubectl``.

### Use minkube with Docker: as root
~~~sh
# minikube start --driver=docker --force
~~~

To make docker the default driver: ``minikube config set driver docker``

### Start Dashbord
~~~sh
$ minikube dashboard
~~~

![dashboard](/docs/images/kubernetes-dashboard.png)

If the dashboard is running on a remote server, you can access it via a ssh tunnel :
~~~sh
ssh -L 43673:127.0.0.1:43673 jammy@your_server_ip
~~~

### Deploy and Test a sample App
- Deploy a sample application on the Cluster  
~~~sh
$ kubectl create deployment web --image=gcr.io/google-samples/hello-app:1.0
~~~

- Expose the application on the http/8080  Port
~~~sh
$ kubectl expose deployment web --type=NodePort --port=8080
~~~

- Check if the application is running
~~~sh
$ kubectl get service web
~~~

- Retrieve the URL to access your sample application
~~~sh
$ minikube service web --url
~~~
  <a>http://192.168.49.2:32255</a>



