---
layout: default
title: Linux
parent: Linux
nav_order: 1
---

## Commands Table
--------------------------------------------------

Shortcuts:
```
  ctrl+]                  : Quit telnet
  ctrl+r                  : search in bach history
```
Commands:

| Command                                            | Description                               | 
| -------------------------------------------------- | ----------------------------------------- |
| dd if=/dev/zero of=disk.img bs=512 count=2000      | create a virtual disk of 1MB              |
| xxd -s 1024 -l 512 disk.img                        | read 512 bytes starting at 1024 byte      |
| sed -i 's/foo/bar/g' devices.h                     | replace in same file (-i option)          |
| find . -name "*.xml" -exec grep -H toto {} \;      | Find-grep(option **H** to display fname)  |
| find . -name "*.h" \| xargs sed -i 's/foo/bar/g';  |                                           |
| find . -name "*.h" -exec sed -i 's/foo/bar/g' {} \;|                                           |
| find . -type f -size +10000k -mtime +60            | files>10Mo, modif date>60 days            |
| grep -nr semaphore --include=*.c .                 |                                           |
| grep error \*\*/\*.log                             | search word in current and sub dirs       | 
| grep -c my.log                                     | count word in file                        | 
| zgrep  my.log.gz                                   | search word in zip file                   | 
| du -d 1 -m .                                       | maxdepth=1, practical                     |
| du -sh *                                           | disk usage grouped by directory           |
| du  -am . \|sort -nr \| head -10                   | list of 10 biggest files                  |
| du -h /var/log \| sort -hr \| head -n 10           | list of 10 biggest Directories            |
| df -m                                              | FS disk usage                             |
| zmore                                              | more of a zipped file                     |
| dos2unix                                           | convert file from dos to unix format      |
| uptime                                             | Last boot                                 |
| mkdir -p roles/apache/{files,templates,tasks}      | create multiple sudir                     |
| tree roles                                         | tree of a directory                       |
| ls -lrt                                            | sort by time modif                        |
| ls -lrS                                            | sort by size                              |
| vimdiff fic1.txt fic2.txt                          |                                           |
| diff fic1.txt fic2.txt                             | 16c16(line first fic+c:change+second fic) |
| stat  test.txt                                     | date creation/modif of a file             |
| $?                                                 | Status de la derniere commande            |
| which cmd_alias                                    | command behind alias                      |
|cmd  2>/dev/null                                    | suppress error message in bash            |
|sudo lsof -iTCP -sTCP:LISTEN                        | wich processing is using a port?          |

## Linux Admin
--------------------------------------------------
### Max number of open file descriptors 
~~~sh
# lsof -u <username> | wc -l
    
# su - <username>
# ulimit -Hn    
~~~

~~~sh
# vi /etc/security/limits.conf	
	tomcat            soft    nofile          65535
	tomcat            hard    nofile          65535
	tomcat            soft    nproc           65535
	tomcat            hard    nproc           65535
~~~

~~~sh
# vi /etc/security/limits.d/90-nproc.conf
	*          soft    nproc     10000
	root       soft    nproc     unlimited
~~~
**Stress tests(ab)**  
Run 100000 requests, 100 ones at time:    

    ab -n 100000 -c 100 http://localhost:8080/
	

**Run command in backgroud**

    nohup command > /dev/null 2>&1 &
	nohup sh -c standalone.sh -c clustered.xml > /dev/null 2>&1 &

**Recover deleted file(currently used by a process)**
 
    nohup tail -c +0 -f /proc/8827/fd/120 > catalina.out&
	

**Genarate a random password**

    openssl rand -base64 32
	
**SSH Tunnel**: Port forwarding to access a remote HTTP port using a ssh tunnel
~~~sh
ssh -L 8080:127.0.0.1:8080 sammy@your_server_ip
~~~

## Redhat RHEL 9
--------------------------
### Red Hat Labs Registration Assistant
Online assistant to register a redhat subscription: https://access.redhat.com/labs/registrationassistant/

### Register and automatically Subscribe
~~~sh
subscription-manager register --username <username> --password <password> --auto-attach
~~~

## Crontab
--------------------------
Create/Edit a job evry 5 minutes:  

	$ crontab -e

	5 * * * * ~/magOS.wiki/commit.sh

List of current user jobs:

	$ crontab  -l
	


## Performances

### SAR

```sh
apt install sysstat
vi /etc/default/sysstat

Cron:  /etc/cron.d/sysstat
Logs :  /var/log/sa/

/etc/init.d/sysstat restart

sar -u   ; CPU
sar -b   ; disque IO
sar -r   ; memory
sar -W   ; swap
sar -d   ; IO par dique 
sar -A   ; All

sar -f /var/log/sa/sa15

```

### net-tools 
this package contains utilities like arp, ifconfig, netstat, rarp, nameif and route.


## SSH

- Install on CentOS
```
  # yum -y install openssh-server openssh-clients
  # service sshd start
  # vi /etc/sysconfig/iptables 
     -A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
     If you want to restict access to 192.168.1.0/24:
     -A RH-Firewall-1-INPUT -s 192.168.1.0/24 -m state --state NEW -p tcp --dport 22 -j ACCEPT
  # service iptables restart
  # vi /etc/ssh/sshd_config 
  # service sshd restart
```

- SSH by root: Permission denied
```
  # edit /etc/ssh/sshd_config
  FROM:
  PermitRootLogin prohibit-password
  TO:
  PermitRootLogin yes
   
  # sudo sed -i 's/prohibit-password/yes/' /etc/ssh/sshd_config
  # sudo systemctl restart sshd
```

## VI Quick reference

| Command               | Description            | 
|:----------------------|:-----------------------|
| :%s/TOMCAT/JBOSS/g    | Substitute Strings     |
| :! ./% arg1           | Execute edited script  |
| :! ls -l              | Execute a commande     |
| Ctrl+f, Ctrl+b        | Move Screen Forward/Backword|           
| shift+g               | move the cursor to endfile  |
| $, 0                  | move cursor end/beginning of line|
| :n                    | go to line n           |




## NFS
NFS Server : CentOS 7  
NFS Client : Ubuntu 20.04  

**NFS Server Configuration**  

Install the NFS Server

	$ yum install nfs-utils nfs-utils-lib

Enable Service

	$ systemctl enable --now rpcbind
	$ systemctl enable --now nfs

Edit **/etc/exports** 

	/opt       192.168.56.1(rw,sync,no_root_squash)

Apply 

	$ exportfs -a

Show exports

	showmount -e

For testing???

	systemctl stop firewalld

**NFS Client**

	$ apt install nfs-common
	
	$ mkdir /mnt/centos2_opt
	$ mount centos2:/opt /mnt/centos2_opt




	

## Miscs

APT with Proxy

    vi /etc/apt/apt.conf.d/proxy
    Acquire::http::Proxy "http://proxy-ip:8080";


Enable Root to connect via ssh

    sed -i 's/prohibit-password/yes/' /etc/ssh/sshd_config

**Base64**
> Base64 encoding is a common method for representing binary data in ASCII string format.
> 
> `echo -n "to be hidden" | base64`
>
> To Reverse: ` echo dG8gYmUgaGlkZGVu | base64 -d`
>


**cUrl**
> `curl -k -v -H "Content-Type: application/json"  -X POST -d @auth_req.json https://localhost:9443/carbon/admin/login.jsp`

auth_req.json 
```json
{ 
   "username": "admin",
   "password": "admin"
}
```


