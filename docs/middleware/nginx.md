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

### Use NGINX as a Static File Server
nginx can be used to host static files. Therefore we can access them via http. 

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


