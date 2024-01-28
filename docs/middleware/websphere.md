---
layout: default
title: Websphere
parent: Middleware
nav_order: 3.5
---

**Environment**: Linux,  WebSphere Application Server ND v9

## Terminology
----------------------------------
- **package**: Entity that Installation Manager installs.
- **Repository**: directory containing IBM packages and defined by its **repository.config**.  
  - ESD-Electronic Software Delivery: packages downlowed from Passport Advantage or Fix Central.It can only be accessed by local file or ftp. 
  - HTTP: remote from ibm.com. Or downloaded by IBM Packaging Utility and served by an http server. 
- **APAR**, Authorized Program Analysis Report: describe a problem found in an IBM product.
- **Fix Pack**: is a cumulative collection of APAR fixes.


## Installation Manager
----------------------------------
v 1.9 

- [x] [Documentation](https://www.ibm.com/docs/en/installation-manager/1.9.2)

### Installation
IBM Installation Manager is an utility to install and apply Fix Packs for IBM softwares. You can install it as Root, User or Group.  **v.1.9** 

	./install     // install as root	
	./userinst   // as user
	./groupinst

### Installation of IM in Silent Mode
Fist unzip IM software.
- **Install as root**
	```sh
	$ ./installc -installationDirectory /opt/IBM/InstallationManager/eclipse \
	   -dL /var/ibm/InstallationManager -acceptLicense -sVP -showProgress
	```
- **Install as user**
	```sh
	$ ./userinstc -installationDirectory /opt/IBM/InstallationManager/eclipse \
	   -dL /var/ibm/InstallationManager -acceptLicense -sVP -showProgress
	```


Default Locations:
```conf
Default installation directory: -installationDirectory
	root : /opt/IBM/InstallationManager/eclipse
	 /<user/IBM/InstallationManager/eclipse
Default agent data location: -dL
	root: /var/ibm/InstallationManager
	user: /<user>/var/ibm/InstallationManager
Log file:
	/var/ibm/InstallationManager/pluginState/.metadata
```

### Working in wizard mode

  ![alt](/docs/images/ibm-installation-manager.png)

Add **Repositories** in _File>Preferences>Repositories_. Here you find Repositories to install Websphere AppServer [Websphere App Server Repositories](https://www.ibm.com/docs/en/was/9.0.5?topic=installation-online-product-repositories-websphere-application-server-offerings)

### Working form command line: imcl
the repository was created on the staging machine via the Packaging Utility tool.

- **Listing available packages**
	```sh
	$ cd /opt/IBM/InstallationManager/eclipse/tools/
	$ ./imcl listAvailablePackages -repositories http://ibm-file-server.safar.ma/repository.config -features -long
	```

	This repositry was dowloaded by [Packaging Utility](#packaging-utility) and  is accessible by http through [Nginx](/docs/middleware/nginx/#nginx-as-a-static-file-server).

- **Install Packages**
	```sh
	$ ./imcl install com.ibm.websphere.ND.v90_9.0.5016.20230609_0954 com.ibm.java.jdk.v8_8.0.8015.20231031_0036 \
		-repositories http://ibm-file-server.safar.ma/repository.config \
		-installationDirectory /opt/IBM/WebSphere/AppServer -acceptLicense -showProgress
	```

	{: .warning :}
	You must Install the WAS and the JDK simultaneously, both by one command imcl

- **Uninstall Packages**
	```sh
	$ ./imcl uninstall com.ibm.websphere.ND.v90_9.0.5016.20230609_0954 com.ibm.java.jdk.v8_8.0.8015.20231031_0036 \
		-installationDirectory /opt/IBM/WebSphere/AppServer -showProgress
	```

### Working in Silent mode
To use silent mode, you must create a **response file** through Installation Manager or  by hand.

## Packaging Utility
------------------------
**IBM Package Utility** is a tool to copy packages(from ibm.com) into repositories for consumption by **Installation Manager**. It can also copy packages from ibm repositories to local disk so Installation Manager can install them using local disk, ftp, http access.

![alt](/docs/images/ibm-packaging-utility-2.png)

**Install It**: donwload it and unzip it

	./install     // install it as root	
	./userinst   // as user
	./groupinst

Screens:

![a](/docs/images/ibm-packaging-utility-main.png)
![b](/docs/images/ibm-packaging-utility-copy.png)

### IBM Repositories
- [Trial WAS Repositories](https://www.ibm.com/docs/en/was/9.0.5?topic=installation-online-product-repositories-websphere-application-server-offerings)

### Provisioning Staging Machine
For provisioning the Adminitrator Staging Machine: 
- install the Packaging Utility to create local **repositories** used to deploy the packages on target machines. 
- Use Http/Https: you should setup an http server. Example here by [nginx](/docs/middleware/nginx/#nginx-as-a-static-file-server)
- Optionaly you can use Network Share or FTP to access the repository instead of http

### Provisioning the Target Machine
First, install the Installation Manager on the target machine

Second, install the packages using the installation Manager. Different modes can be used: graphic, console, command, silent.

## WebSphere App Server
--------------------------------------
### WAS Concepts
![was-concepts](/docs/images/websphere_app_server_concepts.png)

- **Profile**: is basicaly a template of an app server. There are two main types of profiles; **default** profile for servers running applications, and **dmgr** profile for the Deployment Manager.

- **Cell**: is a group of managed **nodes** that are federated to the same **deployement manager**.

### WAS Installation

- [x] [websphere trial options and downloads](https://www.ibm.com/blog/websphere-trial-options-and-downloads/)

Using **imcl** . The **repository** used here was created on the staging machine via the [Packaging Utility](#packaging-utility) tool. 

- **Listing available packages**
	```sh
	$ ./imcl listAvailablePackages -repositories http://ibm-file-server.safar.ma/repository.config -features -long
	```

	This repositry was dowloaded by Packaging Utility and  is accessible by http through [Nginx](/docs/middleware/nginx/#nginx-as-a-static-file-server).

- **Install Packages: WAS and JDK**
    Create a user e.g **wasadmin**
	```sh
	$ su - wasadmin
	$ cd /opt/IBM/InstallationManager/eclipse/tools/
	$ ./imcl install com.ibm.websphere.ND.v90_9.0.5016.20230609_0954 com.ibm.java.jdk.v8_8.0.8015.20231031_0036 \
		-repositories http://ibm-file-server.safar.ma/repository.config \
		-installationDirectory /opt/IBM/WebSphere/AppServer -acceptLicense -showProgress
	```

	{: .warning :}
	You must Install the WAS and the JDK simultaneously, both by one command imcl


- **Check Version**
	```sh
	$ /opt/IBM/WebSphere/AppServer/bin/versionInfo.sh
	```

- **Environment Variables**: to be added to your .bash_profile

	WAS_INSTALL_ROOT=/opt/IBM/WebSphere/AppServer

### Profiles
- **Create Managment Profile**
	```sh
	$ ./manageprofiles.sh -create -templatePath /opt/IBM/WebSphere/AppServer/profileTemplates/management -profileName dmgr
	```


	The profile will be created here: */opt/IBM/WebSphere/AppServer/profiles/dmgr*

- **Start/Stop DMGR**
	```sh
	$ cd /opt/IBM/WebSphere/AppServer/profiles/dmgr/bin
	$ ./startManager.sh
	```
- **Stop Manager**
	```sh	
	$ ./stopManager.sh -user admin -password changeit
	```
	
	{: .warning :}
	For security, it is highly unrecommanded to use password in clear. To disable Prompt for user/password you can modify **/opt/IBM/WebSphere/AppServer/profiles/dmgr/properties/soap.client.props**:  
	com.ibm.SOAP.loginUserid=admin  
	com.ibm.SOAP.loginPassword=changeit

- **Create an Managed Server Profile**
	```sh
	${WAS_INSTALL_ROOT}/bin/manageprofiles.sh -create -profileName AppSrv02
	```
	More Options [Here](https://www.freekb.net/Article?id=1296)

### Ports/Firewall
If there is a firewall between the DMGR and any Node Agent, you must open the   *SOAP_CONNECTOR_ADDRESS* ports (default 8879) and *CELL_DISCOVERY_ADDRESS* ports(default 7277).

Theses Ports can be found here : *WAS_HOME/profiles/dmgr/config/cells/cell-name/nodes/node-name/serverindex.xml*

### Administration Console
- **Console URL**: <a>http://host:9060/ibm/console</a> or <a>https://host:9043/ibm/console</a>

- **Find the Administration Port number**   
  Find theses lines in : */opt/IBM/WebSphere/AppServer/profiles/dmgr/logs/AboutThisProfile.txt*
  ```conf
  Administrative console port: 9060
  Administrative console secure port: 9043
  Management SOAP connector port: 8879
  ```

- **Enable Admin Console Security**: Enable HTTPS and User/Password authentication

  From Console : <a>security > Global security > Clic: Security configuration Wizard </a>

  ![console](/docs/images/was_console_security.png)

  Select **Federated repositories** as user repository, and create a user **admin**.

  You can chose  User repository from :
  - Federated repositories: users/passwords stored in local file.
  - LDAP 
  - Local OS users: if the WAS is run as root  

### IVT - Installation Verification Tool
IVT is used to verify that you have successfully installed a product.
```sh
~ ${WAS_INSTALL_ROOT}/bin/ivt.sh server_name profile_name
```

### Federate a Node: addNode
addNode is used to federate a node to the DMGR. addNode script is invoked from the node that you want to federate. Management SOAP  port (default 8879) is used to connect to the DMGR.  
**TODO**
https://www.freekb.net/Article?id=1544

Below, dmgr is running on centos1. the node to be federated is centos2.

Do on Centos2
:
  - Installation Manager must be installed under wasadmin user.
  - WAS must be installed.
	
  - Create a managed server profile using *manageprofiles* script.
  - Create a dummy node using *addNode* script. If the the node is previously created, add option *-noagent* to addNode. That also federate the node to the dmgr.
	
	```sh
	${WAS_INSTALL_ROOT}/profiles/AppSrv02/bin/addNode.sh dmgr_host dmgr_soap_port_8879 -includeapps
	```

### Nodes
- **Start a Node Agent**
	```sh
	${WAS_INSTALL_ROOT}/profiles/AppSrv02/bin/startNode.sh
	```
### Synchronisation
N.B : install Websphere as root make a problem of synchrinisation when Globlal security is enabled.
- From Web Console
- **Manually synchronize the node**  
  Stop Node, and run syncNode script.
  ```sh
  $WAS_INSTALL_ROOT/profiles/AppSrv02/bin/syncNode.sh <DMgr_hostName> <SOAP_PORT_of_DMGR> -username <username> -password <password>
  ```

## Applications
--------------------------------
- **Default Application Sample**: /opt/IBM/WebSphere/AppServer/installableApps/DefaultApplication.ear
	- Snoop servlet : http://centos2:9081/snoop
	- http://centos2:9081/HitCount.jsp


## WSADMIN Scripting
--------------------------------
- **Disable Administrative Security**: username/password will no longer  be demanded to login.
	```sh
	$WAS_INSTALL_ROOT/bin/wsadmin.sh -conntype NONE -lang jython
	wsadmin>securityoff()
	wsadmin>exit
	```

## IHS
--------------------------------
IBM HTTP Server is an apache httpd server modified by IBM.

TODO https://webspherejungle.blogspot.com/2018/03/configure-plugin-with-ibm-http-server.html

- **Repository** :
	- https://www.ibm.com/software/repositorymanager/com.ibm.websphere.IHS.v90
	- https://www.ibm.com/software/repositorymanager/com.ibm.websphere.PLG.v90

- **Installatio of IHS**: 
	```sh
	$ cd /opt/IBM/InstallationManager/eclipse/tools/
	$ ./imcl install com.ibm.websphere.IHS.v90_9.0.5016.20230609_0954 com.ibm.java.jdk.v8_8.0.8015.20231031_0036 \
		-repositories http://ibm-file-server.safar.ma/repository.config \
		-installationDirectory /opt/IBM/IHS -acceptLicense   -showProgress
	```

## Docs
- [Excellent Articles on the Installation Manager](https://www.ibm.com/docs/en/installation-manager/1.9.2?topic=manager-enterprise-installation-articles)
- [WAS ND 9.0 Docs](https://www.ibm.com/docs/en/was-nd/9.0.5)
- [Blog javaee.goffinet.org](https://javaee.goffinet.org/was-06-taches-administratives/)
- [Blog websphereknowledge](https://websphereknowledge.blogspot.com/)
- [Excellent Blog: freekb](https://www.freekb.net/Articles?tag=IBM%20WebSphere)
- [x] [websphere trial options and downloads](https://www.ibm.com/blog/websphere-trial-options-and-downloads/)
- [x] [Websphere App Server Repositories](https://www.ibm.com/docs/en/was/9.0.5?topic=installation-online-product-repositories-websphere-application-server-offerings)
- [x] [Websphere Liberty Repositories](https://www.ibm.com/support/knowledgecenter/SSEQTP_liberty/com.ibm.websphere.wlp.nd.multiplatform.doc/ae/cwlp_ins_repositories.html)
