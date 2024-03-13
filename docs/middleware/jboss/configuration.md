---
layout: default
title: Configuration
parent: JBoss
grand_parent: Middleware
nav_order: 4
---


⚠️ **These notes are based on Jboss EAP 7.4 and Wildfly 29**

### Domain Configuration Files

- **domain.xml**
	- Contains servers settings, profiles, subsystems, deplyments...
	- Parsed by domain controller(master), but not by slave hosts controllers. A slave host controller gets its configurations from the remote domain controller when it registers with it.

- **host-master.xml**  
	It specifies that a host controller should become a domain controller(Master). No servers will be started by the domain controller(recommended in Production).  

    ~~~sh
	$ bin/domain.sh --host-config=host-master.xml
    ~~~

- **host-slave.xml**  
	It specifies that a host controller should become a Secondary host controller(Slave). It should register with a remote domain controller. This configurartion specifies how many servers to launch, and  what server groups they belong to.   

	~~~sh
	$ bin/domain.sh --host-config=host-slave.xml
    ~~~

- **host.xml**  
	Don't use it, use the two above config files.


### Standalone Configuration Files
- **standalone.xml**   
	- ports: http/8080, management/9990.
	- port-offset: default 0. for example, port-offset=100 gives http port 8180 et console 10090. 

- **standalone-ha.xml**   
	use this configuration to have clustering.
	
Run the standalone with a specefic config file

~~~sh
  ./standalone.sh -c standalone-ha.xml
~~~

### Modules
1. Add a Module with CLI

		./jboss-cli.sh --controller=centos1:9990 --connect

		module add --name=org.postgresql --resources=~/postgresql-42.6.0.jar 
				--dependencies=javax.api,javax.transaction.api

The jar is copied into **modules/org/postgresql/main/**

2. Remove a Module

		module remove --name=org.postgresql

### JDBC Driver
Add a JDBC Driver as a Module(Recommended) using CLI:

	module add --name=org.postgresql --resources=~/postgresql-42.6.0.jar 
			--dependencies=javax.api,javax.transaction.api

	/subsystem=datasources/jdbc-driver=postgres:add(driver-name=postgres, 
							driver-module-name=org.postgresql, 
							driver-class-name=org.postgresql.Driver)


### Data Sources	 
Using Console, Easy. You can Test It!

Using CLI

	data-source add --name=PostgresDS --jndi-name=java:/PostgresDS 
			--driver-name=postgres --connection-url=jdbc:postgresql://localhost:5432/postgresdb 
			--user-name=admin --password=admin

	reload

Test a DataSource

	/subsystem=datasources/data-source=PostgresDS:test-connection-in-pool

Remove a Data source

	data-source remove --name=PostgresDS

	reload


###  Logging
**logging.properties** : This is logging configuration is used when the server boots up until the logging subsystem kicks in.

Standalone Server
>./standalone/log/server.log

### Resource Adapters
Steps to declare a new resource adapter:  
1. Deploy the .rar archive
	Obtain  **wmq.jmsra.rar** in /opt/mqm/java/lib/jca/wmq.jmsra.rar

		CLI:
		
		deploy --server-groups=myapp-server-group /opt/mqm/java/lib/jca/wmq.jmsra.rar

2. Add  the resource adapter

		CLI:

		/profile=full/subsystem=resource-adapters/resource-adapter=wmq.jmsra.rar:add(archive=wmq.jmsra.rar, transaction-support=XATransaction)


3. Configure IBM MQ Adapter

4. Deploy JMS Test Application(find it in ibm mq installation directory) 
		
		deploy --server-groups=myapp-server-group /opt/mqm/java/lib/jca/wmq.jmsra.ivt.ear

5. Test

