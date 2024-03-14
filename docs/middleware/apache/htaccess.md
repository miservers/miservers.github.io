---
layout: default
title: htaccess Files
parent:  Apache
grand_parent: Middleware
nav_order: 4
---


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

