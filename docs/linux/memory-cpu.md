---
layout: default
title: CPU - Memory
parent: Linux
nav_order: 2
---

### vmstat 
Reference: <a>https://access.redhat.com/solutions/1160343</a>


### Extend Swap
[Reference] 
   (https://www.linuxtechi.com/extend-swap-space-using-swap-file-in-linux/)

This worked fine on ubuntu 20.04

***Steps to extends swap***

**check the swap situation**  

    free -m
    swapon -s

**Create a new swap file**  

    sudo dd if=/dev/zero of=/swapfile2 bs=1G count=1
    sudo chmod 600 /swapfile2

**format the file with swap filesystem format**   

    sudo mkswap /swapfile2

**Add swap file to fstab**  

    sudo nano /etc/fstab

**Activate the new swap file**  

    sudo swapon /swapfile2

**To disable the swapfile**   

    swapoff /swapfile2

