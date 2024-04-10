---
layout: default
title: Roles
parent:  Ansible
grand_parent: DevOps
nav_order: 2
---

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

