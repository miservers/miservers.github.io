---
layout: default
title: Nagios
parent: DevOps
nav_order: 4
has_toc: true
---


## Getting Started 
### Nagios Architecture
![alt](/docs/images/nagios-agents-transport.png)

![alt](/docs/images/nagios-architecture.png)

Nagios remotes alert messages to administrators defined in its configuration files, through sms, emails,... It also continuously updates its web console.

Nagios sends a signal through a process scheduler to run the plugins on the local/remote servers.

### Plugins
A plugin is a script used to test a service. Plugins are installed on the remote servers you want to monitor:
  - Return state code : 0=OK, 1=WARNING, 2=CRITICAL et 3=UNKNOW
  - Return a information message
  - Run: ./check_xxx!param1!param2!...!paramx

### NRPE
NRPE-Nagios Remote Plugin Executor, allows to execute plugins on remote servers.

![alt](/docs/images/nagios-nrpe.png)


## Config files and Arbo

**Nagios server**  
 - Config file: /usr/local/nagios/etc/nagios.cfg  

**NRPE Server**  
   - Config file: /etc/nagios/nrpe.cfg  
   - Listening port: 5666  

  
## Monitoring a Linux Remote Host
Use case: 
- front-1(10.2.0.5): Nagios Server. RHEL/Almalinux 9
- alma1(10.2.0.2): Host we want to monitor. RHEL/Almalinux 9.

#### Monitored Host

Install **nagios plugins** and **nrpe** daemon.


Personalize nrep config **/etc/nagios/nrpe.cfg**
  - Add nagios server to allowed hosts  
    > allowed_hosts=127.0.0.1, 192.168.43.80  
  - Config commands  
    ```
    command[check_users]=/usr/lib/nagios/plugins/check_users -w 5 -c 10                       
    command[check_load]=/usr/lib/nagios/plugins/check_load -r -w .15,.10,.05 -c .30,.25,.20   
    command[check_hda1]=/usr/lib/nagios/plugins/check_disk -w 20% -c 10% -p /dev/hda1         
    command[check_zombie_procs]=/usr/lib/nagios/plugins/check_procs -w 5 -c 10 -s Z           
    command[check_total_procs]=/usr/lib/nagios/plugins/check_procs -w 150 -c 200
    ```

Restart nrpe server
  > sudo /etc/init.d/nagios-nrpe-server restart
  
#### Nagios Server
- test nrpe connectivity
  > $ /usr/lib/nagios/plugins/check_nrpe -H 192.168.43.1
- Edit file **/usr/local/nagios/etc/nagios.cfg**
  > cfg_dir=/usr/local/nagios/etc/servers
- add command check_nrpe in **/usr/local/nagios/etc/objects/commands.cfg**  
  ```
  define command{
        command_name check_nrpe
        command_line /usr/lib/nagios/plugins/check_nrpe -H $HOSTADDRESS$ -c $ARG1$
  }
  ```
- create config file to monitor the host
  > nano /usr/local/nagios/etc/servers/redmi-ubuntu.cfg
  ```
  define host {                                                                             
        use linux-server                                                                  
        host_name redmi-ubuntu                                                            
        address 192.168.43.1                                                              
        register 1                                                                        
  }        
  
  define service{                                                                           
      host_name redmi-ubuntu                                                              
      service_description PING                                                            
      check_command check_ping!100,20%!500,60%                                        
      max_check_attempts 2                                                                
      check_interval 2                                                                    
      retry_interval 2                                                                    
      check_period 24x7                                                                   
      check_freshness 1                                                                   
      contact_groups admins                                                               
      notification_interval 2                                                             
      notification_period 24x7                                                            
      notifications_enabled 1                                                             
      register 1                                                                          
  }
  ```
  check_ping est defined in **commands.cfg**   
  **!**: is parametrer separator. warning if rta>100ms or packet lost=m>20%. critical alert if 
  rta>500ms or pl>60%.
- check manually a remote command(defined in **nrpe. cfg**)  
  > $ /usr/lib/nagios/plugins/check_nrpe -H 192.168.43.1 -c check_load  
  > $ /usr/lib/nagios/plugins/check_nrpe -H 192.168.43.1 -c check_total_procs
- restart nagios
  > sudo service nagios restart
- verify on nagios console
  http://localhost/nagios/

##  Graphs
https://support.nagios.com/kb/category.php?id=153  

### PNP4Nagios
ref:  
  https://support.nagios.com/kb/article/nagios-core-performance-graphs-using-pnp4nagios-801.html  
  http://docs.pnp4nagios.org/start  
  

install deps
> sudo  apt install rrdtool  php-gd php-xml php7.2-xml

download from https://github.com/lingej/pnp4nagios 

compile sources

config nagios    
use Bulk NPCD

test installation  
http://localhost/pnp4nagios/

remove file : /usr/local/pnp4nagios/share/install.php


### Nagiosgraph
Ref: https://sourceforge.net/p/nagiosgraph/wiki/Home/

FORGET IT. not working, no longer mintained since 2010

### MRTG
graphs for routers    
doc: https://oss.oetiker.ch/mrtg/  




#### requirements
> $ sudo apt install gcc perl libgd-dev libpng-dev zlib1g-dev

##  Installating Nagios

OS: Ubuntu 18.04 

Good doc: https://tecadmin.net/monitor-remote-linux-host-using-nagios/

### see Official QuickStart

https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/quickstart.html

En résumé, you must

- On Nagios server,

  - install apache/php and dependancy packages

  - donwload and compile nagios core

  - Install this package

    > sudo apt install nagios-nrpe-plugin

- On monitored hosts, install NRPE and nagios plugins packages

  > sudo apt install nagios-nrpe-server nagios-plugins 

## Docs
Official docs: https://support.nagios.com/kb/article/nagios-core-graphing-performance-info-with-mrtg-399.html



