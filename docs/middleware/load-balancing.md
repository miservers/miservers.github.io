---
layout: default
title: Load Balancing
parent: Middleware
nav_order: 9
---


## mod_jk: Wildfly
**Environment**: Centos Stream 9, Wildfly 29, Httpd 2.4

[JBoss EAP 7 - Mod_JK](https://access.redhat.com/documentation/en-us/red_hat_jboss_enterprise_application_platform/7.4/html/configuration_guide/configuring_high_availability#mod_jk-config)

**install mod_jk** 

	$ yum install mod_jk
	$ ls /etc/httpd/modules

**Config File Samples**: under /etc/httpd/conf.d

	 mod_jk.conf.sample
	 uriworkermap.properties.sample
	 workers.properties.sample

{: .error :}
> Error: ajp worker not working between apache and Wildfly/Tomcat.	
> Try `$ setenforce 0`


**Declare AJP Socket in Wildfly:**  

![alt](/docs/images/wildfly-29-sockets.png)

{: .note :}
in **full-ha-sockets** the port AJP is declared by default.


## Mod-Cluster
Env: Centos Stream 9, Wildfly 29, Httpd 2.4

	$ yum install mod_proxy_cluster


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


## Apache Reverse Proxy with mod_proxy
Apache reverse proxy is used as a bridge to access a service(port) via a domaine name. For example you can access the tomcat server http://tomcat1.domaine.com:8080 via the address http://www.domaine.com.

To configure it:

1. Enable Modules proxy and proxy_http

		 a2enmod proxy proxy_http
2. Create and enable this vhost : 
	
		<VirtualHost *:80>
		    ServerName prod.safar.com 
		    ServerAdmin postmaster@domaine.fr
		 
		    ProxyPass / http://192.168.56.101:8080/
		    ProxyPassReverse / http://192.168.56.101:8080/
		    ProxyRequests Off
		</VirtualHost>

3. Test http://prod.safar.com/examples/

Notes:

1. ProxyPass routes http requests to the tomcat server. ProxyPassReverse routes responses to the client.
2. Security: ProxyRequests must be set to Off to disable the proxy server.





## HAProxy
Install HAProxy

	apt install haproxy

/etc/haproxy/haproxy.conf 
```	
	frontend myfrontend
        bind *:80
        mode tcp
        default_backend my_backend
        option tcplog

	backend my_backend
        balance roundrobin
        mode tcp
        server server1 192.168.56.101:80 check
        server server2 192.168.56.102:80 check
```	

Start HAProxy:

	sudo systemctl start haproxy.service 

Access To the Site: http://www.safar.com:81/

## NGINX
Object: use Nginx as a reverse proxy in front of Tomcat

1. Install nginx

		apt install nginx

2. Get the conf template : tomcat-basic.conf

		cd /etc/nginx/conf.d
		curl https://www.nginx.com/resource/conf/tomcat-basic.conf > tomcat-basic.conf

3. Edit tomcat-basic.conf:

	```	
	upstream tomcat {
	    # Use IP Hash for session persistence
	    ip_hash;

	    # List of Tomcat application servers
	    server 192.168.56.101:8080;
	    server ub2:8080;
	}

	server {
	    listen 80;
	    server_name www.safar.com;

	    # Redirect all HTTP requests to HTTPS
	    location / {
	        return 301 https://$server_name$request_uri;
	    }
	}
	 
	server {
	    listen 443 ssl http2;
	    server_name www.safar.com;

	    ssl_certificate     /etc/nginx/ssl/my-certificate.pem;
	    ssl_certificate_key /etc/nginx/ssl/my-privatekey.pem;

	    ssl_session_cache   shared:SSL:1m;
	    ssl_prefer_server_ciphers on;

	    # Load balance requests for /examples/ across Tomcat application servers
	    location /examples/ {
	        proxy_pass http://tomcat;
	        proxy_cache backcache;
	    }

	    # Return a temporary redirect to the /examples/ directory 
	    # when user requests '/'
	    location = / {
	        return 302 /examples/;
	    }
	}
	```

3. Generate a self signed certificate under /etc/nginx/ssl
	
		openssl req -newkey rsa:4096  -x509  -sha512  -days 365 -nodes -out my-certificate.pem -keyout my-privatekey.pem

4. Start Nginx

		systemctl restart nginx

5. Test https://www.safar.com/ 


## HeartBeat

