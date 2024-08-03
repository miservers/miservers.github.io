---
layout: default
title: SSL
parent:  SSL
grand_parent: Security
nav_order: 1
---

## SSL
---------------------------------
Some SSL Certificate Vocabulary:

  - **keytool**: manages Java KeyStores (JKS).
  - **KeyStore**: contains a certificate and a key pairs.
  - **TrustStore**: contains trusted certs. keystores contain private keys, while truststores do not.
  - **Certificate Authority [CA]**: verisign, Thawte,...
  - **Distinguished Name [DN**] :  "/C=FR/ST=France/L=Paris/O=Safar/OU=DSI4/CN=safar.com" 
  - **File format**: Java can manipulate PEM, PKC12 and JKS formats.
  - **PEM**: human readable certificate format. it starts with `----BEGIN CERTIFICATE----`
  - **DER**: compact binary certficate format.

## SSL Handshake
---------------------------------

  1. client request to server
  2. server send to client its cert, containaing server public key 
  3. client autenticate the server: by contacting the CA.
  4. if CA does'nt authenticate the server, the browser handler a warning.

  ![SSL_Handshake](/docs/images/SSL_Handshake.png)


## Certificat with OpenSSL
--------------------------------------------
**Decode a cert, Check Key**
```sh
  openssl x509 [-inform der] -text -noout -in server-cert.pem
  openssl rsa -check -in server-priv.key
```

**Show the Certificate Chain**
```sh
openssl s_client -showcerts -verify 5 -connect www.yousite.com:443 < /dev/null
```

**Generate SSL key pair and certificate**
```sh
  openssl req -x509 -newkey rsa:2048 -keyout server-key.pem -out server-cert.pem -days 365 \
          -subj '/C=FR/ST=France/L=Paris/O=Safar/OU=DSI4/CN=*.safar.com'
```

**Delete passphrase from the key: so tomcat does not prompt for password on startup**
```sh
  openssl rsa -in server-key.pem -out newserver-key.pem
  mv newserver-key.pem server-key.pem
```

**Import cert  from a remote server**
```sh
  openssl s_client -showcerts -connect safarit.com:20076 </dev/null 2>/dev/null | 
  openssl x509 -outform PEM >mycertfile.pem
```

**Catalina OPT (setenv)**
```sh
  -Djavax.net.ssl.trustStore=${PROJ}/conf/keystores/myapp.jks 
  -Djavax.net.ssl.keyStorePassword=mypass -Djavax.net.ssl.trustStoreType=JKS
```

**Test of connection to server**
```sh
   openssl s_client -msg -connect  127.0.0.1:20076
   openssl s_client -debug -connect  127.0.0.1:20076
```

Explain:

- **verify return:1**   => Check **success** for a specific certificate in the certificate chain 
- **verify return:0**   => Check **error** for a specific certificate in the certificate chain 
- **Verify return code: 0 (ok)** => Result OK from the whole verification process
- **Secure Renegotiation IS NOT supported**: rengociation is neot supported in TLS 1.3

### Convert PEM to CRT ( for Apache)

	openssl x509 -outform der -in example-cert.pem -out example-cert.crt
 

## Auto Signed Certificat 
---------------------------------
**generate auto signed certificat**
```sh
  openssl req -x509 -newkey rsa:2048 -keyout server-key.pem -out server-cert.pem -days 3650 \
        -subj '/C=FR/ST=France/L=Paris/O=Safar/OU=DSI4/CN=pclr0181'

  Serveur Reqeuetes longues:		
  openssl req -x509 -newkey rsa:2048 -keyout server-key.pem -out server-cert.pem -days 3650 \
        -subj '/C=FR/ST=France/L=Paris/O=Safar/OU=DSI4/CN=127.0.0.1'
```

**delete password**
```sh
  openssl rsa -in server-key.pem -out server-key.pem
```

**Get app cert**
```sh
  openssl s_client -showcerts -connect MyAPP-qua.app.safar.com:4043 </dev/null 2>/dev/null | 
  openssl x509 -outform PEM >MyAPP-qua.pem
```

**Creating trustStrore**
```sh
  cp $JAVA_HOME/jre/lib/security/cacerts myapp.jks
  Change password : default "changeit"
  keytool -storepasswd -keystore myapp.jks -storepass changeit  -new mypass
```

**Import root CA certs**
```sh
   keytool -importcert -file ca_alf_rec2014bis.crt -alias CA-cert -keystore myapp.jks -storepass weblogic
```

**import certs in truststore**
```sh
  . /soft/ihg/adm/current/setenv_java.sh
  keytool -import -trustcacerts -alias MyAPP-qua -file MyAPP-qua.pem -keystore myapp.jks -storepass mypass
  keytool -delete -alias MyAPP -keystore myapp.jks -storepass mypass
  keytool -importcert -alias MyAPP -file server-cert.pem -keystore myapp.jks -storepass mypass
  - on pres: copy traitment certif in trait-server-cert.pem
   keytool -importcert -alias MyAPP_trait -file trait-server-cert.pem -keystore myapp.jks -storepass mypass
```  

**Genarate a random password**

    openssl rand -base64 32
	
	
**Recreer un certificat**

    openssl s_client -showcerts -connect www.safar.com </dev/null 2>/dev/null | openssl x509 -outform PEM >server.pem
  
**ERROR: java.lang.RuntimeException:Could not generate DH keypair**
  
1. utiliser jdk1.7.0_131
2. http://www.wikiconsole.com/java-lang-runtimeexception-could-not-generate-dh-keypair/


## Using Shared System Certificates
---------------------------------------
**Redhat 7**



- Check if is verified certificate
~~~sh
openssl s_client -connect untrusted-root.badssl.com:443 -verify 5
~~~

You will see this message if the certicate is not verified: 
`Verify return code: 21 (unable to verify the first certificate)`

- Extract the cerificate:
  ~~~sh
  echo | openssl s_client -connect untrusted-root.badssl.com:443  2>/dev/null | openssl x509 > badssl.com.crt
  ~~~

- Adding trusted Root Certificates(CA) to the server
  - list of CAs trusted on the system:

  - Copy it to the **/etc/pki/ca-trust/source/anchors/**
    ~~~sh
	cp example-ca.crt /etc/pki/ca-trust/source/anchors/
	~~~

  - Integrate certificates into the system's certificate set
    ~~~sh
	update-ca-trust
    ~~~

- Verify entry
  ~~~sh
  trust list  | grep  rhel1 -i -A 2 -B 3
  ~~~

- Delete a Root/Intermediate cert 
```sh
# Remove it from anchor directory and  update-ca-trust
# Or
trust list  | grep "DigiCert Global"  -i -A 2 -B 3
trust anchor --remove --verbose pkcs11:id=%4e%22%54%20%18%95%e6%e3%6e%e6%0f%fa%fa%b9%12%ed%06%17%8f%39;type=cert
```
- Locate cacerts
```sh
locate cacerts
```

## HOW TO EXTRACT ROOT AND INTERMEDIATE CERTIFICATES
--------------------------------------------------
https://chadstechnoworks.com/technology_mainpage.html

- Extract the certificate:
  
```sh
$ echo | openssl s_client -connect miservers.github.io:443  2>/dev/null | openssl x509 > miservers.crt
```

- Get the Intermediate Certificate:
  
```
$ openssl x509 -in miservers.crt -text -noout | grep -i "issuer"

    Issuer: C=US, O=DigiCert Inc, CN=DigiCert Global G2 TLS RSA SHA256 2020 CA1
        CA Issuers - URI:http://cacerts.digicert.com/DigiCertGlobalG2TLSRSASHA2562020CA1-1.crt

$ curl -O http://cacerts.digicert.com/DigiCertGlobalG2TLSRSASHA2562020CA1-1.crt
```

- Check if it is root or intermediary
  
```
$ openssl x509 -in DigiCertGlobalG2TLSRSASHA2562020CA1-1.crt -inform DER -text | grep -i CN=
        Issuer: C=US, O=DigiCert Inc, OU=www.digicert.com, CN=DigiCert Global Root G2
        Subject: C=US, O=DigiCert Inc, CN=DigiCert Global G2 TLS RSA SHA256 2020 CA1
```

If Issuer-CN equals to Subject-CN, it is root cert, else it is an intermadiry cert. The cert above is intermidiary.

- Get the Root cert
  
```
$ openssl x509 -in DigiCertGlobalG2TLSRSASHA2562020CA1-1.crt -inform DER -text | grep -i issuer
        Issuer: C=US, O=DigiCert Inc, OU=www.digicert.com, CN=DigiCert Global Root G2
                CA Issuers - URI:http://cacerts.digicert.com/DigiCertGlobalRootG2.crt

$ curl -O http://cacerts.digicert.com/DigiCertGlobalRootG2.crt
``` 

- It is root cert: IssuerCN = SubjectCN
  
```sh
$ openssl x509 -in DigiCertGlobalRootG2.crt -inform DER -text | grep -i CN=
        Issuer: C=US, O=DigiCert Inc, OU=www.digicert.com, CN=DigiCert Global Root G2
        Subject: C=US, O=DigiCert Inc, OU=www.digicert.com, CN=DigiCert Global Root G2
```

## JAVA CACERT
-------------------------------------------------
The OpenJDK 8u322 portable build introduced a change in the handling of cacerts.  

It's looking for the cacerts file in /etc/pki/java/cacerts, and if the file is found it doesn't look in ${java.home}/jre/lib/security/cacerts in TrustStoreManager$TrustStoreDescriptor.  

This is different than u312 where it only looks in ${java.home}/jre/lib/security/cacerts.

Revert to the u312 behavior, as u322 has broken deployments, and consumers of the portable builds are not looking from RHEL integration.



## Certificate Authority - CA
--------------------------------------------------
### How it works?
To request a certificate from a CA like Verisign:
1. You send to them your CSR-Certificate Signing Request 
2. They return to you certificate that they have signed with their private key and their root certificate.
3. All web browser have the root certificate from the various CA.
4. The browser use the root certificate to verify if your certificate is signed.

### Create your own root CA
- Create CA private key
`openssl genrsa -des3 -out myCA.key 2048`

- Create your CA
`openssl req -x509 -new -nodes -key myCA.key -sha256 -days 1825 -out myCA.pem`

Now you become a Certificate Authority, you  can use myCA to sign client certificate.

- Install the CA on RedHat: copy .pem as .crt
  ~~~sh
  cp myCA.pem /etc/pki/ca-trust/source/anchors/myCA.crt
	
  update-ca-trust
  ~~~

- Verify: rhel2 as server nam
  ~~~sh
  trust list  | grep  rhel2 -i -A 2 -B 3
  ~~~
  
  rhel2 is the hostname used when you created the myCA.pem:

  `Common Name (eg, your name or your server's hostname) []:rhel2`



## DOCS
---------------------------------
- https://vyatkins.wordpress.com/2013/11/19/java-base-ssl-connection-to-tomcat-with-server-and-client-certifications/
- http://blog.palominolabs.com/2011/10/18/java-2-way-tlsssl-client-certificates-and-pkcs12-vs-jks-keystores/index.html


