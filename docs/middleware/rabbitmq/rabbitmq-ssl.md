---
layout: default
title: RabbitMQ SSL
parent:  RabbitMQ
grand_parent: Middleware
nav_order: 2
---

### Approches for Client to communicate to RabbitMQ via SSL
Two approches:
1. Configure RabbitMQ to handle SSL connections.
2. Use Proxy or Load balnacer(e.g HAProxy) to perform clients SSL connections. 

### Requirements
Theses packages are required to configure SSL for RabbitMQ
~~~sh
yum install  -y erlang-asn1  erlang-crypto erlang-public-key erlang-ssl
~~~

### Enabling TLS Support in RabbitMQ

Genereate an auto signed certificate
~~~sh
 openssl req -x509 -newkey rsa:2048 -keyout server-key.pem -out server-certificate.pem -days 365 \
         -subj '/C=FR/ST=France/L=Paris/O=Safar/OU=DSI4/CN=rhel2'
~~~

Add SSL config to `rabbitmq.conf`
~~~sh
listeners.ssl.default = 5671

ssl_options.cacertfile = /etc/rabbitmq/ca_certificate.pem
ssl_options.certfile   = /etc/rabbitmq/server_certificate.pem
ssl_options.keyfile    = /etc/rabbitmq/server_key.pem
ssl_options.verify     = verify_peer
ssl_options.fail_if_no_peer_cert = true
ssl_options.password   = changeit
~~~



