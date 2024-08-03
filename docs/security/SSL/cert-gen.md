---
layout: default
title: Cert Generation  - Tuto
parent:  SSL
grand_parent: Security
nav_order: 1
---

## Genartaion de Certificat - complete Tuto 
-------------------------------------------------------

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
    	
