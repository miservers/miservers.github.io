---
layout: default
title: Domain Setup
parent: JBoss
grand_parent: Middleware
nav_order: 2
---


⚠️ **These notes are based on Jboss EAP 7.4 and Wildfly 29**

## Domain Setup
------------------------------------------------------ 
A **Domain** consists of a domain controller, host controllers, server groups per host.

A **server group** is a set of server instances, and are managed and configured as one. each server in a group shares the same configuration and deplyments.

**Domain controller** is the central process controlling the managed domain.

**Host Controller** is launched when  **./domain.sh** is run on a host.

This config example, we have hosts:
- centos1(192.168.56.103) : domain controller host(master). 
- centos2(192.168.56.104) : slave server host.

### Domain Controller Configuration
Host : centos1(192.168.56.103) 

Do steps 1-3 in **host-master.xml** :

1. Choose a logical name of The domain controller: I choose a name **master**

	```xml
	<host xmlns="urn:jboss:domain:16.0" name="master">
	```

2. a host acts as domain controller via **domain-controller** declaration 

	```xml
	<domain-controller>
    	<local/>
	</domain-controller>
	```

3. Management Inteface: 

	```xml
	<interface name="management">
    	    <inet-address value="${jboss.bind.address.management:192.168.56.103}"/>
	</interface>
	```

	Or via *domain.sh* argument : -bmanagement 192.168.56.103
  
4. On the domain controller, create a new user(by **add-user.sh**) that can be used by slave host(centos2) controllers  to connect on the domain controller. I create a user/slave named **centos2**.

5. Start The Master    

	```sh	
	./domain.sh -bmanagement 192.168.56.103 --host-config=host-master.xml
	```

### Slave Host Configuration  
Host: centos2(192.168.56.104) 

To join a domain, a host controller configuration require 3 steps: 

Do  steps 1-3 in  **host-slave.xml**:

1. the logical host name needs to be distinct
	```xml
	<host xmlns="urn:jboss:domain:16.0" name='centos2'>
	```
	
2. Slave needs to know the password of the domain management user:

    {: .warning }
	Legacy security is no longer supported since version 25. Use Elytron. See High Availability topic.
	
	Use the hashed password previousely created  in the domain controller: 

	```xml
	<security-realm name="ManagementRealm">
            <server-identities>
                <secret value="Y2hhbmdlaXQ="/>
      		</server-identities>
	```

3. the Host Controller needs to now the Domain Controller name and IP.   
	
	```xml
	<domain-controller>
    	....
		<static-discovery name="master" protocol="${jboss.domain.master.protocol:remote+http}" 
			host="${jboss.domain.master.address}" port="${jboss.domain.master.port:9990}"/>
	```
		
4. Start The Slave:   

	```sh
	./domain.sh -Djboss.domain.master.address=192.168.56.103 -b 192.168.56.104 --host-config=host-slave.xml
	```


### How To Start Master and Slave on the same Machine

This is necessary if you want to create server instances on the Machine running the Maser.

⚠️ This is not recommanded!. The domain controller should be on a separated server.

		Domain Controller:
		
		[centos1]$ ./domain.sh -bmanagement 192.168.56.103 --host-config=host-master.xml

		Host Controller:

		[centos1]$ ./domain.sh -Djboss.domain.master.address=192.168.56.103 -b 192.168.56.103 --host-config=host-slave.xml

		 

https://www.dbi-services.com/blog/jboss-eap-7-domain-configuration/

