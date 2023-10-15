---
layout: default
title: Apache
parent: Middleware
nav_order: 4
---

## Apache Web Server Basics
----------------------------------
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

## Modules & Directives
---------------------------------
Enable/disable a module(Debian)

	a2enmod ssl
	a2dismod ssl
### DocumentRoot
This directive map URL to FileSystem Path.

If **DocumentRoot** is set to **/www/safar**, 
The URL http://www.safar.com/team.html will be mapped to the file **/www/safar/team.html**.

If a directory is requested(URL with / at the end), the file served is defined by the directive **DirectoryIndex**:

	DirectoryIndex index.html index.php


### Directory
Directory directive allows to enclose directives and options to apply a filesystem directory and its sub directories.

Eg. Limit access to the directory /www/safar/ and its  subdirectories:

	<Directory /www/safar/> 
        Order deny,allow
        Deny from all
        Allow from 192.168.56.110        
    </Directory>  

### Location
Location directive change configuration to apply to a webspace(url).

Eg1. Deny Access to the webspace : http://www.safar.com/private

	<Location /private>
        Order deny,allow
        Deny from all
    </Location>

Eg2. Map a URL to an apache handler

	<Location /server-status>
		SetHandler server-status
	</Location>

### Options 
Options directive controls features in a Directory. Main options are: Indexes, FollowSymLinks, ExecCGI. 

Disable directory listing: 

		<Directory /www/safar>
			Options -Indexes +FollowSymLinks
			...

### Require
Access allowed unconditionally:

	Require all granted

Access denied uncondionally

	Require all denied

Require full ip 

	require ip 192.168.56.1

Require a subnet

	require ip 192.168

### Deny , Allow , Order
/!\ Deprecated by Require directive

## htaccess Files
----------------------------------
.htaccess files are generaly used to configure the Web Server when we don't have access to the httpd.conf. However they slow the Web Server.

Disable Directory Listings in Apache using **.htaccess**:

1. Add directive **AllowOverride All** to the Site Directory 

		<Directory /www/safar>
			Options Indexes FollowSymLinks
			AllowOverride All
			Require all granted
		</Directory>

2. Create the file **.htaccess** under /www/safar with contents

		Options -Indexes

3. Access to http://www.safar.com/images/ will be then forbidden


## Virtual Hosts
---------------------------------
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

## Load Balancing
---------------------------------
See  [load-balancing.md](./load-balancing.md)

## Security
---------------------------------
### HTTPS

LoadModule ssl_module modules/mod_ssl.so

Include conf/safar.com-ssl.conf

<ins>safar.com-ssl.conf:</ins>

	Listen safar192:443
	<VirtualHost *:443>
	    ServerName ar.safar.com
	    SSLEngine on
	    SSLCertificateFile "/path/to/www.mysafar.com.pem"
	    SSLCertificateKeyFile "/path/to/www.mysafar.com.key"
	</VirtualHost>



### Rediriger HTTP vers HTTPS 
#### Using HSTS
```
	LoadModule headers_module modules/mod_headers.so

	<VirtualHost 10.0.0.45:443>
		Header always set Strict-Transport-Security "max-age=63072000; includeSubdomains;"
	</VirtualHost>

	<VirtualHost *:80>
		[...]
		ServerName safarmeit.com
		Redirect permanent / https://safarmeit.com/
	</VirtualHost>
```

#### Using rewrite rule: less secure /!\ MIM vulnerability
```sh
Activate le mod_rewrite
On Debian
 $ a2enmod rewrite
On others:
 LoadModule rewrite_module modules/mod_rewrite.so



<VirtualHost *:80>
  ServerName www.mysafar.com

  RewriteEngine On
  RewriteCond %{HTTPS} off
  RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301] 
</VirtualHost>

ar.safar.com_ssl.conf:
<VirtualHost *:443>
  ServerName www.mysafar.com
  ...
</VirtualHost>

Ou bien si plusieurs domaines

```


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

	
## Known Errors
------------------------
### Forbidden - You don't have permission to access this resource
Error 403.

We assume this VHost:

	<VirtualHost *:80>
	    DocumentRoot "/www/safar/"
	    ServerName www.safar.com

	</VirtualHost>

To resolve this access error, do the following:

1. Grand access to /wwww directory

		<Directory /www/>
			Options Indexes FollowSymLinks
			AllowOverride None
			Require all granted
		</Directory>

2. Allow EXECUTE access to /www/safar

		chmod a+x /www/safar

3. Adjust the directory ownership (www-data OR apache)

		chown -R www-data:www-data /www/safar
		
4. Check .htaccess files

### Erreur: [warn] VirtualHost overlaps with VirtualHost , the first has precedence
Ajouter:

	NameVirtualHost 10.168.1.10:80
	NameVirtualHost 10.168.1.10:443

	<VirtualHost 10.168.1.10:80>
	....
	
	<VirtualHost 10.168.1.10:443>
	....
