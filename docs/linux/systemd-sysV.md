---
layout: default
title: Systemd - sysV
parent: Linux
nav_order: 6
---

## Systemd

### Getting Started

A Service is defined as **Unit**. Unit files end with **.service**

**Systemd Units Locations**
   
	# man systemd.unit

	System Unit Search Path
       /etc/systemd/system/*
	   /lib/systemd/system/*
		...
	User Unit Search Path
       /etc/systemd/user/*
       ~/.local/share/systemd/user/*
	   ...

**Configuration File**

	/etc/systemd/journald.conf

### Logs

{: .highlight }
**journalctl** is a command to view and manage Systemd logs, wich are stored in binary format under **/var/log/journal**.

~~~shell
$ journalctl -xe    // Display paged Logs with explanation       
$ journalctl -b     // Current Boot Logs                         
$ journalctl -k     // Kernel Logs (like dmesg)                  
$ journalctl -u tomcat                      // By Unit                
$ journalctl -f                             // Tail                    
$ journalctl -b  -u tomcat -o json-pretty   // Display in Json Format 
$ journalctl -p err                         // By Level               
~~~

#### Purge journal logs

~~~shell
$ journalctl --disk-usage
$ sudo journalctl --vacuum-size=200M
~~~

### Systemd Commands

~~~shell
$ systemctl start|status|disable tomcat   //  Control a Service  				
$ systemctl list-unit-files     //  List Unit Files 				  	
$ systemctl list-units          //  List Units
$ systemd-analyze blame         //  List services started on boot ordered by time
$ systemd-analyze time          // Time required to boot the machine   						
~~~	

###  Creating a New Service (Tomcat)

1. Create The Unit : **/etc/systemd/system/tomcat.service**

```sh
	[Unit]
	Description=Tomcat Server
	After=network.target remote-fs.target 
	    
	[Service]
	Type=forking

	Environment=JAVA_HOME=/opt/jdk
	Environment=JAVA_OPTS=-Djava.security.egd=file:///dev/urandom
	Environment=CATALINA_PID=/opt/tomcat-10/temp/tomcat.pid
	Environment=CATALINA_BASE=/opt/tomcat-10
	Environment=CATALINA_HOME=/opt/tomcat-10
	Environment="CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC"

	ExecStart=/opt/tomcat-10/bin/startup.sh
	ExecStop=/opt/tomcat-10/bin/shutdown.sh

	User=webadmin
	Group=webadmin


	[Install]
	WantedBy=multi-user.target
```

2. Verify Unit File Syntax

	sudo systemd-analyze verify tomcat.service

3. Reload Systemd Daemon to tacke into account the new service

	sudo systemctl daemon-reload

4. Enable the Service

	sudo systemctl enable tomcat

5. Start the Service

	sudo systemctl start tomcat

5.1 Check The Logs

	journalctl -xe

6. the Status of the Service 

	sudo systemctl status tomcat

Other Commands:

	sudo systemctl reenable tomcat.service

	sudo systemctl list-units



### Documentation
- https://www.freedesktop.org/software/systemd/man/systemd.service.html


## SysV
Liste of all enabled services(sysV, level 4)  
    $ ll /etc/rc4.d

Enable/Disable a service (System V)  
    $ update-rc.d mysql enable|disable
  
Enable will create a symlink in /etc/rc4.d/S02mysql -> ../init.d/mysql

