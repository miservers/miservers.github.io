---
layout: default
title: Installation
parent:  AppDynamics
grand_parent: DevOps
nav_order: 1
---

### Install the Console
~~~sh
sudo su
chmod +x ./platform-setup-x64-linux-24.2.1.10054.sh 

./platform-setup-64bit-linux.sh
~~~


### Install a Controller
1. create a platform
~~~sh
 ./platform-admin.sh create-platform --name appDPlatform1 --installation-dir /opt/appdynamics/appDPlatform/ 
~~~

2. Add Credientials
~~~sh
./platform-admin.sh add-credential --credential-name cred-rhel2 --type ssh --user-name root --ssh-key-file ~/.ssh/id_rsa --platform-name appDPlatform1 
~~~

3. Add Host 
~~~sh
./platform-admin.sh add-hosts --hosts rhel1 --credential cred-rhel2 --platform-name appDPlatform1 
~~~

Install the Controller on remote machine
~~~sh
./platform-admin.sh submit-job --service controller --job install --args controllerPrimaryHost=rhel1 controllerAdminUsername=admin controllerAdminPassword=p controllerRootUserPassword=p mysqlRootPassword=p --platform-name appDPlatform1 

platform-admin.sh submit-job --service controller --job install --args controllerPrimaryHost=<remotehost> controllerAdminUsername=<user1> controllerAdminPassword=<password> controllerRootUserPassword=<rootpassword> mysqlRootPassword=<dbrootpassword>

~~~



