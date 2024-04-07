---
layout: default
title: Vagrant
parent: DevOps
nav_order: 5
---

### Concepts
**Vagrant** enables users to create and configure lightweight, reproducible, and portable development environments(VMs).

### Installation
Install VirtualBox
~~~sh
sudo apt install virtualbox -y
~~~

Install Latest version : Vagrant 2.4
~~~sh
curl -O https://releases.hashicorp.com/vagrant/2.4.1/vagrant_2.4.1-1_amd64.deb

sudo dpkg -i vagrant_2.4.1-1_amd64.deb 
~~~

### VirtualBox Configurations
- Set the **Default Machine Folder**: Directory where the VMs will be created
  - <a>VirtualBox > Preferences > General </a>


### Creating a Box (VM)
For centos7 Box:
~~~sh
mkdir ~/vagrant_vms/centos2
cd  ~/vagrant_vms/centos2
~~~

Initialize the centos Box
~~~sh
vagrant init centos/7
~~~

This Create the **Vagrantfile**. So Adapt it!!. See Example Below

Start The VM:
~~~sh
vagrant up
~~~


### Connecting to the VM via SSH
Localy ssh access using vagrant:
~~~sh
$ vagrant ssh
~~~

~~~
$ vagrant ssh-config
~~~

And add the output to **~/.ssh/config**, after adapting it
~~~
Host centos2
  HostName 127.0.0.1
  User vagrant
  Port 2222
  UserKnownHostsFile /dev/null
  ....
~~~

Now you can localy ssh the VM, without Vagrant:
~~~
$ ssh centos2
~~~

### Remote SSH Access
Generate the SSH Keys:
~~~sh
$ vagrant ssh
[vagrant@centos2 ~]$ ssh-keygen
~~~

Activate ssh password authentication option:
~~~sh
[vagrant@centos2 ~]$ sudo vi /etc/ssh/sshd_config
....
PasswordAuthentication yes
....
~~~

Restart SSHD service
~~~sh
[vagrant@centos2 ~]$ sudo systemctl restart sshd
~~~

Change the **vagrant** user password:
~~~sh
[vagrant@centos2 ~]$ sudo passwd  vagrant
~~~

### Vagrantfile
Explanations:
- **Vagrant.configure(“2”)**: Vagrant will use version 2 of the configuration object. 


Example:
~~~ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.vm.hostname = "centos2"


  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.56.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
   config.vm.network "public_network"

   config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
     vb.memory = "1024"
     vb.cpus = 2
   end
  #
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end
~~~