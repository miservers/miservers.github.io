---
layout: default
title: Networking
parent: Linux
nav_order: 5
---


**Env. Ubuntu 20.04, Centos 7**

## Memos
Wich IP is pinging me?

	$ tcpdump -n -i enp0s8 icmp and icmp[icmptype]=icmp-echo

## Network Manager
### Configure a Static IP
List all net devices: **nmcli**

	$ nmcli d
	
	DEVICE  TYPE      STATE      CONNECTION 
	eth0    ethernet  connected  eth0       
	lo      loopback  unmanaged  --     

* Edit **/etc/sysconfig/network-scripts/ifcfg-eth0** 

![](/docs/images/linux-static-ip.png)

* Or use **nmtui**  
	
	$ nmtui

![](/docs/images/linux-nmtui-edit.png)

Restart NM

	$ systemctl restart network


## IP
### IP vs Ifconfig
IP is a replacement for ifconfig command. IP command is orginazed on two layers: Link Layer(**ip link**), IP Layer(**ip a**).

Dispalay all NICs   
    
    $ ifconfig                                 
    $ ip a                                        

Add IP address     

    $ ifconfig eth0 add 192.168.43.17          
    $ ip a add 192.168.43.17 dev eth0              


Set MAC            

    $ ifconfig eth0 hw ether ae:09:29:13:43:a3 
    $ ip link set dev eth0 address ae:09:29:13:43:a3

Set MTU            

    $ ifconfig eth0 mtu 1800                   
    $ ip link set dev eth0 mtu 1800                 

Set promiscous     
    
    $ ifconfig eth0 promisc                    
    $ ip link set dev eth0 promisc on               

Enable/Disable NIC 
    
    $ ifconfig eth0 [up down]                  
    $ ip link set eth0 [up dow]                      


### Routing Table
Routing table explained: https://geek-university.com/ccna/routing-table-explained

    # route -n
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    0.0.0.0         10.98.56.1      0.0.0.0         UG    100    0        0 enp0s3
    170.56.2.0      10.2.0.1        255.255.255.0   U     100    0        0 enp0s3
    168.254.0.0     0.0.0.0         255.255.0.0     U     1000   0        0 enp0s8

Send to "10.2.0.1"(Gateway) all packets that are destinated to the network 170.56.2.0(from 170.56.2.0 to 
170.56.2.254) by passing by interface enp0s3.

**Default route**: dest=0.0.0.0 and mask=0.0.0.0. route for all packets that don't have a specified route 
in routing table. We use the default route for Internet.

Delete a route:

    # route del default

Add default route

    # route add default gw 10.98.56.1 dev enp0s3


Open connections
	
	netstat -np | grep 8080
	lsof -nPp 2552257 | grep 8080     ; -P : for numerique ports 


### Linux Bridge and Tap

![](/docs/images/Linux-Virtual-Network-Bridge.png)


### TCPDUMP

	tcpdump -v -A -s 0  port 8080 and host 192.168.1.1  -w capt.log   
	
### Wireshark
	use Wireshark to read capt.log
	 
	 

 
