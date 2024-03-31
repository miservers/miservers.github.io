---
layout: default
title: JVM
parent: Middleware
nav_order: 10
---

## JVM
#### MetaSpace
![metaspace](/docs/images/jvm.png)

#### Disassembl the .class  
    javap -p -v Hello.class

#### exract one file from .jar  
    jar xvf rt.jar java/lang/Object.class  

#### extract one file from .zip  
    unzip -l myarchive.zip  
    unzip -j src.zip java/lang/Object.java
 
#### Construct a war
	mv myapp.war temp/
	cd temp/
	jar -xvf myapp.war
	rm myapp.war
	jar -cvf ../myapp.war *

#### Modify a file in a jar
    jar xf catalina.jar org/apache/catalina/util/ServerInfo.properties
    jar uf catalina.jar  org/apache/catalina/util/ServerInfo.properties    
	or
	zip -x|-u

#### Check if JAVA support 64 bits
	java -d64 -version
	
## JVM Tuning
see : http://blog.sokolenko.me/2014/11/javavm-options-production.html

#### Java >= 8 settings in production

~~~sh
    -server
    -Xms<heap size>[g|m|k] -Xmx<heap size>[g|m|k]
    -XX:MaxMetaspaceSize=<metaspace size>[g|m|k]
    -Xmn<young size>[g|m|k]
    -XX:SurvivorRatio=<ratio>
    -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled
    -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=<percent>
    -XX:+ScavengeBeforeFullGC -XX:+CMSScavengeBeforeRemark
    -XX:+PrintGCDateStamps -verbose:gc -XX:+PrintGCDetails -Xloggc:"<path to log>"
    -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M
    -Dsun.net.inetaddr.ttl=<TTL in seconds>
    -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=<path to dump>`date`.hprof
    -Djava.rmi.server.hostname=<external IP>
    -Dcom.sun.management.jmxremote.port=<port> 
    -Dcom.sun.management.jmxremote.authenticate=false 
    -Dcom.sun.management.jmxremote.ssl=false
~~~

#### Large Heap Memory  
Java 64 has no limit of heap memory (>100Go). But GC pauses increase a lot(stop-the-world). Pauses of several tens of seconds 
if Xmx<30Go, and several minutes if >30Go. Tunning: use __-XX:+UseConcMarkSweepGC__. If Xmx<4Go there is no problem.

#### Preserve Memory
Disable loading JVMs Graphic Library: Option  "-Djava.awt.headless=true"

  
## Out Of Memory
**Generate a heapdump**

    jmap -histo -F 6764
    jmap -F -d64 -dump:format=b,file=tempheap.bin 6764
	

**Eclipse Memory Analyzer (MAT)**: very good tool for analysing of HeapDump


## Thread Dump : High CPU

1. Genrerer des threads dumps : 
   ~~~sh
   kill -3 pid
   ~~~
   ou
   ~~~sh
   jstack  -J-d64  -m 24326 >> appli1.tdump
   ~~~

2. Lancer la commande **top**, puis entrer **H** pour show threads on.

3. Identifier le thread qui a le plus de CPU et TIME+

~~~sh
  PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+     COMMAND
10477 tomcat    20   0 13.2g 6.2g  15m R 300  19.9    501:08.65 java
10456 tomcat    20   0 13.2g 6.2g  15m R 47.6 19.9    523:25.89 java
10447 tomcat    20   0 13.2g 6.2g  15m R 47.2 19.9    513:57.74 java
24363 tomcat    20   0 13.2g 6.2g  15m R 46.3 19.9    520:55.67 java
~~~

4. le thread le plus consommatrice est **10477**, transformé en hex, **0x28ed**. Le thread coupable est trouvé dans threadDump **nid=0x28ed**

~~~sh
"asyncThread-16" daemon prio=10 tid=0x00007f81f0035800 nid=0x28ed runnable [0x00007f81d209e000]
   java.lang.Thread.State: RUNNABLE
	at java.util.HashMap.put(Unknown Source)
~~~

[Analysis cpu high](https://blogs.oracle.com/jiechen/analysis-against-jvm-thread-dump-cpu-high-usage-issue)

## Thread Dump: Dead Lock
[Analysis cpu high](https://blogs.oracle.com/jiechen/analysis-against-jvm-thread-dump-dead-lock)

## Thread Dump: Resource Contention
[Analysis Resource Contention](https://blogs.oracle.com/jiechen/analysis-against-jvm-thread-dump-resource-contention)

## Thread Dump: Out Of Thread
[Analysis Out Of Thread](https://blogs.oracle.com/jiechen/analysis-against-jvm-thread-dump-out-of-thread)


## Java Performances Utilities
------------------------------------------

### jcmd
list all runnring jmv

    jcmd

Flight Recording

    jcmd PID JFR.start name=MyRecording settings=profile delay=20s duration=2m filename=~/myrecording.jfr

Flight Recording Status

    jcmd PID JFR.check

Analyse JFR File : use **jmc** tool

### jmc : Java Mission Control


## Java Tools
#### JavaMelody
https://github.com/javamelody/javamelody

#### MAT : Eclipse Memory Analyzer

  
