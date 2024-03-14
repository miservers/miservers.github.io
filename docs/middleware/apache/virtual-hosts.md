---
layout: default
title: Virtual Hosts
parent:  Apache
grand_parent: Middleware
nav_order: 3
---

### Name-Based VHosts
Name-based Vhosts use  ServerName and ServerAlias  directives to determine the Vhost to serve. 

below two VHosts: www.safar.com and dev.safar.com

www.safar.com
```
<VirtualHost *:80>
    ServerName www.safar.com
    ServerAlias prod.safar.com
    ServerAdmin webmaster@me.com  
    ErrorLog /var/log/apache2/prod.safar.com-error_log
    TransferLog /var/log/apache2/prod.safar.com-access_log

    DocumentRoot "/www/safar/"
    <Directory "/www/safar/"> 
            Options -Indexes +FollowSymLinks 
            AllowOverride All 
            Require all granted 
    </Directory> 
</VirtualHost>
```

dev.safar.com
```
<VirtualHost *:80>
    ServerName dev.safar.com
    ServerAdmin webmaster@me.com  
    ErrorLog /var/log/apache2/dev.safar.com-error_log
    TransferLog /var/log/apache2/dev.safar.com-access_log
    
	DocumentRoot "/www/safar-dev"
    <Directory "/www/safar-dev"> 
            Options Indexes FollowSymLinks 
            AllowOverride All 
            Require all granted 
    </Directory> 
</VirtualHost>
```

### IP-Based VHosts
IP-based VHosts use the IP to determine the correct VHost to serve. 

