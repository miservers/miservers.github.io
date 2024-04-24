---
layout: default
title: Roles
parent:  Ansible
grand_parent: DevOps
nav_order: 2
---

### Roles
Roles provide a well-defined framework and structure for setting your tasks, variables, handlers, metadata, templates, and other files. 

Steps to create a role tomcat:

### Role Structutre

**Initiliaze  the role structure**
~~~sh
# ansible-galaxy role init tomcat
~~~

**Role Structure**
~~~sh
# tree tomcat
tomcat
├── defaults          
│   └── main.yml    # default lower priority variables for this role      
├── files           # Contains static and custom files that the role uses to perform various tasks.
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

### Use a Role
Create a playbook using this role : tomcat-playbook.yaml

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



Other Syntax to Call a Role:

~~~yaml
---
- name:                    Install Tomcat
  hosts:                   appservers
  become:                  true
  roles:
    - roles/tomcat
~~~


**Execute the playbook**

~~~sh
# ansible-playbook -i prod-inventory tomcat-playbook.yaml
~~~

### Role Files
~~~yaml
- name: Copy index.html to the Nginx directory
  copy:
    src: files/index.html
    dest: "{{ nginx_custom_directory }}/index.html"
  notify: Restart the Nginx service
 ~~~