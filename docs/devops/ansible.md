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
ansible [pattern] -m [MODULE] -a {COMMAND OPTIONS}
~~~

Examples:
~~~sh
ansible all -m shell -a 'free -m'
~~~

### Vagrant 
vagrant is a tool for building and managing VMs. It works on top of a virtualisation provider(vmware, oracle vbox, kvm).

Configuations are defined in **Vagrantfile**:


### Variables
~~~
vars:
  http_port: 8080
  install_dir: /opt/tomcat
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

### Create a User
~~~yml
- name: Create webadmin user
      user:
        name: webadmin
        password: $5$YQXOijrsiwvkIEMJ$SmB42.jlkrOyg0G/QArrHxV6rqzL3p2
        group: web
        state: present
~~~

Password id Genretated with:
~~~sh
mkpasswd --method=sha-256 changeit
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

### Templates
Template are proccessed by [Jinja2 template language](http://jinja.pocoo.org/docs/)

Example of template personalising tomcat http port:
1. Define vars:
~~~yaml
vars:
    tomcat_http_port: 8180
    catalina_home: /opt/tomcat
~~~

2. Copy server.xml into  templates/server.xml.j2 and edit it:
~~~xml
<Connector port="{{ tomcat_http_port }}" protocol="HTTP/1.1"
               connectionTimeout="20000"
~~~

3. Create task
~~~yaml
- name: Apply server.xml Template
     template:
       src: templates/server.xml.j2
       dest: "{{catalina_home}}/conf/server.xml"
~~~

4. Apply the playbook
~~~sh
ansible-playbook -i ../prod-inventory playbook.yml
~~~

### Roles
Roles let you automatically load related vars, files, tasks, handlers, and other Ansible artifacts based on a known file structure. 

Steps to create a role tomcat:

1. Initiliaze  the Role Structutre

~~~sh
# ansible-galaxy role init tomcat
~~~
~~~sh
# tree tomcat
tomcat
├── defaults          
│   └── main.yml    # default lower priority variables for this role      
├── files           # files to copy, scripts to run
├── handlers          
│   └── main.yml     
├── meta
│   └── main.yml     # role dependencies
├── tasks
│   └── main.yml      
├── templates
├── tests
│   ├── inventory
│   └── test.yml
└── vars
    └── main.yml       # variables associated with this role
~~~
3. Create a playbook using this role : tomcat-playbook.yaml

~~~yaml
- name: Install Tomcat
  hosts: appservers
  gather_facts: yes
  #become: no

  tasks:
    - name: installing tomcat using role
      import_role:
        name: tomcat
~~~

2. Execute the playbook
~~~sh
# ansible-playbook -i prod-inventory tomcat-playbook.yaml
~~~


### Documentation
- [freekb](https://www.freekb.net/Articles?tag=Ansible)
- [playbooks best practices](https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html)
- [Templates For Tomcat](https://github.com/mitre/ansible-cis-tomcat-hardening)

