---
layout: default
title: Nodes
parent: WebSphere
grand_parent: Middleware
nav_order: 2.5
---


### Start/Stop a Node

- **Start a Node Agent**
	~~~sh
	${WAS_INSTALL_ROOT}/profiles/profile_name/bin/startNode.sh
	~~~

### Federate a Node: addNode
addNode is used to federate a node to the DMGR. addNode script is invoked from the node that you want to federate. Management SOAP  port (default 8879) is used to connect to the DMGR.  

Below, dmgr is running on centos1 machine. the node to be federated is centos2.

Do on Centos2
:
  - Installation Manager must be installed under wasadmin user.
  - WAS must be installed.
	
  - Create a managed server profile using *manageprofiles* script.
  - Create a dummy node using *addNode* script. If the the node is previously created, add option *-noagent* to addNode. That also federate the node to the dmgr.
	
	~~~sh
	${WAS_INSTALL_ROOT}/profiles/AppSrv01/bin/addNode.sh dmgr_host dmgr_soap_port_8879  -username wasadmin -password changeit -includeapps
	~~~

### Synchronize a node
N.B : install Websphere as root make a problem of synchrinisation when Globlal security is enabled.
- From Web Console
- **Manually synchronize the node**  
  Stop Node, and run syncNode script.
  ~~~sh
  $WAS_INSTALL_ROOT/profiles/AppSrv02/bin/syncNode.sh <DMgr_hostName> <SOAP_PORT_of_DMGR> -username <username> -password <password>
  ~~~

