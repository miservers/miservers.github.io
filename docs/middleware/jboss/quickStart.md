---
layout: default
title: Quick Start
parent: JBoss
grand_parent: Middleware
nav_order: 1
---


⚠️ **These notes are based on Jboss EAP 7.4 and Wildfly 29**

### Domain Architecture 

![jboss](/docs/images/Jboss-EAP-7.4.-Domain.drawio.png)

### Standalone
**Start/Stop**: Standalone Mode

	./standalone.sh -b 192.168.56.103 -bmanagement 192.168.56.103
 
	./jboss-cli.sh --user=jbossadmin --password=Changeit2! 
                 --connect --controller=$HOST:9990  command=:shutdown

### Console:
> http://HOST:9990/console

### Users	
Add Management/Application Users

	./add-user.sh

**Change Console Password**: Enter the username you want to change the password
	
	./add-user.sh

### Domain
**Start/Stop Domain Controller**:

	$ ./domain.sh -bmanagement 192.168.56.103 --host-config=host-master.xml

	CLI:
		/host=master:shutdown

**Start/Stop Host Controller**:

	$ ./domain.sh -Djboss.domain.master.address=192.168.56.103 -b 192.168.56.104 --host-config=host-slave.xml

	CLI:
		/host=SLAVE_NAME:shutdown
	 
**Start/Stop Servers**  

	[domain@centos1:9990 /] /host=centos2/server=server-one:start

	Others Operations: stop, restart, reload, read-operation-names

### CLI : Memos

	$ ./jboss-cli.sh --controller=centos1:9990 --connect

CLIs:

	# Start all servers of a Group
	/server-group=myapp-server-group:start-servers 

	# Change jvm heap size of a group
	 /server-group=myapp-server-group/jvm=default:write-attribute(name=heap-size, value=128m)


### Versions: Jboss EAP, Wildfly and JBoss AS 

| JBoss EAP  | Wildfly | JBoss AS (Old)|
|------------|---------|---------------|
| 8.0 Beta   | 27      | -             |
| 7.4        | 23      | -             |
| 7.3        | 18      | -             |
| 7.0        | 10      | -             |
| 6.4        | -       | 7.5           |
| 6.0        | -       | 7.1           |
| 5.x        | -       | 5.y           |
| 4.x        | -       | 4.y           |

### Common Errors
--------------------------------
#### Fatal Boot Error: Domain cannot start
Start the the domain controller in ADMIN-ONLY mode and correct the error

	./domain.sh  --admin-only ...


### References
--------------------------------
- https://www.jtips.info/WildFly
