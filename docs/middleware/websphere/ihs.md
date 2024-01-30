---
layout: default
title: IBM HTTP Server
parent: WebSphere
grand_parent: Middleware
nav_order: 4
---

### IHS - IBM HTTP Server
IBM HTTP Server is an apache httpd server modified by IBM.

![ihs](/docs/images/websphere-ihs-plugins.png)

- **Repository** :
	- https://www.ibm.com/software/repositorymanager/com.ibm.websphere.IHS.v90
	- https://www.ibm.com/software/repositorymanager/com.ibm.websphere.PLG.v90

### Installation of IHS
v 9.0

Installation of the IHS as user **wasadmin**.

```sh
$ cd /opt/IBM/InstallationManager/eclipse/tools/
$ ./imcl listAvailablePackages -repositories http://ibm-file-server.safar.ma/repository.config
```

```sh
$ ./imcl install com.ibm.websphere.IHS.v90_9.0.5016.20230609_0954 com.ibm.java.jdk.v8_8.0.8015.20231031_0036 \
	-repositories http://ibm-file-server.safar.ma/repository.config \
	-installationDirectory /opt/IBM/HTTPServer -sharedResourcesDirectory /opt/IBM/IMShared \
	-acceptLicense  -properties "user.ihs.httpPort=80,user.ihs.allowNonRootSilentInstall=true"  -showProgress
```

{: .note }
Because IBM Java SDK  is no longer embedded with the product, you must specify both the IHS ID and the IBM Java SDK ID.

### Start/Stop IHS
two methods:
1. via WAS console: you can administer the IHS through WAS Console using *node agent* or using *IBM HTTP Administration Server* on an umanaged node. 
2. via apachectl: as root if the http port is under 1024. 
   ```sh
   #  /opt/IBM/HTTPServer/bin/apachectl start
   ```   

### IBM HTTP Administration Server
WAS Console can administer the IHS using node agent on managed node. On an unmanaged node, WAS console uses the IHS Administration Server as an interface to administer the IHS.

{: .warning}  
Do not enable the IHS administration server in security-sensitive environments.

### Integrate IHS with WAS Console


1. **Install Web Server Plugings for the WAS**
    ```sh
	$ ./imcl install com.ibm.websphere.PLG.v90_9.0.5016.20230609_0954 com.ibm.java.jdk.v8_8.0.8015.20231031_0036\
		-repositories http://ibm-file-server.safar.ma/repository.config \
		-installationDirectory /opt/IBM/WebSphere/Plugins -acceptLicense   -showProgress
	```
2. On Websphere Console, Add New **Web Server**
  ![ihs](/docs/images/websphere-new-ihs-1.png)
  
- Generate then Propagate Plug-in
  ![ihs](/docs/images/websphere-new-ihs-propagate.png)
  
  The plug-in configuration file **plugin-cfg.xml** is copied  to /opt/IBM/WebSphere/Plugins/config/IHS-01/plugin-cfg.xml on the Web server computer.

- Add Plugin Config and Module WAS to IHS    
  two lines to add to **httpd.conf**:
  1. Load Module mod_was_ap22_http.so
  2. Add Plugin Config: plugin-cfg.xml
	```conf
	LoadModule was_ap24_module /opt/IBM/WebSphere/Plugins/bin/64bits/mod_was_ap24_http.so
	WebSpherePluginConfig /opt/IBM/WebSphere/Plugins/config/IHS-02/plugin-cfg.xml
	```
  3. Copy Kyes
    ```sh
	cp /opt/IBM/WebSphere/Plugins/etc/plugin-key* /opt/IBM/WebSphere/Plugins/config/IHS-02/          
    ```
  4. Create Plugins directories  
    ```sh 
	$ mkdir /opt/IBM/WebSphere/Plugins/logs/IHS-02
	```
	
- Install Default Application :  <a>/opt/IBM/WebSphere/AppServer/installableApps/DefaultApplication.ear</a>
  
  - Map modules to servers : IHS and WAS.  
    In order to have a context root accessible from the IHS, you must select the web server as target during deployment
    ![app](/docs/images/websphere-new-application.png)
  - Generate and Propagate the  Plugin

- Start The Application

- Virtual Hosts  

  You should readjust ports of the Alias of **default_host** virtual host. These are ports of both IHS and WAS.
  
  ![vhost](/docs/images/websphere-virtualhost.png)

- Restart the IHS and WAS
- Test: <a>http://centos2:8000/snoop</a>

### Logs

- Plugin Logs
  
  /opt/IBM/WebSphere/Plugins/logs/IHS-02/http_plugin.log
