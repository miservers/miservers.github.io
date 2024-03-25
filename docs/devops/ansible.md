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
shell: module to run shell commands.
group: module to  create a unix group
user: creates unix users
file: module to create files/directories.
copy: copies files.

### Execute a Playbook
~~~sh
ansible-playbook -i prod-inventory tomcat-playbook.yml 
~~~

### Ansible Playbook to install Tomcat
tomcat-playbook.yml
~~~yml
---
- name: Download Tomcat8 from tomcat.apache.org
  hosts: testserver
  vars:
    download_url: https://dlcdn.apache.org/tomcat/tomcat-8/v8.5.83/bin/apache-tomcat-8.5.83.tar.gz
  tasks:
   - name: Download Open JDK
     become: yes
     apt:
      name: openjdk-8-jre-headless
      update_cache: yes
      state: present
  
   - name: validate if Java is availble 
     shell: 
      java -version
     
   - name: Create the group
     become: yes
     group: 
      name: tomcat
      state: present

   - name: Create the user
     become: yes
     user:
        name: tomcat
        state: present

   - name: Create a Directory /opt/tomcat8
     become: yes
     file:
       path: /opt/tomcat8
       state: directory
       mode: 0755
       owner: tomcat
       group: tomcat

   - name: Download Tomcat using unarchive
     become: yes
     unarchive:
       src: "{{download_url}}"
       dest: /opt/tomcat8
       mode: 0755
       remote_src: yes
       group: tomcat
       owner: tomcat
    
   - name: Move files to the /opt/tomcat8 directory
     become: yes
     become_user: tomcat
     shell: "mv /opt/tomcat8/apache*/* /opt/tomcat8"

   - name: Creating a service file
     become: yes
     copy: 
      content: |-
        [Unit]
        Description=Tomcat Service
        Requires=network.target
        After=network.target

        [Service]
        Type=forking
        User=tomcat
        Environment="CATALINA_PID=/opt/tomcat8/logs/tomcat.pid"
        Environment="CATALINA_BASE=/opt/tomcat8"
        Environment="CATALINA_HOME=/opt/tomcat8"
        Environment="CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC"

        ExecStart=/opt/tomcat8/bin/startup.sh
        ExecStop=/opt/tomcat8/bin/shutdown.sh
        Restart=on-abnormal

        [Install]
        WantedBy=multi-user.target
      dest: /etc/systemd/system/tomcat.service

   - name: Reload the SystemD to re-read configurations
     become: yes
     systemd:
        daemon-reload: yes

   - name: Enable the tomcat service and start
     become: yes
     systemd:
        name: tomcat
        enabled: yes
        state: started

   - name: Connect to Tomcat server on port 8080 and check status 200 - Try 5 times
     tags: test
     uri:
       url: http://localhost:8080
     register: result
     until: "result.status == 200"
     retries: 5
     delay: 10
~~~

