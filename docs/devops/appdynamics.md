---
layout: default
title: AppDynamics
parent: DevOps
nav_order: 5
has_toc: true
---
Env: RHEL 7

## Concepts:
--------------------------------------------------------
- Entreprise Console: aka Plateform Admin
- Controller: aka AppDynamic Plateform
- **Agent**: an Agent is installed in the Application to be monitored.It collects the performance metrics and sends them to the **Controller**.

## Appdynamics Trial
--------------------------------------------------------
There are two modes of appdynamics offering: SaaS and Local installation.

SaaS:
- Create a account on https://www.appdynamics.com/free-trial
- This offer an SAAS Controller
- Account All Infos here: https://accounts.appdynamics.com/overview
- Access to the Controller: https://data2024xxxxxxx.saas.appdynamics.com/controller/

For local installation:
- You must install Entreprise Console, then then the controller

## Java Agent
-------------------------------------------------
- Download and Unzip the Java Appserver Agent


- Edit **controller-info.xml**: under agent_dir/conf/ or agent_dir/ver24.3.0.35708/conf/ 
  - controller-host / controller-port – IP/Port of the AppDynamics Controller. Default port is 8090.
  - application-name – Business Application name. This is the highest level of organization of monitoring Metrics,
  - tier-name – Specific subsystem of the Application (for example, front-end)
  - node-name – the host that is running the JVM
  - account-name, account-access-key

!! Note!! 
> APPSERVER_AGENT_HOME/conf/controller-info.xml or APPSERVER_AGENT_HOME/ver24.3.0.35708/conf/controller-info.xml. It depends on with version used. 

> All these info ca be found on the <a>https://accounts.appdynamics.com/overview</a> or On the Appdynamics Entreprise console:  

**Logs**:
  
  - agent_dir/ver24.3.0.35708/logs/node_name/agent.xxxx.log

### String Boot Application


- Edit **controller-info.xml** : 

    ~~~xml
    <controller-host>data2024xxxxxx.saas.appdynamics.com</controller-host>
    <controller-port>443</controller-port>
    <controller-ssl-enabled>true</controller-ssl-enabled>
    <application-name>sample-spring-boot</application-name>
    <tier-name>safar</tier-name>
    <node-name>rhel3</node-name>
    <account-name>data2024xxxxxxx</account-name>
    <account-access-key>xxxxxxxxxx</account-access-key>
    ~~~
- Or with System Properties:
  
    ~~~sh
    java -javaagent:/opt/appdynamics/appserver-agent/ver24.3.0.35708/javaagent.jar -Dappdynamics.controller.hostName=data202404240311179.saas.appdynamics.com -Dappdynamics.controller.port=443 -Dappdynamics.agent.applicationName=MemoryLeakExample -Dappdynamics.agent.tierName=Tests  -Xmx1024m MemoryLeakExample
    ~~~

- Start Application

  ~~~sh
  java -javaagent:/opt/appdynamics/appserver-agent/javaagent.jar -jar /opt/sample-spring-boot.jar
  ~~~

{: .note }
Agent conf directory set to [/opt/appdynamics/appserver-agent/ver24.3.0.35708/conf]


###  Websphere App Server
- add to **server.policy** under /opt/IBM/WebSphere/AppServer/profiles/AppSrv01/properties
  
  ~~~ 
  grant codeBase "file:/opt/appdynamics/appserver-agent/ver24.3.0.35708/-" { permission java.security.AllPermission; };
  ~~~

- On Console <a>servers > server1 > Performance Monitoring Infrastructure (PMI)</a>
  - **Enable Performance Monitoring Infrastructure**
  - set **Currently monitored statistic** set other than None

- Go to <a> servers > server1 > Process definition > Java Virtual Machine</a>
- Enter in **Generic JVM arguments**
   
   ~~~
   -javaagent:/opt/appdynamics/appserver-agent/javaagent.jar
   ~~~

### Configure Agent
On Controller console: <a>Applications > app_name > Tiers&nodes > node_name > Agents </a> then click on **configure**
![a](/docs/images/appdynamics-agent-configure.png)

## Monitor Critical Metrics
---------------------------------------------------------
### Throughput 
throughput named **Load** : debit. nb the calls to the application in a given time.
### Response Time
![a](/docs/images/appdynamics-load.png)

### Java Heap utilisation
![a](/docs/images/appdynamics-jvm-heap.png)
![a](/docs/images/appdynamics-jvm-heap-2.png)
![a](/docs/images/appdynamics-jvm-heap-3.png)

### Slow Response Time
![a](/docs/images/appdynamics-slow-response.png)

### Database Response Time
### Slowest Databse calls
### GC 

## Troubleshooting Java Memory
--------------------------------------------------------
1. Automatic Leak Detection
2. Objet Instance Tracking

### Automatic Leak Detection
Automatic Leak Detection uses On Demand Capture Sessions to capture any actively used collections (i.e. any class that implements JDK 'Map' or 'Collection' interface) during the 'Capture' period (default is 10 minutes). 
![a](/docs/images/appdynamics-memory-leak.png)

### Objet Instance Tracking
1. Excessive number of objects of certain class
2. Objects with unusually large size

## Install Enterprise Console (Platform Admin)
--------------------------------------------------------
### Requirements
- Open file descriptor limit (nofile): 65535
- Process limit (nproc): 65535

~~~sh
vi /etc/security/limits.conf

<user> hard nofile 65535
<user> soft nofile 65535
<user> hard nproc 65535
<user> soft nproc 65535 
~~~

Packages needed:
~~~sh
yum install libaio numactl ncurses-libs.x86_64 libaio.x86_64 numactl.x86_64 tzdata tar -y
~~~


### Install the Console
~~~sh
sudo su
chmod +x ./platform-setup-x64-linux-24.2.1.10054.sh 

./platform-setup-64bit-linux.sh
~~~

## Appdynamics Entreprise Console 
--------------------------------------------------------
### Start the Console
~~~sh
platform-admin/bin/platform-admin.sh start-platform-admin
~~~

### Console Url  
<a>https://localhost:9191</a>

  - login: admin


##  Controller
--------------------------------------------------------
### Requirements bypasse
For Demo, Edit:  platform-admin/archives/controller/24.2.1-10085/playbooks/controller-demo.groovy
~~~
controller_min_ram_in_mb = 3 * 1024
controller_min_cpus = 2
controller_data_min_disk_space_in_mb = 50 * 1024
remote_controller_min_ram_in_mb = 3 * 1024
remote_controller_min_cpus = 2
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

### Start Controller
~~~sh
 ./platform-admin.sh start-controller-appserver --platform-name appDPlatform1
~~~

### Controller Console
<a>http://rhel1:8090</a>

### Remove a controller
~~~sh
./platform-admin.sh submit-job --job remove --service controller --args removeBinaries=false
~~~

## Machine Agent
---------------------------------------------
### Configure conf/controller-info.xml

### Account Access Key
The account access key used to authenticate with the Controller. Located in the Controller Settings. See Observe License Usage.

Element in controller-info.xml:  <account-access-key>

System Property: -Dappdynamics.agent.accountAccessKey

You can find this value on http://rhel1:8090/controller then  `Settings > Licence > Account > Access Key`

### Start Machine Agent
~~~sh
cd /opt/appdynamics/machineagent

jre/bin/java -jar machineagent.jar
~~~

## Event Service
--------------------------------------------
### Requirements
1524Mo of free RAM for Dev!!!. Stop the Controller to avoid fail checks on RAM!!!

### Install by cli
~~~sh
./platform-admin.sh submit-job  --service events-service --job install --target-version latest --args profile=dev serviceActionHost=rhel1 --platform-name appDPlatform1
~~~

bin/platform-admin.sh install-events-service --profile dev --hosts 192.168.56.22 --data-dir /opt/appdynamics/eventsservice --platform-name controller1


Error: Connection to [http://rhel2:9080/_ping] failed:
- add the event service machine to /etc/hosts file
- use only IP, not hostname in the command
- changed every hostname to IP in the **conf/events-service-api-store.properties**

### Start Event Service by CLI
~~~sh
./platform-admin.sh submit-job --platform-name <platform_name> --service events-service --job start
~~~

## Enterprise Console Command Line
--------------------------------------------------
### Variable APPD_CURRENT_PLATFORM 
set environment variable `APPD_CURRENT_PLATFORM` to avoid   `--platform-name` param at evry command.

### Syntax
~~~sh
./platform-admin.sh [-h] [platform cmd] ...
~~~
Plateform Commands:
  - create-platform
  - list-platforms
  - change-password: Changes the Enterprise Console password
  - ...

~~~sh
platform-admin.sh [host cmd] ...
~~~
Host commands:
  - add-credential, list-credentials
  - add-hosts, remove-hosts
  - list-hosts

~~~sh
platform-admin.sh [-h] [product cmd] ...
~~~
Product Commands:
  -  submit-job, list-jobs, ...

~~~sh
bin/platform-admin.sh -h
~~~



### Remove a Host
~~~sh
./platform-admin.sh remove-hosts --platform-name controller1 --force --hosts rhel1
~~~




## Errors
--------------------------------------------------
1. No current working platform set

~~~sh
./platform-admin.sh list-supported-services

WARNING: no current working platform set. Ensuing commands may fail!
Error code 400
Message: Invalid platform provided.
~~~

Solution set variable APPD_CURRENT_PLATFORM or  --platform-name param:

~~~sh
 ./platform-admin.sh --platform-name controller1 list-supported-services
~~~


## Docs
- Excellent blog: <a>http://karunsubramanian.com/category/appdynamics/</a>
- <a>https://github.com/sherifadel90/AppDynamicsPlatformInstallation</a>
- <a>https://docs.appdynamics.com/appd/onprem/23.x/latest/en/events-service-deployment/install-the-events-service-on-linux</a>
- <a>https://community.appdynamics.com/t5/Business-iQ-Analytics/Starting-Events-Service-cluster/m-p/44127</a>
