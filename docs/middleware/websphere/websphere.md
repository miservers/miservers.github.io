---
layout: default
title: WebSphere App Server
parent: WebSphere
grand_parent: Middleware
nav_order: 1
---


**Environment**: Linux,  WebSphere Application Server ND v9

## Terminology
----------------------------------------------------------------------------------
- **package**: Entity that Installation Manager installs.
- **Repository**: directory containing IBM packages and defined by its **repository.config**.  
  - ESD-Electronic Software Delivery: packages downlowed from Passport Advantage or Fix Central.It can only be accessed by local file or ftp. 
  - HTTP: remote from ibm.com. Or downloaded by IBM Packaging Utility and served by an http server. 
- **APAR**, Authorized Program Analysis Report: describe a problem found in an IBM product.
- **Fix Pack**: is a cumulative collection of APAR fixes.




## WAS Concepts
----------------------------------------------------------------------------------
![was-concepts](/docs/images/websphere_app_server_concepts.png)

- **Profile**: is basicaly a template of an app server. There are two main types of profiles; **default** profile for servers running applications, and **dmgr** profile for the Deployment Manager.

- **Cell**: is a group of managed **nodes** that are federated to the same **deployement manager**.

## WAS Installation
----------------------------------------------------------------------------------

- [x] [websphere trial options and downloads](https://www.ibm.com/blog/websphere-trial-options-and-downloads/)

Using **imcl** . The **repository** used here was created on the staging machine via the [Packaging Utility](#packaging-utility) tool. 

- **Listing available packages**
	~~~sh
	$ ./imcl listAvailablePackages -repositories http://ibm-file-server.safar.ma/repository.config -features -long
	~~~

	This repositry was dowloaded by Packaging Utility and  is accessible by http through [Nginx](/docs/middleware/nginx/#nginx-as-a-static-file-server).

- **Install Packages: WAS and JDK**
    Create a user e.g **wasadmin**
	~~~sh
	$ su - wasadmin
	$ cd /opt/IBM/InstallationManager/eclipse/tools/
	$ ./imcl install com.ibm.websphere.ND.v90_9.0.5016.20230609_0954 com.ibm.java.jdk.v8_8.0.8015.20231031_0036 \
		-repositories http://ibm-file-server.safar.ma/repository.config \
		-installationDirectory /opt/IBM/WebSphere/AppServer -acceptLicense -showProgress
	~~~

	{: .note }
	Because IBM Java SDK  is not embedded with the product, you must specify both the WAS ID and the IBM Java SDK ID.

- **Check Version**
	~~~sh
	$ /opt/IBM/WebSphere/AppServer/bin/versionInfo.sh
	~~~

- **Environment Variables**: to be added to your .bash_profile

	WAS_INSTALL_ROOT=/opt/IBM/WebSphere/AppServer

## WAS Administration
----------------------------------------------------------------------------------
### Start/Stop

- **Start/Stop DMGR**
	~~~sh
	$ cd /opt/IBM/WebSphere/AppServer/profiles/dmgr/bin
	$ ./startManager.sh
	~~~
- **Stop Manager**
	~~~sh	
	$ ./stopManager.sh -user admin -password changeit
	~~~
	
	{: .warning :}
	For security, it is highly unrecommanded to use password in clear. To disable Prompt for user/password you can modify **/opt/IBM/WebSphere/AppServer/profiles/dmgr/properties/soap.client.props**:  
	com.ibm.SOAP.loginUserid=admin  
	com.ibm.SOAP.loginPassword=changeit

- **Start/Stop a Managed Server**
	~~~sh 
	$WAS_INSTALL_ROOT/profiles/AppSrv02/bin/startServer.sh server01
	~~~
### Ports/Firewall
If there is a firewall between the DMGR and any Node Agent, you must open the   *SOAP_CONNECTOR_ADDRESS* ports (default 8879) and *CELL_DISCOVERY_ADDRESS* ports(default 7277).

Theses Ports can be found here : *WAS_HOME/profiles/dmgr/config/cells/cell-name/nodes/node-name/serverindex.xml*

### Administration Console
- **Console URL**: <a>http://host:9060/ibm/console</a> or <a>https://host:9043/ibm/console</a>

- **Find the Administration Port number**   
  Find theses lines in : */opt/IBM/WebSphere/AppServer/profiles/dmgr/logs/AboutThisProfile.txt*
  ~~~conf
  Administrative console port: 9060
  Administrative console secure port: 9043
  Management SOAP connector port: 8879
  ~~~

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
~~~sh
~ ${WAS_INSTALL_ROOT}/bin/ivt.sh server_name profile_name
~~~

  
### Virtual Hosts
You should readjust ports of the Alias of **default_host** virtual host. These are ports of both IHS and WAS.
![vhost](/docs/images/websphere-virtualhost.png)


### Thread Dump
~~~ps
kill -3 SERVER_PID
~~~
Dump is generated here: /opt/IBM/WebSphere/AppServer/profiles/AppSrv01


## Applications
----------------------------------------------------------------------------------
- **Default Application Sample**: /opt/IBM/WebSphere/AppServer/installableApps/DefaultApplication.ear
	- Snoop servlet : http://centos2:9081/snoop
	- http://centos2:9081/HitCount.jsp


## WSADMIN Scripting
----------------------------------------------------------------------------------
- **Disable Administrative Security**: username/password will no longer  be demanded to login.
	~~~sh
	$WAS_INSTALL_ROOT/bin/wsadmin.sh -conntype NONE -lang jython
	wsadmin>securityoff()
	wsadmin>exit
	~~~

## Scripting Jython
----------------------------------------------------------------------------------
{: .warning }
**Jacl** has been deprecated!
### Scripts
Call a Script:
~~~sh
<profile_home>/bin/wsadmin.sh -f script.py
~~~

### Example of Scripts
- [Test Data Sources](/docs/middleware/websphere/scripts/testDS.py)
- [Deploy an Application](/docs/middleware/websphere/scripts/deployApp.py)

### Jython syntax


## Performance Monitoring Infrastructure (PMI)
----------------------------------------------------------------------------------
To enable Performance Monitoring Statistic:

- Under **Application servers** > <server_name> > **Performance Monitoring Infrastructure** (PMI), set  **Currently monitored statistic**.

## FixPacks
----------------------------------------------------------------------------------
- Version of the Fixpacks
	~~~sh
	./versionInfo.sh -fixpacks
	~~~

- Download The fixpack from [Fix Central](https://www.ibm.com/support/fixcentral)
- Apply the Fix using <a>imcl</a> command 


## Docs
----------------------------------------------------------------------------------
- [Excellent Articles on the Installation Manager](https://www.ibm.com/docs/en/installation-manager/1.9.2?topic=manager-enterprise-installation-articles)
- [WAS ND 9.0 Docs](https://www.ibm.com/docs/en/was-nd/9.0.5)
- [Blog javaee.goffinet.org](https://javaee.goffinet.org/was-06-taches-administratives/)
- [Blog websphereknowledge](https://websphereknowledge.blogspot.com/)
- [Excellent Blog: freekb](https://www.freekb.net/Articles?tag=IBM%20WebSphere)
- [x] [websphere trial options and downloads](https://www.ibm.com/blog/websphere-trial-options-and-downloads/)
- [x] [Websphere App Server Repositories](https://www.ibm.com/docs/en/was/9.0.5?topic=installation-online-product-repositories-websphere-application-server-offerings)
- [x] [Websphere Liberty Repositories](https://www.ibm.com/support/knowledgecenter/SSEQTP_liberty/com.ibm.websphere.wlp.nd.multiplatform.doc/ae/cwlp_ins_repositories.html)
