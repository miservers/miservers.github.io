---
layout: default
title: NGINX
parent: Middleware
nav_order: 4.5
---

### Installation
```sh
$ apt install nginx
```

### Configuration Files
```
/etc/nginx/
	├── nginx.conf
	├── conf.d
	├── modules-available
	├── modules-enabled
	├── sites-available
	└── sites-enabled
	...
```

### Start/Stop
```sh
$ systemctl start nginx
```
### Check the Config Syntax
	$ nginx -t

### Nginx as a Static File Server
nginx can be used to host static files. Therefore you can browse directory through http. 

This is a sample configration that does not take Security into consideration:

1. Create a config file: **/etc/nginx/conf.d/ibm-file-server.conf** 
```conf
server {
    listen       80;
    server_name  ibm-file-server.safar.ma;
    root /opt/IBM/PackagingUtility; # your static file directory
    autoindex on; # directory listing

    location / {
        try_files $uri $uri/ =404;
    }
}
```
2. Restart nginx
3. Browse the files: <a>http://ibm-file-server.safar.ma</a>

### Nginx as Reverse Proxy in Front of Tomcat
Object: use Nginx as a reverse proxy in front of Tomcat

1. Get the conf template : tomcat-basic.conf

		cd /etc/nginx/conf.d
		curl https://www.nginx.com/resource/conf/tomcat-basic.conf > tomcat-basic.conf

2. Edit tomcat-basic.conf:
	```conf
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
4. Restart Nginx
5. Test https://www.safar.com/ 



