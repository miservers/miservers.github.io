---
layout: default
title: UFW
parent:  Firewalls
grand_parent: Security
nav_order: 2
---


## ufw
----------------------------------
ufw is a frontend tool uppon iptables. It aims to simplify the  complicated  iptables rules. 

ufw is the default firewall for ubuntu 20.04

Is Firewall Actif:
> $ ufw status

Enable/Start the Firewall:
> $ ufw enable

Allow Incoming on 80 port: 
> $ ufw allow 80/tcp

List of Defined Rules:
> $ ufw status verbose

Delete a Rule:
> $ ufw status numbered

> $ ufw delete 1

Activate Journalisation:
> $ ufw logging on

