---
layout: default
title: Mod-jk / Tomcat
parent:  Load Balancing
grand_parent: Middleware
nav_order: 1
---

## Mod_Jk : Tomcat
Env: Ubuntu 

See : https://tomcat.apache.org/connectors-doc/webserver_howto/apache.html

**1. Install Apache JK Module On ubuntu**
```sh
	sudo apt search libapache2-mod | grep jk
	sudo apt install libapache2-mod-jk
	apache2ctl -M  # show installed modules
```

**2. Configure Apache to Use mod_jk**

Check if JK module installed and Enabled: These Configutation files are automatiquely created by the apt install. 

/etc/apache2/mods-available/jk.load

	LoadModule jk_module /usr/lib/apache2/modules/mod_jk.so

/etc/apache2/mods-available/httpd-jk.conf

	<IfModule jk_module>
	    JkWorkersFile /etc/libapache2-mod-jk/workers.properties
	    JkLogFile /var/log/apache2/mod_jk.log
	    JkLogLevel info

	    <Location /jk-status>
	        JkMount jk-status
	        Require ip 127.0.0.1
	    </Location>
	    <Location /jk-manager>
	        JkMount jk-manager
	        Require ip 127.0.0.1
	    </Location>

	    
	    JkMount /myapp|/* balancer

	    # UnMounting requests for all workers
	    JkUnMount /myapp/static/* *

	</IfModule>

**3. Configure workers.properties**

	worker.list=worker1
	worker.worker1.port=8009
	worker.worker1.host=localhost
	worker.worker1.type=ajp13
	# Low lbfactor means less work done by the worker.
	worker.worker1.lbfactor=50

	worker.loadbalancer.type=lb
	worker.loadbalancer.balance_workers=worker1


**4. Configure Tomcat to use mod_jk**
server.xml

    <Connector protocol="AJP/1.3"
               address="::1"
               port="8009"
               redirectPort="8443" />


### jvmRoute  
Located in server.xml, it is used by the load balancer to enable session affinity. Il must be unique accros tomcat instances..

