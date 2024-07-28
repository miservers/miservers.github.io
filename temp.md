SSL

https://www.rabbitmq.com/docs/ssl#tls-versions

 LTS versions 11.0.11, 1.8.0_291 and up have TLSv1 and TLSv1.1 disabled by default



java.security file. In Java 11 and up it is located in the folder conf/security/ under your JAVA_HOME.

jdk.tls.disabledAlgorithms=SSLv3, RC4, DES, MD5withRSA, DH keySize < 1024, \
    EC keySize < 224, 3DES_EDE_CBC, 

 connect using TLSv1.2
openssl s_client -connect 127.0.0.1:5671 -tls1_2

.
TLS version	Minimum JDK version	Minimum .NET version
TLS 1.3	JDK 8 starting with JDK8u261, JDK 11+	.NET 4.7 on Windows versions that support TLSv1.3
TLS 1.2	JDK 7 (see Protocols, JDK 8 recommended	.NET 4.5
TLS 1.1	JDK 7 (see Protocols, JDK 8 recommended	.NET 4.5





