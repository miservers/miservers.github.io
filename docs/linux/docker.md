---
layout: default
title: Docker
parent: Linux
nav_order: 11
---

### Docker Architecture
![docker](/docs/images/docker-architecture.png)

- **Docker Objects**: images, containers, networks and volumes are called Objects.
- **Docker Images**: are  templates used to run a containers. They can be pulled from Docker Hub. You can create your own image using **dockerfile**.
- **Docker Container**: is a instance of a docker image.
- **Docker Daemon**: **dockerd** is based on a client/server. It listens for API (create, pull, start, run, etc) and manages Docker Objects.
- [Docker Hub](https://hub.docker.com): is a public registry for a wide variety of Docker images.
- **Docker Registry**: is a place where docker images are stored. It can be public or private.
- **Voulmes**: Persisting Data. 
  docker run -d --name mynginx  -v myvolume:/app nginx:latest
- **Networks**: through wich isolated containers can communicate. Types of docker networks: Bridge, Host, Overlay, None, macvlan.
  
### Start Docker Daemon
    sudo systemctl start docker

### Build a Docker Image
Create the  *Dockerfile*

    FROM httpd:2.4
    COPY ./public-html  /usr/local/apache2/htdocs/

Build the Image

    docker build -t myhttpd:2.4 .


### Docker Images
List of installed images

    docker images

Remove an image

    docker rmi [IMAGE_ID]


### Docker Containers
List of Running containers

    docker ps

List of all containers even if stopped

    docker ps -a

Start/start a container

    docker stop/start myhttpd2

Remove a container

    docker rm myhttpd2

### Command Help
All Docker Commands

    docker -h

Help on a Command(eg. build)

    docker build -h


### Tomcat Container
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
    