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

| Java Version                                       | TLS Protocols                              | 
| -------------------------------------------------- | ----------------------------------------- |
| Java 11 and Later                                  | - TLS 1.2 : default <br>- TLS 1.3: supported                        |
| Java 8                                             | - TLSv1.2 : default<br>- TLSv1.1<br>- TLSv1<br>- SSLv3                         |
| Java 7                                             | - TLSv1.2<br>- TLSv1.1<br>- TLSv1 : default<br>- SSLv3              |
| Java 6                                             | - TLS v1.1 : JDK 6 update 111 and above<br>- TLSv1 : default<br>- SSLv3 |
| Java 5 and Earlier                                 | - SSLv3 : default <br>- TLS is not supported.|

Java versions **11.0.11**, **1.8.0_291** and up have TLSv1 and TLSv1.1 disabled by default


### JSSE Parameters
| Parameter                | Description                                                                                       |
|--------------------------|---------------------------------------------------------------------------------------------------|
| javax.net.debug          | Enable Java SSL debugging<br>Eg: -Djavax.net.debug=all or  -Djavax.net.debug=ssl:handshake:verbose|
| https.protocols          | Controls the protocol version used by Java clients which obtain https connections<br> -Dhttps.protocols=TLSv1,TLSv1.1,TLSv1.2|
| jdk.tls.client.protocols | Controls the underlying platform TLS implementation .<br> Eg: -Djdk.tls.client.protocols=TLSv1.1,TLSv1.2<br> Available: JDK 8 , Java 7 update 95, Java 6 update 121|
| https.proxyHost<br>http.proxyPort<br>https.proxyHost<br>https.proxyPort| Use of Http(s) protocol<br> Eg: -Dhttp.proxyHost=proxy.example.com -Dhttp.proxyPort=8080|


### Disable/Enable Tlsv1 


In **java.security** file. In Java 11 and up it is located in the folder conf/security/ under your JAVA_HOME.

~~~
JAVA_OPTS="-Djdk.tls.disabledAlgorithms=SSLv3,Tlsv1,RC4,DES, ....
~~~

Or 

~~~
-Djdk.tls.disabledAlgorithms=Tlsv1
~~~ 


**Enable TLS v1, v1.1 and v1.2**

~~~
JAVA_OPTS="-Dhttps.protocols=TLSv1,TLSv1.1,TLSv1.2 -Djdk.tls.client.protocols=TLSv1,TLSv1.1,TLSv1.2"
~~~~

### Connect using TLSv1.2

```sh
openssl s_client -connect 127.0.0.1:5671 -tls1_2
```
.



### Enabling SSL Debugging in Java

To enable SSL debugging for a Java application, you can use the following command:

```sh
java -Djavax.net.debug=all -jar your-application.jar
```

### Debug Options

The `javax.net.debug` property can take various options, including:

- `all`: Enables all debugging options.
- `ssl`: Enables SSL debugging.
- `handshake`: Enables debugging of the SSL handshake process.
- `data`: Enables debugging of SSL data.
- `trustmanager`: Enables debugging of the trust manager.
- `keymanager`: Enables debugging of the key manager.
- `session`: Enables debugging of session operations.

### Common Issues and Debugging Steps

1. **Certificate Issues:**
   - **Debug Output:** Look for lines indicating problems with certificates or the trust manager.
   - **Resolution:** Ensure that the server's certificate is valid and trusted by the client. You might need to import the server certificate into the Java keystore.

2. **Protocol Mismatches:**
   - **Debug Output:** Look for protocol version mismatches between client and server.
   - **Resolution:** Ensure both client and server support common SSL/TLS protocols (e.g., TLS 1.2).

3. **Cipher Suite Problems:**
   - **Debug Output:** Check the list of cipher suites supported by both client and server.
   - **Resolution:** Ensure that at least one common cipher suite is supported by both parties.

4. **Hostname Verification:**
   - **Debug Output:** Look for issues related to hostname verification in the trust manager output.
   - **Resolution:** Ensure the certificate’s subject matches the hostname of the server.

