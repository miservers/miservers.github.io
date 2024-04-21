---
layout: default
title: Vagrant
parent: DevOps
nav_order: 5
---

### Concepts
Vagrant is a tool for building and managing VMs. It works on top of a virtualisation provider(vmware, oracle vbox, kvm). Configuations are defined in **Vagrantfile**:

  - **Box** : boxes are virtual machine images.

![a](/docs/images/vagrant-concepts.png)

### Vagrant Commands

| Command                            | Description                            |
|:-----------------------------------|:---------------------------------------|
| `vagrant box add generic/rhel7`    | Install a box(optional)                |
| `vagrant box list`                 | List of installed boxes                |
| `vagrant box remove box_name`      | Remove a Box image                     |
| `vagrant ssh`                      | Access a box via ssh                   |




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


### Remote SSH Access to a VM
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

### Disk Size
Install plugin:
~~~sh
vagrant plugin install vagrant-disksize
~~~

Edit Vagrant file:
~~~ruby
Vagrant.configure("2") do |config|
  ... 
  config.vm.disk :disk, size: "150GB", primary: true

~~~

### Vagrantfile
Explanations:
- **Vagrant.configure(“2”)**: Vagrant will use version 2 of the configuration object. 

Example:
~~~ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    
  config.vm.define "rhel1" do |rhel1|
    rhel1.vm.box = "generic/rhel7"
    rhel1.vm.hostname = "rhel1"

    rhel1.vm.box_check_update = false

    rhel1.vm.network "private_network", ip: "192.168.56.21"
    rhel1.vm.network "public_network", bridge: "wlp3s0"

    rhel1.vm.disk :disk, size: "150GB", primary: true

    rhel1.vm.provider "virtualbox" do |vb|
      vb.memory = "3072"
     vb.cpus = 2
    end
  end

  config.vm.define "rhel2" do |rhel2|
    rhel2.vm.box = "generic/rhel7"
    rhel2.vm.hostname = "rhel2"

    rhel2.vm.box_check_update = false

    rhel2.vm.network "private_network", ip: "192.168.56.22"
    rhel2.vm.network "public_network", bridge: "wlp3s0"

    rhel2.vm.disk :disk, size: "150GB", primary: true

    rhel2.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
     vb.cpus = 2
    end
  end
end
~~~
