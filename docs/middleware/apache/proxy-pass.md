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

{: .warning }
Do not enable proxying until you have [secured your server](https://httpd.apache.org/docs/2.4/mod/mod_proxy.html#access). Open proxy servers are dangerous both to your network and to the Internet at large.

~~~xml
<VirtualHost *:80>
    ServerName app.example.com
    
    ProxyPreserveHost On
    ProxyPass / http://server-host:8081
    ProxyPassReverse / http://server-host:8081
    ProxyRequests Off

    ProxyPass /static/ !

    Alias /static/ "/apache/www/"

</VirtualHost>
~~~

`ProxyPass /static/ !` to prevent reverse proxy to forward static requests to the backend server. they will be served by Apache. 


**Proxy Balancer: Module mod_proxy_balancer**

~~~xml
<VirtualHost *:80>
    ServerName app.example.com
	
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

**Forward using AJP**

~~~xml
ProxyPass / ajp://localhost:8009/
ProxyPassReverse / ajp://localhost:8009/
~~~