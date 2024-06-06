---
layout: default
title: ELK
parent: Middleware
nav_order: 13
---

## ELK
**ELK** : is a short of three open sources: Elasticsearch, Logstash, and Kibana. 

## Start/stop
~~~sh
systemctl  start elasticsearch.service 
systemctl  start logstash.service
systemctl  start kibana.service 
~~~

## Configuration
### Elastic search
**/etc/elasticsearch/elasticsearch.yml**
~~~
network.host: <IP>
http.port: 9200
~~~

**/etc/elasticsearch/jvm.options**
~~~
-Xms2g
-Xmx2g
~~~

### Test if elastic started
~~~sh
curl -X GET "IP:9200"
~~~

### Logstash

### Kibana
**/etc/kibana/kibana.yml**
~~~py
server.port: 5601
server.host: "IP"

elasticsearch.url: "http://IP:9200"
~~~

### Console Kibana
<a>http://IP:5601</a>

![a](/docs/images/elk-kibana-home.png)