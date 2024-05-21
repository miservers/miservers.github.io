
## Kubernetes
--------------------------------
### Architecture
![art](/docs/images/kubernetes-cluster-architecture.webp)

### kubectl
kubectl is the official command tool for managing kubernetes clusters.

**List pods running on your cluster**
~~~sh 
$ kubectl get pods 
~~~

~~~log
	NAME                   READY   STATUS    RESTARTS        AGE
	demo                   1/1     Running   0               113s
	web-57f46db77f-9jj6g   1/1     Running   1 (2m32s ago)   24h
~~~

**List of Nodes**
~~~sh
$ kubectl get nodes
~~~

**Display Pod Console/Logs**
~~~sh
$ kubectl logs demo
~~~

~~~log
	PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
	64 bytes from 8.8.8.8: icmp_seq=1 ttl=112 time=186 ms
	64 bytes from 8.8.8.8: icmp_seq=2 ttl=112 time=48.5 ms
	64 bytes from 8.8.8.8: icmp_seq=3 ttl=112 time=67.0 ms
~~~


### Create a Pod from YAML
- Create a *pod.yaml* file  

  ~~~yaml
  apiVersion: v1
  kind: Pod
  metadata:
	name: demo
  spec:
	containers:
	- name: testpod
	  image: almalinux:latest
	  command: ["ping", "8.8.8.8"]
  ~~~

- Deploy the Pod
  ~~~sh
  kubectl apply -f pod.yaml
  ~~~
- List Pods and Check Logs
  ~~~bash
  kubectl get pods
  kubectl logs demo
  ~~~
- Finaly tear your demo 
  ~~~sh
  kubectl delete -f pod.yaml
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

### Set Memory and CPU
~~~sh
$ minikube delete
$ minikube config set memory 2048
$ minikube config set cpus 2
$ minikube start --force
~~~

### Config Files
_~/.minikube/config/config.json_
~~~json
    "cpus": "2",
    "driver": "docker",
    "memory": "2048"
~~~

