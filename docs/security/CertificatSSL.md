---
layout: default
title: SSL Certificate
parent: Security
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

## SSL Handshake
---------------------------------

  1. client request to server
  2. server send to client its cert, containaing server public key 
  3. client autenticate the server: by contacting the CA.
  4. if CA does'nt authenticate the server, the browser handler a warning.

  ![SSL_Handshake](/docs/images/SSL_Handshake.png)

## Genartaion de Certificat - complete Tuto 
---------------------------------

Create CSR request config <ins>example-csr.conf</ins>

	[ req ]
	default_bits       = 4096
	default_md         = sha512
	default_keyfile    = example-priv-key.pem
	output_password    = secret
	prompt             = no
	encrypt_key        = no
	distinguished_name = req_distinguished_name

	req_extensions     = v3_req

	[ req_distinguished_name ]
	countryName            = "MA"                     # C=
	stateOrProvinceName    = "Maroc"                  # ST=
	localityName           = "Casablanca"             # L=
	postalCode             = "20240"                  # L/postalcode=
	streetAddress          = "Mdina 1622"             # L/street=
	organizationName       = "SAFAR"                  # O=
	organizationalUnitName = "DSI"                    # OU=
	commonName             = "example.com"            # CN=
	emailAddress           = "webmaster@example.com"  # CN/emailAddress=

	[ v3_req ]
	# http://www.openssl.org/docs/apps/x509v3_config.html
	subjectAltName  = DNS:www.example.com,DNS:www2.example.com 


### Create the CSR ( Certificate Request) 

Create CSR request from CSR Conf:

    openssl req -config example-csr.conf -newkey rsa:2048 -out example-req.csr

The Private Key is also generated

Decode the Certificate Request

    openssl req -text -noout -in example-req.csr

Send the CSR to the cert authority, and you receive a  signed cert(PEM)
	
### Generate an Auto-Signed Certificate

	openssl x509 -req -in example-req.csr -extensions v3_req -extfile example-csr.conf  \
	       -signkey example-priv-key.pem -out  example-cert.pem  -days 999

Decode The Cerificate:

	openssl x509 -inform  pem  -text -noout -in example-cert.pem

Decode The Private Key:

	openssl rsa -check -in example-priv-key.pem
  

### KeyStores PKCS12 and JKS 
**PKCS#12 KeyStore** is an archive format, commonly used to contain both private keys and their Certificates. **JKS KeyStore** is specific to Java. Since Java 9, the default keystore format is PKCS12. 

**Generate a PKCS12 KeyStore**

    openssl pkcs12 -export -in example-cert.pem -inkey example-priv-key.pem -name example -out  example-pkcs.p12 

**Convert PKCS12 to JKS**

	keytool -importkeystore -srcstoretype pkcs12 -srckeystore example-pkcs.p12 -destkeystore example-keystore.jks

### Convert PEM to CRT ( for Apache)

	openssl x509 -outform der -in example-cert.pem -out example-cert.crt
    	

## Certificat with OpenSSL
---------------------------------
**Decode a cert, Check Key**
```sh
  openssl x509 -inform der -text -noout -in server-cert.pem
  openssl rsa -check -in server-priv.key
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


	
## DOCS
---------------------------------
- https://vyatkins.wordpress.com/2013/11/19/java-base-ssl-connection-to-tomcat-with-server-and-client-certifications/
- http://blog.palominolabs.com/2011/10/18/java-2-way-tlsssl-client-certificates-and-pkcs12-vs-jks-keystores/index.html


