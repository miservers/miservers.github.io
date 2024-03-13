---
layout: default
title: CLI
parent: JBoss
grand_parent: Middleware
nav_order: 5
---


⚠️ **These notes are based on Jboss EAP 7.4 and Wildfly 29**

### Quick Start

http://www.jtips.info/WildFly/CLI

Intéractive mode

	./jboss-cli.sh  -c --controller=centos1:9990
 
non-interactive mode: 

	./jboss-cli.sh -u=jboss -p=pass123  -c --controller=localhost:9990 --commands="cd /core-service,ls"

There are two types to interact with the management interface:  
 - High Level [Commands](#commands)
 - Low Level [Operation Requests](#operation-requests)

### Commands
High level interactive mode with management interface.

	[domain@centos1:9990 /] help --commands
		deployment-info batch deploy deployment-info  deploy-file undeploy cd shutdown connect 
		data-source xa-data-source reload quit info ...

### Operation Requests
Low level interactive mode with management interface.

An Operation request basiquely consists of three parts: *address*, *operation name*, and *parameters*:      
 
	[/node-type=node-name(/node-type=node-name)*]:operation-name [([(param-name=param-value)*])]

For example:  

	/profile=full/subsystem=logging/root-logger=ROOT:write-attribute(name=level, value=INFO)
 
### TAB Completion
Very very useful.

### Main Operations
**read-operation-names** : List all available operations on a node  

	[domain@centos1:9990 /] /host=centos2/server=server-one:read-operation-names
		        ....
		        "read-children-names",
		        "read-children-resources",
		        "read-operation-names",
		        "read-resource",
		        "read-resource-description",
		        "start",
			    "kill",
			    "stop",
		        "write-attribute"

**read-resource**: Display attributes/values of a resource  

	[domain@centos1:9990 /] /server-group=main-server-group:read-resource
			{
			"profile" => "full",
			"socket-binding-default-interface" => undefined,
			"socket-binding-port-offset" => 0,
			"deployment" => {"jboss-as-helloworld.war" => undefined},
	       
**write-attribute** : Modify an attribute value.

	[domain@centos1:9990 /] /server-group=main-server-group:write-attribute(name=socket-binding-port-offset, value=100)


### Commands Standalone
TODO

### Commands in Domain
- **Subsystems and Profiles**   
The main diffence with the standalone, is that subsystems are not located in the root, but in a Profile.

		[domain@centos1:9990 /] /profile=full/subsystem=datasources/data-source=ExampleDS:read-resource

- **Start/Stop a Server**  

		[domain@centos1:9990 /] /host=centos2/server=server-one:start

		Others Operations: stop, restart, reload, read-operation-names

### domain.xml and CLI
![](/docs/images/Jboss-EAP-7.4.domain-cli.drawio.png) 

