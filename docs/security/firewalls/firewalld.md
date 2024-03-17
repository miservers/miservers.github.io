---
layout: default
title: Firewalld
parent:  Firewalls
grand_parent: Security
nav_order: 2
---


## Firewalld 
----------------------------------
Default firewall on CentOS 7.

Stop/Start

	$ systemctl start firewalld

Is firewalld running?

	$ firewall-cmd --state
	running

Defined Firewall Rules: 
> $ firewall-cmd --list-all

> $ firewall-cmd --zone=home --list-all

> $ firewall-cmd --zone=public --list-ports

Open access to HTTP(port 80) service

	$ firewall-cmd --zone=public --permanent  --add-service=http

 	$ firewall-cmd --zone=public --list-services
	
	Output : dhcpv6-client http mdns samba-client ssh

Open a Port on a Zone

	$ firewall-cmd --zone=home --add-port=9990/tcp --permanent 

	$ firewall-cmd --reload

	$ firewall-cmd --zone=home --list-ports
	
	Output: 9990/tcp

Zones: 

	$ firewall-cmd --get-default-zone
	Out: public

Litst of Defined Zones:

	$ firewall-cmd --get-zones
	Out: block dmz drop external home internal public trusted work


Changing the Zone of an Interface

	$ firewall-cmd --zone=home --change-interface=enp0s8 --permanent

	$ firewall-cmd --get-active-zones
	home
  		interfaces: enp0s8
	public
  		interfaces: enp0s3


List of Predefined Services

	$ firewall-cmd --get-services

	... ftp http https ssh ntp ....

See More about a service. eg ssh : **/usr/lib/firewalld/services/ssh.xml**

	<?xml version="1.0" encoding="utf-8"?>
	<service>
  		<short>SSH</short>
	  	<port protocol="tcp" port="22"/>
	</service>
