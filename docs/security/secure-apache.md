---
layout: default
title: Secure Apache
parent: Security
nav_order: 3
---

https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/security_guide/sect-security_guide-server_security-securing_the_apache_http_server#sect-Security_Guide-Server_Security-Securing_the_Apache_HTTP_Server


### Cacher les infos sur Apache
dans httpd.conf
~~~
ServerTokens Prod
ServerSignature Off
~~~

Tester 
~~~
curl -I http://exemple.com
~~~

### Forcer les TLS 1.2 et TLS 1.3
et dèsactiver les autres qui sont obsolètes

dans ssl.conf
~~~
SSLProtocol -SSLv2 -SSLv3 -TLSv1 -TLSv1.1 +TLSv1.2 +TLSv1.3
SSLCipherSuite HIGH:!aNULL:!MD5:!3DES:!RC4
~~~

- HIGH: n'est pas un bon choix,mieux vaut les fixer manuellement

Tester les ciphers et les tls disponibles sur le serveur:

~~~
openssl ciphers -v
openssl -h
~~~

sur **RHEL 8+**, 
```update-crypto-policy --show``` 
si la valeur est **DEFAULT** alors TLS 1.2 et 1.3 sont activées. les TLS 1 et 1.1 sont désactivées. pour les activer, utilser la policy **LEGACY**.

### Options à vérifier
- Indexes: permet de naviguer dans un répertoire, désactivé par defaut

- userDir: permet de naviguer dans les fichiers d'un user, désactivé par defaut

- FollowSymLinks: activé par defaut, attention lors de creation de liens symboliques dans le document root. une très mauvaise idée de créer un lien symbolique vers /