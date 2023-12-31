---
layout: default
title: KVM
parent: Linux
nav_order: 10
---

- Host: ubuntu 22.04
- Guest: centos 7

### Architecture
![alt](/docs/images/Open-source-virtualization-stack.webp)

### Installation of KVM

Packages:

	sudo apt-get install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils

Check virtualisation

	$ kvm-ok

	INFO: /dev/kvm exists
	KVM acceleration can be used

Adding your username to libvirtd group

	$ sudo usermod -aG kvm $USER
	$ sudo usermod -aG libvirt $USER
	$ sudo usermod -aG libvirt-qemu $USER
	

Verify Installation

	$ sudo virsh list --all

**Virtiual Machine Manager**: GUI

	sudo apt-get install virt-manager

After the installation, **you need to relogin**

### Creating VMs

3 ways:

1. virt-manager: a GUI tool
2. virt-install, a python script developed by Red Hat
3. ubuntu-vm-builder, developed by Canonical.

List supported os variant 

	$ virt-install --osinfo list

:warning: Put the iso file in a directory readable by user qemu. For exemple /tmp 

Edit /etc/libvirt/qemu.conf : resolve permission denied problems 

	user = "jadmin"
	group = "libvirt"

and Restart libvirtd

	sudo systemctl restart libvirtd


### Virtual Machine Manager
Practical tool to manage your VMs: create, delete, start, stop, clone,etc

![](/docs/images/linux-kvm-virt-manager.png)

### Creating VMs using virt-install

	$ virt-install \
		  --name centos1 \
		  --memory 512 \
		  --vcpus 1 \
		  --disk size=6 \
		  --disk path=/media/jadmin/Data21/vms-kvm/centos1.img,size=4 \
		  --cdrom /tmp/CentOS-7-x86_64-Minimal-2009.iso \
		  --os-variant centos7

### Start/Stop VMs by Command Line

List of VMs

	$ virsh list --all  

	Id   Name      State
	2    centos1   running
	-    vm1       shut off

Start a VM
	
	$ virsh start centos1

Stop a VM

	$ virsh shutdown centos1


### Linux Bridge

![alt](/docs/images/linux-bridge.drawio.png)

### Create a Bridge
Using **netui**. netui stand for Network Manager text User Inteface.

	$ sudo netui

![alt](/docs/images/linux-bridge-netui1.png)

Choose [Add], and [Bridge]

![alt](/docs/images/linux-bridge-netui2.png)

	$ ip a 

	br0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
    link/ether d2:58:93:2c:82:10 brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.254/24 brd 192.168.122.255 ....

### Connect the Guest to the Bridge

If the Guest is a Centos 7/ redhat

	$ cat /etc/sysconfig/network-scripts/ifcfg-eth0
		TYPE=Ethernet
		BOOTPROTO=dhcp
		NAME=eth0
		UUID=599b4ccc-12f4-45cf-ab8f-915dc8db7a5b
		DEVICE=eth0
		ONBOOT=yes
		BRIDGE=virbr0
		NETBOOT=no
		NM_CONTROLLED=no

{: .warning }
if BRIDGE is set, NM_CONTROLLED must be set to no.

retart NM (Network Manager)

	$ systemctl restart network

