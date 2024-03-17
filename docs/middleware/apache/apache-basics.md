---
layout: default
title: Apache Basics
parent:  Apache
grand_parent: Middleware
nav_order: 1
---


Environment : Apache 2.4 , Ubuntu 20.04

### Stop/Start
### apachectl
### Configuration  Files
Directory:

	/etc/apache2/

### Check Syntax

	/apache/bin/httpd -f httpd.conf -t
	/apache/bin/httpd -f httpd.conf -S

### Logs


### Page de Maintenance
Ajouter un virtual host de maintenance. En remplacement le VHost d'origine.

vhost_mnt.conf
```
<VirtualHost 10.0.0.35>
    ServerName www.mysafar.com
    DocumentRoot /www/data/html
    RewriteEngine on
    RewriteCond %{REQUEST_URI} !.*(npg|gif|jpg)$
    RewriteRule ^/.* /maintenance_mysafar.html
    ErrorLog /logs/maintenance_error_log
    CustomLog /logs/maintenance_access_log combined
</VirtualHost>
```

Puis recharger la conf:
	
	mv vhost_app.conf vhost_app.conf.ORIGIN
	cp vhost_mnt.conf vhost_app.conf
    apachectl reload

### Virtual Host pour Weblogic
	<VirtualHost x.x.x.x>
    ServerName www.application.domaine.fr
     <IfModule mod_weblogic.c>
        WebLogicCluster
               wls1.application.domaine.fr:port,wls2.application.domaine.fr:port
        <Location />
                SetHandler weblogic-handler
        </Location>
    </IfModule>
    ErrorLog /appli/log/application_error_log
    CustomLog /appli/log/application_access_log combined
	</VirtualHost>



