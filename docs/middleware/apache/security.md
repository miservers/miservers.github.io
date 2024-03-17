---
layout: default
title: Security
parent:  Apache
grand_parent: Middleware
nav_order: 5
---

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


