---
layout: default
title: Weblogic
parent: Middleware
nav_order: 3
---

**Environment**: Weblogic 12c, Centos Stream 9

## Domain Concepts  
------------------------------------

![alt](/docs/images/weblogic-concepts.gif)

- [x] [Weblogic Documentation](https://docs.oracle.com/middleware/1212/wls)
- [x] [See This Blog](https://middlewareadmin-pavan.blogspot.com/2021/01/weblogic-14c-horizontal-cluster-setup.html
)


## Installation
------------------------------------

### Installation: Silent

- [x] [Silent Installation](https://oracle-base.com/articles/12c/weblogic-silent-installation-12c)

Create a new group and user.

~~~sh
$ groupadd  oinstall
$ useradd  oracle -g oinstall 
$ passwd oracle
~~~

Create the directories:

~~~sh
$ mkdir -p /u01/app/oracle/middleware
$ mkdir -p /u01/app/oracle/config/domains
$ mkdir -p /u01/app/oracle/config/applications
$ mkdir -p /u01/software
$ chown -R oracle:oinstall /u01
$ chmod -R 775 /u01/
~~~

SetUp profile vars: /home/oracle/.bash_profile

	export MW_HOME=/u01/app/oracle/middleware
	export WLS_HOME=$MW_HOME/wlserver
	export WL_HOME=$WLS_HOME
	export DOMAIN_HOME=$MW_HOME/user_projects/domains/myDomain

	export JAVA_HOME=/opt/jdk1.8.0_381
	export PATH=$JAVA_HOME/bin:$PATH

Create [Response File](https://docs.oracle.com/middleware/1212/core/OUIRF/response_file.htm#OUIRF391):   **/u01/software/wls.rsp**


	[ENGINE]
	Response File Version=1.0.0.0.0
	[GENERIC]
	ORACLE_HOME=/u01/app/oracle/middleware
	INSTALL_TYPE=WebLogic Server
	MYORACLESUPPORT_USERNAME=
	MYORACLESUPPORT_PASSWORD=<SECURE VALUE>
	DECLINE_SECURITY_UPDATES=true
	SECURITY_UPDATES_VIA_MYORACLESUPPORT=false
	PROXY_HOST=
	PROXY_PORT=
	PROXY_USER=
	PROXY_PWD=<SECURE VALUE>
	COLLECTOR_SUPPORTHUB_URL=

Specify an Oracle inventory location: **/u01/software/oraInst.loc**

	inventory_loc=/u01/app/oraInventory
	inst_group=oinstall

WebLogic Silent Installation

~~~sh
$ $JAVA_HOME/bin/java -Xmx1024m -jar /opt/fmw_12.2.1.4.0_wls_lite_generic.jar -silent -responseFile /u01/software/wls.rsp -invPtrLoc /u01/software/oraInst.loc
~~~

### Patching WebLogic Server

- [x] See [This Blog](https://oracle-base.com/articles/12c/weblogic-silent-installation-12c#patching-weblogic-server)

### Uninstall Weblogic: Silent
	
	$ $MW_HOME/oui/bin/deinstall.sh -silent

## Domains
---------------------------------

### Create a Domain: GUI

~~~sh
$ $MW_HOME/oracle_common/common/bin/config.sh
~~~

This wizard can create AdminServer( port 7001), nodemanager, managed nodes

### Create a Domain: using WLST

- [x] See [This Article](https://docs.oracle.com/cd/E28280_01/install.1111/b32474/silent_install.htm#CHDGECID)

~~~sh
$ $MW_HOME/oracle_common/common/bin/wlst.sh create-domain-7001.py
~~~

**create-domain-7001.py**

~~~py
#!/usr/bin/python
import os, sys
readTemplate('/u01/app/oracle/middleware/wlserver/common/templates/wls/wls.jar')
cd('/Security/base_domain/User/weblogic')
cmo.setPassword('changeit1')
cd('/Server/AdminServer')
cmo.setName('AdminServer')
cmo.setListenPort(7001)
cmo.setListenAddress('centos1')
writeDomain('/u01/app/oracle/middleware/user_projects/domains/myDomain')
closeTemplate()
exit()
~~~

SetUp profile vars: /home/oracle/.bash_profile

	export DOMAIN_HOME=$MW_HOME/user_projects/domains/myDomain



### Create Clustered Domain

- [x] See [This Article](https://oracle-base.com/articles/12c/weblogic-12c-clustered-domains-1212#create-the-clustered-domain)

On **machine1**:

~~~sh
	$ cd $MW_HOME/oracle_common/common/bin
	$ ./pack.sh -managed=true -domain=$DOMAIN_HOME -template=${DOMAIN_HOME}-template.jar -template_name=myDomain
~~~

Transfer the generated jar to machine2:

	$ scp ${DOMAIN_HOME}-template.jar oracle@centos2:~/

On **machine2**:

1. Install Weblogic Software
2. Unpack the configuration

~~~sh
$ cd $MW_HOME/oracle_common/common/bin
$ ./unpack.sh -domain=$DOMAIN_HOME -template=/home/oracle/myDomain-template.jar
~~~

Start Weblogic on **machine1**

	$ $DOMAIN_HOME/startWebLogic.sh


On **machine2**:

- Enroll Second Machine

~~~py
connect('weblogic', 'Change_it', 't3://centos1:7001')

nmEnroll('/u01/app/oracle/middleware/user_projects/domains/myDomain', '/u01/app/oracle/middleware/user_projects/domains/myDomain/nodemanager')

disconnect()
exit()
~~~

- Check that  **$MW_HOME/domain-registry.xml** contains:

~~~xml
<domain location="/u01/app/oracle/middleware/user_projects/domains/myDomain"/>
~~~

-  Check **$DOMAIN_HOME/nodemanager/nodemanager.domains** contains:

		myDomain=/u01/app/oracle/middleware/user_projects/domains/myDomain


-  Edit **$DOMAIN_HOME/nodemanager/nodemanager.properties**

		ListenAddress=centos2	
		ListenPort=5556

-  Start NodeManager:

		$ nohup DOMAIN_HOME/bin/startNodeManager.sh > /dev/null 2>&1 &

- Add Machine2 on the Console

![alt](/docs/images/weblogic-12c-machines.png)



### Domain Tree
	DOMAIN_HOME/myDomain
		├── bin
		    ├── startManagedWebLogic.sh
		    ├── startNodeManager.sh
		    ├── startRSDaemon.sh
		    ├── startWebLogic.sh
		    └── stopWebLogic.sh
		├── config
		    ├── config.xml
		    ├── deployments
		    ├── jdbc
		    ├── nodemanager
		    └── security
		├── servers
		    ├── AdminServer
		    └── Server-0
		└── tmp
		    └── 3305975478340.lok


### Config Vars

	-Dweblogic.RootDirectory=path : root directory, contains config/config.xml, servers etc	 

## Start/Stop Weblogic
-------------------------------

~~~sh
$DOMAIN_HOME/bin/startNodeManager.sh
$DOMAIN_HOME/bin/startWebLogic.sh      // Start AdminServer
$DOMAIN_HOME/bin/stopWebLogic.sh
$DOMAIN_HOME/bin/startManagedWebLogic.sh <managedServer>
$DOMAIN_HOME/bin/stopManagedWebLogic.sh <managedServer>
~~~

## Console
---------------

### Url

 <a>http://centos1:7001/console</a>


### Change console/boot Password

Edit Boot Identity File: **$DOMAIN_HOME/servers/AdminServer/security/boot.properties**

    sername=weblogic
    password=Change_it

The first time the admin server start, it reads this file and overwrite it with encrypted username/password. 

## Configuration
-------------------------------

### Node Manager Properties   

Edit **$DOMAIN_HOME/nodemanager/nodemanager.properties**

	ListenAddress=centos1	
	ListenPort=5556

### Machines
You should define machines wich are controlled by Node Manager Processes

![alt](/docs/images/weblogic-12c-machines.png)


### JVM Options

	base_domain/startManagedWebLogic.sh
  
### Enable Production Mode
- Using Console :

![alt](/docs/images/weblogic-12c-production-mode.png)

### Logs

### Debugging Weblogic
see :  
https://docs.oracle.com/middleware/1212/wls/JDBCA/monitor.htm#JDBCA259  
http://weblogic-wonders.com/weblogic/2010/11/18/weblogic-server-debug-flags.


**Activate Debug SQL using JVM Options**  
```sh
-Dweblogic.debug.DebugJDBCSQL=true 
-Dweblogic.log.StdoutSeverity="Debug"
```
These debug flags are added in the JAVA_OPTIONS in the start script.  


**Activate Debug using WLST**
```sh
user='user1'
password='password'
url='t3://localhost:7001'
connect(user, password, url)
edit()
cd('Servers/myserver/ServerDebug/myserver')
startEdit()
set('DebugJDBCSQL','true')
save()
activate()
```

**Activate Debug using Console**  
![alt txt](/docs/images/weblogic-debug.png)

### Configuration des rôles et utilisateurs 
    Domain Structure > Security Realms > myrealm
    
    Onglet Users and Groups > Groups : add group « myAppUsers »

    Onglet Roles and Policies > Realm Roles :
    Domain > DName > Roles
    Créer rôle « myAppUsers »
    Dans « Domain Scoped Role Conditions » 
    Ajout de la condition Group : myAppUsers 

    Onglet Users and Groups > Users :
    Ajout de l’utilisateur  « safar »
    Saisie du mot de passe
    Affecter l’utilisateur au groupe « myAppUsers »

	Tous les autres paramètres du realm/group/user/role laissés par défaut.

## Deploy Applications
-------------------------------
How To Install an Application:
- Example [benefits.war](https://www.oracle.com/webfolder/technetwork/tutorials/obe/fmw/wls/12c/12_1_3/03/deployapps.html)
- Under Domain Structure, click **Deployments**. and follow screens 
- On the review screen, select **No, I will review the configuration later**.

- Activate Changes  
	![alt](/docs/images/weblogic-12c-deploy-app-change.gif)

- Start The Application  
	![alt](/docs/images/weblogic-12c-deploy-app-start.png)

- Test The Application <a>http://centos1:7010/benefits/</a>

## Apache/Weblogic 
-------------------------------
	<VirtualHost 10.0.0.52>
		ServerName www.app1.safar.com
		 <IfModule mod_weblogic.c>
			WebLogicCluster app1-wls1.safar.com:59105,app1-wls2.safar.com:59105
			<Location />
					SetHandler weblogic-handler
			</Location>
		</IfModule>
		ErrorLog /logs/apache/app1_error_log
		CustomLog /logs/apache/app1_access_log combined
	</VirtualHost>


## Tuning of Performances
-------------------------------
### Performance Metrics

1. JVM – Percent of time in Garbage Collection  
CG is a stop world 

2. Execute Thread Counts  

3. Workmanager Thread usage  

4. JDBC  
Current Capacity: pool saturation  
Current Capacity High  
Connection delay time: indicate database responsiveness  

Ref  
https://www.dynatrace.com/blog/top-10-weblogic-performance-metrics-proactively-monitor-server-farm/

### Tuning JDBC Pool

- Maximum Capacity
- Minimum Capacity : to be at least half (50%) of MAX so that the connection pool cannot shrink below this value.
  Used only for connection pool shrinking calculations.
- Initial Capacity : to be at least quarter (25%) of MAX. This is the initial number of connections 
  created when the application server is started
- Inactive Connection Timeout:
  Inactive connection in WebLogic Server will be releases and back into the connection pool if this value set 
  more than 0. Recommendation for this config is specific value in seconds, so if found leaked connections that
  were not correctly closed by the application will be handle via this feature.
- Shrink Frequency : (Harvest Interval) to 1800 (30 minutes). The number of seconds to wait before shrinking a 
  connection pool that has incrementally increased to meet demand. When set to 0, shrinking is disabled. 
  Shrinking means that WebLogic drop some connections from the data source when a peak usage 
  period has ended, freeing up WebLogic Server and DBMS resources. When set to 0, shrinking is disabled.
- Set Connection Creation Retry Frequency to 120 (2 minutes)
- Set Test Frequency to 120 (2 minutes). This is to poll the database to test the connection. This defaults 
  to “SELECT 1 FROM DUAL” which bypasses the buffer cache so it’s not bad.
- Set Seconds to trust an Idle Pool Connection to 10.
- Cache for prepared statements must be set to 20 or higher. Setting this higher should be discussed with your DBA. 
  The total number of cached cursors would be the cache setting*number of connections in pool*number of servers in cluster.   
  This should be set very carefully. That calulation equates to the number of open cursors allowed per session, so if it is set too low then cursors are repeatedly closed and opened.   
  This leads to excessive hard parsing of SQL statements which can also lead to performance degradation. 
  In fact “Bad Use of Cursors” is the number 2 point on the “Top Ten Mistakes” list, and it says that this has an order of magnitude impact in performance, and is totally unscalable.  
  
  ❗Be carefaul :  ORA-01000 maximum open cursors exceeded
    	
		sql > SELECT value FROM v$parameter WHERE name = 'open_cursors';



## WLDF

1. Copy of Console Jar

		$ cp $WL_HOME/server/lib/console-ext/diagnostics-console-extension.jar  $DOMAIN_HOME/console-ext 

2. Restart the Administration Server  
3. Activate Diagnostics Console Extension   
		
		On console: Preferences>Extensions>diagnostics-console-extension

Dashboard  <a>http://localhost:7001/console/dashboard</a>

Graphing Data With the Dashboard. you can access it from Home page.

  ![alt txt](/docs/images/Weblogic-Dashboard.png)



## WLST
```sh
$java -cp /opt/weblogic/wlserver/server/lib/weblogic.jar weblogic.WLST

Connect To Admin Server:
  wls:/offline> connect('weblogic','weblogic1', 't3://localhost:7001')
  
Runtime commands
  wls> domainRuntime()  
  wls> cd('ServerRuntimes/myServer1/JVMRuntime/myServer1')

Commands :
  wls> ls()
   
```





