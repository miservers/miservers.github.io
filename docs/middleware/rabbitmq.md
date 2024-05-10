---
layout: default
title: RabbitMQ
parent: Middleware
nav_order: 6
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

http://host:15672

Default Login: guest/guest

### Consoles Screens
![a](/docs/images/rabbitmq-queues.png)

### AMQP
AMQP - Advanced Manager Queue Protocol.
![a](/docs/images/amqp-arch.png)

 AMQP 0-9-1 brokers provide four exchange types:
  - **Direct exchange** - **Empty string**: it routes messages with a routing key equal to the routing key declared by the binding queue
    ~~~~py
    # Sender
    channel.queue_declare(queue='Q1')
    channel.basic_publish(exchange='', routing_key='Q1', body='Hello World!')

    # Receiver
    channel.queue_declare(queue="Q1")

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")

    channel.basic_consume(
        queue="Q1",
        on_message_callback=callback,
        auto_ack=True,
    )
    ~~~
  - **Fanout** : The Fanout exchange type routes messages to all bound queues indiscriminately. If a routing key is provided, it will simply be ignored.
  - **Topic**: it routes messages to queues whose routing key matches all, or a portion of a routing key.
  - **Headers** : it routes messages based upon a matching of message headers

