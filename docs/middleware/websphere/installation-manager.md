---
layout: default
title: IBM Installation Manager
parent: WebSphere
grand_parent: Middleware
nav_order: 6
---

v 1.9 

## Terminology

- **package**: Entity that Installation Manager installs.
- **Repository**: directory containing IBM packages and defined by its **repository.config**.  
  - ESD-Electronic Software Delivery: packages downlowed from Passport Advantage or Fix Central.It can only be accessed by local file or ftp. 
  - HTTP: remote from ibm.com. Or downloaded by IBM Packaging Utility and served by an http server. 
- **APAR**, Authorized Program Analysis Report: describe a problem found in an IBM product.
- **Fix Pack**: is a cumulative collection of APAR fixes.




## Installation of IM: Gui
IBM Installation Manager is an utility to install and apply Fix Packs for IBM softwares. You can install it as Root, User or Group.  **v.1.9** 

	./install     // install as root	
	./userinst   // as user
	./groupinst

## Installation of IM: Silent 
Fist unzip IM software.
- **Install as root**
	```sh
	$ ./installc -installationDirectory /opt/IBM/InstallationManager/eclipse \
	   -dL /var/ibm/InstallationManager -acceptLicense -sVP -showProgress
	```
- **Install as user**
	```sh
	$ ./userinstc -installationDirectory /opt/IBM/InstallationManager/eclipse \
	   -dL ~/var/ibm/InstallationManager -acceptLicense -sVP -showProgress
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


## Working in wizard mode

  ![alt](/docs/images/ibm-installation-manager.png)

Add **Repositories** in _File>Preferences>Repositories_. Here you find Repositories to install Websphere AppServer [Websphere App Server Repositories](https://www.ibm.com/docs/en/was/9.0.5?topic=installation-online-product-repositories-websphere-application-server-offerings)

## Working form command line: imcl
the repository was created on the staging machine via the Packaging Utility tool.

### List Of Available Packages
```sh
$ cd /opt/IBM/InstallationManager/eclipse/tools/
$ ./imcl listAvailablePackages -repositories http://ibm-file-server.safar.ma/repository.config -features -long
```

This repositry was dowloaded by [Packaging Utility](#packaging-utility) and  is accessible by http through [Nginx](/docs/middleware/nginx/#nginx-as-a-static-file-server).


### Install Packages
```sh
$ ./imcl install com.ibm.websphere.ND.v90_9.0.5016.20230609_0954 com.ibm.java.jdk.v8_8.0.8015.20231031_0036 \
	-repositories http://ibm-file-server.safar.ma/repository.config \
	-installationDirectory /opt/IBM/WebSphere/AppServer -acceptLicense -showProgress
```

{: .warning :}
You must Install the WAS and the JDK simultaneously, both by one command imcl

### List Of Installed Packages
Installed Packages are list here: **/var/ibm/InstallationManager/installed.xml**

```sh
$ ./imcl listInstalledPackages  -features -long
```


### Uninstall Packages   
```sh
$ ./imcl uninstall com.ibm.websphere.ND.v90_9.0.5016.20230609_0954 com.ibm.java.jdk.v8_8.0.8015.20231031_0036 \
	-installationDirectory /opt/IBM/WebSphere/AppServer -showProgress
```

## Working in Silent mode
To use silent mode, you must create a **response file** through Installation Manager or  by hand.

### Record a Response File
Use a Test machine/Desktop to record an xml response file, 
~~~sh
cd /opt/IBM/InstallationManager/eclipse
./IBMIM -record was_nd_rsp.xml  -skipInstall /tmp/ibm_recordData
~~~

Follow the Installation Manager Wizard to simulate the packages installation. 

Thanks to `-skipInstall`, no packages will be installed. 

Here an example of response file: [a](./files/was_nd_rsp.xml)

### Install the WAS Silently
By using the above recorded response file:
~~~sh
./imcl input /path/to/was_nd_rsp.xml -acceptLicense -sVP -log /path/to/was_install.log }}
~~~

## Uninstall IM itself
To unistall Installation manager Or Packaging Utility:
~~~sh
./imcl listInstalledPackages

./imcl uninstall com.ibm.cic.packagingUtility_1.9.2006.20230925_1406

./imcl uninstall com.ibm.cic.agent_1.9.2006.20230925_1323
~~~


## Docs

- [x] [Documentation](https://www.ibm.com/docs/en/installation-manager/1.9.2)
