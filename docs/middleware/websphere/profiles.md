---
layout: default
title: Profiles
parent: WebSphere
grand_parent: Middleware
nav_order: 2
---

### Concepts 
- **Profile**: is basicaly a template of an app server. There are two main types of profiles; **default** profile for servers running applications, and **dmgr** profile for the Deployment Manager.

### Create a managment profile: DMGR

~~~sh
$ ./manageprofiles.sh -create -templatePath /opt/IBM/WebSphere/AppServer/profileTemplates/management -profileName dmgr
~~~


The profile will be created here: */opt/IBM/WebSphere/AppServer/profiles/dmgr*

### Create a managed server profile

~~~sh
${WAS_INSTALL_ROOT}/bin/manageprofiles.sh -create -profileName AppSrv02
~~~
More Options [Here](https://www.freekb.net/Article?id=1296)


### manageprofiles command
Syntax:
~~~sh
./manageprofiles.sh -<mode> -<argument> <argument parameter>
~~~

modes: create, delete, listProfiles, validateRegistry, etc

!! NOTE !!: it is case sensitive, be sure that all argument and parameters are correct.

Depending on the operation that you want to perform with the manageprofiles command, you need to provide one or more of the following parameters: NOT COMPLETE list!
~~~sh
-adminPassword adminPassword
-adminUserName adminUser_ID
-appServerNodeName application_server_node_name
-backupProfile
-cellName cell_name (Optional Parameter)
-create
-defaultPorts
-delete
-dmgrAdminPassword password
-dmgrAdminUserName user_name
-dmgrHost dmgr_host_name (Optional Parameter)
-dmgrPort dmgr_port_number
-dmgrProfilePath dmgr_profile_path
-enableAdminSecurity true | false
-enableService true | false # [Linux]
-federateLater true | false
-getDefaultName
-getName
-hostName host_name
-isDefault
-isDeveloperServer
-listProfiles
-nodeDefaultPorts
-nodeName node_name
-nodePortsFile node_ports_file_path
-nodeProfilePath node_profile_path
-portsFile file_path (Optional Parameter)
-profileName profile_name
-profilePath profile_root
-response response_file
-restoreProfile
-securityLevel security_level
-serverName server_name
-serverType DEPLOYMENT_MANAGER | ADMIN_AGENT | JOB_MANAGER
-serviceUserName service_user_ID # [Linux]
-setDefaultName
-startingPort starting_port | -portsFile ports_file_path | -defaultPorts
-templatePath template_path
-validatePorts
-validateRegistry
-webServerCheck true | false
-webServerHostnamewebserver_host_name
-webServerInstallPath webserver_installpath_name
-webServerName webserver_name
-webServerPort webserver_port
-webServerType webserver_type
~~~

### Response file 
Create WAS Profile with response file. Every mode and argument of manageprofiles command can be used in response file.

Response file for deployment manager (dmgr.rsp)
~~~sh
create
profileName=Dmgr01
templatePath=/opt/IBM/WebSphere/AppServer/profileTemplates/cell/dmgr
nodeProfilePath=/opt/IBM/WebSphere/AppServer/profiles/Dmgr01
cellName=rhel2Cell01
nodeName=rhel2CellManager01
appServerNodeName=rhel2Node01
adminUserName=wasadmin
adminPassword=changeit
enableAdminSecurity=true
~~~

Response file for application server (appsvr.rsp)
~~~sh
create
profileName=AppSrv01
profilePath=/opt/IBM/WebSphere/AppServer/profiles/AppSrv01
templatePath=/opt/IBM/WebSphere/AppServer/profileTemplates/managed
nodeName=rhel3CellNode01
hostName=rhel3
dmgrHost=rhel2
dmgrPort=8879
dmgrAdminUserName=wasadmin
dmgrAdminPassword=changeit
~~~

Run below command to create profiles:

~~~sh
/opt/IBM/WebSphere/AppServer/bin/manageprofiles.sh -response dmgr.rsp
/opt/IBM/WebSphere/AppServer/bin/manageprofiles.sh -response appsvr.rsp
~~~

If succeed, the command output looks like:
~~~
INSTCONFSUCCESS: Success: Profile Dmgr01 now exists. Please consult /opt/IBM/WebSphere/AppServer/profiles/Dmgr01/logs/AboutThisProfile.txt for more information about this profile.
~~~

If failed: `INSTCONFFAILED: ...`


### List of profiles
~~~sh
/opt/IBM/WebSphere/AppServer/bin/manageprofiles.sh -listProfiles
~~~

### Delete a profile
~~~sh
/opt/IBM/WebSphere/AppServer/bin/manageprofiles.sh -delete -profileName AppSrvXY
~~~
