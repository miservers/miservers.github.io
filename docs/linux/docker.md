---
layout: default
title: Docker
parent: Linux
nav_order: 8
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
$ docker pull almalinux:latest   // dowload an Image
$ docker images                  // List of installed images
$ docker rmi [IMAGE_ID]          //Remove an image
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

## Containers
----------------------------------------------------
**Container Commands:**
~~~sh
$ docker ps     // List of Running containers

$ docker ps -a  // List of all containers even if stopped

$ docker stop/start myhttpd2     //Start a container
$ docker stop $(docker ps -a -q) // Stop all containers
$ docker rm myhttpd2          //Remove a container

~~~

- **Create Command** : Create a container from a docker image,  without start it.
- **Start Command**: start a stopped container.
- **Run Command**: create a container from a docker image and start it. Also run command will pull the image if it is not present on the system. 

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

**Docker Container IP Address**:
> By default, the container is assigned an IP address for every docker network it is connected to. 

**Wich IP assigned to the container?**

	~~~sh
	docker inspect -f "{{ .NetworkSettings.IPAddress }}" my-almnalinux
	~~~

## Docker Volumes
----------------------------------------------------
Docker volumes are used to persist data outside the container so it can be backuped or shared. it can be set using option **-v** or **--volume**.

Example :
~~~sh
$ echo "<h1>Hello from Dockered HTTPD </h1>" > ./public-html/index.html
$ docker run -d --name myapp-httpd -p 8080:80 -v "$(pwd)"/public-html:/usr/local/apache2/htdocs/  my-apache2
~~~
That will map container directory */usr/local/apache2/htdocs/* to the host machine directory *$pwd/public-html*



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


## SSH into a Linux Docker Container
----------------------------------------------------
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
	$ docker run -d  --hostname alma1 --name alma1 -p 1022:22 almnalinux
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
  $ dnf install  passwd openssh-clients 
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
    