---
layout: default
title: Known Errors
parent:  Apache
grand_parent: Middleware
nav_order: 6
---

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


