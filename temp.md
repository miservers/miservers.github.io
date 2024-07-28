### The following example uses lsof to display OS processes that listen on port 5672 and use IPv4:

sudo lsof -n -i4TCP:5672 | grep LISTEN





##SSL

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


Java debug ssl
------

Debugging SSL/TLS connections in Java can be essential for diagnosing issues related to SSL handshake failures, certificate verification problems, and other cryptographic errors. Java provides built-in options to enable detailed logging for SSL/TLS operations.

### Enabling SSL Debugging in Java

To enable SSL debugging in Java, you can set the `javax.net.debug` system property to `all` or specify particular components to debug. This can be done via command-line arguments when starting your Java application.

#### Command-Line Example

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

#### Example with Specific Options

If you want to debug only the handshake and trust manager, you can set:

```sh
java -Djavax.net.debug=handshake,trustmanager -jar your-application.jar
```

### Example Output

Here is an example of what the SSL debugging output might look like when you enable it:

```plaintext
trigger seeding of SecureRandom
done seeding SecureRandom
Allow unsafe renegotiation: false
Allow legacy hello messages: true
Is initial handshake: true
Is secure renegotiation: false
%% No cached client session
*** ClientHello, TLSv1.2
RandomCookie:  GMT: 1609459200 bytes = { 4, 15, -128, -34, 127, 63, -94, 123, 20, -32, -4, -33, 98, 31, 44, 64, 45, 12, -56, 82, 92, 105, 12, 32, 65, -14, 15, 20 }
Session ID:  {}
Cipher Suites: [TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA, TLS_RSA_WITH_AES_256_CBC_SHA]
Compression Methods:  { 0 }
***
main, WRITE: TLSv1.2 Handshake, length = 85
main, READ: TLSv1.2 Handshake, length = 70
*** ServerHello, TLSv1.2
RandomCookie:  GMT: 1609459200 bytes = { -1, -13, 11, 45, 127, 63, -94, 123, 20, -32, -4, -33, 98, 31, 44, 64, 45, 12, -56, 82, 92, 105, 12, 32, 65, -14, 15, 20 }
Session ID:  {35, -12, 49, 74, 15, 91, 87, 0, 65, -42, -16, -76, 95, 28, 54, 96, -22, -45, 11, -77, -18, -68, 5, -33, -6, -76, 2, 39, 75, -60, 4, -28}
Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
Compression Method: 0
***
```

### Using SSL Debugging in Code

You can also set the `javax.net.debug` property programmatically within your Java code, typically during development or debugging:

```java
public class SSLDebugExample {
    public static void main(String[] args) {
        System.setProperty("javax.net.debug", "all");
        
        // Your code to create SSL connection
    }
}
```

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

### Summary

Enabling SSL debugging in Java is a powerful way to diagnose issues related to SSL/TLS connections. By using the `javax.net.debug` property, you can obtain detailed logs that help you understand and resolve problems such as handshake failures, certificate issues, and protocol mismatches.




