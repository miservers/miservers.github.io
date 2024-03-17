---
layout: default
title: Mod-jk / Wildfly
parent:  Load Balancing
grand_parent: Middleware
nav_order: 2
---

## mod_jk: Wildfly
**Environment**: Centos Stream 9, Wildfly 29, Httpd 2.4

[JBoss EAP 7 - Mod_JK](https://access.redhat.com/documentation/en-us/red_hat_jboss_enterprise_application_platform/7.4/html/configuration_guide/configuring_high_availability#mod_jk-config)

**install mod_jk** 

	$ yum install mod_jk
	$ ls /etc/httpd/modules

**Config File Samples**: under /etc/httpd/conf.d

	 mod_jk.conf.sample
	 uriworkermap.properties.sample
	 workers.properties.sample


{: .warning }
  If Error: ajp worker not working between apache and Wildfly/Tomcat,  	
  Try `$ setenforce 0`


**Declare AJP Socket in Wildfly:**  

![alt](/docs/images/wildfly-29-sockets.png)

{: .note :}
in **full-ha-sockets** the port AJP is declared by default.


## Mod-Cluster
Env: Centos Stream 9, Wildfly 29, Httpd 2.4

	$ yum install mod_proxy_cluster

