---
layout: default
title: Docker
parent: DevOps
nav_order: 5
---

## Quick Start
----------------------------------------------------

### Docker Architecture
![docker](/docs/images/docker-architecture.png)

Concepts:
> 
- **Docker Objects**: images, containers, networks and volumes are called Objects.
- **Docker Images**: are  templates used to run a containers. They can be pulled from Docker Hub. You can create your own image through a **dockerfile**.
- **Docker Container**: is a instance of a docker image.
- **Docker Daemon**: **dockerd** is based on a client/server architecture. It listens for API (create, pull, start, run, etc) and manages Docker Objects.
- [Docker Hub](https://hub.docker.com): is a public registry for a wide variety of Docker images.
- **Docker Registry**: is a place where docker images are stored. It can be public or private.
- **Voulmes**: Persisting Data. 
  docker run -d --name mynginx  -v myvolume:/app nginx:latest
- **Networks**: through wich isolated containers can communicate. Types of docker networks: Bridge, Host, Overlay, None, macvlan.

### Start Docker Daemon
    
~~~sh 
$ systemctl start docker
~~~
### Help 
~~~sh 
$ docker -h
$ docker build -h
~~~

## Docker Images
----------------------------------------------------
**Command on Images:**
~~~sh 
$ docker pull almalinux:latest       // dowload an Image
$ docker images                      // List of installed images
$ docker build -t image_name:tag .   // Buld an image from Dockerfile
$ docker rmi [IMAGE_ID]              //Remove an image
~~~

**Build Command**: builds docker images from a **Dockerfile** and a Context.  

~~~sh
$ docker build -t my-apache2 .
~~~

**Modify an Image:**
- Create a file named *Dockerfile*
	~~~conf 
    FROM httpd:2.4
    COPY ./public-html  /usr/local/apache2/htdocs/
    ~~~

- Build the Image
	~~~sh
    $ docker build -t myhttpd:2.4 .
	~~~

**Create a new Image from a Container: COMMIT**
~~~sh
$ docker commit container-id newimage-name
~~~

## Containers
----------------------------------------------------
**Container Commands:**

~~~sh
$ docker ps     // List of Running containers
$ docker ps -a  // List of all containers even if stopped

$ docker run --name container_name image_name // Create and Start a container


$ docker stop/start myhttpd2     //Start a container
$ docker stop $(docker ps -a -q) // Stop all containers

$ docker exec {options}          // Execute a command inside running  container

$ docker rm myhttpd2             //Remove a container

$ docker logs --follow alma3     // Logs of a container
~~~

- **Create Command** : Create a container from a docker image,  without start it.
- **Start Command**: start a stopped container.
- **Run Command**: create a container from a docker image and start it. Also run command will pull the image if it is not present on the system. 

**Docker Inspection**  
It prints info about the container:
- inspect configuration: port mappings, 
- volumes, PortBindings, IPAddress,

~~~sh 
$ docker inspect container_name_or_id
~~~

**List of mapped Ports**
~~~sh 
docker port containerId_or_name
~~~

## Netwoks
----------------------------------------------------
Docker Networks: 

![net](/docs/images/docker-networks.png)

~~~sh
$ docker network ls

NETWORK ID     NAME      DRIVER    SCOPE
6720595d9c04   bridge    bridge    local
6a270dade505   host      host      local
d54a5e61ba05   none      null      local
~~~

**Type of Networks**
- **Bridge**:default, named **bridge**. create a subnet  allowing to the containers to communicate with ecah other. It also create a network isolation between the host and containers.   
- **Host**: containers use the host IP subnet. no network isolation between host and containers.
- **None**

**Setup the container network**
~~~sh
$ docker run --network=host ...
$ docker run --network=bridge ...
~~~

**Wich IP assigned to the container?**

{% raw %}
~~~sh
$ docker inspect -f "{{ .NetworkSettings.IPAddress }}" alma1
~~~
{% endraw %}

**Inspect the Bridge**
~~~sh
$ docker network inspect bridge

    "Name": "bridge",
    "Scope": "local",
    ...
        "Subnet": "172.17.0.0/16",
        "Gateway": "172.17.0.1"
    ...
    "Containers": {
            "Name": "alma1",
            "IPv4Address": "172.17.0.2/16",
 ~~~       

**Create a Custom Bridge**
~~~sh
docker network create --driver bridge --subnet 172.20.0.0/16 mynet1
~~~


**Connect a Container to Network**
~~~sh
docker network connect mynet1 alma1
~~~


**Inspect the Bridge**
~~~sh
docker network inspect mynet1

  "Name": "mynet1",
  "Driver": "bridge",
  "Config": [
          "Subnet": "172.20.0.0/16"
  ....
  "Containers": {
      "Name": "alma1",
      "IPv4Address": "172.20.0.2/16",
~~~


## Docker Volumes
----------------------------------------------------
Docker volumes are used to persist data outside the container so it can be backuped or shared. it can be set using option **-v** or **--volume**.

Example :
~~~sh
$ echo "<h1>Hello from Dockered HTTPD </h1>" > ./public-html/index.html
$ docker run -d --name myapp-httpd -p 8080:80 -v /myapp/public-html:/usr/local/apache2/htdocs/  my-apache2
~~~
That will map container directory */usr/local/apache2/htdocs/* to the host machine directory */myapp/public-html*



## HTTPD Container
----------------------------------------------------
1. Pull the Image 
~~~sh
$ docker pull httpd:2.4
~~~

2. Create **Dockerfile** with contents:
	~~~conf
	FROM httpd:2.4

	COPY ./public-html/ /usr/local/apache2/htdocs/
	~~~

   For testing create a file *./public-html/index.html* with somme html code.

	~~~sh
	$ echo "<h1>Hello from Dockered HTTPD </h1>" > ./public-html/index.html
	~~~
	
3. Next, Build and Run the Container
	~~~sh
	$ docker build -t my-apache2 .
	 
	$ docker run -d --name myapp-httpd -p 8080:80 -v "$(pwd)"/public-html:/usr/local/apache2/htdocs/  my-apache2
	~~~

4. Test: <a>http://localhost:8080/</a>

## AlmaLinux Dockered
----------------------------------------------------
### SSH into a Linux Docker Container
- Create Dockerfile:
  ~~~ conf
	FROM almalinux:latest
	RUN dnf -y install openssh-server 
	RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
	RUN ssh-keygen -A
	RUN echo "root:changeit" | chpasswd
	EXPOSE 22
	CMD ["/usr/sbin/sshd", "-D"]
	~~~

- Alma Linux Image:
	~~~sh
	$ docker -D build -t almnalinux .
	~~~

- Create the Container
	~~~sh
	$ docker run -d  --hostname alma1 --name alma1  -p 1022:22 -v /media/jadmin/Data21/containers/alma1/opt:/opt -v /opt/IBM/PackagingUtility:/opt/IBM/PackagingUtility almnalinux
	~~~

- Change the Container hostname
	~~~sh
	$ docker run -d  --hostname alma1 ...
	~~~

- Wich IP assigned to the container? 
    {% raw %}
	~~~~sh
	$ docker inspect -f "{{ .NetworkSettings.IPAddress }}" alma1
	~~~~
	{% endraw %}
	Or look for **IPAddress** in /var/lib/docker/containers/CONTAINER-ID/config.v2.json


- SSH into the Container
	~~~sh
	$ ssh root@172.17.0.2
	~~~

- Packages 
  ~~~sh
  $ dnf install  passwd openssh-clients iproute wget procps sudo
  ~~~

###  Using Docker Compose
Create the file *docker-compose.yml*
~~~yaml
version: '3'
services:
  vm-alma1:
    image: almalinux:latest
    container_name: alma1
    hostname: alma1
    ports:
      - '1022:22'
    volumes:
      - /media/jadmin/Data21/containers/alma1/opt:/opt 
      - /opt/IBM/PackagingUtility:/opt/IBM/PackagingUtility
    networks:
      vlan1:
        ipv4_address: 10.2.0.2
    command:
      - /bin/sh
      - -c
      - |
        dnf -y install openssh-server 
        echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
        ssh-keygen -A
        echo "root:changeit" | chpasswd
        /usr/sbin/sshd -D 
    expose:
      - 22
networks:
  vlan1:
    driver: bridge
    ipam:
     config:
       - subnet: 10.2.0.0/16
         gateway: 10.2.0.1
~~~

Create and start containers:
~~~sh
docker compose up -d
~~~

Start/Stop Services
~~~sh
docker compose start|stop
~~~


## Tomcat Container
----------------------------------------------------
Pull Docker Image From the Hub

    docker pull tomcat:10.0

Create and Start a Tomcat Container from The Image

    docker container create --publish 8888:8080 --name my-tomcat-10 tomcat:10.0
    docker container ls -a
    docker container start my-tomcat-10
    docker container ls  # show running containers

Access Url : <http://localhost:8888>

There are no web apps deployed by default.

Access to Tomcat Container Directory

    Docker container exec -it my-tomcat-10 bash
    root@081fe841268a:/usr/local/tomcat# ls


## Docker Compose
----------------------------------------------------
Docker Compose relies on YAML configuration files, commonly named *docker-compose.yml* placed in working directory.

### Create an HTTPD and MySQL Containers
1. Create *docker-compose.yml* file
   ~~~yaml
	version: '3'
	services:
	  db:
	     image: mysql
	     container_name: mysql_db
	     restart: always
	     environment:
	        - MYSQL_ROOT_PASSWORD="secret"
	  apache:
	    image: httpd:latest
	    container_name: my-apache
	    ports:
	      - '8080:80'
	    volumes:
	      - ./website:/usr/local/apache2/htdocs
	    depends_on:
	      - db
	    restart: always
   ~~~
   
   For Testing create a html file *./websit/index.hml* 

2. Build Images and Start Containers
	~~~sh
	docker compose up -d
	~~~

	Access the website: <a>http://127.0.0.1:8080</a> 
3. Stop Containers
	~~~sh
	docker compose down
	~~~

### Transform Docker commands to compose
<a>https://www.composerize.com</a>

## Miscs
----------------------------------------------------
### Library Missing For Installing WebSphere 
~~~sh
 $ dnf whatprovides '*/libcrypt.so.1'
 $ dnf install libxcrypt-compat
~~~	