### Network Policy

- By default, a pod is non-isolated for egress; all outbound connections are allowed.


 
### Demo on k3s 
index.html
~~~
html>
<head>
  <title>Hello World! DEMO</title>
</head>
<body>Hello World! from k3s demo</body>
</html>
~~~

~~~
kubectl create configmap demo-http --from-file index.html
~~~

~~~
k create namespace httpd-demo-ns
~~~

demo-httpd.yaml
~~~
---
apiVersion: v1
kind: Service
metadata:
  name: httpd-demo-service
  namespace: httpd-demo-ns
spec:
  type: NodePort
  selector:
    app: httpd_demo_app
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30004

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpd-demo-deployment
  namespace: httpd-demo-ns
  labels:
    app: httpd_demo_app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: httpd_demo_app
  template:
    metadata:
      labels:
        app: httpd_demo_app
    spec:
      containers:
        - name: httpd-demo-container
          image: httpd:latest
          ports:
            - containerPort: 80
~~~

~~~
k apply --namespace httpd-demo-ns -f demo-httpd.yaml 
~~~