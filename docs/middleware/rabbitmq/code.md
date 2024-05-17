---
layout: default
title: Code Examples
parent:  RabbitMQ
grand_parent: Middleware
nav_order: 4
---


### Code Examples
<a>https://github.com/rabbitmq/rabbitmq-tutorials/

### Send.py
send.py:
~~~py
#!/usr/bin/env python
# Usage : python send.py <qname>
#
# virtual host 'api' and user 'admin' must be created
#
# Queues and Massages are durable/persistant to crash and reboot of the rabbitmq server

import pika
import sys

# qname = "Q1"
qname = sys.argv[1]

credentials = pika.PlainCredentials('admin', 'changeit')
parameters = pika.ConnectionParameters('rhel2',
                                   5672,
                                   'api',
                                   credentials)

connection = pika.BlockingConnection(parameters)


channel = connection.channel()

channel.queue_declare(queue=qname, durable=True)

channel.basic_publish(exchange="", routing_key=qname, body="Hello World!", 
                        properties=pika.BasicProperties(
                         delivery_mode = pika.DeliveryMode.Persistent
                      ))
print(" [x] Sent 'Hello World!'")

connection.close()
~~~
