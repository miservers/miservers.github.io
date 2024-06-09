---
layout: default
title: Elastic search
parent: Middleware
nav_order: 13
---

## ELK
**ELK** : is a short of three open sources: Elasticsearch, Logstash, and Kibana. 
![a](/docs/images/elastic-architecture.jpg)

{: .warning }
Install ELK stack products on the same version

## Start/stop
~~~sh
systemctl  start elasticsearch 
systemctl  start logstash
systemctl  start filebeat 
systemctl  start kibana 
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

**Test if elastic started** : http://rhel1:9200/

### Logstash
Logstash is an open-source data processing pipeline that ingests data from multiple sources, transforms it, and then sends it to one or more destinations.

Check syntax
~~~
/usr/share/logstash/bin/logstash --path.settings /etc/logstash -t
~~~

Start logstash
~~~
# systemctl start logstash
# sysd did not work for me, below works
/usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/apache_logs.conf
~~~

Check logstatch config
~~~sh
/usr/share/logstash/bin/logstash --config.test_and_exit -f <path_to_config_file>
~~~

### Kibana
**/etc/kibana/kibana.yml**
~~~py
server.port: 5601
server.host: "IP"

kibana.index: ".kibana"

elasticsearch.url: "http://IP:9200"
~~~

### Console Kibana
<a>http://IP:5601</a>

![a](/docs/images/elk-kibana-home.png)

### Filebeat
Installed as an agent on your servers, it monitors the log files, collects log events, and forwards them either to Elasticsearch or Logstash for indexing. 

**Install Filebeat**: Kibana Home -> Add Log Data -> Apache Logs, or System Logs or Others and follow instructions

**/etc/filebeat/filebeat.yml** 
~~~yaml
filebeat.inputs:

- type: log

  enabled: true
  paths:
    - /var/log/httpd/*_log
  fields:
    level: debug
    review: 1
  
  filebeat.config.modules:
  path: ${path.config}/modules.d/*.yml
setup.kibana:
  host: "rhel1:5601"
#output.logstash:
  # The Logstash hosts
  #hosts: ["rhel1:5044"]
output.logstash:
  hosts: ["rhel1:5044"]
~~~

**Enable Module Apache**
~~~sh
filebeat modules enable apache2
~~~

If you use a custom log format, update this file: `/usr/share/filebeat/module/apache2/access/ingest/default.json`


**Setup and Start**
~~~sh
filebeat setup -e
service filebeat start
~~~

**Test Filebeat conf**
~~~sh
filebeat test output
~~~

### Index
- an **index** is a collection of documents that have similar characteristics. 
- **Mapping**, is the process of defining how a document and its fields are stored and indexed. It is like the schema definition in a relational database. 

Command `filebeat setup` automaticaly create index

List Of indexes:
~~~
GET /_cat/indices?v
~~~

Create an Index: apache_log
~~~

~~~


