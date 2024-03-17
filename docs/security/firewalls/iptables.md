---
layout: default
title: Iptables
parent:  Firewalls
grand_parent: Security
nav_order: 3
---


## Iptables
----------------------------------
Current Rules:
> $ iptables -L

Add a Rule
> $ iptables -A INPUT -p tcp --dport ssh -j ACCEPT

Delete a Rule:
> $ iptables -L --line-numbers

> $ iptables -D INPUT 1
