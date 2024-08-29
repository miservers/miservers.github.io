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


### Java: Default and supported TLS versions

| Java Version                                       | TLS version                               | 
| -------------------------------------------------- | ----------------------------------------- |
| Java 8 Update 161 and Later                        | TLS 1.2 is enabled by default. |
| Java 11 and Later                                  | TLS 1.3 is supported, TLS 1.2 remains the default version|
| Java 7                                             | ** Default: TLS 1.0 and TLS 1.1, TLS 1.2 is supported but not enabled by default |
| Java 6                                             | Default: SSL 3.0 and TLS 1.0, TLS 1.1 and TLS 1.2 are not supported by default.|
| Java 5 and Earlier                                 | Default: SSL 3.0., TLS is not supported.|
