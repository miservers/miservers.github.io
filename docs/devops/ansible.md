---
layout: default
title: Ansible
parent: DevOps
nav_order: 2
---


### Concepts
Playbook: means ansible configuration files. It contains a list of tasks that will be executed on set of specified hosts.

### Inventory (Hosts)
Ansible use inventory file to keep track of the hosts belonging to your infrastructure. Default inventory location is **/etc/ansible/hosts**, but you can any other file and use **-i** option. 

**~/ansible/prod-inventory**
~~~
[appservers]
alma1
alma2
10.2.0.4
~~~

To list an inventory hosts:
~~~sh
ansible-inventory -i prod-inventory --list
~~~

Ping All inventory hosts:
~~~sh
ansible all -i prod-inventory -m ping
~~~

### Execute ad-hoc commands
Syntex: 
~~~sh
ansible [pattern] -m [MODULE] -a {COMMAND_OPTIONS}
~~~

~~~sh
ansible all -m shell -a 'free -m'
ansible localhost -m shell -a 
~~~

### Vagrant 
vagrant is a tool for building and managing VMs. It works on top of a virtualisation provider(vmware, oracle vbox, kvm).

Configuations are defined in **Vagrantfile**:


### Variables
~~~
vars:
  http_port: 8080
  install_dir: /opt/tomcat10
~~~
variables can be refered by "{{var name}}"

### Modules
- **shell**: run shell commands.
- **group**: create a unix group.
- **user**: creates unix users.
- **file**: create files/directories.
- **copy**: copies files.
- **unarchive**: unpack an archive. It can copy the archive from the control machine or download it. 
- **blockinfile**: Insert/update/remove a text block in a file

### Privilege escalation: become
Execute tasks with root privileges.


### Execute a Playbook
~~~sh
ansible-playbook -i prod-inventory tomcat-playbook.yml 
~~~

### Create a Symbolic Link
~~~yml
---
- hosts: testserver
  tasks:
    - name: Create a symlink to the JDK
      file:
        src: /opt/jdk-22
        dest: /opt/jdk
        state: link
~~~

### Insert at the end of File
~~~yml
  tasks:
    - name: Setup the  PATH
      blockinfile:
        path: /home/webadmin/.bash_profile
        insertafter: 'EOF'
        block: |
          export JAVA_HOME=/opt/jdk
          export PATH=$JAVA_HOME/bin:$PATH
~~~


### Documentation
- [freekb](https://www.freekb.net/Articles?tag=Ansible)