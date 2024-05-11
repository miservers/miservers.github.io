---
layout: default
title: RabbitMQ
parent: Middleware
nav_order: 6
---

<<<<<<< HEAD
### Concepts
**RabbitMQ** is open source message broker  that implements **AMQP** - Advanced Message Queuing Protocol.


=======
>>>>>>> cc64ad18e0a218c3325392fa3edfb2014b41ba5b
### Config
| Variable                     | Default Value                               | 
|:-----------------------------|:--------------------------------------------|
| RABBITMQ_CONFIG_FILE         |  `/etc/rabbitmq/rabbitmq.config`            |
| RABBITMQ_LOG_BASE            |  `/var/log/rabbitmq`                        |
| RABBITMQ_ENABLED_PLUGINS_FILE|  `/etc/rabbitmq/enabled_plugins`            |
| RABBITMQ_MNESIA_BASE         | Database dir. `/var/lib/rabbitmq/mnesia`    |           


~~~sh
cat /var/log/rabbitmq/rabbit@rhel2.log 
~~~
~~~
=INFO REPORT==== 8-May-2024::19:14:50 ===
node           : rabbit@rhel2
home dir       : /var/lib/rabbitmq
config file(s) : /etc/rabbitmq/rabbitmq.config
log            : /var/log/rabbitmq/rabbit@rhel2.log
sasl log       : /var/log/rabbitmq/rabbit@rhel2-sasl.log
database dir   : /var/lib/rabbitmq/mnesia/rabbit@rhel2
~~~

**/etc/rabbitmq/rabbitmq.config**

### Start 
~~~sh
systemctl start rabbitmq-server
~~~

Or

rabbitmq-server -detached

### rabbitmqadmin
Download it from [here](http://host:15672/cli/rabbitmqadmin)

### rabbitmqctl
`rabbitmqctl` is the main command line tool for managing a RabbitMQ server node, together with `rabbitmq-diagnostics` , `rabbitmq-upgrade `

~~~sh
rabbitmqctl [-n <node>] [-q] <command> [<command options>]

Somme Cmmands:

    stop [<pid_file>]
    start_app
	 
    join_cluster <clusternode> [--ram]
    
    add_user <username> <password>
    set_user_tags <username> <tag> ...
    list_users

    add_vhost <vhostpath>
    set_permissions [-p <vhostpath>] <user> <conf> <write> <read>
    
    set_parameter [-p <vhostpath>] <component_name> <name> <value>
    
    list_policies [-p <vhostpath>]

    list_queues [-p <vhostpath>] [<queueinfoitem> ...]
    list_exchanges [-p <vhostpath>] [<exchangeinfoitem> ...]
    list_bindings [-p <vhostpath>] [<bindinginfoitem> ...]
    list_connections [<connectioninfoitem> ...]
    list_channels [<channelinfoitem> ...]
    list_consumers [-p <vhostpath>]
    status
~~~

### Enable Web Console
~~~sh
rabbitmq-plugins enable rabbitmq_management
~~~

http://host:15672

Default Login: guest/guest

### Authentication, Authorisation
- **Add a new User**: admin1
  ~~~sh
  rabbitmqctl add_user admin1 changeit
  rabbitmqctl set_user_tags admin1 administrator
  rabbitmqctl set_permissions -p / admin1 ".*" ".*" ".*"
~~~  

Default user : **guest/guest**

### Virtual Hosts
connections, exchanges, queues, bindings, user permissions, policies  belong to **virtual hosts**. That is the same idea as virtual hosts in apache or  server block in nginx. 

Create a VHost:

rabbitmqctl add_vhost vh1


List :
~~~sh
curl -i -u guest:guest http://localhost:15672/api/vhosts
~~~

### Consoles Screens
![a](/docs/images/rabbitmq-queues.png)

### Code Examples
<a>https://github.com/rabbitmq/rabbitmq-tutorials/
### AMQP
AMQP - Advanced Manager Queue Protocol.
![a](/docs/images/amqp-arch.png)

 AMQP 0-9-1 brokers provide four exchange types:
  - **Direct exchange** - **Empty string**: it routes messages with a routing key equal to the routing key declared by the binding queue
    ~~~~py
    # Python 
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

<<<<<<< HEAD
![a](/docs/images/rabbitmq-queues.png)

### Send a JSON message with Curl
~~~sh
curl -s -u USERNAME:USERPASSWORD -H "Accept: application/json" -H "Content-Type:application/json" -X POST -d'{
    "vhost": "/",
    "name": "amq.direct",
    "properties": {
        "delivery_mode": 2,
        "headers": {}
    },
    "routing_key": "QUEUE_NAME",
    "delivery_mode": "1",
    "payload":"ENCODED_JSON_PAYLOAD",
    "headers": {},
    "props": {},
    "payload_encoding": "string"
}' http://localhost:15672/api/exchanges/%2F/amq.direct/publish
~~~

=======
>>>>>>> cc64ad18e0a218c3325392fa3edfb2014b41ba5b
