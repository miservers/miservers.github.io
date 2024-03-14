---
layout: default
title: Modules & Directives
parent:  Apache
grand_parent: Middleware
nav_order: 2
---



### Enable/disable a module(Debian)

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
