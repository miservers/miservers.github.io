---
layout: default
title: Montoring - Tuning
parent: JBoss
grand_parent: Middleware
nav_order: 6
---


⚠️ **These notes are based on Jboss EAP 7.4 and Wildfly 29**

**Monitoring**
------------------------------
### Metrics
/extension=org.wildfly.extension.metrics:add

 /profile=full/subsystem=metrics:add

/profile=full/subsystem=metrics:read-resource
{
    "outcome" => "success",
    "result" => {
        "exposed-subsystems" => undefined,
        "prefix" => undefined,
        "security-enabled" => true
    }

http://192.168.56.103:9990/metrics


### Health
 /extension=org.wildfly.extension.health:add
 
/profile=full/subsystem=health:add

**Performance Tuning**
-------------------------------
### 7.1 JVM Settings 
**Domain**  
JVM setting can be defined on different scope: For a Server Group, for a host, or for a specific server.
  
 ⚠️ Below configurations should be done on the [Console > Runtime](http://HOST:9990/console/index.html#runtime)  

- JVM Setting for a Server Group: **domain.xml**  
  All servers of this group inherit these settings.   
	```xml
	<server-group name="myapp-server-goup" profile="full">
        <jvm name="default">
            <heap size="128m" max-size="512m"/>
        </jvm>
	```

- JVM Setting for a host: **host-slave.xml**   
  These settings will be used if no setting are defined for the server group and for the server.   
	```xml
	<jvms>
        <jvm name="default">
            <heap size="64m" max-size="256m"/>
	```

- JVM Setting for a specific server: **host-slave.xml**    
  If defined, these settings have priority.     
	```xml
    <server name="srv1" group="myapp-server-goup" auto-start="false">
        <jvm name="default">
            <heap size="128m" max-size="512m"/>
	```


**Standalone** : standalone.conf

	 JAVA_OPTS="-Xms1024m -Xmx1024m -XX:MetaspaceSize=96M -XX:MaxMetaspaceSize=256m




### 7.2 JConsole
:exclamation: Don't use JDK Jconsole, use EAP_HOME/bin/jconsole.sh

Standalone:

1. Enable JMX Remoting connector:

	> Console : Configuration ⇒ Subsystems/Subsystem ⇒ JMX  ⇒  remoting-connector: jmx

2. EAP_HOME/bin/jconsole.sh
	> service:jmx:http-remoting-jmx://192.168.57.103:9990


### 7.3 VisualVM
Todo

