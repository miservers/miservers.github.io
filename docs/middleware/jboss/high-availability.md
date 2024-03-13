---
layout: default
title: High Availability
parent: JBoss
grand_parent: Middleware
nav_order: 7
---


⚠️ **These notes are based on Jboss EAP 7.4 and Wildfly 29**

**High Availability**
------------------------------------------------------
High availability can be guaranted by Load Balancing or Failover. 

Cluster is made available by jgroup, infinspan and modcluster subsystems. *ha* and *full-ha* profiles enable these subsystems.

**Reference**: [Clustering and Domain Setup Walkthrough](https://docs.wildfly.org/29/High_Availability_Guide.html#Clustering_and_Domain_Setup_Walkthrough)


### Cluster
Environment: Wildfly 29, Centos 7


![](/docs/images/Wildfly-29.-Cluster.drawio.png)

⚠️ NOT recommended to set up domain controller and host controller on the same machine/vm. 

1. **Interface config on the Primary Host Controller**

	<ins>host.xml</ins> : Master Host. IP 192.168.56.103

	```sh
	$ cp host-primary.xml host.xml
	```

	```xml
	<host xmlns="urn:jboss:domain:20.0" name="primary">
	```

	```xml
	<domain-controller>
	    <local/>
	</domain-controller>
	```

	```xml
	<interfaces>
	    <interface name="management">
	        <inet-address value="${jboss.bind.address.management:192.168.56.103}"/>
	    </interface>
	    <interface name="public">
	        <inet-address value="${jboss.bind.address:192.168.56.103}"/>
	    </interface>
	</interfaces>
	```

	On the primary host: with **add-user.sh** create a user **centos2** so that secondary host controller can be authenticated on the primary host controller.

2. **Interface config on the Secondary Host Controller**

	<ins>host.xml</ins> : Secondary Host. IP centos2/**192.168.56.104**
	
	```sh
	$ cp host-secondary.xml host.xml
	```


	```xml
	<host xmlns="urn:jboss:domain:20.0" name='centos2'>
	```

	```xml
	<domain-controller>
        <remote>
            <discovery-options>
                <static-discovery name="primary" protocol="remote+http" host="192.168.56.103" port="9990"/>
            </discovery-options>
        </remote>
    </domain-controller>
	```

	```xml
    <interfaces>
        <interface name="management">
            <inet-address value="${jboss.bind.address.management:192.168.56.104}"/>
        </interface>
        <interface name="public">
            <inet-address value="${jboss.bind.address:192.168.56.104}"/>
        </interface>
    </interfaces>
	```

	**Authentication(Legacy)**: no longer supported from Wildfly 25!


	**Authentication(Elytron)**: <ins>host.xml</ins>.   

	```xml
	<subsystem xmlns="urn:wildfly:elytron:18.0" final-providers="combined-providers" disallowed-providers="OracleUcrypto">
        <authentication-client>
            <authentication-configuration sasl-mechanism-selector="DIGEST-MD5"
                                  name="hostAuthConfig"
                                  authentication-name="centos2"
                                  realm="ManagementRealm">
                    <credential-reference clear-text="changeit"/>
            </authentication-configuration>
            <authentication-context name="hcAuthContext">
                    <match-rule authentication-configuration="hostAuthConfig"/>
            </authentication-context>
        </authentication-client>
		...
	```

	```xml
	<domain-controller>
        <remote protocol="remote+http" host="192.168.56.103" port="9990" username="centos2" authentication-context="hcAuthContext"/>
    </domain-controller>
	```

	**Mask the Password(Elytron)**:

	```sh
	$ bin/elytron-tool.sh mask --salt 12345678 --iteration 256 --secret changeit
	MASK-2pr2SIUwzZyLvedad/aMuC;12345678;256
	```

	```xml
	<subsystem xmlns="urn:wildfly:elytron:18.0" final-providers="combined-providers" disallowed-providers="OracleUcrypto">
        <authentication-client>
            <authentication-configuration sasl-mechanism-selector="DIGEST-MD5"
                                  name="hostAuthConfig"
                                  authentication-name="centos2"
                                  realm="ManagementRealm">
				<credential-reference clear-text="MASK-2pr2SIUwzZyLvedad/aMuC;12345678;256"/>
	```
	

3. **Create a server group with HA capabilities**

![](/docs/images/wildfly-29-cluster2.png)

Create Instances:

![](/docs/images/wildfly-29-cluster3.png)


4. **Deploy an Cluster Demo**

	[github.com/liweinan/cluster-demo](https://github.com/liweinan/cluster-demo)

**web.xml**
	
```xml
  <distributable/>
```

**put.jsp**

```jsp
  <%
  session.setAttribute("current.time", new java.util.Date());
  %>
```

**Generate the war** : 

	$ mvn package

Deploy It! on myapp-server-group

Test Session Replication:

  - http://192.168.56.104:8080/cluster-demo/put.jsp
  - http://192.168.56.103:8080/cluster-demo/get.jsp


### Mod Cluster

{: .warning }
Error compiling mod_cluster under Centos 7 du to the old version of G++ compiler. Compilation OK on Centos Stream 9, BUT httpd service faild to start!!.

- Install httpd server

	yum install httpd

- Download modCluster and Compile it: See the native/README

### Mod JK
See [Load Balancing](/docs/middleware/load-balancing/#mod_jk-wildfly)

### Failover



