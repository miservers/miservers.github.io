---
layout: default
title: Rabbitmq
parent: Middleware
nav_order: 6.3
---


### Config
/etc/rabbitmq/rabbitmq.config

### Start 
~~~sh
systemctl start rabbitmq-server
~~~

Or

rabbitmq-server -detached

### rabbitmqctl
rabbitmqctl list_queues

### Enable Web Console
~~~sh
rabbitmq-plugins enable rabbitmq_management
~~~

http://<host>:15672

Default Login: guest/guest

### Consoles Screens
![a](/docs/images/rabbitmq-queues.png)

### AMQP
AMQP - Advanced Manager Queue Protocol.

