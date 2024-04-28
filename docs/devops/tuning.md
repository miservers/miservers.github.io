---
layout: default
title: Performances Tuning
parent: DevOps
nav_order: 10
---

## Web Stress Tools
-------------------------------
### JMeter

### Apache Bench: ab
~~~sh
ab -c 100 -n 5000 -r http://rhel3:9010/students
~~~
- c: 100 simultanuously concurrent requests
- n: total nb of requets
- r: don't fail when fail 

### Neoload
### OpenSta