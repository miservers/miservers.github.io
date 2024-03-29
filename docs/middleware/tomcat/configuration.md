---
layout: default
title: Configuration
parent:  Tomcat
grand_parent: Middleware
nav_order: 1
---


HowTo set up Tomcat 10: [RUNNING.txt](https://tomcat.apache.org/tomcat-10.1-doc/RUNNING.txt)

### Configure Environment Variables
* CATALINA_HOME(required) : On Linux can be defined in **.bash_profile**

	export CATALINA_HOME=/opt/tomcat-10

* CATALINA_BASE (optional) : usefull in case of multiple tomcat instance. by default it is equal o CATALINA_HOME.
* JAVA_HOME (required) : 
* CATALINA_OPTS (optional) :
* JAVA_OPTS (optional) :


Apart from CATALINA_HOME and  CATALINA_BASE, all this variables can be defined in the **setenv** script.

### setenv script 
On *nix, $CATALINA_BASE/bin/setenv.sh:
~~~sh
  JAVA_HOME=/opt/jdk
  CATALINA_PID=$CATALINA_HOME/run/tomcat.pid
~~~

### Start Tomcat as systemd Service
See [Linux Systemd](/docs/linux/systemd-sysv)

### Admin Manager
http://192.168.56.101:8080/manager/html


Official documentation here : [manager-howto](https://tomcat.apache.org/tomcat-10.0-doc/manager-howto.html)

1. To Access the manager from a REMOTE Host, Allow your IP in <ins>context.xml</ins> under tomcat-10/webapps/manager/META-INF/

```xml
  <Valve className="org.apache.catalina.valves.RemoteAddrValve" 
  allow="^192.168.56.1$" />
```

### Load Balancing
#### Mod_Jk : Apache HTTPD and Tomcat
See  [Load Balancing](/docs/middleware/load-balancing/modjk-tomcat) 

#### jvmRoute  
Located in server.xml, it is used by the load balancer to enable session affinity. Il must be unique accros tomcat instances..
