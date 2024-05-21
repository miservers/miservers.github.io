---
layout: default
title: Podman
parent: DevOps
nav_order: 5.1
---


## Concepts
- **Podman** is an OCI compliant container management tool that offers similar features like Docker.
- Podman runs and manages containers without root privileges  = Security.
- Podman is also daemonless (unlike docker), meaning it doesn’t have a daemon. 

Podman is configured with two container registries.
  
  - <a>quay.io
  - <a>docker.io

By default, podman searches for images in quay.io first and then in docker.io. 

Commands are similar to docker, just replace `docker` by `podman`.

`alias docker=podman`

## Manage Images
- Pull an image:
~~~sh
podman pull docker.io/nginx
~~~

List Of images:  
`podman images`

## Manage Containers
### Run an container
~~~sh
podman  run --name docker-nginx -p 8080:80 docker.io/nginx
~~~

You cannot use ports below 1024 in rootless mode. If you wand a port below 1024, use **sudo**.

### List of Ports
~~~sh
$ podman port -l

80/tcp -> 0.0.0.0:8080
~~~

### Inspect the Container
~~~sh
podman inspect -l
~~~

### Commands
~~~sh
podman ps
podman ps -a
podman stop <container-name>
podman rm <container-name>
~~~

## Pod With Podman
A **pod** is a unit where you can have one or more containers.

`podman pod --help`

Create a Pod:
`podman pod create --name demo-pod`

List of Pods
`podman pod ls`

Run a container inside a Pod:
`podman run -dt --pod demo-pod  nginx`

Create a Pod with Containers:
`podman run -dt --pod new:frontend -p 8080:80 nginx`

Start, Stop and Delete Pod
~~~sh
podman pod start <podname>
podman pod stop <podname>
podman pod rm <podname>
~~~


## Podman and Systemd
~~~sh
man podman run

…

--systemd=true|false

Run container in systemd mode. The default is true.
~~~

Docs : 
- <a>https://developers.redhat.com/blog/2019/04/24/how-to-run-systemd-in-a-container#enter_podman


## Podman Desktop
[Desktop Download](https://podman-desktop.io/)

![a](/docs/images/podman-desktop-1.png)
![a](/docs/images/podman-desktop-2.png)









