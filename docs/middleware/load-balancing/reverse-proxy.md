---
layout: default
title: Reverse Proxy
parent:  Load Balancing
grand_parent: Middleware
nav_order: 3
---

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




