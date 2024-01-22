---
layout: default
title: Websphere
parent: Middleware
nav_order: 3.5
---

**Environment**: Linux,  WebSphere Application Server ND v9

## Terminology
- **package**: Entity that Installation Manager installs.

- **Repository**:  
  - ESD-Electronic Software Delivery: packages downlowed from Passport Advantage or Fix Central.It can only be accessed by local file or ftp.
  - HTTP 


## Installation Manager
------------------------
v 1.9 

- [x] [Documentation](https://www.ibm.com/docs/en/installation-manager/1.9.2)

### Installation
IBM Installation Manager is an utility to install and apply Fix Packs for IBM softwares. You can install it as Root, User or Group.  **v.1.9** 

	./install     // install as root	
	./userinst   // as user
	./groupinst

### Installation of IM in Silent Mode

	./installc -installationDirectory /opt/IBM/InstallationManager/eclipse -dL /var/ibm/InstallationManager -acceptLicense -sVP

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

- Listing available packages
```sh
$ cd /opt/IBM/InstallationManager/eclipse/tools/
$ ./imcl listAvailablePackages -repositories http://ibm-file-server.safar.ma/repository.config -features -long
```

	This repositry was dowloaded by [Packaging Utility](#packaging-utility) and  is accessible by http through [Nginx](/docs/middleware/nginx/#nginx-as-a-static-file-server).

- Install Packages
```sh
$ ./imcl install com.ibm.websphere.ND.v90_9.0.5016.20230609_0954 com.ibm.java.jdk.v8_8.0.8015.20231031_0036 -repositories http://ibm-file-server.safar.ma/repository.config -installationDirectory /opt/IBM/WebSphere/AppServer -acceptLicense 
```

	{: .warning :}
	You must Install the WAS and the JDK simultaneously, both by one command imcl


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

### Provisioning Staging Machine
For provisioning the Adminitrator Staging Machine: 
- install the Packaging Utility to create local **repositories** used to deploy the packages on target machines. 
- Use Http/Https: you should setup an http server. Example here by [nginx](/docs/middleware/nginx/#nginx-as-a-static-file-server)
- Optionaly you can use Network Share or FTP to access the repository instead of http

### Provisioning the Target Machine
First, install the Installation Manager on the target machine

Second, install the packages using the installation Manager. Different modes can be used: graphic, console, command, silent.

## Webspehere
--------------------------------------
### WAS Concepts
![was-concepts](/docs/images/websphere_app_server_concepts.png)

- **Profile**: is basicaly a template of an app server. There are two main types of profiles; **default** profile for servers running applications, and **dmgr** profile for the Deployment Manager.

- **Cell**: is a group of managed **nodes** that are federated to the same **deployement manager**.

### Installation of Webspehere

- [x] [websphere trial options and downloads](https://www.ibm.com/blog/websphere-trial-options-and-downloads/)
- [x] [Websphere App Server Repositories](https://www.ibm.com/docs/en/was/9.0.5?topic=installation-online-product-repositories-websphere-application-server-offerings)
- [x] [Websphere Liberty Repositories](https://www.ibm.com/support/knowledgecenter/SSEQTP_liberty/com.ibm.websphere.wlp.nd.multiplatform.doc/ae/cwlp_ins_repositories.html)

Using **imcl** command of **Installation Manager** that must be previously installed. The packages can be accessed from remote ibm repositories or localy throughout Packaging Utility. In the example below the repository was created on the staging machine via the [Packaging Utility](#packaging-utility) tool.

- Listing available packages
```sh
$ ./imcl listAvailablePackages -repositories http://ibm-file-server.safar.ma/repository.config -features -long
```

	This repositry was dowloaded by Packaging Utility and  is accessible by http through [Nginx](/docs/middleware/nginx/#nginx-as-a-static-file-server).

- Install Packages
```sh
$ ./imcl install com.ibm.websphere.ND.v90_9.0.5016.20230609_0954 com.ibm.java.jdk.v8_8.0.8015.20231031_0036 \
	-repositories http://ibm-file-server.safar.ma/repository.config \
	-installationDirectory /opt/IBM/WebSphere/AppServer -acceptLicense 
```

	{: .warning :}
	You must Install the WAS and the JDK simultaneously, both by one command imcl



### Profiles
Create managment profile:

	./manageprofiles.sh -create -templatePath /opt/IBM/WebSphere/AppServer/profileTemplates/management -profileName dmgr

The profile will be created here:

	/opt/IBM/WebSphere/AppServer/profiles/dmgr



### Docs
- Excellent Articles:  https://www.ibm.com/docs/en/installation-manager/1.9.2?topic=manager-enterprise-installation-articles
- https://www.ibm.com/docs/en/was-nd/9.0.5
- https://javaee.goffinet.org/was-03-installation/
- https://websphereknowledge.blogspot.com/
