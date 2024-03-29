---
layout: default
title: Logs
parent:  Tomcat
grand_parent: Middleware
nav_order: 4
---

### Logs Rotation
Install Package  

	apt install logrotate

Configuration: Create a file **/etc/logrotate.d/tomcat** with content:t

	/opt/tomcat-10/logs/catalina.* {
		daily
    	dateext   
    	copytruncate
    	missingok
    	rotate 14
    	compress
	}
	
copytruncate : truncate the original file after coping it. This allow rotating logs with Tomcat running.

missingok: Don't issue a message error if log file is missing.

Cron daemon launch daily logrotate.

	$ ls /etc/cron.daily/
	logrotate
`

Check Config

	logrotate -d /etc/logrotate.d/tomcat
	
Run logrotate in verbose mode to Test or to Debug problems 
	
	/usr/sbin/logrotate -v /etc/logrotate.conff

### Logs
**JULI** is the default logging librairy. JULI is an improved implementation of java.util.logging API. Because default implementation of java.logging API has many limitations, for example it is'nt possible to have a per-web application logging.

JULI is enabled by default. Logging can be configured:
  - Globally. in <ins>${catalina.base}/conf/logging.properties</ins> 
  - Per-web application. <ins>WEB-INF/classes/logging.properties</ins>


