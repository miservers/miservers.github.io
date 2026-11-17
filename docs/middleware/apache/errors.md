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

### 421: SNI Misredirect Request
SNI - Server Name Indication: une surcouche de SSL qui permet de creer plusieur vhost sur le même serveur (ip).
Le SNI consite à ce que une requête indique le nom de domaine avant le handshake ssl. 

Le problème apparaît suite au durcissement de sécurité à partir de la version 2.4.64 sortie en juillet 2025

Verifier que le cert retourné correspond au site requeté:
~~~sh
openssl s_client -connect ip:port -servername site1.example.com
~~~

Si l’on fait un tcpdump, on verra passer en clair  site1.example.com au début de l’échange :

~~~sh
tcpdump -s0 -XX -ni any port 443
~~~

Verifier que la prmitive **ProxyPreserveHost** est à **Off**(valeur par défaut )
**Références**
- https://blog.evolix.com/restriction-entre-virtualhosts-apache/
- https://community.f5.com/discussions/technicalforum/big-ip-methods-to-fix-the-%E2%80%9C421-misdirected-request%E2%80%9D-error/343284
- 

Config Reverse proxy Apache
~~~sh
SSLProxyEngine on
ProxyPass        / https://site.example.com/
ProxyPassReverse / https://site.example.com/
~~~

Test
~~~sh
curl -vk https://example.com/ --resolve example.com:443:127.0.0.1
~~~

# Compte rendu

Compte rendu – Erreur HTTP 421 avec backend Apache multi-vhosts


---

1. Contexte

Architecture avec un F5 BIG-IP en frontal et des backends Apache hébergeant plusieurs VirtualHosts SSL sur la même IP et le même port (443).

Des erreurs HTTP 421 – Misdirected Request apparaissent lors des health checks du F5 et sur certaines connexions.

Les membres du pool sont marqués DOWN, entraînant des interruptions de service.



---

2. Symptômes

Logs Apache :

AH02032: Hostname provided via SNI and hostname provided via HTTP are different

Certificat SSL incorrect ou réponse 421 lors des tests depuis le F5.



---

3. Analyse et cause racine

Le F5 n’envoie pas le SNI (Server Name Indication) pendant le handshake TLS.

Apache ne peut donc pas sélectionner le bon VirtualHost → il répond avec un certificat par défaut ou renvoie 421.



---

4. Solution recommandée : activer le SNI côté F5

> La solution retenue est d'activer le SNI directement sur le F5 via un profil Server SSL, associé à un monitor HTTPS en mode In-TMM.



Étapes :

1. Créer un profil Server SSL avec sni-default et sni-require enabled.


2. Configurer un monitor HTTPS avec le bon header Host et activer In-TMM.


3. Associer le profil et le monitor au pool backend.


4. Tester avec :

openssl s_client -connect backend:443 -servername site1.example.com


5. Mettre à jour les règles firewall, car l’origine des checks change (Self-IP → IP TMM/SNAT).



Bénéfices :

Suppression des erreurs 421.

Performance accrue grâce à In-TMM Monitoring.

Conformité TLS moderne (SNI, TLS 1.3).

Simplification opérationnelle.



---

5. Pistes étudiées mais non retenues

Piste	Motif du rejet

Ports distincts par VirtualHost	Très complexe à déployer et à maintenir, supprime l’hébergement mutualisé via SNI.
Apache customisé indépendant du système	Coût élevé de maintenance, le problème de SNI persiste.
Certificat commun (wildcard/SAN)	Gestion du cycle de vie complexe et risques sécurité accrus.
Certificat par défaut unique	Non conforme et génère des erreurs côté client.



---

6. Conclusion

L’absence de SNI envoyé par le F5 empêche Apache d’identifier correctement le VirtualHost cible.

> L’activation du SNI sur le F5 via un profil Server SSL et In-TMM Monitoring est la solution définitive, robuste et évolutive, garantissant la suppression des erreurs 421 et la conformité avec les standards TLS.
