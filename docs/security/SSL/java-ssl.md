---
layout: default
title: Java - SSL
parent:  SSL
grand_parent: Security
nav_order: 2
---

### KeyStores PKCS12 and JKS 
**KeyStore** is an archive format, commonly used to contain both private keys and their Certificates.Since Java 9, the default keystore format is PKCS12. 

**Generate a Java KeyStore**

    openssl pkcs12 -export -in example-cert.pem -inkey example-priv-key.pem -name example -out  example-pkcs.p12 

**Convert PKCS12 to JKS**

	keytool -importkeystore -srcstoretype pkcs12 -srckeystore example-pkcs.p12 -destkeystore example-keystore.jks

