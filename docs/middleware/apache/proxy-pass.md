---
layout: default
title: ProxyPass
parent:  Apache
grand_parent: Middleware
nav_order: 3.5
---


- **ProxyPass**: commonly used to forward client requests to backend servers. and return responses to the client.

- **ProxyPassReverse**: it modify the response header sent by the backend server to match the reverse proxy server. in fact the response header may contain url/domain of the backend server. so it rewrite it before to send the response to the client.

- **ProxyRequests**: enable/disable the function of reverse proxy. must be disabled par SECURITY.

~~~xml
<VirtualHost *:80>
    ServerName app.example.com
    
	ProxyPreserveHost On
    ProxyPass / http://server:8081
    ProxyPassReverse / http://server:8081
	ProxyRequests Off

	ProxyPass /static/ !

    Alias /static/ "/apache/www/"

</VirtualHost>
~~~

<Location /jira>
  ProxyPreserveHost On
  ProxyPass http://jiraserver/jira
  ProxyPassReverse http://jiraserver/jira
  ProxyRequests Off
</Location>

~~~xml
<VirtualHost *:80>
	<Proxy balancer://mycluster>
	    BalancerMember http://127.0.0.1:8080
	    BalancerMember http://127.0.0.1:8081
	</Proxy>
    ProxyPreserveHost On
    ProxyPass / balancer://mycluster/
    ProxyPassReverse / balancer://mycluster/
	ProxyRequests Off
</VirtualHost>
~~~


~~~xml
ProxyPass / ajp://localhost:8009/
ProxyPassReverse / ajp://localhost:8009/
~~~