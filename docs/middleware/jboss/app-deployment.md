---
layout: default
title: Apps Deployment
parent: JBoss
grand_parent: Middleware
nav_order: 3
---


⚠️ **These notes are based on Jboss EAP 7.4 and Wildfly 29**

### Deployment On Managed Domain

Deploy/Undeploy.

	[domain@centos1:9990 /] deploy --server-groups=myapp-server-group /opt/helloworld-jboss.war 
	[domain@centos1:9990 /] undeploy --server-groups=myapp-server-group helloworld-jboss.war 

Deployment Status:

	[domain@centos1:9990 /] /server-group=myapp-server-group/deployment=helloworld-jboss.war:read-resource


### Deployment On Standalone server

	[standalone@centos1:9990 /] deploy /opt/jboss-as-helloworld.war
	
	[standalone@centos1:9990 /] undeploy jboss-as-helloworld.war


