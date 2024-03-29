---
layout: default
title: Set Up
parent:  Tomcat
grand_parent: Middleware
nav_order: 4
---


## Configure Security
--------------------------------------------------------------
### Password Encryption

Generate the encrypted password: 

```sh
    TOMCAT_HOME/bin/digest.sh -a sha-256 s3cr3t
    s3cr3t:abb62be83c64497e48608ae0987da$1$918643e3a75d367b0ad45a34bd67..
```

Modify <ins>server.xml</ins>

```xml
<Realm className="org.apache.catalina.realm.UserDatabaseRealm" resourceName="UserDatabase">
  <CredentialHandler className="org.apache.catalina.realm.MessageDigestCredentialHandler" algorithm="SHA-256"/>
</Realm>
```

Edit <ins>tomcat-users.xml</ins>

```xml
  <role rolename="manager-gui"/>
  <user username="admin123"  password="abb62be83c64497e48608ae0987da$1$918643e3a75d367b0ad45a34bd67..." roles="manager-gui"/>
```

Restart Tomcat
 

### Realm
A Realm is a "database" of usernames and passwords that identify valid users of a web application , and roles (similar to Unix groups) assigned to those users. 

Differents implementations of realm can be used:
  - DataSource Database Realm 
  - JNDI Directory Realm
  - UserDatabase Realm: accesses are defined in *conf/tomcat-users.xml* 
  - JAAS Realm

more informations about realms can be found here [Tomcat Realm](https://tomcat.apache.org/tomcat-8.5-doc/realm-howto.html)


### Overload Java Security Policy or Ext lib

Add to _setenv.sh_  

```sh
    CATALINA_OPTS="... -Djava.ext.dirs=jre/lib/ext -Djava.security.policy=jre/lib/security/java.policy"
```

### TrustStore  

Add this options to _CATALINA_OPTS_  

```sh
    -Djavax.net.ssl.trustStore=/path/truststore.jks 
    -Djavax.net.ssl.trustStorePassword=**** 
    -Djavax.net.ssl.trustStoreType=JKS
```



### Activate HTTPS (Tomcat 10)
Uncomment this in <ins>server.xml</ins>

```xml
<Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
               maxThreads="150" SSLEnabled="true">
        <UpgradeProtocol className="org.apache.coyote.http2.Http2Protocol" />
        <SSLHostConfig>
            <Certificate certificateKeystoreFile="conf/localhost-rsa.jks"
                         type="RSA" />
        </SSLHostConfig>
</Connector>
```

Create a local KeyStore with server's private key and self signed certificate:

```sh
keytool -genkey -alias myapp -keyalg RSA -keystore myapp-keystore.jks -keysize 2048 -validity 365
```

Enable Java(JSSE) Connector(APR is **deprecated**):

```xml	
	<Connector
	    protocol="org.apache.coyote.http11.Http11NioProtocol"
	    port="8443"
	    maxThreads="150"
	    SSLEnabled="true">
  		<SSLHostConfig>
    		<Certificate
      			certificateKeystoreFile="${user.home}/myapp-keystore.jks"
      			certificateKeystorePassword="changeit"
      			type="RSA"
      		/>
    	</SSLHostConfig>
	</Connector>
```

https://192.168.56.101:8443/manager/html

Full Docs : https://tomcat.apache.org/tomcat-10.0-doc/ssl-howto.html


## Secure Tomcat
--------------------------------------------------------------

MUST SEE : https://www.owasp.org/index.php/Securing_tomcat

### Disable SSL renegociation 
this vulnerability may allow DDOS. attacker can send renegociation requests that can cause CPU usage to spike. 

Test if renotiation is enabled  

    $ openssl s_client -connect localhost:443
    [snip... a lot of openssl output]
    ---
    HEAD / HTTP/1.0
    R
    RENEGOTIATING
    28874:error:1409E0E5:SSL routines:SSL3_WRITE_BYTES:ssl handshake failure:s3_pkt.c:530:

Enter "HEAD / HTTP/1.0" newline and "R". if response:
* Http request completes, that means that renegotiation is enabled.
* if failure => renogociation is disabled
* if timeout => SSL deals with renegociation

see : https://blog.ivanristic.com/2009/12/testing-for-ssl-renegotiation.html  

To disable renogociation in NIO(style JSSE) protocle, modify connector in **server.xml**, 
**allowUnsafeLegacyRenegotiation=false**


### Eliminate banner grabbing in Apache Tomcat
Access to http://localhost:8080/notFound will show Tomcat Version (eg Apache Tomcat/8.0). To Eliminate it : 

1. Modify server.xml : add server="XYZ" property to connector

```
   <Connector port="8080" protocol="HTTP/1.1"
	    ...
        server="dServer" /> 
```
2. Suppress Version from catalina.jar

```
backup lib/catalina.jar

jar xf catalina.jar org/apache/catalina/util/ServerInfo.properties
ou
zip -x catalina.jar org/apache/catalina/util/ServerInfo.properties

Replace 
  server.info=Apache Tomcat 8.0.x.x/x
  server.number=8.0.1.2
By
  server.info=
  server.number=0.0.0.0
  
jar uf catalina.jar  org/apache/catalina/util/ServerInfo.properties
ou
zip -u catalina.jar  org/apache/catalina/util/ServerInfo.properties

rm org/apache/catalina/util/ServerInfo.properties

```

### Suppressing StackTraces on HTTP 500 Errors 
In **web.xml**, add error-page tag:

```
<error-page>
    <error-code>500</error-code>
    <location>/WEB-INF/jsp/common/error.jsp</location>
</error-page>
```

### Password Encryption (8.5 NOT Tomcat 10 version)
Generate encrypted password

    ./digest.sh -a sha-256 secret
    ./digest.sh -a md5 secret  : for MD5
	
To use encrypted pasword in **tomcat-users.xml**, add digest to **server.xml**

	<Realm className="org.apache.catalina.realm.UserDatabaseRealm"
       resourceName="UserDatabase"
       digest="sha-256" />

_digest.sh_  cannot be used to encrypt passwords for DataSource resources	   
	
### CSRF (Cross-Site Request Forgery)
manager-gui is protected against CSRF but JMX interface is NOT.   


