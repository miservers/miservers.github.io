---
layout: default
title: Elastic Search
parent: DevOps
nav_order: 6
has_toc: true
---

## Filebeat
**Test config**
~~~sh
filebeat test output -c filebeat-apache.yml
filebeat test config -c filebeat-apache.yml
~~~

**Multiline**
~~~yaml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/myapp/*.log
    multiline.pattern: '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'  # Pattern pour détecter le début d'une nouvelle entrée de log
    multiline.negate: true
    multiline.match: after
    multiline.max_lines: 100
~~~

Entry Example:
~~~log
2024-11-01 12:00:01,456 ERROR Error occurred
Stack trace:
    at MyApp.Program.Main(String[] args) in /path/to/Program.cs:line 10
    at java.io.sys....
~~~

## Kibana

## Logstash
**Piplines**
List of pipelines defined here: **config/pipelines.yml**
~~~yml
 - pipeline.id: apache
   queue.type: persisted
   path.config: "/opt/app/logstash/pipeline_conf/apache.config"
~~~

**Log Apache**
~~~yml
filter {
  grok {
    match => { "message" => "%{COMBINEDAPACHELOG}"}
  }
}
~~~

## Elastic