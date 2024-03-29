---
layout: default
title: Performance Tuning
parent:  Tomcat
grand_parent: Middleware
nav_order: 5
---


### Activate remote JMX 
Edit _bin/setenv.sh_ with:  

```sh
export CATALINA_OPTS="-Dcom.sun.management.jmxremote \
                  -Dcom.sun.management.jmxremote.port=3333 \
                  -Dcom.sun.management.jmxremote.ssl=false  \
                  -Dcom.sun.management.jmxremote.authenticate=true\
                  -Dcom.sun.management.jmxremote.password.file=../conf/jmxremote.password\
                  -Dcom.sun.management.jmxremote.access.file=../conf/jmxremote.access"
```
Create files : 

    $ echo "jmxuser readonly" >>  jmxremote.access
    $ echo "jmxuser passwd123" >> jmxremote.password 
    $ chmod go-rwx jmxremote.password

Or Without credentials:

```sh
	-Dcom.sun.management.jmxremote
	-Dcom.sun.management.jmxremote.port=6666
	-Dcom.sun.management.jmxremote.ssl=false
	-Dcom.sun.management.jmxremote.authenticate=false
```

**Probem**: JConsole, connection refused to 127.0.0.1  
Solution: add also this option to the remote JVM, -Djava.rmi.server.hostname=hostIp

**Simple load test simulation** 
  
    ab -n 100000 -c 100 http://localhost:8080/

### JMX Proxy Servlet
Prereq:
* manager application installed
* role manager-jmx

```xml
# cat tomcat-users.xml
  <role rolename="manager-jmx"/>
  <role rolename="manager-gui"/>
  <user username="tomcat" password="changeit" roles="manager-gui,manager-jmx"/>
```
Heap Memory:  
<http://localhost:8080/manager/jmxproxy/?get=java.lang:type=Memory&att=HeapMemoryUsage>

Query All :  
<http://localhost:8080/manager/jmxproxy/?qry=*:*>

Datasource:  
http://localhost:8080/manager/jmxproxy/?qry=Catalina:type=DataSource,host=localhost,context=/examples,
class=javax.sql.DataSource,name=%22jdbc/hellodb%22

### Monitoring FAQ
[FAQ Monitoring](https://wiki.apache.org/tomcat/FAQ/Monitoring)  

### Monitoring using Java Mission Control(JMC)
#### Thread Pool
ThreadPool(Not using Executor) :   

    Catalina:name=http-nio-8080,type=ThreadPool  
    Catalina:name=ajp-nio-8080,type=ThreadPool  
    attributs:
          currentThreadsBusy
          maxThreads
          currentThreadCount
          connectionCount"

![alt txt](/docs/images/Tomcat-Thread-Monitoring-By-JMC.png)

Mbean name can be "http-bio-8080" on tomcat 6 & 7. 

If using Executor: 

    JMX Bean: Catalina:type=Executor,name=[executor name]
    Attributes: poolSize, activeCount 

Recommandation : In Tomcat 7 you must use Executor.
 

#### DataSource
    JMX Bean: Catalina:type=DataSource,context=[context name],
                        host=[hostname],class=javax.sql.DataSource,name="[JNDI name]"
    Attributes: numActive, numIdle

![alt txt](/docs/images/Tomcat-JDBC-Pool-Monitoring-JMC.png)

#### Request Throughput
    JMX Bean: Catalina:type=GlobalRequestProcessor,name="[depends]"
    Attributes: bytesSent, bytesReceived, errorCount, maxTime, requestCount
    Operations: resetCounters 

#### Sessions
    JMX Bean: Catalina:type=Manager,context=[context name],host=[hostname]
    Attributes: activeSessions, sessionCounter, expiredSessions

